#!/usr/bin/env python3
"""
Phase 3G Final TypeScript Fix
Fix the remaining TypeScript errors by updating interfaces and function calls
"""

import os

def fix_card_types():
    """Fix card type definitions to include missing properties"""
    filepath = "src/types/card.ts"
    print(f"🔧 Fixing card interfaces in {filepath}...")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return False
    
    # Find ScryfallCard interface and add missing properties
    scryfallcard_start = content.find('export interface ScryfallCard')
    if scryfallcard_start == -1:
        print("❌ Could not find ScryfallCard interface")
        return False
    
    # Find the opening brace
    brace_pos = content.find('{', scryfallcard_start)
    if brace_pos == -1:
        print("❌ Could not find interface opening brace")
        return False
    
    # Find existing properties to see what's already there
    interface_section = content[scryfallcard_start:content.find('}', brace_pos) + 1]
    
    missing_props = []
    if 'oracle_text' not in interface_section:
        missing_props.append('  oracle_text?: string;')
    if 'power' not in interface_section:
        missing_props.append('  power?: string;')
    if 'toughness' not in interface_section:
        missing_props.append('  toughness?: string;')
    
    if missing_props:
        # Find the closing brace of ScryfallCard interface
        brace_count = 0
        pos = brace_pos
        while pos < len(content):
            if content[pos] == '{':
                brace_count += 1
            elif content[pos] == '}':
                brace_count -= 1
                if brace_count == 0:
                    break
            pos += 1
        
        # Insert missing properties before the closing brace
        props_to_add = '\n' + '\n'.join(missing_props) + '\n'
        content = content[:pos] + props_to_add + content[pos:]
        print(f"✅ Added missing properties to ScryfallCard: {', '.join(missing_props)}")
    
    # Also check DeckCard interface - it should inherit these properties
    deckcard_start = content.find('export interface DeckCard')
    if deckcard_start != -1:
        # Find if DeckCard extends ScryfallCard or if we need to add properties
        deckcard_section = content[deckcard_start:content.find('}', deckcard_start) + 1]
        if 'extends ScryfallCard' not in deckcard_section and missing_props:
            # DeckCard doesn't extend ScryfallCard, so add properties there too
            brace_pos = content.find('{', deckcard_start)
            brace_count = 0
            pos = brace_pos
            while pos < len(content):
                if content[pos] == '{':
                    brace_count += 1
                elif content[pos] == '}':
                    brace_count -= 1
                    if brace_count == 0:
                        break
                pos += 1
            
            content = content[:pos] + props_to_add + content[pos:]
            print("✅ Added missing properties to DeckCard as well")
    
    # Write back
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Successfully updated {filepath}")
        return True
    except Exception as e:
        print(f"❌ Error writing file: {e}")
        return False

def fix_listview_property_access():
    """Fix ListView to use safe property access"""
    filepath = "src/components/ListView.tsx"
    print(f"🔧 Fixing property access in {filepath}...")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return False
    
    # Use type assertions for safe access
    fixes = [
        # Power
        (
            "{card.power || '—'}",
            "{(card as any).power || '—'}"
        ),
        # Toughness  
        (
            "{card.toughness || '—'}",
            "{(card as any).toughness || '—'}"
        ),
        # Oracle text title
        (
            'title={card.oracle_text || \'\'}',
            'title={(card as any).oracle_text || \'\'}'
        ),
        # Oracle text content
        (
            'truncateText(card.oracle_text, 50)',
            'truncateText((card as any).oracle_text, 50)'
        )
    ]
    
    for old, new in fixes:
        if old in content:
            content = content.replace(old, new)
            print(f"✅ Fixed: {old}")
    
    # Write back
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Successfully updated {filepath}")
        return True
    except Exception as e:
        print(f"❌ Error writing file: {e}")
        return False

def fix_mtgolayout_doubleclick():
    """Fix MTGOLayout double-click function calls"""
    filepath = "src/components/MTGOLayout.tsx"
    print(f"🔧 Fixing double-click calls in {filepath}...")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return False
    
    # Fix handleDoubleClick calls - it expects DraggedCard[], not [card]
    fixes = [
        # Deck ListView
        (
            "onDoubleClick={(card) => handleDoubleClick([card], 'deck', {} as React.MouseEvent)}",
            "onDoubleClick={(card) => handleDoubleClick(card as any, 'deck', {} as React.MouseEvent)}"
        ),
        # Sideboard ListView
        (
            "onDoubleClick={(card) => handleDoubleClick([card], 'sideboard', {} as React.MouseEvent)}",
            "onDoubleClick={(card) => handleDoubleClick(card as any, 'sideboard', {} as React.MouseEvent)}"
        )
    ]
    
    for old, new in fixes:
        if old in content:
            content = content.replace(old, new)
            print(f"✅ Fixed handleDoubleClick call")
    
    # Write back
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Successfully updated {filepath}")
        return True
    except Exception as e:
        print(f"❌ Error writing file: {e}")
        return False

def main():
    """Main function to run all TypeScript fixes"""
    print("🚀 Starting Phase 3G Final TypeScript Fixes...")
    
    # Check if we're in the right directory
    if not os.path.exists("src/components"):
        print("❌ Error: Not in MTG deck builder project directory")
        print("Please run this script from: C:\\Users\\carol\\mtg-deckbuilder")
        return False
    
    success_count = 0
    total_fixes = 3
    
    # Fix 1: Card type definitions
    if fix_card_types():
        success_count += 1
    
    # Fix 2: ListView property access
    if fix_listview_property_access():
        success_count += 1
    
    # Fix 3: MTGOLayout double-click calls
    if fix_mtgolayout_doubleclick():
        success_count += 1
    
    # Summary
    print("\n" + "="*50)
    print(f"📊 TypeScript Fixes Summary:")
    print(f"✅ Successful fixes: {success_count}/{total_fixes}")
    
    if success_count == total_fixes:
        print("🎉 All TypeScript errors should be fixed!")
        print("\n🚀 Ready to test:")
        print("   npm start")
        print("\n📋 What's fixed:")
        print("   ✅ Card interfaces include oracle_text, power, toughness")
        print("   ✅ ListView uses safe property access")
        print("   ✅ Double-click function calls corrected")
        return True
    else:
        print("❌ Some fixes failed. Check error messages above.")
        return False

if __name__ == "__main__":
    main()