// src/hooks/useCards.ts - Enhanced with progressive loading (75 initial + 175 per batch)
import { useState, useEffect, useCallback } from 'react';
import { ScryfallCard, PaginatedSearchState } from '../types/card';
import { 
  searchCards, 
  getRandomCard, 
  searchCardsWithFilters, 
  SearchFilters, 
  enhancedSearchCards, 
  getSearchSuggestions, 
  searchCardsWithSort,
  searchCardsWithPagination,
  loadMoreResults
} from '../services/scryfallApi';
import { useSorting, AreaType, SortCriteria, SortDirection } from './useSorting';

export interface UseCardsState {
  cards: ScryfallCard[];
  loading: boolean;
  error: string | null;
  hasMore: boolean;
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

  // Sort integration state
  lastSearchMetadata: {
    query: string;
    filters: any;
    totalCards: number;
    loadedCards: number;
  } | null;

  // Enhanced filtering state
  activeFilters: {
    format: string;
    colors: string[];
    colorIdentity: 'exact' | 'subset' | 'include';
    types: string[];
    rarity: string[];
    sets: string[];
    cmc: { min: number | null; max: number | null };
    power: { min: number | null; max: number | null };
    toughness: { min: number | null; max: number | null };
  };
  isFiltersCollapsed: boolean;
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
  
  // Enhanced filter actions
  updateFilter: (filterType: string, value: any) => void;
  clearAllFilters: () => void;
  toggleFiltersCollapsed: () => void;
  hasActiveFilters: () => boolean;
  
  // Enhanced search actions
  enhancedSearch: (query: string, filtersOverride?: any) => Promise<void>;
  getSearchSuggestions: (query: string) => Promise<void>;
  clearSearchSuggestions: () => void;
  addToSearchHistory: (query: string) => void;
  
  // Sort integration actions
  handleCollectionSortChange: (criteria: SortCriteria, direction: SortDirection) => void;
  
  // Progressive loading actions
  loadMoreResultsAction: () => Promise<void>;
  resetPagination: () => void;
}

const POPULAR_CARDS_QUERY = 'legal:standard (type:creature OR type:instant OR type:sorcery OR type:planeswalker OR type:enchantment OR type:artifact)';

export const useCards = (): UseCardsState & UseCardsActions => {
  // Initialize sorting integration
  const { getScryfallSortParams, subscribe, unsubscribe } = useSorting();
  
  // Internal pagination state for progressive loading
  const [paginationState, setPaginationState] = useState<PaginatedSearchState | null>(null);
  
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
    lastSearchMetadata: null,
    
    // Enhanced filtering state
    activeFilters: {
      format: 'custom-standard',
      colors: [],
      colorIdentity: 'exact',
      types: [],
      rarity: [],
      sets: [],
      cmc: { min: null, max: null },
      power: { min: null, max: null },
      toughness: { min: null, max: null },
    },
    isFiltersCollapsed: false,
  });

  // Clear error when starting new operations
  const clearError = useCallback(() => {
    setState(prev => ({ ...prev, error: null }));
  }, []);

  // Set loading state
  const setLoading = useCallback((loading: boolean) => {
    setState(prev => ({ ...prev, loading }));
  }, []);

  // Reset pagination state
  const resetPagination = useCallback(() => {
    setPaginationState(null);
    setState(prev => ({
      ...prev,
      pagination: {
        totalCards: 0,
        loadedCards: 0,
        hasMore: false,
        isLoadingMore: false,
        currentPage: 1,
      }
    }));
  }, []);

  // Load more results action
  const loadMoreResultsAction = useCallback(async () => {
    if (!paginationState || !paginationState.hasMore || paginationState.isLoadingMore) {
      console.log('🚫 Cannot load more:', { 
        hasPaginationState: !!paginationState,
        hasMore: paginationState?.hasMore,
        isLoadingMore: paginationState?.isLoadingMore
      });
      return;
    }

    console.log('🔄 Loading more results...');
    
    // Update loading state
    setState(prev => ({
      ...prev,
      pagination: { ...prev.pagination, isLoadingMore: true }
    }));
    
    // Update pagination state
    setPaginationState(prev => prev ? { ...prev, isLoadingMore: true } : null);

    try {
      const newCards = await loadMoreResults(
        paginationState,
        (loaded, total) => {
          // Progress callback
          setState(prev => ({
            ...prev,
            pagination: { 
              ...prev.pagination, 
              loadedCards: loaded
            }
          }));
        }
      );

      // Update cards and pagination state
      const updatedCards = [...state.cards, ...newCards];
      const newLoadedCount = updatedCards.length;
      const stillHasMore = newLoadedCount < paginationState.totalCards;
      
      setState(prev => ({
        ...prev,
        cards: updatedCards,
        totalCards: paginationState.totalCards,
        hasMore: stillHasMore,
        pagination: {
          ...prev.pagination,
          loadedCards: newLoadedCount,
          hasMore: stillHasMore,
          isLoadingMore: false,
          currentPage: paginationState.currentPage + 1,
        }
      }));

      // Update internal pagination state
      setPaginationState(prev => prev ? {
        ...prev,
        loadedCards: newLoadedCount,
        hasMore: stillHasMore,
        isLoadingMore: false,
        currentPage: prev.currentPage + 1,
      } : null);

      console.log('✅ Load more results successful:', {
        newCardsLoaded: newCards.length,
        totalLoadedNow: newLoadedCount,
        stillHasMore
      });

    } catch (error) {
      console.error('❌ Failed to load more results:', error);
      
      setState(prev => ({
        ...prev,
        pagination: { ...prev.pagination, isLoadingMore: false },
        error: error instanceof Error ? error.message : 'Failed to load more results'
      }));
      
      setPaginationState(prev => prev ? { ...prev, isLoadingMore: false } : null);
    }
  }, [paginationState, state.cards]);

  // Enhanced search with pagination support
  const searchWithPagination = useCallback(async (query: string, filters: SearchFilters = {}) => {
    const searchId = Date.now() + Math.random();
    (window as any).currentSearchId = searchId;

    console.log('🔍 PAGINATED SEARCH STARTED:', { 
      searchId: searchId.toFixed(3), 
      query, 
      filters,
      initialPageSize: 75
    });

    try {
      clearError();
      setLoading(true);
      resetPagination();

      // Rate limiting
      const now = Date.now();
      const lastSearch = (window as any).lastSearchTime || 0;
      const timeSinceLastSearch = now - lastSearch;
      
      if (timeSinceLastSearch < 150) {
        await new Promise(resolve => setTimeout(resolve, 150 - timeSinceLastSearch));
      }
      
      if ((window as any).currentSearchId !== searchId) {
        console.log('🚫 PAGINATED SEARCH CANCELLED:', searchId.toFixed(3));
        return;
      }
      
      (window as any).lastSearchTime = Date.now();

      // Get Scryfall sort parameters
      const sortParams = getScryfallSortParams('collection');
      
      // Execute paginated search
      const paginationResult = await searchCardsWithPagination(
        query, 
        filters, 
        sortParams.order, 
        sortParams.dir
      );

      if ((window as any).currentSearchId !== searchId) {
        console.log('🚫 PAGINATED SEARCH CANCELLED DURING API:', searchId.toFixed(3));
        return;
      }

      console.log('✅ PAGINATED SEARCH SUCCESS:', {
        searchId: searchId.toFixed(3),
        initialResultCount: paginationResult.initialResults.length,
        totalAvailable: paginationResult.totalCards,
        hasMore: paginationResult.hasMore
      });

      // Update state with initial results
      setState(prev => ({
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

      // Store pagination state for load more functionality
      setPaginationState(paginationResult);

    } catch (error) {
      if ((window as any).currentSearchId === searchId) {
        let errorMessage = error instanceof Error ? error.message : 'Failed to search cards';
        let isNoResults = false;
        
        if (errorMessage.includes('404') || errorMessage.includes('No cards found')) {
          errorMessage = 'No cards found matching your search. Try different keywords or filters.';
          isNoResults = true;
          console.log('📭 No results found for paginated search:', query);
        } else {
          console.error('❌ PAGINATED SEARCH ERROR:', {
            searchId: searchId.toFixed(3),
            query: query,
            error: errorMessage
          });
        }

        setState(prev => ({
          ...prev,
          error: isNoResults ? null : errorMessage,
          cards: [],
          totalCards: 0,
          hasMore: false,
          searchQuery: isNoResults ? 'No results found' : prev.searchQuery,
          pagination: {
            totalCards: 0,
            loadedCards: 0,
            hasMore: false,
            isLoadingMore: false,
            currentPage: 1,
          },
        }));
        
        resetPagination();
      }
    } finally {
      if ((window as any).currentSearchId === searchId) {
        setLoading(false);
      }
    }
  }, [clearError, setLoading, resetPagination, getScryfallSortParams]);

  // Search for cards with query and optional format filter - NOW WITH PAGINATION
  const searchForCards = useCallback(async (query: string, format?: string) => {
    // Handle empty query cases
    if (!query.trim()) {
      if (format && format !== '') {
        query = '*';
      } else {
        setState(prev => ({ 
          ...prev, 
          cards: [], 
          searchQuery: '', 
          totalCards: 0,
          selectedCards: new Set(),
          pagination: {
            totalCards: 0,
            loadedCards: 0,
            hasMore: false,
            isLoadingMore: false,
            currentPage: 1,
          }
        }));
        resetPagination();
        return;
      }
    }

    const filters = format && format !== '' 
      ? { format: format === 'custom-standard' ? 'standard' : format }
      : {};

    await searchWithPagination(query, filters);
  }, [searchWithPagination, resetPagination]);

  // Load popular/example cards
  const loadPopularCards = useCallback(async () => {
    clearError();
    setLoading(true);
    resetPagination();

    try {
      const response = await searchCards(POPULAR_CARDS_QUERY);
      
      // Limit to 75 cards for consistency
      const limitedCards = response.data.slice(0, 75);
      
      setState(prev => ({
        ...prev,
        cards: limitedCards,
        searchQuery: 'Popular Cards',
        totalCards: limitedCards.length,
        hasMore: false,
        selectedCards: new Set(),
        pagination: {
          totalCards: limitedCards.length,
          loadedCards: limitedCards.length,
          hasMore: false,
          isLoadingMore: false,
          currentPage: 1,
        },
      }));
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Failed to load popular cards';
      setState(prev => ({
        ...prev,
        error: errorMessage,
        cards: [],
        totalCards: 0,
        hasMore: false,
        pagination: {
          totalCards: 0,
          loadedCards: 0,
          hasMore: false,
          isLoadingMore: false,
          currentPage: 1,
        },
      }));
    } finally {
      setLoading(false);
    }
  }, [clearError, setLoading, resetPagination]);

  // Load a single random card
  const loadRandomCard = useCallback(async () => {
    clearError();
    setLoading(true);
    resetPagination();

    try {
      const card = await getRandomCard();
      setState(prev => ({
        ...prev,
        cards: [card],
        searchQuery: 'Random Card',
        totalCards: 1,
        hasMore: false,
        selectedCards: new Set(),
        pagination: {
          totalCards: 1,
          loadedCards: 1,
          hasMore: false,
          isLoadingMore: false,
          currentPage: 1,
        },
      }));
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Failed to load random card';
      setState(prev => ({
        ...prev,
        error: errorMessage,
        cards: [],
        totalCards: 0,
        hasMore: false,
        pagination: {
          totalCards: 0,
          loadedCards: 0,
          hasMore: false,
          isLoadingMore: false,
          currentPage: 1,
        },
      }));
    } finally {
      setLoading(false);
    }
  }, [clearError, setLoading, resetPagination]);

  // Card selection functions
  const selectCard = useCallback((cardId: string) => {
    setState(prev => {
      const newSelected = new Set(prev.selectedCards);
      newSelected.add(cardId);
      return {
        ...prev,
        selectedCards: newSelected,
      };
    });
  }, []);

  const deselectCard = useCallback((cardId: string) => {
    setState(prev => {
      const newSelected = new Set(prev.selectedCards);
      newSelected.delete(cardId);
      return {
        ...prev,
        selectedCards: newSelected,
      };
    });
  }, []);

  const clearSelection = useCallback(() => {
    setState(prev => ({
      ...prev,
      selectedCards: new Set(),
    }));
  }, []);

  const isCardSelected = useCallback((cardId: string): boolean => {
    return state.selectedCards.has(cardId);
  }, [state.selectedCards]);

  // Get selected cards data
  const getSelectedCardsData = useCallback((): ScryfallCard[] => {
    return state.cards.filter(card => state.selectedCards.has(card.id));
  }, [state.cards, state.selectedCards]);

  // Clear all cards and reset state
  const clearCards = useCallback(() => {
    resetPagination();
    setState({
      cards: [],
      loading: false,
      error: null,
      hasMore: false,
      selectedCards: new Set(),
      searchQuery: '',
      totalCards: 0,
      searchSuggestions: [],
      showSuggestions: false,
      recentSearches: [],
      pagination: {
        totalCards: 0,
        loadedCards: 0,
        hasMore: false,
        isLoadingMore: false,
        currentPage: 1,
      },
      lastSearchMetadata: null,
      activeFilters: {
        format: '',
        colors: [],
        colorIdentity: 'exact',
        types: [],
        rarity: [],
        sets: [],
        cmc: { min: null, max: null },
        power: { min: null, max: null },
        toughness: { min: null, max: null },
      },
      isFiltersCollapsed: false,
    });
  }, [resetPagination]);

  // Load popular cards on mount
  useEffect(() => {
    loadPopularCards();
  }, [loadPopularCards]);

  // Subscribe to collection sort changes
  useEffect(() => {
    const subscriptionId = subscribe((area: AreaType, sortState) => {
      if (area === 'collection') {
        console.log('🔄 Collection sort changed:', sortState);
        if (state.lastSearchMetadata) {
          handleCollectionSortChange(sortState.criteria, sortState.direction);
        }
      }
    });

    return () => {
      unsubscribe(subscriptionId);
    };
  }, [subscribe, unsubscribe, state.lastSearchMetadata]);

  // Enhanced filter management functions
  const updateFilter = useCallback((filterType: string, value: any) => {
    console.log('🎛️ Updating filter:', filterType, '=', value);
    setState(prev => {
      const newFilters = {
        ...prev.activeFilters,
        [filterType]: value,
      };
      console.log('🎛️ New filter state:', newFilters);
      return {
        ...prev,
        activeFilters: newFilters,
      };
    });
  }, []);

  const clearAllFilters = useCallback(() => {
    console.log('🧹 Clearing all filters and resetting search');
    setState(prev => ({
      ...prev,
      activeFilters: {
        format: '',
        colors: [],
        colorIdentity: 'exact',
        types: [],
        rarity: [],
        sets: [],
        cmc: { min: null, max: null },
        power: { min: null, max: null },
        toughness: { min: null, max: null },
      },
    }));
    
    setTimeout(() => {
      console.log('🧹 Loading popular cards after filter clear');
      loadPopularCards();
    }, 50);
  }, [loadPopularCards]);

  const toggleFiltersCollapsed = useCallback(() => {
    setState(prev => ({
      ...prev,
      isFiltersCollapsed: !prev.isFiltersCollapsed,
    }));
  }, []);

  const hasActiveFilters = useCallback((): boolean => {
    const filters = state.activeFilters;
    return (
      filters.format !== '' ||
      filters.colors.length > 0 ||
      filters.types.length > 0 ||
      filters.rarity.length > 0 ||
      filters.sets.length > 0 ||
      filters.cmc.min !== null ||
      filters.cmc.max !== null ||
      filters.power.min !== null ||
      filters.power.max !== null ||
      filters.toughness.min !== null ||
      filters.toughness.max !== null
    );
  }, [state.activeFilters]);

  // Enhanced search function that uses all active filters with pagination
  const searchWithAllFilters = useCallback(async (query: string, filtersOverride?: any) => {
    const filters = filtersOverride || state.activeFilters;
    
    console.log('🚀 searchWithAllFilters called:', { query, filters, usingOverride: !!filtersOverride });
    
    // Build comprehensive filter object
    const searchFilters: any = {};
    
    if (filters.format && filters.format !== '') {
      searchFilters.format = filters.format;
    }
    if (filters.colors && filters.colors.length > 0) {
      searchFilters.colors = filters.colors;
      searchFilters.colorIdentity = filters.colorIdentity;
    }
    if (filters.types && filters.types.length > 0) {
      searchFilters.types = filters.types;
    }
    if (filters.rarity && filters.rarity.length > 0) {
      searchFilters.rarity = filters.rarity;
    }
    if (filters.sets && filters.sets.length > 0) {
      searchFilters.sets = filters.sets;
    }
    if (filters.cmc && (filters.cmc.min !== null || filters.cmc.max !== null)) {
      searchFilters.cmc = {};
      if (filters.cmc.min !== null) searchFilters.cmc.min = filters.cmc.min;
      if (filters.cmc.max !== null) searchFilters.cmc.max = filters.cmc.max;
    }
    if (filters.power && (filters.power.min !== null || filters.power.max !== null)) {
      searchFilters.power = {};
      if (filters.power.min !== null) searchFilters.power.min = filters.power.min;
      if (filters.power.max !== null) searchFilters.power.max = filters.power.max;
    }
    if (filters.toughness && (filters.toughness.min !== null || filters.toughness.max !== null)) {
      searchFilters.toughness = {};
      if (filters.toughness.min !== null) searchFilters.toughness.min = filters.toughness.min;
      if (filters.toughness.max !== null) searchFilters.toughness.max = filters.toughness.max;
    }

    // Determine query strategy
    const hasFilters = Object.keys(searchFilters).length > 0;
    const hasQuery = query && query.trim() !== '';
    
    let actualQuery: string;
    if (hasQuery) {
      actualQuery = query.trim();
    } else if (hasFilters) {
      actualQuery = '*';
    } else {
      console.log('❌ No query and no filters - falling back to popular cards');
      loadPopularCards();
      return;
    }
    
    await searchWithPagination(actualQuery, searchFilters);
  }, [state.activeFilters, searchWithPagination, loadPopularCards]);

  // Enhanced search function with full-text capabilities and pagination
  const enhancedSearch = useCallback(async (query: string, filtersOverride?: any) => {
    const filters = filtersOverride || state.activeFilters;
    
    console.log('🔍 enhancedSearch called with:', { query, filters, hasFilters: Object.keys(filters).length });
    
    // Handle empty query cases
    if (!query.trim()) {
      if (Object.keys(filters).some(key => {
        const value = filters[key];
        return value && (Array.isArray(value) ? value.length > 0 : 
                        typeof value === 'object' ? Object.values(value).some(v => v !== null) :
                        value !== '');
      })) {
        query = '*';
      } else {
        loadPopularCards();
        return;
      }
    }

    await searchWithPagination(query, filters);
    addToSearchHistory(query);
  }, [state.activeFilters, searchWithPagination, loadPopularCards]);

  const getSearchSuggestionsFunc = useCallback(async (query: string) => {
    if (!query.trim() || query.length < 2) {
      setState(prev => ({ ...prev, searchSuggestions: [], showSuggestions: false }));
      return;
    }

    try {
      const suggestions = await getSearchSuggestions(query);
      setState(prev => ({ 
        ...prev, 
        searchSuggestions: suggestions.slice(0, 8),
        showSuggestions: suggestions.length > 0 
      }));
    } catch (error) {
      console.error('Failed to get search suggestions:', error);
    }
  }, []);

  const clearSearchSuggestions = useCallback(() => {
    setState(prev => ({ ...prev, searchSuggestions: [], showSuggestions: false }));
  }, []);

  const addToSearchHistory = useCallback((query: string) => {
    if (!query.trim() || query === '*') return;
    
    setState(prev => {
      const newHistory = [query, ...prev.recentSearches.filter(h => h !== query)].slice(0, 10);
      return { ...prev, recentSearches: newHistory };
    });
  }, []);

  // Handle collection sort changes with smart re-search logic - UPDATED FOR 75-card threshold
  const handleCollectionSortChange = useCallback(async (criteria: SortCriteria, direction: SortDirection) => {
    const metadata = state.lastSearchMetadata;
    if (!metadata) {
      console.log('🔄 No search metadata available for sort change');
      return;
    }

    // Updated threshold: Use server-side sort if we have more than 75 cards loaded
    const shouldUseServerSort = metadata.totalCards > 75 && metadata.loadedCards < metadata.totalCards;
    console.log('🔄 Sort change analysis:', {
      criteria,
      direction,
      totalCards: metadata.totalCards,
      loadedCards: metadata.loadedCards,
      threshold: 75,
      shouldUseServerSort
    });

    if (shouldUseServerSort) {
      console.log('🌐 Using server-side sorting - re-searching with new sort parameters');
      
      // Get Scryfall sort parameters
      const sortParams = getScryfallSortParams('collection');
      console.log('🔧 Scryfall sort params:', sortParams);
      
      // Re-search with same query and filters but new sort
      await searchWithPagination(metadata.query, metadata.filters);
    } else {
      console.log('🏠 Using client-side sorting - dataset is small enough or all results loaded');
      // Client-side sorting will be handled by the UI component
      // No action needed here as the sortCards function in MTGOLayout will handle it
    }
  }, [state.lastSearchMetadata, getScryfallSortParams, searchWithPagination]);

  return {
    ...state,
    searchForCards,
    searchWithAllFilters,
    loadPopularCards,
    loadRandomCard,
    selectCard,
    deselectCard,
    clearSelection,
    isCardSelected,
    getSelectedCardsData,
    clearCards,
    updateFilter,
    clearAllFilters,
    toggleFiltersCollapsed,
    hasActiveFilters,
    enhancedSearch,
    getSearchSuggestions: getSearchSuggestionsFunc,
    clearSearchSuggestions,
    addToSearchHistory,
    handleCollectionSortChange,
    loadMoreResultsAction,
    resetPagination,
  };
};