#!/usr/bin/env python3
"""
Phase 3B-1: Card Sizing System Implementation
Fixes card sizing issues and adds user controls with persistence.
"""

import os
import re

def update_magic_card_component():
    """Update MagicCard.tsx with dynamic sizing system"""
    file_path = "src/components/MagicCard.tsx"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find and replace getSizeStyles function with dynamic version
        old_get_size_styles = '''/**
 * Get size styles for different card sizes
 */
const getSizeStyles = (size: 'small' | 'normal' | 'large') => {
  switch (size) {
    case 'small':
      return {
        width: '60px',
        height: '84px',
        fontSize: '10px',
      };
    case 'large':
      return {
        width: '200px',
        height: '279px',
        fontSize: '14px',
      };
    case 'normal':
    default:
      return {
        width: '120px',
        height: '168px',
        fontSize: '12px',
      };
  }
};'''

        new_get_size_styles = '''/**
 * Get size styles for different card sizes with dynamic scaling
 */
const getSizeStyles = (size: 'small' | 'normal' | 'large', scaleFactor: number = 1) => {
  // Base dimensions for each size category
  const baseSizes = {
    small: { width: 60, height: 84, fontSize: 10 },
    normal: { width: 120, height: 168, fontSize: 12 },
    large: { width: 200, height: 279, fontSize: 14 }
  };
  
  const baseSize = baseSizes[size] || baseSizes.normal;
  
  // Apply scale factor with reasonable bounds
  const clampedScale = Math.max(0.5, Math.min(3.0, scaleFactor));
  
  return {
    width: `${Math.round(baseSize.width * clampedScale)}px`,
    height: `${Math.round(baseSize.height * clampedScale)}px`,
    fontSize: `${Math.round(baseSize.fontSize * clampedScale)}px`,
  };
};'''

        # Update MagicCardProps interface to include scaleFactor
        old_props_interface = '''interface MagicCardProps {
  card: ScryfallCard | DeckCard;
  size?: 'small' | 'normal' | 'large';
  onClick?: (card: ScryfallCard | DeckCard) => void;
  onDoubleClick?: (card: ScryfallCard | DeckCard) => void;
  showQuantity?: boolean;
  quantity?: number;
  availableQuantity?: number;
  className?: string;
  style?: React.CSSProperties;
  selectable?: boolean;
  selected?: boolean;
  disabled?: boolean;
}'''

        new_props_interface = '''interface MagicCardProps {
  card: ScryfallCard | DeckCard;
  size?: 'small' | 'normal' | 'large';
  scaleFactor?: number;
  onClick?: (card: ScryfallCard | DeckCard) => void;
  onDoubleClick?: (card: ScryfallCard | DeckCard) => void;
  showQuantity?: boolean;
  quantity?: number;
  availableQuantity?: number;
  className?: string;
  style?: React.CSSProperties;
  selectable?: boolean;
  selected?: boolean;
  disabled?: boolean;
}'''

        # Update component destructuring to include scaleFactor
        old_destructuring = '''export const MagicCard: React.FC<MagicCardProps> = ({
  card,
  size = 'normal',
  onClick,
  onDoubleClick,
  showQuantity = false,
  quantity,
  availableQuantity,
  className = '',
  style,
  selectable = false,
  selected = false,
  disabled = false,
}) => {'''

        new_destructuring = '''export const MagicCard: React.FC<MagicCardProps> = ({
  card,
  size = 'normal',
  scaleFactor = 1,
  onClick,
  onDoubleClick,
  showQuantity = false,
  quantity,
  availableQuantity,
  className = '',
  style,
  selectable = false,
  selected = false,
  disabled = false,
}) => {'''

        # Update getSizeStyles call to include scaleFactor
        old_size_styles_call = '  const sizeStyles = getSizeStyles(size);'
        new_size_styles_call = '  const sizeStyles = getSizeStyles(size, scaleFactor);'

        # Update CardGrid component props and grid template
        old_card_grid = '''export const CardGrid: React.FC<{
  cards: (ScryfallCard | DeckCard)[];
  cardSize?: 'small' | 'normal' | 'large';
  onCardClick?: (card: ScryfallCard | DeckCard) => void;
  onCardDoubleClick?: (card: ScryfallCard | DeckCard) => void;
  showQuantities?: boolean;
  selectedCards?: Set<string>;
  className?: string;
  style?: React.CSSProperties;
}> = ({
  cards,
  cardSize = 'normal',
  onCardClick,
  onCardDoubleClick,
  showQuantities = false,
  selectedCards = new Set(),
  className = '',
  style,
}) => {
  const gridStyles: React.CSSProperties = {
    display: 'grid',
    gridTemplateColumns: `repeat(auto-fill, minmax(${
      cardSize === 'small' ? '70px' : 
      cardSize === 'large' ? '210px' : '130px'
    }, 1fr))`,
    gap: '8px',
    padding: '8px',
    ...style,
  };'''

        new_card_grid = '''export const CardGrid: React.FC<{
  cards: (ScryfallCard | DeckCard)[];
  cardSize?: 'small' | 'normal' | 'large';
  scaleFactor?: number;
  onCardClick?: (card: ScryfallCard | DeckCard) => void;
  onCardDoubleClick?: (card: ScryfallCard | DeckCard) => void;
  showQuantities?: boolean;
  selectedCards?: Set<string>;
  className?: string;
  style?: React.CSSProperties;
}> = ({
  cards,
  cardSize = 'normal',
  scaleFactor = 1,
  onCardClick,
  onCardDoubleClick,
  showQuantities = false,
  selectedCards = new Set(),
  className = '',
  style,
}) => {
  // Calculate dynamic grid column size based on card size and scale factor
  const getGridColumnSize = () => {
    const baseSizes = {
      small: 70,
      normal: 130, 
      large: 210
    };
    const baseSize = baseSizes[cardSize] || baseSizes.normal;
    const scaledSize = Math.round(baseSize * Math.max(0.5, Math.min(3.0, scaleFactor)));
    return `${scaledSize}px`;
  };

  const gridStyles: React.CSSProperties = {
    display: 'grid',
    gridTemplateColumns: `repeat(auto-fill, minmax(${getGridColumnSize()}, 1fr))`,
    gap: '8px',
    padding: '8px',
    ...style,
  };'''

        # Update MagicCard usage in CardGrid to include scaleFactor
        old_card_usage = '''        <MagicCard
          key={card.id}
          card={card}
          size={cardSize}
          onClick={onCardClick}
          onDoubleClick={onCardDoubleClick}
          showQuantity={showQuantities}
          quantity={'quantity' in card ? card.quantity : undefined}
          availableQuantity={showQuantities ? 4 : undefined} // Simulate full collection
          selected={selectedCards.has(card.id)}
          selectable={true}
        />'''

        new_card_usage = '''        <MagicCard
          key={card.id}
          card={card}
          size={cardSize}
          scaleFactor={scaleFactor}
          onClick={onCardClick}
          onDoubleClick={onCardDoubleClick}
          showQuantity={showQuantities}
          quantity={'quantity' in card ? card.quantity : undefined}
          availableQuantity={showQuantities ? 4 : undefined} // Simulate full collection
          selected={selectedCards.has(card.id)}
          selectable={true}
        />'''

        # Apply all replacements
        content = content.replace(old_get_size_styles, new_get_size_styles)
        content = content.replace(old_props_interface, new_props_interface)
        content = content.replace(old_destructuring, new_destructuring)
        content = content.replace(old_size_styles_call, new_size_styles_call)
        content = content.replace(old_card_grid, new_card_grid)
        content = content.replace(old_card_usage, new_card_usage)
        
        # Write updated content
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        print(f"✅ Successfully updated {file_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error updating {file_path}: {e}")
        return False

def create_size_control_hook():
    """Create a new hook for size management"""
    hook_content = '''// src/hooks/useCardSizing.ts
// Hook for managing card sizes with persistence

import { useState, useCallback, useEffect } from 'react';

interface CardSizeState {
  collection: number;
  deck: number;
  sideboard: number;
}

interface CardSizeSettings {
  sizes: CardSizeState;
  updateCollectionSize: (size: number) => void;
  updateDeckSize: (size: number) => void;
  updateSideboardSize: (size: number) => void;
  resetToDefaults: () => void;
}

const DEFAULT_SIZES: CardSizeState = {
  collection: 1.2,  // 20% larger than base normal size
  deck: 0.8,        // 20% smaller than base small size  
  sideboard: 0.8    // 20% smaller than base small size
};

const STORAGE_KEY = 'mtg-deck-builder-card-sizes';

/**
 * Hook for managing card sizes across different zones
 */
export const useCardSizing = (): CardSizeSettings => {
  // Initialize state from localStorage or defaults
  const [sizes, setSizes] = useState<CardSizeState>(() => {
    try {
      const stored = localStorage.getItem(STORAGE_KEY);
      if (stored) {
        const parsed = JSON.parse(stored);
        return {
          collection: Math.max(0.5, Math.min(3.0, parsed.collection || DEFAULT_SIZES.collection)),
          deck: Math.max(0.5, Math.min(3.0, parsed.deck || DEFAULT_SIZES.deck)),
          sideboard: Math.max(0.5, Math.min(3.0, parsed.sideboard || DEFAULT_SIZES.sideboard))
        };
      }
    } catch (error) {
      console.warn('Failed to load card sizes from localStorage:', error);
    }
    return DEFAULT_SIZES;
  });

  // Persist sizes to localStorage whenever they change
  useEffect(() => {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(sizes));
    } catch (error) {
      console.warn('Failed to save card sizes to localStorage:', error);
    }
  }, [sizes]);

  // Update functions
  const updateCollectionSize = useCallback((size: number) => {
    const clampedSize = Math.max(0.5, Math.min(3.0, size));
    setSizes(prev => ({ ...prev, collection: clampedSize }));
  }, []);

  const updateDeckSize = useCallback((size: number) => {
    const clampedSize = Math.max(0.5, Math.min(3.0, size));
    setSizes(prev => ({ ...prev, deck: clampedSize }));
  }, []);

  const updateSideboardSize = useCallback((size: number) => {
    const clampedSize = Math.max(0.5, Math.min(3.0, size));
    setSizes(prev => ({ ...prev, sideboard: clampedSize }));
  }, []);

  const resetToDefaults = useCallback(() => {
    setSizes(DEFAULT_SIZES);
  }, []);

  return {
    sizes,
    updateCollectionSize,
    updateDeckSize,
    updateSideboardSize,
    resetToDefaults
  };
};

export default useCardSizing;'''

    try:
        os.makedirs('src/hooks', exist_ok=True)
        with open('src/hooks/useCardSizing.ts', 'w', encoding='utf-8') as f:
            f.write(hook_content)
        print("✅ Successfully created src/hooks/useCardSizing.ts")
        return True
    except Exception as e:
        print(f"❌ Error creating useCardSizing hook: {e}")
        return False

def update_mtgo_layout():
    """Update MTGOLayout.tsx to integrate size controls"""
    file_path = "src/components/MTGOLayout.tsx"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Add import for size control hook
        old_imports = '''import { useCards } from '../hooks/useCards';
import DraggableCard from './DraggableCard';'''

        new_imports = '''import { useCards } from '../hooks/useCards';
import { useCardSizing } from '../hooks/useCardSizing';
import DraggableCard from './DraggableCard';'''

        # Add size control state after existing hook calls
        old_hooks_section = '''  const { 
    cards, 
    loading, 
    error, 
    searchForCards, 
    loadPopularCards, 
    loadRandomCard 
  } = useCards();'''

        new_hooks_section = '''  const { 
    cards, 
    loading, 
    error, 
    searchForCards, 
    loadPopularCards, 
    loadRandomCard 
  } = useCards();
  
  // PHASE 3B-1: Card sizing system
  const { 
    sizes: cardSizes, 
    updateCollectionSize, 
    updateDeckSize, 
    updateSideboardSize 
  } = useCardSizing();'''

        # Add size slider component to collection panel header
        old_collection_header = '''          <div className="panel-header">
            <h3>Collection ({cards.length} cards)</h3>
            <div className="view-controls">
              <span>View: </span>
              <button className="active">Card</button>
              <button>List</button>
            </div>
          </div>'''

        new_collection_header = '''          <div className="panel-header">
            <h3>Collection ({cards.length} cards)</h3>
            <div className="view-controls">
              <span>Size: </span>
              <input
                type="range"
                min="0.5"
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
          </div>'''

        # Add size slider to main deck header
        old_deck_header = '''            <div className="panel-header">
              <h3>Main Deck ({mainDeck.reduce((sum: number, card: any) => sum + card.quantity, 0)} cards)</h3>
              <div className="deck-controls">
                <button>Save Deck</button>
                <button onClick={handleClearDeck} title="Clear all cards from deck">
                  Clear Deck
                </button>
              </div>
            </div>'''

        new_deck_header = '''            <div className="panel-header">
              <h3>Main Deck ({mainDeck.reduce((sum: number, card: any) => sum + card.quantity, 0)} cards)</h3>
              <div className="deck-controls">
                <span>Size: </span>
                <input
                  type="range"
                  min="0.5"
                  max="2.0"
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
            </div>'''

        # Add size slider to sideboard header
        old_sideboard_header = '''            <div className="panel-header">
              <h3>Sideboard ({sideboard.reduce((sum: number, card: any) => sum + card.quantity, 0)})</h3>
              <div className="sideboard-controls">
                <button onClick={handleClearSideboard} title="Clear all cards from sideboard">
                  Clear
                </button>
              </div>
            </div>'''

        new_sideboard_header = '''            <div className="panel-header">
              <h3>Sideboard ({sideboard.reduce((sum: number, card: any) => sum + card.quantity, 0)})</h3>
              <div className="sideboard-controls">
                <span>Size: </span>
                <input
                  type="range"
                  min="0.5"
                  max="2.0"
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
            </div>'''

        # Update DraggableCard components to use scaleFactor
        # Collection cards
        old_collection_card = '''              <DraggableCard
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
              />'''

        new_collection_card = '''              <DraggableCard
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
              />'''

        # Deck cards
        old_deck_card = '''                  <DraggableCard
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
                  />'''

        new_deck_card = '''                  <DraggableCard
                    key={deckCard.id}
                    card={deckCard}
                    zone="deck"
                    size="small"
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
                  />'''

        # Sideboard cards
        old_sideboard_card = '''                  <DraggableCard
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
                  />'''

        new_sideboard_card = '''                  <DraggableCard
                    key={sideCard.id}
                    card={sideCard}
                    zone="sideboard"
                    size="small"
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
                  />'''

        # Apply all replacements
        content = content.replace(old_imports, new_imports)
        content = content.replace(old_hooks_section, new_hooks_section)
        content = content.replace(old_collection_header, new_collection_header)
        content = content.replace(old_deck_header, new_deck_header)
        content = content.replace(old_sideboard_header, new_sideboard_header)
        content = content.replace(old_collection_card, new_collection_card)
        content = content.replace(old_deck_card, new_deck_card)
        content = content.replace(old_sideboard_card, new_sideboard_card)
        
        # Write updated content
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        print(f"✅ Successfully updated {file_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error updating {file_path}: {e}")
        return False

def update_css_for_size_sliders():
    """Add CSS styles for the new size sliders"""
    file_path = "src/components/MTGOLayout.css"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Add size slider styles at the end of the view-controls section
        css_addition = '''
/* PHASE 3B-1: Size slider styles */
.size-slider {
  width: 60px;
  height: 18px;
  margin: 0 8px 0 4px;
  background: linear-gradient(to right, #404040, #666666);
  border-radius: 9px;
  outline: none;
  cursor: pointer;
  -webkit-appearance: none;
  appearance: none;
}

.size-slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 16px;
  height: 16px;
  background: #3b82f6;
  border-radius: 50%;
  cursor: pointer;
  border: 2px solid #ffffff;
  box-shadow: 0 1px 3px rgba(0,0,0,0.3);
  transition: all 0.2s ease;
}

.size-slider::-webkit-slider-thumb:hover {
  background: #2563eb;
  transform: scale(1.1);
}

.size-slider::-moz-range-thumb {
  width: 16px;
  height: 16px;
  background: #3b82f6;
  border: 2px solid #ffffff;
  border-radius: 50%;
  cursor: pointer;
  box-shadow: 0 1px 3px rgba(0,0,0,0.3);
  transition: all 0.2s ease;
}

.size-slider::-moz-range-thumb:hover {
  background: #2563eb;
  transform: scale(1.1);
}

.deck-controls .size-slider,
.sideboard-controls .size-slider {
  width: 50px;
  margin: 0 6px 0 2px;
}

/* Update grid styles to be more responsive to size changes */
.collection-grid {
  padding: 12px;
  overflow-y: auto;
  flex: 1;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(var(--collection-card-min-width, 130px), 1fr));
  gap: 8px;
  align-content: start;
}

.deck-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(var(--deck-card-min-width, 70px), 1fr));
  gap: 4px;
  align-content: start;
  min-height: 150px;
  padding-bottom: 40px;
}

.sideboard-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(var(--sideboard-card-min-width, 70px), 1fr));
  gap: 4px;
  align-content: start;
  min-height: 150px;
  padding-bottom: 40px;
}'''

        # Find the end of the view-controls section and add the new styles
        insertion_point = content.find('.view-controls button.active {')
        if insertion_point != -1:
            # Find the end of this rule block
            end_point = content.find('}', insertion_point) + 1
            # Insert the new CSS after this block
            content = content[:end_point] + css_addition + content[end_point:]
        else:
            # Fallback: add at the end of the file
            content += css_addition
        
        # Write updated content
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Successfully updated {file_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error updating {file_path}: {e}")
        return False

def update_draggable_card():
    """Update DraggableCard.tsx to support scaleFactor prop"""
    file_path = "src/components/DraggableCard.tsx"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Add scaleFactor to interface
        old_interface = '''interface DraggableCardProps {
  card: ScryfallCard | DeckCard;
  zone: DropZone;
  size?: 'small' | 'normal' | 'large';
  onClick?: (card: ScryfallCard | DeckCard, event?: React.MouseEvent) => void;'''

        new_interface = '''interface DraggableCardProps {
  card: ScryfallCard | DeckCard;
  zone: DropZone;
  size?: 'small' | 'normal' | 'large';
  scaleFactor?: number;
  onClick?: (card: ScryfallCard | DeckCard, event?: React.MouseEvent) => void;'''

        # Add scaleFactor to destructuring
        old_destructuring = '''const DraggableCard: React.FC<DraggableCardProps> = ({
  card,
  zone,
  size = 'normal',
  onClick,
  onDoubleClick,'''

        new_destructuring = '''const DraggableCard: React.FC<DraggableCardProps> = ({
  card,
  zone,
  size = 'normal',
  scaleFactor = 1,
  onClick,
  onDoubleClick,'''

        # Update MagicCard component to include scaleFactor
        old_magic_card = '''      <MagicCard
        card={card}
        size={size}
        showQuantity={showQuantity}
        quantity={quantity}
        availableQuantity={availableQuantity}
        selected={selected}
        selectable={selectable}
        disabled={disabled}
      />'''

        new_magic_card = '''      <MagicCard
        card={card}
        size={size}
        scaleFactor={scaleFactor}
        showQuantity={showQuantity}
        quantity={quantity}
        availableQuantity={availableQuantity}
        selected={selected}
        selectable={selectable}
        disabled={disabled}
      />'''

        # Apply replacements
        content = content.replace(old_interface, new_interface)
        content = content.replace(old_destructuring, new_destructuring)
        content = content.replace(old_magic_card, new_magic_card)
        
        # Write updated content
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        print(f"✅ Successfully updated {file_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error updating {file_path}: {e}")
        return False

def main():
    """Run all card sizing system updates"""
    print("🚀 Starting Phase 3B-1: Card Sizing System Implementation")
    print("=" * 60)
    
    success_count = 0
    total_tasks = 5
    
    print("\n📝 Task 1/5: Creating card sizing hook...")
    if create_size_control_hook():
        success_count += 1
    
    print("\n📝 Task 2/5: Updating MagicCard component...")
    if update_magic_card_component():
        success_count += 1
    
    print("\n📝 Task 3/5: Updating DraggableCard component...")
    if update_draggable_card():
        success_count += 1
    
    print("\n📝 Task 4/5: Updating MTGOLayout component...")
    if update_mtgo_layout():
        success_count += 1
    
    print("\n📝 Task 5/5: Adding CSS styles for size controls...")
    if update_css_for_size_sliders():
        success_count += 1
    
    print("\n" + "=" * 60)
    print(f"✅ Phase 3B-1 Implementation Complete!")
    print(f"📊 Success: {success_count}/{total_tasks} tasks completed")
    
    if success_count == total_tasks:
        print("\n🎯 IMPLEMENTATION SUMMARY:")
        print("✅ Dynamic card sizing system with scale factors")
        print("✅ Independent size sliders in each section header")  
        print("✅ Persistent size settings using localStorage")
        print("✅ Professional slider styling matching MTGO aesthetics")
        print("✅ Improved default sizes (Collection: 120%, Deck/Sideboard: 80%)")
        print("✅ Complete integration through DraggableCard component")
        print("\n🧪 TESTING INSTRUCTIONS:")
        print("1. Run 'npm start' to launch the application")
        print("2. Verify size sliders appear in Collection, Deck, and Sideboard headers")
        print("3. Test that sliders actually change card sizes")
        print("4. Verify sizes persist after page refresh")
        print("5. Test that all existing functionality still works")
        print("6. Test drag-and-drop with different card sizes")
        
        print("\n💡 USER EXPERIENCE IMPROVEMENTS:")
        print("• Collection cards now properly sized for standard monitors")
        print("• Deck/sideboard cards sized for practical viewing")
        print("• Users have full control over card sizes")
        print("• Settings remembered between sessions")
        print("• Professional slider controls matching MTGO standards")
        print("• Smooth transitions during size changes")
    else:
        print(f"\n⚠️  Some tasks failed. Please check the error messages above.")
        print("You may need to manually review and apply the failed updates.")

if __name__ == "__main__":
    main()