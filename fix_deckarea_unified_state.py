#!/usr/bin/env python3
"""
Fix DeckArea to use unified deck/sideboard state instead of separate state.
Root cause: DeckArea using cardSizes.deck + updateDeckSize (old) 
instead of layout.cardSizes.deckSideboard + updateDeckSideboardCardSize (unified)
"""

import re

def fix_deckarea_unified_state():
    mtgo_layout_path = "src/components/MTGOLayout.tsx"
    
    try:
        with open(mtgo_layout_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print("🔧 Fixing DeckArea unified state connection...")
        
        # Find the DeckArea component in MTGOLayout
        deckarea_pattern = r'(<DeckArea\s+[^>]*?>)'
        deckarea_match = re.search(deckarea_pattern, content, re.DOTALL)
        
        if not deckarea_match:
            print("❌ Could not find DeckArea component")
            return False
        
        # Fix 1: Change cardSize prop from cardSizes.deck to layout.cardSizes.deckSideboard
        print("🔧 Step 1: Updating cardSize prop...")
        content = re.sub(
            r'cardSize=\{cardSizes\.deck\}',
            'cardSize={layout.cardSizes.deckSideboard}',
            content
        )
        
        # Fix 2: Change onCardSizeChange prop from updateDeckSize to updateDeckSideboardCardSize  
        print("🔧 Step 2: Updating onCardSizeChange callback...")
        content = re.sub(
            r'onCardSizeChange=\{updateDeckSize\}',
            'onCardSizeChange={updateDeckSideboardCardSize}',
            content
        )
        
        # Verify the changes were made
        if 'cardSize={layout.cardSizes.deckSideboard}' not in content:
            print("❌ Failed to update cardSize prop")
            return False
            
        if 'onCardSizeChange={updateDeckSideboardCardSize}' not in content:
            print("❌ Failed to update onCardSizeChange callback")
            return False
        
        # Save the file
        with open(mtgo_layout_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ DeckArea unified state connection fixed!")
        print("   • cardSize: cardSizes.deck → layout.cardSizes.deckSideboard")
        print("   • onCardSizeChange: updateDeckSize → updateDeckSideboardCardSize")
        print("   • Both DeckArea and SideboardArea now use unified state")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = fix_deckarea_unified_state()
    if success:
        print("\n🎯 Root cause resolved! Size slider should now synchronize between deck and sideboard.")
        print("🧪 Test the size slider in deck area - it should now affect both areas.")
    else:
        print("\n❌ Fix failed. Manual correction needed.")
