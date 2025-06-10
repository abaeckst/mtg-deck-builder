// src/hooks/useCards.ts - Refactored coordinator with clean separation of concerns
import { useEffect, useCallback, useRef } from 'react';
import { ScryfallCard } from '../types/card';
import { SortCriteria, SortDirection } from './useSorting';
import { useFilters, FilterState } from './useFilters';
import { useSearch } from './useSearch';
import { usePagination } from './usePagination';
import { useCardSelection } from './useCardSelection';
import { useSearchSuggestions } from './useSearchSuggestions';
import { useSorting } from './useSorting';

export interface UseCardsState {
  cards: ScryfallCard[];
  loading: boolean;
  error: string | null;
  selectedCards: Set<string>;
  searchQuery: string;
  totalCards: number;
  
  // Enhanced search state
  searchSuggestions: string[];
  showSuggestions: boolean;
  recentSearches: string[];

  // Progressive loading pagination state
  pagination: {
    totalCards: number;
    loadedCards: number;
    hasMore: boolean;
    isLoadingMore: boolean;
    currentPage: number;
  };

  // Simplified sort integration state
  lastSearchMetadata: {
    query: string;
    filters: FilterState;
    totalCards: number;
    loadedCards: number;
  } | null;
  
  // Re-sorting state
  isResorting: boolean;
}

export interface UseCardsActions {
  searchForCards: (query: string, format?: string) => Promise<void>;
  searchWithAllFilters: (query: string, filtersOverride?: any) => Promise<void>;
  loadPopularCards: () => Promise<void>;
  loadRandomCard: () => Promise<void>;
  selectCard: (cardId: string) => void;
  deselectCard: (cardId: string) => void;
  clearSelection: () => void;
  isCardSelected: (cardId: string) => boolean;
  getSelectedCardsData: () => ScryfallCard[];
  clearCards: () => void;
  
  // Enhanced search actions
  enhancedSearch: (query: string, filtersOverride?: any) => Promise<void>;
  getSearchSuggestions: (query: string) => Promise<void>;
  clearSearchSuggestions: () => void;
  addToSearchHistory: (query: string) => void;
  
  // Dual sort system action
  handleCollectionSortChange: (criteria: SortCriteria, direction: SortDirection) => Promise<void>;
  
  // Progressive loading actions
  loadMoreResultsAction: () => Promise<void>;
  resetPagination: () => void;
  
  // Filter integration (pass-through to useFilters)
  activeFilters: FilterState;
  isFiltersCollapsed: boolean;
  updateFilter: (filterType: string, value: any) => void;
  clearAllFilters: () => void;
  toggleFiltersCollapsed: () => void;
  hasActiveFilters: () => boolean;
  updateSectionState: (section: string, isExpanded: boolean) => void;
  getSectionState: (section: string) => boolean;
  autoExpandSection: (section: string) => void;
}

export const useCards = (): UseCardsState & UseCardsActions => {
  // Integrate with useFilters hook
  const {
    activeFilters,
    isFiltersCollapsed,
    updateFilter,
    clearAllFilters: clearFilters,
    toggleFiltersCollapsed,
    hasActiveFilters,
    updateSectionState,
    getSectionState,
    autoExpandSection,
  } = useFilters();

  // Card selection hook
  const {
    selectedCards,
    selectCard,
    deselectCard,
    clearSelection,
    isCardSelected,
    getSelectedCardsData: getSelectedCardsDataFunc,
  } = useCardSelection();

  // Search suggestions hook
  const {
    searchSuggestions,
    showSuggestions,
    recentSearches,
    getSearchSuggestions,
    clearSearchSuggestions,
    addToSearchHistory,
  } = useSearchSuggestions();

  // Sort coordination hook
  const { getScryfallSortParams } = useSorting();
  
  // Get collection sort parameters for coordination with useSearch
  const getCollectionSortParams = useCallback(() => {
    return getScryfallSortParams('collection');
  }, [getScryfallSortParams]);

  // Pagination hook with proper coordination
  const {
    pagination,
    resetPagination,
    setPaginationState,
    updatePagination,
  } = usePagination();

  // Search hook with coordination callbacks
  const {
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
  });
  // Coordinated Load More function
  const coordinatedLoadMore = useCallback(async () => {
    console.log('🎯 useCards coordinated Load More executing');
    
    if (!pagination.hasMore || pagination.isLoadingMore) {
      console.log('🚫 Cannot load more:', { 
        hasMore: pagination.hasMore,
        isLoadingMore: pagination.isLoadingMore
      });
      return;
    }

    console.log('🔄 Setting loading state...');
    updatePagination({ isLoadingMore: true });

    try {
      console.log('📡 Calling search hook loadMoreCards...');
      await searchHookLoadMore();
      console.log('✅ Coordinated Load More successful');
    } catch (error) {
      console.error('❌ Coordinated Load More failed:', error);
      updatePagination({ isLoadingMore: false });
    }
  }, [pagination.hasMore, pagination.isLoadingMore, updatePagination, searchHookLoadMore]);



  // Enhanced filter-aware clear function
  const clearAllFilters = useCallback(() => {
    console.log('🧹 Clearing all filters and resetting search');
    clearFilters(); // Clear filters using useFilters hook
    
    setTimeout(() => {
      console.log('🧹 Loading popular cards after filter clear');
      loadPopularCards();
    }, 50);
  }, [clearFilters, loadPopularCards]);

  // Clear cards with selection reset
  const clearCards = useCallback(() => {
    clearCardsSearch();
    clearSelection();
  }, [clearCardsSearch, clearSelection]);

  // Get selected cards data with current cards
  const getSelectedCardsData = useCallback((): ScryfallCard[] => {
    return getSelectedCardsDataFunc(cards);
  }, [getSelectedCardsDataFunc, cards]);

  // Load popular cards on mount
  useEffect(() => {
    loadPopularCards();
  }, [loadPopularCards]);

  // FILTER CHANGE REACTIVITY: Trigger fresh search when filters change
  // Skip on initial mount to prevent interference with loadPopularCards
  const isInitialMount = useRef(true);
  
  useEffect(() => {
    // Skip filter reactivity on initial mount
    if (isInitialMount.current) {
      isInitialMount.current = false;
      return;
    }
    
    // Skip if no active filters (user cleared filters - handled by clearAllFilters)
    if (!hasActiveFilters()) {
      return;
    }
    
    console.log('🎯 Filter change detected, triggering fresh search');
    
    // Trigger fresh search with current filters
    // Use '*' as base query to get all cards matching filters
    searchWithAllFilters('*');
    
  }, [activeFilters, hasActiveFilters, searchWithAllFilters]);
  
  // SORT CHANGE REACTIVITY: Currently handled by useSorting hook coordination
  // No additional effect needed as handleCollectionSortChange is already wired up

  return {
    // Search state
    cards,
    loading,
    error,
    searchQuery,
    totalCards,
    lastSearchMetadata,
    isResorting,
    
    // Selection state
    selectedCards,
    
    // Search suggestions state
    searchSuggestions,
    showSuggestions,
    recentSearches,
    
    // Pagination state
    pagination,
    
    // Filter integration (pass-through)
    activeFilters,
    isFiltersCollapsed,
    updateFilter,
    clearAllFilters,
    toggleFiltersCollapsed,
    hasActiveFilters,
    updateSectionState,
    getSectionState,
    autoExpandSection,
    
    // Search actions
    searchForCards,
    searchWithAllFilters,
    enhancedSearch,
    loadPopularCards,
    loadRandomCard,
    clearCards,
    
    // Selection actions
    selectCard,
    deselectCard,
    clearSelection,
    isCardSelected,
    getSelectedCardsData,
    
    // Search suggestions actions
    getSearchSuggestions,
    clearSearchSuggestions,
    addToSearchHistory,
    
    // Sort system
    handleCollectionSortChange,
    
    // Pagination actions
    loadMoreResultsAction: coordinatedLoadMore,
    resetPagination,
  };
};