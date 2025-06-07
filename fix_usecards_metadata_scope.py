#!/usr/bin/env python3

import os
import sys

def fix_usecards_metadata_scope(filename):
    """Fix the global metadata exposure scope issue in useCards.ts"""
    
    if not os.path.exists(filename):
        print(f"Error: {filename} not found")
        return False
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove the incorrectly placed global metadata exposure
    incorrect_metadata = '''
      // Expose search metadata globally for direct architecture
      (window as any).lastSearchMetadata = {
        query,
        filters,
        totalCards: paginationResult.totalCards,
        loadedCards: paginationResult.loadedCards,
      };'''
    
    if incorrect_metadata in content:
        content = content.replace(incorrect_metadata, '')
        print("✅ Removed incorrectly placed global metadata exposure")
    else:
        print("❌ Could not find incorrectly placed metadata to remove")
        return False
    
    # Find the correct location within the setState call and add metadata exposure there
    old_setstate = '''      setState(prev => ({
        ...prev,
        cards: paginationResult.initialResults,
        searchQuery: query === '*' ? 'Filtered Results' : query,
        totalCards: paginationResult.totalCards,
        hasMore: paginationResult.hasMore,
        selectedCards: new Set(),
        pagination: {
          totalCards: paginationResult.totalCards,
          loadedCards: paginationResult.loadedCards,
          hasMore: paginationResult.hasMore,
          isLoadingMore: false,
          currentPage: 1,
        },
        lastSearchMetadata: {
          query,
          filters,
          totalCards: paginationResult.totalCards,
          loadedCards: paginationResult.loadedCards,
        },
      }));'''

    new_setstate = '''      setState(prev => ({
        ...prev,
        cards: paginationResult.initialResults,
        searchQuery: query === '*' ? 'Filtered Results' : query,
        totalCards: paginationResult.totalCards,
        hasMore: paginationResult.hasMore,
        selectedCards: new Set(),
        pagination: {
          totalCards: paginationResult.totalCards,
          loadedCards: paginationResult.loadedCards,
          hasMore: paginationResult.hasMore,
          isLoadingMore: false,
          currentPage: 1,
        },
        lastSearchMetadata: {
          query,
          filters,
          totalCards: paginationResult.totalCards,
          loadedCards: paginationResult.loadedCards,
        },
      }));

      // Expose search metadata globally for direct architecture
      (window as any).lastSearchMetadata = {
        query,
        filters,
        totalCards: paginationResult.totalCards,
        loadedCards: paginationResult.loadedCards,
      };'''

    if old_setstate in content:
        content = content.replace(old_setstate, new_setstate)
        print("✅ Added global metadata exposure in correct scope")
    else:
        print("❌ Could not find setState pattern to update")
        return False

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Successfully fixed {filename} - metadata exposure now in correct scope")
    return True

if __name__ == "__main__":
    success = fix_usecards_metadata_scope("src/hooks/useCards.ts")
    sys.exit(0 if success else 1)
