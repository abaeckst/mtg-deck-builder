#!/usr/bin/env python3

import os
import sys

def force_react_ui_updates():
    """Force React to properly update UI when cards state changes"""
    
    # Fix 1: Update useCards.ts to force React re-renders
    filename1 = "src/hooks/useCards.ts"
    
    if not os.path.exists(filename1):
        print(f"Error: {filename1} not found")
        return False
    
    with open(filename1, 'r', encoding='utf-8') as f:
        content1 = f.read()
    
    # Add a render force trigger state
    old_state_init = """  const [state, setState] = useState<UseCardsState>({
    cards: [],
    loading: false,
    error: null,
    hasMore: false,
    selectedCards: new Set(),
    searchQuery: '',
    totalCards: 0,
    
    // Enhanced search state
    searchSuggestions: [],
    showSuggestions: false,
    recentSearches: [],
    
    // Progressive loading pagination state
    pagination: {
      totalCards: 0,
      loadedCards: 0,
      hasMore: false,
      isLoadingMore: false,
      currentPage: 1,
    },
    
    // Sort integration state
    lastSearchMetadata: null,"""

    new_state_init = """  // Add render trigger for forcing React updates
  const [renderTrigger, setRenderTrigger] = useState(0);
  
  const [state, setState] = useState<UseCardsState>({
    cards: [],
    loading: false,
    error: null,
    hasMore: false,
    selectedCards: new Set(),
    searchQuery: '',
    totalCards: 0,
    
    // Enhanced search state
    searchSuggestions: [],
    showSuggestions: false,
    recentSearches: [],
    
    // Progressive loading pagination state
    pagination: {
      totalCards: 0,
      loadedCards: 0,
      hasMore: false,
      isLoadingMore: false,
      currentPage: 1,
    },
    
    // Sort integration state
    lastSearchMetadata: null,"""

    if old_state_init in content1:
        content1 = content1.replace(old_state_init, new_state_init)
        print("✅ Added render trigger state")
    else:
        print("❌ Could not find state initialization")
        return False

    # Force render trigger when cards are updated
    old_cards_update = """      // Create new array reference to ensure React detects change
      const newCards = [...paginationResult.initialResults];
      const updateTimestamp = Date.now();
      
      console.log('🔄 UPDATING STATE WITH NEW CARDS:', {
        searchId: searchId.toFixed(3),
        cardsLength: newCards.length,
        firstCard: newCards[0]?.name || 'None',
        lastCard: newCards[newCards.length - 1]?.name || 'None',
        isPriority: isPrioritySearch,
        updateTimestamp
      });

      setState(prev => ({
        ...prev,
        cards: newCards, // New array reference
        searchQuery: query === '*' ? 'Filtered Results' : query,
        totalCards: paginationResult.totalCards,
        hasMore: paginationResult.hasMore,
        selectedCards: new Set<string>(),
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
      }));"""

    new_cards_update = """      // Create new array reference to ensure React detects change
      const newCards = [...paginationResult.initialResults];
      const updateTimestamp = Date.now();
      
      console.log('🔄 UPDATING STATE WITH NEW CARDS:', {
        searchId: searchId.toFixed(3),
        cardsLength: newCards.length,
        firstCard: newCards[0]?.name || 'None',
        lastCard: newCards[newCards.length - 1]?.name || 'None',
        isPriority: isPrioritySearch,
        updateTimestamp
      });

      setState(prev => ({
        ...prev,
        cards: newCards, // New array reference
        searchQuery: query === '*' ? 'Filtered Results' : query,
        totalCards: paginationResult.totalCards,
        hasMore: paginationResult.hasMore,
        selectedCards: new Set<string>(),
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
      
      // CRITICAL: Force React re-render by triggering render count change
      setRenderTrigger(prev => prev + 1);
      console.log('🔄 FORCED RENDER TRIGGER:', renderTrigger + 1);"""

    if old_cards_update in content1:
        content1 = content1.replace(old_cards_update, new_cards_update)
        print("✅ Added render trigger to state updates")
    else:
        print("❌ Could not find cards update section")
        return False

    # Write the updated useCards.ts
    with open(filename1, 'w', encoding='utf-8') as f:
        f.write(content1)
    
    # Fix 2: Update MTGOLayout.tsx to use render trigger in dependencies
    filename2 = "src/components/MTGOLayout.tsx"
    
    if not os.path.exists(filename2):
        print(f"Error: {filename2} not found")
        return False
    
    with open(filename2, 'r', encoding='utf-8') as f:
        content2 = f.read()
    
    # Update the cards destructuring to include renderTrigger
    old_cards_destructure = """  const { 
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
    autoExpandSection,} = useCards();"""

    new_cards_destructure = """  const { 
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
    autoExpandSection,} = useCards();
  
  // Track cards changes with render counter
  const cardsChangeTracker = useMemo(() => {
    return {
      length: cards.length,
      firstCard: cards[0]?.name || 'Empty',
      timestamp: Date.now()
    };
  }, [cards]);"""

    if old_cards_destructure in content2:
        content2 = content2.replace(old_cards_destructure, new_cards_destructure)
        print("✅ Added cards change tracker")
    else:
        print("❌ Could not find cards destructuring")
        return False

    # Update the sortedCollectionCards useMemo to use the tracker
    old_sorted_memo = """  // Get sorted cards for each area - FIXED FOR PROPER REACT UPDATES
  const sortedCollectionCards = useMemo(() => {
    // Add update tracking for debugging
    const updateTracker = (window as any).lastSuccessfulSortUpdate || 0;
    
    console.log('🔄 ===== COLLECTION CARDS MEMO RECALCULATION =====');
    console.log('🔄 MEMO DEPENDENCIES CHECK:', {
      cardsLength: cards.length,
      cardsFirstCard: cards[0]?.name || 'None',
      sortCriteria: collectionSort.criteria,
      sortDirection: collectionSort.direction,
      updateTracker: updateTracker,
      cardsReference: cards === (window as any).lastCardsReference ? 'SAME' : 'DIFFERENT'
    });
    
    // Store cards reference for tracking
    (window as any).lastCardsReference = cards;"""

    new_sorted_memo = """  // Get sorted cards for each area - FORCED REACT UPDATES
  const sortedCollectionCards = useMemo(() => {
    const updateTracker = (window as any).lastSuccessfulSortUpdate || 0;
    
    console.log('🔄 ===== COLLECTION CARDS MEMO RECALCULATION =====');
    console.log('🔄 MEMO DEPENDENCIES CHECK:', {
      cardsLength: cards.length,
      cardsFirstCard: cards[0]?.name || 'None',
      sortCriteria: collectionSort.criteria,
      sortDirection: collectionSort.direction,
      updateTracker: updateTracker,
      changeTracker: cardsChangeTracker,
      forceRender: true
    });"""

    if old_sorted_memo in content2:
        content2 = content2.replace(old_sorted_memo, new_sorted_memo)
        print("✅ Updated memo to use change tracker")
    else:
        print("❌ Could not find sorted memo")
        return False

    # Update the memo dependencies to include the change tracker
    old_memo_deps = """    return sorted;
  }, [cards, collectionSort.criteria, collectionSort.direction, sortCards, pagination, (window as any).lastSuccessfulSortUpdate]);"""

    new_memo_deps = """    return sorted;
  }, [cards, collectionSort.criteria, collectionSort.direction, sortCards, pagination, cardsChangeTracker]);"""

    if old_memo_deps in content2:
        content2 = content2.replace(old_memo_deps, new_memo_deps)
        print("✅ Updated memo dependencies")
    else:
        print("❌ Could not find memo dependencies")
        return False

    # Add a debug effect that logs when sortedCollectionCards actually changes
    old_debug_effect = """  // Debug effect to track card changes
  useEffect(() => {
    if (cards.length > 0) {
      console.log('🎯 CARDS STATE CHANGED IN MTGO LAYOUT:', {
        cardsLength: cards.length,
        firstCard: cards[0]?.name || 'None',
        lastCard: cards[cards.length - 1]?.name || 'None',
        timestamp: Date.now(),
        isAfterSort: (window as any).lastSortChangeTime && 
                     (Date.now() - (window as any).lastSortChangeTime) < 3000
      });
    }
  }, [cards]);"""

    new_debug_effect = """  // Debug effect to track card changes
  useEffect(() => {
    if (cards.length > 0) {
      console.log('🎯 CARDS STATE CHANGED IN MTGO LAYOUT:', {
        cardsLength: cards.length,
        firstCard: cards[0]?.name || 'None',
        lastCard: cards[cards.length - 1]?.name || 'None',
        timestamp: Date.now(),
        isAfterSort: (window as any).lastSortChangeTime && 
                     (Date.now() - (window as any).lastSortChangeTime) < 3000
      });
    }
  }, [cards]);

  // Debug effect to track when sortedCollectionCards changes
  useEffect(() => {
    if (sortedCollectionCards.length > 0) {
      console.log('🎯 SORTED COLLECTION CARDS CHANGED:', {
        sortedLength: sortedCollectionCards.length,
        sortedFirst: sortedCollectionCards[0]?.name || 'None',
        sortedLast: sortedCollectionCards[sortedCollectionCards.length - 1]?.name || 'None',
        changeTracker: cardsChangeTracker,
        timestamp: Date.now()
      });
    }
  }, [sortedCollectionCards, cardsChangeTracker]);"""

    if old_debug_effect in content2:
        content2 = content2.replace(old_debug_effect, new_debug_effect)
        print("✅ Added sorted cards change tracking")
    else:
        print("❌ Could not find debug effect")
        return False

    # Write the updated MTGOLayout.tsx
    with open(filename2, 'w', encoding='utf-8') as f:
        f.write(content2)
    
    print(f"✅ Successfully updated both {filename1} and {filename2} with forced React updates")
    return True

if __name__ == "__main__":
    success = force_react_ui_updates()
    sys.exit(0 if success else 1)