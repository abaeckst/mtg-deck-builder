#!/usr/bin/env python3

import os
import re

def update_use_search():
    """Update useSearch.ts to coordinate with useSorting for default sort parameters"""
    
    file_path = r"C:\Users\abaec\Development\mtg-deck-builder\src\hooks\useSearch.ts"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"❌ File not found: {file_path}")
        return False
    
    print("🔧 UPDATING useSearch.ts for proper sort coordination...")
    
    # Add useSorting import
    import_pattern = r"import { SortCriteria, SortDirection } from './useSorting';"
    
    # Check if useSorting import already includes what we need
    if "import { SortCriteria, SortDirection } from './useSorting';" in content:
        print("✅ useSorting import already present")
    else:
        print("❌ Missing proper useSorting import")
        return False
    
    # Add interface prop for getting sort state
    interface_pattern = r"interface UseSearchProps \{[\s\S]*?\}"
    
    # Update the interface to include getSortState
    new_interface = """interface UseSearchProps {
  activeFilters: FilterState;
  hasActiveFilters: () => boolean;
  onPaginationStateChange: (state: PaginatedSearchState | null) => void;
  onPaginationUpdate: (update: Partial<{
    totalCards: number;
    loadedCards: number;
    hasMore: boolean;
    isLoadingMore: boolean;
    currentPage: number;
  }>) => void;
  resetPagination: () => void;
  addToSearchHistory: (query: string) => void;
  // ADDED: Get default sort parameters from useSorting
  getCollectionSortParams: () => { order: string; dir: 'asc' | 'desc' };
}"""
    
    content = re.sub(interface_pattern, new_interface, content)
    
    # Update the hook parameter destructuring
    hook_params_pattern = r"export const useSearch = \(\{\s*activeFilters,\s*hasActiveFilters,\s*onPaginationStateChange,\s*onPaginationUpdate,\s*resetPagination,\s*addToSearchHistory\s*\}: UseSearchProps\)"
    
    new_hook_params = """export const useSearch = ({
  activeFilters,
  hasActiveFilters,
  onPaginationStateChange,
  onPaginationUpdate,
  resetPagination,
  addToSearchHistory,
  getCollectionSortParams
}: UseSearchProps)"""
    
    content = re.sub(hook_params_pattern, new_hook_params, content)
    
    # Update searchWithPagination to use default sort parameters
    search_func_pattern = r"const searchWithPagination = useCallback\(async \(\s*query: string,\s*filters: SearchFilters = \{\},\s*sortOrder = 'name',\s*sortDirection: 'asc' \| 'desc' = 'asc'\s*\) => \{"
    
    new_search_func = """const searchWithPagination = useCallback(async (
    query: string, 
    filters: SearchFilters = {},
    sortOrder?: string,
    sortDirection?: 'asc' | 'desc'
  ) => {
    // Get default sort parameters from useSorting if not provided
    const defaultSortParams = getCollectionSortParams();
    const actualSortOrder = sortOrder || defaultSortParams.order;
    const actualSortDirection = sortDirection || defaultSortParams.dir;"""
    
    content = re.sub(search_func_pattern, new_search_func, content)
    
    # Update the console.log to use actual parameters
    log_pattern = r"console\.log\('🔍 SIMPLIFIED SEARCH:', \{ query, filters, sort: \{ sortOrder, sortDirection \} \}\);"
    new_log = "console.log('🔍 SIMPLIFIED SEARCH:', { query, filters, sort: { actualSortOrder, actualSortDirection } });"
    content = re.sub(log_pattern, new_log, content)
    
    # Update the API call to use actual parameters
    api_call_pattern = r"console\.log\('🔍 Calling searchCardsWithPagination with sort:', \{ sortOrder, sortDirection \}\);"
    new_api_call_log = "console.log('🔍 Calling searchCardsWithPagination with sort:', { actualSortOrder, actualSortDirection });"
    content = re.sub(api_call_pattern, new_api_call_log, content)
    
    # Update the actual API call
    api_call_pattern2 = r"const paginationResult = await searchCardsWithPagination\(\s*query,\s*filters,\s*sortOrder,\s*sortDirection\s*\);"
    new_api_call = "const paginationResult = await searchCardsWithPagination(query, filters, actualSortOrder, actualSortDirection);"
    content = re.sub(api_call_pattern2, new_api_call, content)
    
    # Update success log
    success_log_pattern = r"sortApplied: \{ sortOrder, sortDirection \}"
    new_success_log = "sortApplied: { actualSortOrder, actualSortDirection }"
    content = re.sub(success_log_pattern, new_success_log, content)
    
    # Update dependency array to include getCollectionSortParams
    deps_pattern = r"\], \[clearError, setLoading, resetPagination, onPaginationUpdate, onPaginationStateChange\]\);"
    new_deps = "], [clearError, setLoading, resetPagination, onPaginationUpdate, onPaginationStateChange, getCollectionSortParams]);"
    content = re.sub(deps_pattern, new_deps, content)
    
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ useSearch.ts updated successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to write useSearch.ts: {e}")
        return False

def update_use_cards():
    """Update useCards.ts to pass sort coordination to useSearch"""
    
    file_path = r"C:\Users\abaec\Development\mtg-deck-builder\src\hooks\useCards.ts"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"❌ File not found: {file_path}")
        return False
    
    print("🔧 UPDATING useCards.ts for sort coordination...")
    
    # Add useSorting import - check if it exists
    if "import { useSorting }" in content:
        print("✅ useSorting import already present")
    else:
        # Add the import
        import_pattern = r"(import { useSearchSuggestions } from './useSearchSuggestions';)"
        new_import = r"\1\nimport { useSorting } from './useSorting';"
        content = re.sub(import_pattern, new_import, content)
        print("✅ Added useSorting import")
    
    # Add useSorting hook call after other hooks
    hook_call_pattern = r"(\s+const \{\s+searchSuggestions,[\s\S]*?\} = useSearchSuggestions\(\);)"
    
    new_hook_call = r"""\1

  // Sort coordination hook
  const { getScryfallSortParams } = useSorting();
  
  // Get collection sort parameters for coordination with useSearch
  const getCollectionSortParams = useCallback(() => {
    return getScryfallSortParams('collection');
  }, [getScryfallSortParams]);"""
    
    content = re.sub(hook_call_pattern, new_hook_call, content)
    
    # Update useSearch call to include getCollectionSortParams
    use_search_pattern = r"const \{\s*cards,[\s\S]*?\} = useSearch\(\{\s*activeFilters,\s*hasActiveFilters,\s*onPaginationStateChange: setPaginationState,\s*onPaginationUpdate: updatePagination,\s*resetPagination,\s*addToSearchHistory,\s*\}\);"
    
    new_use_search = """const {
    cards,
    loading,
    error,
    searchQuery,
    totalCards,
    lastSearchMetadata,
    isResorting,
    searchForCards,
    searchWithAllFilters,
    enhancedSearch,
    loadPopularCards,
    loadRandomCard,
    clearCards: clearCardsSearch,
    handleCollectionSortChange,
    loadMoreCards: searchHookLoadMore,
  } = useSearch({
    activeFilters,
    hasActiveFilters,
    onPaginationStateChange: setPaginationState,
    onPaginationUpdate: updatePagination,
    resetPagination,
    addToSearchHistory,
    getCollectionSortParams, // ADDED: Sort coordination
  });"""
    
    content = re.sub(use_search_pattern, new_use_search, content)
    
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ useCards.ts updated successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to write useCards.ts: {e}")
        return False

def main():
    print("🚀 FIXING SEARCH SORT COORDINATION")
    print("=" * 50)
    print("Problem: useSearch hardcodes sortOrder='name' instead of using useSorting defaults")
    print("Solution: Make useSearch coordinate with useSorting for default sort parameters")
    print()
    
    success1 = update_use_search()
    success2 = update_use_cards()
    
    if success1 and success2:
        print("\n✅ ALL UPDATES SUCCESSFUL!")
        print("🎯 Expected behavior:")
        print("  • Initial searches will use mana value (cmc) sorting")
        print("  • API calls will include order=cmc&dir=asc by default")
        print("  • Results will be sorted by mana value from the server")
        print("  • No more client-side sort mismatch!")
        print("\n🧪 Test by:")
        print("  1. Refresh localhost:3000")
        print("  2. Search for anything (e.g., 'lightning bolt')")
        print("  3. Results should be sorted by mana value (0,1,2,3...)")
        print("  4. Check console for 'sort: { actualSortOrder: cmc, actualSortDirection: asc }'")
    else:
        print("\n❌ UPDATES FAILED")
        print("Please check the files manually")

if __name__ == "__main__":
    main()