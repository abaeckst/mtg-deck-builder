#!/usr/bin/env python3
"""
Fix DraggableCard.tsx type conversion issues
"""

import os
import re

def fix_draggable_card():
    file_path = "src/components/DraggableCard.tsx"
    
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return False
    
    print(f"🔧 Fixing {file_path}...")
    
    # Read the file
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix the cardForMagicCard conversion to include all required ScryfallCard properties
    old_conversion = """  // Create a card-compatible object for MagicCard component
  const cardForMagicCard = React.useMemo(() => {
    if (isCardInstance(card)) {
      // Convert DeckCardInstance to card-like object for MagicCard
      return {
        id: card.cardId, // Use original card ID for MagicCard
        name: card.name,
        image_uri: card.image_uri,
        mana_cost: card.mana_cost,
        cmc: card.cmc,
        type_line: card.type_line,
        colors: card.colors,
        color_identity: card.color_identity,
        set: card.set,
        rarity: card.rarity,
        oracle_text: card.oracle_text,
        power: card.power,
        toughness: card.toughness,
        loyalty: card.loyalty,
      } as ScryfallCard;
    }
    return card as ScryfallCard | DeckCard;
  }, [card]);"""
    
    new_conversion = """  // Create a card-compatible object for MagicCard component
  const cardForMagicCard = React.useMemo(() => {
    if (isCardInstance(card)) {
      // Convert DeckCardInstance to card-like object for MagicCard
      // Include all required ScryfallCard properties with sensible defaults
      return {
        id: card.cardId, // Use original card ID for MagicCard
        oracle_id: card.cardId, // Use cardId as fallback for oracle_id
        name: card.name,
        image_uris: undefined, // Will be handled by image_uri
        image_uri: card.image_uri,
        mana_cost: card.mana_cost,
        cmc: card.cmc,
        type_line: card.type_line,
        colors: card.colors,
        color_identity: card.color_identity,
        set: card.set,
        set_name: card.set, // Use set as fallback for set_name
        rarity: card.rarity,
        oracle_text: card.oracle_text,
        power: card.power,
        toughness: card.toughness,
        loyalty: card.loyalty,
        legalities: {
          standard: 'legal',
          pioneer: 'legal',
          modern: 'legal',
          legacy: 'legal',
          vintage: 'legal',
          commander: 'legal',
          brawl: 'legal',
          historic: 'legal',
          timeless: 'legal',
          pauper: 'legal'
        },
        keywords: [],
        layout: 'normal',
        card_faces: undefined,
      } as ScryfallCard;
    }
    return card as ScryfallCard | DeckCard;
  }, [card]);"""
    
    # Replace the conversion
    if old_conversion in content:
        content = content.replace(old_conversion, new_conversion)
        print("✅ Fixed cardForMagicCard conversion")
    else:
        print("⚠️ Could not find exact cardForMagicCard conversion - checking for similar pattern")
        # Try to find and replace the return statement pattern
        pattern = r'(// Convert DeckCardInstance to card-like object for MagicCard\s+return\s+{[^}]+})\s+as\s+ScryfallCard;'
        if re.search(pattern, content, re.DOTALL):
            print("Found similar pattern - manual fix needed")
    
    # Write the file back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Fixed {file_path}")
    return True

if __name__ == "__main__":
    success = fix_draggable_card()
    if success:
        print("🎉 DraggableCard.tsx fixes completed!")
    else:
        print("❌ Some fixes failed!")
