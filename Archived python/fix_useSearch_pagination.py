#!/usr/bin/env python3
"""
Fix the TypeScript compilation error in useSearch.ts by adding the missing 
pagination tracking fields to the currentPaginationState object.
"""

import re

def fix_pagination_state():
    """Add missing fields to currentPaginationState in useSearch.ts"""
    print("🔧 Fixing currentPaginationState in useSearch.ts...")
    
    with open('src/hooks/useSearch.ts', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the currentPaginationState object (around line 499)
    pattern = r'const currentPaginationState: PaginatedSearchState = \{[\s\S]*?lastSort: \{ order: "name", dir: "asc" \},\s*\};'
    
    replacement = '''const currentPaginationState: PaginatedSearchState = {
        totalCards: metadata.totalCards,
        loadedCards: actualLoadedCards, // ✅ Use actual current cards count
        hasMore: actualLoadedCards < metadata.totalCards,
        isLoadingMore: false,
        currentPage: Math.floor(actualLoadedCards / 175) + 1, // ✅ Fixed: 175 cards per page, not 75
        initialResults: state.cards,
        lastQuery: metadata.query,
        lastFilters: metadata.filters,
        lastSort: { order: "name", dir: "asc" },
        // Enhanced partial page consumption tracking
        currentScryfallPage: Math.floor(actualLoadedCards / 175) + 1,
        cardsConsumedFromCurrentPage: actualLoadedCards % 175,
        currentPageCards: [], // Empty since we don't store full page data in useSearch
        scryfallPageSize: 175,
        displayBatchSize: 75,
      };'''
    
    updated_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    if updated_content != content:
        with open('src/hooks/useSearch.ts', 'w', encoding='utf-8') as f:
            f.write(updated_content)
        print("✅ Added missing pagination tracking fields to useSearch.ts")
        return True
    else:
        print("⚠️ Could not find currentPaginationState pattern to update")
        return False

def clean_unused_variables():
    """Remove unused variables from scryfallApi.ts to clean up warnings"""
    print("🧹 Cleaning up unused variables in scryfallApi.ts...")
    
    with open('src/services/scryfallApi.ts', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    updated_lines = []
    changes_made = False
    
    for line in lines:
        # Remove the unused captureSearchDebug function
        if 'function captureSearchDebug()' in line:
            # Skip this function and its closing brace
            changes_made = True
            continue
        elif line.strip().startswith('console.log(') and ('SEARCH DEBUG CAPTURE' in line or 'Ready for copy/paste' in line or 'perform your search' in line):
            changes_made = True
            continue
        elif line.strip() == '}' and changes_made and len(updated_lines) > 0 and 'captureSearchDebug' in ''.join(updated_lines[-5:]):
            changes_made = True
            continue
        # Remove unused LOAD_MORE_PAGE_SIZE constant
        elif 'const LOAD_MORE_PAGE_SIZE = 175;' in line:
            changes_made = True
            continue
        else:
            updated_lines.append(line)
    
    if changes_made:
        with open('src/services/scryfallApi.ts', 'w', encoding='utf-8') as f:
            f.writelines(updated_lines)
        print("✅ Removed unused variables from scryfallApi.ts")
        return True
    else:
        print("ℹ️ No unused variables found to remove")
        return False

def main():
    """Execute the fixes"""
    print("🚀 Fixing TypeScript compilation error in useSearch.ts")
    print("=" * 60)
    
    # Step 1: Fix the missing pagination fields
    pagination_fixed = fix_pagination_state()
    
    # Step 2: Clean up unused variables (optional)
    cleanup_done = clean_unused_variables()
    
    print("\n🎯 FIX RESULTS:")
    if pagination_fixed:
        print("1. ✅ Fixed currentPaginationState missing fields in useSearch.ts")
    else:
        print("1. ❌ Could not fix currentPaginationState - manual fix needed")
    
    if cleanup_done:
        print("2. ✅ Cleaned up unused variables in scryfallApi.ts")
    else:
        print("2. ℹ️ No cleanup needed for unused variables")
    
    print("\n🧪 Next Steps:")
    print("1. Run: npm start")
    print("2. Test Load More functionality in Card view")
    print("3. Verify alphabetical sequence continuity (A→B→C)")
    
    return pagination_fixed

if __name__ == "__main__":
    main()
