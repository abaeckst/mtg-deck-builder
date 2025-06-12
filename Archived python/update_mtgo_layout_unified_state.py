#!/usr/bin/env python3
"""
Update MTGOLayout.tsx to integrate unified deck/sideboard state management.
This connects the unified controls from DeckArea to control both deck and sideboard areas.
"""

import re
import os

def update_mtgo_layout():
    """Update MTGOLayout.tsx with unified state management integration."""
    
    try:
        # Read current MTGOLayout.tsx
        with open('src/components/MTGOLayout.tsx', 'r', encoding='utf-8') as f:
            content = f.read()
        
        print("🔧 Updating MTGOLayout.tsx with unified deck/sideboard state management...")
        
        # 1. Update useLayout hook destructuring to include unified functions
        layout_hook_pattern = r'const\s*\{\s*([^}]+)\s*\}\s*=\s*useLayout\(\);'
        def replace_layout_hook(match):
            # Extract current destructured properties
            current_props = match.group(1)
            
            # Add unified functions if not already present
            if 'updateDeckSideboardViewMode' not in current_props:
                # Add the new unified functions
                updated_props = current_props.strip()
                if not updated_props.endswith(','):
                    updated_props += ','
                updated_props += '\n    updateDeckSideboardViewMode, // NEW: Unified deck/sideboard view mode'
                updated_props += '\n    updateDeckSideboardCardSize,  // NEW: Unified deck/sideboard card size'
                
                return f'const {{\n    {updated_props}\n  }} = useLayout();'
            return match.group(0)
        
        content = re.sub(layout_hook_pattern, replace_layout_hook, content, flags=re.DOTALL)
        
        # 2. Update DeckArea props to use unified state
        # Find DeckArea component usage
        deck_area_pattern = r'(<DeckArea\s+[^>]*viewMode={layout\.viewModes\.deck}[^>]*onViewModeChange={\([^}]+\)}[^>]*cardSize={layout\.cardSizes\.deck}[^>]*onCardSizeChange={\([^}]+\)}[^>]*/>)'
        
        def replace_deck_area_props(match):
            deck_area_content = match.group(1)
            
            # Replace old deck-specific state with unified state
            deck_area_content = re.sub(
                r'viewMode={layout\.viewModes\.deck}',
                'viewMode={layout.viewModes.deckSideboard}',
                deck_area_content
            )
            
            deck_area_content = re.sub(
                r'onViewModeChange={\([^}]+\)}',
                'onViewModeChange={updateDeckSideboardViewMode}',
                deck_area_content
            )
            
            deck_area_content = re.sub(
                r'cardSize={layout\.cardSizes\.deck}',
                'cardSize={layout.cardSizes.deckSideboard}',
                deck_area_content
            )
            
            deck_area_content = re.sub(
                r'onCardSizeChange={\([^}]+\)}',
                'onCardSizeChange={updateDeckSideboardCardSize}',
                deck_area_content
            )
            
            return deck_area_content
        
        content = re.sub(deck_area_pattern, replace_deck_area_props, content, flags=re.DOTALL)
        
        # 3. Update SideboardArea props to use unified state (read-only)
        sideboard_area_pattern = r'(<SideboardArea\s+[^>]*viewMode={layout\.viewModes\.sideboard}[^>]*onViewModeChange={\([^}]+\)}[^>]*cardSize={layout\.cardSizes\.sideboard}[^>]*onCardSizeChange={\([^}]+\)}[^>]*/>)'
        
        def replace_sideboard_area_props(match):
            sideboard_area_content = match.group(1)
            
            # Replace old sideboard-specific state with unified state (but keep callbacks for consistency)
            sideboard_area_content = re.sub(
                r'viewMode={layout\.viewModes\.sideboard}',
                'viewMode={layout.viewModes.deckSideboard}',
                sideboard_area_content
            )
            
            sideboard_area_content = re.sub(
                r'onViewModeChange={\([^}]+\)}',
                'onViewModeChange={updateDeckSideboardViewMode}',
                sideboard_area_content
            )
            
            sideboard_area_content = re.sub(
                r'cardSize={layout\.cardSizes\.sideboard}',
                'cardSize={layout.cardSizes.deckSideboard}',
                sideboard_area_content
            )
            
            sideboard_area_content = re.sub(
                r'onCardSizeChange={\([^}]+\)}',
                'onCardSizeChange={updateDeckSideboardCardSize}',
                sideboard_area_content
            )
            
            return sideboard_area_content
        
        content = re.sub(sideboard_area_pattern, replace_sideboard_area_props, content, flags=re.DOTALL)
        
        # 4. Alternative approach: Look for DeckArea and SideboardArea more broadly
        if 'updateDeckSideboardViewMode' not in content:
            print("🔧 Using alternative pattern matching approach...")
            
            # Find DeckArea component
            deck_area_start = content.find('<DeckArea')
            if deck_area_start != -1:
                # Find the end of DeckArea component
                deck_area_end = content.find('/>', deck_area_start)
                if deck_area_end == -1:
                    deck_area_end = content.find('</DeckArea>', deck_area_start)
                    if deck_area_end != -1:
                        deck_area_end = content.find('>', deck_area_end) + 1
                
                if deck_area_end != -1:
                    deck_area_section = content[deck_area_start:deck_area_end]
                    
                    # Update DeckArea props
                    updated_deck_area = deck_area_section
                    updated_deck_area = re.sub(
                        r'viewMode={[^}]+}',
                        'viewMode={layout.viewModes.deckSideboard}',
                        updated_deck_area
                    )
                    updated_deck_area = re.sub(
                        r'onViewModeChange={[^}]+}',
                        'onViewModeChange={updateDeckSideboardViewMode}',
                        updated_deck_area
                    )
                    updated_deck_area = re.sub(
                        r'cardSize={[^}]+}',
                        'cardSize={layout.cardSizes.deckSideboard}',
                        updated_deck_area
                    )
                    updated_deck_area = re.sub(
                        r'onCardSizeChange={[^}]+}',
                        'onCardSizeChange={updateDeckSideboardCardSize}',
                        updated_deck_area
                    )
                    
                    content = content[:deck_area_start] + updated_deck_area + content[deck_area_end:]
            
            # Find SideboardArea component
            sideboard_area_start = content.find('<SideboardArea')
            if sideboard_area_start != -1:
                # Find the end of SideboardArea component
                sideboard_area_end = content.find('/>', sideboard_area_start)
                if sideboard_area_end == -1:
                    sideboard_area_end = content.find('</SideboardArea>', sideboard_area_start)
                    if sideboard_area_end != -1:
                        sideboard_area_end = content.find('>', sideboard_area_end) + 1
                
                if sideboard_area_end != -1:
                    sideboard_area_section = content[sideboard_area_start:sideboard_area_end]
                    
                    # Update SideboardArea props
                    updated_sideboard_area = sideboard_area_section
                    updated_sideboard_area = re.sub(
                        r'viewMode={[^}]+}',
                        'viewMode={layout.viewModes.deckSideboard}',
                        updated_sideboard_area
                    )
                    updated_sideboard_area = re.sub(
                        r'onViewModeChange={[^}]+}',
                        'onViewModeChange={updateDeckSideboardViewMode}',
                        updated_sideboard_area
                    )
                    updated_sideboard_area = re.sub(
                        r'cardSize={[^}]+}',
                        'cardSize={layout.cardSizes.deckSideboard}',
                        updated_sideboard_area
                    )
                    updated_sideboard_area = re.sub(
                        r'onCardSizeChange={[^}]+}',
                        'onCardSizeChange={updateDeckSideboardCardSize}',
                        updated_sideboard_area
                    )
                    
                    content = content[:sideboard_area_start] + updated_sideboard_area + content[sideboard_area_end:]
        
        # 5. Add comments explaining the unified state
        if '// UNIFIED STATE MANAGEMENT' not in content:
            # Find the useLayout hook and add comment above it
            layout_hook_index = content.find('const {')
            if layout_hook_index != -1:
                # Find the start of the line
                line_start = content.rfind('\n', 0, layout_hook_index) + 1
                comment = '  // UNIFIED STATE MANAGEMENT: deck and sideboard share view mode and card size\n  '
                content = content[:line_start] + comment + content[line_start:]
        
        # Write updated content
        with open('src/components/MTGOLayout.tsx', 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ Successfully updated MTGOLayout.tsx with unified deck/sideboard state management!")
        print("📋 Changes made:")
        print("   - Added updateDeckSideboardViewMode and updateDeckSideboardCardSize to useLayout destructuring")
        print("   - Updated DeckArea props to use layout.viewModes.deckSideboard and unified callbacks")
        print("   - Updated SideboardArea props to use layout.viewModes.deckSideboard and unified callbacks")
        print("   - Both areas now synchronized: DeckArea controls affect both deck and sideboard")
        
        return True
        
    except FileNotFoundError:
        print("❌ Error: Could not find src/components/MTGOLayout.tsx")
        print("   Make sure you're running this script from the project root directory")
        return False
    except Exception as e:
        print(f"❌ Error updating MTGOLayout.tsx: {e}")
        return False

if __name__ == "__main__":
    print("🚀 MTGOLayout.tsx Unified State Integration")
    print("=" * 50)
    
    success = update_mtgo_layout()
    
    if success:
        print("\n🎯 Next steps:")
        print("1. Save the updated useLayout.ts file")
        print("2. Save the updated DeckArea.tsx file") 
        print("3. Save the updated SideboardArea.tsx file")
        print("4. Run 'npm start' to test unified state management")
        print("5. Verify that DeckArea controls affect both deck and sideboard")
        print("\n✨ Segment 1 Complete: State Synchronization + MTGO Base Styling!")
    else:
        print("\n❌ Setup incomplete. Please check the errors above and try again.")
