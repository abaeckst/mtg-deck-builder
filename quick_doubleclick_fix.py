#!/usr/bin/env python3
"""
Quick fix for ListView onDoubleClick arguments
"""

import os

def fix_doubleclick_args():
    """Fix the handleDoubleClick argument count"""
    filepath = "src/components/MTGOLayout.tsx"
    print(f"🔧 Fixing handleDoubleClick arguments in {filepath}...")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return False
    
    # Fix deck ListView onDoubleClick - should remove one copy
    old_deck = """onDoubleClick={(card) => handleDoubleClick(card, 'deck')}"""
    new_deck = """onDoubleClick={(card) => {
                    if ('quantity' in card && card.quantity > 1) {
                      setMainDeck(prev => prev.map(c => c.id === card.id ? {...c, quantity: c.quantity - 1} : c));
                    } else {
                      setMainDeck(prev => prev.filter(c => c.id !== card.id));
                    }
                  }}"""
    
    if old_deck in content:
        content = content.replace(old_deck, new_deck)
        print("✅ Fixed deck ListView onDoubleClick")
    
    # Fix sideboard ListView onDoubleClick - should remove one copy
    old_sideboard = """onDoubleClick={(card) => handleDoubleClick(card, 'sideboard')}"""
    new_sideboard = """onDoubleClick={(card) => {
                    if ('quantity' in card && card.quantity > 1) {
                      setSideboard(prev => prev.map(c => c.id === card.id ? {...c, quantity: c.quantity - 1} : c));
                    } else {
                      setSideboard(prev => prev.filter(c => c.id !== card.id));
                    }
                  }}"""
    
    if old_sideboard in content:
        content = content.replace(old_sideboard, new_sideboard)
        print("✅ Fixed sideboard ListView onDoubleClick")
    
    # Write back
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Successfully updated {filepath}")
        return True
    except Exception as e:
        print(f"❌ Error writing file: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Running quick DoubleClick fix...")
    if fix_doubleclick_args():
        print("🎉 Fix complete! Try npm start now.")
    else:
        print("❌ Fix failed.")
