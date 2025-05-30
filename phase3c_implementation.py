# Phase 3C Implementation Script - Enhanced Filtering System
# This script will update your existing files to add comprehensive filtering

import os
import re

def update_scryfall_api():
    """Step 1: Enhance scryfallApi.ts with comprehensive SearchFilters interface"""
    
    # Read the current file
    with open('src/services/scryfallApi.ts', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find and replace the SearchFilters interface
    old_interface = '''export interface SearchFilters {
  format?: string;
  colors?: string[];
  types?: string[];
  rarity?: string[];
  set?: string;
  cmc?: { min?: number; max?: number };
  power?: { min?: number; max?: number };
  toughness?: { min?: number; max?: number };
}'''
    
    new_interface = '''export interface SearchFilters {
  format?: string;
  colors?: string[];
  colorIdentity?: 'exact' | 'subset' | 'include'; // How to match colors
  types?: string[];
  rarity?: string[];
  sets?: string[];
  cmc?: { min?: number; max?: number };
  power?: { min?: number; max?: number };
  toughness?: { min?: number; max?: number };
  keywords?: string[];
  artist?: string;
  price?: { min?: number; max?: number };
}'''
    
    content = content.replace(old_interface, new_interface)
    
    # Enhance the searchCardsWithFilters function
    old_function_start = '''export const searchCardsWithFilters = async (
  query: string,
  filters: SearchFilters = {},
  page = 1
): Promise<ScryfallSearchResponse> => {
  let searchQuery = query;
  
  // Add format filter with Custom Standard support
  if (filters.format) {
    if (filters.format === 'custom-standard') {
      // Custom Standard: Use standard legality as base
      // In future phases, this will be extended to include unreleased sets
      searchQuery += ` legal:standard`;
    } else {
      searchQuery += ` legal:${filters.format}`;
    }
  }
  
  // Add color filters
  if (filters.colors && filters.colors.length > 0) {
    const colorQuery = filters.colors.join('');
    searchQuery += ` color:${colorQuery}`;
  }'''
    
    new_function_start = '''export const searchCardsWithFilters = async (
  query: string,
  filters: SearchFilters = {},
  page = 1
): Promise<ScryfallSearchResponse> => {
  let searchQuery = query;
  
  // Add format filter with Custom Standard support
  if (filters.format) {
    if (filters.format === 'custom-standard') {
      // Custom Standard: Use standard legality as base
      // In future phases, this will be extended to include unreleased sets
      searchQuery += ` legal:standard`;
    } else {
      searchQuery += ` legal:${filters.format}`;
    }
  }
  
  // Add color identity filters with advanced logic
  if (filters.colors && filters.colors.length > 0) {
    const colorQuery = filters.colors.join('');
    const colorMode = filters.colorIdentity || 'include';
    
    switch (colorMode) {
      case 'exact':
        searchQuery += ` color=${colorQuery}`;
        break;
      case 'subset':
        searchQuery += ` color<=${colorQuery}`;
        break;
      case 'include':
      default:
        searchQuery += ` color:${colorQuery}`;
        break;
    }
  }'''
    
    content = content.replace(old_function_start, new_function_start)
    
    # Add enhanced set filtering
    old_set_filter = '''  // Add set filter
  if (filters.set) {
    searchQuery += ` set:${filters.set}`;
  }'''
    
    new_set_filter = '''  // Add set filters (multiple sets support)
  if (filters.sets && filters.sets.length > 0) {
    if (filters.sets.length === 1) {
      searchQuery += ` set:${filters.sets[0]}`;
    } else {
      const setQuery = filters.sets.map(set => `set:${set}`).join(' OR ');
      searchQuery += ` (${setQuery})`;
    }
  }
  
  // Backward compatibility for single set filter
  if (filters.set && !filters.sets) {
    searchQuery += ` set:${filters.set}`;
  }'''
    
    content = content.replace(old_set_filter, new_set_filter)
    
    # Write the updated file
    with open('src/services/scryfallApi.ts', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Updated scryfallApi.ts with enhanced SearchFilters interface")

def update_use_cards_hook():
    """Step 2: Add comprehensive filter state management to useCards.ts"""
    
    # Read the current file
    with open('src/hooks/useCards.ts', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Add filter state to UseCardsState interface
    old_state_interface = '''export interface UseCardsState {
  cards: ScryfallCard[];
  loading: boolean;
  error: string | null;
  hasMore: boolean;
  selectedCards: Set<string>;
  searchQuery: string;
  totalCards: number;
}'''
    
    new_state_interface = '''export interface UseCardsState {
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
}'''
    
    content = content.replace(old_state_interface, new_state_interface)
    
    # Add filter actions to UseCardsActions interface
    old_actions_interface = '''export interface UseCardsActions {
  searchForCards: (query: string, format?: string) => Promise<void>;
  loadPopularCards: () => Promise<void>;
  loadRandomCard: () => Promise<void>;
  selectCard: (cardId: string) => void;
  deselectCard: (cardId: string) => void;
  clearSelection: () => void;
  isCardSelected: (cardId: string) => boolean;
  getSelectedCardsData: () => ScryfallCard[];
  clearCards: () => void;
}'''
    
    new_actions_interface = '''export interface UseCardsActions {
  searchForCards: (query: string, format?: string) => Promise<void>;
  searchWithAllFilters: (query: string) => Promise<void>;
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
}'''
    
    content = content.replace(old_actions_interface, new_actions_interface)
    
    # Update the initial state
    old_initial_state = '''  const [state, setState] = useState<UseCardsState>({
    cards: [],
    loading: false,
    error: null,
    hasMore: false,
    selectedCards: new Set(),
    searchQuery: '',
    totalCards: 0,
  });'''
    
    new_initial_state = '''  const [state, setState] = useState<UseCardsState>({
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
      colorIdentity: 'include',
      types: [],
      rarity: [],
      sets: [],
      cmc: { min: null, max: null },
      power: { min: null, max: null },
      toughness: { min: null, max: null },
    },
    isFiltersCollapsed: false,
  });'''
    
    content = content.replace(old_initial_state, new_initial_state)
    
    # Add new filter management functions before the return statement
    return_statement = '''  return {
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
  };'''
    
    new_functions = '''  // Enhanced filter management functions
  const updateFilter = useCallback((filterType: string, value: any) => {
    setState(prev => ({
      ...prev,
      activeFilters: {
        ...prev.activeFilters,
        [filterType]: value,
      },
    }));
  }, []);

  const clearAllFilters = useCallback(() => {
    setState(prev => ({
      ...prev,
      activeFilters: {
        format: '',
        colors: [],
        colorIdentity: 'include',
        types: [],
        rarity: [],
        sets: [],
        cmc: { min: null, max: null },
        power: { min: null, max: null },
        toughness: { min: null, max: null },
      },
    }));
  }, []);

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

  // Enhanced search function that uses all active filters
  const searchWithAllFilters = useCallback(async (query: string) => {
    const filters = state.activeFilters;
    
    // Build comprehensive filter object
    const searchFilters: any = {};
    
    if (filters.format) searchFilters.format = filters.format;
    if (filters.colors.length > 0) {
      searchFilters.colors = filters.colors;
      searchFilters.colorIdentity = filters.colorIdentity;
    }
    if (filters.types.length > 0) searchFilters.types = filters.types;
    if (filters.rarity.length > 0) searchFilters.rarity = filters.rarity;
    if (filters.sets.length > 0) searchFilters.sets = filters.sets;
    if (filters.cmc.min !== null || filters.cmc.max !== null) {
      searchFilters.cmc = {};
      if (filters.cmc.min !== null) searchFilters.cmc.min = filters.cmc.min;
      if (filters.cmc.max !== null) searchFilters.cmc.max = filters.cmc.max;
    }
    if (filters.power.min !== null || filters.power.max !== null) {
      searchFilters.power = {};
      if (filters.power.min !== null) searchFilters.power.min = filters.power.min;
      if (filters.power.max !== null) searchFilters.power.max = filters.power.max;
    }
    if (filters.toughness.min !== null || filters.toughness.max !== null) {
      searchFilters.toughness = {};
      if (filters.toughness.min !== null) searchFilters.toughness.min = filters.toughness.min;
      if (filters.toughness.max !== null) searchFilters.toughness.max = filters.toughness.max;
    }

    // Use the same race-condition-safe logic as searchForCards
    const searchId = Date.now() + Math.random();
    (window as any).currentSearchId = searchId;

    console.log('🔍 ENHANCED SEARCH:', { 
      searchId: searchId.toFixed(3), 
      query, 
      filters: searchFilters 
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

      const response = await searchCardsWithFilters(query || '*', searchFilters);

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
        const errorMessage = error instanceof Error ? error.message : 'Failed to search with filters';
        setState(prev => ({
          ...prev,
          error: errorMessage,
          cards: [],
          totalCards: 0,
          hasMore: false,
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
  };'''
    
    content = content.replace(return_statement, new_functions)
    
    # Write the updated file
    with open('src/hooks/useCards.ts', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Updated useCards.ts with comprehensive filter state management")

def update_mtgo_layout():
    """Step 3: Replace the filter panel in MTGOLayout.tsx with comprehensive filtering"""
    
    # Read the current file
    with open('src/components/MTGOLayout.tsx', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Update the useCards destructuring to include new functions
    old_destructuring = '''  const { 
    cards, 
    loading, 
    error, 
    searchForCards, 
    loadPopularCards, 
    loadRandomCard 
  } = useCards();'''
    
    new_destructuring = '''  const { 
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
  } = useCards();'''
    
    content = content.replace(old_destructuring, new_destructuring)
    
    # Remove the old local filter state since we're now using the hook
    old_local_state = '''  // Local state for search and filters
  const [searchText, setSearchText] = useState('');
  const [selectedFormat, setSelectedFormat] = useState('');
  const [selectedColors, setSelectedColors] = useState<string[]>([]);'''
    
    new_local_state = '''  // Local state for search only - filters now managed by useCards hook
  const [searchText, setSearchText] = useState('');'''
    
    content = content.replace(old_local_state, new_local_state)
    
    # Update the search handler to work with new system
    old_search_handler = '''  // Search handling with format support - FIXED race condition
  const handleSearch = useCallback((text: string) => {
    setSearchText(text);
    if (text.trim()) {
      searchForCards(text, selectedFormat);
    } else {
      loadPopularCards();
    }
  }, [selectedFormat, searchForCards, loadPopularCards]);
  
  // Handle format changes by re-searching with current text
  const handleFormatChange = useCallback((newFormat: string) => {
    setSelectedFormat(newFormat);
    // Always trigger search when format changes, even with empty search text
    setTimeout(() => {
      searchForCards(searchText, newFormat);
    }, 50);
  }, [searchText, searchForCards]);'''
    
    new_search_handler = '''  // Enhanced search handling with comprehensive filters
  const handleSearch = useCallback((text: string) => {
    setSearchText(text);
    if (text.trim() || hasActiveFilters()) {
      searchWithAllFilters(text);
    } else {
      loadPopularCards();
    }
  }, [searchWithAllFilters, loadPopularCards, hasActiveFilters]);
  
  // Handle any filter change by triggering new search
  const handleFilterChange = useCallback((filterType: string, value: any) => {
    updateFilter(filterType, value);
    // Trigger search after filter update
    setTimeout(() => {
      if (searchText.trim() || hasActiveFilters()) {
        searchWithAllFilters(searchText);
      }
    }, 50);
  }, [updateFilter, searchWithAllFilters, searchText, hasActiveFilters]);'''
    
    content = content.replace(old_search_handler, new_search_handler)
    
    # Now replace the entire filter panel section with the comprehensive version
    old_filter_panel_start = '''      {/* Filter Panel - Left Side */}
      <div 
        className="mtgo-filter-panel"
        style={{ width: layout.panels.filterPanelWidth }}
      >
        <div className="panel-header">
          <h3>Filters</h3>
        </div>
        
        <div className="filter-content">'''
    
    # Find the end of the filter panel content by looking for the resize handle
    old_filter_panel_end = '''        {/* PHASE 3A: Enhanced Resize Handle with larger hit zone */}
        <div 
          className="resize-handle resize-handle-right"
          onMouseDown={resizeHandlers.onFilterPanelResize}
          title="Drag to resize filter panel"
          style={{
            position: 'absolute',
            top: 0,
            right: -15,
            width: 30,
            height: '100%',
            cursor: 'ew-resize',
            background: 'transparent',
            zIndex: 1001
          }}
        />
      </div>'''
    
    new_filter_panel = '''      {/* Enhanced Filter Panel - Left Side */}
      <div 
        className={`mtgo-filter-panel ${isFiltersCollapsed ? 'collapsed' : ''}`}
        style={{ width: isFiltersCollapsed ? '40px' : layout.panels.filterPanelWidth }}
      >
        <div className="panel-header">
          <h3>{isFiltersCollapsed ? '' : 'Filters'}</h3>
          <div className="filter-controls">
            {!isFiltersCollapsed && hasActiveFilters() && (
              <button onClick={clearAllFilters} className="clear-filters-btn" title="Clear all filters">
                Clear
              </button>
            )}
            <button 
              onClick={toggleFiltersCollapsed} 
              className="collapse-toggle-btn"
              title={isFiltersCollapsed ? 'Expand filters' : 'Collapse filters'}
            >
              {isFiltersCollapsed ? '→' : '←'}
            </button>
          </div>
        </div>
        
        {!isFiltersCollapsed && (
          <div className="filter-content">
            {/* Search Group */}
            <div className="filter-group">
              <label>Search</label>
              <input
                type="text"
                value={searchText}
                onChange={(e) => handleSearch(e.target.value)}
                placeholder="Card name..."
                className="search-input"
              />
            </div>
            
            {/* Format Group */}
            <div className="filter-group">
              <label>Format</label>
              <select 
                value={activeFilters.format} 
                onChange={(e) => handleFilterChange('format', e.target.value)}
                className="format-select"
              >
                <option value="">All Formats</option>
                <option value="standard">Standard</option>
                <option value="custom-standard">Custom Standard (Standard + Unreleased)</option>
                <option value="pioneer">Pioneer</option>
                <option value="modern">Modern</option>
                <option value="legacy">Legacy</option>
                <option value="vintage">Vintage</option>
                <option value="commander">Commander</option>
                <option value="pauper">Pauper</option>
              </select>
            </div>
            
            {/* Color Identity Group */}
            <div className="filter-group">
              <label>Color Identity</label>
              <div className="color-identity-controls">
                <div className="color-filter-grid">
                  {['W', 'U', 'B', 'R', 'G'].map((color: string) => (
                    <button
                      key={color}
                      className={`color-button color-${color.toLowerCase()} ${
                        activeFilters.colors.includes(color) ? 'selected' : ''
                      }`}
                      onClick={() => {
                        const newColors = activeFilters.colors.includes(color)
                          ? activeFilters.colors.filter((c: string) => c !== color)
                          : [...activeFilters.colors, color];
                        handleFilterChange('colors', newColors);
                      }}
                    >
                      {color}
                    </button>
                  ))}
                </div>
                <select
                  value={activeFilters.colorIdentity}
                  onChange={(e) => handleFilterChange('colorIdentity', e.target.value)}
                  className="color-mode-select"
                >
                  <option value="include">Include these colors</option>
                  <option value="exact">Exactly these colors</option>
                  <option value="subset">At most these colors</option>
                </select>
              </div>
            </div>
            
            {/* Mana Cost Group */}
            <div className="filter-group">
              <label>Mana Cost (CMC)</label>
              <div className="range-filter">
                <input
                  type="number"
                  placeholder="Min"
                  min="0"
                  max="20"
                  value={activeFilters.cmc.min || ''}
                  onChange={(e) => handleFilterChange('cmc', {
                    ...activeFilters.cmc,
                    min: e.target.value ? parseInt(e.target.value) : null
                  })}
                  className="range-input"
                />
                <span>to</span>
                <input
                  type="number"
                  placeholder="Max"
                  min="0"
                  max="20"
                  value={activeFilters.cmc.max || ''}
                  onChange={(e) => handleFilterChange('cmc', {
                    ...activeFilters.cmc,
                    max: e.target.value ? parseInt(e.target.value) : null
                  })}
                  className="range-input"
                />
              </div>
            </div>
            
            {/* Card Types Group */}
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
            
            {/* Rarity Group */}
            <div className="filter-group">
              <label>Rarity</label>
              <div className="rarity-filter-grid">
                {[
                  { key: 'common', label: 'Common', symbol: 'C' },
                  { key: 'uncommon', label: 'Uncommon', symbol: 'U' },
                  { key: 'rare', label: 'Rare', symbol: 'R' },
                  { key: 'mythic', label: 'Mythic', symbol: 'M' }
                ].map((rarity) => (
                  <button
                    key={rarity.key}
                    className={`rarity-button rarity-${rarity.key} ${
                      activeFilters.rarity.includes(rarity.key) ? 'selected' : ''
                    }`}
                    onClick={() => {
                      const newRarity = activeFilters.rarity.includes(rarity.key)
                        ? activeFilters.rarity.filter((r: string) => r !== rarity.key)
                        : [...activeFilters.rarity, rarity.key];
                      handleFilterChange('rarity', newRarity);
                    }}
                    title={rarity.label}
                  >
                    {rarity.symbol}
                  </button>
                ))}
              </div>
            </div>
            
            {/* Creature Stats Group */}
            <div className="filter-group">
              <label>Creature Stats</label>
              <div className="stats-filter">
                <div className="stat-row">
                  <span>Power:</span>
                  <input
                    type="number"
                    placeholder="Min"
                    min="0"
                    max="20"
                    value={activeFilters.power.min || ''}
                    onChange={(e) => handleFilterChange('power', {
                      ...activeFilters.power,
                      min: e.target.value ? parseInt(e.target.value) : null
                    })}
                    className="stat-input"
                  />
                  <span>to</span>
                  <input
                    type="number"
                    placeholder="Max"
                    min="0"
                    max="20"
                    value={activeFilters.power.max || ''}
                    onChange={(e) => handleFilterChange('power', {
                      ...activeFilters.power,
                      max: e.target.value ? parseInt(e.target.value) : null
                    })}
                    className="stat-input"
                  />
                </div>
                <div className="stat-row">
                  <span>Toughness:</span>
                  <input
                    type="number"
                    placeholder="Min"
                    min="0"
                    max="20"
                    value={activeFilters.toughness.min || ''}
                    onChange={(e) => handleFilterChange('toughness', {
                      ...activeFilters.toughness,
                      min: e.target.value ? parseInt(e.target.value) : null
                    })}
                    className="stat-input"
                  />
                  <span>to</span>
                  <input
                    type="number"
                    placeholder="Max"
                    min="0"
                    max="20"
                    value={activeFilters.toughness.max || ''}
                    onChange={(e) => handleFilterChange('toughness', {
                      ...activeFilters.toughness,
                      max: e.target.value ? parseInt(e.target.value) : null
                    })}
                    className="stat-input"
                  />
                </div>
              </div>
            </div>
            
            {/* Quick Actions Group */}
            <div className="filter-group">
              <label>Quick Actions</label>
              <div className="quick-actions">
                <button onClick={loadPopularCards}>Popular Cards</button>
                <button onClick={loadRandomCard}>Random Card</button>
                <button onClick={clearSelection}>Clear Selection</button>
              </div>
            </div>
          </div>
        )}
        
        {/* Enhanced Resize Handle */}
        <div 
          className="resize-handle resize-handle-right"
          onMouseDown={resizeHandlers.onFilterPanelResize}
          title="Drag to resize filter panel"
          style={{
            position: 'absolute',
            top: 0,
            right: -15,
            width: 30,
            height: '100%',
            cursor: 'ew-resize',
            background: 'transparent',
            zIndex: 1001
          }}
        />
      </div>'''
    
    # Find the complete old filter panel section to replace
    start_index = content.find(old_filter_panel_start)
    end_index = content.find(old_filter_panel_end) + len(old_filter_panel_end)
    
    if start_index != -1 and end_index != -1:
        content = content[:start_index] + new_filter_panel + content[end_index:]
    else:
        print("❌ Could not find filter panel section to replace")
        return
    
    # Write the updated file
    with open('src/components/MTGOLayout.tsx', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Updated MTGOLayout.tsx with comprehensive filter panel")

def update_css_styles():
    """Step 4: Add comprehensive filter panel styling to MTGOLayout.css"""
    
    # Read the current file
    with open('src/components/MTGOLayout.css', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Add new comprehensive filter styles before the resize handle styles
    filter_styles = '''
/* PHASE 3C: Enhanced Filter Panel Styles */

/* Filter Panel Collapse/Expand */
.mtgo-filter-panel.collapsed {
  min-width: 40px;
  max-width: 40px;
}

.mtgo-filter-panel.collapsed .panel-header h3 {
  display: none;
}

.filter-controls {
  display: flex;
  align-items: center;
  gap: 6px;
}

.clear-filters-btn {
  background-color: #ef4444;
  color: #ffffff;
  border: 1px solid #dc2626;
  padding: 4px 8px;
  border-radius: 3px;
  font-size: 11px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.clear-filters-btn:hover {
  background-color: #dc2626;
  transform: scale(1.05);
}

.collapse-toggle-btn {
  background-color: #3b82f6;
  color: #ffffff;
  border: 1px solid #2563eb;
  padding: 4px 8px;
  border-radius: 3px;
  font-size: 12px;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.2s ease;
  min-width: 24px;
}

.collapse-toggle-btn:hover {
  background-color: #2563eb;
  transform: scale(1.1);
}

/* Color Identity Controls */
.color-identity-controls {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.color-mode-select {
  width: 100%;
  background-color: #1a1a1a;
  border: 1px solid #404040;
  color: #ffffff;
  padding: 6px 8px;
  border-radius: 4px;
  font-size: 11px;
  cursor: pointer;
}

.color-mode-select:focus {
  outline: none;
  border-color: #3b82f6;
}

/* Range Filter Styles */
.range-filter {
  display: flex;
  align-items: center;
  gap: 8px;
}

.range-input {
  width: 60px;
  background-color: #1a1a1a;
  border: 1px solid #404040;
  color: #ffffff;
  padding: 6px 8px;
  border-radius: 4px;
  font-size: 12px;
  text-align: center;
}

.range-input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 1px #3b82f6;
}

.range-filter span {
  color: #cccccc;
  font-size: 11px;
}

/* Multi-Select Grid for Card Types */
.multi-select-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 4px;
}

.type-button {
  background-color: #404040;
  color: #ffffff;
  border: 1px solid #555555;
  padding: 6px 8px;
  border-radius: 4px;
  font-size: 10px;
  cursor: pointer;
  transition: all 0.2s ease;
  text-align: center;
}

.type-button:hover {
  background-color: #4a4a4a;
  transform: scale(1.02);
}

.type-button.selected {
  background-color: #3b82f6;
  border-color: #2563eb;
  box-shadow: 0 0 0 1px #2563eb;
}

/* Rarity Filter Grid */
.rarity-filter-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 4px;
}

.rarity-button {
  width: 32px;
  height: 32px;
  border-radius: 6px;
  border: 2px solid #404040;
  color: #ffffff;
  font-weight: bold;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.rarity-button:hover {
  border-color: #ffffff;
  transform: scale(1.1);
}

.rarity-button.selected {
  border-color: #3b82f6;
  box-shadow: 0 0 0 2px #3b82f6;
}

/* Rarity-specific colors */
.rarity-button.rarity-common { background-color: #6b7280; }
.rarity-button.rarity-uncommon { background-color: #c0c0c0; color: #000000; }
.rarity-button.rarity-rare { background-color: #fbbf24; color: #000000; }
.rarity-button.rarity-mythic { background-color: #f59e0b; color: #000000; }

/* Creature Stats Filter */
.stats-filter {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.stat-row {
  display: flex;
  align-items: center;
  gap: 6px;
}

.stat-row span {
  color: #cccccc;
  font-size: 11px;
  min-width: 65px;
}

.stat-input {
  width: 50px;
  background-color: #1a1a1a;
  border: 1px solid #404040;
  color: #ffffff;
  padding: 4px 6px;
  border-radius: 4px;
  font-size: 11px;
  text-align: center;
}

.stat-input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 1px #3b82f6;
}

/* Enhanced Filter Group Spacing */
.filter-group {
  margin-bottom: 20px;
  padding-bottom: 16px;
  border-bottom: 1px solid #333333;
}

.filter-group:last-child {
  border-bottom: none;
}

.filter-group label {
  display: block;
  font-size: 12px;
  font-weight: 600;
  color: #ffffff;
  margin-bottom: 8px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

/* Filter Panel Collapse Animation */
.mtgo-filter-panel {
  transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  overflow: hidden;
}

.filter-content {
  opacity: 1;
  transition: opacity 0.2s ease;
}

.mtgo-filter-panel.collapsed .filter-content {
  opacity: 0;
  display: none;
}

/* Active Filter Indicators */
.filter-group.has-active-filters label::after {
  content: " •";
  color: #3b82f6;
  font-weight: bold;
}

/* Responsive Filter Adjustments */
@media (max-width: 1200px) {
  .multi-select-grid {
    grid-template-columns: 1fr;
  }
  
  .rarity-filter-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .range-filter {
    flex-direction: column;
    align-items: stretch;
    gap: 4px;
  }
  
  .range-input {
    width: 100%;
  }
}

/* Enhanced Scrollbar for Filter Content */
.filter-content::-webkit-scrollbar {
  width: 6px;
}

.filter-content::-webkit-scrollbar-track {
  background-color: #1a1a1a;
  border-radius: 3px;
}

.filter-content::-webkit-scrollbar-thumb {
  background-color: #404040;
  border-radius: 3px;
}

.filter-content::-webkit-scrollbar-thumb:hover {
  background-color: #555555;
}

'''
    
    # Insert the new styles before the resize handle styles
    resize_handle_comment = '/* Enhanced Resize Handles - Larger hit zones */'
    insert_position = content.find(resize_handle_comment)
    
    if insert_position != -1:
        content = content[:insert_position] + filter_styles + content[insert_position:]
    else:
        # If we can't find the specific location, append to the end
        content += filter_styles
    
    # Write the updated file
    with open('src/components/MTGOLayout.css', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Updated MTGOLayout.css with comprehensive filter styling")

def main():
    """Execute all Phase 3C implementation steps"""
    try:
        print("🚀 Starting Phase 3C Implementation: Enhanced Filtering System")
        print("=" * 60)
        
        # Step 1: Enhance API service
        print("\n📋 Step 1: Enhancing Scryfall API service...")
        update_scryfall_api()
        
        # Step 2: Update useCards hook
        print("\n📋 Step 2: Adding filter state management to useCards hook...")
        update_use_cards_hook()
        
        # Step 3: Update MTGO Layout component
        print("\n📋 Step 3: Implementing comprehensive filter panel...")
        update_mtgo_layout()
        
        # Step 4: Update CSS styles
        print("\n📋 Step 4: Adding professional filter styling...")
        update_css_styles()
        
        print("\n" + "=" * 60)
        print("✅ Phase 3C Implementation Complete!")
        print("\n🎯 New Features Added:")
        print("   • Comprehensive color identity filtering with 3 matching modes")
        print("   • Mana cost (CMC) range filtering")
        print("   • Multi-select card type filtering")
        print("   • Visual rarity filtering with symbols")
        print("   • Creature power/toughness range filtering")
        print("   • Collapsible filter panel with expand/collapse button")
        print("   • Clear all filters functionality")
        print("   • Professional MTGO styling")
        print("   • Race-condition-safe enhanced search")
        print("\n🧪 Testing Instructions:")
        print("   1. Run 'npm start' to launch the application")
        print("   2. Try different filter combinations")
        print("   3. Test the collapse/expand functionality")
        print("   4. Verify filters work with and without search text")
        print("   5. Test the 'Clear' button functionality")
        print("\n🎮 New User Experience:")
        print("   • Professional filtering for competitive deck building")
        print("   • Flexible UI with collapsible filters")
        print("   • All filters work together seamlessly")
        print("   • Maintains existing search and format functionality")
        
    except Exception as e:
        print(f"\n❌ Error during implementation: {e}")
        print("Please check the file paths and try again.")

if __name__ == "__main__":
    main()
