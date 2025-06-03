#!/usr/bin/env python3
"""
Add Missing Import Script: Add ScryfallCard and DeckCard import to MTGOLayout.tsx
"""

import os

def add_missing_import():
    """Add the missing card types import to MTGOLayout.tsx"""
    
    file_path = r'C:\Users\carol\mtg-deckbuilder\src\components\MTGOLayout.tsx'
    
    if not os.path.exists(file_path):
        print(f"❌ Error: File not found at {file_path}")
        return False
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"📁 Reading MTGOLayout.tsx to add missing import")
        
        # Find the line with ContextMenu.css import and add the card types import after it
        old_context_menu_import = "import './ContextMenu.css';"
        new_context_menu_import = """import './ContextMenu.css';

// Card types import
import { ScryfallCard, DeckCard } from '../types/card';"""

        if old_context_menu_import in content:
            content = content.replace(old_context_menu_import, new_context_menu_import)
            print("✅ Added ScryfallCard and DeckCard import after ContextMenu.css")
        else:
            # Fallback: add after the component imports section
            old_component_imports = """// Import components
import { useCards } from '../hooks/useCards';
import { useCardSizing } from '../hooks/useCardSizing';
import DraggableCard from './DraggableCard';
import DropZoneComponent from './DropZone';
import DragPreview from './DragPreview';
import ContextMenu from './ContextMenu';
import PileView from './PileView';"""

            new_component_imports = """// Import components
import { useCards } from '../hooks/useCards';
import { useCardSizing } from '../hooks/useCardSizing';
import DraggableCard from './DraggableCard';
import DropZoneComponent from './DropZone';
import DragPreview from './DragPreview';
import ContextMenu from './ContextMenu';
import PileView from './PileView';

// Card types import
import { ScryfallCard, DeckCard } from '../types/card';"""

            if old_component_imports in content:
                content = content.replace(old_component_imports, new_component_imports)
                print("✅ Added ScryfallCard and DeckCard import after component imports")
            else:
                print("❌ Could not find suitable location to add import")
                return False
        
        # Write the updated file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Import added successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error adding import: {e}")
        return False

def main():
    print("🔧 Adding Missing Card Types Import")
    print("=" * 40)
    
    if add_missing_import():
        print()
        print("🎉 Import Fix Complete!")
        print("✅ ScryfallCard and DeckCard types now imported")
        print()  
        print("🧪 Next Steps:")
        print("1. Run `npm start` to verify compilation")
        print("2. All TypeScript errors should be resolved")
        print("3. Test pile view functionality with Pile buttons")
    else:
        print("❌ Import fix failed")

if __name__ == "__main__":
    main()
