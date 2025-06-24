// src/hooks/useSearchSuggestions.ts - Search autocomplete and history management
import { useState, useCallback } from 'react';
import { getSearchSuggestions } from '../services/scryfallApi';

export interface SearchSuggestionsState {
  searchSuggestions: string[];
  showSuggestions: boolean;
  recentSearches: string[];
}

export interface SearchSuggestionsActions {
  getSearchSuggestions: (query: string) => Promise<void>;
  clearSearchSuggestions: () => void;
  addToSearchHistory: (query: string) => void;
}

export const useSearchSuggestions = (): SearchSuggestionsState & SearchSuggestionsActions => {
  const [state, setState] = useState<SearchSuggestionsState>({
    searchSuggestions: [],
    showSuggestions: false,
    recentSearches: [],
  });

  // Search suggestions
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

  return {
    ...state,
    getSearchSuggestions: getSearchSuggestionsFunc,
    clearSearchSuggestions,
    addToSearchHistory,
  };
};