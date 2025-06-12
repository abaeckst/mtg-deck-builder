#!/usr/bin/env python3
"""
Fix MTGOLayout.tsx to use unified deck/sideboard state management.
"""

import re
import os

def fix_mtgo_layout():
    """Fix MTGOLayout.tsx with proper unified state usage."""
    
    file_path = 'src/components/MTGOLayout.tsx'
    
    if not os.path.exists(file_path):
        print(f"❌ Error: Could not find {file_path}")
        print("   Make sure you're running this script from the project root directory")
        return False
    
    try:
        # Read current MTGOLayout.tsx
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print("🔧 Fixing MTGOLayout.tsx unified state integration...")
        
        # 1. Fix the useLayout destructuring (find the existing pattern)
        old_destructuring_pattern = r'const\s*\{\s*([^}]+)\s*\}\s*=\s*useLayout\(\);'
        
        new_destructuring = '''const {
    layout,
    updatePanelDimensions,
    updateDeckAreaHeightByPixels,
    updatePreviewPane,
    updateViewMode,
    updateCardSize,
    updateDeckSideboardViewMode, // NEW: Unified deck/sideboard view mode
    updateDeckSideboardCardSize, // NEW: Unified deck/sideboard card size
    resetLayout,
    togglePreviewPane,
    constraints,
    getCalculatedHeights,
  } = useLayout();'''
        
        content = re.sub(old_destructuring_pattern, new_destructuring, content, flags=re.DOTALL)
        
        # 2. Update DeckArea viewMode prop
        content = re.sub(
            r'viewMode={layout\.viewModes\.deck}',
            'viewMode={layout.viewModes.deckSideboard}',
            content
        )
        
        # 3. Update DeckArea onViewModeChange prop
        content = re.sub(
            r'onViewModeChange={\([^}]+\)\s*=>\s*updateViewMode\([\'"]deck[\'"],\s*\w+\)}',
            'onViewModeChange={updateDeckSideboardViewMode}',
            content
        )
        
        # Alternative pattern for onViewModeChange
        content = re.sub(
            r'onViewModeChange={\([^}]+\)\s*=>\s*\{\s*clearSelection\(\);\s*updateViewMode\([\'"]deck[\'"],\s*\w+\);\s*\}}',
            'onViewModeChange={(mode) => { clearSelection(); updateDeckSideboardViewMode(mode); }}',
            content
        )
        
        # 4. Update DeckArea cardSize prop
        content = re.sub(
            r'cardSize={layout\.cardSizes\.deck}',
            'cardSize={layout.cardSizes.deckSideboard}',
            content
        )
        
        # 5. Update DeckArea onCardSizeChange prop
        content = re.sub(
            r'onCardSizeChange={\([^}]+\)\s*=>\s*updateCardSize\([\'"]deck[\'"],\s*\w+\)}',
            'onCardSizeChange={updateDeckSideboardCardSize}',
            content
        )
        
        # 6. Update SideboardArea viewMode prop
        content = re.sub(
            r'viewMode={layout\.viewModes\.sideboard}',
            'viewMode={layout.viewModes.deckSideboard}',
            content
        )
        
        # 7. Update SideboardArea onViewModeChange prop
        content = re.sub(
            r'onViewModeChange={\([^}]+\)\s*=>\s*updateViewMode\([\'"]sideboard[\'"],\s*\w+\)}',
            'onViewModeChange={updateDeckSideboardViewMode}',
            content
        )
        
        # Alternative pattern for sideboard onViewModeChange
        content = re.sub(
            r'onViewModeChange={\([^}]+\)\s*=>\s*\{\s*clearSelection\(\);\s*updateViewMode\([\'"]sideboard[\'"],\s*\w+\);\s*\}}',
            'onViewModeChange={(mode) => { clearSelection(); updateDeckSideboardViewMode(mode); }}',
            content
        )
        
        # 8. Update SideboardArea cardSize prop
        content = re.sub(
            r'cardSize={layout\.cardSizes\.sideboard}',
            'cardSize={layout.cardSizes.deckSideboard}',
            content
        )
        
        # 9. Update SideboardArea onCardSizeChange prop
        content = re.sub(
            r'onCardSizeChange={\([^}]+\)\s*=>\s*updateCardSize\([\'"]sideboard[\'"],\s*\w+\)}',
            'onCardSizeChange={updateDeckSideboardCardSize}',
            content
        )
        
        # Write updated content
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ Successfully fixed MTGOLayout.tsx unified state integration!")
        print("📋 Changes made:")
        print("   - Fixed useLayout destructuring with unified functions")
        print("   - Updated DeckArea to use layout.viewModes.deckSideboard")
        print("   - Updated DeckArea to use updateDeckSideboardViewMode")
        print("   - Updated DeckArea to use layout.cardSizes.deckSideboard")
        print("   - Updated DeckArea to use updateDeckSideboardCardSize")
        print("   - Updated SideboardArea to use unified state (same changes)")
        
        return True
        
    except Exception as e:
        print(f"❌ Error fixing MTGOLayout.tsx: {e}")
        return False

if __name__ == "__main__":
    print("🚀 MTGOLayout.tsx Unified State Fix")
    print("=" * 40)
    
    success = fix_mtgo_layout()
    
    if success:
        print("\n🎯 Next steps:")
        print("1. Save the corrected useLayout.ts file")
        print("2. Save the DeckArea.tsx file") 
        print("3. Save the SideboardArea.tsx file")
        print("4. Run 'npm start' to test unified state management")
        print("\n✨ Segment 1 should now compile and work correctly!")
    else:
        print("\n❌ Fix incomplete. Please check the errors above and try again.")
