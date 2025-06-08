#!/usr/bin/env python3

import os
import sys

def update_usecards_metadata_exposure(filename):
    """Update useCards.ts to expose search metadata globally for direct architecture"""
    
    if not os.path.exists(filename):
        print(f"Error: {filename} not found")
        return False
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find where lastSearchMetadata is updated and add global exposure
    old_metadata_update = '''        lastSearchMetadata: {
          query,
          filters,
          totalCards: paginationResult.totalCards,
          loadedCards: paginationResult.loadedCards,
        },'''

    new_metadata_update = '''        lastSearchMetadata: {
          query,
          filters,
          totalCards: paginationResult.totalCards,
          loadedCards: paginationResult.loadedCards,
        },'''

    # Add global metadata exposure after the setState
    add_global_exposure = '''
      // Expose search metadata globally for direct architecture
      (window as any).lastSearchMetadata = {
        query,
        filters,
        totalCards: paginationResult.totalCards,
        loadedCards: paginationResult.loadedCards,
      };'''

    if old_metadata_update in content:
        # Find the position after the setState call and add global exposure
        setState_end = content.find('});', content.find(old_metadata_update))
        if setState_end != -1:
            # Insert after the setState call
            insert_pos = setState_end + 3  # After '});'
            content = content[:insert_pos] + add_global_exposure + content[insert_pos:]
            print("✅ Added global metadata exposure after setState")
        else:
            print("❌ Could not find setState end position")
            return False
    else:
        print("❌ Could not find lastSearchMetadata update location")
        return False

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Successfully updated {filename} with global metadata exposure")
    return True

if __name__ == "__main__":
    success = update_usecards_metadata_exposure("src/hooks/useCards.ts")
    sys.exit(0 if success else 1)
