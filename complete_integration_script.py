#!/usr/bin/env python3
"""
Complete Instance-based Architecture Integration Script
Updates all remaining components for individual card selection
"""

import re
import os

def update_drag_and_drop():
    """Update useDragAndDrop.ts to handle instances"""
    file_path = 'src/hooks/useDragAndDrop.ts'
    
    if not os.path.exists(file_path):
        print(f"❌ Error: {file_path} not found")
        return False
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"📁 Updating {file_path}")
        
        # Update imports to include DeckCardInstance
        old_import = "import { ScryfallCard, DeckCard } from '../types/card';"
        new_import = "import { ScryfallCard, DeckCard, DeckCardInstance } from '../types/card';"
        content = content.replace(old_import, new_import)
        
        # Update DraggedCard type to include instances
        old_type = "export type DraggedCard = ScryfallCard | DeckCard;"
        new_type = "export type DraggedCard = ScryfallCard | DeckCard | DeckCardInstance;"
        content = content.replace(old_type, new_type)
        
        # No other changes needed - the hook handles cards by their ID property which both types have
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ Updated useDragAndDrop.ts")
        return True
        
    except Exception as e:
        print(f"❌ Error updating {file_path}: {str(e)}")
        return False

def update_context_menu():
    """Update useContextMenu.ts to handle instances"""
    file_path = 'src/hooks/useContextMenu.ts'
    
    if not os.path.exists(file_path):
        print(f"❌ Error: {file_path} not found")
        return False
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"📁 Updating {file_path}")
        
        # Update imports
        old_import = "import { ScryfallCard, DeckCard } from '../types/card';"
        new_import = "import { ScryfallCard, DeckCard, DeckCardInstance } from '../types/card';"
        content = content.replace(old_import, new_import)
        
        # Update interface types
        old_interface = """export interface ContextMenuState {
  visible: boolean;
  x: number;
  y: number;
  targetCard: ScryfallCard | DeckCard | null;
  targetZone: DropZone | null;
  selectedCards: (ScryfallCard | DeckCard)[];
}"""
        
        new_interface = """export interface ContextMenuState {
  visible: boolean;
  x: number;
  y: number;
  targetCard: ScryfallCard | DeckCard | DeckCardInstance | null;
  targetZone: DropZone | null;
  selectedCards: (ScryfallCard | DeckCard | DeckCardInstance)[];
}"""
        
        content = content.replace(old_interface, new_interface)
        
        # Update callback interface
        old_callbacks = """export interface DeckManagementCallbacks {
  addToDeck: (cards: (ScryfallCard | DeckCard)[], quantity?: number) => void;
  removeFromDeck: (cards: (ScryfallCard | DeckCard)[], quantity?: number) => void;
  addToSideboard: (cards: (ScryfallCard | DeckCard)[], quantity?: number) => void;
  removeFromSideboard: (cards: (ScryfallCard | DeckCard)[], quantity?: number) => void;
  moveDeckToSideboard: (cards: (ScryfallCard | DeckCard)[], quantity?: number) => void;
  moveSideboardToDeck: (cards: (ScryfallCard | DeckCard)[], quantity?: number) => void;
  getDeckQuantity: (cardId: string) => number;
  getSideboardQuantity: (cardId: string) => number;
}"""
        
        new_callbacks = """export interface DeckManagementCallbacks {
  addToDeck: (cards: (ScryfallCard | DeckCard | DeckCardInstance)[], quantity?: number) => void;
  removeFromDeck: (cards: (ScryfallCard | DeckCard | DeckCardInstance)[], quantity?: number) => void;
  addToSideboard: (cards: (ScryfallCard | DeckCard | DeckCardInstance)[], quantity?: number) => void;
  removeFromSideboard: (cards: (ScryfallCard | DeckCard | DeckCardInstance)[], quantity?: number) => void;
  moveDeckToSideboard: (cards: (ScryfallCard | DeckCard | DeckCardInstance)[], quantity?: number) => void;
  moveSideboardToDeck: (cards: (ScryfallCard | DeckCard | DeckCardInstance)[], quantity?: number) => void;
  getDeckQuantity: (cardId: string) => number;
  getSideboardQuantity: (cardId: string) => number;
}"""
        
        content = content.replace(old_callbacks, new_callbacks)
        
        # Update showContextMenu function
        old_show = """  const showContextMenu = useCallback((
    event: React.MouseEvent,
    card: ScryfallCard | DeckCard,
    zone: DropZone,
    selectedCards: (ScryfallCard | DeckCard)[] = []
  ) => {"""
        
        new_show = """  const showContextMenu = useCallback((
    event: React.MouseEvent,
    card: ScryfallCard | DeckCard | DeckCardInstance,
    zone: DropZone,
    selectedCards: (ScryfallCard | DeckCard | DeckCardInstance)[] = []
  ) => {"""
        
        content = content.replace(old_show, new_show)
        
        # Update getDeckQuantity call to handle instances
        old_deck_qty = "const deckQuantity = callbacks.getDeckQuantity(targetCard.id);"
        new_deck_qty = "const deckQuantity = callbacks.getDeckQuantity('cardId' in targetCard ? targetCard.cardId : targetCard.id);"
        content = content.replace(old_deck_qty, new_deck_qty)
        
        # Update getSideboardQuantity call
        old_side_qty = "const sideboardQuantity = callbacks.getSideboardQuantity(targetCard.id);"
        new_side_qty = "const sideboardQuantity = callbacks.getSideboardQuantity('cardId' in targetCard ? targetCard.cardId : targetCard.id);"
        content = content.replace(old_side_qty, new_side_qty)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ Updated useContextMenu.ts")
        return True
        
    except Exception as e:
        print(f"❌ Error updating {file_path}: {str(e)}")
        return False

def update_list_view():
    """Update ListView.tsx to handle instances"""
    file_path = 'src/components/ListView.tsx'
    
    if not os.path.exists(file_path):
        print(f"❌ Error: {file_path} not found")
        return False
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"📁 Updating {file_path}")
        
        # Update imports
        old_import = "import { ScryfallCard, DeckCard, isBasicLand } from '../types/card';"
        new_import = "import { ScryfallCard, DeckCard, DeckCardInstance, isBasicLand } from '../types/card';"
        content = content.replace(old_import, new_import)
        
        # Update interface types
        old_interface = """interface ListViewProps {
  cards: (ScryfallCard | DeckCard)[];"""
        
        new_interface = """interface ListViewProps {
  cards: (ScryfallCard | DeckCard | DeckCardInstance)[];"""
        
        content = content.replace(old_interface, new_interface)
        
        # Update handler types
        old_handlers = """  // Standard card interaction handlers
  onClick: (card: ScryfallCard | DeckCard, event?: React.MouseEvent) => void;
  onDoubleClick: (card: ScryfallCard | DeckCard) => void;
  onRightClick: (card: ScryfallCard | DeckCard, zone: DropZone, event: React.MouseEvent) => void;
  onDragStart: (cards: (ScryfallCard | DeckCard)[], zone: DropZone, event: React.MouseEvent) => void;
  // Selection and drag state
  isSelected: (cardId: string) => boolean;
  selectedCards: (ScryfallCard | DeckCard)[];"""
        
        new_handlers = """  // Standard card interaction handlers
  onClick: (card: ScryfallCard | DeckCard | DeckCardInstance, event?: React.MouseEvent) => void;
  onDoubleClick: (card: ScryfallCard | DeckCard | DeckCardInstance) => void;
  onRightClick: (card: ScryfallCard | DeckCard | DeckCardInstance, zone: DropZone, event: React.MouseEvent) => void;
  onDragStart: (cards: (ScryfallCard | DeckCard | DeckCardInstance)[], zone: DropZone, event: React.MouseEvent) => void;
  // Selection and drag state
  isSelected: (cardId: string) => boolean;
  selectedCards: (ScryfallCard | DeckCard | DeckCardInstance)[];"""
        
        content = content.replace(old_handlers, new_handlers)
        
        # Update card rendering to use proper ID for instances
        old_render = """                <tr
                  key={card.id}
                  className={`list-view-row ${isSelected(card.id) ? 'selected' : ''} ${"""
        
        new_render = """                <tr
                  key={'instanceId' in card ? card.instanceId : card.id}
                  className={`list-view-row ${isSelected('instanceId' in card ? card.instanceId : card.id) ? 'selected' : ''} ${"""
        
        content = content.replace(old_render, new_render)
        
        # Update drag start to check selection with proper ID
        old_drag_start = """  const handleRowDragStart = useCallback((card: ScryfallCard | DeckCard, event: React.MouseEvent) => {
    // Only handle left mouse button for drag
    if (event.button !== 0) return;
    
    const dragCards = isSelected(card.id) && selectedCards.length > 1 
      ? selectedCards 
      : [card];"""
        
        new_drag_start = """  const handleRowDragStart = useCallback((card: ScryfallCard | DeckCard | DeckCardInstance, event: React.MouseEvent) => {
    // Only handle left mouse button for drag
    if (event.button !== 0) return;
    
    const cardIdOrInstanceId = 'instanceId' in card ? card.instanceId : card.id;
    const dragCards = isSelected(cardIdOrInstanceId) && selectedCards.length > 1 
      ? selectedCards 
      : [card];"""
        
        content = content.replace(old_drag_start, new_drag_start)
        
        # Update quantity controls for instances
        old_quantity = """  const handleQuantityChange = useCallback((card: ScryfallCard | DeckCard, delta: number) => {
    if (!onQuantityChange || !('quantity' in card)) return;
    
    const currentQuantity = card.quantity || 0;
    const maxQuantity = isBasicLand(card) ? Infinity : 4;
    const newQuantity = Math.max(0, Math.min(maxQuantity, currentQuantity + delta));
    
    onQuantityChange(card.id, newQuantity);
  }, [onQuantityChange]);"""
        
        new_quantity = """  const handleQuantityChange = useCallback((card: ScryfallCard | DeckCard | DeckCardInstance, delta: number) => {
    if (!onQuantityChange) return;
    
    // For instances, quantity is always 1, so we handle add/remove differently
    if ('instanceId' in card) {
      // For deck instances, we use the original card ID for quantity management
      const currentQuantity = 1; // Each instance represents 1 copy
      const newQuantity = delta > 0 ? 1 : 0; // Adding or removing the instance
      onQuantityChange(card.cardId, newQuantity);
    } else if ('quantity' in card) {
      // For DeckCard objects, use existing logic
      const currentQuantity = card.quantity || 0;
      const maxQuantity = isBasicLand(card) ? Infinity : 4;
      const newQuantity = Math.max(0, Math.min(maxQuantity, currentQuantity + delta));
      onQuantityChange(card.id, newQuantity);
    }
  }, [onQuantityChange]);"""
        
        content = content.replace(old_quantity, new_quantity)
        
        # Update quantity display for instances
        old_qty_display = """                      {column.id === 'quantity' && 'quantity' in card && onQuantityChange && (
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
                      )}"""
        
        new_qty_display = """                      {column.id === 'quantity' && onQuantityChange && (
                        <div className="quantity-controls">
                          <span className="quantity-display">
                            {'instanceId' in card ? 1 : ('quantity' in card ? card.quantity : 0)}
                          </span>
                          <div className="quantity-buttons">
                            <button 
                              className="quantity-btn minus"
                              onClick={(e) => {
                                e.stopPropagation();
                                handleQuantityChange(card, -1);
                              }}
                              disabled={'instanceId' in card ? false : ('quantity' in card ? card.quantity === 0 : true)}
                            >
                              −
                            </button>
                            <button 
                              className="quantity-btn plus"
                              onClick={(e) => {
                                e.stopPropagation();
                                handleQuantityChange(card, 1);
                              }}
                              disabled={'instanceId' in card ? false : (!isBasicLand(card) && 'quantity' in card && card.quantity >= 4)}
                            >
                              +
                            </button>
                          </div>
                        </div>
                      )}"""
        
        content = content.replace(old_qty_display, new_qty_display)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ Updated ListView.tsx")
        return True
        
    except Exception as e:
        print(f"❌ Error updating {file_path}: {str(e)}")
        return False

def update_pile_view():
    """Update PileView.tsx and PileColumn.tsx to handle instances"""
    # Update PileView.tsx
    file_path = 'src/components/PileView.tsx'
    
    if not os.path.exists(file_path):
        print(f"❌ Error: {file_path} not found")
        return False
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"📁 Updating {file_path}")
        
        # Update imports
        old_import = "import { ScryfallCard, DeckCard } from '../types/card';"
        new_import = "import { ScryfallCard, DeckCard, DeckCardInstance } from '../types/card';"
        content = content.replace(old_import, new_import)
        
        # Update interface types
        old_interface = """interface PileViewProps {
  cards: (ScryfallCard | DeckCard)[];"""
        
        new_interface = """interface PileViewProps {
  cards: (ScryfallCard | DeckCard | DeckCardInstance)[];"""
        
        content = content.replace(old_interface, new_interface)
        
        # Update handler types (multiple occurrences)
        old_handlers = [
            "onClick?: (card: ScryfallCard | DeckCard, event?: React.MouseEvent) => void;",
            "onDoubleClick?: (card: ScryfallCard | DeckCard) => void;",
            "onEnhancedDoubleClick?: (card: ScryfallCard | DeckCard, zone: DropZone, event: React.MouseEvent) => void;",
            "onRightClick?: (card: ScryfallCard | DeckCard, zone: DropZone, event: React.MouseEvent) => void;",
            "onDragStart?: (cards: (ScryfallCard | DeckCard)[], zone: DropZone, event: React.MouseEvent) => void;",
            "selectedCards?: (ScryfallCard | DeckCard)[];"
        ]
        
        new_handlers = [
            "onClick?: (card: ScryfallCard | DeckCard | DeckCardInstance, event?: React.MouseEvent) => void;",
            "onDoubleClick?: (card: ScryfallCard | DeckCard | DeckCardInstance) => void;",
            "onEnhancedDoubleClick?: (card: ScryfallCard | DeckCard | DeckCardInstance, zone: DropZone, event: React.MouseEvent) => void;",
            "onRightClick?: (card: ScryfallCard | DeckCard | DeckCardInstance, zone: DropZone, event: React.MouseEvent) => void;",
            "onDragStart?: (cards: (ScryfallCard | DeckCard | DeckCardInstance)[], zone: DropZone, event: React.MouseEvent) => void;",
            "selectedCards?: (ScryfallCard | DeckCard | DeckCardInstance)[];"
        ]
        
        for old, new in zip(old_handlers, new_handlers):
            content = content.replace(old, new)
        
        # Update organize functions to handle instances
        old_organize = "const organizeByManaValue = useCallback((cardList: (ScryfallCard | DeckCard)[]): ColumnData[] => {"
        new_organize = "const organizeByManaValue = useCallback((cardList: (ScryfallCard | DeckCard | DeckCardInstance)[]): ColumnData[] => {"
        content = content.replace(old_organize, new_organize)
        
        # Update all other organize functions
        organize_functions = ['organizeByColor', 'organizeByRarity', 'organizeByType']
        for func in organize_functions:
            old_func = f"const {func} = useCallback((cardList: (ScryfallCard | DeckCard)[]): ColumnData[] => {{"
            new_func = f"const {func} = useCallback((cardList: (ScryfallCard | DeckCard | DeckCardInstance)[]): ColumnData[] => {{"
            content = content.replace(old_func, new_func)
        
        # Update ColumnData interface
        old_column = """interface ColumnData {
  id: string;
  title: string;
  cards: (ScryfallCard | DeckCard)[];
  sortValue: string | number;
}"""
        
        new_column = """interface ColumnData {
  id: string;
  title: string;
  cards: (ScryfallCard | DeckCard | DeckCardInstance)[];
  sortValue: string | number;
}"""
        
        content = content.replace(old_column, new_column)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ Updated PileView.tsx")
        
        # Update PileColumn.tsx
        file_path = 'src/components/PileColumn.tsx'
        
        if not os.path.exists(file_path):
            print(f"❌ Warning: {file_path} not found, skipping")
            return True
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"📁 Updating PileColumn.tsx")
        
        # Update imports
        old_import = "import { ScryfallCard, DeckCard } from '../types/card';"
        new_import = "import { ScryfallCard, DeckCard, DeckCardInstance } from '../types/card';"
        content = content.replace(old_import, new_import)
        
        # Update interface
        old_pile_interface = """interface PileColumnProps {
  columnId: string;
  title: string;
  cards: (ScryfallCard | DeckCard)[];"""
        
        new_pile_interface = """interface PileColumnProps {
  columnId: string;
  title: string;
  cards: (ScryfallCard | DeckCard | DeckCardInstance)[];"""
        
        content = content.replace(old_pile_interface, new_pile_interface)
        
        # Update all handler types in PileColumn
        pile_handlers = [
            "onClick?: (card: ScryfallCard | DeckCard, event?: React.MouseEvent) => void;",
            "onDoubleClick?: (card: ScryfallCard | DeckCard) => void;",
            "onEnhancedDoubleClick?: (card: ScryfallCard | DeckCard, zone: DropZone, event: React.MouseEvent) => void;",
            "onRightClick?: (card: ScryfallCard | DeckCard, zone: DropZone, event: React.MouseEvent) => void;",
            "onDragStart?: (cards: (ScryfallCard | DeckCard)[], zone: DropZone, event: React.MouseEvent) => void;",
            "selectedCards?: (ScryfallCard | DeckCard)[];"
        ]
        
        pile_new_handlers = [
            "onClick?: (card: ScryfallCard | DeckCard | DeckCardInstance, event?: React.MouseEvent) => void;",
            "onDoubleClick?: (card: ScryfallCard | DeckCard | DeckCardInstance) => void;",
            "onEnhancedDoubleClick?: (card: ScryfallCard | DeckCard | DeckCardInstance, zone: DropZone, event: React.MouseEvent) => void;",
            "onRightClick?: (card: ScryfallCard | DeckCard | DeckCardInstance, zone: DropZone, event: React.MouseEvent) => void;",
            "onDragStart?: (cards: (ScryfallCard | DeckCard | DeckCardInstance)[], zone: DropZone, event: React.MouseEvent) => void;",
            "selectedCards?: (ScryfallCard | DeckCard | DeckCardInstance)[];"
        ]
        
        for old, new in zip(pile_handlers, pile_new_handlers):
            content = content.replace(old, new)
        
        # Update card rendering in PileColumn to use proper keys for instances
        old_pile_render = """        // Get quantity for this card
        let cardQuantity = 1;
        if (typeof card === 'object' && card !== null) {
          if ('quantity' in card && typeof card.quantity === 'number' && card.quantity > 0) {
            cardQuantity = card.quantity;
          }
        }

        // Create individual draggable cards for each copy (MTGO-style stacking)
        for (let i = 0; i < cardQuantity; i++) {"""
        
        new_pile_render = """        // Get quantity for this card
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
        for (let i = 0; i < cardQuantity; i++) {"""
        
        content = content.replace(old_pile_render, new_pile_render)
        
        # Update the key generation for instances
        old_key = 'key={`${card.id}-${i}`}'
        new_key = 'key={`${"instanceId" in card ? card.instanceId : card.id}-${i}`}'
        content = content.replace(old_key, new_key)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ Updated PileColumn.tsx")
        return True
        
    except Exception as e:
        print(f"❌ Error updating pile view files: {str(e)}")
        return False

def main():
    """Run all updates for instance-based architecture"""
    print("🚀 Starting complete instance-based architecture integration...")
    print()
    
    success_count = 0
    total_updates = 4
    
    # Update all components
    if update_drag_and_drop():
        success_count += 1
    
    if update_context_menu():
        success_count += 1
    
    if update_list_view():
        success_count += 1
    
    if update_pile_view():
        success_count += 1
    
    print()
    print(f"📊 Completed {success_count}/{total_updates} updates")
    
    if success_count == total_updates:
        print("🎉 All updates completed successfully!")
        print()
        print("📋 Next steps to complete the implementation:")
        print("1. Run the MTGOLayout update script: python update_mtgo_layout.py")
        print("2. Replace the files with the new versions")
        print("3. Update MTGOLayout.tsx to use the new selection methods")
        print("4. Test individual card selection in deck/sideboard")
        print("5. Verify all existing functionality still works")
    else:
        print("💥 Some updates failed - please check the errors above")

if __name__ == "__main__":
    main()
