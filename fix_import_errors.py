#!/usr/bin/env python3
"""
Fix import syntax errors in MTG Deck Builder components
Fixes the broken import statements that are causing compilation failures
"""

import os
import re

def fix_mtgo_layout_imports():
    """Fix the broken import statement in MTGOLayout.tsx"""
    file_path = "src/components/MTGOLayout.tsx"
    
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return False
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix the broken import on lines 12-14
    old_import = """import { ScryfallCard, DeckCard, DeckCardInstance, scryfallToDeckCard, scryfallToDeckInstance, 
         deckCardToDeckInstance, isBasicLand, getTotalCardQuantity, getCardQuantityInZone, 
         removeInstancesForCard }, getCardId } from '../types/card';"""
    
    new_import = """import { ScryfallCard, DeckCard, DeckCardInstance, scryfallToDeckCard, scryfallToDeckInstance, 
         deckCardToDeckInstance, isBasicLand, getTotalCardQuantity, getCardQuantityInZone, 
         removeInstancesForCard, getCardId } from '../types/card';"""
    
    if old_import in content:
        content = content.replace(old_import, new_import)
        print("✅ Fixed MTGOLayout.tsx import statement")
    else:
        print("⚠️ Could not find exact import pattern in MTGOLayout.tsx")
        # Try to fix with regex
        import_pattern = r"import \{\s*ScryfallCard[^}]+removeInstancesForCard\s*\}\s*,\s*getCardId\s*\}\s*from"
        if re.search(import_pattern, content):
            content = re.sub(import_pattern, 
                           "import { ScryfallCard, DeckCard, DeckCardInstance, scryfallToDeckCard, scryfallToDeckInstance, deckCardToDeckInstance, isBasicLand, getTotalCardQuantity, getCardQuantityInZone, removeInstancesForCard, getCardId } from", 
                           content)
            print("✅ Fixed MTGOLayout.tsx import with regex")
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True

def fix_pile_column_imports():
    """Fix the broken import statement in PileColumn.tsx"""
    file_path = "src/components/PileColumn.tsx"
    
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return False
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix the broken import 
    old_import = """import { ScryfallCard, DeckCard, DeckCardInstance }, getCardId, getSelectionId } from '../types/card';"""
    new_import = """import { ScryfallCard, DeckCard, DeckCardInstance, getCardId, getSelectionId } from '../types/card';"""
    
    if old_import in content:
        content = content.replace(old_import, new_import)
        print("✅ Fixed PileColumn.tsx import statement")
    else:
        print("⚠️ Could not find exact import pattern in PileColumn.tsx")
        # Try regex fix
        content = re.sub(r"import \{ ([^}]+) \}, ([^}]+) \} from", r"import { \1, \2 } from", content)
        print("✅ Fixed PileColumn.tsx import with regex")
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True

def fix_pile_view_imports():
    """Fix the broken import statement in PileView.tsx"""
    file_path = "src/components/PileView.tsx"
    
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return False
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix the broken import
    old_import = """import { ScryfallCard, DeckCard, DeckCardInstance }, getCardId } from '../types/card';"""
    new_import = """import { ScryfallCard, DeckCard, DeckCardInstance, getCardId } from '../types/card';"""
    
    if old_import in content:
        content = content.replace(old_import, new_import)
        print("✅ Fixed PileView.tsx import statement")
    else:
        print("⚠️ Could not find exact import pattern in PileView.tsx")
        # Try regex fix
        content = re.sub(r"import \{ ([^}]+) \}, ([^}]+) \} from", r"import { \1, \2 } from", content)
        print("✅ Fixed PileView.tsx import with regex")
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True

def fix_drag_preview_imports():
    """Fix missing imports in DragPreview.tsx"""
    file_path = "src/components/DragPreview.tsx"
    
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return False
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if imports are missing
    if "ScryfallCard" not in content or "DeckCard" not in content:
        # Find the import section and add the missing imports
        import_pattern = r"(import [^;]+from ['\"][^'\"]+['\"];)"
        imports = re.findall(import_pattern, content)
        
        # Add the missing import after the last import
        if imports:
            last_import = imports[-1]
            new_import = "\nimport { ScryfallCard, DeckCard, DeckCardInstance } from '../types/card';"
            content = content.replace(last_import, last_import + new_import)
            print("✅ Added missing imports to DragPreview.tsx")
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    return True

def main():
    """Fix all import syntax errors"""
    print("🔧 Fixing import syntax errors...")
    
    # Change to project directory if needed
    if os.path.exists("src/components"):
        os.chdir(".")
    elif os.path.exists("mtg-deckbuilder/src/components"):
        os.chdir("mtg-deckbuilder")
    else:
        print("❌ Could not find project directory")
        return
    
    success_count = 0
    
    # Fix each file
    if fix_mtgo_layout_imports():
        success_count += 1
    
    if fix_pile_column_imports():
        success_count += 1
        
    if fix_pile_view_imports():
        success_count += 1
        
    if fix_drag_preview_imports():
        success_count += 1
    
    print(f"\n✅ Fixed import errors in {success_count}/4 files")
    print("🚀 Run 'npm start' to check compilation status")

if __name__ == "__main__":
    main()
