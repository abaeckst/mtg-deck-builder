import React, { useState, useCallback, useEffect, useRef, useMemo } from 'react';
import { useLayout } from '../hooks/useLayout';
import { useSelection } from '../hooks/useSelection';
import { useResize } from '../hooks/useResize';
import { useDragAndDrop, DraggedCard, DropZone as DropZoneType } from '../hooks/useDragAndDrop';
import { useContextMenu, DeckManagementCallbacks } from '../hooks/useContextMenu';
import { DeviceCapabilities } from '../utils/deviceDetection';
import './MTGOLayout.css';
import './ResizeHandles.css';
import './ContextMenu.css';
import './FilterPanel.css';

// Card types import
import { ScryfallCard, DeckCard, DeckCardInstance, scryfallToDeckCard, scryfallToDeckInstance, 
         deckCardToDeckInstance, isBasicLand, getTotalCardQuantity, getCardQuantityInZone, 
         removeInstancesForCard } from '../types/card';

// Import components
import { useCards } from '../hooks/useCards';
import { useSorting, SortCriteria, SortDirection } from '../hooks/useSorting';
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
import FilterPanel from './FilterPanel';
// Export modal imports
import { TextExportModal } from './TextExportModal';
import { ScreenshotModal } from './ScreenshotModal';
import { getFormatDisplayName } from '../utils/deckFormatting';

interface MTGOLayoutProps {
  // Props for any data that needs to be passed down
}

// Pile view sort state - using SortCriteria from useSorting hook

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
    searchSuggestions,
    showSuggestions,
    getSearchSuggestions,
    clearSearchSuggestions,
    addToSearchHistory,
    // Progressive loading actions
    pagination,
    loadMoreResultsAction,
    resetPagination,
    // Dual sort system integration
    handleCollectionSortChange,
    // Filter integration (pass-through from useFilters)
    activeFilters,
    isFiltersCollapsed,
    updateFilter,
    clearAllFilters,
    toggleFiltersCollapsed,
    hasActiveFilters,
    updateSectionState,
    getSectionState,
    autoExpandSection
  } = useCards();
  
  // PHASE 3B-1: Card sizing system
  const { 
    sizes: cardSizes, 
    updateCollectionSize, 
    updateDeckSize, 
    updateSideboardSize 
  } = useCardSizing();
  
  // UPDATED: Initialize resize functionality with new percentage-based system
  const { handlers: resizeHandlers } = useResize({ 
    layout, 
    updatePanelDimensions,
    updateDeckAreaHeightByPixels,
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
  
  // Enhanced sorting system with dual sort integration
  const { updateSort, getSortState } = useSorting();
  
  // Integrate dual sort system with sort button handlers
  const handleSortChange = useCallback(async (area: 'collection' | 'deck' | 'sideboard', criteria: SortCriteria, direction: SortDirection) => {
    // Always update the sort state first (for UI consistency)
    updateSort(area, criteria, direction);
    
    // For collection area, trigger dual sort system
    if (area === 'collection') {
      await handleCollectionSortChange(criteria, direction);
    }
  }, [updateSort, handleCollectionSortChange]);
  
  // Get current sort states from hook
  const collectionSort = getSortState('collection');
  const deckSort = getSortState('deck');
  const sideboardSort = getSortState('sideboard');
  
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
  const getCardId = (card: ScryfallCard | DeckCard | DeckCardInstance): string => {
    if ('instanceId' in card) {
      return card.cardId; // DeckCardInstance - use cardId (original Scryfall ID)
    }
    return card.id; // ScryfallCard or DeckCard - use id
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
        const instancesToMove = mainDeck.filter(instance => instance.cardId === cardId).slice(0, quantity);
        
        if (instancesToMove.length > 0) {
          setMainDeck(prev => prev.filter(instance => !instancesToMove.includes(instance)));
          const sideboardInstances = instancesToMove.map(instance => ({ ...instance, zone: 'sideboard' as const }));
          setSideboard(prev => [...prev, ...sideboardInstances]);
        }
      });
    }, [mainDeck]),

    moveSideboardToDeck: useCallback((cards: (ScryfallCard | DeckCard | DeckCardInstance)[], quantity = 1) => {
      cards.forEach(card => {
        const cardId = getCardId(card);
        const instancesToMove = sideboard.filter(instance => instance.cardId === cardId).slice(0, quantity);
        
        if (instancesToMove.length > 0) {
          setSideboard(prev => prev.filter(instance => !instancesToMove.includes(instance)));
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
          const instanceToMove = mainDeck.find(instance => instance.cardId === cardId);
          if (instanceToMove) {
            setMainDeck(prev => prev.filter(instance => instance !== instanceToMove));
            setSideboard(prev => [...prev, { ...instanceToMove, zone: 'sideboard' }]);
          }
        } else if (from === 'sideboard' && to === 'deck') {
          const instanceToMove = sideboard.find(instance => instance.cardId === cardId);
          if (instanceToMove) {
            setSideboard(prev => prev.filter(instance => instance !== instanceToMove));
            setMainDeck(prev => [...prev, { ...instanceToMove, zone: 'deck' }]);
          }
        } else if (from === 'deck' && to === 'collection') {
          const instanceToRemove = mainDeck.find(instance => instance.cardId === cardId);
          if (instanceToRemove) {
            setMainDeck(prev => prev.filter(instance => instance !== instanceToRemove));
          }
        } else if (from === 'sideboard' && to === 'collection') {
          const instanceToRemove = sideboard.find(instance => instance.cardId === cardId);
          if (instanceToRemove) {
            setSideboard(prev => prev.filter(instance => instance !== instanceToRemove));
          }
        }
      });
      
      clearSelection();
    }, [mainDeck, sideboard, getTotalCopies, clearSelection]),

    onDragStart: useCallback((cards: DraggedCard[], from: DropZoneType) => {
      // Drag start callback
    }, []),

    onDragEnd: useCallback((cards: DraggedCard[], success: boolean) => {
      // Drag end callback
    }, [])
  };

  // Initialize enhanced drag and drop with double-click handler
  const { dragState, startDrag, setDropZone, canDropInZone, handleDoubleClick } = useDragAndDrop(dragCallbacks);
  
  // Check if device supports MTGO interface
  const canUseMTGO = DeviceCapabilities.canUseAdvancedInterface();
  
  // Enhanced search handling with comprehensive filters
  const handleSearch = useCallback((text: string) => {
    setSearchText(text);
    if (text.trim()) {
      enhancedSearch(text);
    } else if (hasActiveFilters()) {
      enhancedSearch('');
    } else {
      loadPopularCards();
    }
  }, [enhancedSearch, loadPopularCards, hasActiveFilters]);
  
  // Handle any filter change
  const handleFilterChange = useCallback((filterType: string, value: any) => {
    // Input validation for range fields
    if (filterType === 'cmc' && value && typeof value === 'object') {
      if (value.min !== null && value.max !== null && value.min > value.max) {
        alert('Invalid CMC range: Minimum cannot be greater than maximum');
        return;
      }
    }
    
    if (filterType === 'power' && value && typeof value === 'object') {
      if (value.min !== null && value.max !== null && value.min > value.max) {
        alert('Invalid Power range: Minimum cannot be greater than maximum');
        return;
      }
    }
    
    if (filterType === 'toughness' && value && typeof value === 'object') {
      if (value.min !== null && value.max !== null && value.min > value.max) {
        alert('Invalid Toughness range: Minimum cannot be greater than maximum');
        return;
      }
    }
    
    // Build the new filter state manually
    const newFilters = {
      ...activeFilters,
      [filterType]: value,
    };
    
    // Update the filter state
    updateFilter(filterType, value);
    
    // Trigger search with the new filters
    setTimeout(() => {
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

  // Simple client-side card sorting helper function
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

  // Get sorted cards for each area - SIMPLIFIED CLIENT-SIDE ONLY
  const sortedCollectionCards = useMemo(() => {
    return sortCards([...cards], collectionSort.criteria, collectionSort.direction);
  }, [cards, collectionSort.criteria, collectionSort.direction, sortCards]);

  const sortedMainDeck = useMemo((): DeckCardInstance[] => {
    return layout.viewModes.deck === 'pile' ? mainDeck : sortCards(mainDeck as any, deckSort.criteria, deckSort.direction) as DeckCardInstance[];
  }, [mainDeck, deckSort.criteria, deckSort.direction, layout.viewModes.deck, sortCards]);

  const sortedSideboard = useMemo((): DeckCardInstance[] => {
    return layout.viewModes.sideboard === 'pile' ? sideboard : sortCards(sideboard as any, sideboardSort.criteria, sideboardSort.direction) as DeckCardInstance[];
  }, [sideboard, sideboardSort.criteria, sideboardSort.direction, layout.viewModes.sideboard, sortCards]);

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
      
      {/* Phase 4B: Enhanced Filter Panel */}
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
      {!isFiltersCollapsed && (
        <div 
          className="resize-handle resize-handle-right"
          onMouseDown={resizeHandlers.onFilterPanelResize}
          title="Drag to resize filter panel"
          style={{
            position: 'absolute',
            top: 0,
            right: -3,
            width: 6,
            height: '100%',
            cursor: 'ew-resize',
            background: 'linear-gradient(90deg, transparent 0%, #555555 50%, transparent 100%)',
            zIndex: 1001,
            opacity: 0.7,
            transition: 'opacity 0.2s ease'
          }}
          onMouseEnter={(e) => e.currentTarget.style.opacity = '1'}
          onMouseLeave={(e) => e.currentTarget.style.opacity = '0.7'}
        />
      )}
      
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
            <h3>Collection ({cards.length.toLocaleString()} {pagination.totalCards > pagination.loadedCards && (<span className="pagination-info">of {pagination.totalCards.toLocaleString()}</span>)} cards)</h3>

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
                      className={collectionSort.criteria === 'name' ? 'active' : ''}
                      onClick={() => { 
                        if (collectionSort.criteria === 'name') {
                          const newDirection = collectionSort.direction === 'asc' ? 'desc' : 'asc';
                          handleSortChange('collection', 'name', newDirection);
                        } else {
                          handleSortChange('collection', 'name', 'asc');
                        }
                        setShowCollectionSortMenu(false); 
                      }}
                    >
                      Name {collectionSort.criteria === 'name' ? (collectionSort.direction === 'asc' ? '↑' : '↓') : ''}
                    </button>
                    <button 
                      className={collectionSort.criteria === 'mana' ? 'active' : ''}
                      onClick={() => { 
                        if (collectionSort.criteria === 'mana') {
                          handleSortChange('collection', 'mana', collectionSort.direction === 'asc' ? 'desc' : 'asc');
                        } else {
                          handleSortChange('collection', 'mana', 'asc');
                        }
                        setShowCollectionSortMenu(false); 
                      }}
                    >
                      Mana Value {collectionSort.criteria === 'mana' ? (collectionSort.direction === 'asc' ? '↑' : '↓') : ''}
                    </button>
                    <button 
                      className={collectionSort.criteria === 'color' ? 'active' : ''}
                      onClick={() => { 
                        if (collectionSort.criteria === 'color') {
                          handleSortChange('collection', 'color', collectionSort.direction === 'asc' ? 'desc' : 'asc');
                        } else {
                          handleSortChange('collection', 'color', 'asc');
                        }
                        setShowCollectionSortMenu(false); 
                      }}
                    >
                      Color {collectionSort.criteria === 'color' ? (collectionSort.direction === 'asc' ? '↑' : '↓') : ''}
                    </button>
                    <button 
                      className={collectionSort.criteria === 'rarity' ? 'active' : ''}
                      onClick={() => { 
                        if (collectionSort.criteria === 'rarity') {
                          handleSortChange('collection', 'rarity', collectionSort.direction === 'asc' ? 'desc' : 'asc');
                        } else {
                          handleSortChange('collection', 'rarity', 'asc');
                        }
                        setShowCollectionSortMenu(false); 
                      }}
                    >
                      Rarity {collectionSort.criteria === 'rarity' ? (collectionSort.direction === 'asc' ? '↑' : '↓') : ''}
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
              <>
                <ListView
                  cards={sortedCollectionCards}
                  area="collection"
                  scaleFactor={cardSizes.collection}
                  sortCriteria={collectionSort.criteria}
                  sortDirection={collectionSort.direction}
                  onSortChange={(criteria, direction) => {
                    handleSortChange('collection', criteria, direction);
                  }}
                  onClick={handleCardClick}
                  onDoubleClick={handleAddToDeck}
                  onRightClick={handleRightClick}
                  onDragStart={handleDragStart}
                  isSelected={isSelected}
                  selectedCards={getSelectedCardObjects()}
                  isDragActive={dragState.isDragging}
                />
                
                {/* Load More Results integrated into List View */}
                {!loading && !error && pagination.hasMore && (
                  <div className="load-more-section-integrated">
                    {pagination.isLoadingMore ? (
                      <div className="loading-progress">
                        <div className="progress-bar">
                          <div 
                            className="progress-fill" 
                            style={{
                              width: `${(pagination.loadedCards / pagination.totalCards) * 100}%`
                            }}
                          />
                        </div>
                        <span className="progress-text">
                          Loading... ({pagination.loadedCards.toLocaleString()}/{pagination.totalCards.toLocaleString()} cards)
                        </span>
                      </div>
                    ) : (
                      <button 
                        className="load-more-results-btn"
                        onClick={loadMoreResultsAction}
                        disabled={loading}
                        title={`Load 175 more cards (${pagination.totalCards - pagination.loadedCards} remaining)`}
                      >
                        Load More Results ({(pagination.totalCards - pagination.loadedCards).toLocaleString()} more cards)
                      </button>
                    )}
                  </div>
                )}
              </>
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
                
                {/* Load More Results integrated into Card Grid */}
                {!loading && !error && pagination.hasMore && (
                  <div className="load-more-section-integrated" style={{
                    gridColumn: '1 / -1',
                    display: 'flex',
                    justifyContent: 'center',
                    padding: '20px',
                    marginTop: '10px'
                  }}>
                    {pagination.isLoadingMore ? (
                      <div className="loading-progress">
                        <div className="progress-bar">
                          <div 
                            className="progress-fill" 
                            style={{
                              width: `${(pagination.loadedCards / pagination.totalCards) * 100}%`
                            }}
                          />
                        </div>
                        <span className="progress-text">
                          Loading... ({pagination.loadedCards.toLocaleString()}/{pagination.totalCards.toLocaleString()} cards)
                        </span>
                      </div>
                    ) : (
                      <button 
                        className="load-more-results-btn"
                        onClick={loadMoreResultsAction}
                        disabled={loading}
                        title={`Load 175 more cards (${pagination.totalCards - pagination.loadedCards} remaining)`}
                      >
                        Load More Results ({(pagination.totalCards - pagination.loadedCards).toLocaleString()} more cards)
                      </button>
                    )}
                  </div>
                )}
              </div>
            )
          )}
          
          {/* Resize Handle */}
          <div 
            className="resize-handle resize-handle-bottom"
            onMouseDown={resizeHandlers.onDeckAreaResize}
            title="Drag to resize collection area"
            style={{
              position: 'absolute',
              left: 0,
              bottom: -3,
              width: '100%',
              height: 6,
              cursor: 'ns-resize',
              background: 'linear-gradient(0deg, transparent 0%, #555555 50%, transparent 100%)',
              zIndex: 1001,
              opacity: 0.7,
              transition: 'opacity 0.2s ease'
            }}
            onMouseEnter={(e) => e.currentTarget.style.opacity = '1'}
            onMouseLeave={(e) => e.currentTarget.style.opacity = '0.7'}
          />
        </DropZoneComponent>
        
        {/* Bottom Area */}
        <div className="mtgo-bottom-area">
          {/* Vertical Resize Handle */}
          <div 
            className="resize-handle resize-handle-vertical"
            onMouseDown={resizeHandlers.onVerticalResize}
            title="Drag to resize between collection and deck areas"
            style={{
              position: 'absolute',
              top: -3,
              left: 0,
              width: '100%',
              height: 6,
              cursor: 'ns-resize',
              background: 'linear-gradient(0deg, transparent 0%, #555555 50%, transparent 100%)',
              zIndex: 1001,
              opacity: 0.7,
              transition: 'opacity 0.2s ease'
            }}
            onMouseEnter={(e) => e.currentTarget.style.opacity = '1'}
            onMouseLeave={(e) => e.currentTarget.style.opacity = '0.7'}
          />
          
          {/* Main Deck Area */}
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
                        className={deckSort.criteria === 'mana' ? 'active' : ''}
                        onClick={() => { 
                          if (layout.viewModes.deck === 'card' && deckSort.criteria === 'mana') {
                            updateSort('deck', 'mana', deckSort.direction === 'asc' ? 'desc' : 'asc');
                          } else {
                            updateSort('deck', 'mana', 'asc');
                          }
                          setShowDeckSortMenu(false); 
                        }}
                      >
                        Mana Value {deckSort.criteria === 'mana' && layout.viewModes.deck === 'card' ? (deckSort.direction === 'asc' ? '↑' : '↓') : ''}
                      </button>
                      <button 
                        className={deckSort.criteria === 'color' ? 'active' : ''}
                        onClick={() => { 
                          if (layout.viewModes.deck === 'card' && deckSort.criteria === 'color') {
                            updateSort('deck', 'color', deckSort.direction === 'asc' ? 'desc' : 'asc');
                          } else {
                            updateSort('deck', 'color', 'asc');
                          }
                          setShowDeckSortMenu(false); 
                        }}
                      >
                        Color {deckSort.criteria === 'color' && layout.viewModes.deck === 'card' ? (deckSort.direction === 'asc' ? '↑' : '↓') : ''}
                      </button>
                      <button 
                        className={deckSort.criteria === 'rarity' ? 'active' : ''}
                        onClick={() => { 
                          if (layout.viewModes.deck === 'card' && deckSort.criteria === 'rarity') {
                            updateSort('deck', 'rarity', deckSort.direction === 'asc' ? 'desc' : 'asc');
                          } else {
                            updateSort('deck', 'rarity', 'asc');
                          }
                          setShowDeckSortMenu(false); 
                        }}
                      >
                        Rarity {deckSort.criteria === 'rarity' && layout.viewModes.deck === 'card' ? (deckSort.direction === 'asc' ? '↑' : '↓') : ''}
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
                </button>
                <button onClick={handleTextExport} title="Export deck as text for MTGO">
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
                  forcedSortCriteria={deckSort.criteria === 'name' || deckSort.criteria === 'type' ? 'mana' : deckSort.criteria as any}
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
                  sortCriteria={deckSort.criteria}
                  sortDirection={deckSort.direction}
                  onSortChange={(criteria, direction) => {
                    if (criteria === 'name' || criteria === 'mana' || criteria === 'color' || criteria === 'rarity') {
                      updateSort('deck', criteria, direction);
                    }
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
                      setMainDeck(prev => prev.filter(instance => instance.cardId !== cardId));
                    } else {
                      const currentQuantity = getDeckQuantity(cardId);
                      const diff = newQuantity - currentQuantity;
                      
                      if (diff > 0) {
                        const cardData = cards.find(c => c.id === cardId);
                        if (cardData) {
                          const newInstances: DeckCardInstance[] = [];
                          for (let i = 0; i < diff; i++) {
                            newInstances.push(createDeckInstance(cardData, 'deck'));
                          }
                          setMainDeck(prev => [...prev, ...newInstances]);
                        }
                      } else if (diff < 0) {
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
                    // Group instances by cardId for clean stacking
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
                        if (instances.length > 1) {
                          const unselectedInstance = instances.find(inst => !isSelected(inst.instanceId));
                          const targetInstance = unselectedInstance || instances[0];
                          handleInstanceClick(targetInstance.instanceId, targetInstance, event as React.MouseEvent);
                        } else {
                          handleInstanceClick(representativeCard.instanceId, representativeCard, event as React.MouseEvent);
                        }
                      };

                      const handleStackInstanceClick = (instanceId: string, instance: DeckCardInstance, event: React.MouseEvent) => {
                        handleStackClick(instance, event);
                      };

                      const handleStackDragStart = (cards: any[], zone: any, event: React.MouseEvent) => {
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
                  
                  {sideboard.length === 0 && (
                    <div className="empty-sideboard-message">
                      Drag cards here for your sideboard
                    </div>
                  )}
                </div>
              )}
            </div>
            
          </DropZoneComponent>
          
          {/* Sideboard Area */}
          <DropZoneComponent
            zone="sideboard"
            onDragEnter={handleDragEnter}
            onDragLeave={handleDragLeave}
            canDrop={canDropInZone('sideboard', dragState.draggedCards)}
            isDragActive={dragState.isDragging}
            className="mtgo-sideboard-panel"
            style={{ width: `${layout.panels.sideboardWidth}px` }}
          >
            {/* Horizontal Resize Handle */}
            <div 
              className="resize-handle resize-handle-left"
              onMouseDown={resizeHandlers.onSideboardResize}
              title="Drag to resize sideboard"
              style={{
                position: 'absolute',
                top: 0,
                left: -3,
                width: 6,
                height: '100%',
                cursor: 'ew-resize',
                background: 'linear-gradient(90deg, transparent 0%, #555555 50%, transparent 100%)',
                zIndex: 1001,
                opacity: 0.7,
                transition: 'opacity 0.2s ease'
              }}
              onMouseEnter={(e) => e.currentTarget.style.opacity = '1'}
              onMouseLeave={(e) => e.currentTarget.style.opacity = '0.7'}
            />
            <div className="panel-header">
              <h3>Sideboard ({sideboard.length} cards)</h3>
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
                        className={sideboardSort.criteria === 'mana' ? 'active' : ''}
                        onClick={() => { 
                          if (layout.viewModes.sideboard === 'card' && sideboardSort.criteria === 'mana') {
                            updateSort('sideboard', 'mana', sideboardSort.direction === 'asc' ? 'desc' : 'asc');
                          } else {
                            updateSort('sideboard', 'mana', 'asc');
                          }
                          setShowSideboardSortMenu(false); 
                        }}
                      >
                        Mana Value {sideboardSort.criteria === 'mana' && layout.viewModes.sideboard === 'card' ? (sideboardSort.direction === 'asc' ? '↑' : '↓') : ''}
                      </button>
                      <button 
                        className={sideboardSort.criteria === 'color' ? 'active' : ''}
                        onClick={() => { 
                          if (layout.viewModes.sideboard === 'card' && sideboardSort.criteria === 'color') {
                            updateSort('sideboard', 'color', sideboardSort.direction === 'asc' ? 'desc' : 'asc');
                          } else {
                            updateSort('sideboard', 'color', 'asc');
                          }
                          setShowSideboardSortMenu(false); 
                        }}
                      >
                        Color {sideboardSort.criteria === 'color' && layout.viewModes.sideboard === 'card' ? (sideboardSort.direction === 'asc' ? '↑' : '↓') : ''}
                      </button>
                      <button 
                        className={sideboardSort.criteria === 'rarity' ? 'active' : ''}
                        onClick={() => { 
                          if (layout.viewModes.sideboard === 'card' && sideboardSort.criteria === 'rarity') {
                            updateSort('sideboard', 'rarity', sideboardSort.direction === 'asc' ? 'desc' : 'asc');
                          } else {
                            updateSort('sideboard', 'rarity', 'asc');
                          }
                          setShowSideboardSortMenu(false); 
                        }}
                      >
                        Rarity {sideboardSort.criteria === 'rarity' && layout.viewModes.sideboard === 'card' ? (sideboardSort.direction === 'asc' ? '↑' : '↓') : ''}
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
                  forcedSortCriteria={sideboardSort.criteria === 'name' || sideboardSort.criteria === 'type' ? 'mana' : sideboardSort.criteria as any}
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
                  sortCriteria={sideboardSort.criteria}
                  sortDirection={sideboardSort.direction}
                  onSortChange={(criteria, direction) => {
                    if (criteria === 'name' || criteria === 'mana' || criteria === 'color' || criteria === 'rarity') {
                      updateSort('sideboard', criteria, direction);
                    }
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
                      setSideboard(prev => prev.filter(instance => instance.cardId !== cardId));
                    } else {
                      const currentQuantity = getSideboardQuantity(cardId);
                      const diff = newQuantity - currentQuantity;
                      
                      if (diff > 0) {
                        const cardData = cards.find(c => c.id === cardId);
                        if (cardData) {
                          const newInstances: DeckCardInstance[] = [];
                          for (let i = 0; i < diff; i++) {
                            newInstances.push(createDeckInstance(cardData, 'sideboard'));
                          }
                          setSideboard(prev => [...prev, ...newInstances]);
                        }
                      } else if (diff < 0) {
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
                    // Group instances by cardId for clean stacking
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
                        if (instances.length > 1) {
                          const unselectedInstance = instances.find(inst => !isSelected(inst.instanceId));
                          const targetInstance = unselectedInstance || instances[0];
                          handleInstanceClick(targetInstance.instanceId, targetInstance, event as React.MouseEvent);
                        } else {
                          handleInstanceClick(representativeCard.instanceId, representativeCard, event as React.MouseEvent);
                        }
                      };

                      const handleStackInstanceClick = (instanceId: string, instance: DeckCardInstance, event: React.MouseEvent) => {
                        handleStackClick(instance, event);
                      };

                      const handleStackDragStart = (cards: any[], zone: any, event: React.MouseEvent) => {
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