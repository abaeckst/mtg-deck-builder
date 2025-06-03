# PileView Individual Selection Fix - File Update Script
# This script updates PileView and PileColumn components to support instance-based selection
# while maintaining the visual stacking behavior and adding selection clearing on view switches.

import os
import sys

def find_and_replace_file(file_path, replacements):
    """Apply multiple find-and-replace operations to a file"""
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return False
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        original_content = content
        
        for find_text, replace_text in replacements:
            if find_text not in content:
                print(f"⚠️ Text not found in {file_path}: {find_text[:50]}...")
                continue
            content = content.replace(find_text, replace_text)
            print(f"✅ Replaced text in {file_path}")
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)
            print(f"✅ Successfully updated {file_path}")
            return True
        else:
            print(f"⚠️ No changes made to {file_path}")
            return False
            
    except Exception as e:
        print(f"❌ Error updating {file_path}: {e}")
        return False

def main():
    """Main function to apply all pile view individual selection fixes"""
    print("🚀 Starting PileView Individual Selection Implementation...")
    
    # Define all the file updates needed
    
    # 1. Update PileColumn.tsx to use instance-based selection and proper rendering
    pile_column_updates = [
        # Update the renderCards function to work with instances properly
        (
            """// MTGO-style card stacking - ALL cards stack together with proper overlap
  const renderCards = useCallback(() => {
    try {
      const renderedCards: React.ReactElement[] = [];
      let cardIndex = 0; // Track position across all cards for proper stacking
      
      cards.forEach(card => {
        // Validate card has required properties
        if (!card || !getCardId(card)) {
          console.warn('Invalid card object:', card);
          return;
        }

        // Get quantity for this card
        let cardQuantity = 1;
        if (typeof card === 'object' && card !== null) {
          if ('instanceId' in card) {
            // DeckCardInstance - each instance represents 1 copy
            cardQuantity = 1;
          } else if ('quantity' in card && typeof card.quantity === 'number' && card.quantity > 0) {
            // DeckCard - use quantity property
            cardQuantity = card.quantity;
          }
        }

        // Create individual draggable cards for each copy (MTGO-style stacking)
        for (let i = 0; i < cardQuantity; i++) {
          // MTGO-style tight stacking - show ~15% of each card (name area visible)
          // Typical card is ~180px tall, we want ~27px showing = 85% overlap
          const cardHeight = Math.round(180 * scaleFactor); // Estimated card height at current scale
          const visiblePortion = Math.round(cardHeight * 0.14); // Show 14% of card (name area)
          const stackOffset = -(cardHeight - visiblePortion); // Negative offset to stack tightly
          
          renderedCards.push(
            <div
              key={`${"instanceId" in card ? card.instanceId : card.id}-${i}`}
              className="pile-card-stack-item"
              style={{
                marginTop: cardIndex > 0 ? `${stackOffset}px` : '0px', // Stack ALL cards, not just same card
                zIndex: cardIndex, // Last card has highest z-index (most visible), first card lowest
                position: 'relative',
              }}
            >
              <DraggableCard
                card={card}
                zone={zone}
                size="normal"
                scaleFactor={scaleFactor}
                onClick={onClick}
                onDoubleClick={onDoubleClick}
                onEnhancedDoubleClick={onEnhancedDoubleClick}
                onRightClick={onRightClick}
                onDragStart={onDragStart}
                showQuantity={false} // Don't show quantity on individual cards
                quantity={1} // Each rendered card represents 1 copy
                selected={isSelected ? isSelected(getSelectionId(card)) : false}
                selectable={true}
                isDragActive={isDragActive}
                isBeingDragged={isDragActive && selectedCards.some(sc => getCardId(sc) === getCardId(card))}
                selectedCards={selectedCards}
              />
            </div>
          );
          
          cardIndex++; // Increment for next card in stack
        }
      });
      
      return renderedCards;
    } catch (error) {
      console.error('Error rendering cards in pile column:', error);
      return [<div key="error" className="error-message">Error rendering cards</div>];
    }
  }, [cards, zone, scaleFactor, onClick, onDoubleClick, onEnhancedDoubleClick, onRightClick, onDragStart, isSelected, selectedCards, isDragActive]);""",
            """// MTGO-style card stacking - optimized for instance-based selection
  const renderCards = useCallback(() => {
    try {
      const renderedCards: React.ReactElement[] = [];
      let cardIndex = 0; // Track position across all cards for proper stacking
      
      cards.forEach(card => {
        // Validate card has required properties
        if (!card || !getCardId(card)) {
          console.warn('Invalid card object:', card);
          return;
        }

        // For instances, render each one individually
        // For legacy cards with quantity, render multiple copies
        let cardQuantity = 1;
        if (typeof card === 'object' && card !== null) {
          if ('instanceId' in card) {
            // DeckCardInstance - each instance represents 1 copy
            cardQuantity = 1;
          } else if ('quantity' in card && typeof card.quantity === 'number' && card.quantity > 0) {
            // DeckCard - use quantity property
            cardQuantity = card.quantity;
          }
        }

        // Create individual draggable cards for each copy (MTGO-style stacking)
        for (let i = 0; i < cardQuantity; i++) {
          // MTGO-style tight stacking - show ~15% of each card (name area visible)
          // Typical card is ~180px tall, we want ~27px showing = 85% overlap
          const cardHeight = Math.round(180 * scaleFactor); // Estimated card height at current scale
          const visiblePortion = Math.round(cardHeight * 0.14); // Show 14% of card (name area)
          const stackOffset = -(cardHeight - visiblePortion); // Negative offset to stack tightly
          
          // Determine if this is an instance card and use appropriate selection logic
          const isInstance = 'instanceId' in card;
          const selectionId = isInstance ? card.instanceId : `${card.id}-${i}`;
          
          renderedCards.push(
            <div
              key={selectionId}
              className="pile-card-stack-item"
              style={{
                marginTop: cardIndex > 0 ? `${stackOffset}px` : '0px', // Stack ALL cards, not just same card
                zIndex: cardIndex, // Last card has highest z-index (most visible), first card lowest
                position: 'relative',
              }}
            >
              <DraggableCard
                card={card}
                zone={zone}
                size="normal"
                scaleFactor={scaleFactor}
                onClick={isInstance ? undefined : onClick} // Use instance click for instances
                onInstanceClick={isInstance ? onClick : undefined} // Pass instance click handler
                instanceId={isInstance ? card.instanceId : undefined}
                isInstance={isInstance}
                onDoubleClick={onDoubleClick}
                onEnhancedDoubleClick={onEnhancedDoubleClick}
                onRightClick={onRightClick}
                onDragStart={onDragStart}
                showQuantity={false} // Don't show quantity on individual cards
                quantity={1} // Each rendered card represents 1 copy
                selected={isSelected ? isSelected(selectionId) : false}
                selectable={true}
                isDragActive={isDragActive}
                isBeingDragged={isDragActive && selectedCards.some(sc => {
                  if (isInstance) {
                    return 'instanceId' in sc ? sc.instanceId === card.instanceId : false;
                  } else {
                    return getCardId(sc) === getCardId(card);
                  }
                })}
                selectedCards={selectedCards}
              />
            </div>
          );
          
          cardIndex++; // Increment for next card in stack
        }
      });
      
      return renderedCards;
    } catch (error) {
      console.error('Error rendering cards in pile column:', error);
      return [<div key="error" className="error-message">Error rendering cards</div>];
    }
  }, [cards, zone, scaleFactor, onClick, onDoubleClick, onEnhancedDoubleClick, onRightClick, onDragStart, isSelected, selectedCards, isDragActive]);"""
        )
    ]
    
    # 2. Update PileView.tsx to properly pass through instances instead of grouping
    pile_view_updates = [
        # Update the interface to better handle instances
        (
            """interface PileViewProps {
  cards: (ScryfallCard | DeckCard | DeckCardInstance)[];
  zone: 'deck' | 'sideboard';
  scaleFactor: number;
  forcedSortCriteria?: PileSortCriteria; // External sort control from parent
  // Existing card interaction handlers from MTGOLayout
  onClick?: (card: ScryfallCard | DeckCard | DeckCardInstance, event?: React.MouseEvent) => void;
  onDoubleClick?: (card: ScryfallCard | DeckCard | DeckCardInstance) => void;
  onEnhancedDoubleClick?: (card: ScryfallCard | DeckCard | DeckCardInstance, zone: DropZone, event: React.MouseEvent) => void;
  onRightClick?: (card: ScryfallCard | DeckCard | DeckCardInstance, zone: DropZone, event: React.MouseEvent) => void;
  onDragStart?: (cards: (ScryfallCard | DeckCard | DeckCardInstance)[], zone: DropZone, event: React.MouseEvent) => void;
  // Selection and drag state
  isSelected?: (cardId: string) => boolean;
  selectedCards?: (ScryfallCard | DeckCard | DeckCardInstance)[];
  isDragActive?: boolean;
  // Drop zone handlers
  onDragEnter?: (zone: DropZone, canDrop: boolean) => void;
  onDragLeave?: () => void;
  canDropInZone?: (zone: DropZone, cards: (ScryfallCard | DeckCard)[]) => boolean;
}""",
            """interface PileViewProps {
  cards: (ScryfallCard | DeckCard | DeckCardInstance)[];
  zone: 'deck' | 'sideboard';
  scaleFactor: number;
  forcedSortCriteria?: PileSortCriteria; // External sort control from parent
  // Enhanced card interaction handlers - now supporting both card and instance clicks
  onClick?: (card: ScryfallCard | DeckCard | DeckCardInstance, event?: React.MouseEvent) => void;
  onInstanceClick?: (instanceId: string, instance: DeckCardInstance, event: React.MouseEvent) => void;
  onDoubleClick?: (card: ScryfallCard | DeckCard | DeckCardInstance) => void;
  onEnhancedDoubleClick?: (card: ScryfallCard | DeckCard | DeckCardInstance, zone: DropZone, event: React.MouseEvent) => void;
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
}"""
        ),
        # Update the component props destructuring to include onInstanceClick
        (
            """const PileView: React.FC<PileViewProps> = ({
  cards,
  zone,
  scaleFactor,
  forcedSortCriteria,
  onClick,
  onDoubleClick,
  onEnhancedDoubleClick,
  onRightClick,
  onDragStart,
  isSelected = () => false,
  selectedCards = [],
  isDragActive = false,
  onDragEnter,
  onDragLeave,
  canDropInZone,
}) => {""",
            """const PileView: React.FC<PileViewProps> = ({
  cards,
  zone,
  scaleFactor,
  forcedSortCriteria,
  onClick,
  onInstanceClick,
  onDoubleClick,
  onEnhancedDoubleClick,
  onRightClick,
  onDragStart,
  isSelected = () => false,
  selectedCards = [],
  isDragActive = false,
  onDragEnter,
  onDragLeave,
  canDropInZone,
}) => {"""
        ),
        # Update the PileColumn props to pass the new handlers
        (
            """        // Pass through all interaction handlers
        onClick={onClick}
        onDoubleClick={onDoubleClick}
        onEnhancedDoubleClick={onEnhancedDoubleClick}
        onRightClick={onRightClick}
        onDragStart={onDragStart}
        isSelected={isSelected}
        selectedCards={selectedCards}
        isDragActive={isDragActive}
        onDragEnter={onDragEnter}
        onDragLeave={onDragLeave}
        canDropInZone={canDropInZone}
        onManualMove={handleManualMove}""",
            """        // Pass through all interaction handlers including instance support
        onClick={onInstanceClick || onClick} // Prefer instance click for deck/sideboard
        onDoubleClick={onDoubleClick}
        onEnhancedDoubleClick={onEnhancedDoubleClick}
        onRightClick={onRightClick}
        onDragStart={onDragStart}
        isSelected={isSelected}
        selectedCards={selectedCards}
        isDragActive={isDragActive}
        onDragEnter={onDragEnter}
        onDragLeave={onDragLeave}
        canDropInZone={canDropInZone}
        onManualMove={handleManualMove}"""
        )
    ]
    
    # 3. Update MTGOLayout.tsx to add selection clearing on view switch and proper PileView integration
    mtgo_layout_updates = [
        # Add selection clearing when view modes change
        (
            """  // Update view modes
  const updateViewMode = useCallback((area: keyof LayoutState['viewModes'], mode: string) => {
    setLayout(prev => {
      const newLayout = {
        ...prev,
        viewModes: {
          ...prev.viewModes,
          [area]: mode,
        },
      };
      saveLayout(newLayout);
      return newLayout;
    });
  }, [saveLayout]);""",
            """  // Update view modes with selection clearing
  const updateViewModeWithClearSelection = useCallback((area: keyof LayoutState['viewModes'], mode: string) => {
    // Clear selections when switching view modes for better UX
    clearSelection();
    
    setLayout(prev => {
      const newLayout = {
        ...prev,
        viewModes: {
          ...prev.viewModes,
          [area]: mode,
        },
      };
      saveLayout(newLayout);
      return newLayout;
    });
  }, [saveLayout, clearSelection]);"""
        ),
        # Update the view mode button click handlers to use the new function
        (
            """                onClick={() => updateViewMode('collection', 'grid')}""",
            """                onClick={() => updateViewModeWithClearSelection('collection', 'grid')}"""
        ),
        (
            """                onClick={() => updateViewMode('collection', 'list')}""",
            """                onClick={() => updateViewModeWithClearSelection('collection', 'list')}"""
        ),
        (
            """                  onClick={() => updateViewMode('deck', 'card')}""",
            """                  onClick={() => updateViewModeWithClearSelection('deck', 'card')}"""
        ),
        (
            """                  onClick={() => updateViewMode('deck', 'pile')}""",
            """                  onClick={() => updateViewModeWithClearSelection('deck', 'pile')}"""
        ),
        (
            """                  onClick={() => updateViewMode('deck', 'list')}""",
            """                  onClick={() => updateViewModeWithClearSelection('deck', 'list')}"""
        ),
        (
            """                  onClick={() => updateViewMode('sideboard', 'card')}""",
            """                  onClick={() => updateViewModeWithClearSelection('sideboard', 'card')}"""
        ),
        (
            """                  onClick={() => updateViewMode('sideboard', 'pile')}""",
            """                  onClick={() => updateViewModeWithClearSelection('sideboard', 'pile')}"""
        ),
        (
            """                  onClick={() => updateViewMode('sideboard', 'list')}""",
            """                  onClick={() => updateViewModeWithClearSelection('sideboard', 'list')}"""
        ),
        # Update PileView calls to pass onInstanceClick handler
        (
            """                <PileView
                  cards={mainDeck}
                  zone="deck"
                  scaleFactor={cardSizes.deck}
                  forcedSortCriteria={deckSortCriteria === 'name' ? 'mana' : deckSortCriteria}
                  onClick={(card, event) => handleCardClick(card, event)}
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
                />""",
            """                <PileView
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
                />"""
        ),
        (
            """                <PileView
                  cards={sideboard}
                  zone="sideboard"
                  scaleFactor={cardSizes.sideboard}
                  forcedSortCriteria={sideboardSortCriteria === 'name' ? 'mana' : sideboardSortCriteria}
                  onClick={(card, event) => handleCardClick(card, event)}
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
                />""",
            """                <PileView
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
                />"""
        )
    ]
    
    # 4. Update PileColumn.tsx interface to support instance click handlers
    pile_column_interface_updates = [
        (
            """interface PileColumnProps {
  columnId: string;
  title: string;
  cards: (ScryfallCard | DeckCard | DeckCardInstance)[];
  zone: 'deck' | 'sideboard';
  scaleFactor: number;
  isEmpty?: boolean;
  // Card interaction handlers
  onClick?: (card: ScryfallCard | DeckCard | DeckCardInstance, event?: React.MouseEvent) => void;
  onDoubleClick?: (card: ScryfallCard | DeckCard | DeckCardInstance) => void;
  onEnhancedDoubleClick?: (card: ScryfallCard | DeckCard | DeckCardInstance, zone: DropZone, event: React.MouseEvent) => void;
  onRightClick?: (card: ScryfallCard | DeckCard | DeckCardInstance, zone: DropZone, event: React.MouseEvent) => void;
  onDragStart?: (cards: (ScryfallCard | DeckCard | DeckCardInstance)[], zone: DropZone, event: React.MouseEvent) => void;
  // Selection and drag state
  isSelected?: (cardId: string) => boolean;
  selectedCards?: (ScryfallCard | DeckCard | DeckCardInstance)[];
  isDragActive?: boolean;
  // Drop zone handlers
  onDragEnter?: (zone: DropZone, canDrop: boolean) => void;
  onDragLeave?: () => void;
  canDropInZone?: (zone: DropZone, cards: (ScryfallCard | DeckCard)[]) => boolean;
  // Manual movement
  onManualMove?: (cardId: string, fromColumn: string, toColumn: string) => void;
}""",
            """interface PileColumnProps {
  columnId: string;
  title: string;
  cards: (ScryfallCard | DeckCard | DeckCardInstance)[];
  zone: 'deck' | 'sideboard';
  scaleFactor: number;
  isEmpty?: boolean;
  // Enhanced card interaction handlers - supporting both card and instance selection
  onClick?: (card: ScryfallCard | DeckCard | DeckCardInstance, event?: React.MouseEvent) => void;
  onInstanceClick?: (instanceId: string, instance: DeckCardInstance, event: React.MouseEvent) => void;
  onDoubleClick?: (card: ScryfallCard | DeckCard | DeckCardInstance) => void;
  onEnhancedDoubleClick?: (card: ScryfallCard | DeckCard | DeckCardInstance, zone: DropZone, event: React.MouseEvent) => void;
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
  // Manual movement
  onManualMove?: (cardId: string, fromColumn: string, toColumn: string) => void;
}"""
        ),
        # Update the props destructuring
        (
            """const PileColumn: React.FC<PileColumnProps> = ({
  columnId,
  title,
  cards,
  zone,
  scaleFactor,
  isEmpty = false,
  onClick,
  onDoubleClick,
  onEnhancedDoubleClick,
  onRightClick,
  onDragStart,
  isSelected = () => false,
  selectedCards = [],
  isDragActive = false,
  onDragEnter,
  onDragLeave,
  canDropInZone,
  onManualMove,
}) => {""",
            """const PileColumn: React.FC<PileColumnProps> = ({
  columnId,
  title,
  cards,
  zone,
  scaleFactor,
  isEmpty = false,
  onClick,
  onInstanceClick,
  onDoubleClick,
  onEnhancedDoubleClick,
  onRightClick,
  onDragStart,
  isSelected = () => false,
  selectedCards = [],
  isDragActive = false,
  onDragEnter,
  onDragLeave,
  canDropInZone,
  onManualMove,
}) => {"""
        )
    ]
    
    # Apply all updates
    success_count = 0
    total_updates = 4
    
    print("\n📋 Applying PileColumn.tsx individual selection updates...")
    if find_and_replace_file("src/components/PileColumn.tsx", pile_column_updates + pile_column_interface_updates):
        success_count += 1
    
    print("\n📋 Applying PileView.tsx instance-aware updates...")
    if find_and_replace_file("src/components/PileView.tsx", pile_view_updates):
        success_count += 1
    
    print("\n📋 Applying MTGOLayout.tsx selection clearing updates...")
    if find_and_replace_file("src/components/MTGOLayout.tsx", mtgo_layout_updates):
        success_count += 1
    
    # Report results
    print(f"\n🎯 Summary:")
    print(f"✅ Successfully updated: {success_count}/{total_updates} files")
    
    if success_count == total_updates:
        print("\n🚀 All updates completed successfully!")
        print("\n📋 What was implemented:")
        print("✅ PileView now uses instance-based selection for individual cards")
        print("✅ PileColumn renders individual instances with proper stacking")
        print("✅ Selection clearing on view mode switches")
        print("✅ Proper integration with existing instance selection system")
        
        print("\n🧪 Testing checklist:")
        print("1. Test individual card selection in pile view (deck & sideboard)")
        print("2. Test multi-selection with Ctrl+click in pile view")
        print("3. Test selection clearing when switching view modes")
        print("4. Verify visual stacking still works correctly")
        print("5. Test context menus and drag & drop with individual instances")
        
        print("\n🎯 Expected behavior:")
        print("- Clicking one card in pile view selects only that instance")
        print("- Switching between card/pile/list views clears selections")
        print("- Individual instances can be selected, dragged, and context-clicked")
        print("- Visual stacking maintained with proper quantity display")
    else:
        print("\n⚠️ Some updates failed. Check the error messages above.")
        print("You may need to apply the changes manually or run the script again.")
    
    print(f"\n✨ Individual card selection implementation complete!")

if __name__ == "__main__":
    main()
