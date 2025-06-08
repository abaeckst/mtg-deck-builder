#!/usr/bin/env python3
"""
Fix DeckArea onCardSizeChange prop to use unified callback
instead of the old updateDeckSize function
"""

def fix_deckarea_callback():
    # Read current MTGOLayout.tsx
    with open('src/components/MTGOLayout.tsx', 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("🔧 Fixing DeckArea onCardSizeChange callback connection...")
    
    # Find and fix the DeckArea onCardSizeChange prop
    lines = content.split('\n')
    fixed_lines = []
    
    in_deckarea_component = False
    
    for line in lines:
        if '<DeckArea' in line:
            in_deckarea_component = True
        elif in_deckarea_component and '/>' in line:
            in_deckarea_component = False
        elif in_deckarea_component and '>' in line and not line.strip().endswith('='):
            in_deckarea_component = False
        
        # Fix the onCardSizeChange prop
        if in_deckarea_component and 'onCardSizeChange={updateDeckSize}' in line:
            print(f"  📝 Found incorrect callback: {line.strip()}")
            line = line.replace('onCardSizeChange={updateDeckSize}', 'onCardSizeChange={updateDeckSideboardCardSize}')
            print(f"  ✅ Fixed to unified callback: {line.strip()}")
        elif in_deckarea_component and 'onCardSizeChange={' in line and 'updateDeckSideboardCardSize' not in line:
            print(f"  📝 Found other callback pattern: {line.strip()}")
            # Handle other possible patterns
            if 'cardSizes.deck' in line or 'updateDeckSize' in line:
                line = line.replace('updateDeckSize', 'updateDeckSideboardCardSize')
                print(f"  ✅ Fixed callback pattern: {line.strip()}")
        
        fixed_lines.append(line)
    
    # Write the fixed content back
    fixed_content = '\n'.join(fixed_lines)
    with open('src/components/MTGOLayout.tsx', 'w', encoding='utf-8') as f:
        f.write(fixed_content)
    
    print("✅ Fixed DeckArea onCardSizeChange callback!")
    print("🔗 DeckArea now calls updateDeckSideboardCardSize (unified state)")
    
    return True

if __name__ == '__main__':
    print("🚀 Fixing DeckArea callback connection...")
    fix_deckarea_callback()
    print("\n🎯 Fix complete! Size slider should now update unified state.")
    print("\n📝 Expected flow:")
    print("   1. Slider onChange → onCardSizeChange(newSize)")
    print("   2. onCardSizeChange → updateDeckSideboardCardSize(newSize)")
    print("   3. updateDeckSideboardCardSize → layout.cardSizes.deckSideboard")
    print("   4. Both DeckArea and SideboardArea read from layout.cardSizes.deckSideboard")
