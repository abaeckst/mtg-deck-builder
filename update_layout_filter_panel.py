#!/usr/bin/env python3

import os
import sys

def update_layout_filter_panel(filename):
    """Update MTGOLayout.tsx to use FilterPanel component for Phase 4B"""
    
    if not os.path.exists(filename):
        print(f"Error: {filename} not found")
        return False
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Make replacements with exact string matching
    updates = [
        # 1. Add FilterPanel import to existing component imports
        (
            """// Import components
import { useCards } from '../hooks/useCards';
import { useSorting } from '../hooks/useSorting';
import { useCardSizing } from '../hooks/useCardSizing';
import DraggableCard from './DraggableCard';
import DropZoneComponent from './DropZone';
import DragPreview from './DragPreview';
import ContextMenu from './ContextMenu';
import SearchAutocomplete from './SearchAutocomplete';
import PileView from './PileView';
import ListView from './ListView';
import AdaptiveHeader from './AdaptiveHeader';""",
            """// Import components
import { useCards } from '../hooks/useCards';
import { useSorting } from '../hooks/useSorting';
import { useCardSizing } from '../hooks/useCardSizing';
import DraggableCard from './DraggableCard';
import DropZoneComponent from './DropZone';
import DragPreview from './DragPreview';
import ContextMenu from './ContextMenu';
import SearchAutocomplete from './SearchAutocomplete';
import PileView from './PileView';
import ListView from './ListView';
import AdaptiveHeader from './AdaptiveHeader';
// Phase 4B: Enhanced filter components
import FilterPanel from './FilterPanel';""",
            "Add FilterPanel import"
        ),
        
        # 2. Add new useCards actions to destructuring
        (
            """  const { 
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
    // Progressive loading actions
    pagination,
    loadMoreResultsAction,
    resetPagination,} = useCards();""",
            """  const { 
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
    // Progressive loading actions
    pagination,
    loadMoreResultsAction,
    resetPagination,
    // Phase 4B: Enhanced filter actions
    updateSectionState,
    getSectionState,
    autoExpandSection,} = useCards();""",
            "Add enhanced filter actions"
        ),
        
        # 3. Replace the entire embedded filter panel with FilterPanel component
        (
            """      {/* Enhanced Filter Panel - Left Side */}
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
              <SearchAutocomplete
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
                placeholder="Search cards... (try: flying, &quot;exact phrase&quot;, -exclude, name:lightning)"
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
                  {['W', 'U', 'B', 'R', 'G', 'C'].map((color: string) => (
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
                  <option value="exact">Exactly these colors</option>
                  <option value="include">Include these colors</option>
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
      </div>""",
            """      {/* Phase 4B: Enhanced Filter Panel with Professional Components */}
      <FilterPanel
        searchText={searchText}
        onSearchTextChange={setSearchText}
        onSearch={handleSearch}
        searchSuggestions={searchSuggestions}
        showSuggestions={showSuggestions}
        onSuggestionSelect={(suggestion) => {
          setSearchText(suggestion);
          handleSearch(suggestion);
        }}
        onSuggestionsRequested={getSearchSuggestions}
        onSuggestionsClear={clearSearchSuggestions}
        activeFilters={activeFilters}
        isFiltersCollapsed={isFiltersCollapsed}
        hasActiveFilters={hasActiveFilters()}
        onFilterChange={handleFilterChange}
        onClearAllFilters={clearAllFilters}
        onToggleFiltersCollapsed={toggleFiltersCollapsed}
        getSectionState={getSectionState}
        updateSectionState={updateSectionState}
        autoExpandSection={autoExpandSection}
        onLoadPopularCards={loadPopularCards}
        onLoadRandomCard={loadRandomCard}
        onClearSelection={clearSelection}
        width={isFiltersCollapsed ? 40 : layout.panels.filterPanelWidth}
      />
      
      {/* Enhanced Resize Handle */}
      <div 
        className="resize-handle resize-handle-right"
        onMouseDown={resizeHandlers.onFilterPanelResize}
        title="Drag to resize filter panel"
        style={{
          position: 'absolute',
          top: 0,
          right: isFiltersCollapsed ? 25 : layout.panels.filterPanelWidth - 15,
          width: 30,
          height: '100%',
          cursor: 'ew-resize',
          background: 'transparent',
          zIndex: 1001
        }}
      />""",
            "Replace embedded filter UI with FilterPanel component"
        ),
    ]
    
    for old_str, new_str, desc in updates:
        if old_str in content:
            content = content.replace(old_str, new_str)
            print(f"✅ {desc}")
        else:
            print(f"❌ Could not find: {desc}")
            return False
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Successfully updated {filename}")
    return True

if __name__ == "__main__":
    success = update_layout_filter_panel("src/components/MTGOLayout.tsx")
    sys.exit(0 if success else 1)
