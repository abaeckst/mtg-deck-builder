#!/usr/bin/env python3

import os
import sys

def fix_usecards_sort_override_specific(filename):
    """Fix useCards to use override sort parameters when available"""
    
    if not os.path.exists(filename):
        print(f"Error: {filename} not found")
        return False
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the exact pattern from the file
    old_sort_params = '''      // Get Scryfall sort parameters
      const sortParams = getScryfallSortParams('collection');'''

    new_sort_params = '''      // Get Scryfall sort parameters with override support
      const baseSortParams = getScryfallSortParams('collection');
      const overrideParams = (window as any).overrideSortParams;
      const sortParams = overrideParams || baseSortParams;
      
      // Clear override after use
      if (overrideParams) {
        delete (window as any).overrideSortParams;
        console.log('🔧 USING OVERRIDE SORT PARAMS:', sortParams);
      } else {
        console.log('🔧 USING REGULAR SORT PARAMS:', sortParams);
      }'''

    if old_sort_params in content:
        content = content.replace(old_sort_params, new_sort_params)
        print("✅ Added sort parameter override logic")
    else:
        print("❌ Could not find the exact sort parameters section")
        print("Looking for alternative patterns...")
        
        # Try alternative pattern
        alt_pattern = '''      const sortParams = getScryfallSortParams('collection');'''
        
        if alt_pattern in content:
            new_alt_pattern = '''      // Get Scryfall sort parameters with override support
      const baseSortParams = getScryfallSortParams('collection');
      const overrideParams = (window as any).overrideSortParams;
      const sortParams = overrideParams || baseSortParams;
      
      // Clear override after use
      if (overrideParams) {
        delete (window as any).overrideSortParams;
        console.log('🔧 USING OVERRIDE SORT PARAMS:', sortParams);
      } else {
        console.log('🔧 USING REGULAR SORT PARAMS:', sortParams);
      }'''
            
            content = content.replace(alt_pattern, new_alt_pattern)
            print("✅ Added sort parameter override logic (alternative pattern)")
        else:
            print("❌ Could not find any sort parameter patterns")
            return False

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Successfully added sort override to {filename}")
    return True

if __name__ == "__main__":
    success = fix_usecards_sort_override_specific("src/hooks/useCards.ts")
    sys.exit(0 if success else 1)
