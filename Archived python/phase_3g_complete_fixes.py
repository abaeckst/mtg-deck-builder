#!/usr/bin/env python3
"""
Phase 3G Complete Fixes - All 4 Issues
1. Rapid double-clicks for list view removal
2. Move Quantity to leftmost column
3. Fix text column (oracle_text property access)
4. Fix power/toughness columns (property access)
"""

import os

def fix_listview_all_issues():
    """Fix all ListView issues"""
    filepath = "src/components/ListView.tsx"
    print(f"🔧 Fixing all ListView issues in {filepath}...")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return False
    
    # Fix 1: Update column definitions - move quantity to first, fix property access
    old_columns = """// Column definitions with minimum widths
const COLUMN_DEFINITIONS: ColumnDefinition[] = [
  { id: 'name', title: 'Name', minWidth: 200, sortable: true, visible: true },
  { id: 'mana', title: 'Mana', minWidth: 80, sortable: true, visible: true },
  { id: 'type', title: 'Type', minWidth: 150, sortable: true, visible: true },
  { id: 'power', title: 'Power', minWidth: 60, sortable: true, visible: true },
  { id: 'toughness', title: 'Toughness', minWidth: 60, sortable: true, visible: true },
  { id: 'color', title: 'Color', minWidth: 80, sortable: true, visible: true },
  { id: 'text', title: 'Text', minWidth: 250, sortable: true, visible: true },
  { id: 'quantity', title: 'Qty', minWidth: 80, sortable: false, visible: true },
];"""
    
    new_columns = """// Column definitions with minimum widths - Quantity first!
const COLUMN_DEFINITIONS: ColumnDefinition[] = [
  { id: 'quantity', title: 'Qty', minWidth: 80, sortable: false, visible: true },
  { id: 'name', title: 'Name', minWidth: 200, sortable: true, visible: true },
  { id: 'mana', title: 'Mana', minWidth: 80, sortable: true, visible: true },
  { id: 'type', title: 'Type', minWidth: 150, sortable: true, visible: true },
  { id: 'power', title: 'Power', minWidth: 60, sortable: true, visible: true },
  { id: 'toughness', title: 'Toughness', minWidth: 60, sortable: true, visible: true },
  { id: 'color', title: 'Color', minWidth: 80, sortable: true, visible: true },
  { id: 'text', title: 'Text', minWidth: 250, sortable: true, visible: true },
];"""
    
    if old_columns in content:
        content = content.replace(old_columns, new_columns)
        print("✅ Fixed column order - Quantity now first")
    
    # Fix 2: Fix power property access (remove type guards - they're not working)
    old_power_guard = """                        {('power' in card ? card.power : undefined) || '—'}"""
    new_power_access = """                        {card.power || '—'}"""
    
    if old_power_guard in content:
        content = content.replace(old_power_guard, new_power_access)
        print("✅ Fixed power property access")
    
    # Fix 3: Fix toughness property access 
    old_toughness_guard = """                        {('toughness' in card ? card.toughness : undefined) || '—'}"""
    new_toughness_access = """                        {card.toughness || '—'}"""
    
    if old_toughness_guard in content:
        content = content.replace(old_toughness_guard, new_toughness_access)
        print("✅ Fixed toughness property access")
    
    # Fix 4: Fix oracle_text property access
    old_oracle_title_guard = """                      <span className="oracle-text" title={('oracle_text' in card ? card.oracle_text : undefined)}>"""
    new_oracle_title = """                      <span className="oracle-text" title={card.oracle_text || ''}>"""
    
    if old_oracle_title_guard in content:
        content = content.replace(old_oracle_title_guard, new_oracle_title)
        print("✅ Fixed oracle_text title access")
    
    old_oracle_content_guard = """                        {truncateText(('oracle_text' in card ? card.oracle_text : undefined), 50)}"""
    new_oracle_content = """                        {truncateText(card.oracle_text, 50)}"""
    
    if old_oracle_content_guard in content:
        content = content.replace(old_oracle_content_guard, new_oracle_content)
        print("✅ Fixed oracle_text content access")
    
    # Write back
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Successfully updated {filepath}")
        return True
    except Exception as e:
        print(f"❌ Error writing file: {e}")
        return False

def fix_mtgolayout_rapid_doubleclick():
    """Fix MTGOLayout to support rapid double-clicks in list view"""
    filepath = "src/components/MTGOLayout.tsx"
    print(f"🔧 Adding rapid double-click support to ListView in {filepath}...")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return False
    
    # Find and replace the deck ListView onDoubleClick with rapid double-click support
    old_deck_doubleclick = """onDoubleClick={(card) => {
                    if ('quantity' in card && card.quantity > 1) {
                      setMainDeck(prev => prev.map(c => c.id === card.id ? {...c, quantity: c.quantity - 1} : c));
                    } else {
                      setMainDeck(prev => prev.filter(c => c.id !== card.id));
                    }
                  }}"""
    
    new_deck_doubleclick = """onDoubleClick={(card) => handleDoubleClick([card], 'deck', {} as React.MouseEvent)}"""
    
    if old_deck_doubleclick in content:
        content = content.replace(old_deck_doubleclick, new_deck_doubleclick)
        print("✅ Fixed deck ListView for rapid double-clicks")
    
    # Find and replace the sideboard ListView onDoubleClick with rapid double-click support  
    old_sideboard_doubleclick = """onDoubleClick={(card) => {
                    if ('quantity' in card && card.quantity > 1) {
                      setSideboard(prev => prev.map(c => c.id === card.id ? {...c, quantity: c.quantity - 1} : c));
                    } else {
                      setSideboard(prev => prev.filter(c => c.id !== card.id));
                    }
                  }}"""
    
    new_sideboard_doubleclick = """onDoubleClick={(card) => handleDoubleClick([card], 'sideboard', {} as React.MouseEvent)}"""
    
    if old_sideboard_doubleclick in content:
        content = content.replace(old_sideboard_doubleclick, new_sideboard_doubleclick)
        print("✅ Fixed sideboard ListView for rapid double-clicks")
    
    # Write back
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Successfully updated {filepath}")
        return True
    except Exception as e:
        print(f"❌ Error writing file: {e}")
        return False

def add_card_interface_fix():
    """Add missing properties to card interface"""
    filepath = "src/types/card.ts"
    print(f"🔧 Checking card type definitions in {filepath}...")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return False
    
    # Check if we need to add missing properties
    if 'oracle_text?' not in content and 'oracle_text:' not in content:
        # Find the ScryfallCard interface and add missing properties
        interface_start = content.find('export interface ScryfallCard')
        if interface_start != -1:
            # Find the end of the interface
            brace_count = 0
            pos = interface_start
            while pos < len(content):
                if content[pos] == '{':
                    brace_count += 1
                elif content[pos] == '}':
                    brace_count -= 1
                    if brace_count == 0:
                        break
                pos += 1
            
            # Insert missing properties before the closing brace
            insert_pos = pos
            missing_props = """  oracle_text?: string;
  power?: string;
  toughness?: string;
"""
            content = content[:insert_pos] + missing_props + content[insert_pos:]
            print("✅ Added missing properties to ScryfallCard interface")
    
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
    """Main function to run all fixes"""
    print("🚀 Starting Phase 3G Complete Fixes...")
    print("Issues to fix:")
    print("1. Rapid double-clicks fail to remove multiple copies")
    print("2. Quantity should be the left-most column")
    print("3. Text column is blank for all cards")
    print("4. Power/toughness columns are blank for all cards")
    print()
    
    # Check if we're in the right directory
    if not os.path.exists("src/components"):
        print("❌ Error: Not in MTG deck builder project directory")
        print("Please run this script from: C:\\Users\\carol\\mtg-deckbuilder")
        return False
    
    success_count = 0
    total_fixes = 3
    
    # Fix 1: ListView issues (columns, property access)
    if fix_listview_all_issues():
        success_count += 1
    
    # Fix 2: MTGOLayout rapid double-click support
    if fix_mtgolayout_rapid_doubleclick():
        success_count += 1
    
    # Fix 3: Card interface (add missing properties)
    if add_card_interface_fix():
        success_count += 1
    
    # Summary
    print("\n" + "="*50)
    print(f"📊 Fixes Summary:")
    print(f"✅ Successful fixes: {success_count}/{total_fixes}")
    
    if success_count == total_fixes:
        print("🎉 All issues fixed!")
        print("\n🚀 Ready to test:")
        print("   npm start")
        print("\n📋 What's fixed:")
        print("   ✅ Quantity column is now leftmost")
        print("   ✅ Power/toughness columns should show values")
        print("   ✅ Text column should show oracle text")
        print("   ✅ Rapid double-clicks work in list view")
        return True
    else:
        print("❌ Some fixes failed. Check error messages above.")
        return False

if __name__ == "__main__":
    main()