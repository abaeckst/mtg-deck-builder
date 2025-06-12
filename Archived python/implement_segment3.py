#!/usr/bin/env python3
"""
Segment 3 Implementation: Enhanced Control Grouping + Responsive Features
- Enhanced visual control grouping with MTGO styling
- Responsive overflow menu for space-constrained scenarios
- Text overflow solutions and responsive design
- MTGO visual polish with hover effects and micro-animations
"""

import os
import shutil

def backup_file(file_path):
    """Create a backup of the original file"""
    backup_path = f"{file_path}.segment3_backup"
    if os.path.exists(file_path):
        shutil.copy2(file_path, backup_path)
        print(f"✅ Backup created: {backup_path}")
    return backup_path

def update_deckarea_file():
    """Update DeckArea.tsx with enhanced responsive controls"""
    file_path = "src/components/DeckArea.tsx"
    
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return False
    
    # Create backup
    backup_file(file_path)
    
    # Enhanced DeckArea.tsx content with all Segment 3 features
    enhanced_content = '''import React, { useState, useCallback, useRef, useEffect } from 'react';
import { ScryfallCard, DeckCard, DeckCardInstance, getCardId } from '../types/card';
import { SortCriteria, SortDirection } from '../hooks/useSorting';
import { DropZone as DropZoneType, DraggedCard } from '../hooks/useDragAndDrop';
import DraggableCard from './DraggableCard';
import DropZoneComponent from './DropZone';
import ListView from './ListView';
import PileView from './PileView';
import ViewModeDropdown from './ViewModeDropdown';

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
  cardSize: number;
  onCardSizeChange: (size: number) => void; // This will affect both deck and sideboard
  
  // Card interactions
  onCardClick: (card: ScryfallCard | DeckCard | DeckCardInstance, event?: React.MouseEvent) => void;
  onInstanceClick: (instanceId: string, instance: DeckCardInstance, event: React.MouseEvent) => void;
  onCardDoubleClick: (card: ScryfallCard | DeckCard | DeckCardInstance) => void;
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
  cardSize,
  onCardSizeChange,
  onCardClick,
  onInstanceClick,
  onCardDoubleClick,
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

  // Responsive overflow menu state
  const [showOverflowMenu, setShowOverflowMenu] = useState(false);
  const [hiddenControls, setHiddenControls] = useState<string[]>([]);
  const headerRef = useRef<HTMLDivElement>(null);
  const controlsRef = useRef<HTMLDivElement>(null);
  const overflowRef = useRef<HTMLDivElement>(null);

  // Click-outside effect for sort menu
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (sortRef.current && !sortRef.current.contains(event.target as Node)) {
        setShowSortMenu(false);
      }
      if (overflowRef.current && !overflowRef.current.contains(event.target as Node)) {
        setShowOverflowMenu(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, []);

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
        padding: '8px 12px',
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
          padding: '12px 16px',
          color: '#ffffff',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          gap: '16px',
          fontSize: '14px',
          position: 'relative'
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
            fontSize: '16px',
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
            fontSize: '14px',
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
            gap: '12px',
            fontSize: '13px',
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
              gap: '8px',
              padding: '4px 8px',
              background: 'rgba(255,255,255,0.05)',
              borderRadius: '4px',
              border: '1px solid rgba(255,255,255,0.1)'
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
                      padding: '4px 8px',
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
                      background: '#2a2a2a',
                      border: '1px solid #555555',
                      borderRadius: '2px',
                      boxShadow: '0 2px 8px rgba(0,0,0,0.5)',
                      zIndex: 10001,
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
              gap: '8px',
              borderLeft: '1px solid #555555',
              paddingLeft: '12px',
              background: 'rgba(255,255,255,0.03)',
              padding: '4px 8px 4px 12px',
              borderRadius: '4px'
            }}>
              <span style={{ 
                color: '#cccccc',
                fontSize: '12px',
                fontWeight: '500'
              }}>Size:</span>
              <input
                type="range"
                min="1.3"
                max="2.5"
                step="0.1"
                value={cardSize}
                onChange={(e) => {
                  const newSize = parseFloat(e.target.value);
                  onCardSizeChange(newSize);
                }}
                className="mtgo-slider-enhanced"
                title={`Card size: ${Math.round(cardSize * 100)}%`}
                style={{
                  width: '80px',
                  height: '6px',
                  background: 'linear-gradient(to right, #555555, #777777)',
                  outline: 'none',
                  borderRadius: '3px',
                  cursor: 'pointer',
                  transition: 'all 0.2s ease'
                }}
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
              paddingLeft: '12px',
              background: 'rgba(255,255,255,0.03)',
              padding: '4px 6px 4px 12px',
              borderRadius: '4px'
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
                    padding: '4px 8px',
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
                onClick={() => setShowOverflowMenu(!showOverflowMenu)}
                title="More controls"
                style={{
                  padding: '4px 8px',
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
                  background: '#2a2a2a',
                  border: '1px solid #555555',
                  borderRadius: '4px',
                  boxShadow: '0 4px 12px rgba(0,0,0,0.5)',
                  zIndex: 10001,
                  minWidth: '200px',
                  overflow: 'hidden'
                }}>
                  {renderOverflowControl('view', (
                    <div style={{ display: 'flex', alignItems: 'center', gap: '8px', width: '100%' }}>
                      <span style={{ color: '#cccccc', fontSize: '12px' }}>View:</span>
                      <ViewModeDropdown
                        currentView={viewMode}
                        onViewChange={(mode) => { 
                          clearSelection(); 
                          onViewModeChange(mode); 
                          setShowOverflowMenu(false);
                        }}
                      />
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
                      <input
                        type="range"
                        min="1.3"
                        max="2.5"
                        step="0.1"
                        value={cardSize}
                        onChange={(e) => onCardSizeChange(parseFloat(e.target.value))}
                        style={{
                          width: '80px',
                          height: '4px',
                          background: '#555555',
                          borderRadius: '2px'
                        }}
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
                            padding: '4px 8px',
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
            scaleFactor={cardSize}
            forcedSortCriteria={sortState.criteria === 'name' || sortState.criteria === 'type' ? 'mana' : sortState.criteria as any}
            onClick={(card, event) => onCardClick(card, event)}
            onInstanceClick={onInstanceClick}
            onDoubleClick={onCardDoubleClick}
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
            scaleFactor={cardSize}
            sortCriteria={sortState.criteria}
            sortDirection={sortState.direction}
            onSortChange={(criteria, direction) => {
              if (criteria === 'name' || criteria === 'mana' || criteria === 'color' || criteria === 'rarity') {
                onSortChange(criteria, direction);
              }
            }}
            onClick={(card, event) => onCardClick(card, event)}
            onDoubleClick={(card) => onEnhancedDoubleClick(card as any, 'deck', { preventDefault: () => {}, stopPropagation: () => {} } as React.MouseEvent)}
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
              gridTemplateColumns: `repeat(auto-fill, minmax(${Math.round(130 * cardSize)}px, max-content))`,
              gap: `${Math.round(4 * cardSize)}px`,
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
                  onDragStart(instances as any[], zone, event);
                };

                return (
                  <DraggableCard
                    key={cardId}
                    card={representativeCard}
                    zone="deck"
                    size="normal"
                    scaleFactor={cardSize}
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

export default DeckArea;'''
    
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(enhanced_content)
        print(f"✅ Updated {file_path} with Segment 3 responsive controls and enhanced grouping")
        return True
    except Exception as e:
        print(f"❌ Error updating {file_path}: {e}")
        return False

def update_css_file():
    """Add Segment 3 enhanced styles to MTGOLayout.css"""
    css_file_path = "src/components/MTGOLayout.css"
    
    if not os.path.exists(css_file_path):
        print(f"❌ File not found: {css_file_path}")
        return False
    
    # Create backup
    backup_file(css_file_path)
    
    # Segment 3 enhanced CSS styles
    segment3_css = '''

/* ===== SEGMENT 3: ENHANCED CONTROL GROUPING + RESPONSIVE FEATURES ===== */

/* Enhanced Control Groups with MTGO Visual Hierarchy */
.control-group-1,
.control-group-2,
.control-group-3 {
  position: relative;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

.control-group-1:hover,
.control-group-2:hover,
.control-group-3:hover {
  background: rgba(255,255,255,0.08) !important;
  border-color: rgba(255,255,255,0.2) !important;
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(0,0,0,0.3);
}

/* Enhanced MTGO Button Styling with Micro-Animations */
.mtgo-button-enhanced {
  position: relative;
  overflow: hidden;
}

.mtgo-button-enhanced::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
  transition: left 0.5s ease;
}

.mtgo-button-enhanced:hover::before {
  left: 100%;
}

/* Enhanced Slider Styling with Professional Polish */
.mtgo-slider-enhanced {
  -webkit-appearance: none;
  appearance: none;
  background: linear-gradient(to right, #555555, #777777);
  outline: none;
  border-radius: 3px;
  cursor: pointer;
  transition: all 0.2s ease;
  position: relative;
}

.mtgo-slider-enhanced:hover {
  background: linear-gradient(to right, #666666, #888888);
  transform: scaleY(1.2);
}

.mtgo-slider-enhanced::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 16px;
  height: 16px;
  background: radial-gradient(circle, #3b82f6, #2563eb);
  border-radius: 50%;
  cursor: pointer;
  border: 2px solid #ffffff;
  box-shadow: 0 2px 4px rgba(0,0,0,0.3);
  transition: all 0.2s ease;
}

.mtgo-slider-enhanced::-webkit-slider-thumb:hover {
  background: radial-gradient(circle, #2563eb, #1d4ed8);
  transform: scale(1.15);
  box-shadow: 0 4px 8px rgba(59,130,246,0.4);
}

.mtgo-slider-enhanced::-webkit-slider-thumb:active {
  transform: scale(1.05);
  box-shadow: 0 2px 6px rgba(59,130,246,0.6);
}

.mtgo-slider-enhanced::-moz-range-thumb {
  width: 16px;
  height: 16px;
  background: radial-gradient(circle, #3b82f6, #2563eb);
  border: 2px solid #ffffff;
  border-radius: 50%;
  cursor: pointer;
  box-shadow: 0 2px 4px rgba(0,0,0,0.3);
  transition: all 0.2s ease;
}

.mtgo-slider-enhanced::-moz-range-thumb:hover {
  background: radial-gradient(circle, #2563eb, #1d4ed8);
  transform: scale(1.15);
  box-shadow: 0 4px 8px rgba(59,130,246,0.4);
}

/* Responsive Overflow Menu Styling */
.overflow-menu-container {
  z-index: 10003 !important;
}

.overflow-menu-toggle {
  position: relative;
  overflow: hidden;
}

.overflow-menu-toggle::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  background: rgba(255,255,255,0.2);
  border-radius: 50%;
  transform: translate(-50%, -50%);
  transition: width 0.3s ease, height 0.3s ease;
}

.overflow-menu-toggle:hover::after {
  width: 200%;
  height: 200%;
}

.overflow-menu {
  animation: menuSlideIn 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  backdrop-filter: blur(8px);
  border: 1px solid rgba(255,255,255,0.1) !important;
}

@keyframes menuSlideIn {
  from {
    opacity: 0;
    transform: translateY(-10px) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.overflow-menu-item {
  transition: background-color 0.2s ease, transform 0.1s ease;
  border-bottom: 1px solid rgba(255,255,255,0.1) !important;
}

.overflow-menu-item:last-child {
  border-bottom: none !important;
}

.overflow-menu-item:hover {
  background-color: rgba(255,255,255,0.1) !important;
  transform: translateX(2px);
}

/* Text Overflow Solutions for Responsive Headers */
.title-section {
  position: relative;
}

.title-section span:first-child {
  position: relative;
}

.title-section span:first-child::after {
  content: attr(title);
  position: absolute;
  bottom: 120%;
  left: 0;
  background: rgba(0,0,0,0.9);
  color: #ffffff;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  white-space: nowrap;
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.2s ease;
  z-index: 10005;
}

.title-section span:first-child:hover::after {
  opacity: 1;
}

/* Enhanced Responsive Controls Container */
.deck-controls-responsive {
  position: relative;
  min-height: 32px;
}

/* Smooth transitions for control hiding/showing */
.control-group-1,
.control-group-2,
.control-group-3 {
  transition: opacity 0.3s ease, transform 0.3s ease, width 0.3s ease;
}

.control-group-1[style*="display: none"],
.control-group-2[style*="display: none"],
.control-group-3[style*="display: none"] {
  opacity: 0;
  transform: scale(0.8);
  width: 0;
  overflow: hidden;
}

/* Enhanced Sort Menu with MTGO Polish */
.sort-menu {
  animation: menuSlideIn 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  backdrop-filter: blur(4px);
  border: 1px solid rgba(255,255,255,0.1) !important;
}

.mtgo-menu-item {
  position: relative;
  overflow: hidden;
}

.mtgo-menu-item::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  width: 0;
  height: 100%;
  background: linear-gradient(90deg, #3b82f6, #2563eb);
  transition: width 0.3s ease;
  z-index: -1;
}

.mtgo-menu-item:hover::before {
  width: 100%;
}

.mtgo-menu-item.active::before {
  width: 100%;
  background: linear-gradient(90deg, #2563eb, #1d4ed8);
}

/* Professional Focus States */
.mtgo-button-enhanced:focus,
.mtgo-slider-enhanced:focus,
.overflow-menu-toggle:focus {
  outline: 2px solid #3b82f6;
  outline-offset: 2px;
}

/* Accessibility: High Contrast Mode Support */
@media (prefers-contrast: high) {
  .control-group-1,
  .control-group-2,
  .control-group-3 {
    border: 2px solid currentColor !important;
  }
  
  .overflow-menu {
    border: 2px solid currentColor !important;
  }
}

/* Accessibility: Reduced Motion Support */
@media (prefers-reduced-motion: reduce) {
  .control-group-1,
  .control-group-2,
  .control-group-3,
  .mtgo-button-enhanced,
  .mtgo-slider-enhanced,
  .overflow-menu-toggle,
  .overflow-menu,
  .overflow-menu-item {
    transition: none !important;
    animation: none !important;
  }
  
  .mtgo-button-enhanced::before,
  .overflow-menu-toggle::after,
  .mtgo-menu-item::before {
    transition: none !important;
  }
}

/* Enhanced Header Responsiveness */
@media (max-width: 1200px) {
  .mtgo-header {
    padding: 10px 12px !important;
    gap: 12px !important;
  }
  
  .control-group-1,
  .control-group-2,
  .control-group-3 {
    gap: 6px !important;
    padding: 3px 6px !important;
  }
  
  .title-section {
    max-width: 250px !important;
  }
}

@media (max-width: 900px) {
  .mtgo-header {
    padding: 8px 10px !important;
    gap: 8px !important;
  }
  
  .title-section {
    max-width: 200px !important;
  }
  
  .title-section span:first-child {
    font-size: 14px !important;
  }
  
  .title-section span:last-child {
    font-size: 12px !important;
  }
}

@media (max-width: 600px) {
  .mtgo-header {
    flex-direction: column !important;
    align-items: stretch !important;
    gap: 8px !important;
  }
  
  .title-section {
    max-width: none !important;
    justify-content: center !important;
  }
  
  .deck-controls-responsive {
    justify-content: center !important;
  }
}

/* Enhanced Visual Feedback for Interactive Elements */
.mtgo-button-enhanced:active {
  transform: translateY(0) scale(0.98) !important;
}

.overflow-menu-toggle:active {
  transform: scale(0.95) !important;
}

/* Subtle Glow Effects for Premium Feel */
.control-group-1:hover,
.control-group-2:hover,
.control-group-3:hover {
  box-shadow: 
    0 2px 8px rgba(0,0,0,0.3),
    inset 0 1px 0 rgba(255,255,255,0.1) !important;
}

.mtgo-button-enhanced:hover {
  box-shadow: 
    0 2px 4px rgba(0,0,0,0.3),
    0 0 8px rgba(59,130,246,0.2) !important;
}

.overflow-menu-toggle:hover {
  box-shadow: 
    0 2px 8px rgba(59,130,246,0.3),
    0 0 12px rgba(59,130,246,0.2) !important;
}

/* Loading States for Async Operations */
.mtgo-button-enhanced.loading {
  position: relative;
  color: transparent !important;
}

.mtgo-button-enhanced.loading::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 12px;
  height: 12px;
  border: 2px solid #ffffff;
  border-top: 2px solid transparent;
  border-radius: 50%;
  transform: translate(-50%, -50%);
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: translate(-50%, -50%) rotate(0deg); }
  100% { transform: translate(-50%, -50%) rotate(360deg); }
}

/* Enhanced Z-Index Management */
.mtgo-header {
  position: relative;
  z-index: 100;
}

.sort-menu,
.overflow-menu {
  z-index: 10001 !important;
}

.overflow-menu-container {
  z-index: 10002 !important;
}

/* Professional Typography Refinements */
.mtgo-header * {
  font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
  font-feature-settings: 'tnum', 'liga';
  text-rendering: optimizeLegibility;
}

.control-group-1 span,
.control-group-2 span,
.control-group-3 span {
  text-shadow: 0 1px 2px rgba(0,0,0,0.5);
  letter-spacing: 0.025em;
}

/* ===== END SEGMENT 3 ENHANCED STYLES ===== */'''
    
    try:
        # Read existing content
        with open(css_file_path, 'r', encoding='utf-8') as f:
            existing_content = f.read()
        
        # Append Segment 3 styles
        updated_content = existing_content + segment3_css
        
        # Write updated content
        with open(css_file_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        print(f"✅ Added Segment 3 enhanced styles to {css_file_path}")
        return True
    except Exception as e:
        print(f"❌ Error updating {css_file_path}: {e}")
        return False

def main():
    """Main implementation function"""
    print("🚀 Implementing Segment 3: Enhanced Control Grouping + Responsive Features")
    print("=" * 80)
    
    # Implementation steps
    success_count = 0
    total_steps = 2
    
    print("\n📋 Step 1: Updating DeckArea.tsx with responsive controls and enhanced grouping...")
    if update_deckarea_file():
        success_count += 1
    
    print("\n📋 Step 2: Adding Segment 3 enhanced CSS styles...")
    if update_css_file():
        success_count += 1
    
    # Summary
    print("\n" + "=" * 80)
    print(f"🎯 Segment 3 Implementation Summary: {success_count}/{total_steps} steps completed")
    
    if success_count == total_steps:
        print("✅ SUCCESS: All Segment 3 features implemented!")
        print("\n🎨 Segment 3 Features Added:")
        print("   • Enhanced control grouping with visual hierarchy")
        print("   • Responsive overflow menu for space-constrained scenarios")
        print("   • Text overflow solutions with MTGO theming")
        print("   • MTGO visual polish with hover effects and micro-animations")
        print("   • Professional focus states and accessibility support")
        print("   • Smooth transitions and premium interaction feedback")
        
        print("\n🧪 Testing Instructions:")
        print("   1. Run `npm start` to test the application")
        print("   2. Resize the browser window to see responsive overflow menu")
        print("   3. Test hover effects on control groups and buttons")
        print("   4. Verify dropdown menus appear above all other elements")
        print("   5. Test overflow menu functionality in narrow layouts")
        
        print("\n📱 Responsive Features:")
        print("   • Controls automatically hide when space is limited")
        print("   • Overflow menu appears with hidden controls")
        print("   • Graceful degradation at different screen sizes")
        print("   • Text truncation prevents layout breaking")
        
        print("\n🎯 Ready for production use with professional MTGO styling!")
    else:
        print("⚠️  PARTIAL SUCCESS: Some steps failed - check errors above")
        print("💡 Restore backups if needed: .segment3_backup files created")

if __name__ == "__main__":
    main()
