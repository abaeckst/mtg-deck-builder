#!/usr/bin/env python3

import os
import sys

def fix_default_sort_and_server_search():
    """Fix default sort to be alphabetical and ensure server-side sorting works"""
    
    # Fix 1: Check the default sort settings
    sorting_file = "src/hooks/useSorting.ts"
    cards_file = "src/hooks/useCards.ts"
    
    files_modified = 0
    
    # Check useSorting.ts for default sort settings
    if os.path.exists(sorting_file):
        with open(sorting_file, 'r', encoding='utf-8') as f:
            sorting_content = f.read()
        
        # Look for default sort direction and make sure it's 'asc' for alphabetical
        if 'direction: \'desc\'' in sorting_content and 'collection' in sorting_content:
            sorting_content = sorting_content.replace('direction: \'desc\'', 'direction: \'asc\'')
            with open(sorting_file, 'w', encoding='utf-8') as f:
                f.write(sorting_content)
            print("✅ Fixed default sort direction to ascending (alphabetical)")
            files_modified += 1
        else:
            print("ℹ️ Default sort direction appears to be correct or not found")
    
    # Fix 2: Ensure handleCollectionSortChange is actually being called
    if not os.path.exists(cards_file):
        print(f"Error: {cards_file} not found")
        return False
    
    with open(cards_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Make sure the sort subscription is working properly and triggers server-side searches
    old_subscription = """  // Subscribe to collection sort changes
  useEffect(() => {
    const subscriptionId = subscribe((area: AreaType, sortState) => {
      if (area === 'collection') {
        console.log('🔄 Collection sort changed:', sortState);
        if (state.lastSearchMetadata) {
          handleCollectionSortChange(sortState.criteria, sortState.direction);
        }
      }
    });

    return () => {
      unsubscribe(subscriptionId);
    };
  }, [subscribe, unsubscribe, state.lastSearchMetadata]);"""
    
    new_subscription = """  // Subscribe to collection sort changes with enhanced debugging
  useEffect(() => {
    const subscriptionId = subscribe((area: AreaType, sortState) => {
      if (area === 'collection') {
        console.log('🔄 Collection sort changed:', sortState);
        console.log('🔍 Current search metadata:', state.lastSearchMetadata);
        
        if (state.lastSearchMetadata) {
          console.log('✅ Triggering handleCollectionSortChange');
          handleCollectionSortChange(sortState.criteria, sortState.direction);
        } else {
          console.log('❌ No search metadata - cannot trigger sort change');
        }
      }
    });

    return () => {
      unsubscribe(subscriptionId);
    };
  }, [subscribe, unsubscribe, state.lastSearchMetadata, handleCollectionSortChange]);"""
    
    if old_subscription in content:
        content = content.replace(old_subscription, new_subscription)
        print("✅ Enhanced sort subscription debugging")
        files_modified += 1
    else:
        print("⚠️ Could not find exact sort subscription pattern")
    
    # Ensure the dependency array includes handleCollectionSortChange
    if "}, [subscribe, unsubscribe, state.lastSearchMetadata]);" in content:
        content = content.replace(
            "}, [subscribe, unsubscribe, state.lastSearchMetadata]);",
            "}, [subscribe, unsubscribe, state.lastSearchMetadata, handleCollectionSortChange]);"
        )
        print("✅ Fixed dependency array to include handleCollectionSortChange")
        files_modified += 1
    
    if files_modified > 0:
        with open(cards_file, 'w', encoding='utf-8') as f:
            f.write(content)
    
    print(f"✅ Successfully modified {files_modified} areas in the files")
    return True

if __name__ == "__main__":
    success = fix_default_sort_and_server_search()
    sys.exit(0 if success else 1)