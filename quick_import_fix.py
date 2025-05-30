#!/usr/bin/env python3
"""
Quick Fix: Add missing DeckCard import to MTGOLayout.tsx
"""

import os

def fix_missing_import():
    """Add DeckCard to the existing card types import"""
    
    file_path = r'C:\Users\carol\mtg-deckbuilder\src\components\MTGOLayout.tsx'
    
    if not os.path.exists(file_path):
        print(f"❌ Error: File not found at {file_path}")
        return False
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"📁 Reading MTGOLayout.tsx to fix import")
        
        # Find the line with card types import and check what's there
        if "import { ScryfallCard, DeckCard } from '../types/card';" in content:
            print("✅ DeckCard import already present - no changes needed")
            return True
        elif "import { ScryfallCard } from '../types/card';" in content:
            # Add DeckCard to existing import
            content = content.replace(
                "import { ScryfallCard } from '../types/card';",
                "import { ScryfallCard, DeckCard } from '../types/card';"
            )
            print("✅ Added DeckCard to existing import")
        else:
            # Look for any import from types/card and show what we found
            lines = content.split('\n')
            for i, line in enumerate(lines[:50]):  # Check first 50 lines
                if "'../types/card'" in line:
                    print(f"Found import on line {i+1}: {line.strip()}")
            
            print("❌ Could not find the card types import to modify")
            print("Please manually add: import { ScryfallCard, DeckCard } from '../types/card';")
            return False
        
        # Write the updated file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Import fix complete!")
        return True
        
    except Exception as e:
        print(f"❌ Error during import fix: {e}")
        return False

def main():
    print("🔧 Quick Fix: Adding Missing DeckCard Import")
    print("=" * 45)
    
    if fix_missing_import():
        print()
        print("🎉 Import Fix Complete!")
        print("✅ DeckCard type should now be available")
        print()  
        print("🧪 Next Steps:")
        print("1. Run `npm start` to verify compilation")
        print("2. All TypeScript errors should be resolved")
        print("3. Test pile view functionality")
    else:
        print("❌ Import fix failed - manual intervention needed")

if __name__ == "__main__":
    main()
