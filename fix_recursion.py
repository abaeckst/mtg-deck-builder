#!/usr/bin/env python3
"""
Fix infinite recursion in getCardId function
Critical runtime error fix
"""

import os

def fix_infinite_recursion():
    filepath = "src/components/MTGOLayout.tsx"
    
    if not os.path.exists(filepath):
        print(f"❌ File not found: {filepath}")
        return False
    
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
        
        print("🔧 Fixing infinite recursion in getCardId function...")
        
        # Find and fix the broken getCardId function
        broken_function = """  const getCardId = (card: ScryfallCard | DeckCard | DeckCardInstance): string => {
    if ('instanceId' in card) return card.cardId; // DeckCardInstance - use cardId
    return card.id; // ScryfallCard or DeckCard - use id
  };
  
  // Helper to get original card ID for quantity tracking
  const getOriginalCardId = (card: ScryfallCard | DeckCard | DeckCardInstance): string => {
    if ('cardId' in card) return card.cardId;
    return card.id;
  };"""
        
        # Also try the other broken version
        broken_function_alt = """  const getCardId = (card: ScryfallCard | DeckCard | DeckCardInstance): string => {
    if ('instanceId' in card) return getCardId(card); // DeckCardInstance has id as alias
    return getCardId(card);
  };"""
        
        fixed_function = """  // Helper to safely get card ID from any card type
  const getCardId = (card: ScryfallCard | DeckCard | DeckCardInstance): string => {
    if ('instanceId' in card) {
      return card.cardId; // DeckCardInstance - use cardId (original Scryfall ID)
    }
    return card.id; // ScryfallCard or DeckCard - use id
  };
  
  // Helper to get original card ID for quantity tracking
  const getOriginalCardId = (card: ScryfallCard | DeckCard | DeckCardInstance): string => {
    if ('cardId' in card) return card.cardId;
    return card.id;
  };"""
        
        # Try to fix either version
        if broken_function in content:
            content = content.replace(broken_function, fixed_function)
            print("✅ Fixed getCardId infinite recursion (version 1)")
        elif broken_function_alt in content:
            content = content.replace(broken_function_alt, fixed_function)
            print("✅ Fixed getCardId infinite recursion (version 2)")
        else:
            # Look for any version with the recursion pattern
            import re
            pattern = r'const getCardId = \([^}]+getCardId\([^}]+\}'
            if re.search(pattern, content):
                print("⚠️ Found recursive getCardId but couldn't match exact pattern")
                print("Manual fix needed - replacing with corrected version")
                
                # Find any getCardId function and replace it
                getCardId_pattern = r'const getCardId = \(card: [^}]+\}\;'
                replacement = """const getCardId = (card: ScryfallCard | DeckCard | DeckCardInstance): string => {
    if ('instanceId' in card) {
      return card.cardId; // DeckCardInstance - use cardId (original Scryfall ID)
    }
    return card.id; // ScryfallCard or DeckCard - use id
  };"""
                
                content = re.sub(getCardId_pattern, replacement, content)
                print("✅ Replaced recursive getCardId with corrected version")
            else:
                print("❌ Could not find the problematic getCardId function")
                return False
        
        # Write the fixed content back
        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(content)
        
        print("✅ File updated successfully")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("🚨 CRITICAL FIX: Infinite Recursion in getCardId")
    print("=" * 50)
    
    success = fix_infinite_recursion()
    
    if success:
        print("\n✅ RECURSION FIXED!")
        print("The infinite loop in getCardId has been resolved.")
        print("\nTry 'npm start' again - the app should now load properly.")
    else:
        print("\n❌ MANUAL FIX NEEDED")
        print("Please check the getCardId function in MTGOLayout.tsx")
