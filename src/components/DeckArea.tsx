import React, { useState, useCallback, useRef, useEffect } from 'react';
import { ScryfallCard, DeckCard, DeckCardInstance, CardSizeMode, getSizeConfig } from '../types/card';
import { SortCriteria, SortDirection } from '../hooks/useSorting';
import { DropZone as DropZoneType, DraggedCard } from '../hooks/useDragAndDrop';
import DraggableCard from './DraggableCard';
import DropZoneComponent from './DropZone';
import ListView from './ListView';
import PileView from './PileView';
import ViewModeDropdown from './ViewModeDropdown';
import CardSizeButtons from './CardSizeButtons';
import './FilterPanel.css'; // For card size button styles

interface DeckAreaProps {
  mainDeck: DeckCardInstance[];
  cards: ScryfallCard[]; // For creating new instances
  
  // Sorting
  sortState: {
    criteria: SortCriteria;
    direction: SortDirection;
  };
  onSortChange: (criteria: SortCriteria, direction: SortDirection) => void;
  
  // View and sizing - UNIFIED CONTROLS
  viewMode: 'card' | 'pile' | 'list';
  onViewModeChange: (mode: 'card' | 'pile' | 'list') => void; // This will affect both deck and sideboard
  cardSizeMode: CardSizeMode;
  onCardSizeChange: (mode: CardSizeMode) => void; // This will affect both deck and sideboard
  
  // Card interactions
  onCardClick: (card: ScryfallCard | DeckCard | DeckCardInstance, event?: React.MouseEvent) => void;
  onInstanceClick: (instanceId: string, instance: DeckCardInstance, event: React.MouseEvent) => void;
  onEnhancedDoubleClick: (card: any, zone: DropZoneType, event: React.MouseEvent) => void;
  onCardRightClick: (card: any, zone: DropZoneType, event: React.MouseEvent) => void;
  onDragStart: (cards: DraggedCard[], zone: DropZoneType, event: React.MouseEvent) => void;
  
  // Drag and drop
  onDragEnter: (zone: DropZoneType, canDrop: boolean) => void;
  onDragLeave: () => void;
  canDropInZone: (zone: DropZoneType, cards: DraggedCard[]) => boolean;
  dragState: {
    isDragging: boolean;
    draggedCards: DraggedCard[];
  };
  
  // Selection
  isSelected: (cardId: string) => boolean;
  getSelectedCardObjects: () => any[];
  clearSelection: () => void;
  
  // Deck management
  onTextExport: () => void;
  onScreenshot: () => void;
  onClearDeck: () => void;
  getDeckQuantity: (cardId: string) => number;
  onQuantityChange: (cardId: string, newQuantity: number) => void;
  
  // Utility
  sortCards: (cards: (ScryfallCard | DeckCard | DeckCardInstance)[], criteria: SortCriteria, direction: 'asc' | 'desc') => (ScryfallCard | DeckCard | DeckCardInstance)[];
  createDeckInstance: (card: ScryfallCard | DeckCard | DeckCardInstance, zone: 'deck' | 'sideboard') => DeckCardInstance;
}

const DeckArea: React.FC<DeckAreaProps> = ({
  mainDeck,
  cards,
  sortState,
  onSortChange,
  viewMode,
  onViewModeChange,
  cardSizeMode,
  onCardSizeChange,
  onCardClick,
  onInstanceClick,
  onEnhancedDoubleClick,
  onCardRightClick,
  onDragStart,
  onDragEnter,
  onDragLeave,
  canDropInZone,
  dragState,
  isSelected,
  getSelectedCardObjects,
  clearSelection,
  onTextExport,
  onScreenshot,
  onClearDeck,
  getDeckQuantity,
  onQuantityChange,
  sortCards,
  createDeckInstance
}) => {
  // Sort menu state
  const [showSortMenu, setShowSortMenu] = useState(false);
  const sortRef = useRef<HTMLDivElement>(null);

  const [showOverflowMenu, setShowOverflowMenu] = useState(false);
  
  // Debug logging for overflow menu state
  useEffect(() => {
    console.log('🔧 Overflow menu state changed:', showOverflowMenu);
  }, [showOverflowMenu]);
  const [hiddenControls, setHiddenControls] = useState<string[]>([]);
  const headerRef = useRef<HTMLDivElement>(null);
  const controlsRef = useRef<HTMLDivElement>(null);
  const overflowRef = useRef<HTMLDivElement>(null);

  // Z-INDEX NUCLEAR OPTION: Hide resize handles when overflow menu is open
  useEffect(() => {
    const hideResizeHandles = () => {
      const resizeHandles = document.querySelectorAll('.resize-handle, .resize-handle-left, .resize-handle-right, .resize-handle-bottom');
      resizeHandles.forEach(handle => {
        if (showOverflowMenu) {
          (handle as HTMLElement).style.display = 'none';
        } else {
          (handle as HTMLElement).style.display = '';
        }
      });
    };
    
    hideResizeHandles();
    
    // Also hide when sort menu is open for good measure
    if (showSortMenu) {
      const resizeHandles = document.querySelectorAll('.resize-handle, .resize-handle-left, .resize-handle-right, .resize-handle-bottom');
      resizeHandles.forEach(handle => {
        (handle as HTMLElement).style.display = 'none';
      });
    }
    
    return () => {
      // Cleanup: restore resize handles when component unmounts
      const resizeHandles = document.querySelectorAll('.resize-handle, .resize-handle-left, .resize-handle-right, .resize-handle-bottom');
      resizeHandles.forEach(handle => {
        (handle as HTMLElement).style.display = '';
      });
    };
  }, [showOverflowMenu, showSortMenu]);

  // Click-outside effect for sort menu and overflow menu - FIXED TIMING
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      console.log('🔧 Click outside detected');
      
      if (sortRef.current && !sortRef.current.contains(event.target as Node)) {
        console.log('🔧 Closing sort menu');
        setShowSortMenu(false);
      }
      
      if (overflowRef.current && !overflowRef.current.contains(event.target as Node)) {
        console.log('🔧 Closing overflow menu');  
        setShowOverflowMenu(false);
      }
    };

    if (showSortMenu || showOverflowMenu) {
      // CRITICAL FIX: Add delay to prevent immediate closure from same click
      const timeoutId = setTimeout(() => {
        document.addEventListener('mousedown', handleClickOutside);
      }, 10); // Small delay to let the menu render
      
      return () => {
        clearTimeout(timeoutId);
        document.removeEventListener('mousedown', handleClickOutside);
      };
    }
  }, [showSortMenu, showOverflowMenu]);

  // Responsive layout detection
  useEffect(() => {
    const checkOverflow = () => {
      if (!headerRef.current || !controlsRef.current) return;

      const headerWidth = headerRef.current.offsetWidth;
      const titleSection = headerRef.current.querySelector('.title-section') as HTMLElement;
      const titleWidth = titleSection ? titleSection.offsetWidth : 200;
      
      // Available space for controls (minus title and padding)
      const availableWidth = headerWidth - titleWidth - 80; // 80px buffer for spacing

      // Control priorities (higher priority = hide later)
      const controls = [
        { id: 'actions', priority: 1, minWidth: 180 }, // Export, Screenshot, Clear
        { id: 'size', priority: 2, minWidth: 120 },    // Size slider
        { id: 'sort', priority: 3, minWidth: 80 },     // Sort dropdown  
        { id: 'view', priority: 4, minWidth: 100 },    // View dropdown
      ];

      let totalWidth = 0;
      const toHide: string[] = [];

      // Calculate total width needed
      controls.forEach(control => {
        totalWidth += control.minWidth;
      });

      // If total width exceeds available space, hide lower priority controls
      if (totalWidth > availableWidth) {
        let remainingWidth = availableWidth - 40; // Reserve space for overflow menu
        
        // Sort by priority (hide lower priority first)
        const sortedControls = [...controls].sort((a, b) => a.priority - b.priority);
        
        for (const control of sortedControls) {
          if (remainingWidth < control.minWidth) {
            toHide.push(control.id);
          } else {
            remainingWidth -= control.minWidth;
          }
        }
      }

      setHiddenControls(toHide);
    };

    // Initial check
    checkOverflow();

    // Check on resize
    const resizeObserver = new ResizeObserver(checkOverflow);
    if (headerRef.current) {
      resizeObserver.observe(headerRef.current);
    }

    window.addEventListener('resize', checkOverflow);

    return () => {
      resizeObserver.disconnect();
      window.removeEventListener('resize', checkOverflow);
    };
  }, []);

  // Sort button handlers
  const handleSortButtonClick = useCallback((criteria: SortCriteria) => {
    if (viewMode === 'card' && sortState.criteria === criteria) {
      onSortChange(criteria, sortState.direction === 'asc' ? 'desc' : 'asc');
    } else {
      onSortChange(criteria, 'asc');
    }
    setShowSortMenu(false);
  }, [viewMode, sortState.criteria, sortState.direction, onSortChange]);

  // Get sorted cards
  const sortedMainDeck = viewMode === 'pile' ? mainDeck : sortCards(mainDeck as any, sortState.criteria, sortState.direction) as DeckCardInstance[];

  // Helper to check if control should be visible
  const isControlVisible = (controlId: string) => !hiddenControls.includes(controlId);

  // Render control in overflow menu
  const renderOverflowControl = (controlId: string, children: React.ReactNode) => {
    if (!hiddenControls.includes(controlId)) return null;
    
    return (
      <div className="overflow-menu-item" style={{
        padding: '6px 12px',
        borderBottom: '1px solid #555555',
        display: 'flex',
        alignItems: 'center',
        gap: '8px'
      }}>
        {children}
      </div>
    );
  };

  return (
    <DropZoneComponent
      zone="deck"
      onDragEnter={onDragEnter}
      onDragLeave={onDragLeave}
      canDrop={canDropInZone('deck', dragState.draggedCards)}
      isDragActive={dragState.isDragging}
      className="mtgo-deck-area"
    >
      {/* MTGO-Style Enhanced Header with Responsive Controls */}
      <div 
        ref={headerRef}
        className="mtgo-header" 
        style={{
          background: 'linear-gradient(180deg, #2a2a2a 0%, #1a1a1a 100%)',
          border: '1px solid #444',
          borderTop: '1px solid #666',
          boxShadow: '0 2px 4px rgba(0,0,0,0.3)',
          padding: '6px 12px',
          color: '#ffffff',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          gap: '12px',
          fontSize: '13px',
          position: 'relative',
          minHeight: '32px'
        }}
      >
        {/* Title Section with Text Overflow Handling */}
        <div className="title-section" style={{ 
          display: 'flex', 
          alignItems: 'center', 
          gap: '8px',
          minWidth: '150px',
          maxWidth: '300px'
        }}>
          <span style={{
            fontSize: '15px',
            fontWeight: '600',
            color: '#ffffff',
            textShadow: '0 1px 2px rgba(0,0,0,0.3)',
            whiteSpace: 'nowrap',
            overflow: 'hidden',
            textOverflow: 'ellipsis'
          }}>
            Main Deck
          </span>
          <span style={{
            color: '#cccccc',
            fontSize: '13px',
            whiteSpace: 'nowrap'
          }}>
            ({mainDeck.length} cards)
          </span>
        </div>
        
        {/* Enhanced Controls Section with Responsive Layout */}
        <div 
          ref={controlsRef}
          className="deck-controls-responsive" 
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: '10px',
            fontSize: '12px',
            flex: 1,
            justifyContent: 'flex-end',
            minWidth: 0 // Allow shrinking
          }}
        >
          {/* Group 1: View & Sort - Enhanced Grouping */}
          {(isControlVisible('view') || isControlVisible('sort')) && (
            <div className="control-group-1" style={{ 
              display: 'flex', 
              alignItems: 'center', 
              gap: '6px',
              paddingRight: '12px',
              borderRight: '1px solid #555555'
            }}>
              {isControlVisible('view') && (
                <>
                  <span style={{ 
                    color: '#cccccc', 
                    fontSize: '12px',
                    fontWeight: '500' 
                  }}>View:</span>
                  <ViewModeDropdown
                    currentView={viewMode}
                    onViewChange={(mode) => { clearSelection(); onViewModeChange(mode); }}
                  />
                </>
              )}
              
              {isControlVisible('sort') && (
                <div className="sort-button-container" ref={sortRef} style={{ position: 'relative' }}>
                  <button 
                    className="mtgo-button sort-toggle-btn"
                    onClick={() => setShowSortMenu(!showSortMenu)}
                    title="Sort options"
                    style={{
                      padding: '3px 6px',
                      background: '#333333',
                      border: '1px solid #555555',
                      color: '#ffffff',
                      fontSize: '12px',
                      cursor: 'pointer',
                      borderRadius: '2px',
                      transition: 'all 0.2s ease'
                    }}
                    onMouseEnter={(e) => e.currentTarget.style.background = '#4a4a4a'}
                    onMouseLeave={(e) => e.currentTarget.style.background = '#333333'}
                  >
                    Sort
                  </button>
                  {showSortMenu && (
                    <div className="sort-menu" style={{
                      position: 'fixed',
                      top: `${sortRef.current?.getBoundingClientRect().bottom || 0}px`,
                      left: `${sortRef.current?.getBoundingClientRect().left || 0}px`,
                      background: '#2a2a2a',
                      border: '1px solid #555555',
                      borderRadius: '2px',
                      boxShadow: '0 2px 8px rgba(0,0,0,0.5)',
                      zIndex: 500000, // NUCLEAR Z-INDEX - Sort menu
                      minWidth: '120px'
                    }}>
                      {['mana', 'color', 'rarity'].map((criteria) => (
                        <button 
                          key={criteria}
                          className={`mtgo-menu-item ${sortState.criteria === criteria ? 'active' : ''}`}
                          onClick={() => handleSortButtonClick(criteria as SortCriteria)}
                          style={{
                            display: 'block',
                            width: '100%',
                            padding: '6px 10px',
                            background: sortState.criteria === criteria ? '#4a4a4a' : 'transparent',
                            border: 'none',
                            color: '#ffffff',
                            fontSize: '12px',
                            textAlign: 'left',
                            cursor: 'pointer',
                            transition: 'background 0.2s ease'
                          }}
                          onMouseEnter={(e) => e.currentTarget.style.background = '#3a3a3a'}
                          onMouseLeave={(e) => e.currentTarget.style.background = sortState.criteria === criteria ? '#4a4a4a' : 'transparent'}
                        >
                          {criteria === 'mana' ? 'Mana Value' : criteria.charAt(0).toUpperCase() + criteria.slice(1)} {sortState.criteria === criteria && viewMode === 'card' ? (sortState.direction === 'asc' ? '↑' : '↓') : ''}
                        </button>
                      ))}
                    </div>
                  )}
                </div>
              )}
            </div>
          )}
          
          {/* Group 2: Size Control - Enhanced with Visual Grouping */}
          {isControlVisible('size') && (
            <div className="control-group-2" style={{ 
              display: 'flex', 
              alignItems: 'center', 
              gap: '6px',
              borderLeft: '1px solid #555555',
              paddingLeft: '12px',
              paddingRight: '12px'
            }}>
              <span style={{ 
                color: '#cccccc',
                fontSize: '12px',
                fontWeight: '500'
              }}>Size:</span>
              <CardSizeButtons
                currentMode={cardSizeMode}
                onModeChange={onCardSizeChange}
              />
            </div>
          )}
          
          {/* Group 3: Action Buttons - Enhanced Visual Hierarchy */}
          {isControlVisible('actions') && (
            <div className="control-group-3" style={{ 
              display: 'flex', 
              alignItems: 'center', 
              gap: '6px',
              borderLeft: '1px solid #555555',
              paddingLeft: '12px'
            }}>
              {[
                { onClick: onTextExport, title: "Export deck as text for MTGO", text: "Export" },
                { onClick: onScreenshot, title: "Generate deck image", text: "Screenshot" },
                { onClick: onClearDeck, title: "Clear all cards from deck and sideboard", text: "Clear" }
              ].map((button, index) => (
                <button 
                  key={index}
                  onClick={button.onClick} 
                  title={button.title}
                  className="mtgo-button-enhanced"
                  style={{
                    padding: '3px 6px',
                    background: '#333333',
                    border: '1px solid #555555',
                    color: '#ffffff',
                    fontSize: '12px',
                    cursor: 'pointer',
                    borderRadius: '2px',
                    transition: 'all 0.2s ease',
                    fontWeight: '500'
                  }}
                  onMouseEnter={(e) => {
                    e.currentTarget.style.background = '#4a4a4a';
                    e.currentTarget.style.transform = 'translateY(-1px)';
                    e.currentTarget.style.boxShadow = '0 2px 4px rgba(0,0,0,0.3)';
                  }}
                  onMouseLeave={(e) => {
                    e.currentTarget.style.background = '#333333';
                    e.currentTarget.style.transform = 'translateY(0)';
                    e.currentTarget.style.boxShadow = 'none';
                  }}
                >
                  {button.text}
                </button>
              ))}
            </div>
          )}

          {/* Responsive Overflow Menu */}
          {hiddenControls.length > 0 && (
            <div className="overflow-menu-container" ref={overflowRef} style={{ position: 'relative' }}>
              <button
                className="overflow-menu-toggle"
                onClick={(e) => { e.stopPropagation(); console.log("🔧 Overflow menu button clicked"); setShowOverflowMenu(!showOverflowMenu); }}
                title="More controls"
                style={{
                  padding: '3px 6px',
                  background: '#3b82f6',
                  border: '1px solid #2563eb',
                  color: '#ffffff',
                  fontSize: '12px',
                  cursor: 'pointer',
                  borderRadius: '2px',
                  fontWeight: 'bold',
                  transition: 'all 0.2s ease'
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.background = '#2563eb';
                  e.currentTarget.style.transform = 'scale(1.05)';
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.background = '#3b82f6';
                  e.currentTarget.style.transform = 'scale(1)';
                }}
              >
                ⋯
              </button>

              {showOverflowMenu && (
                <div className="overflow-menu" style={{
                  position: 'fixed',
                  top: `${overflowRef.current?.getBoundingClientRect().bottom || 0}px`,
                  left: `${overflowRef.current?.getBoundingClientRect().left || 0}px`,
                  background: '#2a2a2a',
                  border: '1px solid #555555',
                  borderRadius: '4px',
                  boxShadow: '0 4px 12px rgba(0,0,0,0.5)',
                  zIndex: 1000000, // MAXIMUM NUCLEAR Z-INDEX
                  minWidth: '200px',
                  overflow: 'visible'
                }}>
                  {renderOverflowControl('view', (
                    <div style={{ display: 'flex', alignItems: 'center', gap: '8px', width: '100%' }}>
                      <span style={{ color: '#cccccc', fontSize: '12px' }}>View:</span>
                      <div style={{ position: 'relative', zIndex: 10008 }}>
                        <ViewModeDropdown
                          currentView={viewMode}
                          onViewChange={(mode) => { 
                            clearSelection(); 
                            onViewModeChange(mode); 
                            setShowOverflowMenu(false);
                          }}
                        />
                      </div>
                    </div>
                  ))}

                  {renderOverflowControl('sort', (
                    <div style={{ display: 'flex', alignItems: 'center', gap: '8px', width: '100%' }}>
                      <span style={{ color: '#cccccc', fontSize: '12px' }}>Sort:</span>
                      <select 
                        value={sortState.criteria}
                        onChange={(e) => {
                          handleSortButtonClick(e.target.value as SortCriteria);
                          setShowOverflowMenu(false);
                        }}
                        style={{
                          background: '#333333',
                          border: '1px solid #555555',
                          color: '#ffffff',
                          fontSize: '12px',
                          padding: '2px 4px',
                          borderRadius: '2px'
                        }}
                      >
                        <option value="mana">Mana Value</option>
                        <option value="color">Color</option>
                        <option value="rarity">Rarity</option>
                      </select>
                    </div>
                  ))}

                  {renderOverflowControl('size', (
                    <div style={{ display: 'flex', alignItems: 'center', gap: '8px', width: '100%' }}>
                      <span style={{ color: '#cccccc', fontSize: '12px' }}>Size:</span>
                      <CardSizeButtons
                        currentMode={cardSizeMode}
                        onModeChange={onCardSizeChange}
                      />
                    </div>
                  ))}

                  {renderOverflowControl('actions', (
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '4px', width: '100%' }}>
                      {[
                        { onClick: onTextExport, text: "Export" },
                        { onClick: onScreenshot, text: "Screenshot" },
                        { onClick: onClearDeck, text: "Clear" }
                      ].map((button, index) => (
                        <button
                          key={index}
                          onClick={() => {
                            button.onClick();
                            setShowOverflowMenu(false);
                          }}
                          style={{
                            padding: '3px 6px',
                            background: '#333333',
                            border: '1px solid #555555',
                            color: '#ffffff',
                            fontSize: '12px',
                            cursor: 'pointer',
                            borderRadius: '2px',
                            textAlign: 'left'
                          }}
                        >
                          {button.text}
                        </button>
                      ))}
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}
        </div>
      </div>
      
      <div className="deck-content">
        {viewMode === 'pile' ? (
          <PileView
            cards={mainDeck}
            zone="deck"
            scaleFactor={getSizeConfig(cardSizeMode).scale}
            forcedSortCriteria={sortState.criteria === 'name' || sortState.criteria === 'type' ? 'mana' : sortState.criteria as any}
            onClick={(card, event) => onCardClick(card, event)}
            onInstanceClick={onInstanceClick}
            onEnhancedDoubleClick={onEnhancedDoubleClick}
            onRightClick={onCardRightClick}
            onDragStart={onDragStart}
            isSelected={isSelected}
            selectedCards={getSelectedCardObjects()}
            isDragActive={dragState.isDragging}
            onDragEnter={onDragEnter}
            onDragLeave={onDragLeave}
            canDropInZone={canDropInZone}
          />
        ) : viewMode === 'list' ? (
          <ListView
            cards={sortedMainDeck}
            area="deck"
            scaleFactor={getSizeConfig(cardSizeMode).scale}
            sortCriteria={sortState.criteria}
            sortDirection={sortState.direction}
            onSortChange={(criteria, direction) => {
              if (criteria === 'name' || criteria === 'mana' || criteria === 'color' || criteria === 'rarity') {
                onSortChange(criteria, direction);
              }
            }}
            onClick={(card, event) => onCardClick(card, event)}

            onRightClick={onCardRightClick}
            onDragStart={onDragStart}
            isSelected={isSelected}
            selectedCards={getSelectedCardObjects()}
            isDragActive={dragState.isDragging}
            onQuantityChange={onQuantityChange}
          />
        ) : (
          <div 
            className="deck-grid"
            style={{
              display: 'grid',
              gridTemplateColumns: `repeat(auto-fill, minmax(${Math.round(130 * getSizeConfig(cardSizeMode).scale)}px, max-content))`,
              gap: `${Math.round(4 * getSizeConfig(cardSizeMode).scale)}px`,
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
                    onInstanceClick(targetInstance.instanceId, targetInstance, event as React.MouseEvent);
                  } else {
                    onInstanceClick(representativeCard.instanceId, representativeCard, event as React.MouseEvent);
                  }
                };

                const handleStackInstanceClick = (instanceId: string, instance: DeckCardInstance, event: React.MouseEvent) => {
                  handleStackClick(instance, event);
                };

                const handleStackDragStart = (cards: any[], zone: any, event: React.MouseEvent) => {
                  onDragStart(cards, zone, event);
                };

                return (
                  <DraggableCard
                    key={cardId}
                    card={representativeCard}
                    zone="deck"
                    size="normal"
                    scaleFactor={getSizeConfig(cardSizeMode).scale}
                    onClick={handleStackClick}
                    instanceId={representativeCard.instanceId}
                    isInstance={true}
                    onInstanceClick={handleStackInstanceClick}
                    onEnhancedDoubleClick={onEnhancedDoubleClick}
                    onRightClick={onCardRightClick}
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
          </div>
        )}
      </div>
    </DropZoneComponent>
  );
};

export default DeckArea;