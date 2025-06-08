#!/usr/bin/env python3

import os
import sys

def update_layout_hooks_integration(filename):
    """Update MTGOLayout.tsx to integrate with new useCards + useFilters architecture"""
    
    if not os.path.exists(filename):
        print(f"Error: {filename} not found")
        return False
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Make replacements to integrate new hook architecture
    updates = [
        # 1. Update the useCards destructuring to remove filter-related items
        (
            """  const { 
    cards, 
    loading, 
    error, 
    searchForCards,
    searchWithAllFilters,
    enhancedSearch,
    loadPopularCards, 
    loadRandomCard,
    activeFilters,
    isFiltersCollapsed,
    updateFilter,
    clearAllFilters,
    toggleFiltersCollapsed,
    hasActiveFilters,
    searchSuggestions,
    showSuggestions,
    getSearchSuggestions,
    clearSearchSuggestions,
    addToSearchHistory,
    // Progressive loading actions
    pagination,
    loadMoreResultsAction,
    resetPagination,
    // Phase 4B: Enhanced filter actions
    updateSectionState,
    getSectionState,
    autoExpandSection
  } = useCards();""",
            """  const { 
    cards, 
    loading, 
    error, 
    searchForCards,
    searchWithAllFilters,
    enhancedSearch,
    loadPopularCards, 
    loadRandomCard,
    searchSuggestions,
    showSuggestions,
    getSearchSuggestions,
    clearSearchSuggestions,
    addToSearchHistory,
    // Progressive loading actions
    pagination,
    loadMoreResultsAction,
    resetPagination,
    // Dual sort system integration
    handleCollectionSortChange,
    // Filter integration (pass-through from useFilters)
    activeFilters,
    isFiltersCollapsed,
    updateFilter,
    clearAllFilters,
    toggleFiltersCollapsed,
    hasActiveFilters,
    updateSectionState,
    getSectionState,
    autoExpandSection
  } = useCards();""",
            "Update useCards destructuring with dual sort integration"
        ),
        
        # 2. Add useSorting integration for dual sort system
        (
            """  // Simplified sorting system - client-side only
  const { updateSort, getSortState } = useSorting();""",
            """  // Enhanced sorting system with dual sort integration
  const { updateSort, getSortState } = useSorting();
  
  // Integrate dual sort system with sort button handlers
  const handleSortChange = useCallback(async (area: 'collection' | 'deck' | 'sideboard', criteria: SortCriteria, direction: SortDirection) => {
    // Always update the sort state first (for UI consistency)
    updateSort(area, criteria, direction);
    
    // For collection area, trigger dual sort system
    if (area === 'collection') {
      await handleCollectionSortChange(criteria, direction);
    }
  }, [updateSort, handleCollectionSortChange]);""",
            "Add dual sort system integration"
        ),
        
        # 3. Update collection sort button handlers to use dual sort system
        (
            """                      onClick={() => { 
                        if (collectionSort.criteria === 'name') {
                          const newDirection = collectionSort.direction === 'asc' ? 'desc' : 'asc';
                          updateSort('collection', 'name', newDirection);
                        } else {
                          updateSort('collection', 'name', 'asc');
                        }
                        setShowCollectionSortMenu(false); 
                      }}""",
            """                      onClick={() => { 
                        if (collectionSort.criteria === 'name') {
                          const newDirection = collectionSort.direction === 'asc' ? 'desc' : 'asc';
                          handleSortChange('collection', 'name', newDirection);
                        } else {
                          handleSortChange('collection', 'name', 'asc');
                        }
                        setShowCollectionSortMenu(false); 
                      }}""",
            "Update name sort button to use dual sort system"
        ),
        
        # 4. Update mana sort button handler
        (
            """                      onClick={() => { 
                        if (collectionSort.criteria === 'mana') {
                          updateSort('collection', 'mana', collectionSort.direction === 'asc' ? 'desc' : 'asc');
                        } else {
                          updateSort('collection', 'mana', 'asc');
                        }
                        setShowCollectionSortMenu(false); 
                      }}""",
            """                      onClick={() => { 
                        if (collectionSort.criteria === 'mana') {
                          handleSortChange('collection', 'mana', collectionSort.direction === 'asc' ? 'desc' : 'asc');
                        } else {
                          handleSortChange('collection', 'mana', 'asc');
                        }
                        setShowCollectionSortMenu(false); 
                      }}""",
            "Update mana sort button to use dual sort system"
        ),
        
        # 5. Update color sort button handler
        (
            """                      onClick={() => { 
                        if (collectionSort.criteria === 'color') {
                          updateSort('collection', 'color', collectionSort.direction === 'asc' ? 'desc' : 'asc');
                        } else {
                          updateSort('collection', 'color', 'asc');
                        }
                        setShowCollectionSortMenu(false); 
                      }}""",
            """                      onClick={() => { 
                        if (collectionSort.criteria === 'color') {
                          handleSortChange('collection', 'color', collectionSort.direction === 'asc' ? 'desc' : 'asc');
                        } else {
                          handleSortChange('collection', 'color', 'asc');
                        }
                        setShowCollectionSortMenu(false); 
                      }}""",
            "Update color sort button to use dual sort system"
        ),
        
        # 6. Update rarity sort button handler  
        (
            """                      onClick={() => { 
                        if (collectionSort.criteria === 'rarity') {
                          updateSort('collection', 'rarity', collectionSort.direction === 'asc' ? 'desc' : 'asc');
                        } else {
                          updateSort('collection', 'rarity', 'asc');
                        }
                        setShowCollectionSortMenu(false); 
                      }}""",
            """                      onClick={() => { 
                        if (collectionSort.criteria === 'rarity') {
                          handleSortChange('collection', 'rarity', collectionSort.direction === 'asc' ? 'desc' : 'asc');
                        } else {
                          handleSortChange('collection', 'rarity', 'asc');
                        }
                        setShowCollectionSortMenu(false); 
                      }}""",
            "Update rarity sort button to use dual sort system"
        ),
        
        # 7. Update ListView sort change handler to use dual sort for collection
        (
            """                  onSortChange={(criteria, direction) => {
                    updateSort('collection', criteria, direction);
                  }}""",
            """                  onSortChange={(criteria, direction) => {
                    handleSortChange('collection', criteria, direction);
                  }}""",
            "Update ListView sort handler for dual sort system"
        ),
        
        # 8. Add type definitions import for new hook integration
        (
            """import { useSorting } from '../hooks/useSorting';""",
            """import { useSorting, SortCriteria, SortDirection } from '../hooks/useSorting';""",
            "Add type imports for dual sort system"
        )
    ]
    
    for old_str, new_str, desc in updates:
        if old_str in content:
            content = content.replace(old_str, new_str)
            print(f"✅ {desc}")
        else:
            print(f"❌ Could not find: {desc}")
            return False
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Successfully updated {filename} with dual sort system integration")
    return True

if __name__ == "__main__":
    success = update_layout_hooks_integration("src/components/MTGOLayout.tsx")
    sys.exit(0 if success else 1)