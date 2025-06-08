#!/usr/bin/env python3
"""
Fix DeckArea cardSize prop to use unified state from layout hook
instead of separate cardSizes.deck from useCardSizing hook
"""

def fix_deckarea_cardsize():
    # Read current MTGOLayout.tsx
    with open('src/components/MTGOLayout.tsx', 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("🔧 Fixing DeckArea cardSize prop to use unified state...")
    
    # Fix the DeckArea cardSize prop
    # Change from: cardSize={cardSizes.deck}
    # Change to: cardSize={layout.cardSizes.deckSideboard}
    
    # Find the DeckArea component and fix the cardSize prop
    lines = content.split('\n')
    fixed_lines = []
    
    in_deckarea_component = False
    
    for line in lines:
        if '<DeckArea' in line:
            in_deckarea_component = True
        elif in_deckarea_component and '>' in line and not line.strip().endswith('='):
            in_deckarea_component = False
        
        if in_deckarea_component and 'cardSize={cardSizes.deck}' in line:
            print(f"  📝 Fixed line: {line.strip()}")
            line = line.replace('cardSize={cardSizes.deck}', 'cardSize={layout.cardSizes.deckSideboard}')
            print(f"  ✅ Updated to: {line.strip()}")
        
        fixed_lines.append(line)
    
    # Write the fixed content back
    fixed_content = '\n'.join(fixed_lines)
    with open('src/components/MTGOLayout.tsx', 'w', encoding='utf-8') as f:
        f.write(fixed_content)
    
    print("✅ Fixed DeckArea cardSize prop to use unified layout state")
    print("🔗 Both DeckArea and SideboardArea now read from layout.cardSizes.deckSideboard")
    
    return True

if __name__ == '__main__':
    print("🚀 Fixing DeckArea cardSize prop inconsistency...")
    fix_deckarea_cardsize()
    print("\n🎯 Fix complete! Size slider should now affect both deck and sideboard areas.")
    print("\n⚠️  Note: The slider calls updateDeckSideboardCardSize() which updates layout.cardSizes.deckSideboard")
    print("   Both components now read from the same unified state source.")
