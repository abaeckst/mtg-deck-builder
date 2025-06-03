#!/usr/bin/env python3
"""
Fix property access errors in MTG Deck Builder
Replaces direct .id access with getCardId() utility function calls
"""

import os
import re

def fix_mtgo_layout_property_access():
    """Fix property access errors in MTGOLayout.tsx"""
    file_path = "src/components/MTGOLayout.tsx"
    
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return False
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Track changes
    changes_made = 0
    
    # Fix all instances of card.id to getCardId(card)
    # Pattern: variable.id where variable is likely a card
    card_id_patterns = [
        (r'(\w+)\.id(?=\s*===?\s*card\.id)', r'getCardId(\1)'),  # deckCard.id === card.id
        (r'card\.id(?=\s*[)},;])', r'getCardId(card)'),          # card.id at end of expressions
        (r'(\w+Card)\.id(?=\s*[)},;])', r'getCardId(\1)'),       # someCard.id at end
        (r'(\w+)\.id(?=\s*!==?\s*card\.id)', r'getCardId(\1)'),  # dc.id !== card.id
        (r'card\.id(?=\s*!==?\s*)', r'getCardId(card)'),         # card.id !== 
    ]
    
    for pattern, replacement in card_id_patterns:
        old_content = content
        content = re.sub(pattern, replacement, content)
        if content != old_content:
            changes_made += 1
    
    # Fix specific problematic lines based on the error output
    specific_fixes = [
        # Line 352: deckCard.id === card.id
        (r'deckCard\.id\s*===\s*card\.id', 'getCardId(deckCard) === getCardId(card)'),
        # Line 364: deckCard.id === card.id  
        (r'deckCard\.id\s*===\s*card\.id', 'getCardId(deckCard) === getCardId(card)'),
        # Line 377: sideCard.id === card.id
        (r'sideCard\.id\s*===\s*card\.id', 'getCardId(sideCard) === getCardId(card)'),
        # Line 385: sideCard.id === card.id
        (r'sideCard\.id\s*===\s*card\.id', 'getCardId(sideCard) === getCardId(card)'),
        # Line 395: dc.id === card.id
        (r'dc\.id\s*===\s*card\.id', 'getCardId(dc) === getCardId(card)'),
        # Line 399: dc.id === card.id
        (r'dc\.id\s*===\s*card\.id', 'getCardId(dc) === getCardId(card)'),
        # Line 404: dc.id !== card.id
        (r'dc\.id\s*!==\s*card\.id', 'getCardId(dc) !== getCardId(card)'),
        # Line 407: sc.id === card.id
        (r'sc\.id\s*===\s*card\.id', 'getCardId(sc) === getCardId(card)'),
        # Line 410: sc.id === card.id
        (r'sc\.id\s*===\s*card\.id', 'getCardId(sc) === getCardId(card)'),
        # Line 420: sc.id === card.id
        (r'sc\.id\s*===\s*card\.id', 'getCardId(sc) === getCardId(card)'),
        # Line 425: sc.id === card.id
        (r'sc\.id\s*===\s*card\.id', 'getCardId(sc) === getCardId(card)'),
        # Line 430: sc.id !== card.id
        (r'sc\.id\s*!==\s*card\.id', 'getCardId(sc) !== getCardId(card)'),
        # Line 434: dc.id === card.id
        (r'dc\.id\s*===\s*card\.id', 'getCardId(dc) === getCardId(card)'),
        # Line 437: dc.id === card.id
        (r'dc\.id\s*===\s*card\.id', 'getCardId(dc) === getCardId(card)'),
        # Line 447: dc.id === card.id
        (r'dc\.id\s*===\s*card\.id', 'getCardId(dc) === getCardId(card)'),
        # Line 451: dc.id === card.id
        (r'dc\.id\s*===\s*card\.id', 'getCardId(dc) === getCardId(card)'),
        # Line 456: dc.id !== card.id
        (r'dc\.id\s*!==\s*card\.id', 'getCardId(dc) !== getCardId(card)'),
        # Line 461: sc.id === card.id
        (r'sc\.id\s*===\s*card\.id', 'getCardId(sc) === getCardId(card)'),
        # Line 465: sc.id === card.id
        (r'sc\.id\s*===\s*card\.id', 'getCardId(sc) === getCardId(card)'),
        # Line 470: sc.id !== card.id
        (r'sc\.id\s*!==\s*card\.id', 'getCardId(sc) !== getCardId(card)'),
    ]
    
    for pattern, replacement in specific_fixes:
        old_content = content
        content = re.sub(pattern, replacement, content)
        if content != old_content:
            changes_made += 1
    
    # Fix the sortCards return type issue (lines 663, 667)
    # Fix the ternary operator that returns boolean instead of array
    sort_fixes = [
        (r"layout\.viewModes\.deck === \\'pile\\' \? mainDeck : sortCards\([^)]+\) as DeckCardInstance\[\]", 
         "layout.viewModes.deck === 'pile' ? mainDeck : (sortCards(mainDeck, deckSortCriteria, deckSortDirection) as DeckCardInstance[])"),
        (r"layout\.viewModes\.sideboard === \\'pile\\' \? sideboard : sortCards\([^)]+\) as DeckCardInstance\[\]",
         "layout.viewModes.sideboard === 'pile' ? sideboard : (sortCards(sideboard, sideboardSortCriteria, sideboardSortDirection) as DeckCardInstance[])")
    ]
    
    for pattern, replacement in sort_fixes:
        old_content = content
        content = re.sub(pattern, replacement, content)
        if content != old_content:
            changes_made += 1
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Fixed {changes_made} property access issues in MTGOLayout.tsx")
    return True

def fix_missing_utility_imports():
    """Ensure all necessary utility functions are imported"""
    file_path = "src/components/MTGOLayout.tsx"
    
    if not os.path.exists(file_path):
        return False
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if getSelectionId is imported
    if 'getSelectionId' not in content:
        # Add getSelectionId to the import
        import_pattern = r"(import \{[^}]*getCardId[^}]*\} from '../types/card';)"
        if re.search(import_pattern, content):
            content = re.sub(
                r"(getCardId)(\s*\} from '../types/card';)",
                r"\1, getSelectionId\2",
                content
            )
            print("✅ Added getSelectionId import to MTGOLayout.tsx")
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True

def main():
    """Fix all property access errors"""
    print("🔧 Fixing property access errors...")
    
    # Change to project directory if needed
    if os.path.exists("src/components"):
        os.chdir(".")
    elif os.path.exists("mtg-deckbuilder/src/components"):
        os.chdir("mtg-deckbuilder")
    else:
        print("❌ Could not find project directory")
        return
    
    success_count = 0
    
    # Fix property access
    if fix_mtgo_layout_property_access():
        success_count += 1
    
    # Fix missing imports
    if fix_missing_utility_imports():
        success_count += 1
    
    print(f"\n✅ Applied property access fixes")
    print("🚀 Run the import fix script first, then this script, then check compilation")

if __name__ == "__main__":
    main()
