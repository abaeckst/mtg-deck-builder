// src/hooks/useSearch.ts - Core search and API communication
import { useState, useCallback } from 'react';
import { ScryfallCard, PaginatedSearchState } from '../types/card';
import { 
  getRandomCard, 
  searchCardsWithPagination,
  SearchFilters
} from '../services/scryfallApi';
import { SortCriteria, SortDirection } from './useSorting';
import { FilterState } from './useFilters';

export interface SearchState {
  cards: ScryfallCard[];
  loading: boolean;
  error: string | null;
  searchQuery: string;
  totalCards: number;
  lastSearchMetadata: {
    query: string;
    filters: FilterState;
    totalCards: number;
    loadedCards: number;
  } | null;
  isResorting: boolean;
}

export interface SearchActions {

  searchForCards: (query: string, format?: string) => Promise<void>;
  searchWithAllFilters: (query: string, filtersOverride?: any) => Promise<void>;
  enhancedSearch: (query: string, filtersOverride?: any) => Promise<void>;
  loadPopularCards: () => Promise<void>;
  loadRandomCard: () => Promise<void>;
  clearCards: () => void;
  handleCollectionSortChange: (criteria: SortCriteria, direction: SortDirection) => Promise<void>;
  loadMoreCards: () => Promise<ScryfallCard[]>;
}

const POPULAR_CARDS_QUERY = 'legal:standard t:creature cmc>=7';

interface UseSearchProps {
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
}

export const useSearch = ({
  activeFilters,
  hasActiveFilters,
  onPaginationStateChange,
  onPaginationUpdate,
  resetPagination,
  addToSearchHistory,
  getCollectionSortParams
}: UseSearchProps): SearchState & SearchActions => {
  const [state, setState] = useState<SearchState>({
    cards: [],
    loading: false,
    error: null,
    searchQuery: '',
    totalCards: 0,
    lastSearchMetadata: null,
    isResorting: false,
  });

  // Clear error when starting new operations
  const clearError = useCallback(() => {
    setState(prev => ({ ...prev, error: null }));
  }, []);

  // Set loading state
  const setLoading = useCallback((loading: boolean) => {
    setState(prev => ({ ...prev, loading }));
  }, []);

  // Enhanced search with pagination support - SIMPLIFIED, NO RACE CONDITIONS
  const searchWithPagination = useCallback(async (
    query: string, 
    filters: SearchFilters = {},
    sortOrder?: string,
    sortDirection?: 'asc' | 'desc'
  ) => {
    // Get default sort parameters from useSorting if not provided
    const defaultSortParams = getCollectionSortParams();
    const actualSortOrder = sortOrder || defaultSortParams.order;
    const actualSortDirection = sortDirection || defaultSortParams.dir;
    console.log('🔍 SIMPLIFIED SEARCH:', { query, filters, sort: { actualSortOrder, actualSortDirection } });

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
      
      (window as any).lastSearchTime = Date.now();

      // Execute paginated search
      console.log('🔍 Calling searchCardsWithPagination with sort:', { actualSortOrder, actualSortDirection });
      const paginationResult = await searchCardsWithPagination(query, filters, actualSortOrder, actualSortDirection);

      console.log('✅ SEARCH SUCCESS:', {
        initialResultCount: paginationResult.initialResults.length,
        totalAvailable: paginationResult.totalCards,
        hasMore: paginationResult.hasMore,
        sortApplied: { actualSortOrder, actualSortDirection }
      });

      // Update state with new results
      setState(prev => ({
        ...prev,
        cards: [...paginationResult.initialResults], // New array reference
        searchQuery: query === '*' ? 'Filtered Results' : query,
        totalCards: paginationResult.totalCards,
        lastSearchMetadata: {
          query,
          filters: filters as FilterState,
          totalCards: paginationResult.totalCards,
          loadedCards: paginationResult.loadedCards,
        },
      }));

      // Update pagination through callback
      onPaginationUpdate({
        totalCards: paginationResult.totalCards,
        loadedCards: paginationResult.loadedCards,
        hasMore: paginationResult.hasMore,
        isLoadingMore: false,
        currentPage: 1,
      });

      // Store pagination state for load more functionality
      onPaginationStateChange(paginationResult);

    } catch (error) {
      let errorMessage = error instanceof Error ? error.message : 'Failed to search cards';
      let isNoResults = false;
      
      if (errorMessage.includes('404') || errorMessage.includes('No cards found')) {
        errorMessage = 'No cards found matching your search. Try different keywords or filters.';
        isNoResults = true;
        console.log('📭 No results found for search:', query);
      } else {
        console.error('❌ SEARCH ERROR:', { query, error: errorMessage });
      }

      setState(prev => ({
        ...prev,
        error: isNoResults ? null : errorMessage,
        cards: [],
        totalCards: 0,
        searchQuery: isNoResults ? 'No results found' : prev.searchQuery,
      }));
      
      onPaginationUpdate({
        totalCards: 0,
        loadedCards: 0,
        hasMore: false,
        isLoadingMore: false,
        currentPage: 1,
      });
      
      resetPagination();
    } finally {
      setLoading(false);
    }
  }, [clearError, setLoading, resetPagination, onPaginationUpdate, onPaginationStateChange]);

  // DUAL SORT SYSTEM - Simple and reliable
  const handleCollectionSortChange = useCallback(async (criteria: SortCriteria, direction: SortDirection) => {
    console.log('🎯 DUAL SORT SYSTEM:', { criteria, direction });
    
    const metadata = state.lastSearchMetadata;
    if (!metadata) {
      console.log('❌ No search metadata available for sort change');
      return;
    }

    // Simple decision logic: complete dataset (≤75 total) = client sort
    const isCompleteDataset = metadata.totalCards <= 75;
    
    console.log('🤔 Sort decision:', {
      criteria,
      direction,
      totalCards: metadata.totalCards,
      loadedCards: metadata.loadedCards,
      threshold: 75,
      isCompleteDataset,
      decision: isCompleteDataset ? 'CLIENT-SIDE (instant)' : 'SERVER-SIDE (new search)'
    });

    if (isCompleteDataset) {
      console.log('🏠 CLIENT-SIDE SORT: Dataset complete, will be handled by UI components');
      // Client-side sorting handled automatically by UI components using useSorting hook
    } else {
      console.log('🌐 SERVER-SIDE SORT: Large dataset, triggering new search');
      
      // Convert SortCriteria to Scryfall sort parameters
      const scryfallSortMapping: Record<SortCriteria, string> = {
        mana: 'cmc',
        color: 'color',
        rarity: 'rarity',
        name: 'name',
        type: 'type',
      };
      
      const sortOrder = scryfallSortMapping[criteria];
      const sortDirection = direction;
      
      try {
        setState(prev => ({ ...prev, isResorting: true }));
        
        console.log('🚀 EXECUTING SERVER-SIDE SORT:', {
          query: metadata.query,
          filters: metadata.filters,
          sortOrder,
          sortDirection
        });
        
        // Clear current results and show loading
        setState(prev => ({ ...prev, cards: [] }));
        
        // Trigger new search with sort parameters
        await searchWithPagination(
          metadata.query, 
          metadata.filters as SearchFilters, 
          sortOrder, 
          sortDirection
        );
        
        console.log('✅ Server-side sort completed successfully');
      } catch (error) {
        console.error('❌ Server-side sort failed:', error);
        setState(prev => ({
          ...prev,
          error: 'Failed to apply sort. Please try again.'
        }));
      } finally {
        setState(prev => ({ ...prev, isResorting: false }));
      }
    }
  }, [state.lastSearchMetadata, searchWithPagination]);

  // Search for cards with query and optional format filter
  const searchForCards = useCallback(async (query: string, format?: string) => {
    if (!query.trim()) {
      if (format && format !== '') {
        query = '*';
      } else {
        setState(prev => ({ 
          ...prev, 
          cards: [], 
          searchQuery: '', 
          totalCards: 0,
        }));
        onPaginationUpdate({
          totalCards: 0,
          loadedCards: 0,
          hasMore: false,
          isLoadingMore: false,
          currentPage: 1,
        });
        resetPagination();
        return;
      }
    }

    const filters = format && format !== '' 
      ? { format: format === 'custom-standard' ? 'standard' : format }
      : {};

    await searchWithPagination(query, filters);
  }, [searchWithPagination, resetPagination, onPaginationUpdate]);

  // Load popular/example cards
  const loadPopularCards = useCallback(async () => {
    console.log('🎯 Loading popular cards...');
    
    try {
      // Use descending CMC sort to show expensive creatures first
    const defaultSortParams = getCollectionSortParams();
    await searchWithPagination(POPULAR_CARDS_QUERY, {}, defaultSortParams.order, 'desc');
      setState(prev => ({
        ...prev,
        searchQuery: 'Standard Cards',
      }));
      console.log('✅ Popular cards loaded successfully');
    } catch (error) {
      console.error('❌ Failed to load popular cards:', error);
      
      // Fallback: try a simpler query
      try {
        console.log('🔄 Trying fallback query: creature');
        await searchWithPagination('creature', {});
        setState(prev => ({
          ...prev,
          searchQuery: 'Standard Cards',
        }));
        console.log('✅ Fallback popular cards loaded');
      } catch (fallbackError) {
        console.error('❌ Fallback also failed:', fallbackError);
        setState(prev => ({
          ...prev,
          error: 'Failed to load popular cards. Try searching manually.',
          searchQuery: 'Error loading popular cards',
        }));
      }
    }
  }, [searchWithPagination]);

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
      }));
      
      onPaginationUpdate({
        totalCards: 1,
        loadedCards: 1,
        hasMore: false,
        isLoadingMore: false,
        currentPage: 1,
      });
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Failed to load random card';
      setState(prev => ({
        ...prev,
        error: errorMessage,
        cards: [],
        totalCards: 0,
      }));
      
      onPaginationUpdate({
        totalCards: 0,
        loadedCards: 0,
        hasMore: false,
        isLoadingMore: false,
        currentPage: 1,
      });
    } finally {
      setLoading(false);
    }
  }, [clearError, setLoading, resetPagination, onPaginationUpdate]);

  // Enhanced search function that uses all active filters
  const searchWithAllFilters = useCallback(async (query: string, filtersOverride?: any) => {
    const filters = filtersOverride || activeFilters;
    
    console.log('🚀 searchWithAllFilters called:', { query, filters, usingOverride: !!filtersOverride });
    
    // Build comprehensive filter object for SearchFilters interface
    const searchFilters: SearchFilters = {};
    
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
    if (filters.subtypes && filters.subtypes.length > 0) {
      searchFilters.subtypes = filters.subtypes;
    }
    if (filters.isGoldMode) {
      searchFilters.isGoldMode = filters.isGoldMode;
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
    
    // Get default sort parameters for consistent sorting
    const defaultSortParams = getCollectionSortParams();
    await searchWithPagination(actualQuery, searchFilters, defaultSortParams.order, defaultSortParams.dir);
  }, [activeFilters, searchWithPagination, loadPopularCards]);

  // Enhanced search function with full-text capabilities
  const enhancedSearch = useCallback(async (query: string, filtersOverride?: any) => {
    const filters = filtersOverride || activeFilters;
    
    console.log('🔍 enhancedSearch called with:', { query, filters });
    
    // Handle empty query cases
    if (!query.trim()) {
      if (hasActiveFilters()) {
        query = '*';
      } else {
        loadPopularCards();
        return;
      }
    }

    // Get default sort parameters for consistent sorting
    const defaultSortParams = getCollectionSortParams();
    await searchWithPagination(query, filters as SearchFilters, defaultSortParams.order, defaultSortParams.dir);
    addToSearchHistory(query);
  }, [activeFilters, searchWithPagination, loadPopularCards, hasActiveFilters, addToSearchHistory]);

  // Clear all cards and reset state
  const clearCards = useCallback(() => {
    resetPagination();
    setState(prev => ({
      ...prev,
      cards: [],
      loading: false,
      error: null,
      searchQuery: '',
      totalCards: 0,
      lastSearchMetadata: null,
      isResorting: false,
    }));
    
    onPaginationUpdate({
      totalCards: 0,
      loadedCards: 0,
      hasMore: false,
      isLoadingMore: false,
      currentPage: 1,
    });
  }, [resetPagination, onPaginationUpdate]);

  // Load more cards for progressive loading
  const loadMoreCards = useCallback(async (): Promise<ScryfallCard[]> => {
    console.log('🔄 useSearch.loadMoreCards called');
    
    const metadata = state.lastSearchMetadata;
    if (!metadata) {
      console.log('❌ No search metadata available for load more');
      throw new Error('No search metadata available');
    }

    try {
      console.log('📡 Loading more cards via API...');
      
      // ✅ FIXED: Use actual current cards count instead of metadata
      const actualLoadedCards = state.cards.length;
      console.log('📄 Pagination calculation:', {
        actualLoadedCards,
        metadataLoadedCards: metadata.loadedCards,
        totalCards: metadata.totalCards,
        nextPage: Math.floor(actualLoadedCards / 75) + 1
      });
      
      // ✅ FIXED: Build corrected pagination state for loadMoreResults API
      const currentPaginationState: PaginatedSearchState = {
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
      };
      
      console.log('📄 Using pagination state:', {
        loadedCards: currentPaginationState.loadedCards,
        currentPage: currentPaginationState.currentPage,
        hasMore: currentPaginationState.hasMore
      });

      // ✅ FIXED: Use loadMoreResults API instead of searchCardsWithPagination
      const { loadMoreResults } = await import('../services/scryfallApi');
      const newCards = await loadMoreResults(currentPaginationState);
      
      console.log('✅ Load more API successful:', {
        newCardsCount: newCards.length,
        previousTotal: state.cards.length
      });

      // Update local state with appended cards
      setState(prev => {
        const updatedCards = [...prev.cards, ...newCards];
        console.log('🔄 Updating useSearch cards state:', {
          previousCount: prev.cards.length,
          newCardsCount: newCards.length,
          finalCount: updatedCards.length
        });
        
        return {
          ...prev,
          cards: updatedCards,
          lastSearchMetadata: prev.lastSearchMetadata ? {
            ...prev.lastSearchMetadata,
            loadedCards: updatedCards.length
          } : null
        };
      });

      // Update pagination through callback
      onPaginationUpdate({
        loadedCards: state.cards.length + newCards.length,
        hasMore: (state.cards.length + newCards.length) < metadata.totalCards,
        isLoadingMore: false,
        currentPage: Math.floor((state.cards.length + newCards.length) / 175) + 1,
      });

      return newCards;
      
    } catch (error) {
      console.error('❌ Load more failed in useSearch:', error);
      throw error;
    }
  }, [state.lastSearchMetadata, state.cards.length, onPaginationUpdate]);

  return {

    ...state,
    searchForCards,
    searchWithAllFilters,
    enhancedSearch,
    loadPopularCards,
    loadRandomCard,
    clearCards,
    handleCollectionSortChange,
    loadMoreCards,
  };
};