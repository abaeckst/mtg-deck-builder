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
    loadPopularCards, 
    loadRandomCard 
  } = useCards();
  
  // UPDATED: Initialize resize functionality with new percentage-based system
  const { handlers: resizeHandlers } = useResize({ 
    layout, 
    updatePanelDimensions,
    updateDeckAreaHeightByPixels, // NEW: Required for percentage-based system
    constraints 
  });
  
  // Local state for search and filters
  const [searchText, setSearchText] = useState('');
  const [selectedFormat, setSelectedFormat] = useState('');
  const [selectedColors, setSelectedColors] = useState<string[]>([]);
  
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
  
  // Search handling
  const handleSearch = (text: string) => {
    setSearchText(text);
    if (text.trim()) {
      searchForCards(text);
    } else {
      loadPopularCards();
    }
  };
  
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
      
      {/* Filter Panel - Left Side */}
      <div 
        className="mtgo-filter-panel"
        style={{ width: layout.panels.filterPanelWidth }}
      >
        <div className="panel-header">
          <h3>Filters</h3>
        </div>
        
        <div className="filter-content">
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
          
          <div className="filter-group">
            <label>Format</label>
            <select 
              value={selectedFormat} 
              onChange={(e) => setSelectedFormat(e.target.value)}
              className="format-select"
            >
              <option value="">All Formats</option>
              <option value="standard">Standard</option>
              <option value="pioneer">Pioneer</option>
              <option value="modern">Modern</option>
              <option value="legacy">Legacy</option>
              <option value="vintage">Vintage</option>
            </select>
          </div>
          
          <div className="filter-group">
            <label>Colors</label>
            <div className="color-filter-grid">
              {['W', 'U', 'B', 'R', 'G'].map((color: string) => (
                <button
                  key={color}
                  className={`color-button color-${color.toLowerCase()} ${
                    selectedColors.includes(color) ? 'selected' : ''
                  }`}
                  onClick={() => {
                    setSelectedColors((prev: string[]) => 
                      prev.includes(color) 
                        ? prev.filter((c: string) => c !== color)
                        : [...prev, color]
                    );
                  }}
                >
                  {color}
                </button>
              ))}
            </div>
          </div>
          
          <div className="filter-group">
            <label>Quick Load</label>
            <div className="quick-actions">
              <button onClick={loadPopularCards}>Popular Cards</button>
              <button onClick={loadRandomCard}>Random Card</button>
              <button onClick={clearSelection}>Clear Selection</button>
            </div>
          </div>
        </div>
        
        {/* PHASE 3A: Enhanced Resize Handle with larger hit zone */}
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
              <span>View: </span>
              <button className="active">Card</button>
              <button>List</button>
            </div>
          </div>
          
          <div className="collection-grid">
            {loading && <div className="loading-message">Loading cards...</div>}
            {error && <div className="error-message">Error: {error}</div>}
            {cards.map(card => (
              <DraggableCard
                key={card.id}
                card={card}
                zone="collection"
                size="normal"
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
                <button>Save Deck</button>
                <button onClick={handleClearDeck} title="Clear all cards from deck">
                  Clear Deck
                </button>
              </div>
            </div>
            
            <div className="deck-content">
              <div className="deck-grid">
                {mainDeck.map((deckCard: any) => (
                  <DraggableCard
                    key={deckCard.id}
                    card={deckCard}
                    zone="deck"
                    size="small"
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
                <button onClick={handleClearSideboard} title="Clear all cards from sideboard">
                  Clear
                </button>
              </div>
            </div>
            
            <div className="sideboard-content">
              <div className="sideboard-grid">
                {sideboard.map((sideCard: any) => (
                  <DraggableCard
                    key={sideCard.id}
                    card={sideCard}
                    zone="sideboard"
                    size="small"
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