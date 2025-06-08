#!/usr/bin/env python3

import os
import sys

def fix_actual_cancellation(filename):
    """Fix the actual cancellation patterns found in useCards.ts"""
    
    if not os.path.exists(filename):
        print(f"Error: {filename} not found")
        return False
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix the first cancellation check (before API call)
    old_first_check = '''      if ((window as any).currentSearchId !== searchId) {
        console.log('🚫 PAGINATED SEARCH CANCELLED:', searchId.toFixed(3));
        return;
      }'''

    new_first_check = '''      // Enhanced cancellation check - preserve sort-triggered searches
      const isSortTriggered = (window as any).lastSortChangeTime && 
                             (Date.now() - (window as any).lastSortChangeTime) < 5000;
      
      if ((window as any).currentSearchId !== searchId) {
        // Don't cancel sort-triggered searches
        if (isSortTriggered) {
          console.log('🎯 CONTINUING SORT-TRIGGERED SEARCH despite ID change:', searchId.toFixed(3));
        } else {
          console.log('🚫 PAGINATED SEARCH CANCELLED:', searchId.toFixed(3));
          return;
        }
      }'''

    if old_first_check in content:
        content = content.replace(old_first_check, new_first_check)
        print("✅ Enhanced first cancellation check for sort searches")
    else:
        print("❌ Could not find first cancellation pattern")
        return False
    
    # Fix the second cancellation check (after API call)
    old_second_check = '''      if ((window as any).currentSearchId !== searchId) {
        console.log('🚫 PAGINATED SEARCH CANCELLED DURING API:', searchId.toFixed(3));
        return;
      }
      
      // Additional check: if this is a sort-triggered search, ensure it completes
      const isSortTriggered = (window as any).lastSortChangeTime && 
                             (Date.now() - (window as any).lastSortChangeTime) < 3000;
      if (isSortTriggered) {
        console.log('🎯 SORT-TRIGGERED SEARCH - ensuring completion');
      }'''

    new_second_check = '''      // Enhanced post-API cancellation check for sort searches
      const isSortTriggered = (window as any).lastSortChangeTime && 
                             (Date.now() - (window as any).lastSortChangeTime) < 5000;
      
      if ((window as any).currentSearchId !== searchId) {
        // For sort-triggered searches, allow completion even with ID mismatch
        if (isSortTriggered) {
          console.log('🎯 ALLOWING SORT-TRIGGERED SEARCH completion despite ID mismatch:', searchId.toFixed(3));
          // Continue with state update
        } else {
          console.log('🚫 PAGINATED SEARCH CANCELLED DURING API:', searchId.toFixed(3));
          return;
        }
      } else if (isSortTriggered) {
        console.log('🎯 SORT-TRIGGERED SEARCH - ensuring completion');
      }'''

    if old_second_check in content:
        content = content.replace(old_second_check, new_second_check)
        print("✅ Enhanced second cancellation check for sort searches")
    else:
        print("⚠️ Could not find second cancellation pattern - will continue")
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Successfully updated {filename}")
    return True

if __name__ == "__main__":
    success = fix_actual_cancellation("src/hooks/useCards.ts")
    
    if success:
        print("\n🎯 CANCELLATION FIX APPLIED")
        print("Sort-triggered searches should now complete even with rapid re-renders")
        print("Test by clicking sort buttons - results should actually update now")
        print("\nThis prevents the React re-render cancellation issue")
    
    sys.exit(0 if success else 1)