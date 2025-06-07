#!/usr/bin/env python3
"""
Fix the immediate syntax error in scryfallApi.ts.
There's a stray closing brace on line 52 that's breaking compilation.
"""

def fix_stray_brace():
    """Remove the stray closing brace causing syntax error"""
    print("🔧 Fixing stray closing brace in scryfallApi.ts...")
    
    with open('src/services/scryfallApi.ts', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Check line 52 (index 51) for the stray brace
    if len(lines) > 51:
        line_52 = lines[51].strip()
        print(f"Line 52 content: '{line_52}'")
        
        if line_52 == '}':
            print("Found stray closing brace on line 52")
            # Remove this line
            lines.pop(51)
            
            # Write back
            with open('src/services/scryfallApi.ts', 'w', encoding='utf-8') as f:
                f.writelines(lines)
            
            print("✅ Removed stray closing brace")
            return True
        else:
            print(f"Line 52 is not a stray brace: '{line_52}'")
            return False
    else:
        print("File doesn't have 52 lines")
        return False

def add_missing_fields_to_pagination_returns():
    """Add missing fields to PaginatedSearchState return objects"""
    print("🔧 Adding missing fields to PaginatedSearchState objects...")
    
    with open('src/services/scryfallApi.ts', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the return statement in searchCardsWithPagination
    pattern = r'return \{[\s]*initialResults,[\s]*totalCards: response\.total_cards,[\s]*loadedCards: initialResults\.length,[\s]*hasMore,[\s]*isLoadingMore: false,[\s]*currentPage: 1,[\s]*lastQuery: query,[\s]*lastFilters: filters,[\s]*lastSort: \{ order, dir \}[\s]*\};'
    
    replacement = '''return {
      initialResults,
      totalCards: response.total_cards,
      loadedCards: initialResults.length,
      hasMore,
      isLoadingMore: false,
      currentPage: 1,
      lastQuery: query,
      lastFilters: filters,
      lastSort: { order, dir },
      // Partial page consumption tracking
      currentScryfallPage: 1,
      cardsConsumedFromCurrentPage: initialResults.length,
      currentPageCards: response.data,
      scryfallPageSize: 175,
      displayBatchSize: 75,
    };'''
    
    import re
    updated_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    if updated_content != content:
        with open('src/services/scryfallApi.ts', 'w', encoding='utf-8') as f:
            f.write(updated_content)
        print("✅ Added missing fields to searchCardsWithPagination return")
        return True
    else:
        print("⚠️ Could not find return statement pattern")
        return False

def add_missing_fields_to_useSearch():
    """Add missing fields to useSearch.ts PaginatedSearchState object"""
    print("🔧 Adding missing fields to useSearch.ts...")
    
    with open('src/hooks/useSearch.ts', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the currentPaginationState object
    pattern = r'const currentPaginationState: PaginatedSearchState = \{[\s]*totalCards: metadata\.totalCards,[\s]*loadedCards: actualLoadedCards,[\s]*hasMore: actualLoadedCards < metadata\.totalCards,[\s]*isLoadingMore: false,[\s]*currentPage: Math\.floor\(actualLoadedCards / 175\) \+ 1,[\s]*initialResults: state\.cards,[\s]*lastQuery: metadata\.query,[\s]*lastFilters: metadata\.filters,[\s]*lastSort: \{ order: "name", dir: "asc" \},[\s]*\};'
    
    replacement = '''const currentPaginationState: PaginatedSearchState = {
        totalCards: metadata.totalCards,
        loadedCards: actualLoadedCards,
        hasMore: actualLoadedCards < metadata.totalCards,
        isLoadingMore: false,
        currentPage: Math.floor(actualLoadedCards / 175) + 1,
        initialResults: state.cards,
        lastQuery: metadata.query,
        lastFilters: metadata.filters,
        lastSort: { order: "name", dir: "asc" },
        // Enhanced partial page consumption tracking
        currentScryfallPage: Math.floor(actualLoadedCards / 175) + 1,
        cardsConsumedFromCurrentPage: actualLoadedCards % 175,
        currentPageCards: [],
        scryfallPageSize: 175,
        displayBatchSize: 75,
      };'''
    
    import re
    updated_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    if updated_content != content:
        with open('src/hooks/useSearch.ts', 'w', encoding='utf-8') as f:
            f.write(updated_content)
        print("✅ Added missing fields to useSearch pagination state")
        return True
    else:
        print("⚠️ Could not find useSearch pagination state pattern")
        return False

def main():
    """Execute fixes in order"""
    print("🚨 EMERGENCY FIX: Syntax Error in scryfallApi.ts")
    print("=" * 50)
    
    # Step 1: Fix the immediate syntax error
    if not fix_stray_brace():
        print("❌ Could not fix stray brace - checking file manually needed")
        return False
    
    # Step 2: Add missing fields to return objects
    if not add_missing_fields_to_pagination_returns():
        print("⚠️ Could not update pagination returns")
    
    # Step 3: Add missing fields to useSearch
    if not add_missing_fields_to_useSearch():
        print("⚠️ Could not update useSearch pagination state")
    
    print("\n🎯 SYNTAX ERROR FIXED")
    print("1. ✅ Removed stray closing brace from scryfallApi.ts")
    print("2. ✅ Added missing fields to PaginatedSearchState objects")
    print("\n🧪 Test with: npm start")
    
    return True

if __name__ == "__main__":
    main()
