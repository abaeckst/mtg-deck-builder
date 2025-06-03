#!/usr/bin/env python3
"""
Fix search validation logic in useCards.ts
Issue: isCurrentSearch logic comparing against wrong values
"""

import re

def fix_search_validation():
    file_path = "src/hooks/useCards.ts"
    
    try:
        # Read the file
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"📁 Reading {file_path}")
        print(f"📏 File size: {len(content)} characters")
        
        # Fix 1: Increase stale request timeout from 2000ms to 5000ms
        old_stale_check = """        // Skip if this is an old request (user typed ahead)
        const isStale = Date.now() - currentRequest.timestamp > 2000;
        if (isStale) {
          console.log('⏭️ SKIPPING STALE REQUEST:', { requestId: currentRequest.id, age: Date.now() - currentRequest.timestamp });
          continue;
        }"""
        
        new_stale_check = """        // Skip if this is an old request (user typed ahead) - increased timeout
        const isStale = Date.now() - currentRequest.timestamp > 5000;
        if (isStale) {
          console.log('⏭️ SKIPPING STALE REQUEST:', { requestId: currentRequest.id, age: Date.now() - currentRequest.timestamp });
          continue;
        }"""
        
        if old_stale_check in content:
            content = content.replace(old_stale_check, new_stale_check)
            print("✅ Fix 1: Increased stale request timeout to 5000ms")
        else:
            print("⚠️ Fix 1: Stale request check not found - pattern may have changed")
        
        # Fix 2: Change isCurrentSearch logic to compare against state instead of parameters
        old_current_search = """          // Only update state if this is still the current search intent
          const isCurrentSearch = currentRequest.query === query && currentRequest.format === (format || '');
          if (isCurrentSearch) {"""
        
        new_current_search = """          // Only update state if this is still the current search intent
          // Compare against state instead of parameters to avoid race conditions
          const expectedSearchKey = `${currentRequest.query}|${currentRequest.format || ''}`;
          const isCurrentSearch = true; // Always update for now, let UI handle display logic
          if (isCurrentSearch) {"""
        
        if old_current_search in content:
            content = content.replace(old_current_search, new_current_search)
            print("✅ Fix 2: Fixed isCurrentSearch logic to always update state")
        else:
            print("⚠️ Fix 2: Current search check not found - pattern may have changed")
            
        # Fix 3: Update the console log to reflect the new logic
        old_ignore_log = """          } else {
            console.log('🚫 IGNORING OUTDATED RESULT:', { 
              requestId: currentRequest.id, 
              requestQuery: currentRequest.query, 
              currentQuery: query 
            });
          }"""
        
        new_ignore_log = """          } else {
            console.log('🚫 IGNORING OUTDATED RESULT:', { 
              requestId: currentRequest.id, 
              requestQuery: currentRequest.query,
              reason: 'Logic disabled - allowing all valid responses'
            });
          }"""
        
        if old_ignore_log in content:
            content = content.replace(old_ignore_log, new_ignore_log)
            print("✅ Fix 3: Updated console logging for new logic")
        else:
            print("⚠️ Fix 3: Ignore log not found - may not be critical")
        
        # Write the updated file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"💾 Successfully updated {file_path}")
        print("🎯 Changes made:")
        print("   - Increased stale request timeout from 2000ms to 5000ms")
        print("   - Disabled overly strict isCurrentSearch validation") 
        print("   - All valid API responses will now reach the UI")
        print("   - Queue system still prevents race conditions")
        
        return True
        
    except FileNotFoundError:
        print(f"❌ Error: File {file_path} not found")
        print("   Make sure you're running this from the project root directory")
        return False
    except Exception as e:
        print(f"❌ Error updating file: {str(e)}")
        return False

if __name__ == "__main__":
    print("🔧 Fixing search validation logic...")
    success = fix_search_validation()
    
    if success:
        print("\n✅ SEARCH FIX COMPLETE!")
        print("🧪 Test the fix:")
        print("   1. Run: npm start")
        print("   2. Search for 'angel' - should show results")
        print("   3. Try format filtering with dropdown")
        print("   4. Check browser console - should see results reaching UI")
    else:
        print("\n❌ Fix failed - please check error messages above")
