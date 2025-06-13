import React, { useState, useCallback } from 'react';
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
         removeInstancesForCard, getCardId } from '../types/card';

// Import components
import { useCards } from '../hooks/useCards';
import { useSorting, SortCriteria, SortDirection } from '../hooks/useSorting';
import { useCardSizing } from '../hooks/useCardSizing';
import DragPreview from './DragPreview';
import ContextMenu from './ContextMenu';
import FilterPanel from './FilterPanel';
import CollectionArea from './CollectionArea';
import DeckArea from './DeckArea';
import SideboardArea from './SideboardArea';
// Export modal imports
import { TextExportModal } from './TextExportModal';
import { ScreenshotModal } from './ScreenshotModal';

interface MTGOLayoutProps {
  // Props for any data that needs to be passed down
}

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
  // UNIFIED STATE MANAGEMENT: deck and sideboard share view mode and card size
    const {
    layout,
    updatePanelDimensions,
    updateDeckAreaHeightByPixels,
    updatePreviewPane,
    updateViewMode,
    updateCardSize,
    updateDeckSideboardViewMode, // NEW: Unified deck/sideboard view mode
    updateDeckSideboardCardSize, // NEW: Unified deck/sideboard card size
    resetLayout,
    togglePreviewPane,
    constraints,
    getCalculatedHeights,
  } = useLayout();
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
  
  // Card sizing system
  const { 
    sizes: cardSizes, 
    updateCollectionSize, 
    updateDeckSize, 
    updateSideboardSize 
  } = useCardSizing();
  
  // Initialize resize functionality
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

  // Clear sideboard functionality
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
  
  // Enhanced drag and drop callbacks
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

  // Deck quantity change handlers
  const handleDeckQuantityChange = useCallback((cardId: string, newQuantity: number) => {
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
  }, [cards, getDeckQuantity]);

  const handleSideboardQuantityChange = useCallback((cardId: string, newQuantity: number) => {
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
  }, [cards, getSideboardQuantity]);

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
      
      {/* Enhanced Filter Panel */}
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
        hasActiveFilters={hasActiveFilters}
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
        {/* Collection Area */}
        <CollectionArea
          cards={cards}
          loading={loading}
          error={error}
          pagination={pagination}
          loadMoreResultsAction={loadMoreResultsAction}
          sortState={collectionSort}
          onSortChange={(criteria, direction) => handleSortChange('collection', criteria, direction)}
          viewMode={layout.viewModes.collection}
          onViewModeChange={(mode) => updateViewMode('collection', mode)}
          cardSize={cardSizes.collection}
          onCardSizeChange={updateCollectionSize}
          onCardClick={handleCardClick}
          onCardDoubleClick={handleAddToDeck}
          onCardRightClick={handleRightClick}
          onDragStart={handleDragStart}
          onDragEnter={handleDragEnter}
          onDragLeave={handleDragLeave}
          canDropInZone={canDropInZone}
          dragState={dragState}
          isSelected={isSelected}
          getSelectedCardObjects={getSelectedCardObjects}
          clearSelection={clearSelection}
          getTotalCopies={getTotalCopies}
          sortCards={sortCards}
        />
        
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
          <DeckArea
            mainDeck={mainDeck}
            cards={cards}
            sortState={deckSort}
            onSortChange={(criteria, direction) => updateSort('deck', criteria, direction)}
            viewMode={layout.viewModes.deckSideboard}
            onViewModeChange={updateDeckSideboardViewMode}
            cardSize={layout.cardSizes.deckSideboard}
            onCardSizeChange={updateDeckSideboardCardSize}
            onCardClick={handleCardClick}
            onInstanceClick={handleInstanceClick}
            onCardDoubleClick={handleAddToDeck}
            onEnhancedDoubleClick={handleDoubleClick}
            onCardRightClick={handleRightClick}
            onDragStart={handleDragStart}
            onDragEnter={handleDragEnter}
            onDragLeave={handleDragLeave}
            canDropInZone={canDropInZone}
            dragState={dragState}
            isSelected={isSelected}
            getSelectedCardObjects={getSelectedCardObjects}
            clearSelection={clearSelection}
            onTextExport={handleTextExport}
            onScreenshot={handleScreenshot}
            onClearDeck={handleClearDeck}
            getDeckQuantity={getDeckQuantity}
            onQuantityChange={handleDeckQuantityChange}
            sortCards={sortCards}
            createDeckInstance={createDeckInstance}
          />
          
          {/* Sideboard Area */}
          <SideboardArea
            sideboard={sideboard}
            sideboardWidth={layout.panels.sideboardWidth}
            sortState={sideboardSort}
            onSortChange={(criteria, direction) => updateSort('sideboard', criteria, direction)}
            cardSize={layout.cardSizes.deckSideboard}
            viewMode={layout.viewModes.deckSideboard}
            onViewModeChange={updateDeckSideboardViewMode}            onCardSizeChange={updateSideboardSize}
            onCardClick={handleCardClick}
            onInstanceClick={handleInstanceClick}
            onCardDoubleClick={handleAddToDeck}
            onEnhancedDoubleClick={handleDoubleClick}
            onCardRightClick={handleRightClick}
            onDragStart={handleDragStart}
            onDragEnter={handleDragEnter}
            onDragLeave={handleDragLeave}
            canDropInZone={canDropInZone}
            dragState={dragState}
            isSelected={isSelected}
            getSelectedCardObjects={getSelectedCardObjects}
            clearSelection={clearSelection}
            onClearSideboard={handleClearSideboard}
            getSideboardQuantity={getSideboardQuantity}
            onQuantityChange={handleSideboardQuantityChange}
            onSideboardResize={resizeHandlers.onSideboardResize}
            sortCards={sortCards}
          />
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