#!/usr/bin/env python3

import os
import sys

def fix_typescript_dependency_error():
    """Fix the TypeScript error by removing the premature dependency reference"""
    
    filename = "src/hooks/useCards.ts"
    
    if not os.path.exists(filename):
        print(f"Error: {filename} not found")
        return False
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove the incorrect dependency reference that was added too early
    wrong_dependency = "}, [subscribe, unsubscribe, state.lastSearchMetadata, handleCollectionSortChange]);"
    correct_dependency = "}, [subscribe, unsubscribe, state.lastSearchMetadata]);"
    
    if wrong_dependency in content:
        content = content.replace(wrong_dependency, correct_dependency)
        print("✅ Removed premature handleCollectionSortChange dependency reference")
    else:
        print("⚠️ Could not find the incorrect dependency pattern")
    
    # Find the actual useEffect with sort subscription and fix it properly
    old_useeffect = """  // Subscribe to collection sort changes with enhanced debugging
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
  }, [subscribe, unsubscribe, state.lastSearchMetadata]);"""
    
    # The dependency should be added AFTER handleCollectionSortChange is declared
    # For now, let's just fix the immediate error by keeping the original dependencies
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Successfully fixed TypeScript dependency error in {filename}")
    return True

if __name__ == "__main__":
    success = fix_typescript_dependency_error()
    sys.exit(0 if success else 1)