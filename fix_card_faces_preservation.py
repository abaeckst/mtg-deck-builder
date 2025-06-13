#!/usr/bin/env python3
"""
Fix card.ts to preserve card_faces data in DeckCardInstance for double-faced card support
This ensures flip functionality works for cards in deck and sideboard areas
"""

import os
import shutil

def fix_card_types():
    file_path = "src/types/card.ts"
    backup_path = f"{file_path}.backup"
    
    # Create backup
    if os.path.exists(file_path):
        shutil.copy2(file_path, backup_path)
        print(f"✅ Backup created: {backup_path}")
    
    # Read current content
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find and update the DeckCardInstance interface
    old_interface = """/**
 * Individual deck card instance with unique ID for proper selection
 * Each physical card copy in deck/sideboard gets its own instance
 */
export interface DeckCardInstance {
  instanceId: string;        // Unique: "cardId-zone-timestamp-random"
  cardId: string;           // Original Scryfall ID (for grouping, limits, etc.)
  name: string;
  image_uri: string;
  mana_cost?: string;
  cmc: number;
  type_line: string;
  colors: string[];
  color_identity: string[];
  set: string;
  rarity: 'common' | 'uncommon' | 'rare' | 'mythic' | 'special' | 'bonus';
  zone: 'deck' | 'sideboard';  // Track which zone this instance belongs to
  addedAt: number;             // Timestamp for ordering/history
  
  // Card text and stats
  oracle_text?: string;
  power?: string;
  toughness?: string;
  loyalty?: string;
  
  // Format legality (inherited from original card)
  legal_in_format?: boolean;
}"""

    new_interface = """/**
 * Individual deck card instance with unique ID for proper selection
 * Each physical card copy in deck/sideboard gets its own instance
 */
export interface DeckCardInstance {
  instanceId: string;        // Unique: "cardId-zone-timestamp-random"
  cardId: string;           // Original Scryfall ID (for grouping, limits, etc.)
  name: string;
  image_uri: string;
  mana_cost?: string;
  cmc: number;
  type_line: string;
  colors: string[];
  color_identity: string[];
  set: string;
  rarity: 'common' | 'uncommon' | 'rare' | 'mythic' | 'special' | 'bonus';
  zone: 'deck' | 'sideboard';  // Track which zone this instance belongs to
  addedAt: number;             // Timestamp for ordering/history
  
  // Card text and stats
  oracle_text?: string;
  power?: string;
  toughness?: string;
  loyalty?: string;
  
  // Double-faced card support (NEW)
  card_faces?: CardFace[];     // Preserve card faces for flip functionality
  
  // Format legality (inherited from original card)
  legal_in_format?: boolean;
}"""

    # Replace the interface
    if old_interface in content:
        content = content.replace(old_interface, new_interface)
        print("✅ Updated DeckCardInstance interface to include card_faces")
    else:
        print("⚠️  Could not find exact DeckCardInstance interface - checking for variations")
        # Try a more flexible approach - look for the interface definition
        import re
        pattern = r'export interface DeckCardInstance \{[^}]+\}'
        if re.search(pattern, content, re.DOTALL):
            print("   Found DeckCardInstance interface but format differs from expected")
            print("   Manual update may be needed to add: card_faces?: CardFace[];")
        else:
            print("   Could not locate DeckCardInstance interface")
            return

    # Find and update the scryfallToDeckInstance function
    old_function = """/**
 * Convert a ScryfallCard to a DeckCardInstance for deck/sideboard use
 */
export const scryfallToDeckInstance = (
  scryfallCard: ScryfallCard, 
  zone: 'deck' | 'sideboard'
): DeckCardInstance => {
  return {
    instanceId: generateInstanceId(scryfallCard.id, zone),
    cardId: scryfallCard.id,
    name: scryfallCard.name,
    image_uri: getCardImageUri(scryfallCard),
    mana_cost: scryfallCard.mana_cost,
    cmc: scryfallCard.cmc,
    type_line: scryfallCard.type_line,
    colors: scryfallCard.colors,
    color_identity: scryfallCard.color_identity,
    set: scryfallCard.set,
    rarity: scryfallCard.rarity,
    zone,
    addedAt: Date.now(),
    oracle_text: scryfallCard.oracle_text,
    power: scryfallCard.power,
    toughness: scryfallCard.toughness,
    loyalty: scryfallCard.loyalty,
  };
};"""

    new_function = """/**
 * Convert a ScryfallCard to a DeckCardInstance for deck/sideboard use
 */
export const scryfallToDeckInstance = (
  scryfallCard: ScryfallCard, 
  zone: 'deck' | 'sideboard'
): DeckCardInstance => {
  return {
    instanceId: generateInstanceId(scryfallCard.id, zone),
    cardId: scryfallCard.id,
    name: scryfallCard.name,
    image_uri: getCardImageUri(scryfallCard),
    mana_cost: scryfallCard.mana_cost,
    cmc: scryfallCard.cmc,
    type_line: scryfallCard.type_line,
    colors: scryfallCard.colors,
    color_identity: scryfallCard.color_identity,
    set: scryfallCard.set,
    rarity: scryfallCard.rarity,
    zone,
    addedAt: Date.now(),
    oracle_text: scryfallCard.oracle_text,
    power: scryfallCard.power,
    toughness: scryfallCard.toughness,
    loyalty: scryfallCard.loyalty,
    // NEW: Preserve card faces for double-faced card support
    card_faces: scryfallCard.card_faces,
  };
};"""

    # Replace the function
    if old_function in content:
        content = content.replace(old_function, new_function)
        print("✅ Updated scryfallToDeckInstance to preserve card_faces")
    else:
        print("⚠️  Could not find exact scryfallToDeckInstance function - may need manual update")

    # Find and update the deckCardToDeckInstance function (legacy support)
    old_legacy_function = """/**
 * Convert a DeckCard to a DeckCardInstance for deck/sideboard use
 * DEPRECATED: For backward compatibility only
 */
export const deckCardToDeckInstance = (
  deckCard: DeckCard, 
  zone: 'deck' | 'sideboard'
): DeckCardInstance => {
  return {
    instanceId: generateInstanceId(deckCard.id, zone),
    cardId: deckCard.id,
    name: deckCard.name,
    image_uri: deckCard.image_uri,
    mana_cost: deckCard.mana_cost,
    cmc: deckCard.cmc,
    type_line: deckCard.type_line,
    colors: deckCard.colors,
    color_identity: deckCard.color_identity,
    set: deckCard.set,
    rarity: deckCard.rarity,
    zone,
    addedAt: Date.now(),
    oracle_text: deckCard.oracle_text,
    power: deckCard.power,
    toughness: deckCard.toughness,
    loyalty: deckCard.loyalty,
    legal_in_format: deckCard.legal_in_format,
  };
};"""

    new_legacy_function = """/**
 * Convert a DeckCard to a DeckCardInstance for deck/sideboard use
 * DEPRECATED: For backward compatibility only
 */
export const deckCardToDeckInstance = (
  deckCard: DeckCard, 
  zone: 'deck' | 'sideboard'
): DeckCardInstance => {
  return {
    instanceId: generateInstanceId(deckCard.id, zone),
    cardId: deckCard.id,
    name: deckCard.name,
    image_uri: deckCard.image_uri,
    mana_cost: deckCard.mana_cost,
    cmc: deckCard.cmc,
    type_line: deckCard.type_line,
    colors: deckCard.colors,
    color_identity: deckCard.color_identity,
    set: deckCard.set,
    rarity: deckCard.rarity,
    zone,
    addedAt: Date.now(),
    oracle_text: deckCard.oracle_text,
    power: deckCard.power,
    toughness: deckCard.toughness,
    loyalty: deckCard.loyalty,
    legal_in_format: deckCard.legal_in_format,
    // NEW: DeckCard doesn't have card_faces, so this will be undefined
    card_faces: undefined,
  };
};"""

    # Replace the legacy function
    if old_legacy_function in content:
        content = content.replace(old_legacy_function, new_legacy_function)
        print("✅ Updated deckCardToDeckInstance with card_faces (undefined for legacy)")
    else:
        print("⚠️  Could not find exact deckCardToDeckInstance function")

    # Write the updated content
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Updated {file_path}")
    print("")
    print("📝 Changes made:")
    print("   - Added card_faces?: CardFace[] to DeckCardInstance interface")
    print("   - Updated scryfallToDeckInstance() to preserve card_faces data")
    print("   - Updated deckCardToDeckInstance() to handle card_faces (legacy)")
    print("")
    print("🧪 Testing Instructions:")
    print("   1. Restart the app: npm start")
    print("   2. Search for double-faced cards like 'Heliod, the Radiant Dawn'")
    print("   3. Add them to deck or sideboard")
    print("   4. Flip buttons should now appear on deck/sideboard cards")
    print("   5. Test flipping functionality in all areas")

if __name__ == "__main__":
    fix_card_types()
