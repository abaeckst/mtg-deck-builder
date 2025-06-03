#!/usr/bin/env python3
"""
Add Debug Logging to ListView Component
Run from project root: python debug_listview.py
"""

import os
import sys

def add_debug_logging():
    """Add detailed debug logging to ListView component"""
    
    # Verify we're in the correct directory
    if not os.path.exists('src/components/ListView.tsx'):
        print("❌ Error: Please run this script from the project root directory (mtg-deckbuilder)")
        return False
    
    print("🔧 Adding debug logging to ListView component...")
    
    try:
        with open('src/components/ListView.tsx', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find the existing tbody section and replace it with debug version
        old_tbody_start = """          {/* Body */}
          <tbody>
            {cards.map((card, index) => (
              <tr"""
        
        new_tbody_start = """          {/* Body - DEBUG VERSION */}
          <tbody>
            {cards.map((card, index) => {
              // DETAILED DEBUG LOGGING - Add this for first card only
              if (index === 0) {
                console.log('🔍 DETAILED CARD ANALYSIS:');
                console.log('Card object:', card);
                console.log('All card properties:', Object.keys(card));
                console.log('Oracle text check:', {
                  'oracle_text in card': 'oracle_text' in card,
                  'card.oracle_text': (card as any).oracle_text,
                  'typeof oracle_text': typeof (card as any).oracle_text
                });
                console.log('Power check:', {
                  'power in card': 'power' in card,
                  'card.power': (card as any).power,
                  'typeof power': typeof (card as any).power
                });
                console.log('Toughness check:', {
                  'toughness in card': 'toughness' in card,
                  'card.toughness': (card as any).toughness,
                  'typeof toughness': typeof (card as any).toughness
                });
                
                // Check for alternative property names
                console.log('Alternative properties check:', {
                  'text': (card as any).text,
                  'oracle': (card as any).oracle,
                  'rules_text': (card as any).rules_text,
                  'card_text': (card as any).card_text
                });
              }
              
              return (
                <tr"""
        
        if old_tbody_start in content:
            content = content.replace(old_tbody_start, new_tbody_start)
            print("   ✅ Added detailed debug logging to ListView")
        else:
            print("   ⚠️  Could not find tbody section to modify")
            return False
        
        # Also need to change the closing part from )} to })}
        old_closing = """              )}
            ))}
          </tbody>"""
        
        new_closing = """              );
            })}
          </tbody>"""
        
        if old_closing in content:
            content = content.replace(old_closing, new_closing)
            print("   ✅ Fixed closing syntax for debug version")
        
        with open('src/components/ListView.tsx', 'w', encoding='utf-8') as f:
            f.write(content)
            
    except Exception as e:
        print(f"   ❌ Error modifying ListView.tsx: {e}")
        return False
    
    print("\n🎯 Debug logging added successfully!")
    print("\nNext steps:")
    print("1. Run 'npm start' to restart the application")
    print("2. Switch to List view in any area")
    print("3. Open browser DevTools → Console")
    print("4. Look for the detailed card analysis output")
    print("5. Share the console output with me")
    
    return True

if __name__ == "__main__":
    success = add_debug_logging()
    if success:
        print("\n✅ ListView debug logging ready!")
    else:
        print("\n❌ Failed to add debug logging")
        sys.exit(1)