#!/usr/bin/env python3
"""
Phase 3G TypeScript Fixes
Resolves compilation errors to enable ListView testing
Run from project root: python fix_typescript.py
"""

import os
import sys

def apply_fixes():
    """Apply all TypeScript fixes for Phase 3G"""
    
    # Verify we're in the correct directory
    if not os.path.exists('src/types/card.ts'):
        print("❌ Error: Please run this script from the project root directory (mtg-deckbuilder)")
        return False
    
    print("🔧 Applying Phase 3G TypeScript fixes...")
    
    # Fix 1: Remove duplicate properties in card.ts
    print("1. Fixing duplicate identifiers in card.ts...")
    try:
        with open('src/types/card.ts', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remove the duplicate declarations (lines 78-80)
        old_duplicate = """  oracle_text?: string;
  power?: string;
  toughness?: string;
}"""
        
        new_without_duplicate = """}"""
        
        if old_duplicate in content:
            content = content.replace(old_duplicate, new_without_duplicate)
            print("   ✅ Removed duplicate oracle_text, power, toughness declarations")
        else:
            print("   ⚠️  Duplicate declarations not found - may already be fixed")
        
        with open('src/types/card.ts', 'w', encoding='utf-8') as f:
            f.write(content)
            
    except Exception as e:
        print(f"   ❌ Error fixing card.ts: {e}")
        return False
    
    # Fix 2: Update MTGOLayout.tsx function calls
    print("2. Fixing function signature in MTGOLayout.tsx...")
    try:
        with open('src/components/MTGOLayout.tsx', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Fix the handleDoubleClick calls in ListView components
        old_call_deck = """onDoubleClick={(card) => handleDoubleClick(card as any, 'deck', {} as React.MouseEvent)}"""
        new_call_deck = """onDoubleClick={(card) => handleDoubleClick(card as any, 'deck', { preventDefault: () => {}, stopPropagation: () => {} } as React.MouseEvent)}"""
        
        old_call_sideboard = """onDoubleClick={(card) => handleDoubleClick(card as any, 'sideboard', {} as React.MouseEvent)}"""
        new_call_sideboard = """onDoubleClick={(card) => handleDoubleClick(card as any, 'sideboard', { preventDefault: () => {}, stopPropagation: () => {} } as React.MouseEvent)}"""
        
        if old_call_deck in content:
            content = content.replace(old_call_deck, new_call_deck)
            print("   ✅ Fixed deck ListView handleDoubleClick call")
        
        if old_call_sideboard in content:
            content = content.replace(old_call_sideboard, new_call_sideboard)
            print("   ✅ Fixed sideboard ListView handleDoubleClick call")
        
        with open('src/components/MTGOLayout.tsx', 'w', encoding='utf-8') as f:
            f.write(content)
            
    except Exception as e:
        print(f"   ❌ Error fixing MTGOLayout.tsx: {e}")
        return False
    
    # Fix 3: Update ListView.tsx to handle optional properties safely
    print("3. Fixing property access in ListView.tsx...")
    try:
        with open('src/components/ListView.tsx', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Fix power property access
        old_power = """{column.id === 'power' && (
                      <span className="power">
                        {(card as any).power || '—'}
                      </span>
                    )}"""
        
        new_power = """{column.id === 'power' && (
                      <span className="power">
                        {'power' in card ? (card as any).power || '—' : '—'}
                      </span>
                    )}"""
        
        # Fix toughness property access
        old_toughness = """{column.id === 'toughness' && (
                      <span className="toughness">
                        {(card as any).toughness || '—'}
                      </span>
                    )}"""
        
        new_toughness = """{column.id === 'toughness' && (
                      <span className="toughness">
                        {'toughness' in card ? (card as any).toughness || '—' : '—'}
                      </span>
                    )}"""
        
        # Fix oracle_text property access
        old_oracle_text = """{column.id === 'text' && (
                      <span className="oracle-text" title={(card as any).oracle_text || ''}>
                        {truncateText((card as any).oracle_text, 50)}
                      </span>
                    )}"""
        
        new_oracle_text = """{column.id === 'text' && (
                      <span className="oracle-text" title={'oracle_text' in card ? (card as any).oracle_text || '' : ''}>
                        {truncateText('oracle_text' in card ? (card as any).oracle_text : '', 50)}
                      </span>
                    )}"""
        
        if old_power in content:
            content = content.replace(old_power, new_power)
            print("   ✅ Fixed power property access")
        
        if old_toughness in content:
            content = content.replace(old_toughness, new_toughness)
            print("   ✅ Fixed toughness property access")
        
        if old_oracle_text in content:
            content = content.replace(old_oracle_text, new_oracle_text)
            print("   ✅ Fixed oracle_text property access")
        
        with open('src/components/ListView.tsx', 'w', encoding='utf-8') as f:
            f.write(content)
            
    except Exception as e:
        print(f"   ❌ Error fixing ListView.tsx: {e}")
        return False
    
    print("\n🎉 All TypeScript fixes applied successfully!")
    print("\nNext steps:")
    print("1. Run 'npm start' to verify compilation")
    print("2. Test List view buttons in all three areas")
    print("3. Verify rapid double-click functionality")
    print("4. Check that all columns display data correctly")
    
    return True

if __name__ == "__main__":
    success = apply_fixes()
    if success:
        print("\n✅ Phase 3G is ready for testing!")
    else:
        print("\n❌ Some fixes failed - please check the errors above")
        sys.exit(1)