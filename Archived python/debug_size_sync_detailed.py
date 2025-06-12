#!/usr/bin/env python3
"""
Add detailed debugging to track size synchronization issues
"""

def add_debugging():
    # Debug MTGOLayout.tsx to see what cardSize is passed to each component
    with open('src/components/MTGOLayout.tsx', 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("🔧 Adding debugging to MTGOLayout.tsx...")
    
    # Find the DeckArea and SideboardArea props and add debugging
    lines = content.split('\n')
    fixed_lines = []
    
    for i, line in enumerate(lines):
        # Add debug logging before DeckArea component
        if '<DeckArea' in line and 'mainDeck={mainDeck}' in lines[i-1:i+5]:
            fixed_lines.append('        {/* DEBUG: DeckArea cardSize prop */}')
            fixed_lines.append('        {console.log("🔧 DeckArea cardSize prop:", layout.cardSizes.deckSideboard)}')
        
        # Add debug logging before SideboardArea component  
        elif '<SideboardArea' in line and 'sideboard={sideboard}' in lines[i-1:i+5]:
            fixed_lines.append('        {/* DEBUG: SideboardArea cardSize prop */}')
            fixed_lines.append('        {console.log("🔧 SideboardArea cardSize prop:", layout.cardSizes.deckSideboard)}')
        
        fixed_lines.append(line)
    
    # Write back the content
    debug_content = '\n'.join(fixed_lines)
    with open('src/components/MTGOLayout.tsx', 'w', encoding='utf-8') as f:
        f.write(debug_content)
    
    # Now debug useLayout.ts to see if the unified state is updating
    with open('src/hooks/useLayout.ts', 'r', encoding='utf-8') as f:
        layout_content = f.read()
    
    print("🔧 Adding debugging to useLayout.ts...")
    
    # Add debug logging to updateDeckSideboardCardSize function
    layout_lines = layout_content.split('\n')
    layout_fixed = []
    
    for line in layout_lines:
        if 'const updateDeckSideboardCardSize = useCallback((size: number) => {' in line:
            layout_fixed.append(line)
            layout_fixed.append('    console.log("🔧 updateDeckSideboardCardSize called with:", size);')
        elif 'updateCardSize(\'deckSideboard\', size);' in line:
            layout_fixed.append('    console.log("🔧 About to call updateCardSize with:", size);')
            layout_fixed.append(line)
            layout_fixed.append('    console.log("🔧 updateCardSize completed");')
        else:
            layout_fixed.append(line)
    
    layout_debug_content = '\n'.join(layout_fixed)
    with open('src/hooks/useLayout.ts', 'w', encoding='utf-8') as f:
        f.write(layout_debug_content)
    
    # Debug DeckArea.tsx to see the slider behavior
    with open('src/components/DeckArea.tsx', 'r', encoding='utf-8') as f:
        deck_content = f.read()
    
    print("🔧 Adding debugging to DeckArea.tsx size slider...")
    
    deck_lines = deck_content.split('\n')
    deck_fixed = []
    
    for line in deck_lines:
        if 'onChange={(e) => onCardSizeChange(parseFloat(e.target.value))}' in line:
            deck_fixed.append('              onChange={(e) => {')
            deck_fixed.append('                const newSize = parseFloat(e.target.value);')
            deck_fixed.append('                console.log("🔧 DeckArea slider changed to:", newSize);')
            deck_fixed.append('                onCardSizeChange(newSize);')
            deck_fixed.append('              }}')
        else:
            deck_fixed.append(line)
    
    deck_debug_content = '\n'.join(deck_fixed)
    with open('src/components/DeckArea.tsx', 'w', encoding='utf-8') as f:
        f.write(deck_debug_content)
    
    # Debug SideboardArea.tsx to see if it receives prop changes
    with open('src/components/SideboardArea.tsx', 'r', encoding='utf-8') as f:
        sidebar_content = f.read()
    
    print("🔧 Adding debugging to SideboardArea.tsx...")
    
    sidebar_lines = sidebar_content.split('\n')
    sidebar_fixed = []
    
    found_component_start = False
    for line in sidebar_lines:
        if 'const SideboardArea: React.FC<SideboardAreaProps> = ({' in line:
            found_component_start = True
            sidebar_fixed.append(line)
        elif found_component_start and 'sortCards' in line and '}) => {' in line:
            sidebar_fixed.append(line)
            sidebar_fixed.append('  // DEBUG: Log cardSize prop changes')
            sidebar_fixed.append('  console.log("🔧 SideboardArea received cardSize prop:", cardSize);')
            found_component_start = False
        else:
            sidebar_fixed.append(line)
    
    sidebar_debug_content = '\n'.join(sidebar_fixed)
    with open('src/components/SideboardArea.tsx', 'w', encoding='utf-8') as f:
        f.write(sidebar_debug_content)
    
    print("✅ Added comprehensive debugging!")
    print("\n🔍 Debug points added:")
    print("  1. MTGOLayout.tsx - logs cardSize props passed to both components")
    print("  2. useLayout.ts - logs updateDeckSideboardCardSize calls")
    print("  3. DeckArea.tsx - logs slider onChange events")
    print("  4. SideboardArea.tsx - logs cardSize prop reception")
    
    return True

if __name__ == '__main__':
    print("🚀 Adding detailed size synchronization debugging...")
    add_debugging()
    print("\n🎯 Debugging added! Now test the size slider and check console for:")
    print("   1. Slider onChange events")
    print("   2. updateDeckSideboardCardSize calls") 
    print("   3. cardSize props being passed")
    print("   4. SideboardArea prop reception")
