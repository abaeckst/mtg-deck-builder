import React, { useState, useCallback } from 'react';
import { useLayout } from '../hooks/useLayout';
import { useSelection } from '../hooks/useSelection';
import { useResize } from '../hooks/useResize';
import { useDragAndDrop, DraggedCard, DropZone as DropZoneType } from '../hooks/useDragAndDrop';
import { useContextMenu, DeckManagementCallbacks } from '../hooks/useContextMenu';
import { DeviceCapabilities } from '../utils/deviceDetection';
import './MTGOLayout.css';
import './ContextMenu.css';

// Import components
import { useCards } from '../hooks/useCards';
import { useCardSizing } from '../hooks/useCardSizing';
import DraggableCard from './DraggableCard';
import DropZoneComponent from './DropZone';
import DragPreview from './DragPreview';
import ContextMenu from './ContextMenu';

interface MTGOLayoutProps {
  // Props for any data that needs to be passed down
}

const MTGOLayout: React.FC<MTGOLayoutProps> = () => {
  const { layout, updatePanelDimensions, updateDeckAreaHeightByPixels, constraints } = useLayout();
  const { 
    selectedCards, 
    selectCard, 
    clearSelection, 
    isSelected,
    getSelectedCardObjects 
  } = useSelection();
  const { 
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
  } = useCards();
  
  // PHASE 3B-1: Card sizing system
  const { 
    sizes: cardSizes, 
    updateCollectionSize, 
    updateDeckSize, 
    updateSideboardSize 
  } = useCardSizing();
  
  // Debug logging for sizing issues
  console.log('Current card sizes:', cardSizes);
  console.log('Collection grid calc:', {
    minmax: Math.max(90, Math.round(110 * cardSizes.collection)),
    gap: Math.max(6, Math.min(12, Math.round(8 * cardSizes.collection)))
  });
  console.log('Deck grid calc:', {
    minmax: Math.max(90, Math.round(110 * cardSizes.deck)),
    gap: Math.max(6, Math.min(12, Math.round(8 * cardSizes.deck)))
  });
  
  // UPDATED: Initialize resize functionality with new percentage-based system
  const { handlers: resizeHandlers } = useResize({ 
    layout, 
    updatePanelDimensions,
    updateDeckAreaHeightByPixels, // NEW: Required for percentage-based system
    constraints 
  });
  
  // Local state for search only - filters now managed by useCards hook
  const [searchText, setSearchText] = useState('');
  
  // Deck state with proper typing
  const [mainDeck, setMainDeck] = useState<Array<{ id: string; name: string; quantity: number; [key: string]: any }>>([]);
  const [sideboard, setSideboard] = useState<Array<{ id: string; name: string; quantity: number; [key: string]: any }>>([]);
  
  // PHASE 3A: Clear deck functionality - FIXED
  const handleClearDeck = useCallback(() => {
    setMainDeck([]);
    clearSelection();
    console.log('Deck cleared - all cards moved back to collection');
  }, [clearSelection]);

  // PHASE 3A: Clear sideboard functionality
  const handleClearSideboard = useCallback(() => {
    setSideboard([]);
    clearSelection();
    console.log('Sideboard cleared - all cards moved back to collection');
  }, [clearSelection]);

  // Context menu callback implementations
  const deckManagementCallbacks: DeckManagementCallbacks = {
    addToDeck: useCallback((cards: (any)[], quantity = 1) => {
      cards.forEach(card => {
        const existingCard = mainDeck.find(deckCard => deckCard.id === card.id);
        const currentQuantity = existingCard?.quantity || 0;
        
        if (existingCard) {
          const newQuantity = Math.min(currentQuantity + quantity, 4);
          if (newQuantity > currentQuantity) {
            setMainDeck(prev => prev.map(deckCard => 
              deckCard.id === card.id 
                ? { ...deckCard, quantity: newQuantity }
                : deckCard
            ));
          }
        } else {
          const addQuantity = Math.min(quantity, 4);
          setMainDeck(prev => [...prev, { ...card, quantity: addQuantity }]);
        }
      });
    }, [mainDeck]),

    removeFromDeck: useCallback((cards: (any)[], quantity = 1) => {
      cards.forEach(card => {
        const existingCard = mainDeck.find(deckCard => deckCard.id === card.id);
        if (existingCard) {
          const newQuantity = Math.max(0, existingCard.quantity - quantity);
          if (newQuantity === 0) {
            setMainDeck(prev => prev.filter(deckCard => deckCard.id !== card.id));
          } else {
            setMainDeck(prev => prev.map(deckCard => 
              deckCard.id === card.id 
                ? { ...deckCard, quantity: newQuantity }
                : deckCard
            ));
          }
        }
      });
    }, [mainDeck]),

    addToSideboard: useCallback((cards: (any)[], quantity = 1) => {
      cards.forEach(card => {
        const existingCard = sideboard.find(sideCard => sideCard.id === card.id);
        const currentQuantity = existingCard?.quantity || 0;
        
        if (existingCard) {
          const newQuantity = Math.min(currentQuantity + quantity, 4);
          if (newQuantity > currentQuantity) {
            setSideboard(prev => prev.map(sideCard => 
              sideCard.id === card.id 
                ? { ...sideCard, quantity: newQuantity }
                : sideCard
            ));
          }
        } else {
          const addQuantity = Math.min(quantity, 4);
          setSideboard(prev => [...prev, { ...card, quantity: addQuantity }]);
        }
      });
    }, [sideboard]),

    removeFromSideboard: useCallback((cards: (any)[], quantity = 1) => {
      cards.forEach(card => {
        const existingCard = sideboard.find(sideCard => sideCard.id === card.id);
        if (existingCard) {
          const newQuantity = Math.max(0, existingCard.quantity - quantity);
          if (newQuantity === 0) {
            setSideboard(prev => prev.filter(sideCard => sideCard.id !== card.id));
          } else {
            setSideboard(prev => prev.map(sideCard => 
              sideCard.id === card.id 
                ? { ...sideCard, quantity: newQuantity }
                : sideCard
            ));
          }
        }
      });
    }, [sideboard]),

    moveDeckToSideboard: useCallback((cards: (any)[], quantity = 1) => {
      cards.forEach(card => {
        const deckCard = mainDeck.find(dc => dc.id === card.id);
        if (deckCard) {
          const moveQuantity = Math.min(quantity, deckCard.quantity);
          
          // Remove from deck
          const newDeckQuantity = deckCard.quantity - moveQuantity;
          if (newDeckQuantity === 0) {
            setMainDeck(prev => prev.filter(dc => dc.id !== card.id));
          } else {
            setMainDeck(prev => prev.map(dc => 
              dc.id === card.id 
                ? { ...dc, quantity: newDeckQuantity }
                : dc
            ));
          }
          
          // Add to sideboard
          const existingSideCard = sideboard.find(sc => sc.id === card.id);
          if (existingSideCard) {
            setSideboard(prev => prev.map(sc => 
              sc.id === card.id 
                ? { ...sc, quantity: sc.quantity + moveQuantity }
                : sc
            ));
          } else {
            setSideboard(prev => [...prev, { ...card, quantity: moveQuantity }]);
          }
        }
      });
    }, [mainDeck, sideboard]),

    moveSideboardToDeck: useCallback((cards: (any)[], quantity = 1) => {
      cards.forEach(card => {
        const sideCard = sideboard.find(sc => sc.id === card.id);
        if (sideCard) {
          const moveQuantity = Math.min(quantity, sideCard.quantity);
          
          // Remove from sideboard
          const newSideQuantity = sideCard.quantity - moveQuantity;
          if (newSideQuantity === 0) {
            setSideboard(prev => prev.filter(sc => sc.id !== card.id));
          } else {
            setSideboard(prev => prev.map(sc => 
              sc.id === card.id 
                ? { ...sc, quantity: newSideQuantity }
                : sc
            ));
          }
          
          // Add to deck
          const existingDeckCard = mainDeck.find(dc => dc.id === card.id);
          if (existingDeckCard) {
            const newDeckQuantity = Math.min(existingDeckCard.quantity + moveQuantity, 4);
            setMainDeck(prev => prev.map(dc => 
              dc.id === card.id 
                ? { ...dc, quantity: newDeckQuantity }
                : dc
            ));
          } else {
            setMainDeck(prev => [...prev, { ...card, quantity: moveQuantity }]);
          }
        }
      });
    }, [mainDeck, sideboard]),

    getDeckQuantity: useCallback((cardId: string) => {
      return mainDeck.find(card => card.id === cardId)?.quantity || 0;
    }, [mainDeck]),

    getSideboardQuantity: useCallback((cardId: string) => {
      return sideboard.find(card => card.id === cardId)?.quantity || 0;
    }, [sideboard]),
  };

  // Initialize context menu hook
  const { contextMenuState, showContextMenu, hideContextMenu, getContextMenuActions } = useContextMenu(deckManagementCallbacks);
  
  // PHASE 3A: Enhanced drag and drop callbacks
  const dragCallbacks = {
    onCardMove: useCallback((cards: DraggedCard[], from: DropZoneType, to: DropZoneType) => {
      console.log('🚀 DRAG CALLBACK TRIGGERED');
      console.log('📊 Cards being moved:', cards.map(c => c.name));
      console.log('📊 From zone:', from, 'To zone:', to);
      console.log('📊 BEFORE - MainDeck:', mainDeck.map(c => `${c.name}(${c.quantity})`));
      console.log('📊 BEFORE - Sideboard:', sideboard.map(c => `${c.name}(${c.quantity})`));
      
      cards.forEach(card => {
        console.log(`🎯 Processing card: ${card.name}`);
        
        if (from === 'collection' && to === 'deck') {
          console.log('➡️ COLLECTION → DECK');
          const existingCard = mainDeck.find(deckCard => deckCard.id === card.id);
          console.log('📋 Existing in deck:', existingCard ? `${existingCard.name}(${existingCard.quantity})` : 'none');
          
          if (existingCard && existingCard.quantity < 4) {
            console.log('🔄 Updating existing deck card quantity');
            setMainDeck(prev => prev.map(deckCard => 
              deckCard.id === card.id 
                ? { ...deckCard, quantity: deckCard.quantity + 1 }
                : deckCard
            ));
          } else if (!existingCard) {
            console.log('🆕 Adding new card to deck');
            setMainDeck(prev => [...prev, { ...card, quantity: 1 }]);
          } else {
            console.log('❌ Cannot add - deck limit reached');
          }
        } else if (from === 'collection' && to === 'sideboard') {
          console.log('➡️ COLLECTION → SIDEBOARD');
          const existingCard = sideboard.find(sideCard => sideCard.id === card.id);
          if (existingCard && existingCard.quantity < 4) {
            setSideboard(prev => prev.map(sideCard => 
              sideCard.id === card.id 
                ? { ...sideCard, quantity: sideCard.quantity + 1 }
                : sideCard
            ));
          } else if (!existingCard) {
            setSideboard(prev => [...prev, { ...card, quantity: 1 }]);
          }
        } else if (from === 'deck' && to === 'sideboard') {
          console.log('➡️ DECK → SIDEBOARD');
          const deckCard = mainDeck.find(dc => dc.id === card.id);
          if (deckCard) {
            if (deckCard.quantity > 1) {
              setMainDeck(prev => prev.map(dc => 
                dc.id === card.id 
                  ? { ...dc, quantity: dc.quantity - 1 }
                  : dc
              ));
            } else {
              setMainDeck(prev => prev.filter(dc => dc.id !== card.id));
            }
            
            const existingCard = sideboard.find(sc => sc.id === card.id);
            if (existingCard) {
              setSideboard(prev => prev.map(sc => 
                sc.id === card.id 
                  ? { ...sc, quantity: sc.quantity + 1 }
                  : sc
              ));
            } else {
              setSideboard(prev => [...prev, { ...card, quantity: 1 }]);
            }
          }
        } else if (from === 'sideboard' && to === 'deck') {
          console.log('➡️ SIDEBOARD → DECK');
          const sideCard = sideboard.find(sc => sc.id === card.id);
          if (sideCard) {
            if (sideCard.quantity > 1) {
              setSideboard(prev => prev.map(sc => 
                sc.id === card.id 
                  ? { ...sc, quantity: sc.quantity - 1 }
                  : sc
              ));
            } else {
              setSideboard(prev => prev.filter(sc => sc.id !== card.id));
            }
            
            const existingCard = mainDeck.find(dc => dc.id === card.id);
            if (existingCard && existingCard.quantity < 4) {
              setMainDeck(prev => prev.map(dc => 
                dc.id === card.id 
                  ? { ...dc, quantity: dc.quantity + 1 }
                  : dc
              ));
            } else if (!existingCard) {
              setMainDeck(prev => [...prev, { ...card, quantity: 1 }]);
            }
          }
        } else if (from === 'deck' && to === 'collection') {
          console.log('➡️ DECK → COLLECTION');
          const deckCard = mainDeck.find(dc => dc.id === card.id);
          if (deckCard) {
            if (deckCard.quantity > 1) {
              setMainDeck(prev => prev.map(dc => 
                dc.id === card.id 
                  ? { ...dc, quantity: dc.quantity - 1 }
                  : dc
              ));
            } else {
              setMainDeck(prev => prev.filter(dc => dc.id !== card.id));
            }
          }
        } else if (from === 'sideboard' && to === 'collection') {
          console.log('➡️ SIDEBOARD → COLLECTION');
          const sideCard = sideboard.find(sc => sc.id === card.id);
          if (sideCard) {
            if (sideCard.quantity > 1) {
              setSideboard(prev => prev.map(sc => 
                sc.id === card.id 
                  ? { ...sc, quantity: sc.quantity - 1 }
                  : sc
              ));
            } else {
              setSideboard(prev => prev.filter(sc => sc.id !== card.id));
            }
          }
        }
      });
      
      // Check state after processing  
      setTimeout(() => {
        console.log('📊 AFTER - MainDeck:', mainDeck.map(c => `${c.name}(${c.quantity})`));
        console.log('📊 AFTER - Sideboard:', sideboard.map(c => `${c.name}(${c.quantity})`));
      }, 100);
      
      clearSelection();
    }, [mainDeck, sideboard, clearSelection]),

    onDragStart: useCallback((cards: DraggedCard[], from: DropZoneType) => {
      console.log(`Started dragging ${cards.length} cards from ${from}`);
    }, []),

    onDragEnd: useCallback((cards: DraggedCard[], success: boolean) => {
      console.log(`Drag ended: ${success ? 'success' : 'failed'}`);
    }, [])
  };

  // PHASE 3A: Initialize enhanced drag and drop with double-click handler
  const { dragState, startDrag, setDropZone, canDropInZone, handleDoubleClick } = useDragAndDrop(dragCallbacks);
  
  // Check if device supports MTGO interface
  const canUseMTGO = DeviceCapabilities.canUseAdvancedInterface();
  
  // Enhanced search handling with comprehensive filters - FIXED
  const handleSearch = useCallback((text: string) => {
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
  }, [searchWithAllFilters, loadPopularCards, hasActiveFilters]);
  
  // Handle any filter change with validation - FIXED v3 (Integrated Validation)
  const handleFilterChange = useCallback((filterType: string, value: any) => {
    console.log('🔧 Filter changing with validation:', filterType, '=', value);
    
    // Input validation for range fields
    if (filterType === 'cmc' && value && typeof value === 'object') {
      if (value.min !== null && value.max !== null && value.min > value.max) {
        console.log('⚠️ Validation error: CMC min cannot exceed max');
        alert('Invalid CMC range: Minimum cannot be greater than maximum');
        return;
      }
    }
    
    if (filterType === 'power' && value && typeof value === 'object') {
      if (value.min !== null && value.max !== null && value.min > value.max) {
        console.log('⚠️ Validation error: Power min cannot exceed max');
        alert('Invalid Power range: Minimum cannot be greater than maximum');
        return;
      }
    }
    
    if (filterType === 'toughness' && value && typeof value === 'object') {
      if (value.min !== null && value.max !== null && value.min > value.max) {
        console.log('⚠️ Validation error: Toughness min cannot exceed max');
        alert('Invalid Toughness range: Minimum cannot be greater than maximum');
        return;
      }
    }
    
    // Build the new filter state manually to avoid closure issues
    const newFilters = {
      ...activeFilters,
      [filterType]: value,
    };
    
    console.log('🔧 New filters will be:', newFilters);
    
    // Update the filter state
    updateFilter(filterType, value);
    
    // Trigger search immediately with the new filters (don't wait for state update)
    setTimeout(() => {
      console.log('🔧 Triggering search with new filters');
      searchWithAllFilters(searchText, newFilters);
    }, 50);
  }, [updateFilter, searchWithAllFilters, searchText, activeFilters]);
  
  
  // Card interaction handlers
  const handleCardClick = (card: any, event?: React.MouseEvent) => {
    if (contextMenuState.visible) {
      hideContextMenu();
    }
    selectCard(card.id, card, event?.ctrlKey);
  };

  const handleRightClick = useCallback((card: any, zone: DropZoneType, event: React.MouseEvent) => {
    const selectedCardObjects = getSelectedCardObjects();
    showContextMenu(event, card, zone, selectedCardObjects);
  }, [showContextMenu, getSelectedCardObjects]);
  
  // Legacy double-click handler for fallback
  const handleAddToDeck = (card: any) => {
    const existingCard = mainDeck.find((deckCard: any) => deckCard.id === card.id);
    if (existingCard && existingCard.quantity < 4) {
      setMainDeck((prev: any) => prev.map((deckCard: any) => 
        deckCard.id === card.id 
          ? { ...deckCard, quantity: deckCard.quantity + 1 }
          : deckCard
      ));
    } else if (!existingCard) {
      setMainDeck((prev: any) => [...prev, { ...card, quantity: 1 }]);
    }
  };

  // Enhanced drag start handler
  const handleDragStart = useCallback((cards: DraggedCard[], zone: DropZoneType, event: React.MouseEvent) => {
    startDrag(cards, zone, event);
  }, [startDrag]);

  // Enhanced drop zone handlers
  const handleDragEnter = useCallback((zone: DropZoneType, canDrop: boolean) => {
    setDropZone(zone, canDrop);
  }, [setDropZone]);

  const handleDragLeave = useCallback(() => {
    setDropZone(null, false);
  }, [setDropZone]);
  
  // Mobile fallback
  if (!canUseMTGO) {
    return (
      <div className="mtgo-mobile-warning">
        <h2>Desktop Required</h2>
        <p>This MTGO-style interface requires a desktop computer with mouse support for optimal deck building experience.</p>
        <p>Please use a desktop or laptop computer to access the full functionality.</p>
      </div>
    );
  }
  
  return (
    <div className="mtgo-layout">
      {/* Drag Preview */}
      <DragPreview dragState={dragState} />
      
      {/* Enhanced Filter Panel - Left Side */}
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
      </div>
      
      {/* Main Content Area */}
      <div className="mtgo-main-content">
        {/* Collection Grid - Drop Zone */}
        <DropZoneComponent
          zone="collection"
          onDragEnter={handleDragEnter}
          onDragLeave={handleDragLeave}
          canDrop={canDropInZone('collection', dragState.draggedCards)}
          isDragActive={dragState.isDragging}
          className="mtgo-collection-area"
        >
          <div className="panel-header">
            <h3>Collection ({cards.length} cards)</h3>
            <div className="view-controls">
              <span>Size: </span>
              <input
                type="range"
                min="0.7"
                max="2.5"
                step="0.1"
                value={cardSizes.collection}
                onChange={(e) => updateCollectionSize(parseFloat(e.target.value))}
                className="size-slider"
                title={`Card size: ${Math.round(cardSizes.collection * 100)}%`}
              />
              <span>View: </span>
              <button className="active">Card</button>
              <button>List</button>
            </div>
          </div>
          
          <div 
            className="collection-grid"
            style={{
              display: 'grid',
              gridTemplateColumns: `repeat(auto-fill, minmax(${Math.round(130 * cardSizes.collection)}px, max-content))`,
              gap: `${Math.round(4 * cardSizes.collection)}px`,
              alignContent: 'start',
              padding: '8px'
            }}
          >
            {loading && <div className="loading-message">Loading cards...</div>}
            {error && <div className="error-message">Error: {error}</div>}
            {!loading && !error && cards.length === 0 && (
              <div className="no-results-message">
                <div className="no-results-icon">🔍</div>
                <h3>No cards found</h3>
                <p>No cards match your current search and filter criteria.</p>
                <div className="no-results-suggestions">
                  <p><strong>Try:</strong></p>
                  <ul>
                    <li>Adjusting your search terms</li>
                    <li>Changing filter settings</li>
                    <li>Using broader criteria</li>
                    <li>Clearing some filters</li>
                  </ul>
                </div>
              </div>
            )}
            {cards.map(card => (
              <DraggableCard
                key={card.id}
                card={card}
                zone="collection"
                size="normal"
                scaleFactor={cardSizes.collection}
                onClick={(card, event) => handleCardClick(card, event)} 
                onDoubleClick={handleAddToDeck}
                onEnhancedDoubleClick={handleDoubleClick}
                onRightClick={handleRightClick}
                onDragStart={handleDragStart}
                showQuantity={true}
                availableQuantity={4}
                quantity={mainDeck.find((dc: any) => dc.id === card.id)?.quantity || 0}
                selected={isSelected(card.id)}
                selectable={true}
                isDragActive={dragState.isDragging}
                isBeingDragged={dragState.draggedCards.some(dc => dc.id === card.id)}
                selectedCards={getSelectedCardObjects()}
              />
            ))}
          </div>
          
          {/* PHASE 3A: Enhanced Resize Handle with larger hit zone */}
          <div 
            className="resize-handle resize-handle-bottom"
            onMouseDown={resizeHandlers.onDeckAreaResize}
            title="Drag to resize collection area"
            style={{
              position: 'absolute',
              left: 0,
              bottom: -15,
              width: '100%',
              height: 30,
              cursor: 'ns-resize',
              background: 'transparent',
              zIndex: 1001
            }}
          />
        </DropZoneComponent>
        
        {/* Bottom Area */}
        <div className="mtgo-bottom-area">
          {/* PHASE 3A: NEW - Vertical Resize Handle at top of bottom area */}
          <div 
            className="resize-handle resize-handle-vertical"
            onMouseDown={resizeHandlers.onVerticalResize}
            title="Drag to resize between collection and deck areas"
            style={{
              position: 'absolute',
              top: -15,
              left: 0,
              width: '100%',
              height: 30,
              cursor: 'ns-resize',
              background: 'transparent',
              zIndex: 1001
            }}
          />
          
          {/* Main Deck Area - Drop Zone */}
          <DropZoneComponent
            zone="deck"
            onDragEnter={handleDragEnter}
            onDragLeave={handleDragLeave}
            canDrop={canDropInZone('deck', dragState.draggedCards)}
            isDragActive={dragState.isDragging}
            className="mtgo-deck-area"
          >
            <div className="panel-header">
              <h3>Main Deck ({mainDeck.reduce((sum: number, card: any) => sum + card.quantity, 0)} cards)</h3>
              <div className="deck-controls">
                <span>Size: </span>
                <input
                  type="range"
                  min="0.7"
                  max="2.5"
                  step="0.1"
                  value={cardSizes.deck}
                  onChange={(e) => updateDeckSize(parseFloat(e.target.value))}
                  className="size-slider"
                  title={`Card size: ${Math.round(cardSizes.deck * 100)}%`}
                />
                <button>Save Deck</button>
                <button onClick={handleClearDeck} title="Clear all cards from deck">
                  Clear Deck
                </button>
              </div>
            </div>
            
            <div className="deck-content">
              <div 
                className="deck-grid"
                style={{
                  display: 'grid',
                  gridTemplateColumns: `repeat(auto-fill, minmax(${Math.round(130 * cardSizes.deck)}px, 1fr))`,
                  gap: `${Math.round(4 * cardSizes.deck)}px`,
                  alignContent: 'start',
                  minHeight: '150px',
                  paddingBottom: '40px'
                }}
              >
                {mainDeck.map((deckCard: any) => (
                  <DraggableCard
                    key={deckCard.id}
                    card={deckCard}
                    zone="deck"
                    size="normal"
                    scaleFactor={cardSizes.deck}
                    onClick={(card, event) => handleCardClick(card, event)}
                    onEnhancedDoubleClick={handleDoubleClick}
                    onRightClick={handleRightClick}
                    onDragStart={handleDragStart}
                    showQuantity={true}
                    quantity={deckCard.quantity}
                    selected={isSelected(deckCard.id)}
                    selectable={true}
                    isDragActive={dragState.isDragging}
                    isBeingDragged={dragState.draggedCards.some(dc => dc.id === deckCard.id)}
                    selectedCards={getSelectedCardObjects()}
                  />
                ))}
                {mainDeck.length === 0 && (
                  <div className="empty-deck-message">
                    Double-click or drag cards from the collection to add them to your deck
                  </div>
                )}
              </div>
            </div>
          </DropZoneComponent>
          
          {/* Sideboard Panel - Drop Zone */}
          <DropZoneComponent
            zone="sideboard"
            onDragEnter={handleDragEnter}
            onDragLeave={handleDragLeave}
            canDrop={canDropInZone('sideboard', dragState.draggedCards)}
            isDragActive={dragState.isDragging}
            className="mtgo-sideboard-panel"
            style={{ width: layout.panels.sideboardWidth }}
          >
            <div className="panel-header">
              <h3>Sideboard ({sideboard.reduce((sum: number, card: any) => sum + card.quantity, 0)})</h3>
              <div className="sideboard-controls">
                <span>Size: </span>
                <input
                  type="range"
                  min="0.7"
                  max="2.5"
                  step="0.1"
                  value={cardSizes.sideboard}
                  onChange={(e) => updateSideboardSize(parseFloat(e.target.value))}
                  className="size-slider"
                  title={`Card size: ${Math.round(cardSizes.sideboard * 100)}%`}
                />
                <button onClick={handleClearSideboard} title="Clear all cards from sideboard">
                  Clear
                </button>
              </div>
            </div>
            
            <div className="sideboard-content">
              <div 
                className="sideboard-grid"
                style={{
                  display: 'grid',
                  gridTemplateColumns: `repeat(auto-fill, minmax(${Math.round(130 * cardSizes.sideboard)}px, 1fr))`,
                  gap: `${Math.round(4 * cardSizes.sideboard)}px`,
                  alignContent: 'start',
                  minHeight: '150px',
                  paddingBottom: '40px'
                }}
              >
                {sideboard.map((sideCard: any) => (
                  <DraggableCard
                    key={sideCard.id}
                    card={sideCard}
                    zone="sideboard"
                    size="normal"
                    scaleFactor={cardSizes.sideboard}
                    onClick={(card, event) => handleCardClick(card, event)}
                    onEnhancedDoubleClick={handleDoubleClick}
                    onRightClick={handleRightClick}
                    onDragStart={handleDragStart}
                    showQuantity={true}
                    quantity={sideCard.quantity}
                    selected={isSelected(sideCard.id)}
                    selectable={true}
                    isDragActive={dragState.isDragging}
                    isBeingDragged={dragState.draggedCards.some(dc => dc.id === sideCard.id)}
                    selectedCards={getSelectedCardObjects()}
                  />
                ))}
                {sideboard.length === 0 && (
                  <div className="empty-sideboard-message">
                    Drag cards here for your sideboard
                  </div>
                )}
              </div>
            </div>
            
            {/* PHASE 3A: Enhanced Resize Handle with larger hit zone */}
            <div 
              className="resize-handle resize-handle-left"
              onMouseDown={resizeHandlers.onSideboardResize}
              title="Drag to resize sideboard"
              style={{
                position: 'absolute',
                top: 0,
                left: -15,
                width: 30,
                height: '100%',
                cursor: 'ew-resize',
                background: 'transparent',
                zIndex: 1001
              }}
            />
          </DropZoneComponent>
        </div>
      </div>

      {/* Context Menu */}
      <ContextMenu
        visible={contextMenuState.visible}
        x={contextMenuState.x}
        y={contextMenuState.y}
        actions={getContextMenuActions()}
        onClose={hideContextMenu}
      />
    </div>
  );
};

export default MTGOLayout;