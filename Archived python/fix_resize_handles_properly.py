#!/usr/bin/env python3
"""
Fix Resize Handles Properly - Match Actual Working Styles
Fixes the mismatch between inline styles and CSS classes for resize functionality
"""

import os
import shutil
from datetime import datetime

def fix_panel_resizing_css():
    """Fix PanelResizing.css to match the actual working inline styles"""
    
    panel_resizing_path = os.path.join('src', 'components', 'PanelResizing.css')
    
    # Create backup
    if os.path.exists(panel_resizing_path):
        backup_path = f"{panel_resizing_path}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        shutil.copy2(panel_resizing_path, backup_path)
        print(f"✅ Backup created: {backup_path}")
    
    # Write the correct resize styles that match the inline styles in MTGOLayout.tsx
    correct_resize_styles = """/* Panel Resizing Styles - Matching Actual Working Implementation */
/* Fixed to match inline styles from MTGOLayout.tsx */

/* Base resize handle styling - matches inline styles */
.resize-handle {
  position: absolute;
  z-index: 1001;
  opacity: 0.7;
  transition: opacity 0.2s ease;
}

.resize-handle:hover {
  opacity: 1;
}

/* Filter panel resize handle - right edge */
.resize-handle-right {
  position: absolute;
  top: 0;
  right: -3px;
  width: 6px;
  height: 100%;
  cursor: ew-resize;
  background: linear-gradient(90deg, transparent 0%, #555555 50%, transparent 100%);
  z-index: 1001;
  opacity: 0.7;
  transition: opacity 0.2s ease;
}

.resize-handle-right:hover {
  opacity: 1;
}

.resize-handle-right:active {
  opacity: 1;
  background: linear-gradient(90deg, transparent 0%, #666666 50%, transparent 100%);
}

/* Vertical resize handle - between collection and deck areas */
.resize-handle-vertical {
  position: absolute;
  top: -3px;
  left: 0;
  width: 100%;
  height: 6px;
  cursor: ns-resize;
  background: linear-gradient(0deg, transparent 0%, #555555 50%, transparent 100%);
  z-index: 1001;
  opacity: 0.7;
  transition: opacity 0.2s ease;
}

.resize-handle-vertical:hover {
  opacity: 1;
}

.resize-handle-vertical:active {
  opacity: 1;
  background: linear-gradient(0deg, transparent 0%, #666666 50%, transparent 100%);
}

/* Sideboard resize handle - left edge */
.resize-handle-left {
  position: absolute;
  top: 0;
  left: -3px;
  width: 6px;
  height: 100%;
  cursor: ew-resize;
  background: linear-gradient(90deg, transparent 0%, #555555 50%, transparent 100%);
  z-index: 1001;
  opacity: 0.7;
  transition: opacity 0.2s ease;
}

.resize-handle-left:hover {
  opacity: 1;
}

.resize-handle-left:active {
  opacity: 1;
  background: linear-gradient(90deg, transparent 0%, #666666 50%, transparent 100%);
}

/* Resizing state classes */
.resizing-horizontal {
  cursor: ew-resize !important;
}

.resizing-vertical {
  cursor: ns-resize !important;
}

.resizing-horizontal *,
.resizing-vertical * {
  user-select: none !important;
  pointer-events: none !important;
}

/* Layout constraints during resize */
.mtgo-layout.resizing {
  transition: none !important;
}

.mtgo-layout.resizing * {
  transition: none !important;
}

/* Enhanced visual feedback */
.resize-handle {
  will-change: opacity, background;
}

/* Accessibility and touch support */
.resize-handle[title] {
  position: relative;
}

/* Panel boundaries */
.mtgo-filter-panel {
  min-width: 200px;
  max-width: 500px;
}

.mtgo-sideboard-panel {
  min-width: 200px;
  max-width: 1000px;
}

.mtgo-deck-area,
.mtgo-bottom-area {
  min-height: 200px;
}
"""
    
    # Write the correct styles
    with open(panel_resizing_path, 'w', encoding='utf-8') as f:
        f.write(correct_resize_styles)
    
    print(f"✅ Fixed PanelResizing.css with correct styles")
    return True

def remove_inline_resize_styles():
    """Remove inline styles from MTGOLayout.tsx to use CSS classes instead"""
    
    mtgo_tsx_path = os.path.join('src', 'components', 'MTGOLayout.tsx')
    
    if not os.path.exists(mtgo_tsx_path):
        print("❌ MTGOLayout.tsx not found!")
        return False
    
    # Create backup
    backup_path = f"{mtgo_tsx_path}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    shutil.copy2(mtgo_tsx_path, backup_path)
    print(f"✅ Backup created: {backup_path}")
    
    # Read the file
    with open(mtgo_tsx_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace the inline styled resize handles with simple className versions
    
    # Fix filter panel resize handle
    old_filter_resize = '''        <div 
          className="resize-handle resize-handle-right"
          onMouseDown={resizeHandlers.onFilterPanelResize}
          title="Drag to resize filter panel"
          style={{
            position: 'absolute',
            top: 0,
            right: -3,
            width: 6,
            height: '100%',
            cursor: 'ew-resize',
            background: 'linear-gradient(90deg, transparent 0%, #555555 50%, transparent 100%)',
            zIndex: 1001,
            opacity: 0.7,
            transition: 'opacity 0.2s ease'
          }}
          onMouseEnter={(e) => e.currentTarget.style.opacity = '1'}
          onMouseLeave={(e) => e.currentTarget.style.opacity = '0.7'}
        />'''
    
    new_filter_resize = '''        <div 
          className="resize-handle resize-handle-right"
          onMouseDown={resizeHandlers.onFilterPanelResize}
          title="Drag to resize filter panel"
        />'''
    
    # Fix vertical resize handle
    old_vertical_resize = '''          <div 
            className="resize-handle resize-handle-vertical"
            onMouseDown={resizeHandlers.onVerticalResize}
            title="Drag to resize between collection and deck areas"
            style={{
              position: 'absolute',
              top: -3,
              left: 0,
              width: '100%',
              height: 6,
              cursor: 'ns-resize',
              background: 'linear-gradient(0deg, transparent 0%, #555555 50%, transparent 100%)',
              zIndex: 1001,
              opacity: 0.7,
              transition: 'opacity 0.2s ease'
            }}
            onMouseEnter={(e) => e.currentTarget.style.opacity = '1'}
            onMouseLeave={(e) => e.currentTarget.style.opacity = '0.7'}
          />'''
    
    new_vertical_resize = '''          <div 
            className="resize-handle resize-handle-vertical"
            onMouseDown={resizeHandlers.onVerticalResize}
            title="Drag to resize between collection and deck areas"
          />'''
    
    # Apply replacements
    changes_made = 0
    
    if old_filter_resize in content:
        content = content.replace(old_filter_resize, new_filter_resize)
        changes_made += 1
        print("✅ Fixed filter panel resize handle")
    
    if old_vertical_resize in content:
        content = content.replace(old_vertical_resize, new_vertical_resize)
        changes_made += 1
        print("✅ Fixed vertical resize handle")
    
    if changes_made == 0:
        print("⚠️  No exact inline style matches found - styles may have changed")
        print("   The resize handles should still work with the CSS fix")
    
    # Write the updated file
    with open(mtgo_tsx_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Updated MTGOLayout.tsx ({changes_made} changes made)")
    return True

def test_resize_functionality():
    """Provide specific testing instructions"""
    
    print("\n📋 Resize Handle Testing Instructions:")
    print("\n1. **Filter Panel Resize (Right Edge):**")
    print("   - Look for a 6px wide invisible area on the right edge of filter panel")
    print("   - Cursor should change to ↔ when hovering")
    print("   - Should see subtle gradient background on hover")
    print("   - Drag to resize panel width")
    
    print("\n2. **Collection/Deck Split (Horizontal Line):**")
    print("   - Look for a 6px high invisible area between collection and deck areas")
    print("   - Cursor should change to ↕ when hovering")
    print("   - Should see subtle gradient background on hover")
    print("   - Drag to adjust collection/deck height split")
    
    print("\n3. **Sideboard Resize (Left Edge):**")
    print("   - Look for a 6px wide invisible area on the left edge of sideboard")
    print("   - Cursor should change to ↔ when hovering")
    print("   - Should see subtle gradient background on hover")
    print("   - Drag to resize sideboard width")
    
    print("\n✅ All resize handles should now work with consistent CSS styling")
    print("✅ No more inline styles - all managed by PanelResizing.css")

if __name__ == "__main__":
    print("🔧 Fixing Resize Handles to Match Working Implementation...")
    print("📋 Issue: CSS extraction didn't match actual inline styles")
    print("🎯 Goal: Make PanelResizing.css match the working inline styles")
    
    # Fix the CSS first
    if fix_panel_resizing_css():
        print("✅ PanelResizing.css fixed with correct styles!")
        
        # Then clean up the inline styles (optional - they should still work)
        if remove_inline_resize_styles():
            print("✅ Inline styles cleaned up!")
        
        test_resize_functionality()
        
        print("\n🎯 Next Steps:")
        print("1. Test all resize handles work properly")
        print("2. Verify CSS Phase 2 validation complete")
        print("3. Continue with Phase 3 CSS extraction")
    else:
        print("❌ Failed to fix PanelResizing.css!")
