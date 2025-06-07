#!/usr/bin/env python3
"""
MTG Deck Builder - useCards Hook Refactoring Script
Extracts focused hooks from useCards.ts following Code Organization Guide recommendations
"""

import os
import shutil
from pathlib import Path

def create_backup():
    """Create backup of original useCards.ts"""
    src_path = Path("src/hooks/useCards.ts")
    backup_path = Path("src/hooks/useCards.ts.backup")
    
    if src_path.exists():
        shutil.copy2(src_path, backup_path)
        print(f"✅ Created backup: {backup_path}")
    else:
        print(f"❌ Source file not found: {src_path}")
        return False
    return True

def create_use_search_hook():
    """Create the useSearch.ts hook"""
    content = '''// src/hooks/useSearch.ts - Core search and API communication
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
}

const POPULAR_CARDS_QUERY = 'type:creature legal:standard';

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
}

export const useSearch = ({
  activeFilters,
  hasActiveFilters,
  onPaginationStateChange,
  onPaginationUpdate,
  resetPagination,
  addToSearchHistory
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
    sortOrder = 'name',
    sortDirection: 'asc' | 'desc' = 'asc'
  ) => {
    console.log('🔍 SIMPLIFIED SEARCH:', { query, filters, sort: { sortOrder, sortDirection } });

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
      console.log('🔍 Calling searchCardsWithPagination with sort:', { sortOrder, sortDirection });
      const paginationResult = await searchCardsWithPagination(
        query, 
        filters, 
        sortOrder, 
        sortDirection
      );

      console.log('✅ SEARCH SUCCESS:', {
        initialResultCount: paginationResult.initialResults.length,
        totalAvailable: paginationResult.totalCards,
        hasMore: paginationResult.hasMore,
        sortApplied: { sortOrder, sortDirection }
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
      await searchWithPagination(POPULAR_CARDS_QUERY, {});
      setState(prev => ({
        ...prev,
        searchQuery: 'Popular Cards',
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
          searchQuery: 'Popular Cards',
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
    
    await searchWithPagination(actualQuery, searchFilters);
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

    await searchWithPagination(query, filters as SearchFilters);
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

  return {
    ...state,
    searchForCards,
    searchWithAllFilters,
    enhancedSearch,
    loadPopularCards,
    loadRandomCard,
    clearCards,
    handleCollectionSortChange,
  };
};
'''
    
    file_path = Path("src/hooks/useSearch.ts")
    file_path.write_text(content, encoding='utf-8')
    print(f"✅ Created: {file_path}")

def create_use_pagination_hook():
    """Create the usePagination.ts hook"""
    content = '''// src/hooks/usePagination.ts - Progressive loading and Load More functionality
import { useState, useCallback } from 'react';
import { ScryfallCard, PaginatedSearchState } from '../types/card';
import { loadMoreResults } from '../services/scryfallApi';

export interface PaginationState {
  pagination: {
    totalCards: number;
    loadedCards: number;
    hasMore: boolean;
    isLoadingMore: boolean;
    currentPage: number;
  };
}

export interface PaginationActions {
  loadMoreResultsAction: () => Promise<void>;
  resetPagination: () => void;
}

interface UsePaginationProps {
  cards: ScryfallCard[];
  onCardsUpdate: (cards: ScryfallCard[]) => void;
  onErrorUpdate: (error: string | null) => void;
}

export const usePagination = ({
  cards,
  onCardsUpdate,
  onErrorUpdate
}: UsePaginationProps): PaginationState & PaginationActions & {
  setPaginationState: (state: PaginatedSearchState | null) => void;
  updatePagination: (update: Partial<PaginationState['pagination']>) => void;
} => {
  // Internal pagination state for progressive loading
  const [paginationState, setPaginationState] = useState<PaginatedSearchState | null>(null);
  
  const [pagination, setPagination] = useState({
    totalCards: 0,
    loadedCards: 0,
    hasMore: false,
    isLoadingMore: false,
    currentPage: 1,
  });

  // Reset pagination state
  const resetPagination = useCallback(() => {
    setPaginationState(null);
    setPagination({
      totalCards: 0,
      loadedCards: 0,
      hasMore: false,
      isLoadingMore: false,
      currentPage: 1,
    });
  }, []);

  // Update pagination state
  const updatePagination = useCallback((update: Partial<typeof pagination>) => {
    setPagination(prev => ({ ...prev, ...update }));
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
    setPagination(prev => ({ ...prev, isLoadingMore: true }));
    
    // Update pagination state
    setPaginationState(prev => prev ? { ...prev, isLoadingMore: true } : null);

    try {
      const newCards = await loadMoreResults(
        paginationState,
        (loaded, total) => {
          // Progress callback
          setPagination(prev => ({ ...prev, loadedCards: loaded }));
        }
      );

      // Update cards and pagination state
      const updatedCards = [...cards, ...newCards];
      const newLoadedCount = updatedCards.length;
      const stillHasMore = newLoadedCount < paginationState.totalCards;
      
      onCardsUpdate(updatedCards);
      
      setPagination(prev => ({
        ...prev,
        loadedCards: newLoadedCount,
        hasMore: stillHasMore,
        isLoadingMore: false,
        currentPage: paginationState.currentPage + 1,
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
      
      setPagination(prev => ({ ...prev, isLoadingMore: false }));
      setPaginationState(prev => prev ? { ...prev, isLoadingMore: false } : null);
      
      const errorMessage = error instanceof Error ? error.message : 'Failed to load more results';
      onErrorUpdate(errorMessage);
    }
  }, [paginationState, cards, onCardsUpdate, onErrorUpdate]);

  return {
    pagination,
    loadMoreResultsAction,
    resetPagination,
    setPaginationState,
    updatePagination,
  };
};
'''
    
    file_path = Path("src/hooks/usePagination.ts")
    file_path.write_text(content, encoding='utf-8')
    print(f"✅ Created: {file_path}")

def create_use_card_selection_hook():
    """Create the useCardSelection.ts hook"""
    content = '''// src/hooks/useCardSelection.ts - Card selection state management
import { useState, useCallback } from 'react';
import { ScryfallCard } from '../types/card';

export interface CardSelectionState {
  selectedCards: Set<string>;
}

export interface CardSelectionActions {
  selectCard: (cardId: string) => void;
  deselectCard: (cardId: string) => void;
  clearSelection: () => void;
  isCardSelected: (cardId: string) => boolean;
  getSelectedCardsData: (cards: ScryfallCard[]) => ScryfallCard[];
}

export const useCardSelection = (): CardSelectionState & CardSelectionActions => {
  const [selectedCards, setSelectedCards] = useState<Set<string>>(new Set());

  // Card selection functions
  const selectCard = useCallback((cardId: string) => {
    setSelectedCards(prev => {
      const newSelected = new Set(prev);
      newSelected.add(cardId);
      return newSelected;
    });
  }, []);

  const deselectCard = useCallback((cardId: string) => {
    setSelectedCards(prev => {
      const newSelected = new Set(prev);
      newSelected.delete(cardId);
      return newSelected;
    });
  }, []);

  const clearSelection = useCallback(() => {
    setSelectedCards(new Set());
  }, []);

  const isCardSelected = useCallback((cardId: string): boolean => {
    return selectedCards.has(cardId);
  }, [selectedCards]);

  const getSelectedCardsData = useCallback((cards: ScryfallCard[]): ScryfallCard[] => {
    return cards.filter(card => selectedCards.has(card.id));
  }, [selectedCards]);

  return {
    selectedCards,
    selectCard,
    deselectCard,
    clearSelection,
    isCardSelected,
    getSelectedCardsData,
  };
};