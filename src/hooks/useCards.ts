// src/hooks/useCards.ts - Remove unused import warning
import { useState, useEffect, useCallback } from 'react';
import { ScryfallCard } from '../types/card';
import { searchCards, getRandomCard } from '../services/scryfallApi';

export interface UseCardsState {
  cards: ScryfallCard[];
  loading: boolean;
  error: string | null;
  hasMore: boolean;
  selectedCards: Set<string>;
  searchQuery: string;
  totalCards: number;
}

export interface UseCardsActions {
  searchForCards: (query: string) => Promise<void>;
  loadPopularCards: () => Promise<void>;
  loadRandomCard: () => Promise<void>;
  selectCard: (cardId: string) => void;
  deselectCard: (cardId: string) => void;
  clearSelection: () => void;
  isCardSelected: (cardId: string) => boolean;
  getSelectedCardsData: () => ScryfallCard[];
  clearCards: () => void;
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
  });

  // Clear error when starting new operations
  const clearError = useCallback(() => {
    setState(prev => ({ ...prev, error: null }));
  }, []);

  // Set loading state
  const setLoading = useCallback((loading: boolean) => {
    setState(prev => ({ ...prev, loading }));
  }, []);

  // Search for cards with query
  const searchForCards = useCallback(async (query: string) => {
    if (!query.trim()) {
      setState(prev => ({ 
        ...prev, 
        cards: [], 
        searchQuery: '', 
        totalCards: 0,
        selectedCards: new Set() // Clear selection when clearing search
      }));
      return;
    }

    clearError();
    setLoading(true);

    try {
      const response = await searchCards(query);
      setState(prev => ({
        ...prev,
        cards: response.data,
        searchQuery: query,
        totalCards: response.total_cards,
        hasMore: response.has_more,
        selectedCards: new Set(), // Clear selection on new search
      }));
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Failed to search cards';
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
    });
  }, []);

  // Load popular cards on mount
  useEffect(() => {
    loadPopularCards();
  }, [loadPopularCards]);

  return {
    ...state,
    searchForCards,
    loadPopularCards,
    loadRandomCard,
    selectCard,
    deselectCard,
    clearSelection,
    isCardSelected,
    getSelectedCardsData,
    clearCards,
  };
};