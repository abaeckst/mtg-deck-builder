#!/usr/bin/env python3

import os

def read_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return None

def write_file(filepath, content):
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed: {filepath}")
        return True
    except Exception as e:
        print(f"Error writing {filepath}: {e}")
        return False

def fix_syntax_errors():
    filepath = "src/hooks/useSearch.ts"
    content = read_file(filepath)
    
    if not content:
        return False
    
    # Fix 1: Remove double comma
    content = content.replace('handleCollectionSortChange,,', 'handleCollectionSortChange,')
    
    # Fix 2: Fix the PaginatedSearchState type issue
    # Replace the problematic currentPaginationState construction
    old_state_construction = '''      // Use the existing pagination state to load more
      const currentPaginationState = {
        totalCards: metadata.totalCards,
        loadedCards: metadata.loadedCards,
        hasMore: metadata.loadedCards < metadata.totalCards,
        isLoadingMore: false,
        currentPage: Math.floor(metadata.loadedCards / 75) + 1,
        nextUrl: null,
        query: metadata.query,
        filters: metadata.filters,
      };

      const { loadMoreResults } = await import('../services/scryfallApi');
      const newCards = await loadMoreResults(currentPaginationState);'''
    
    new_state_construction = '''      // Use the existing pagination state to load more
      const currentPaginationState: PaginatedSearchState = {
        totalCards: metadata.totalCards,
        loadedCards: metadata.loadedCards,
        hasMore: metadata.loadedCards < metadata.totalCards,
        isLoadingMore: false,
        currentPage: Math.floor(metadata.loadedCards / 75) + 1,
        nextUrl: null,
        initialResults: state.cards,
        lastQuery: metadata.query,
        lastFilters: metadata.filters,
        lastSort: null,
      };

      const { loadMoreResults } = await import('../services/scryfallApi');
      const newCards = await loadMoreResults(currentPaginationState);'''
    
    content = content.replace(old_state_construction, new_state_construction)
    
    return write_file(filepath, content)

def main():
    print("🔧 Fixing syntax errors in useSearch.ts...")
    
    if not os.path.exists("src/hooks"):
        print("❌ Error: Not in project root directory.")
        return False
    
    if fix_syntax_errors():
        print("✅ Syntax errors fixed successfully!")
        print("📋 Fixed issues:")
        print("   • Removed double comma in return statement")
        print("   • Fixed PaginatedSearchState type compatibility")
        print()
        print("🧪 Try running 'npm start' again")
        return True
    else:
        print("❌ Failed to fix syntax errors")
        return False

if __name__ == "__main__":
    main()
