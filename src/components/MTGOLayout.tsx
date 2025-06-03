import React, { useState, useCallback, useEffect, useRef, useMemo } from 'react';
import { useLayout } from '../hooks/useLayout';
import { useSelection } from '../hooks/useSelection';
import { useResize } from '../hooks/useResize';
import { useDragAndDrop, DraggedCard, DropZone as DropZoneType } from '../hooks/useDragAndDrop';
import { useContextMenu, DeckManagementCallbacks } from '../hooks/useContextMenu';
import { DeviceCapabilities } from '../utils/deviceDetection';
import './MTGOLayout.css';
import './ContextMenu.css';

// Card types import
import { ScryfallCard, DeckCard, DeckCardInstance, scryfallToDeckCard, scryfallToDeckInstance, 
         deckCardToDeckInstance, isBasicLand, getTotalCardQuantity, getCardQuantityInZone, 
         removeInstancesForCard } from '../types/card';

// Import components
import { useCards } from '../hooks/useCards';
import { useCardSizing } from '../hooks/useCardSizing';
import DraggableCard from './DraggableCard';
import DropZoneComponent from './DropZone';
import DragPreview from './DragPreview';
import ContextMenu from './ContextMenu';
import SearchAutocomplete from './SearchAutocomplete';
import PileView from './PileView';
import ListView from './ListView';
import AdaptiveHeader from './AdaptiveHeader';
// Export modal imports
import { TextExportModal } from './TextExportModal';
import { ScreenshotModal } from './ScreenshotModal';
import { getFormatDisplayName } from '../utils/deckFormatting';

interface MTGOLayoutProps {
  // Props for any data that needs to be passed down
}

// Pile view sort state
type SortCriteria = 'name' | 'mana' | 'color' | 'rarity' | 'type';

// MJ's Championship Helper: Pure instance creation
const createDeckInstance = (card: ScryfallCard | DeckCard | DeckCardInstance, zone: 'deck' | 'sideboard'): DeckCardInstance => {
  // If already an instance, just update zone
  if ('instanceId' in card) {
    return { ...card, zone };
  }
  
  // If ScryfallCard, convert directly
  if ('oracle_id' in card) {
    return scryfallToDeckInstance(card as ScryfallCard, zone);
  }
  
  // If DeckCard, convert using bridge function
  return deckCardToDeckInstance(card as DeckCard, zone);
};

const MTGOLayout: React.FC<MTGOLayoutProps> = () => {
  const { layout, updatePanelDimensions, updateDeckAreaHeightByPixels, updateViewMode, constraints } = useLayout();
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
  const [mainDeck, setMainDeck] = useState<DeckCardInstance[]>([]);
  const [sideboard, setSideboard] = useState<DeckCardInstance[]>([]);
  // Export modal state
  const [showTextExportModal, setShowTextExportModal] = useState(false);
  const [showScreenshotModal, setShowScreenshotModal] = useState(false);
  
  // Universal sort state for all areas and view modes
  const [collectionSortCriteria, setCollectionSortCriteria] = useState<SortCriteria>('name');
  const [collectionSortDirection, setCollectionSortDirection] = useState<'asc' | 'desc'>('asc');
  const [deckSortCriteria, setDeckSortCriteria] = useState<SortCriteria>('mana');
  const [deckSortDirection, setDeckSortDirection] = useState<'asc' | 'desc'>('asc');
  const [sideboardSortCriteria, setSideboardSortCriteria] = useState<SortCriteria>('mana');
  const [sideboardSortDirection, setSideboardSortDirection] = useState<'asc' | 'desc'>('asc');
  
  // Sort menu visibility state for all areas
  const [showCollectionSortMenu, setShowCollectionSortMenu] = useState(false);
  const [showDeckSortMenu, setShowDeckSortMenu] = useState(false);
  const [showSideboardSortMenu, setShowSideboardSortMenu] = useState(false);
  
  // Refs for click-outside detection
  const collectionSortRef = useRef<HTMLDivElement>(null);
  const deckSortRef = useRef<HTMLDivElement>(null);
  const sideboardSortRef = useRef<HTMLDivElement>(null);
  // Click-outside effect for sort menus
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (collectionSortRef.current && !collectionSortRef.current.contains(event.target as Node)) {
        setShowCollectionSortMenu(false);
      }
      if (deckSortRef.current && !deckSortRef.current.contains(event.target as Node)) {
        setShowDeckSortMenu(false);
      }
      if (sideboardSortRef.current && !sideboardSortRef.current.contains(event.target as Node)) {
        setShowSideboardSortMenu(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, []);
  
  // Clear both deck and sideboard functionality
  const handleClearDeck = useCallback(() => {
    setMainDeck([]);
    setSideboard([]);
    clearSelection();
    console.log('Deck and sideboard cleared - all cards moved back to collection');
  }, [clearSelection]);
  // Export modal handlers
  const handleTextExport = useCallback(() => {
    setShowTextExportModal(true);
  }, []);
  
  const handleScreenshot = useCallback(() => {
    setShowScreenshotModal(true);
  }, []);
  
  const handleCloseTextExport = useCallback(() => {
    setShowTextExportModal(false);
  }, []);
  
  const handleCloseScreenshot = useCallback(() => {
    setShowScreenshotModal(false);
  }, []);

  // Helper to safely get card ID from any card type
  // Helper to safely get card ID from any card type
  const getCardId = (card: ScryfallCard | DeckCard | DeckCardInstance): string => {
    if ('instanceId' in card) {
      return card.cardId; // DeckCardInstance - use cardId (original Scryfall ID)
    }
    return card.id; // ScryfallCard or DeckCard - use id
  };
  
  // Helper to get original card ID for quantity tracking
  const getOriginalCardId = (card: ScryfallCard | DeckCard | DeckCardInstance): string => {
    if ('cardId' in card) return card.cardId;
    return card.id;
  };

// Helper function to get total copies across deck and sideboard
  const getTotalCopies = useCallback((cardId: string): number => {
    return getTotalCardQuantity(mainDeck, sideboard, cardId);
  }, [mainDeck, sideboard]);
  
  // Helper functions for individual zone quantities
  const getDeckQuantity = useCallback((cardId: string): number => {
    return getCardQuantityInZone(mainDeck, cardId);
  }, [mainDeck]);

  const getSideboardQuantity = useCallback((cardId: string): number => {
    return getCardQuantityInZone(sideboard, cardId);
  }, [sideboard]);

  // PHASE 3A: Clear sideboard functionality
  const handleClearSideboard = useCallback(() => {
    setSideboard([]);
    clearSelection();
    console.log('Sideboard cleared - all cards moved back to collection');
  }, [clearSelection]);

  // Context menu callback implementations
  const deckManagementCallbacks: DeckManagementCallbacks = {
    addToDeck: useCallback((cards: (ScryfallCard | DeckCard | DeckCardInstance)[], quantity = 1) => {
      cards.forEach(card => {
        const cardId = getCardId(card);
        const totalCopies = getTotalCopies(cardId);
        const isBasic = isBasicLand(card);
        const maxAllowed = isBasic ? Infinity : 4;
        const canAdd = Math.max(0, maxAllowed - totalCopies);
        const actualQuantity = Math.min(quantity, canAdd);
        
        // MJ's way: Create the exact number of instances needed
        const newInstances: DeckCardInstance[] = [];
        for (let i = 0; i < actualQuantity; i++) {
          newInstances.push(createDeckInstance(card, 'deck'));
        }
        
        if (newInstances.length > 0) {
          setMainDeck(prev => [...prev, ...newInstances]);
        }
      });
    }, [getTotalCopies]),

    removeFromDeck: useCallback((cards: (ScryfallCard | DeckCard | DeckCardInstance)[], quantity = 1) => {
      cards.forEach(card => {
        const cardId = 'cardId' in card ? card.cardId : getCardId(card);
        setMainDeck(prev => removeInstancesForCard(prev, cardId, quantity));
      });
    }, []),

    addToSideboard: useCallback((cards: (ScryfallCard | DeckCard | DeckCardInstance)[], quantity = 1) => {
      cards.forEach(card => {
        const cardId = getCardId(card);
        const totalCopies = getTotalCopies(cardId);
        const isBasic = isBasicLand(card);
        const maxAllowed = isBasic ? Infinity : 4;
        const canAdd = Math.max(0, maxAllowed - totalCopies);
        const actualQuantity = Math.min(quantity, canAdd);
        
        // MJ's way: Create the exact number of instances needed
        const newInstances: DeckCardInstance[] = [];
        for (let i = 0; i < actualQuantity; i++) {
          newInstances.push(createDeckInstance(card, 'sideboard'));
        }
        
        if (newInstances.length > 0) {
          setSideboard(prev => [...prev, ...newInstances]);
        }
      });
    }, [getTotalCopies]),

    removeFromSideboard: useCallback((cards: (ScryfallCard | DeckCard | DeckCardInstance)[], quantity = 1) => {
      cards.forEach(card => {
        const cardId = 'cardId' in card ? card.cardId : getCardId(card);
        setSideboard(prev => removeInstancesForCard(prev, cardId, quantity));
      });
    }, []),

    moveDeckToSideboard: useCallback((cards: (ScryfallCard | DeckCard | DeckCardInstance)[], quantity = 1) => {
      cards.forEach(card => {
        const cardId = getCardId(card);
        // MJ's approach: Find actual instances and move them
        const instancesToMove = mainDeck.filter(instance => instance.cardId === cardId).slice(0, quantity);
        
        if (instancesToMove.length > 0) {
          // Remove from deck
          setMainDeck(prev => prev.filter(instance => !instancesToMove.includes(instance)));
          // Add to sideboard with updated zone
          const sideboardInstances = instancesToMove.map(instance => ({ ...instance, zone: 'sideboard' as const }));
          setSideboard(prev => [...prev, ...sideboardInstances]);
        }
      });
    }, [mainDeck]),

    moveSideboardToDeck: useCallback((cards: (ScryfallCard | DeckCard | DeckCardInstance)[], quantity = 1) => {
      cards.forEach(card => {
        const cardId = getCardId(card);
        // MJ's approach: Find actual instances and move them
        const instancesToMove = sideboard.filter(instance => instance.cardId === cardId).slice(0, quantity);
        
        if (instancesToMove.length > 0) {
          // Remove from sideboard
          setSideboard(prev => prev.filter(instance => !instancesToMove.includes(instance)));
          // Add to deck with updated zone  
          const deckInstances = instancesToMove.map(instance => ({ ...instance, zone: 'deck' as const }));
          setMainDeck(prev => [...prev, ...deckInstances]);
        }
      });
    }, [sideboard]),

    getDeckQuantity: useCallback((cardId: string) => {
      return getDeckQuantity(cardId);
    }, [getDeckQuantity]),

    getSideboardQuantity: useCallback((cardId: string) => {
      return getSideboardQuantity(cardId);
    }, [getSideboardQuantity]),
  };

  // Initialize context menu hook
  const { contextMenuState, showContextMenu, hideContextMenu, getContextMenuActions } = useContextMenu(deckManagementCallbacks);
  
  // PHASE 3A: Enhanced drag and drop callbacks
  const dragCallbacks = {
    onCardMove: useCallback((cards: DraggedCard[], from: DropZoneType, to: DropZoneType) => {
      console.log(`🏀 MJ's drag handler: Moving ${cards.length} cards from ${from} to ${to}`);
      
      cards.forEach(card => {
        const cardId = getCardId(card);
        
        if (from === 'collection' && to === 'deck') {
          const totalCopies = getTotalCopies(cardId);
          const isBasic = isBasicLand(card);
          const maxAllowed = isBasic ? Infinity : 4;
          
          if (totalCopies < maxAllowed) {
            const newInstance = createDeckInstance(card, 'deck');
            setMainDeck(prev => [...prev, newInstance]);
          }
        } else if (from === 'collection' && to === 'sideboard') {
          const totalCopies = getTotalCopies(cardId);
          const isBasic = isBasicLand(card);
          const maxAllowed = isBasic ? Infinity : 4;
          
          if (totalCopies < maxAllowed) {
            const newInstance = createDeckInstance(card, 'sideboard');
            setSideboard(prev => [...prev, newInstance]);
          }
        } else if (from === 'deck' && to === 'sideboard') {
          // Move one instance from deck to sideboard
          const instanceToMove = mainDeck.find(instance => instance.cardId === cardId);
          if (instanceToMove) {
            setMainDeck(prev => prev.filter(instance => instance !== instanceToMove));
            setSideboard(prev => [...prev, { ...instanceToMove, zone: 'sideboard' }]);
          }
        } else if (from === 'sideboard' && to === 'deck') {
          // Move one instance from sideboard to deck
          const instanceToMove = sideboard.find(instance => instance.cardId === cardId);
          if (instanceToMove) {
            setSideboard(prev => prev.filter(instance => instance !== instanceToMove));
            setMainDeck(prev => [...prev, { ...instanceToMove, zone: 'deck' }]);
          }
        } else if (from === 'deck' && to === 'collection') {
          // Remove one instance from deck
          const instanceToRemove = mainDeck.find(instance => instance.cardId === cardId);
          if (instanceToRemove) {
            setMainDeck(prev => prev.filter(instance => instance !== instanceToRemove));
          }
        } else if (from === 'sideboard' && to === 'collection') {
          // Remove one instance from sideboard
          const instanceToRemove = sideboard.find(instance => instance.cardId === cardId);
          if (instanceToRemove) {
            setSideboard(prev => prev.filter(instance => instance !== instanceToRemove));
          }
        }
      });
      
      clearSelection();
    }, [mainDeck, sideboard, getTotalCopies, clearSelection]),

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
    console.log('🔍 Enhanced search triggered:', { text, hasFilters: hasActiveFilters() });
    // Use enhanced search for better results
    if (text.trim()) {
      enhancedSearch(text);
    } else if (hasActiveFilters()) {
      enhancedSearch('');
    } else {
      loadPopularCards();
    }
  }, [enhancedSearch, loadPopularCards, hasActiveFilters]);
  
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
      console.log('🔧 Triggering enhanced search with new filters');
      enhancedSearch(searchText, newFilters);
    }, 50);
  }, [updateFilter, enhancedSearch, searchText, activeFilters]);

  // Card interaction handlers
  const handleCardClick = useCallback((card: ScryfallCard | DeckCard | DeckCardInstance, event?: React.MouseEvent) => {
    if (contextMenuState.visible) {
      hideContextMenu();
    }
    selectCard(getCardId(card), card as any, event?.ctrlKey);
  }, [contextMenuState.visible, hideContextMenu, selectCard]);

  // Instance-based click handler for deck/sideboard cards
  const handleInstanceClick = useCallback((instanceId: string, instance: DeckCardInstance, event: React.MouseEvent) => {
    if (contextMenuState.visible) {
      hideContextMenu();
    }
    // Use instance-based selection for deck/sideboard cards
    console.log(`Instance click: ${instanceId} for card ${instance.name}`);
    selectCard(instanceId, instance as any, event.ctrlKey);
  }, [contextMenuState.visible, hideContextMenu, selectCard]);

    const handleRightClick = useCallback((card: any, zone: DropZoneType, event: React.MouseEvent) => {
    const selectedCardObjects = getSelectedCardObjects();
    showContextMenu(event, card, zone, selectedCardObjects);
  }, [showContextMenu, getSelectedCardObjects]);
  
  // Legacy double-click handler for fallback
  const handleAddToDeck = useCallback((card: ScryfallCard | DeckCard | DeckCardInstance) => {
    const cardId = getCardId(card);
    const totalCopies = getTotalCopies(cardId);
    const isBasic = isBasicLand(card);
    const maxAllowed = isBasic ? Infinity : 4;
    
    if (totalCopies < maxAllowed) {
      const newInstance = createDeckInstance(card, 'deck');
      setMainDeck(prev => [...prev, newInstance]);
    }
  }, [getTotalCopies]);

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

  // Card sorting helper function for all areas
  const sortCards = useCallback((cards: (ScryfallCard | DeckCard | DeckCardInstance)[], criteria: SortCriteria, direction: 'asc' | 'desc'): (ScryfallCard | DeckCard | DeckCardInstance)[] => {
    const sorted = [...cards].sort((a, b) => {
      let comparison = 0;
      
      switch (criteria) {
        case 'name':
          comparison = a.name.localeCompare(b.name);
          break;
        case 'mana':
          comparison = (a.cmc ?? 0) - (b.cmc ?? 0);
          break;
        case 'color':
          const aColors = a.colors?.join('') || 'Z';
          const bColors = b.colors?.join('') || 'Z';
          comparison = aColors.localeCompare(bColors);
          break;
        case 'rarity':
          const rarityOrder = { common: 1, uncommon: 2, rare: 3, mythic: 4 };
          const aRarity = rarityOrder[a.rarity as keyof typeof rarityOrder] || 0;
          const bRarity = rarityOrder[b.rarity as keyof typeof rarityOrder] || 0;
          comparison = aRarity - bRarity;
          break;
        case 'type':
          const aType = a.type_line || '';
          const bType = b.type_line || '';
          comparison = aType.localeCompare(bType);
          break;
        default:
          comparison = a.name.localeCompare(b.name);
      }
      
      return direction === 'desc' ? -comparison : comparison;
    });
    
    return sorted;
  }, []);

  // Get sorted cards for each area
  const sortedCollectionCards = useMemo(() => {
    return sortCards(cards, collectionSortCriteria, collectionSortDirection);
  }, [cards, collectionSortCriteria, collectionSortDirection, sortCards]);

  const sortedMainDeck = useMemo((): DeckCardInstance[] => {
    return layout.viewModes.deck === 'pile' ? mainDeck : sortCards(mainDeck as any, deckSortCriteria, deckSortDirection) as DeckCardInstance[];
  }, [mainDeck, deckSortCriteria, deckSortDirection, layout.viewModes.deck, sortCards]);

  const sortedSideboard = useMemo((): DeckCardInstance[] => {
    return layout.viewModes.sideboard === 'pile' ? sideboard : sortCards(sideboard as any, sideboardSortCriteria, sideboardSortDirection) as DeckCardInstance[];
  }, [sideboard, sideboardSortCriteria, sideboardSortDirection, layout.viewModes.sideboard, sortCards]);

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
              <div className="sort-button-container" ref={collectionSortRef}>
                <button 
                  className="sort-toggle-btn"
                  onClick={() => setShowCollectionSortMenu(!showCollectionSortMenu)}
                  title="Sort options"
                >
                  Sort
                </button>
                {showCollectionSortMenu && (
                  <div className="sort-menu">
                    <button 
                      className={collectionSortCriteria === 'name' ? 'active' : ''}
                      onClick={() => { 
                        if (collectionSortCriteria === 'name') {
                          setCollectionSortDirection(collectionSortDirection === 'asc' ? 'desc' : 'asc');
                        } else {
                          setCollectionSortCriteria('name'); 
                          setCollectionSortDirection('asc');
                        }
                        setShowCollectionSortMenu(false); 
                      }}
                    >
                      Name {collectionSortCriteria === 'name' ? (collectionSortDirection === 'asc' ? '↑' : '↓') : ''}
                    </button>
                    <button 
                      className={collectionSortCriteria === 'mana' ? 'active' : ''}
                      onClick={() => { 
                        if (collectionSortCriteria === 'mana') {
                          setCollectionSortDirection(collectionSortDirection === 'asc' ? 'desc' : 'asc');
                        } else {
                          setCollectionSortCriteria('mana'); 
                          setCollectionSortDirection('asc');
                        }
                        setShowCollectionSortMenu(false); 
                      }}
                    >
                      Mana Value {collectionSortCriteria === 'mana' ? (collectionSortDirection === 'asc' ? '↑' : '↓') : ''}
                    </button>
                    <button 
                      className={collectionSortCriteria === 'color' ? 'active' : ''}
                      onClick={() => { 
                        if (collectionSortCriteria === 'color') {
                          setCollectionSortDirection(collectionSortDirection === 'asc' ? 'desc' : 'asc');
                        } else {
                          setCollectionSortCriteria('color'); 
                          setCollectionSortDirection('asc');
                        }
                        setShowCollectionSortMenu(false); 
                      }}
                    >
                      Color {collectionSortCriteria === 'color' ? (collectionSortDirection === 'asc' ? '↑' : '↓') : ''}
                    </button>
                    <button 
                      className={collectionSortCriteria === 'rarity' ? 'active' : ''}
                      onClick={() => { 
                        if (collectionSortCriteria === 'rarity') {
                          setCollectionSortDirection(collectionSortDirection === 'asc' ? 'desc' : 'asc');
                        } else {
                          setCollectionSortCriteria('rarity'); 
                          setCollectionSortDirection('asc');
                        }
                        setShowCollectionSortMenu(false); 
                      }}
                    >
                      Rarity {collectionSortCriteria === 'rarity' ? (collectionSortDirection === 'asc' ? '↑' : '↓') : ''}
                    </button>
                    <button 
                      className={collectionSortCriteria === 'type' ? 'active' : ''}
                      onClick={() => { 
                        if (collectionSortCriteria === 'type') {
                          setCollectionSortDirection(collectionSortDirection === 'asc' ? 'desc' : 'asc');
                        } else {
                          setCollectionSortCriteria('type'); 
                          setCollectionSortDirection('asc');
                        }
                        setShowCollectionSortMenu(false); 
                      }}
                    >
                      Card Type {collectionSortCriteria === 'type' ? (collectionSortDirection === 'asc' ? '↑' : '↓') : ''}
                    </button>
                  </div>
                )}
              </div>
              <span>View: </span>
              <button 
                className={layout.viewModes.collection === 'grid' ? 'active' : ''}
                onClick={() => { clearSelection(); updateViewMode('collection', 'grid'); }}
              >
                Card
              </button>
              <button 
                className={layout.viewModes.collection === 'list' ? 'active' : ''}
                onClick={() => { clearSelection(); updateViewMode('collection', 'list'); }}
              >
                List
              </button>
            </div>
          </div>
          
          {/* Collection Content - Conditional Rendering */}
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
          
          {!loading && !error && cards.length > 0 && (
            layout.viewModes.collection === 'list' ? (
              <ListView
                cards={sortedCollectionCards}
                area="collection"
                scaleFactor={cardSizes.collection}
                sortCriteria={collectionSortCriteria}
                sortDirection={collectionSortDirection}
                onSortChange={(criteria, direction) => {
                  setCollectionSortCriteria(criteria);
                  setCollectionSortDirection(direction);
                }}
                onClick={handleCardClick}
                onDoubleClick={handleAddToDeck}
                onRightClick={handleRightClick}
                onDragStart={handleDragStart}
                isSelected={isSelected}
                selectedCards={getSelectedCardObjects()}
                isDragActive={dragState.isDragging}
              />
            ) : (
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
                {sortedCollectionCards.map((card) => (
                  <DraggableCard
                    key={getCardId(card)}
                    card={card}
                    zone="collection"
                    size="normal"
                    scaleFactor={cardSizes.collection}
                    onClick={(card, event) => handleCardClick(card, event)} 
                    onDoubleClick={(card) => handleAddToDeck(card)}
                    onEnhancedDoubleClick={handleDoubleClick}
                    onRightClick={handleRightClick}
                    onDragStart={handleDragStart}
                    showQuantity={true}
                    availableQuantity={4}
                    quantity={getTotalCopies(getCardId(card))}
                    selected={isSelected(getCardId(card))}
                    selectable={true}
                    isDragActive={dragState.isDragging}
                    isBeingDragged={dragState.draggedCards.some(dc => getCardId(dc) === getCardId(card))}
                    selectedCards={getSelectedCardObjects()}
                  />
                ))}
              </div>
            )
          )}
          
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
              <h3>Main Deck ({mainDeck.length} cards)</h3>
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
                <div className="sort-button-container" ref={deckSortRef}>
                  <button 
                    className="sort-toggle-btn"
                    onClick={() => setShowDeckSortMenu(!showDeckSortMenu)}
                    title="Sort options"
                  >
                    Sort
                  </button>
                  {showDeckSortMenu && (
                    <div className="sort-menu">
                      <button 
                        className={deckSortCriteria === 'mana' ? 'active' : ''}
                        onClick={() => { 
                          if (layout.viewModes.deck === 'card' && deckSortCriteria === 'mana') {
                            setDeckSortDirection(deckSortDirection === 'asc' ? 'desc' : 'asc');
                          } else {
                            setDeckSortCriteria('mana'); 
                            if (layout.viewModes.deck === 'card') setDeckSortDirection('asc');
                          }
                          setShowDeckSortMenu(false); 
                        }}
                      >
                        Mana Value {deckSortCriteria === 'mana' && layout.viewModes.deck === 'card' ? (deckSortDirection === 'asc' ? '↑' : '↓') : ''}
                      </button>
                      <button 
                        className={deckSortCriteria === 'color' ? 'active' : ''}
                        onClick={() => { 
                          if (layout.viewModes.deck === 'card' && deckSortCriteria === 'color') {
                            setDeckSortDirection(deckSortDirection === 'asc' ? 'desc' : 'asc');
                          } else {
                            setDeckSortCriteria('color'); 
                            if (layout.viewModes.deck === 'card') setDeckSortDirection('asc');
                          }
                          setShowDeckSortMenu(false); 
                        }}
                      >
                        Color {deckSortCriteria === 'color' && layout.viewModes.deck === 'card' ? (deckSortDirection === 'asc' ? '↑' : '↓') : ''}
                      </button>
                      <button 
                        className={deckSortCriteria === 'rarity' ? 'active' : ''}
                        onClick={() => { 
                          if (layout.viewModes.deck === 'card' && deckSortCriteria === 'rarity') {
                            setDeckSortDirection(deckSortDirection === 'asc' ? 'desc' : 'asc');
                          } else {
                            setDeckSortCriteria('rarity'); 
                            if (layout.viewModes.deck === 'card') setDeckSortDirection('asc');
                          }
                          setShowDeckSortMenu(false); 
                        }}
                      >
                        Rarity {deckSortCriteria === 'rarity' && layout.viewModes.deck === 'card' ? (deckSortDirection === 'asc' ? '↑' : '↓') : ''}
                      </button>
                      <button 
                        className={deckSortCriteria === 'type' ? 'active' : ''}
                        onClick={() => { 
                          if (layout.viewModes.deck === 'card' && deckSortCriteria === 'type') {
                            setDeckSortDirection(deckSortDirection === 'asc' ? 'desc' : 'asc');
                          } else {
                            setDeckSortCriteria('type'); 
                            if (layout.viewModes.deck === 'card') setDeckSortDirection('asc');
                          }
                          setShowDeckSortMenu(false); 
                        }}
                      >
                        Card Type {deckSortCriteria === 'type' && layout.viewModes.deck === 'card' ? (deckSortDirection === 'asc' ? '↑' : '↓') : ''}
                      </button>
                    </div>
                  )}
                </div>
                <span>View: </span>
                <button 
                  className={layout.viewModes.deck === 'card' ? 'active' : ''}
                  onClick={() => { clearSelection(); updateViewMode('deck', 'card'); }}
                >
                  Card
                </button>
                <button 
                  className={layout.viewModes.deck === 'pile' ? 'active' : ''}
                  onClick={() => { clearSelection(); updateViewMode('deck', 'pile'); }}
                >
                  Pile
                </button>
                <button 
                  className={layout.viewModes.deck === 'list' ? 'active' : ''}
                  onClick={() => { clearSelection(); updateViewMode('deck', 'list'); }}
                >
                  List
                </button>                <button onClick={handleTextExport} title="Export deck as text for MTGO">
                  Export Text
                </button>
                <button onClick={handleScreenshot} title="Generate deck image">
                  Screenshot
                </button>
                
                <button>Save Deck</button>
                <button onClick={handleClearDeck} title="Clear all cards from deck and sideboard">
                  Clear All
                </button>
              </div>
            </div>
            
            <div className="deck-content">
              {layout.viewModes.deck === 'pile' ? (
                <PileView
                  cards={mainDeck}
                  zone="deck"
                  scaleFactor={cardSizes.deck}
                  forcedSortCriteria={deckSortCriteria === 'name' ? 'mana' : deckSortCriteria}
                  onClick={(card, event) => handleCardClick(card, event)}
                  onInstanceClick={handleInstanceClick}
                  onDoubleClick={handleAddToDeck}
                  onEnhancedDoubleClick={handleDoubleClick}
                  onRightClick={handleRightClick}
                  onDragStart={handleDragStart}
                  isSelected={isSelected}
                  selectedCards={getSelectedCardObjects()}
                  isDragActive={dragState.isDragging}
                  onDragEnter={handleDragEnter}
                  onDragLeave={handleDragLeave}
                  canDropInZone={canDropInZone}
                />
              ) : layout.viewModes.deck === 'list' ? (
                <ListView
                  cards={sortedMainDeck}
                  area="deck"
                  scaleFactor={cardSizes.deck}
                  sortCriteria={deckSortCriteria}
                  sortDirection={deckSortDirection}
                  onSortChange={(criteria, direction) => {
                    setDeckSortCriteria(criteria);
                    setDeckSortDirection(direction);
                  }}
                  onClick={(card, event) => handleCardClick(card, event)}
                  onDoubleClick={(card) => handleDoubleClick(card as any, 'deck', { preventDefault: () => {}, stopPropagation: () => {} } as React.MouseEvent)}
                  onRightClick={handleRightClick}
                  onDragStart={handleDragStart}
                  isSelected={isSelected}
                  selectedCards={getSelectedCardObjects()}
                  isDragActive={dragState.isDragging}
                  onQuantityChange={(cardId, newQuantity) => {
                    if (newQuantity === 0) {
                      // Remove all instances of this card
                      setMainDeck(prev => prev.filter(instance => instance.cardId !== cardId));
                    } else {
                      // Add or remove instances to match desired quantity
                      const currentQuantity = getDeckQuantity(cardId);
                      const diff = newQuantity - currentQuantity;
                      
                      if (diff > 0) {
                        // Add instances
                        const cardData = cards.find(c => c.id === cardId);
                        if (cardData) {
                          const newInstances: DeckCardInstance[] = [];
                          for (let i = 0; i < diff; i++) {
                            newInstances.push(createDeckInstance(cardData, 'deck'));
                          }
                          setMainDeck(prev => [...prev, ...newInstances]);
                        }
                      } else if (diff < 0) {
                        // Remove instances
                        setMainDeck(prev => removeInstancesForCard(prev, cardId, Math.abs(diff)));
                      }
                    }
                  }}
                />
              ) : (
                <div 
                  className="deck-grid"
                  style={{
                    display: 'grid',
                    gridTemplateColumns: `repeat(auto-fill, minmax(${Math.round(130 * cardSizes.deck)}px, max-content))`,
                    gap: `${Math.round(4 * cardSizes.deck)}px`,
                    alignContent: 'start',
                    minHeight: '150px',
                    paddingBottom: '40px'
                  }}
                >
                  {(() => {
                    // Group instances by cardId for clean stacking (collection style)
                    const groupedCards = new Map<string, DeckCardInstance[]>();
                    sortedMainDeck.forEach(instance => {
                      const cardId = instance.cardId;
                      if (!groupedCards.has(cardId)) {
                        groupedCards.set(cardId, []);
                      }
                      groupedCards.get(cardId)!.push(instance);
                    });

                    return Array.from(groupedCards.entries()).map(([cardId, instances]) => {
                      const representativeCard = instances[0];
                      const quantity = instances.length;
                      const isAnySelected = instances.some(instance => isSelected(instance.instanceId));

                      const handleStackClick = (card: any, event?: React.MouseEvent) => {
                        // If multiple instances, select the first non-selected one, or all if all selected
                        if (instances.length > 1) {
                          const unselectedInstance = instances.find(inst => !isSelected(inst.instanceId));
                          const targetInstance = unselectedInstance || instances[0];
                          handleInstanceClick(targetInstance.instanceId, targetInstance, event as React.MouseEvent);
                        } else {
                          handleInstanceClick(representativeCard.instanceId, representativeCard, event as React.MouseEvent);
                        }
                      };

                      const handleStackInstanceClick = (instanceId: string, instance: DeckCardInstance, event: React.MouseEvent) => {
                        // For stacks, use the same logic but with proper signature
                        handleStackClick(instance, event);
                      };

                      const handleStackDragStart = (cards: any[], zone: any, event: React.MouseEvent) => {
                        // When dragging a stack, drag all instances of the card
                        handleDragStart(instances as any[], zone, event);
                      };

                      return (
                        <DraggableCard
                          key={cardId}
                          card={representativeCard}
                          zone="deck"
                          size="normal"
                          scaleFactor={cardSizes.deck}
                          onClick={handleStackClick}
                          instanceId={representativeCard.instanceId}
                          isInstance={true}
                          onInstanceClick={handleStackInstanceClick}
                          onEnhancedDoubleClick={handleDoubleClick}
                          onRightClick={handleRightClick}
                          onDragStart={handleStackDragStart}
                          showQuantity={true}
                          quantity={quantity}
                          selected={isAnySelected}
                          selectable={true}
                          isDragActive={dragState.isDragging}
                          isBeingDragged={dragState.draggedCards.some(dc => 
                            instances.some(inst => 
                              'instanceId' in dc ? dc.instanceId === inst.instanceId : dc.id === inst.cardId
                            )
                          )}
                          selectedCards={getSelectedCardObjects()}
                        />
                      );
                    });
                  })()}
                  
                  {mainDeck.length === 0 && (
                    <div className="empty-deck-message">
                      Double-click or drag cards from the collection to add them to your deck
                    </div>
                  )}
                </div>
              )}
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
              <h3>Sideboard ({sideboard.length})</h3>
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
                <div className="sort-button-container" ref={sideboardSortRef}>
                  <button 
                    className="sort-toggle-btn"
                    onClick={() => setShowSideboardSortMenu(!showSideboardSortMenu)}
                    title="Sort options"
                  >
                    Sort
                  </button>
                  {showSideboardSortMenu && (
                    <div className="sort-menu">
                      <button 
                        className={sideboardSortCriteria === 'mana' ? 'active' : ''}
                        onClick={() => { 
                          if (layout.viewModes.sideboard === 'card' && sideboardSortCriteria === 'mana') {
                            setSideboardSortDirection(sideboardSortDirection === 'asc' ? 'desc' : 'asc');
                          } else {
                            setSideboardSortCriteria('mana'); 
                            if (layout.viewModes.sideboard === 'card') setSideboardSortDirection('asc');
                          }
                          setShowSideboardSortMenu(false); 
                        }}
                      >
                        Mana Value {sideboardSortCriteria === 'mana' && layout.viewModes.sideboard === 'card' ? (sideboardSortDirection === 'asc' ? '↑' : '↓') : ''}
                      </button>
                      <button 
                        className={sideboardSortCriteria === 'color' ? 'active' : ''}
                        onClick={() => { 
                          if (layout.viewModes.sideboard === 'card' && sideboardSortCriteria === 'color') {
                            setSideboardSortDirection(sideboardSortDirection === 'asc' ? 'desc' : 'asc');
                          } else {
                            setSideboardSortCriteria('color'); 
                            if (layout.viewModes.sideboard === 'card') setSideboardSortDirection('asc');
                          }
                          setShowSideboardSortMenu(false); 
                        }}
                      >
                        Color {sideboardSortCriteria === 'color' && layout.viewModes.sideboard === 'card' ? (sideboardSortDirection === 'asc' ? '↑' : '↓') : ''}
                      </button>
                      <button 
                        className={sideboardSortCriteria === 'rarity' ? 'active' : ''}
                        onClick={() => { 
                          if (layout.viewModes.sideboard === 'card' && sideboardSortCriteria === 'rarity') {
                            setSideboardSortDirection(sideboardSortDirection === 'asc' ? 'desc' : 'asc');
                          } else {
                            setSideboardSortCriteria('rarity'); 
                            if (layout.viewModes.sideboard === 'card') setSideboardSortDirection('asc');
                          }
                          setShowSideboardSortMenu(false); 
                        }}
                      >
                        Rarity {sideboardSortCriteria === 'rarity' && layout.viewModes.sideboard === 'card' ? (sideboardSortDirection === 'asc' ? '↑' : '↓') : ''}
                      </button>
                      <button 
                        className={sideboardSortCriteria === 'type' ? 'active' : ''}
                        onClick={() => { 
                          if (layout.viewModes.sideboard === 'card' && sideboardSortCriteria === 'type') {
                            setSideboardSortDirection(sideboardSortDirection === 'asc' ? 'desc' : 'asc');
                          } else {
                            setSideboardSortCriteria('type'); 
                            if (layout.viewModes.sideboard === 'card') setSideboardSortDirection('asc');
                          }
                          setShowSideboardSortMenu(false); 
                        }}
                      >
                        Card Type {sideboardSortCriteria === 'type' && layout.viewModes.sideboard === 'card' ? (sideboardSortDirection === 'asc' ? '↑' : '↓') : ''}
                      </button>
                    </div>
                  )}
                </div>
                <span>View: </span>
                <button 
                  className={layout.viewModes.sideboard === 'card' ? 'active' : ''}
                  onClick={() => { clearSelection(); updateViewMode('sideboard', 'card'); }}
                >
                  Card
                </button>
                <button 
                  className={layout.viewModes.sideboard === 'pile' ? 'active' : ''}
                  onClick={() => { clearSelection(); updateViewMode('sideboard', 'pile'); }}
                >
                  Pile
                </button>
                <button 
                  className={layout.viewModes.sideboard === 'list' ? 'active' : ''}
                  onClick={() => { clearSelection(); updateViewMode('sideboard', 'list'); }}
                >
                  List
                </button>
                <button onClick={handleClearSideboard} title="Clear all cards from sideboard">
                  Clear
                </button>
              </div>
            </div>
            
            <div className="sideboard-content">
              {layout.viewModes.sideboard === 'pile' ? (
                <PileView
                  cards={sideboard}
                  zone="sideboard"
                  scaleFactor={cardSizes.sideboard}
                  forcedSortCriteria={sideboardSortCriteria === 'name' ? 'mana' : sideboardSortCriteria}
                  onClick={(card, event) => handleCardClick(card, event)}
                  onInstanceClick={handleInstanceClick}
                  onDoubleClick={handleAddToDeck}
                  onEnhancedDoubleClick={handleDoubleClick}
                  onRightClick={handleRightClick}
                  onDragStart={handleDragStart}
                  isSelected={isSelected}
                  selectedCards={getSelectedCardObjects()}
                  isDragActive={dragState.isDragging}
                  onDragEnter={handleDragEnter}
                  onDragLeave={handleDragLeave}
                  canDropInZone={canDropInZone}
                />
              ) : layout.viewModes.sideboard === 'list' ? (
                <ListView
                  cards={sortedSideboard}
                  area="sideboard"
                  scaleFactor={cardSizes.sideboard}
                  sortCriteria={sideboardSortCriteria}
                  sortDirection={sideboardSortDirection}
                  onSortChange={(criteria, direction) => {
                    setSideboardSortCriteria(criteria);
                    setSideboardSortDirection(direction);
                  }}
                  onClick={(card, event) => handleCardClick(card, event)}
                  onDoubleClick={(card) => handleDoubleClick(card as any, 'sideboard', { preventDefault: () => {}, stopPropagation: () => {} } as React.MouseEvent)}
                  onRightClick={handleRightClick}
                  onDragStart={handleDragStart}
                  isSelected={isSelected}
                  selectedCards={getSelectedCardObjects()}
                  isDragActive={dragState.isDragging}
                  onQuantityChange={(cardId, newQuantity) => {
                    if (newQuantity === 0) {
                      // Remove all instances of this card
                      setSideboard(prev => prev.filter(instance => instance.cardId !== cardId));
                    } else {
                      // Add or remove instances to match desired quantity
                      const currentQuantity = getSideboardQuantity(cardId);
                      const diff = newQuantity - currentQuantity;
                      
                      if (diff > 0) {
                        // Add instances
                        const cardData = cards.find(c => c.id === cardId);
                        if (cardData) {
                          const newInstances: DeckCardInstance[] = [];
                          for (let i = 0; i < diff; i++) {
                            newInstances.push(createDeckInstance(cardData, 'sideboard'));
                          }
                          setSideboard(prev => [...prev, ...newInstances]);
                        }
                      } else if (diff < 0) {
                        // Remove instances
                        setSideboard(prev => removeInstancesForCard(prev, cardId, Math.abs(diff)));
                      }
                    }
                  }}
                />
              ) : (
                <div 
                  className="sideboard-grid"
                  style={{
                    display: 'grid',
                    gridTemplateColumns: `repeat(auto-fill, minmax(${Math.round(130 * cardSizes.sideboard)}px, max-content))`,
                    gap: `${Math.round(4 * cardSizes.sideboard)}px`,
                    alignContent: 'start',
                    minHeight: '150px',
                    paddingBottom: '40px'
                  }}
                >
                  {(() => {
                    // Group instances by cardId for clean stacking (collection style)
                    const groupedCards = new Map<string, DeckCardInstance[]>();
                    sortedSideboard.forEach(instance => {
                      const cardId = instance.cardId;
                      if (!groupedCards.has(cardId)) {
                        groupedCards.set(cardId, []);
                      }
                      groupedCards.get(cardId)!.push(instance);
                    });

                    return Array.from(groupedCards.entries()).map(([cardId, instances]) => {
                      const representativeCard = instances[0];
                      const quantity = instances.length;
                      const isAnySelected = instances.some(instance => isSelected(instance.instanceId));

                      const handleStackClick = (card: any, event?: React.MouseEvent) => {
                        // If multiple instances, select the first non-selected one, or all if all selected
                        if (instances.length > 1) {
                          const unselectedInstance = instances.find(inst => !isSelected(inst.instanceId));
                          const targetInstance = unselectedInstance || instances[0];
                          handleInstanceClick(targetInstance.instanceId, targetInstance, event as React.MouseEvent);
                        } else {
                          handleInstanceClick(representativeCard.instanceId, representativeCard, event as React.MouseEvent);
                        }
                      };

                      const handleStackInstanceClick = (instanceId: string, instance: DeckCardInstance, event: React.MouseEvent) => {
                        // For stacks, use the same logic but with proper signature
                        handleStackClick(instance, event);
                      };

                      const handleStackDragStart = (cards: any[], zone: any, event: React.MouseEvent) => {
                        // When dragging a stack, drag all instances of the card
                        handleDragStart(instances as any[], zone, event);
                      };

                      return (
                        <DraggableCard
                          key={cardId}
                          card={representativeCard}
                          zone="sideboard"
                          size="normal"
                          scaleFactor={cardSizes.sideboard}
                          onClick={handleStackClick}
                          instanceId={representativeCard.instanceId}
                          isInstance={true}
                          onInstanceClick={handleStackInstanceClick}
                          onEnhancedDoubleClick={handleDoubleClick}
                          onRightClick={handleRightClick}
                          onDragStart={handleStackDragStart}
                          showQuantity={true}
                          quantity={quantity}
                          selected={isAnySelected}
                          selectable={true}
                          isDragActive={dragState.isDragging}
                          isBeingDragged={dragState.draggedCards.some(dc => 
                            instances.some(inst => 
                              'instanceId' in dc ? dc.instanceId === inst.instanceId : dc.id === inst.cardId
                            )
                          )}
                          selectedCards={getSelectedCardObjects()}
                        />
                      );
                    });
                  })()}
                  
                  {sideboard.length === 0 && (
                    <div className="empty-sideboard-message">
                      Drag cards here for your sideboard
                    </div>
                  )}
                </div>
              )}
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
      {/* Export Modals */}
      <TextExportModal
        isOpen={showTextExportModal}
        onClose={handleCloseTextExport}
        mainDeck={mainDeck}
        sideboard={sideboard}
        format={activeFilters.format}
        deckName="Untitled Deck"
      />
      
      <ScreenshotModal
        isOpen={showScreenshotModal}
        onClose={handleCloseScreenshot}
        mainDeck={mainDeck}
        sideboard={sideboard}
        deckName="Untitled Deck"
      />


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