#!/usr/bin/env python3
"""
Fix remaining component integration issues
"""

import os
import re

def fix_drag_preview():
    file_path = "src/components/DragPreview.tsx"
    
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return False
    
    print(f"🔧 Fixing {file_path}...")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Add import for utility functions
    if "import { getCardId, getSelectionId } from '../types/card';" not in content:
        # Find the existing import line and add our utilities
        import_pattern = r"(import.*from '\.\./types/card';)"
        if re.search(import_pattern, content):
            content = re.sub(
                r"(import\s+{[^}]+})\s+from\s+'\.\./types/card';",
                r"\1, getCardId, getSelectionId } from '../types/card';",
                content
            )
        else:
            # Add new import line
            content = "import { getCardId, getSelectionId } from '../types/card';\n" + content
    
    # Fix the key generation
    content = content.replace(
        'key={`${card.id}-${index}`}',
        'key={`${getCardId(card)}-${index}`}'
    )
    
    # Fix the MagicCard prop - create compatible object
    old_magic_card = """            <MagicCard
              card={card}"""
    
    new_magic_card = """            <MagicCard
              card={card as ScryfallCard | DeckCard}"""
    
    content = content.replace(old_magic_card, new_magic_card)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Fixed {file_path}")
    return True

def fix_pile_column():
    file_path = "src/components/PileColumn.tsx"
    
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return False
    
    print(f"🔧 Fixing {file_path}...")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Add import for utility functions
    if "getCardId, getSelectionId" not in content:
        content = re.sub(
            r"(import\s+{[^}]+})\s+from\s+'\.\./types/card';",
            r"\1, getCardId, getSelectionId } from '../types/card';",
            content
        )
    
    # Fix card validation
    content = content.replace(
        'if (!card || !card.id) {',
        'if (!card || !getCardId(card)) {'
    )
    
    # Fix selection checking
    content = content.replace(
        'selected={isSelected ? isSelected(card.id) : false}',
        'selected={isSelected ? isSelected(getSelectionId(card)) : false}'
    )
    
    # Fix drag checking
    content = content.replace(
        'isBeingDragged={isDragActive && selectedCards.some(sc => sc.id === card.id)}',
        'isBeingDragged={isDragActive && selectedCards.some(sc => getCardId(sc) === getCardId(card))}'
    )
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Fixed {file_path}")
    return True

def fix_pile_view():
    file_path = "src/components/PileView.tsx"
    
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return False
    
    print(f"🔧 Fixing {file_path}...")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Add import for utility functions
    if "getCardId" not in content:
        content = re.sub(
            r"(import\s+{[^}]+})\s+from\s+'\.\./types/card';",
            r"\1, getCardId } from '../types/card';",
            content
        )
    
    # Fix grouping logic - change type annotations to handle instances
    content = content.replace(
        'const colorGroups = new Map<string, (ScryfallCard | DeckCard)[]>();',
        'const colorGroups = new Map<string, (ScryfallCard | DeckCard | DeckCardInstance)[]>();'
    )
    
    content = content.replace(
        'const typeGroups = new Map<string, (ScryfallCard | DeckCard)[]>();',
        'const typeGroups = new Map<string, (ScryfallCard | DeckCard | DeckCardInstance)[]>();'
    )
    
    # Fix manual arrangement checking
    content = content.replace(
        'cards: column.cards.filter(card => !manualArrangements.has(card.id))',
        'cards: column.cards.filter(card => !manualArrangements.has(getCardId(card)))'
    )
    
    content = content.replace(
        'const card = cards.find(c => c.id === cardId);',
        'const card = cards.find(c => getCardId(c) === cardId);'
    )
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Fixed {file_path}")
    return True

def fix_list_view():
    file_path = "src/components/ListView.tsx"
    
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return False
    
    print(f"🔧 Fixing {file_path}...")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Update the handler function signatures to accept instances
    content = content.replace(
        'const handleRowClick = useCallback((card: ScryfallCard | DeckCard, event: React.MouseEvent) => {',
        'const handleRowClick = useCallback((card: ScryfallCard | DeckCard | DeckCardInstance, event: React.MouseEvent) => {'
    )
    
    content = content.replace(
        'const handleRowDoubleClick = useCallback((card: ScryfallCard | DeckCard) => {',
        'const handleRowDoubleClick = useCallback((card: ScryfallCard | DeckCard | DeckCardInstance) => {'
    )
    
    content = content.replace(
        'const handleRowRightClick = useCallback((card: ScryfallCard | DeckCard, event: React.MouseEvent) => {',
        'const handleRowRightClick = useCallback((card: ScryfallCard | DeckCard | DeckCardInstance, event: React.MouseEvent) => {'
    )
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Fixed {file_path}")
    return True

if __name__ == "__main__":
    print("🔧 Fixing remaining component integration issues...")
    
    success = True
    success &= fix_drag_preview()
    success &= fix_pile_column() 
    success &= fix_pile_view()
    success &= fix_list_view()
    
    if success:
        print("🎉 All component fixes completed!")
    else:
        print("❌ Some fixes failed!")
