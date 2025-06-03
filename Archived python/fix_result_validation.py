#!/usr/bin/env python3
"""
Fix result validation in useCards.ts
Issue: Search results don't match the actual search query (showing wrong results)
Solution: Properly validate results match the current search state
"""

def fix_result_validation():
    file_path = "src/hooks/useCards.ts"
    
    try:
        # Read the file
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"📁 Reading {file_path}")
        print(f"📏 File size: {len(content)} characters")
        
        # Fix: Replace the broken isCurrentSearch logic with proper validation
        old_validation = """          // Only update state if this is still the current search intent
          // Compare against state instead of parameters to avoid race conditions
          const expectedSearchKey = `${currentRequest.query}|${currentRequest.format || ''}`;
          const isCurrentSearch = true; // Always update for now, let UI handle display logic
          if (isCurrentSearch) {"""
        
        new_validation = """          // Only update state if this matches what the user is currently expecting
          // Get the most recent search from the queue or current request
          const latestQueuedSearch = winTracker.apiHealth.requestQueue.length > 0 
            ? winTracker.apiHealth.requestQueue[winTracker.apiHealth.requestQueue.length - 1]
            : currentRequest;
          
          const isCurrentSearch = currentRequest.query === latestQueuedSearch.query && 
                                currentRequest.format === latestQueuedSearch.format;
          
          console.log('🎯 RESULT VALIDATION:', {
            requestId: currentRequest.id,
            requestQuery: currentRequest.query,
            requestFormat: currentRequest.format || 'none',
            latestQuery: latestQueuedSearch.query,
            latestFormat: latestQueuedSearch.format || 'none',
            isCurrentSearch: isCurrentSearch,
            queueLength: winTracker.apiHealth.requestQueue.length
          });
          
          if (isCurrentSearch) {"""
        
        if old_validation in content:
            content = content.replace(old_validation, new_validation)
            print("✅ Fix 1: Replaced broken validation with proper search matching")
        else:
            print("⚠️ Fix 1: Validation pattern not found - may need manual update")
            
        # Fix: Update the ignore message to be more descriptive
        old_ignore_msg = """          } else {
            console.log('🚫 IGNORING OUTDATED RESULT:', { 
              requestId: currentRequest.id, 
              requestQuery: currentRequest.query,
              reason: 'Logic disabled - allowing all valid responses'
            });
          }"""
        
        new_ignore_msg = """          } else {
            console.log('🚫 IGNORING OUTDATED RESULT:', { 
              requestId: currentRequest.id, 
              requestQuery: currentRequest.query,
              requestFormat: currentRequest.format || 'none',
              reason: 'Search was superseded by newer search'
            });
          }"""
        
        if old_ignore_msg in content:
            content = content.replace(old_ignore_msg, new_ignore_msg)
            print("✅ Fix 2: Updated ignore message to be more descriptive")
        else:
            print("⚠️ Fix 2: Ignore message pattern not found - not critical")
        
        # Write the updated file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"💾 Successfully updated {file_path}")
        print("🎯 Changes made:")
        print("   - Fixed result validation to check against latest queued search")
        print("   - Added detailed logging to debug result matching")
        print("   - Results will only display if they match current search intent")
        print("   - Prevents cross-contamination between different searches")
        
        return True
        
    except FileNotFoundError:
        print(f"❌ Error: File {file_path} not found")
        print("   Make sure you're running this from the project root directory")
        return False
    except Exception as e:
        print(f"❌ Error updating file: {str(e)}")
        return False

if __name__ == "__main__":
    print("🔧 Fixing result validation logic...")
    success = fix_result_validation()
    
    if success:
        print("\n✅ RESULT VALIDATION FIX COMPLETE!")
        print("🧪 Test the fix:")
        print("   1. Run: npm start")
        print("   2. Search for 'angel' - should only show angel-related cards")
        print("   3. Search for 'snap' - should only show snap-related cards")
        print("   4. Check console for '🎯 RESULT VALIDATION' logs")
        print("   5. Look for '🚫 IGNORING OUTDATED RESULT' messages")
    else:
        print("\n❌ Fix failed - please check error messages above")
