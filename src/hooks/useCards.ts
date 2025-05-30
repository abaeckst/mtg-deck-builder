// src/hooks/useCards.ts - Complete working version with exports
import { useState, useEffect, useCallback } from 'react';
import { ScryfallCard } from '../types/card';
import { searchCards, getRandomCard, searchCardsWithFilters, SearchFilters } from '../services/scryfallApi';

export interface UseCardsState {
  cards: ScryfallCard[];
  loading: boolean;
  error: string | null;
  hasMore: boolean;
  selectedCards: Set<string>;
  searchQuery: string;
  totalCards: number;
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
}

const POPULAR_CARDS_QUERY = 'is:commander OR name:"Lightning Bolt" OR name:"Counterspell" OR name:"Sol Ring" OR name:"Path to Exile" OR name:"Swords to Plowshares" OR name:"Birds of Paradise" OR name:"Dark Ritual" OR name:"Giant Growth" OR name:"Ancestral Recall"';

export const useCards = (): UseCardsState & UseCardsActions => {
  const [state, setState] = useState<UseCardsState>({
    cards: [],
    loading: false,
    error: null,
    hasMore: false,
    selectedCards: new Set(),
    searchQuery: '',
    totalCards: 0,
    // Enhanced filtering state
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

  // Clear error when starting new operations
  const clearError = useCallback(() => {
    setState(prev => ({ ...prev, error: null }));
  }, []);

  // Set loading state
  const setLoading = useCallback((loading: boolean) => {
    setState(prev => ({ ...prev, loading }));
  }, []);

  // Search for cards with query and optional format filter - RACE CONDITION SAFE
  const searchForCards = useCallback(async (query: string, format?: string) => {
    // Handle empty query cases
    if (!query.trim()) {
      // If there's a format selected, search for all cards in that format
      if (format && format !== '') {
        // Don't return early - continue with format-only search
        query = '*'; // Use wildcard to get all cards
      } else {
        // No query and no format - clear results
        setState(prev => ({ 
          ...prev, 
          cards: [], 
          searchQuery: '', 
          totalCards: 0,
          selectedCards: new Set() // Clear selection when clearing search
        }));
        return;
      }
    }

    // Create unique search ID to prevent race conditions
    const searchId = Date.now() + Math.random();
    (window as any).currentSearchId = searchId;

    console.log('🔍 SEARCH STARTED:', { 
      searchId: searchId.toFixed(3), 
      query, 
      format: format || 'none' 
    });

    try {
      clearError();
      setLoading(true);

      // Simple rate limiting - wait 150ms between searches
      const now = Date.now();
      const lastSearch = (window as any).lastSearchTime || 0;
      const timeSinceLastSearch = now - lastSearch;
      
      if (timeSinceLastSearch < 150) {
        await new Promise(resolve => setTimeout(resolve, 150 - timeSinceLastSearch));
      }
      
      // Check if this search was cancelled while waiting
      if ((window as any).currentSearchId !== searchId) {
        console.log('🚫 SEARCH CANCELLED:', { 
          searchId: searchId.toFixed(3), 
          query,
          reason: 'superseded by newer search'
        });
        return;
      }
      
      (window as any).lastSearchTime = Date.now();

      // Execute API call
      const response = format && format !== '' 
        ? await searchCardsWithFilters(query, { 
            format: format === 'custom-standard' ? 'standard' : format 
          })
        : await searchCards(query);

      // Check if this search was cancelled while API call was in progress
      if ((window as any).currentSearchId !== searchId) {
        console.log('🚫 SEARCH CANCELLED:', { 
          searchId: searchId.toFixed(3), 
          query,
          reason: 'superseded during API call'
        });
        return;
      }

      console.log('✅ SEARCH SUCCESS:', {
        searchId: searchId.toFixed(3),
        query: query,
        format: format || 'none',
        resultCount: response.data.length,
        firstCard: response.data[0]?.name || 'NO_RESULTS',
        isFormatOnly: query === '*'
      });

      // Only update state if this is still the current search
      setState(prev => ({
        ...prev,
        cards: response.data,
        searchQuery: query === '*' ? `All ${format || 'Cards'}` : query,
        totalCards: response.total_cards,
        hasMore: response.has_more,
        selectedCards: new Set(), // Clear selection on new search
      }));

    } catch (error) {
      // Only show error if this search wasn't cancelled
      if ((window as any).currentSearchId === searchId) {
        let errorMessage = error instanceof Error ? error.message : 'Failed to search cards';
        let isNoResults = false;
        
        // Handle 404 as "no results found" rather than error
        if (errorMessage.includes('404') || errorMessage.includes('No cards found')) {
          errorMessage = 'No cards found matching your search. Try different keywords or filters.';
          isNoResults = true;
          console.log('📭 No results found for search:', query);
        } else {
          console.error('❌ SEARCH ERROR:', {
            searchId: searchId.toFixed(3),
            query: query,
            format: format || 'none',
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
        }));
      }
    } finally {
      // Only clear loading if this is still the current search
      if ((window as any).currentSearchId === searchId) {
        setLoading(false);
      }
    }
  }, [clearError, setLoading]);

  // Load popular/example cards
  const loadPopularCards = useCallback(async () => {
    clearError();
    setLoading(true);

    try {
      const response = await searchCards(POPULAR_CARDS_QUERY);
      setState(prev => ({
        ...prev,
        cards: response.data,
        searchQuery: 'Popular Cards',
        totalCards: response.total_cards,
        hasMore: response.has_more,
        selectedCards: new Set(),
      }));
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Failed to load popular cards';
      setState(prev => ({
        ...prev,
        error: errorMessage,
        cards: [],
        totalCards: 0,
        hasMore: false,
      }));
    } finally {
      setLoading(false);
    }
  }, [clearError, setLoading]);

  // Load a single random card
  const loadRandomCard = useCallback(async () => {
    clearError();
    setLoading(true);

    try {
      const card = await getRandomCard();
      setState(prev => ({
        ...prev,
        cards: [card],
        searchQuery: 'Random Card',
        totalCards: 1,
        hasMore: false,
        selectedCards: new Set(),
      }));
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Failed to load random card';
      setState(prev => ({
        ...prev,
        error: errorMessage,
        cards: [],
        totalCards: 0,
        hasMore: false,
      }));
    } finally {
      setLoading(false);
    }
  }, [clearError, setLoading]);

  // Card selection functions - FIXED Set iteration
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
    setState({
      cards: [],
      loading: false,
      error: null,
      hasMore: false,
      selectedCards: new Set(),
      searchQuery: '',
      totalCards: 0,
      // Enhanced filtering state
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
  }, []);

  // Load popular cards on mount
  useEffect(() => {
    loadPopularCards();
  }, [loadPopularCards]);

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
    
    // Reset search results to popular cards after clearing filters
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

  // Enhanced search function that uses all active filters - FIXED v3 (State Closure)
  const searchWithAllFilters = useCallback(async (query: string, filtersOverride?: any) => {
    // Use provided filters or current state - this fixes the closure issue
    const filters = filtersOverride || state.activeFilters;
    
    console.log('🚀 searchWithAllFilters called:', { query, filters, usingOverride: !!filtersOverride });
    
    // Build comprehensive filter object - FIXED to properly check filter values
    const searchFilters: any = {};
    
    console.log('🔍 Raw filters received:', filters);
    console.log('🔍 Checking format:', filters.format, 'isEmpty?', !filters.format || filters.format === '');
    
    if (filters.format && filters.format !== '') {
      searchFilters.format = filters.format;
      console.log('✅ Adding format filter:', filters.format);
    } else {
      console.log('❌ Skipping format filter - empty or undefined');
    }
    console.log('🔍 Checking colors:', filters.colors, 'length:', filters.colors ? filters.colors.length : 'undefined');
    if (filters.colors && filters.colors.length > 0) {
      searchFilters.colors = filters.colors;
      searchFilters.colorIdentity = filters.colorIdentity;
      console.log('✅ Adding color filter:', filters.colors, filters.colorIdentity);
    } else {
      console.log('❌ Skipping color filter - empty or undefined');
    }
    if (filters.types && filters.types.length > 0) {
      searchFilters.types = filters.types;
      console.log('✅ Adding type filter:', filters.types);
    }
    if (filters.rarity && filters.rarity.length > 0) {
      searchFilters.rarity = filters.rarity;
      console.log('✅ Adding rarity filter:', filters.rarity);
    }
    if (filters.sets && filters.sets.length > 0) {
      searchFilters.sets = filters.sets;
      console.log('✅ Adding sets filter:', filters.sets);
    }
    if (filters.cmc && (filters.cmc.min !== null || filters.cmc.max !== null)) {
      searchFilters.cmc = {};
      if (filters.cmc.min !== null) searchFilters.cmc.min = filters.cmc.min;
      if (filters.cmc.max !== null) searchFilters.cmc.max = filters.cmc.max;
      console.log('✅ Adding CMC filter:', searchFilters.cmc);
    }
    if (filters.power && (filters.power.min !== null || filters.power.max !== null)) {
      searchFilters.power = {};
      if (filters.power.min !== null) searchFilters.power.min = filters.power.min;
      if (filters.power.max !== null) searchFilters.power.max = filters.power.max;
      console.log('✅ Adding power filter:', searchFilters.power);
    }
    if (filters.toughness && (filters.toughness.min !== null || filters.toughness.max !== null)) {
      searchFilters.toughness = {};
      if (filters.toughness.min !== null) searchFilters.toughness.min = filters.toughness.min;
      if (filters.toughness.max !== null) searchFilters.toughness.max = filters.toughness.max;
      console.log('✅ Adding toughness filter:', searchFilters.toughness);
    }

    // Use the same race-condition-safe logic as searchForCards
    const searchId = Date.now() + Math.random();
    (window as any).currentSearchId = searchId;

    // Determine query strategy
    const hasFilters = Object.keys(searchFilters).length > 0;
    const hasQuery = query && query.trim() !== '';
    
    let actualQuery: string;
    if (hasQuery) {
      actualQuery = query.trim();
    } else if (hasFilters) {
      // Use wildcard when we have filters but no search text
      actualQuery = '*';
    } else {
      // No query and no filters - this should not happen, but fallback to popular cards
      console.log('❌ No query and no filters - falling back to popular cards');
      loadPopularCards();
      return;
    }
    
    console.log('🔍 ENHANCED SEARCH:', { 
      searchId: searchId.toFixed(3), 
      originalQuery: query,
      actualQuery: actualQuery,
      filters: searchFilters,
      filterCount: Object.keys(searchFilters).length,
      hasQuery,
      hasFilters
    });

    try {
      clearError();
      setLoading(true);

      // Rate limiting
      const now = Date.now();
      const lastSearch = (window as any).lastSearchTime || 0;
      const timeSinceLastSearch = now - lastSearch;
      
      if (timeSinceLastSearch < 150) {
        await new Promise(resolve => setTimeout(resolve, 150 - timeSinceLastSearch));
      }
      
      if ((window as any).currentSearchId !== searchId) {
        console.log('🚫 ENHANCED SEARCH CANCELLED:', searchId.toFixed(3));
        return;
      }
      
      (window as any).lastSearchTime = Date.now();

      const response = await searchCardsWithFilters(actualQuery, searchFilters);

      if ((window as any).currentSearchId !== searchId) {
        console.log('🚫 ENHANCED SEARCH CANCELLED DURING API:', searchId.toFixed(3));
        return;
      }

      console.log('✅ ENHANCED SEARCH SUCCESS:', {
        searchId: searchId.toFixed(3),
        resultCount: response.data.length
      });

      setState(prev => ({
        ...prev,
        cards: response.data,
        searchQuery: query || 'Filtered Results',
        totalCards: response.total_cards,
        hasMore: response.has_more,
        selectedCards: new Set(),
      }));

    } catch (error) {
      if ((window as any).currentSearchId === searchId) {
        let errorMessage = error instanceof Error ? error.message : 'Failed to search with filters';
        let isNoResults = false;
        
        // Handle 404 as "no results found" rather than error
        if (errorMessage.includes('404') || errorMessage.includes('No cards found')) {
          errorMessage = 'No cards found matching your search criteria. Try adjusting your filters.';
          isNoResults = true;
          console.log('📭 No results found for current filters');
        } else {
          console.error('❌ Search error:', errorMessage);
        }
        
        setState(prev => ({
          ...prev,
          error: isNoResults ? null : errorMessage, // Don't show error state for no results
          cards: [],
          totalCards: 0,
          hasMore: false,
          searchQuery: isNoResults ? 'No results found' : prev.searchQuery,
        }));
      }
    } finally {
      if ((window as any).currentSearchId === searchId) {
        setLoading(false);
      }
    }
  }, [state.activeFilters, clearError, setLoading]);

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
  };
};
