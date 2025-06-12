#!/usr/bin/env python3
"""
Simple repair script for MTGOLayout.tsx syntax error
Fixes the corrupted arrow function
"""

import os

def simple_repair():
    file_path = "src/components/MTGOLayout.tsx"
    
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("🚨 SIMPLE SYNTAX REPAIR")
    print("="*30)
    
    # Simple string replacement for the specific broken syntax
    broken_text = "onSortChange={(criteria, direction) =\n          cardSize={layout.cardSizes.deckSideboard}> updateSort('sideboard', criteria, direction)}"
    
    fixed_text = """onSortChange={(criteria, direction) => updateSort('sideboard', criteria, direction)}
            cardSize={layout.cardSizes.deckSideboard}"""
    
    if broken_text in content:
        content = content.replace(broken_text, fixed_text)
        print("✅ Found and fixed the exact broken pattern")
    else:
        # Try alternative patterns
        alt_broken = "onSortChange={(criteria, direction) =\n           cardSize={layout.cardSizes.deckSideboard}> updateSort('sideboard', criteria, direction)}"
        if alt_broken in content:
            content = content.replace(alt_broken, fixed_text)
            print("✅ Found and fixed alternative broken pattern")
        else:
            print("❌ Could not find the exact broken pattern")
            print("📝 Manual fix needed:")
            print("   1. Find the line with: onSortChange={(criteria, direction) =")
            print("   2. Find the next line with: cardSize={...}> updateSort(...)")
            print("   3. Fix the arrow function: => instead of =")
            print("   4. Move cardSize to separate line")
            return
    
    # Write the repaired content back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ REPAIR COMPLETED!")
    print("   📁 Fixed: src/components/MTGOLayout.tsx")
    print("   🔧 Restored proper syntax")

if __name__ == "__main__":
    simple_repair()
