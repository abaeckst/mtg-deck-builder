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

def fix_pagination_state_object():
    filepath = "src/hooks/useSearch.ts"
    content = read_file(filepath)
    
    if not content:
        return False
    
    # Remove the nextUrl property which doesn't exist in PaginatedSearchState
    old_pagination_state = '''      const currentPaginationState: PaginatedSearchState = {
        totalCards: metadata.totalCards,
        loadedCards: metadata.loadedCards,
        hasMore: metadata.loadedCards < metadata.totalCards,
        isLoadingMore: false,
        currentPage: Math.floor(metadata.loadedCards / 75) + 1,
        nextUrl: null,
        initialResults: state.cards,
        lastQuery: metadata.query,
        lastFilters: metadata.filters,
        lastSort: { order: "name", dir: "asc" },
      };'''
    
    new_pagination_state = '''      const currentPaginationState: PaginatedSearchState = {
        totalCards: metadata.totalCards,
        loadedCards: metadata.loadedCards,
        hasMore: metadata.loadedCards < metadata.totalCards,
        isLoadingMore: false,
        currentPage: Math.floor(metadata.loadedCards / 75) + 1,
        initialResults: state.cards,
        lastQuery: metadata.query,
        lastFilters: metadata.filters,
        lastSort: { order: "name", dir: "asc" },
      };'''
    
    content = content.replace(old_pagination_state, new_pagination_state)
    
    return write_file(filepath, content)

def main():
    print("🔧 Fixing PaginatedSearchState type compatibility...")
    
    if not os.path.exists("src/hooks"):
        print("❌ Error: Not in project root directory.")
        return False
    
    if fix_pagination_state_object():
        print("✅ PaginatedSearchState type error fixed!")
        print("📋 Removed: nextUrl property (not in interface)")
        print()
        print("🧪 Try running 'npm start' again")
        return True
    else:
        print("❌ Failed to fix type error")
        return False

if __name__ == "__main__":
    main()
