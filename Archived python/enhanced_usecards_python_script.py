#!/usr/bin/env python3

import os
import sys

def update_use_cards():
    """Update useCards.ts with sort integration and subscription system"""
    
    filename = "src/hooks/useCards.ts"
    
    if not os.path.exists(filename):
        print(f"Error: {filename} not found")
        return False
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Make replacements with exact string matching
    updates = [
        # Add sort integration imports
        (
            "import { searchCards, getRandomCard, searchCardsWithFilters, SearchFilters, enhancedSearchCards, getSearchSuggestions } from '../services/scryfallApi';",
            "import { searchCards, getRandomCard, searchCardsWithFilters, SearchFilters, enhancedSearchCards, getSearchSuggestions, searchCardsWithSort } from '../services/scryfallApi';\nimport { useSorting, AreaType, SortCriteria, SortDirection } from './useSorting';",
            "Add sort integration imports"
        ),
        
        # Add sort state to UseCardsState interface
        (
            "  // Enhanced search state\n  searchSuggestions: string[];\n  showSuggestions: boolean;\n  recentSearches: string[];",
            "  // Enhanced search state\n  searchSuggestions: string[];\n  showSuggestions: boolean;\n  recentSearches: string[];\n\n  // Sort integration state\n  lastSearchMetadata: {\n    query: string;\n    filters: any;\n    totalCards: number;\n    loadedCards: number;\n  } | null;",
            "Add sort state to UseCardsState interface"
        ),
        
        # Add sort integration actions
        (
            "  addToSearchHistory: (query: string) => void;\n\n}",
            "  addToSearchHistory: (query: string) => void;\n  // Sort integration actions\n  handleCollectionSortChange: (criteria: SortCriteria, direction: SortDirection) => void;\n\n}",
            "Add sort integration actions"
        ),
        
        # Add sort integration to initial state
        (
            "    // Enhanced search state\n    searchSuggestions: [],\n    showSuggestions: false,\n    recentSearches: [],",
            "    // Enhanced search state\n    searchSuggestions: [],\n    showSuggestions: false,\n    recentSearches: [],\n    // Sort integration state\n    lastSearchMetadata: null,",
            "Add sort integration to initial state"
        ),
        
        # Initialize sort integration after state declaration
        (
            "export const useCards = (): UseCardsState & UseCardsActions => {\n  const [state, setState] = useState<UseCardsState>({",
            "export const useCards = (): UseCardsState & UseCardsActions => {\n  // Initialize sorting integration\n  const { getScryfallSortParams, subscribe, unsubscribe } = useSorting();\n  \n  const [state, setState] = useState<UseCardsState>({",
            "Initialize sort integration after state declaration"
        ),
        
        # Add subscription setup after state initialization
        (
            "  // Load popular cards on mount\n  useEffect(() => {\n    loadPopularCards();\n  }, [loadPopularCards]);",
            "  // Load popular cards on mount\n  useEffect(() => {\n    loadPopularCards();\n  }, [loadPopularCards]);\n\n  // Subscribe to collection sort changes\n  useEffect(() => {\n    const subscriptionId = subscribe((area: AreaType, sortState) => {\n      if (area === 'collection') {\n        console.log('🔄 Collection sort changed:', sortState);\n        // Trigger re-search with new sort parameters\n        if (state.lastSearchMetadata) {\n          handleCollectionSortChange(sortState.criteria, sortState.direction);\n        }\n      }\n    });\n\n    return () => {\n      unsubscribe(subscriptionId);\n    };\n  }, [subscribe, unsubscribe, state.lastSearchMetadata]);",
            "Add subscription setup after state initialization"
        ),
        
        # Add smart re-search logic for collection sort changes
        (
            "  const addToSearchHistory = useCallback((query: string) => {\n    if (!query.trim() || query === '*') return;\n    \n    setState(prev => {\n      const newHistory = [query, ...prev.recentSearches.filter(h => h !== query)].slice(0, 10);\n      return { ...prev, recentSearches: newHistory };\n    });\n  }, []);",
            "  const addToSearchHistory = useCallback((query: string) => {\n    if (!query.trim() || query === '*') return;\n    \n    setState(prev => {\n      const newHistory = [query, ...prev.recentSearches.filter(h => h !== query)].slice(0, 10);\n      return { ...prev, recentSearches: newHistory };\n    });\n  }, []);\n\n  // Handle collection sort changes with smart re-search logic\n  const handleCollectionSortChange = useCallback(async (criteria: SortCriteria, direction: SortDirection) => {\n    const metadata = state.lastSearchMetadata;\n    if (!metadata) {\n      console.log('🔄 No search metadata available for sort change');\n      return;\n    }\n\n    const shouldUseServerSort = metadata.totalCards > metadata.loadedCards;\n    console.log('🔄 Sort change analysis:', {\n      criteria,\n      direction,\n      totalCards: metadata.totalCards,\n      loadedCards: metadata.loadedCards,\n      shouldUseServerSort\n    });\n\n    if (shouldUseServerSort) {\n      console.log('🌐 Using server-side sorting - re-searching with new sort parameters');\n      \n      // Get Scryfall sort parameters\n      const sortParams = getScryfallSortParams('collection');\n      console.log('🔧 Scryfall sort params:', sortParams);\n      \n      // Re-search with same query and filters but new sort\n      try {\n        clearError();\n        setLoading(true);\n        \n        const searchId = Date.now() + Math.random();\n        (window as any).currentSearchId = searchId;\n        \n        // Rate limiting\n        const now = Date.now();\n        const lastSearch = (window as any).lastSearchTime || 0;\n        const timeSinceLastSearch = now - lastSearch;\n        \n        if (timeSinceLastSearch < 150) {\n          await new Promise(resolve => setTimeout(resolve, 150 - timeSinceLastSearch));\n        }\n        \n        if ((window as any).currentSearchId !== searchId) {\n          return;\n        }\n        \n        (window as any).lastSearchTime = Date.now();\n        \n        // Execute search with sort parameters\n        const response = await searchCardsWithFilters(\n          metadata.query, \n          metadata.filters, \n          1, // Reset to page 1 for new sort\n          sortParams.order, \n          sortParams.dir\n        );\n        \n        if ((window as any).currentSearchId !== searchId) {\n          return;\n        }\n        \n        setState(prev => ({\n          ...prev,\n          cards: response.data,\n          totalCards: response.total_cards,\n          hasMore: response.has_more,\n          selectedCards: new Set(),\n          lastSearchMetadata: {\n            ...metadata,\n            totalCards: response.total_cards,\n            loadedCards: response.data.length,\n          },\n        }));\n        \n        console.log('✅ Server-side sort applied successfully');\n        \n      } catch (error) {\n        console.error('❌ Server-side sort failed:', error);\n        // Let client-side sorting handle it as fallback\n      } finally {\n        if ((window as any).currentSearchId === searchId) {\n          setLoading(false);\n        }\n      }\n    } else {\n      console.log('🏠 Using client-side sorting - all results already loaded');\n      // Client-side sorting will be handled by the UI component\n      // No action needed here as the sortCards function in MTGOLayout will handle it\n    }\n  }, [state.lastSearchMetadata, getScryfallSortParams, clearError, setLoading]);",
            "Add smart re-search logic for collection sort changes"
        ),
        
        # Update search functions to store metadata
        (
            "      setState(prev => ({\n        ...prev,\n        cards: response.data,\n        searchQuery: query === '*' ? `All ${format || 'Cards'}` : query,\n        totalCards: response.total_cards,\n        hasMore: response.has_more,\n        selectedCards: new Set(), // Clear selection on new search\n      }));",
            "      setState(prev => ({\n        ...prev,\n        cards: response.data,\n        searchQuery: query === '*' ? `All ${format || 'Cards'}` : query,\n        totalCards: response.total_cards,\n        hasMore: response.has_more,\n        selectedCards: new Set(), // Clear selection on new search\n        lastSearchMetadata: {\n          query,\n          filters: format ? { format: format === 'custom-standard' ? 'standard' : format } : {},\n          totalCards: response.total_cards,\n          loadedCards: response.data.length,\n        },\n      }));",
            "Update search functions to store metadata"
        ),
        
        # Update enhancedSearch to store metadata
        (
            "      setState(prev => ({\n        ...prev,\n        cards: response.data,\n        searchQuery: query === '*' ? 'Filtered Results' : query,\n        totalCards: response.total_cards,\n        hasMore: response.has_more,\n        selectedCards: new Set(),\n        showSuggestions: false,\n      }));",
            "      setState(prev => ({\n        ...prev,\n        cards: response.data,\n        searchQuery: query === '*' ? 'Filtered Results' : query,\n        totalCards: response.total_cards,\n        hasMore: response.has_more,\n        selectedCards: new Set(),\n        showSuggestions: false,\n        lastSearchMetadata: {\n          query,\n          filters,\n          totalCards: response.total_cards,\n          loadedCards: response.data.length,\n        },\n      }));",
            "Update enhancedSearch to store metadata"
        ),
        
        # Update searchWithAllFilters to store metadata
        (
            "      setState(prev => ({\n        ...prev,\n        cards: response.data,\n        searchQuery: query || 'Filtered Results',\n        totalCards: response.total_cards,\n        hasMore: response.has_more,\n        selectedCards: new Set(),\n      }));",
            "      setState(prev => ({\n        ...prev,\n        cards: response.data,\n        searchQuery: query || 'Filtered Results',\n        totalCards: response.total_cards,\n        hasMore: response.has_more,\n        selectedCards: new Set(),\n        lastSearchMetadata: {\n          query: actualQuery,\n          filters: searchFilters,\n          totalCards: response.total_cards,\n          loadedCards: response.data.length,\n        },\n      }));",
            "Update searchWithAllFilters to store metadata"
        ),
        
        # Add handleCollectionSortChange to return object
        (
            "    clearSearchSuggestions,\n    addToSearchHistory,\n\n  };",
            "    clearSearchSuggestions,\n    addToSearchHistory,\n    handleCollectionSortChange,\n\n  };",
            "Add handleCollectionSortChange to return object"
        ),
        
        # Reset metadata in clearCards function
        (
            "      // Enhanced search state\n      searchSuggestions: [],\n      showSuggestions: false,\n      recentSearches: [],",
            "      // Enhanced search state\n      searchSuggestions: [],\n      showSuggestions: false,\n      recentSearches: [],\n      // Sort integration state\n      lastSearchMetadata: null,",
            "Reset metadata in clearCards function"
        )
    ]
    
    for old_str, new_str, description in updates:
        if old_str in content:
            content = content.replace(old_str, new_str)
            print(f"✅ {description}")
        else:
            print(f"❌ Could not find: {description}")
            return False
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Successfully updated {filename}")
    return True

if __name__ == "__main__":
    success = update_use_cards()
    sys.exit(0 if success else 1)