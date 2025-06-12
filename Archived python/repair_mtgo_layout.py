#!/usr/bin/env python3
"""
Emergency repair script for MTGOLayout.tsx syntax error
Fixes the corrupted arrow function and cardSize prop placement
"""

import re
import os

def repair_mtgo_layout_syntax():
    file_path = "src/components/MTGOLayout.tsx"
    
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("🚨 EMERGENCY SYNTAX REPAIR")
    print("="*40)
    
    # Fix the corrupted line that looks like:
    # onSortChange={(criteria, direction) =
    # cardSize={layout.cardSizes.deckSideboard}> updateSort('sideboard', criteria, direction)}
    
    # Pattern to find the corrupted arrow function
    corrupted_pattern = r'onSortChange=\{\(criteria,\s*direction\)\s*=\s*cardSize=\{[^}]+\}>\s*updateSort\([^}]+\)\}'
    
    # Replacement: Fix the arrow function and add cardSize as separate prop
    def fix_corrupted_function(match):
        return '''onSortChange={(criteria, direction) => updateSort('sideboard', criteria, direction)}
            cardSize={layout.cardSizes.deckSideboard}'''
    
    # Apply the fix
    original_content = content
    content = re.sub(corrupted_pattern, fix_corrupted_function, content, flags=re.MULTILINE | re.DOTALL)
    
    # Alternative pattern if the above doesn't match exactly
    if content == original_content:
        # More flexible pattern for the specific broken syntax
        alt_pattern = r'(onSortChange=\{\(criteria,\s*direction\)\s*=)\s*(cardSize=\{[^}]+\}>)\s*(updateSort\([^}]+\)\})'
        
        def fix_alt_pattern(match):
            return f'{match.group(1)}> {match.group(3)}\n            {match.group(2)[:-1]}}'
        
        content = re.sub(alt_pattern, fix_alt_pattern, content, flags=re.MULTILINE | re.DOTALL)
    
    # If still not fixed, try a more specific line-by-line approach
    if content == original_content:
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if 'onSortChange={(criteria, direction) =' in line:
                # Find the broken line and the next line
                if i + 1 < len(lines) and 'cardSize={' in lines[i + 1] and '> updateSort(' in lines[i + 1]:
                    # Fix the broken arrow function
                    next_line = lines[i + 1]
                    # Extract the updateSort call
                    update_call = next_line.split('> ')[-1]
                    # Extract the cardSize prop
                    cardsize_prop = next_line.split('> ')[0].strip()
                    
                    # Fix the current line
                    lines[i] = line + '> ' + update_call
                    # Replace next line with cardSize prop
                    lines[i + 1] = '            ' + cardsize_prop
                    
                    content = '\n'.join(lines)
                    break
    
    if content == original_content:
        print("❌ Could not auto-repair the syntax error")
        print("📝 Manual fix needed:")
        print("   1. Find line ~696 with: onSortChange={(criteria, direction) =")
        print("   2. Change to: onSortChange={(criteria, direction) => updateSort('sideboard', criteria, direction)}")
        print("   3. Add on new line: cardSize={layout.cardSizes.deckSideboard}")
        return
    
    # Write the repaired content back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ SYNTAX ERROR REPAIRED!")
    print("   📁 Fixed: src/components/MTGOLayout.tsx")
    print("   🔧 Restored: Proper arrow function syntax")
    print("   ➕ Added: cardSize prop for SideboardArea")
    print("\n📋 NEXT STEPS:")
    print("   1. Check if the app compiles successfully")
    print("   2. Test the size slider synchronization")
    print("   3. If still issues, check console for any remaining errors")

if __name__ == "__main__":
    repair_mtgo_layout_syntax()
