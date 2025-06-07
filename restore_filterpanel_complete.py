#!/usr/bin/env python3

import os
import sys

def restore_filterpanel_complete():
    """Restore FilterPanel.tsx with correct JSX structure and all polish features"""
    
    filename = "src/components/FilterPanel.tsx"
    
    # Complete working FilterPanel.tsx with all polish features
    content = '''// src/components/FilterPanel.tsx - Phase 4B: Professional MTGO-style filter interface
import React, { useCallback } from 'react';
import CollapsibleSection from './CollapsibleSection';
import GoldButton from './GoldButton';
import SubtypeInput from './SubtypeInput';
import SearchAutocomplete from './SearchAutocomplete';

interface FilterPanelProps {
  // Search props
  searchText: string;
  onSearchTextChange: (text: string) => void;
  onSearch: (text: string) => void;
  searchSuggestions: string[];
  showSuggestions: boolean;
  onSuggestionSelect: (suggestion: string) => void;
  onSuggestionsRequested: (query: string) => Promise<void>;
  onSuggestionsClear: () => void;
  
  // Filter state
  activeFilters: any;
  isFiltersCollapsed: boolean;
  hasActiveFilters: boolean;
  
  // Filter actions
  onFilterChange: (filterType: string, value: any) => void;
  onClearAllFilters: () => void;
  onToggleFiltersCollapsed: () => void;
  
  // Section state management
  getSectionState: (section: string) => boolean;
  updateSectionState: (section: string, isExpanded: boolean) => void;
  autoExpandSection: (section: string) => void;
  
  // Quick actions
  onLoadPopularCards: () => void;
  onLoadRandomCard: () => void;
  onClearSelection: () => void;
  
  // Panel width
  width: number;
}

const FilterPanel: React.FC<FilterPanelProps> = ({
  searchText,
  onSearchTextChange,
  onSearch,
  searchSuggestions,
  showSuggestions,
  onSuggestionSelect,
  onSuggestionsRequested,
  onSuggestionsClear,
  activeFilters,
  isFiltersCollapsed,
  hasActiveFilters,
  onFilterChange,
  onClearAllFilters,
  onToggleFiltersCollapsed,
  getSectionState,
  updateSectionState,
  autoExpandSection,
  onLoadPopularCards,
  onLoadRandomCard,
  onClearSelection,
  width
}) => {
  // Color selection handler with gold button logic
  const handleColorSelection = useCallback((color: string) => {
    let newColors: string[];
    
    if (color === 'GOLD') {
      // Toggle gold mode
      const newGoldMode = !activeFilters.isGoldMode;
      onFilterChange('isGoldMode', newGoldMode);
      
      // Auto-disable colorless when gold is active
      if (newGoldMode && activeFilters.colors.includes('C')) {
        newColors = activeFilters.colors.filter((c: string) => c !== 'C');
        onFilterChange('colors', newColors);
      }
      
      autoExpandSection('colors');
      return;
    }
    
    // Handle colorless selection
    if (color === 'C') {
      // Disable gold mode when colorless is selected
      if (activeFilters.isGoldMode) {
        onFilterChange('isGoldMode', false);
      }
    }
    
    // Toggle color selection
    if (activeFilters.colors.includes(color)) {
      newColors = activeFilters.colors.filter((c: string) => c !== color);
    } else {
      newColors = [...activeFilters.colors, color];
    }
    
    onFilterChange('colors', newColors);
    autoExpandSection('colors');
  }, [activeFilters.colors, activeFilters.isGoldMode, onFilterChange, autoExpandSection]);

  // Subtype handlers
  const handleSubtypeAdd = useCallback((subtype: string) => {
    const newSubtypes = [...activeFilters.subtypes, subtype];
    onFilterChange('subtypes', newSubtypes);
    autoExpandSection('subtypes');
  }, [activeFilters.subtypes, onFilterChange, autoExpandSection]);

  const handleSubtypeRemove = useCallback((subtype: string) => {
    const newSubtypes = activeFilters.subtypes.filter((s: string) => s !== subtype);
    onFilterChange('subtypes', newSubtypes);
    if (newSubtypes.length === 0) {
      updateSectionState('subtypes', false);
    }
  }, [activeFilters.subtypes, onFilterChange, updateSectionState]);

  // Range filter handlers with validation
  const handleRangeChange = useCallback((filterType: string, field: 'min' | 'max', value: string) => {
    const numValue = value ? parseInt(value) : null;
    const currentRange = activeFilters[filterType];
    const newRange = { ...currentRange, [field]: numValue };
    
    // Validation
    if (newRange.min !== null && newRange.max !== null && newRange.min > newRange.max) {
      return; // Don't update if invalid range
    }
    
    onFilterChange(filterType, newRange);
    autoExpandSection(filterType === 'cmc' ? 'cmc' : 'stats');
  }, [activeFilters, onFilterChange, autoExpandSection]);

  if (isFiltersCollapsed) {
    return (
      <div className="mtgo-filter-panel collapsed" style={{ width: 40 }}>
        <button 
          onClick={onToggleFiltersCollapsed} 
          className="collapse-toggle-btn"
          title="Expand filters"
        >
          →
        </button>
      </div>
    );
  }

  return (
    <div className="mtgo-filter-panel" style={{ width, minWidth: '280px' }}>
      {/* Panel Header */}
      <div className="panel-header">
        <h3>Filters</h3>
        <div className="filter-controls">
          {hasActiveFilters && (
            <button onClick={onClearAllFilters} className="clear-filters-btn" title="Clear all filters">
              Clear
            </button>
          )}
          <button 
            onClick={onToggleFiltersCollapsed} 
            className="collapse-toggle-btn"
            title="Collapse filters"
          >
            ←
          </button>
        </div>
      </div>
      
      <div className="filter-content">
        {/* Search Group - Always Visible */}
        <div className="filter-group search-group">
          <label>Search</label>
          <SearchAutocomplete
            value={searchText}
            onChange={onSearchTextChange}
            onSearch={onSearch}
            suggestions={searchSuggestions}
            showSuggestions={showSuggestions}
            onSuggestionSelect={onSuggestionSelect}
            onSuggestionsRequested={onSuggestionsRequested}
            onSuggestionsClear={onSuggestionsClear}
            placeholder="Search cards... (try: flying, &quot;exact phrase&quot;, -exclude, name:lightning)"
            className="search-input"
          />
        </div>
        
        {/* Format Group - Always Visible */}
        <div className="filter-group format-group">
          <label>Format</label>
          <select 
            value={activeFilters.format} 
            onChange={(e) => onFilterChange('format', e.target.value)}
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
        
        {/* Colors Group - Collapsible */}
        <CollapsibleSection
          title="COLORS"
          isExpanded={getSectionState('colors')}
          hasActiveFilters={activeFilters.colors.length > 0 || activeFilters.isGoldMode}
          onToggle={() => updateSectionState('colors', !getSectionState('colors'))}
        >
          <div className="filter-group">
            <div className="color-identity-controls">
              <div className="color-filter-grid-row1">
                {/* Row 1: W U B R G */}
                {['W', 'U', 'B', 'R', 'G'].map((color: string) => (
                  <button
                    key={color}
                    className={`color-button color-${color.toLowerCase()} ${
                      activeFilters.colors.includes(color) ? 'selected' : ''
                    }`}
                    onClick={() => handleColorSelection(color)}
                    title={`Toggle ${color} color filter`}
                  >
                    {color}
                  </button>
                ))}
              </div>
              <div className="color-filter-grid-row2">
                {/* Row 2: Colorless and Gold */}
                {['C'].map((color: string) => (
                  <button
                    key={color}
                    className={`color-button color-${color.toLowerCase()} ${
                      activeFilters.colors.includes(color) ? 'selected' : ''
                    } ${
                      color === 'C' && activeFilters.isGoldMode ? 'disabled' : ''
                    }`}
                    onClick={() => handleColorSelection(color)}
                    disabled={color === 'C' && activeFilters.isGoldMode}
                    title={
                      color === 'C' && activeFilters.isGoldMode 
                        ? "Colorless cannot be used with multicolor filter" 
                        : `Toggle ${color} color filter`
                    }
                  >
                    {color}
                  </button>
                ))}
                <GoldButton
                  isSelected={activeFilters.isGoldMode}
                  onClick={() => handleColorSelection('GOLD')}
                  disabled={activeFilters.colors.includes('C')}
                />
              </div>
              <select
                value={activeFilters.colorIdentity}
                onChange={(e) => onFilterChange('colorIdentity', e.target.value)}
                className="color-mode-select"
              >
                <option value="exact">Exactly these colors</option>
                <option value="include">Include these colors</option>
                <option value="subset">At most these colors</option>
              </select>
            </div>
          </div>
        </CollapsibleSection>
        
        {/* Mana Value Group - Collapsible */}
        <CollapsibleSection
          title="MANA VALUE (MV)"
          isExpanded={getSectionState('cmc')}
          hasActiveFilters={activeFilters.cmc.min !== null || activeFilters.cmc.max !== null}
          onToggle={() => updateSectionState('cmc', !getSectionState('cmc'))}
        >
          <div className="filter-group">
            <label>Range</label>
            <div className="range-filter">
              <input
                type="number"
                placeholder="Min"
                min="0"
                max="20"
                value={activeFilters.cmc.min || ''}
                onChange={(e) => handleRangeChange('cmc', 'min', e.target.value)}
                className="range-input"
              />
              <span>to</span>
              <input
                type="number"
                placeholder="Max"
                min="0"
                max="20"
                value={activeFilters.cmc.max || ''}
                onChange={(e) => handleRangeChange('cmc', 'max', e.target.value)}
                className="range-input"
              />
            </div>
          </div>
        </CollapsibleSection>
        
        {/* Card Types Group - Collapsible */}
        <CollapsibleSection
          title="CARD TYPES"
          isExpanded={getSectionState('types')}
          hasActiveFilters={activeFilters.types.length > 0}
          onToggle={() => updateSectionState('types', !getSectionState('types'))}
        >
          <div className="filter-group">
            <div className="multi-select-grid">
              {['Creature', 'Instant', 'Sorcery', 'Artifact', 'Enchantment', 'Planeswalker', 'Land'].map((type: string) => (
                <button
                  key={type}
                  className={`type-button ${activeFilters.types.includes(type.toLowerCase()) ? 'selected' : ''}`}
                  onClick={() => {
                    const newTypes = activeFilters.types.includes(type.toLowerCase())
                      ? activeFilters.types.filter((t: string) => t !== type.toLowerCase())
                      : [...activeFilters.types, type.toLowerCase()];
                    onFilterChange('types', newTypes);
                    autoExpandSection('types');
                  }}
                >
                  {type}
                </button>
              ))}
            </div>
          </div>
        </CollapsibleSection>

        {/* More Types (Subtypes) Group - Collapsible */}
        <CollapsibleSection
          title="MORE TYPES"
          isExpanded={getSectionState('subtypes')}
          hasActiveFilters={activeFilters.subtypes.length > 0}
          onToggle={() => updateSectionState('subtypes', !getSectionState('subtypes'))}
        >
          <div className="filter-group">
            <SubtypeInput
              selectedSubtypes={activeFilters.subtypes}
              onSubtypeAdd={handleSubtypeAdd}
              onSubtypeRemove={handleSubtypeRemove}
              placeholder="Type subtypes..."
            />
          </div>
        </CollapsibleSection>

        {/* Advanced Sections - Collapsible */}
        
        {/* Sets Section - Future Implementation */}
        <CollapsibleSection
          title="SETS"
          isExpanded={getSectionState('sets')}
          hasActiveFilters={activeFilters.sets.length > 0}
          onToggle={() => updateSectionState('sets', !getSectionState('sets'))}
        >
          <div className="filter-group">
            <div className="sets-placeholder">
              <p style={{ fontStyle: 'italic', color: '#999' }}>
                Set filtering will be available in a future update
              </p>
            </div>
          </div>
        </CollapsibleSection>

        {/* Rarity Section */}
        <CollapsibleSection
          title="RARITY"
          isExpanded={getSectionState('rarity')}
          hasActiveFilters={activeFilters.rarity.length > 0}
          onToggle={() => updateSectionState('rarity', !getSectionState('rarity'))}
        >
          <div className="filter-group">
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
                    onFilterChange('rarity', newRarity);
                    autoExpandSection('rarity');
                  }}
                  title={rarity.label}
                >
                  {rarity.symbol}
                </button>
              ))}
            </div>
          </div>
        </CollapsibleSection>

        {/* Creature Stats Section */}
        <CollapsibleSection
          title="CREATURE STATS"
          isExpanded={getSectionState('stats')}
          hasActiveFilters={
            activeFilters.power.min !== null || activeFilters.power.max !== null ||
            activeFilters.toughness.min !== null || activeFilters.toughness.max !== null
          }
          onToggle={() => updateSectionState('stats', !getSectionState('stats'))}
        >
          <div className="filter-group">
            <div className="stats-filter">
              <div className="stat-row">
                <span>Power:</span>
                <input
                  type="number"
                  placeholder="Min"
                  min="0"
                  max="20"
                  value={activeFilters.power.min || ''}
                  onChange={(e) => handleRangeChange('power', 'min', e.target.value)}
                  className="stat-input"
                />
                <span>to</span>
                <input
                  type="number"
                  placeholder="Max"
                  min="0"
                  max="20"
                  value={activeFilters.power.max || ''}
                  onChange={(e) => handleRangeChange('power', 'max', e.target.value)}
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
                  onChange={(e) => handleRangeChange('toughness', 'min', e.target.value)}
                  className="stat-input"
                />
                <span>to</span>
                <input
                  type="number"
                  placeholder="Max"
                  min="0"
                  max="20"
                  value={activeFilters.toughness.max || ''}
                  onChange={(e) => handleRangeChange('toughness', 'max', e.target.value)}
                  className="stat-input"
                />
              </div>
            </div>
          </div>
        </CollapsibleSection>
        
        {/* Quick Actions Group */}
        <div className="filter-group">
          <label>Quick Actions</label>
          <div className="quick-actions">
            <button onClick={onLoadPopularCards}>Popular Cards</button>
            <button onClick={onLoadRandomCard}>Random Card</button>
            <button onClick={onClearSelection}>Clear Selection</button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default FilterPanel;'''
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Successfully restored {filename}")
        return True
    except Exception as e:
        print(f"❌ Failed to restore {filename}: {e}")
        return False

if __name__ == "__main__":
    success = restore_filterpanel_complete()
    sys.exit(0 if success else 1)