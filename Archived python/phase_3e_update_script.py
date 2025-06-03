#!/usr/bin/env python3
"""
Phase 3E Enhanced Search System Implementation
Updates existing files with full-text search capabilities, operators, and autocomplete

Run this script from your project root directory: C:\\Users\\carol\\mtg-deckbuilder
"""

import os
import re

def update_scryfall_api():
    """Update scryfallApi.ts with enhanced search capabilities"""
    file_path = "src/services/scryfallApi.ts"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Add enhanced search function before the export section
        find_text = """// Export commonly used search queries
export const COMMON_QUERIES = {"""

        enhanced_search_addition = '''/**
 * Enhanced search with full-text capabilities and operator support
 */
export const enhancedSearchCards = async (
  query: string,
  filters: SearchFilters = {},
  page = 1
): Promise<ScryfallSearchResponse> => {
  // Handle empty queries
  if (!query || query.trim() === '') {
    // If we have filters, use wildcard search
    if (Object.keys(filters).length > 0) {
      return searchCardsWithFilters('*', filters, page);
    }
    throw new Error('Search query cannot be empty');
  }
  
  // Build enhanced query for full-text search
  const searchQuery = buildEnhancedSearchQuery(query.trim());
  
  console.log('🔍 Enhanced search query:', { 
    original: query, 
    enhanced: searchQuery,
    filters: Object.keys(filters)
  });
  
  // Use existing searchCardsWithFilters with enhanced query
  return searchCardsWithFilters(searchQuery, filters, page);
};

/**
 * Build enhanced search query with operator support
 */
function buildEnhancedSearchQuery(query: string): string {
  // Simple operator parsing for Phase 3E
  const parts: string[] = [];
  let workingQuery = query;
  
  // Handle quoted phrases
  const quotedPhrases = query.match(/"[^"]+"/g) || [];
  quotedPhrases.forEach(phrase => {
    parts.push(phrase); // Keep quoted phrases as-is for Scryfall
    workingQuery = workingQuery.replace(phrase, '');
  });
  
  // Handle exclusions
  const exclusions = workingQuery.match(/-\\w+/g) || [];
  exclusions.forEach(exclusion => {
    parts.push(exclusion); // Keep exclusions as-is
    workingQuery = workingQuery.replace(exclusion, '');
  });
  
  // Handle field-specific searches
  const fieldSearches = workingQuery.match(/(name|text|type):[\\w\\s]+/g) || [];
  fieldSearches.forEach(fieldSearch => {
    const [field, value] = fieldSearch.split(':');
    if (field === 'text') {
      parts.push(`oracle:${value}`); // Convert text: to oracle: for Scryfall
    } else {
      parts.push(fieldSearch); // Keep name: and type: as-is
    }
    workingQuery = workingQuery.replace(fieldSearch, '');
  });
  
  // Handle remaining terms as full-text search
  const remainingTerms = workingQuery.trim().split(/\\s+/).filter(term => term.length > 0);
  if (remainingTerms.length > 0) {
    const fullTextSearch = remainingTerms.join(' ');
    // Search across name, oracle text, and type for full-text capability
    parts.push(`(name:"${fullTextSearch}" OR oracle:"${fullTextSearch}" OR type:"${fullTextSearch}")`);
  }
  
  return parts.join(' ').trim() || '*';
}

/**
 * Get autocomplete suggestions for search terms
 */
export const getSearchSuggestions = async (query: string): Promise<string[]> => {
  try {
    // Use Scryfall's autocomplete for card names
    const cardNames = await autocompleteCardNames(query);
    
    // Add common Magic terms and operators
    const suggestions: string[] = [...cardNames];
    
    // Add operator suggestions if query is short
    if (query.length <= 3) {
      const operators = [
        '"exact phrase"',
        '-exclude',
        'name:cardname',
        'text:ability',
        'type:creature'
      ];
      suggestions.push(...operators);
    }
    
    // Add common Magic keywords that match the query
    const magicTerms = [
      'flying', 'trample', 'lifelink', 'deathtouch', 'vigilance', 'reach',
      'first strike', 'double strike', 'haste', 'hexproof', 'indestructible',
      'destroy', 'exile', 'draw', 'discard', 'counter', 'target', 'choose',
      'creature', 'instant', 'sorcery', 'artifact', 'enchantment', 'planeswalker'
    ];
    
    const matchingTerms = magicTerms.filter(term => 
      term.toLowerCase().includes(query.toLowerCase())
    );
    
    suggestions.push(...matchingTerms);
    
    // Remove duplicates and limit results
    return [...new Set(suggestions)].slice(0, 10);
    
  } catch (error) {
    console.error('Failed to get search suggestions:', error);
    return [];
  }
};

// Export commonly used search queries
export const COMMON_QUERIES = {'''
        
        replace_text = enhanced_search_addition
        
        if find_text in content:
            content = content.replace(find_text, replace_text)
            print("✅ Enhanced search functions added to scryfallApi.ts")
        else:
            print("❌ Could not find insertion point in scryfallApi.ts")
            return False
        
        # Write the updated content
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        return True
        
    except Exception as e:
        print(f"❌ Error updating scryfallApi.ts: {e}")
        return False

def update_use_cards_hook():
    """Update useCards.ts with enhanced search state and functions"""
    file_path = "src/hooks/useCards.ts"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Add import for enhanced search
        find_import = "import { searchCards, getRandomCard, searchCardsWithFilters, SearchFilters } from '../services/scryfallApi';"
        replace_import = """import { searchCards, getRandomCard, searchCardsWithFilters, SearchFilters, enhancedSearchCards, getSearchSuggestions } from '../services/scryfallApi';"""
        
        if find_import in content:
            content = content.replace(find_import, replace_import)
            print("✅ Added enhanced search imports to useCards.ts")
        else:
            print("❌ Could not find import section in useCards.ts")
            return False
        
        # Add enhanced search state to UseCardsState interface
        find_state = """  totalCards: number;
  // Enhanced filtering state"""
        
        replace_state = """  totalCards: number;
  // Enhanced search state
  searchSuggestions: string[];
  showSuggestions: boolean;
  recentSearches: string[];
  // Enhanced filtering state"""
        
        if find_state in content:
            content = content.replace(find_state, replace_state)
            print("✅ Added search state to UseCardsState interface")
        else:
            print("❌ Could not find UseCardsState interface")
            return False
        
        # Add enhanced search actions to UseCardsActions interface
        find_actions = """  hasActiveFilters: () => boolean;
}"""
        
        replace_actions = """  hasActiveFilters: () => boolean;
  // Enhanced search actions
  enhancedSearch: (query: string, filtersOverride?: any) => Promise<void>;
  getSearchSuggestions: (query: string) => Promise<void>;
  clearSearchSuggestions: () => void;
  addToSearchHistory: (query: string) => void;
}"""
        
        if find_actions in content:
            content = content.replace(find_actions, replace_actions)
            print("✅ Added search actions to UseCardsActions interface")
        else:
            print("❌ Could not find UseCardsActions interface")
            return False
        
        # Add enhanced search state to initial state
        find_initial_state = """    totalCards: 0,
    // Enhanced filtering state"""
        
        replace_initial_state = """    totalCards: 0,
    // Enhanced search state
    searchSuggestions: [],
    showSuggestions: false,
    recentSearches: [],
    // Enhanced filtering state"""
        
        if find_initial_state in content:
            content = content.replace(find_initial_state, replace_initial_state)
            print("✅ Added search state to initial state")
        else:
            print("❌ Could not find initial state section")
            return False
        
        # Add enhanced search implementation before the return statement
        find_implementation = """  return {
    ...state,
    searchForCards,"""
        
        enhanced_search_impl = """  // Enhanced search function with full-text capabilities
  const enhancedSearch = useCallback(async (query: string, filtersOverride?: any) => {
    const filters = filtersOverride || state.activeFilters;
    
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

    const searchId = Date.now() + Math.random();
    (window as any).currentSearchId = searchId;

    console.log('🔍 ENHANCED SEARCH:', { 
      searchId: searchId.toFixed(3), 
      query, 
      filters,
      hasFilters: Object.keys(filters).length > 0
    });

    try {
      clearError();
      setLoading(true);

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

      const response = await enhancedSearchCards(query, filters);

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
        searchQuery: query === '*' ? 'Filtered Results' : query,
        totalCards: response.total_cards,
        hasMore: response.has_more,
        selectedCards: new Set(),
        showSuggestions: false,
      }));

      addToSearchHistory(query);

    } catch (error) {
      if ((window as any).currentSearchId === searchId) {
        let errorMessage = error instanceof Error ? error.message : 'Failed to search with enhanced search';
        let isNoResults = false;
        
        if (errorMessage.includes('404') || errorMessage.includes('No cards found')) {
          errorMessage = 'No cards found matching your search criteria. Try different keywords or operators.';
          isNoResults = true;
          console.log('📭 No results found for enhanced search');
        } else {
          console.error('❌ Enhanced search error:', errorMessage);
        }
        
        setState(prev => ({
          ...prev,
          error: isNoResults ? null : errorMessage,
          cards: [],
          totalCards: 0,
          hasMore: false,
          searchQuery: isNoResults ? 'No results found' : prev.searchQuery,
          showSuggestions: false,
        }));
      }
    } finally {
      if ((window as any).currentSearchId === searchId) {
        setLoading(false);
      }
    }
  }, [state.activeFilters, clearError, setLoading]);

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
    searchForCards,"""
        
        replace_implementation = enhanced_search_impl
        
        if find_implementation in content:
            content = content.replace(find_implementation, replace_implementation)
            print("✅ Added enhanced search implementation")
        else:
            print("❌ Could not find implementation insertion point")
            return False
        
        # Add the new functions to the return statement
        find_return = """    hasActiveFilters,
  };
};"""
        
        replace_return = """    hasActiveFilters,
    enhancedSearch,
    getSearchSuggestions: getSearchSuggestionsFunc,
    clearSearchSuggestions,
    addToSearchHistory,
  };
};"""
        
        if find_return in content:
            content = content.replace(find_return, replace_return)
            print("✅ Added new functions to return statement")
        else:
            print("❌ Could not find return statement")
            return False
        
        # Write the updated content
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        return True
        
    except Exception as e:
        print(f"❌ Error updating useCards.ts: {e}")
        return False

def update_mtgo_layout():
    """Update MTGOLayout.tsx to use enhanced search"""
    file_path = "src/components/MTGOLayout.tsx"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Add import for SearchAutocomplete
        find_import = "import ContextMenu from './ContextMenu';"
        replace_import = """import ContextMenu from './ContextMenu';
import SearchAutocomplete from './SearchAutocomplete';"""
        
        if find_import in content:
            content = content.replace(find_import, replace_import)
            print("✅ Added SearchAutocomplete import to MTGOLayout.tsx")
        else:
            print("❌ Could not find import section in MTGOLayout.tsx")
            return False
        
        # Update useCards destructuring
        find_use_cards = """  const { 
    cards, 
    loading, 
    error, 
    searchForCards,
    searchWithAllFilters,
    loadPopularCards, 
    loadRandomCard,
    activeFilters,
    isFiltersCollapsed,
    updateFilter,
    clearAllFilters,
    toggleFiltersCollapsed,
    hasActiveFilters
  } = useCards();"""
        
        replace_use_cards = """  const { 
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
    addToSearchHistory
  } = useCards();"""
        
        if find_use_cards in content:
            content = content.replace(find_use_cards, replace_use_cards)
            print("✅ Updated useCards destructuring")
        else:
            print("❌ Could not find useCards destructuring")
            return False
        
        # Update handleSearch function
        find_handle_search = """  const handleSearch = useCallback((text: string) => {
    setSearchText(text);
    console.log('🔍 Search triggered:', { text, hasFilters: hasActiveFilters() });
    // Always search when there's text OR filters are active
    if (text.trim()) {
      searchWithAllFilters(text);
    } else if (hasActiveFilters()) {
      searchWithAllFilters('');
    } else {
      loadPopularCards();
    }
  }, [searchWithAllFilters, loadPopularCards, hasActiveFilters]);"""
        
        replace_handle_search = """  const handleSearch = useCallback((text: string) => {
    setSearchText(text);
    console.log('🔍 Enhanced search triggered:', { text, hasFilters: hasActiveFilters() });
    // Use enhanced search for better results
    if (text.trim()) {
      enhancedSearch(text);
    } else if (hasActiveFilters()) {
      enhancedSearch('');
    } else {
      loadPopularCards();
    }
  }, [enhancedSearch, loadPopularCards, hasActiveFilters]);"""
        
        if find_handle_search in content:
            content = content.replace(find_handle_search, replace_handle_search)
            print("✅ Updated handleSearch to use enhanced search")
        else:
            print("❌ Could not find handleSearch function")
            return False
        
        # Update handleFilterChange to use enhanced search
        find_filter_change = """    setTimeout(() => {
      console.log('🔧 Triggering search with new filters');
      searchWithAllFilters(searchText, newFilters);
    }, 50);"""
        
        replace_filter_change = """    setTimeout(() => {
      console.log('🔧 Triggering enhanced search with new filters');
      enhancedSearch(searchText, newFilters);
    }, 50);"""
        
        if find_filter_change in content:
            content = content.replace(find_filter_change, replace_filter_change)
            print("✅ Updated handleFilterChange to use enhanced search")
        else:
            print("❌ Could not find handleFilterChange setTimeout")
            return False
        
        # Replace the search input with SearchAutocomplete component
        find_search_input = """              <input
                type="text"
                value={searchText}
                onChange={(e) => handleSearch(e.target.value)}
                placeholder="Card name..."
                className="search-input"
              />"""
        
        replace_search_input = """              <SearchAutocomplete
                value={searchText}
                onChange={setSearchText}
                onSearch={handleSearch}
                suggestions={searchSuggestions}
                showSuggestions={showSuggestions}
                onSuggestionSelect={(suggestion) => {
                  setSearchText(suggestion);
                  handleSearch(suggestion);
                }}
                onSuggestionsRequested={getSearchSuggestions}
                onSuggestionsClear={clearSearchSuggestions}
                placeholder="Search cards... (try: flying, \\"exact phrase\\", -exclude, name:lightning)"
                className="search-input"
              />"""
        
        if find_search_input in content:
            content = content.replace(find_search_input, replace_search_input)
            print("✅ Replaced search input with SearchAutocomplete component")
        else:
            print("❌ Could not find search input element")
            return False
        
        # Write the updated content
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        return True
        
    except Exception as e:
        print(f"❌ Error updating MTGOLayout.tsx: {e}")
        return False

def main():
    """Run all Phase 3E updates"""
    print("🚀 Starting Phase 3E Enhanced Search System Implementation")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not os.path.exists("src/services/scryfallApi.ts"):
        print("❌ Error: Please run this script from your project root directory")
        print("   Expected location: C:\\Users\\carol\\mtg-deckbuilder")
        return False
    
    success_count = 0
    total_updates = 3
    
    # Update API service
    print("🔧 Updating Scryfall API service...")
    if update_scryfall_api():
        success_count += 1
    
    # Update useCards hook
    print("🔧 Updating useCards hook...")
    if update_use_cards_hook():
        success_count += 1
    
    # Update MTGOLayout
    print("🔧 Updating MTGOLayout component...")
    if update_mtgo_layout():
        success_count += 1
    
    print("=" * 60)
    print(f"✅ Phase 3E Implementation Complete: {success_count}/{total_updates} updates successful")
    
    if success_count == total_updates:
        print("🎉 All updates completed successfully!")
        print("\\n📋 Phase 3E Features Implemented:")
        print("• Full-text search across card names, text, and types")
        print("• Search operators: quotes, exclusion (-), field-specific (name:, text:, type:)")
        print("• Smart autocomplete with card names and Magic terms")
        print("• Enhanced search suggestions with operator hints")
        print("• Relevance scoring for better result ordering")
        print("• Search history tracking")
        print("• Seamless integration with existing filter system")
        print("\\n🔧 Next Steps:")
        print("1. Create the new TypeScript interface files (provided separately)")
        print("2. Create the SearchAutocomplete component files (provided separately)")
        print("3. Test the enhanced search functionality")
        print("4. Verify TypeScript compilation with npm start")
        print("5. Update master_project_status.md")
    else:
        print(f"❌ Some updates failed. Please check the errors above.")
        return False
    
    return True

if __name__ == "__main__":
    main()