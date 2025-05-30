#!/usr/bin/env python3
"""
Fix ListView Property Access for Power, Toughness, and Oracle Text
Based on Scryfall API property names
Run from project root: python fix_listview_properties.py
"""

import os
import sys

def fix_property_access():
    """Fix the property access in ListView to use correct Scryfall API property names"""
    
    # Verify we're in the correct directory
    if not os.path.exists('src/components/ListView.tsx'):
        print("❌ Error: Please run this script from the project root directory (mtg-deckbuilder)")
        return False
    
    print("🔧 Fixing ListView property access for Scryfall API...")
    
    try:
        with open('src/components/ListView.tsx', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Fix power property access - handle both null and undefined
        old_power = """{column.id === 'power' && (
                        <span className="power">
                          {'power' in card ? (card as any).power || '—' : '—'}
                        </span>
                      )}"""
        
        new_power = """{column.id === 'power' && (
                        <span className="power">
                          {(card as any).power !== null && (card as any).power !== undefined ? (card as any).power : '—'}
                        </span>
                      )}"""
        
        # Fix toughness property access - handle both null and undefined
        old_toughness = """{column.id === 'toughness' && (
                        <span className="toughness">
                          {'toughness' in card ? (card as any).toughness || '—' : '—'}
                        </span>
                      )}"""
        
        new_toughness = """{column.id === 'toughness' && (
                        <span className="toughness">
                          {(card as any).toughness !== null && (card as any).toughness !== undefined ? (card as any).toughness : '—'}
                        </span>
                      )}"""
        
        # Fix oracle_text property access - handle both null and undefined
        old_oracle_text = """{column.id === 'text' && (
                        <span className="oracle-text" title={'oracle_text' in card ? (card as any).oracle_text || '' : ''}>
                          {truncateText('oracle_text' in card ? (card as any).oracle_text : '', 50)}
                        </span>
                      )}"""
        
        new_oracle_text = """{column.id === 'text' && (
                        <span className="oracle-text" title={(card as any).oracle_text || ''}>
                          {truncateText((card as any).oracle_text || '', 50)}
                        </span>
                      )}"""
        
        # Also add better debug logging to show actual values
        old_debug_oracle = """                console.log('Oracle text check:', {
                  'oracle_text in card': 'oracle_text' in card,
                  'card.oracle_text': (card as any).oracle_text,
                  'typeof oracle_text': typeof (card as any).oracle_text
                });"""
        
        new_debug_oracle = """                console.log('Oracle text check:', {
                  'oracle_text in card': 'oracle_text' in card,
                  'card.oracle_text': (card as any).oracle_text,
                  'typeof oracle_text': typeof (card as any).oracle_text,
                  'oracle_text is null': (card as any).oracle_text === null,
                  'oracle_text is undefined': (card as any).oracle_text === undefined
                });"""
        
        old_debug_power = """                console.log('Power check:', {
                  'power in card': 'power' in card,
                  'card.power': (card as any).power,
                  'typeof power': typeof (card as any).power
                });"""
        
        new_debug_power = """                console.log('Power check:', {
                  'power in card': 'power' in card,
                  'card.power': (card as any).power,
                  'typeof power': typeof (card as any).power,
                  'power is null': (card as any).power === null,
                  'power is undefined': (card as any).power === undefined
                });"""
        
        old_debug_toughness = """                console.log('Toughness check:', {
                  'toughness in card': 'toughness' in card,
                  'card.toughness': (card as any).toughness,
                  'typeof toughness': typeof (card as any).toughness
                });"""
        
        new_debug_toughness = """                console.log('Toughness check:', {
                  'toughness in card': 'toughness' in card,
                  'card.toughness': (card as any).toughness,
                  'typeof toughness': typeof (card as any).toughness,
                  'toughness is null': (card as any).toughness === null,
                  'toughness is undefined': (card as any).toughness === undefined
                });"""
        
        # Apply all fixes
        fixes_applied = 0
        
        if old_power in content:
            content = content.replace(old_power, new_power)
            fixes_applied += 1
            print("   ✅ Fixed power property access")
        
        if old_toughness in content:
            content = content.replace(old_toughness, new_toughness)
            fixes_applied += 1
            print("   ✅ Fixed toughness property access")
        
        if old_oracle_text in content:
            content = content.replace(old_oracle_text, new_oracle_text)
            fixes_applied += 1
            print("   ✅ Fixed oracle_text property access")
        
        # Apply debug fixes
        if old_debug_oracle in content:
            content = content.replace(old_debug_oracle, new_debug_oracle)
            print("   ✅ Enhanced oracle_text debug logging")
        
        if old_debug_power in content:
            content = content.replace(old_debug_power, new_debug_power)
            print("   ✅ Enhanced power debug logging")
        
        if old_debug_toughness in content:
            content = content.replace(old_debug_toughness, new_debug_toughness)
            print("   ✅ Enhanced toughness debug logging")
        
        if fixes_applied == 0:
            print("   ⚠️  No property access patterns found to fix")
            return False
        
        with open('src/components/ListView.tsx', 'w', encoding='utf-8') as f:
            f.write(content)
            
    except Exception as e:
        print(f"   ❌ Error fixing ListView.tsx: {e}")
        return False
    
    print(f"\n🎯 Fixed {fixes_applied} property access patterns!")
    print("\nNext steps:")
    print("1. Run 'npm start' to test the fixes")
    print("2. Switch to List view and check the console")
    print("3. See if power, toughness, and text columns now show data")
    print("4. The enhanced debug logging will show null/undefined status")
    
    return True

if __name__ == "__main__":
    success = fix_property_access()
    if success:
        print("\n✅ ListView property access should now work correctly!")
    else:
        print("\n❌ Could not fix the property access - may need manual correction")
        sys.exit(1)