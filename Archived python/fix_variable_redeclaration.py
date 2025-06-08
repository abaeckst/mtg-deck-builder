#!/usr/bin/env python3

import os
import sys

def fix_variable_redeclaration(filename):
    """Fix the variable redeclaration issue in useCards.ts"""
    
    if not os.path.exists(filename):
        print(f"Error: {filename} not found")
        return False
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix the first occurrence - keep as is
    first_pattern = '''      // Enhanced cancellation check - preserve sort-triggered searches
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

    # Keep first occurrence as is (no change needed)
    
    # Fix the second occurrence - use different variable name
    second_old = '''      // Enhanced post-API cancellation check for sort searches
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

    second_new = '''      // Enhanced post-API cancellation check for sort searches
      const isSortTriggeredPost = (window as any).lastSortChangeTime && 
                                 (Date.now() - (window as any).lastSortChangeTime) < 5000;
      
      if ((window as any).currentSearchId !== searchId) {
        // For sort-triggered searches, allow completion even with ID mismatch
        if (isSortTriggeredPost) {
          console.log('🎯 ALLOWING SORT-TRIGGERED SEARCH completion despite ID mismatch:', searchId.toFixed(3));
          // Continue with state update
        } else {
          console.log('🚫 PAGINATED SEARCH CANCELLED DURING API:', searchId.toFixed(3));
          return;
        }
      } else if (isSortTriggeredPost) {
        console.log('🎯 SORT-TRIGGERED SEARCH - ensuring completion');
      }'''

    if second_old in content:
        content = content.replace(second_old, second_new)
        print("✅ Fixed variable redeclaration by renaming second occurrence")
    else:
        print("❌ Could not find second occurrence pattern")
        return False
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Successfully updated {filename}")
    return True

if __name__ == "__main__":
    success = fix_variable_redeclaration("src/hooks/useCards.ts")
    
    if success:
        print("\n🎯 VARIABLE REDECLARATION FIXED")
        print("The app should now compile without TypeScript errors")
        print("Sort functionality should work correctly")
    
    sys.exit(0 if success else 1)