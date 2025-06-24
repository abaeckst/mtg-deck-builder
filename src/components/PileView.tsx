// ===== FILE: src/components/PileView.tsx - PERFORMANCE OPTIMIZATION =====
import React, { useState, useCallback, useMemo } from 'react';
import { ScryfallCard, DeckCard, DeckCardInstance, getCardId } from '../types/card';
import { DropZone } from '../hooks/useDragAndDrop';
import PileColumn from './PileColumn';
// import PileSortControls from './PileSortControls'; // Unused import

export type PileSortCriteria = 'mana' | 'color' | 'rarity' | 'type';
export type SortCriteria = 'name' | 'mana' | 'color' | 'rarity' | 'type';

interface PileViewProps {
  cards: (ScryfallCard | DeckCard | DeckCardInstance)[];
  zone: 'deck' | 'sideboard';
  scaleFactor: number;
  forcedSortCriteria?: PileSortCriteria; // External sort control from parent
  // Enhanced card interaction handlers - now supporting both card and instance clicks
  onClick?: (card: ScryfallCard | DeckCard | DeckCardInstance, event?: React.MouseEvent) => void;
  onInstanceClick?: (instanceId: string, instance: DeckCardInstance, event: React.MouseEvent) => void;  onEnhancedDoubleClick?: (card: ScryfallCard | DeckCard | DeckCardInstance, zone: DropZone, event: React.MouseEvent) => void;
  onRightClick?: (card: ScryfallCard | DeckCard | DeckCardInstance, zone: DropZone, event: React.MouseEvent) => void;
  onDragStart?: (cards: (ScryfallCard | DeckCard | DeckCardInstance)[], zone: DropZone, event: React.MouseEvent) => void;
  // Selection and drag state
  isSelected?: (id: string) => boolean; // Now accepts both card IDs and instance IDs
  selectedCards?: (ScryfallCard | DeckCard | DeckCardInstance)[];
  isDragActive?: boolean;
  // Drop zone handlers
  onDragEnter?: (zone: DropZone, canDrop: boolean) => void;
  onDragLeave?: () => void;
  canDropInZone?: (zone: DropZone, cards: (ScryfallCard | DeckCard)[]) => boolean;
}

interface ColumnData {
  id: string;
  title: string;
  cards: (ScryfallCard | DeckCard | DeckCardInstance)[];
  sortValue: string | number;
}

const PileView: React.FC<PileViewProps> = ({
  cards,
  zone,
  scaleFactor,
  forcedSortCriteria,
  onClick,
  onInstanceClick,  onEnhancedDoubleClick,
  onRightClick,
  onDragStart,
  isSelected = () => false,
  selectedCards = [],
  isDragActive = false,
  onDragEnter,
  onDragLeave,
  canDropInZone
}) => {
  // Use external sort criteria or default to mana
  const sortCriteria = forcedSortCriteria || 'mana';
  
  // Manual arrangements state (persisted per zone)
  const [manualArrangements, setManualArrangements] = useState<Map<string, string>>(new Map());

  // PERFORMANCE FIX: Memoize color name mapping
  const colorNameMap = useMemo<Record<string, string>>(() => ({
    'W': 'White',
    'U': 'Blue', 
    'B': 'Black',
    'R': 'Red',
    'G': 'Green',
    'C': 'Colorless'
  }), []);

  // Helper function for color names - now using memoized map
  const getColorName = useCallback((colorCode: string): string => {
    return colorNameMap[colorCode] || colorCode;
  }, [colorNameMap]);

  // PERFORMANCE FIX: Memoize rarity configuration
  const rarityConfig = useMemo(() => ({
    order: ['common', 'uncommon', 'rare', 'mythic'] as const,
    labels: {
      common: 'Common', 
      uncommon: 'Uncommon', 
      rare: 'Rare', 
      mythic: 'Mythic' 
    } as Record<string, string>
  }), []);

  // Organize by mana value (0|1|2|3|4|5|6|7+) - Only show columns with cards
  const organizeByManaValue = useCallback((cardList: (ScryfallCard | DeckCard | DeckCardInstance)[]): ColumnData[] => {
    const columns: ColumnData[] = [];
    
    // Create columns for CMC 0-6 - only if they have cards
    for (let cmc = 0; cmc <= 6; cmc++) {
      const columnCards = cardList.filter(card => {
        const cardCmc = card.cmc ?? 0;
        return cardCmc === cmc;
      });
      if (columnCards.length > 0) {
        columns.push({
          id: `cmc-${cmc}`,
          title: `${cmc}`,
          cards: columnCards,
          sortValue: cmc
        });
      }
    }
    
    // 7+ column - only if it has cards
    const highCmcCards = cardList.filter(card => {
      const cardCmc = card.cmc ?? 0;
      return cardCmc >= 7;
    });
    if (highCmcCards.length > 0) {
      columns.push({
        id: 'cmc-7plus',
        title: '7+',
        cards: highCmcCards,
        sortValue: 7
      });
    }
    
    return columns;
  }, []);

  // Organize by color (W|U|B|R|G|Multi|C) - separate column for each combination
  const organizeByColor = useCallback((cardList: (ScryfallCard | DeckCard | DeckCardInstance)[]): ColumnData[] => {
    const colorGroups = new Map<string, (ScryfallCard | DeckCard | DeckCardInstance)[]>();
    
    cardList.forEach(card => {
      const colors = card.colors ?? [];
      let colorKey: string;
      
      if (colors.length === 0) {
        colorKey = 'C'; // Colorless
      } else if (colors.length === 1) {
        colorKey = colors[0]; // Single color
      } else {
        // Multi-color - sort colors for consistent key
        colorKey = [...colors].sort().join('');
      }
      
      if (!colorGroups.has(colorKey)) {
        colorGroups.set(colorKey, []);
      }
      colorGroups.get(colorKey)!.push(card);
    });
    
    // Convert to columns with proper titles
    const columns: ColumnData[] = [];
    const colorOrder = ['W', 'U', 'B', 'R', 'G', 'C']; // Single colors first
    
    // Add single color columns
    colorOrder.forEach(color => {
      if (colorGroups.has(color)) {
        const colorName = getColorName(color);
        columns.push({
          id: `color-${color}`,
          title: colorName,
          cards: colorGroups.get(color)!,
          sortValue: color
        });
        colorGroups.delete(color);
      }
    });
    
    // Add multi-color columns (sorted by color combination)
    Array.from(colorGroups.entries())
      .sort(([a], [b]) => a.localeCompare(b))
      .forEach(([colorKey, colorCards]) => {
        const title = colorKey.length > 1 ? 'Multi' : colorKey;
        columns.push({
          id: `color-${colorKey}`,
          title: title,
          cards: colorCards,
          sortValue: colorKey
        });
      });
    
    return columns;
  }, [getColorName]);

  // Organize by rarity (C|U|R|M) - now using memoized config
  const organizeByRarity = useCallback((cardList: (ScryfallCard | DeckCard | DeckCardInstance)[]): ColumnData[] => {
    return rarityConfig.order
      .map(rarity => {
        const rarityCards = cardList.filter(card => card.rarity === rarity);
        return {
          id: `rarity-${rarity}`,
          title: rarityConfig.labels[rarity] || rarity,
          cards: rarityCards,
          sortValue: rarity
        };
      })
      .filter(column => column.cards.length > 0);
  }, [rarityConfig]);

  // PERFORMANCE FIX: Memoize type order configuration
  const typeOrderConfig = useMemo(() => [
    'Creatures', 'Instants', 'Sorceries', 'Artifacts', 'Enchantments', 'Planeswalkers', 'Lands', 'Other'
  ], []);

  // Organize by card type (Creatures, Instants, Sorceries, etc.)
  const organizeByType = useCallback((cardList: (ScryfallCard | DeckCard | DeckCardInstance)[]): ColumnData[] => {
    const typeGroups = new Map<string, (ScryfallCard | DeckCard | DeckCardInstance)[]>();
    
    cardList.forEach(card => {
      const typeLine = card.type_line ?? '';
      let primaryType = 'Other';
      const lowerTypeLine = typeLine.toLowerCase();
      
      // Determine primary type from type line
      if (lowerTypeLine.includes('creature')) primaryType = 'Creatures';
      else if (lowerTypeLine.includes('instant')) primaryType = 'Instants';
      else if (lowerTypeLine.includes('sorcery')) primaryType = 'Sorceries';
      else if (lowerTypeLine.includes('artifact')) primaryType = 'Artifacts';
      else if (lowerTypeLine.includes('enchantment')) primaryType = 'Enchantments';
      else if (lowerTypeLine.includes('planeswalker')) primaryType = 'Planeswalkers';
      else if (lowerTypeLine.includes('land')) primaryType = 'Lands';
      
      if (!typeGroups.has(primaryType)) {
        typeGroups.set(primaryType, []);
      }
      typeGroups.get(primaryType)!.push(card);
    });
    
    // Convert to columns in logical order
    return typeOrderConfig
      .filter(type => typeGroups.has(type))
      .map(type => ({
        id: `type-${type.toLowerCase()}`,
        title: type,
        cards: typeGroups.get(type)!,
        sortValue: type
      }));
  }, [typeOrderConfig]);

  // Organize cards into columns based on sort criteria
  const organizedColumns = useMemo((): ColumnData[] => {
    console.log(`🏗️ Organizing ${cards.length} cards by ${sortCriteria} for ${zone}`);
    
    try {
      switch (sortCriteria) {
        case 'mana':
          return organizeByManaValue(cards);
        case 'color':
          return organizeByColor(cards);  
        case 'rarity':
          return organizeByRarity(cards);
        case 'type':
          return organizeByType(cards);
        default:
          console.warn(`Unknown sort criteria: ${sortCriteria}, defaulting to mana`);
          return organizeByManaValue(cards);
      }
    } catch (error) {
      console.error('Error organizing cards:', error);
      return [];
    }
  }, [cards, sortCriteria, zone, organizeByManaValue, organizeByColor, organizeByRarity, organizeByType]);

  // Sort criteria is now managed externally - clear manual arrangements when it changes
  React.useEffect(() => {
    setManualArrangements(new Map());
  }, [sortCriteria]);

  // Handle manual card movement between columns
  const handleManualMove = useCallback((cardId: string, fromColumnId: string, toColumnId: string) => {
    if (!cardId || !fromColumnId || !toColumnId) {
      console.warn('Invalid manual move parameters');
      return;
    }
    
    console.log(`🔄 Manual move: ${cardId} from ${fromColumnId} to ${toColumnId}`);
    setManualArrangements(prev => {
      const newArrangements = new Map(prev);
      newArrangements.set(cardId, toColumnId);
      return newArrangements;
    });
  }, []);

  // Apply manual arrangements to organized columns
  const finalColumns = useMemo((): (ColumnData & { isEmpty?: boolean })[] => {
    try {
      if (manualArrangements.size === 0) {
        // No manual arrangements, add empty column at the end
        return [...organizedColumns, {
          id: 'empty-column',
          title: '',
          cards: [],
          sortValue: 999,
          isEmpty: true
        }];
      }
      
      // Apply manual arrangements
      const columnsWithManual = organizedColumns.map(column => ({
        ...column,
        cards: column.cards.filter(card => !manualArrangements.has(getCardId(card)))
      }));
      
      // Add manually arranged cards to their designated columns
      manualArrangements.forEach((targetColumnId, cardId) => {
        const card = cards.find(c => getCardId(c) === cardId);
        if (card) {
          let targetColumn = columnsWithManual.find(col => col.id === targetColumnId);
          if (!targetColumn) {
            // Create new column if it doesn't exist
            targetColumn = {
              id: targetColumnId,
              title: 'Manual',
              cards: [],
              sortValue: 998
            };
            columnsWithManual.push(targetColumn);
          }
          targetColumn.cards.push(card);
        }
      });
      
      // Add empty column at the end
      return [...columnsWithManual, {
        id: 'empty-column',
        title: '',
        cards: [],
        sortValue: 999,
        isEmpty: true
      }];
    } catch (error) {
      console.error('Error applying manual arrangements:', error);
      return [...organizedColumns, {
        id: 'empty-column',
        title: '',
        cards: [],
        sortValue: 999,
        isEmpty: true
      }];
    }
  }, [organizedColumns, manualArrangements, cards]);

  // PERFORMANCE FIX: Memoize column rendering to prevent unnecessary re-renders
  const renderedColumns = useMemo(() => {
    return finalColumns.map(column => (
      <PileColumn
        key={column.id}
        columnId={column.id}
        title={column.isEmpty ? '' : `${column.title}${column.cards.length > 0 ? ` (${column.cards.length})` : ''}`}
        cards={column.cards}
        zone={zone}
        scaleFactor={scaleFactor}
        isEmpty={column.isEmpty}
        // Pass through all interaction handlers
        onClick={onClick}
        onInstanceClick={onInstanceClick}        onEnhancedDoubleClick={onEnhancedDoubleClick}
        onRightClick={onRightClick}
        onDragStart={onDragStart}
        isSelected={isSelected}
        selectedCards={selectedCards}
        isDragActive={isDragActive}
        onDragEnter={onDragEnter}
        onDragLeave={onDragLeave}
        canDropInZone={canDropInZone}
        onManualMove={handleManualMove}
      />
    ));
  }, [finalColumns, zone, scaleFactor, onClick, onInstanceClick, onEnhancedDoubleClick, onRightClick, onDragStart, isSelected, selectedCards, isDragActive, onDragEnter, onDragLeave, canDropInZone, handleManualMove]);

  return (
    <div className="pile-view">
      {/* Pile Columns Container - Sort controls now in parent header */}
      <div className="pile-columns-container">
        {renderedColumns}
      </div>
    </div>
  );
};

export default PileView;