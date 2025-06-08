#!/usr/bin/env python3

import os
import sys

def update_card_selection_behavior(filename):
    """Update DraggableCard.tsx to fix right-click selection and remove duplicate selection boxes"""
    
    if not os.path.exists(filename):
        print(f"Error: {filename} not found")
        return False
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Make replacements with exact string matching
    updates = [
        # Remove duplicate selection border that's causing multiple boxes
        (
            """      {/* Visual feedback for interaction states */}
      {selected && !isBeingDragged && (
        <div
          style={{
            position: 'absolute',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            border: '2px solid #3b82f6',
            borderRadius: '8px',
            pointerEvents: 'none',
            transition: 'all 0.2s ease',
            boxShadow: '0 0 0 1px rgba(59, 130, 246, 0.3)',
          }}
        />
      )}""",
            "",
            "Removed duplicate selection border (MagicCard already handles selection styling)"
        ),
        
        # Update right-click handler to select card first, then show context menu
        (
            """  const handleContextMenu = useCallback((event: React.MouseEvent) => {
    event.preventDefault();
    event.stopPropagation();
    
    if (disabled) {
      console.log(`Right-click prevented on ${card.name}: disabled`);
      return;
    }
    
    console.log(`Right-click on ${card.name} in ${zone}`);
    onRightClick?.(card, zone, event);
  }, [card, zone, onRightClick, disabled]);""",
            """  const handleContextMenu = useCallback((event: React.MouseEvent) => {
    event.preventDefault();
    event.stopPropagation();
    
    if (disabled) {
      console.log(`Right-click prevented on ${card.name}: disabled`);
      return;
    }
    
    console.log(`Right-click on ${card.name} in ${zone} - triggering selection`);
    
    // Right-click should select the card first
    if (cardIsInstance && cardInstanceId && onInstanceClick) {
      // Instance-based selection for deck/sideboard cards
      onInstanceClick(cardInstanceId, card as DeckCardInstance, event);
    } else {
      // Card-based selection for collection cards
      onClick?.(card, event);
    }
    
    // Then show context menu
    onRightClick?.(card, zone, event);
  }, [card, zone, onRightClick, disabled, cardIsInstance, cardInstanceId, onInstanceClick, onClick]);""",
            "Updated right-click handler to select card before showing context menu"
        )
    ]
    
    for old_str, new_str, desc in updates:
        if old_str in content:
            content = content.replace(old_str, new_str)
            print(f"✅ {desc}")
        else:
            print(f"❌ Could not find: {desc}")
            return False
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Successfully updated {filename}")
    return True

if __name__ == "__main__":
    success = update_card_selection_behavior("src/components/DraggableCard.tsx")
    sys.exit(0 if success else 1)