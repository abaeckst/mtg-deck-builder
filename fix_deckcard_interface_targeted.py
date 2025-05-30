#!/usr/bin/env python3
"""
Fix DeckCard Interface - Add missing properties
More targeted approach to fix the TypeScript error
Run from project root: python fix_deckcard_interface.py
"""

import os
import sys

def fix_deckcard_interface():
    """Fix the DeckCard interface to include missing properties"""
    
    # Verify we're in the correct directory
    if not os.path.exists('src/types/card.ts'):
        print("❌ Error: Please run this script from the project root directory (mtg-deckbuilder)")
        return False
    
    print("🔧 Fixing DeckCard interface...")
    
    try:
        with open('src/types/card.ts', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find the end of the DeckCard interface and add missing properties
        # Look for the line right before the closing brace
        old_interface_end = """  // Format legality
  legal_in_format?: boolean; // Will be set based on selected format
  
  // Card text and stats (from Scryfall)
  oracle_text?: string;
  power?: string;
  toughness?: string;
  loyalty?: string;
}"""
        
        # If that pattern doesn't exist, try a simpler pattern
        if old_interface_end not in content:
            # Look for just the legal_in_format line and the closing brace
            old_interface_end = """  // Format legality
  legal_in_format?: boolean; // Will be set based on selected format
}"""
            
            new_interface_end = """  // Format legality
  legal_in_format?: boolean; // Will be set based on selected format
  
  // Card text and stats (from Scryfall)
  oracle_text?: string;
  power?: string;
  toughness?: string;
  loyalty?: string;
}"""
        else:
            # Pattern already exists, no change needed
            new_interface_end = old_interface_end
        
        if old_interface_end in content and old_interface_end != new_interface_end:
            content = content.replace(old_interface_end, new_interface_end)
            print("   ✅ Added missing properties to DeckCard interface")
        else:
            print("   ⚠️  DeckCard interface pattern not found or already updated")
            
            # Try to find any DeckCard interface and show what we found
            if "export interface DeckCard" in content:
                start_pos = content.find("export interface DeckCard")
                end_pos = content.find("}", start_pos) + 1
                found_interface = content[start_pos:end_pos]
                print("   📄 Found DeckCard interface:")
                print("   " + "\n   ".join(found_interface.split("\n")[-10:]))  # Show last 10 lines
        
        with open('src/types/card.ts', 'w', encoding='utf-8') as f:
            f.write(content)
            
    except Exception as e:
        print(f"   ❌ Error fixing card.ts: {e}")
        return False
    
    print("\n🎯 Interface fix applied!")
    print("\nNext steps:")
    print("1. Run 'npm start' to test TypeScript compilation")
    print("2. If it compiles, search for new cards to see the ListView data")
    
    return True

if __name__ == "__main__":
    success = fix_deckcard_interface()
    if success:
        print("\n✅ DeckCard interface should now include missing properties!")
    else:
        print("\n❌ Could not fix the interface automatically")
        print("Please manually add these lines to the DeckCard interface in card.ts:")
        print("  oracle_text?: string;")
        print("  power?: string;") 
        print("  toughness?: string;")
        print("  loyalty?: string;")
        sys.exit(1)