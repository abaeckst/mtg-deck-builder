#!/usr/bin/env python3
"""
Fix 2: Set Filter Addition
Adds complete set filtering functionality with search and multi-select checkboxes
Updates both useCards.ts and MTGOLayout.tsx
"""

import re
import os

def add_set_filter_to_use_cards():
    """Add set filter state management to useCards.ts"""
    file_path = "src/hooks/useCards.ts"
    
    if not os.path.exists(file_path):
        print(f"❌ ERROR: File {file_path} not found!")
        return False
    
    print(f"🔧 Reading {file_path}...")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Add set search state to UseCardsState interface
        old_interface = """export interface UseCardsState {
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
  recentSearches: string[];"""
        
        new_interface = """export interface UseCardsState {
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
  // Set filter state
  availableSets: any[];
  setSearchText: string;
  filteredSets: any[];"""
        
        if old_interface in content:
            content = content.replace(old_interface, new_interface)
            print("✅ Added set filter state to UseCardsState interface")
        else:
            print("⚠️  Could not find UseCardsState interface pattern")
        
        # Add imports for set functions
        old_import = """import { searchCards, getRandomCard, searchCardsWithFilters, SearchFilters, enhancedSearchCards, getSearchSuggestions } from '../services/scryfallApi';"""
        
        new_import = """import { searchCards, getRandomCard, searchCardsWithFilters, SearchFilters, enhancedSearchCards, getSearchSuggestions, getSets } from '../services/scryfallApi';"""
        
        if old_import in content:
            content = content.replace(old_import, new_import)
            print("✅ Added getSets import")
        else:
            print("⚠️  Could not find import pattern, getSets may need to be imported manually")
        
        # Add set filter actions to UseCardsActions interface
        old_actions = """export interface UseCardsActions {
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
}"""
        
        new_actions = """export interface UseCardsActions {
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
  // Set filter actions
  updateSetSearchText: (text: string) => void;
  toggleSetSelection: (setCode: string) => void;
}"""
        
        if old_actions in content:
            content = content.replace(old_actions, new_actions)
            print("✅ Added set filter actions to UseCardsActions interface")
        else:
            print("⚠️  Could not find UseCardsActions interface pattern")
        
        # Add set filter state initialization
        old_state_init = """    // Enhanced filtering state
    activeFilters: {
      format: 'standard',
      colors: [],
      colorIdentity: 'exact',
      types: [],
      rarity: [],
      sets: [],
      cmc: { min: null, max: null },
      power: { min: null, max: null },
      toughness: { min: null, max: null },
    },
    isFiltersCollapsed: false,"""
        
        new_state_init = """    // Enhanced filtering state
    activeFilters: {
      format: 'standard',
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
    // Set filter state
    availableSets: [],
    setSearchText: '',
    filteredSets: [],"""
        
        if old_state_init in content:
            content = content.replace(old_state_init, new_state_init)
            print("✅ Added set filter state initialization")
        else:
            print("⚠️  Could not find state initialization pattern")
        
        # Add set loading effect near the end of useCards function
        old_effect = """  // Load popular cards on mount
  useEffect(() => {
    loadPopularCards();
  }, [loadPopularCards]);"""
        
        new_effect = """  // Load popular cards on mount
  useEffect(() => {
    loadPopularCards();
  }, [loadPopularCards]);

  // Load sets on mount
  useEffect(() => {
    getSets().then(sets => {
      setState(prev => ({
        ...prev,
        availableSets: sets,
        filteredSets: sets.slice(0, 20), // Show first 20 initially
      }));
    }).catch(error => {
      console.error('Failed to load sets:', error);
    });
  }, []);

  // Filter sets based on search
  useEffect(() => {
    if (!state.setSearchText.trim()) {
      setState(prev => ({
        ...prev,
        filteredSets: prev.availableSets.slice(0, 20),
      }));
    } else {
      const searchTerm = state.setSearchText.toLowerCase();
      const filtered = state.availableSets.filter(set =>
        set.name.toLowerCase().includes(searchTerm) ||
        set.code.toLowerCase().includes(searchTerm)
      );
      setState(prev => ({
        ...prev,
        filteredSets: filtered.slice(0, 20),
      }));
    }
  }, [state.setSearchText, state.availableSets]);"""
        
        if old_effect in content:
            content = content.replace(old_effect, new_effect)
            print("✅ Added set loading and filtering effects")
        else:
            print("⚠️  Could not find useEffect pattern for loading")
        
        # Add set filter functions before the return statement
        old_return_section = """  const addToSearchHistory = useCallback((query: string) => {
    if (!query.trim() || query === '*') return;
    
    setState(prev => {
      const newHistory = [query, ...prev.recentSearches.filter(h => h !== query)].slice(0, 10);
      return { ...prev, recentSearches: newHistory };
    });
  }, []);

  return {"""
        
        new_return_section = """  const addToSearchHistory = useCallback((query: string) => {
    if (!query.trim() || query === '*') return;
    
    setState(prev => {
      const newHistory = [query, ...prev.recentSearches.filter(h => h !== query)].slice(0, 10);
      return { ...prev, recentSearches: newHistory };
    });
  }, []);

  // Set filter functions
  const updateSetSearchText = useCallback((text: string) => {
    setState(prev => ({ ...prev, setSearchText: text }));
  }, []);

  const toggleSetSelection = useCallback((setCode: string) => {
    const newSets = state.activeFilters.sets.includes(setCode)
      ? state.activeFilters.sets.filter(code => code !== setCode)
      : [...state.activeFilters.sets, setCode];
    
    updateFilter('sets', newSets);
    
    // Trigger search with updated filters
    setTimeout(() => {
      enhancedSearch(state.searchQuery || '', {
        ...state.activeFilters,
        sets: newSets
      });
    }, 50);
  }, [state.activeFilters.sets, updateFilter, enhancedSearch, state.searchQuery, state.activeFilters]);

  return {"""
        
        if old_return_section in content:
            content = content.replace(old_return_section, new_return_section)
            print("✅ Added set filter functions")
        else:
            print("⚠️  Could not find return section pattern")
        
        # Add set filter actions to return object
        old_return_obj = """    enhancedSearch,
    getSearchSuggestions: getSearchSuggestionsFunc,
    clearSearchSuggestions,
    addToSearchHistory,
  };"""
        
        new_return_obj = """    enhancedSearch,
    getSearchSuggestions: getSearchSuggestionsFunc,
    clearSearchSuggestions,
    addToSearchHistory,
    updateSetSearchText,
    toggleSetSelection,
  };"""
        
        if old_return_obj in content:
            content = content.replace(old_return_obj, new_return_obj)
            print("✅ Added set filter actions to return object")
        else:
            print("⚠️  Could not find return object pattern")
        
        # Write the updated content back to file
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        
        print(f"✅ SUCCESS: Set filter state management added to {file_path}")
        return True
        
    except Exception as e:
        print(f"❌ ERROR: Failed to update {file_path}: {str(e)}")
        return False

def add_set_filter_ui():
    """Add set filter UI to MTGOLayout.tsx"""
    file_path = "src/components/MTGOLayout.tsx"
    
    if not os.path.exists(file_path):
        print(f"❌ ERROR: File {file_path} not found!")
        return False
    
    print(f"🔧 Reading {file_path}...")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Add set filter state destructuring
        old_destructuring = """  const { 
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
        
        new_destructuring = """  const { 
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
    availableSets,
    setSearchText,
    filteredSets,
    updateSetSearchText,
    toggleSetSelection
  } = useCards();"""
        
        if old_destructuring in content:
            content = content.replace(old_destructuring, new_destructuring)
            print("✅ Added set filter state destructuring")
        else:
            print("⚠️  Could not find useCards destructuring pattern")
        
        # Add set filter UI after Card Types and before Rarity
        old_ui_section = """            {/* Card Types Group */}
            <div className="filter-group">
              <label>Card Types</label>
              <div className="multi-select-grid">
                {['Creature', 'Instant', 'Sorcery', 'Artifact', 'Enchantment', 'Planeswalker', 'Land'].map((type: string) => (
                  <button
                    key={type}
                    className={`type-button ${activeFilters.types.includes(type.toLowerCase()) ? 'selected' : ''}`}
                    onClick={() => {
                      const newTypes = activeFilters.types.includes(type.toLowerCase())
                        ? activeFilters.types.filter((t: string) => t !== type.toLowerCase())
                        : [...activeFilters.types, type.toLowerCase()];
                      handleFilterChange('types', newTypes);
                    }}
                  >
                    {type}
                  </button>
                ))}
              </div>
            </div>
            
            {/* Rarity Group */}"""
        
        new_ui_section = """            {/* Card Types Group */}
            <div className="filter-group">
              <label>Card Types</label>
              <div className="multi-select-grid">
                {['Creature', 'Instant', 'Sorcery', 'Artifact', 'Enchantment', 'Planeswalker', 'Land'].map((type: string) => (
                  <button
                    key={type}
                    className={`type-button ${activeFilters.types.includes(type.toLowerCase()) ? 'selected' : ''}`}
                    onClick={() => {
                      const newTypes = activeFilters.types.includes(type.toLowerCase())
                        ? activeFilters.types.filter((t: string) => t !== type.toLowerCase())
                        : [...activeFilters.types, type.toLowerCase()];
                      handleFilterChange('types', newTypes);
                    }}
                  >
                    {type}
                  </button>
                ))}
              </div>
            </div>
            
            {/* Sets Group */}
            <div className="filter-group">
              <label>Sets</label>
              <div className="set-filter-container">
                <input
                  type="text"
                  placeholder="Search sets..."
                  value={setSearchText}
                  onChange={(e) => updateSetSearchText(e.target.value)}
                  className="set-search-input"
                  style={{
                    width: '100%',
                    padding: '6px 10px',
                    borderRadius: '4px',
                    border: '1px solid #404040',
                    backgroundColor: '#2a2a2a',
                    color: '#fff',
                    fontSize: '14px',
                    marginBottom: '8px'
                  }}
                />
                <div className="set-selection-area" style={{
                  maxHeight: '150px',
                  overflowY: 'auto',
                  border: '1px solid #404040',
                  borderRadius: '4px',
                  backgroundColor: '#1e1e1e',
                  padding: '4px'
                }}>
                  {filteredSets.map((set: any) => (
                    <label key={set.code} className="set-checkbox-label" style={{
                      display: 'block',
                      padding: '4px 8px',
                      cursor: 'pointer',
                      borderRadius: '2px',
                      fontSize: '13px',
                      color: '#ccc',
                      ':hover': { backgroundColor: '#333' }
                    }}>
                      <input
                        type="checkbox"
                        checked={activeFilters.sets.includes(set.code)}
                        onChange={() => toggleSetSelection(set.code)}
                        style={{ marginRight: '8px' }}
                      />
                      <span className="set-display">
                        {set.name} ({set.code})
                      </span>
                    </label>
                  ))}
                  {filteredSets.length === 0 && setSearchText && (
                    <div style={{ padding: '8px', color: '#888', textAlign: 'center', fontSize: '13px' }}>
                      No sets found
                    </div>
                  )}
                </div>
                {activeFilters.sets.length > 0 && (
                  <div style={{ marginTop: '8px', fontSize: '12px', color: '#888' }}>
                    {activeFilters.sets.length} set{activeFilters.sets.length !== 1 ? 's' : ''} selected
                  </div>
                )}
              </div>
            </div>
            
            {/* Rarity Group */}"""
        
        if old_ui_section in content:
            content = content.replace(old_ui_section, new_ui_section)
            print("✅ Added set filter UI component")
        else:
            print("⚠️  Could not find card types/rarity section pattern")
        
        # Write the updated content back to file
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        
        print(f"✅ SUCCESS: Set filter UI added to {file_path}")
        return True
        
    except Exception as e:
        print(f"❌ ERROR: Failed to update {file_path}: {str(e)}")
        return False

def add_set_search_functions():
    """Add set search functions to scryfallApi.ts"""
    file_path = "src/services/scryfallApi.ts"
    
    if not os.path.exists(file_path):
        print(f"❌ ERROR: File {file_path} not found!")
        return False
    
    print(f"🔧 Reading {file_path}...")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Add set search functions before the export section
        old_exports = """// Export commonly used search queries
export const COMMON_QUERIES = {"""
        
        new_exports = """/**
 * Search sets with text query
 */
export const searchSets = async (query: string): Promise<any[]> => {
  const allSets = await getSets();
  
  if (!query.trim()) return allSets.slice(0, 20);
  
  const searchTerm = query.toLowerCase();
  return allSets.filter(set => 
    set.name.toLowerCase().includes(searchTerm) ||
    set.code.toLowerCase().includes(searchTerm)
  ).slice(0, 20);
};

/**
 * Get popular/recent sets for quick selection
 */
export const getPopularSets = async (): Promise<any[]> => {
  const allSets = await getSets();
  // Return last 10 expansion sets
  return allSets
    .filter(set => set.set_type === 'expansion')
    .sort((a, b) => new Date(b.released_at).getTime() - new Date(a.released_at).getTime())
    .slice(0, 10);
};

// Export commonly used search queries
export const COMMON_QUERIES = {"""
        
        if old_exports in content:
            content = content.replace(old_exports, new_exports)
            print("✅ Added set search functions to scryfallApi.ts")
        else:
            print("⚠️  Could not find export section pattern")
        
        # Write the updated content back to file
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        
        print(f"✅ SUCCESS: Set search functions added to {file_path}")
        return True
        
    except Exception as e:
        print(f"❌ ERROR: Failed to update {file_path}: {str(e)}")
        return False

def main():
    print("🚀 MTG Deck Builder - Fix 2: Set Filter Addition")
    print("=" * 60)
    print("This script adds complete set filtering functionality with search and multi-select.\n")
    
    success = True
    
    # Step 1: Add set filter state management
    print("📦 Step 1: Adding set filter state management...")
    if not add_set_filter_to_use_cards():
        success = False
    
    # Step 2: Add set filter UI
    print("\n🎨 Step 2: Adding set filter UI...")
    if not add_set_filter_ui():
        success = False
    
    # Step 3: Add set search functions
    print("\n🔍 Step 3: Adding set search functions...")
    if not add_set_search_functions():
        success = False
    
    if success:
        print("\n🎉 Set filter addition completed successfully!")
        print("📋 Testing instructions:")
        print("   1. Search for set names (e.g., 'Innistrad', 'Midnight')")
        print("   2. Search for set codes (e.g., 'MID', 'NEO')")
        print("   3. Select multiple sets and verify filtering works")
        print("   4. Verify set filter combines with other filters")
        print("   5. Test 'Clear All Filters' includes set selection")
    else:
        print("\n❌ Set filter addition failed. Please check the error messages above.")

if __name__ == "__main__":
    main()
