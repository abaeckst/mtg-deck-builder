// src/components/ListView.tsx - Universal List View Component
import React, { useState, useCallback, useMemo, useRef, useEffect } from 'react';
import { ScryfallCard, DeckCard, isBasicLand } from '../types/card';
import { DropZone } from '../hooks/useDragAndDrop';

export type SortCriteria = 'name' | 'mana' | 'color' | 'rarity' | 'type';

interface ListViewProps {
  cards: (ScryfallCard | DeckCard)[];
  area: 'collection' | 'deck' | 'sideboard';
  scaleFactor: number;
  sortCriteria: SortCriteria;
  sortDirection: 'asc' | 'desc';
  onSortChange: (criteria: SortCriteria, direction: 'asc' | 'desc') => void;
  // Standard card interaction handlers
  onClick: (card: ScryfallCard | DeckCard, event?: React.MouseEvent) => void;
  onDoubleClick: (card: ScryfallCard | DeckCard) => void;
  onRightClick: (card: ScryfallCard | DeckCard, zone: DropZone, event: React.MouseEvent) => void;
  onDragStart: (cards: (ScryfallCard | DeckCard)[], zone: DropZone, event: React.MouseEvent) => void;
  // Selection and drag state
  isSelected: (cardId: string) => boolean;
  selectedCards: (ScryfallCard | DeckCard)[];
  isDragActive: boolean;
  // Quantity management (deck/sideboard only)
  onQuantityChange?: (cardId: string, newQuantity: number) => void;
}

interface ColumnDefinition {
  id: string;
  title: string;
  minWidth: number;
  sortable: boolean;
  visible: boolean;
}

// Column definitions with minimum widths - Quantity first!
const COLUMN_DEFINITIONS: ColumnDefinition[] = [
  { id: 'quantity', title: 'Qty', minWidth: 80, sortable: false, visible: true },
  { id: 'name', title: 'Name', minWidth: 200, sortable: true, visible: true },
  { id: 'mana', title: 'Mana', minWidth: 80, sortable: true, visible: true },
  { id: 'type', title: 'Type', minWidth: 150, sortable: true, visible: true },
  { id: 'power', title: 'Power', minWidth: 60, sortable: true, visible: true },
  { id: 'toughness', title: 'Toughness', minWidth: 60, sortable: true, visible: true },
  { id: 'color', title: 'Color', minWidth: 80, sortable: true, visible: true },
  { id: 'text', title: 'Text', minWidth: 250, sortable: true, visible: true },
];

const ListView: React.FC<ListViewProps> = ({
  cards,
  area,
  scaleFactor,
  sortCriteria,
  sortDirection,
  onSortChange,
  onClick,
  onDoubleClick,
  onRightClick,
  onDragStart,
  isSelected,
  selectedCards,
  isDragActive,
  onQuantityChange,
}) => {
  const tableRef = useRef<HTMLDivElement>(null);
  const [columnWidths, setColumnWidths] = useState<Record<string, number>>(() => {
    const initialWidths: Record<string, number> = {};
    COLUMN_DEFINITIONS.forEach(col => {
      initialWidths[col.id] = col.minWidth;
    });
    return initialWidths;
  });
  const [resizing, setResizing] = useState<{
    columnId: string;
    startX: number;
    startWidth: number;
  } | null>(null);

  // Get visible columns based on area
  const visibleColumns = useMemo(() => {
    return COLUMN_DEFINITIONS.filter(col => {
      if (col.id === 'quantity') {
        return area !== 'collection'; // Only show quantity in deck/sideboard
      }
      return true;
    });
  }, [area]);

  // Handle column header click for sorting
  const handleHeaderClick = useCallback((columnId: string, sortable: boolean) => {
    if (!sortable) return;
    
    const newCriteria = columnId as SortCriteria;
    const newDirection = sortCriteria === newCriteria && sortDirection === 'asc' ? 'desc' : 'asc';
    onSortChange(newCriteria, newDirection);
  }, [sortCriteria, sortDirection, onSortChange]);

  // Handle column resize start
  const handleResizeStart = useCallback((columnId: string, event: React.MouseEvent) => {
    event.preventDefault();
    setResizing({
      columnId,
      startX: event.clientX,
      startWidth: columnWidths[columnId],
    });
  }, [columnWidths]);

  // Handle mouse move during resize
  useEffect(() => {
    const handleMouseMove = (event: MouseEvent) => {
      if (!resizing) return;
      
      const deltaX = event.clientX - resizing.startX;
      const newWidth = Math.max(
        COLUMN_DEFINITIONS.find(col => col.id === resizing.columnId)?.minWidth || 100,
        resizing.startWidth + deltaX
      );
      
      setColumnWidths(prev => ({
        ...prev,
        [resizing.columnId]: newWidth,
      }));
    };

    const handleMouseUp = () => {
      setResizing(null);
    };

    if (resizing) {
      document.addEventListener('mousemove', handleMouseMove);
      document.addEventListener('mouseup', handleMouseUp);
    }

    return () => {
      document.removeEventListener('mousemove', handleMouseMove);
      document.removeEventListener('mouseup', handleMouseUp);
    };
  }, [resizing]);

  // Format mana cost for display
  const formatManaCost = useCallback((manaCost?: string): string => {
    if (!manaCost) return '';
    // For now, return text. Could be enhanced with mana symbols later
    return manaCost;
  }, []);

  // Format colors for display
  const renderColors = useCallback((colors?: string[]): React.ReactNode => {
    if (!colors || colors.length === 0) {
      return <span className="color-circle color-c">C</span>;
    }

    return (
      <div className="color-circles">
        {colors.map((color, index) => (
          <span 
            key={index} 
            className={`color-circle color-${color.toLowerCase()}`}
            title={color}
          >
            {color}
          </span>
        ))}
      </div>
    );
  }, []);

  // Truncate text with ellipsis
  const truncateText = useCallback((text?: string, maxLength: number = 100): string => {
    if (!text) return '';
    return text.length > maxLength ? `${text.substring(0, maxLength)}...` : text;
  }, []);

  // Handle row click
  const handleRowClick = useCallback((card: ScryfallCard | DeckCard, event: React.MouseEvent) => {
    onClick(card, event);
  }, [onClick]);

  // Handle row double-click
  const handleRowDoubleClick = useCallback((card: ScryfallCard | DeckCard) => {
    onDoubleClick(card);
  }, [onDoubleClick]);

  // Handle row right-click
  const handleRowRightClick = useCallback((card: ScryfallCard | DeckCard, event: React.MouseEvent) => {
    event.preventDefault();
    onRightClick(card, area as DropZone, event);
  }, [onRightClick, area]);

  // Handle row drag start
  const handleRowDragStart = useCallback((card: ScryfallCard | DeckCard, event: React.MouseEvent) => {
    // Only handle left mouse button for drag
    if (event.button !== 0) return;
    
    const dragCards = isSelected(card.id) && selectedCards.length > 1 
      ? selectedCards 
      : [card];
    
    onDragStart(dragCards, area as DropZone, event);
  }, [isSelected, selectedCards, onDragStart, area]);

  // Handle quantity change
  const handleQuantityChange = useCallback((card: ScryfallCard | DeckCard, delta: number) => {
    if (!onQuantityChange || !('quantity' in card)) return;
    
    const currentQuantity = card.quantity || 0;
    const maxQuantity = isBasicLand(card) ? Infinity : 4;
    const newQuantity = Math.max(0, Math.min(maxQuantity, currentQuantity + delta));
    
    onQuantityChange(card.id, newQuantity);
  }, [onQuantityChange]);

  // Calculate total table width
  const totalWidth = useMemo(() => {
    return visibleColumns.reduce((sum, col) => sum + columnWidths[col.id], 0);
  }, [visibleColumns, columnWidths]);

  return (
    <div className="list-view" ref={tableRef}>
      <div className="list-view-container" style={{ overflowX: 'auto' }}>
        <table className="list-view-table" style={{ minWidth: `${totalWidth}px` }}>
          {/* Header */}
          <thead>
            <tr className="list-view-header-row">
              {visibleColumns.map((column, index) => (
                <th 
                  key={column.id}
                  className={`list-view-header-cell ${column.sortable ? 'sortable' : ''} ${
                    sortCriteria === column.id ? 'active' : ''
                  }`}
                  style={{ 
                    width: `${columnWidths[column.id]}px`,
                    minWidth: `${column.minWidth}px`,
                    position: 'relative',
                  }}
                  onClick={() => handleHeaderClick(column.id, column.sortable)}
                >
                  <div className="header-content">
                    <span className="header-title">{column.title}</span>
                    {column.sortable && sortCriteria === column.id && (
                      <span className="sort-indicator">
                        {sortDirection === 'asc' ? '↑' : '↓'}
                      </span>
                    )}
                  </div>
                  
                  {/* Resize handle */}
                  {index < visibleColumns.length - 1 && (
                    <div
                      className="column-resize-handle"
                      onMouseDown={(e) => handleResizeStart(column.id, e)}
                      style={{
                        position: 'absolute',
                        right: '-2px',
                        top: 0,
                        bottom: 0,
                        width: '4px',
                        cursor: 'col-resize',
                        backgroundColor: 'transparent',
                        borderRight: '1px solid #555',
                      }}
                    />
                  )}
                </th>
              ))}
            </tr>
          </thead>
          
          {/* Body - DEBUG VERSION */}
          <tbody>
            {cards.map((card, index) => {
              // DETAILED DEBUG LOGGING - Add this for first card only
              if (index === 0) {
                console.log('🔍 DETAILED CARD ANALYSIS:');
                console.log('Card object:', card);
                console.log('All card properties:', Object.keys(card));
                console.log('Oracle text check:', {
                  'oracle_text in card': 'oracle_text' in card,
                  'card.oracle_text': (card as any).oracle_text,
                  'typeof oracle_text': typeof (card as any).oracle_text,
                  'oracle_text is null': (card as any).oracle_text === null,
                  'oracle_text is undefined': (card as any).oracle_text === undefined
                });
                console.log('Power check:', {
                  'power in card': 'power' in card,
                  'card.power': (card as any).power,
                  'typeof power': typeof (card as any).power,
                  'power is null': (card as any).power === null,
                  'power is undefined': (card as any).power === undefined
                });
                console.log('Toughness check:', {
                  'toughness in card': 'toughness' in card,
                  'card.toughness': (card as any).toughness,
                  'typeof toughness': typeof (card as any).toughness,
                  'toughness is null': (card as any).toughness === null,
                  'toughness is undefined': (card as any).toughness === undefined
                });
                
                // Check for alternative property names
                console.log('Alternative properties check:', {
                  'text': (card as any).text,
                  'oracle': (card as any).oracle,
                  'rules_text': (card as any).rules_text,
                  'card_text': (card as any).card_text
                });
              }
              
              return (
                <tr
                  key={card.id}
                  className={`list-view-row ${isSelected(card.id) ? 'selected' : ''} ${
                    index % 2 === 0 ? 'even' : 'odd'
                  }`}
                  onClick={(e) => handleRowClick(card, e)}
                  onDoubleClick={() => handleRowDoubleClick(card)}
                  onContextMenu={(e) => handleRowRightClick(card, e)}
                  onMouseDown={(e) => {
                    // Only handle left mouse button for drag
                    if (e.button === 0) {
                      handleRowDragStart(card, e);
                    }
                  }}
                  draggable={true}
                >
                  {visibleColumns.map((column) => (
                    <td 
                      key={column.id}
                      className="list-view-cell"
                      style={{ 
                        width: `${columnWidths[column.id]}px`,
                        minWidth: `${column.minWidth}px`,
                      }}
                    >
                      {column.id === 'name' && (
                        <span className="card-name" title={card.name}>
                          {truncateText(card.name, 30)}
                        </span>
                      )}
                      
                      {column.id === 'mana' && (
                        <span className="mana-cost">
                          {formatManaCost(card.mana_cost)}
                        </span>
                      )}
                      
                      {column.id === 'type' && (
                        <span className="type-line" title={card.type_line}>
                          {truncateText(card.type_line, 20)}
                        </span>
                      )}
                      
                      {column.id === 'power' && (
                        <span className="power">
                          {(card as any).power !== null && (card as any).power !== undefined ? (card as any).power : '—'}
                        </span>
                      )}
                      
                      {column.id === 'toughness' && (
                        <span className="toughness">
                          {(card as any).toughness !== null && (card as any).toughness !== undefined ? (card as any).toughness : '—'}
                        </span>
                      )}
                      
                      {column.id === 'color' && renderColors(card.colors)}
                      
                      {column.id === 'text' && (
                        <span className="oracle-text" title={(card as any).oracle_text || ''}>
                          {truncateText((card as any).oracle_text || '', 50)}
                        </span>
                      )}
                      
                      {column.id === 'quantity' && 'quantity' in card && onQuantityChange && (
                        <div className="quantity-controls">
                          <span className="quantity-display">{card.quantity}</span>
                          <div className="quantity-buttons">
                            <button 
                              className="quantity-btn minus"
                              onClick={(e) => {
                                e.stopPropagation();
                                handleQuantityChange(card, -1);
                              }}
                              disabled={card.quantity === 0}
                            >
                              −
                            </button>
                            <button 
                              className="quantity-btn plus"
                              onClick={(e) => {
                                e.stopPropagation();
                                handleQuantityChange(card, 1);
                              }}
                              disabled={!isBasicLand(card) && card.quantity >= 4}
                            >
                              +
                            </button>
                          </div>
                        </div>
                      )}
                    </td>
                  ))}
                </tr>
              );
            })}
          </tbody>
        </table>
        
        {/* Empty state */}
        {cards.length === 0 && (
          <div className="list-view-empty">
            <div className="empty-message">
              {area === 'collection' ? 'No cards found' : `No cards in ${area}`}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default ListView;