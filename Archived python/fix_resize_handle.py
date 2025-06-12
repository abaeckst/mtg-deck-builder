#!/usr/bin/env python3
"""
Fix resize handle regression and overflow menu z-index issues.
This script addresses the core problems:
1. SideboardArea.tsx inline styles overriding CSS (6px -> 20px width)
2. Z-index conflicts between inline styles and CSS
3. Sideboard content overlapping resize handles
4. Overflow menu appearing behind sideboard
"""

import re

def fix_sideboard_resize_handle():
    """Fix SideboardArea.tsx resize handle inline styles"""
    
    try:
        with open('src/components/SideboardArea.tsx', 'r', encoding='utf-8') as f:
            content = f.read()
        
        print("🔧 Fixing SideboardArea.tsx resize handle...")
        
        # Find and replace the problematic resize handle div
        old_resize_handle = r'''<div 
        className="resize-handle resize-handle-left"
        onMouseDown={onSideboardResize}
        title="Drag to resize sideboard"
        style={{
          position: 'absolute',
          top: 0,
          left: -3,
          width: 6,
          height: '100%',
          cursor: 'ew-resize',
          background: 'linear-gradient\(90deg, transparent 0%, #555555 50%, transparent 100%\)',
          zIndex: 1001,
          opacity: 0\.7,
          transition: 'opacity 0\.2s ease'
        }}
        onMouseEnter={\(e\) => e\.currentTarget\.style\.opacity = '1'}
        onMouseLeave={\(e\) => e\.currentTarget\.style\.opacity = '0\.7'}
      />'''
        
        # New resize handle with corrected styles - use CSS classes instead of inline overrides
        new_resize_handle = '''<div 
        className="resize-handle resize-handle-left"
        onMouseDown={onSideboardResize}
        title="Drag to resize sideboard"
      />'''
        
        # Replace the resize handle
        content = re.sub(
            r'<div\s+className="resize-handle resize-handle-left"[^>]*?onMouseDown={onSideboardResize}[^>]*?>.*?</div>',
            new_resize_handle,
            content,
            flags=re.DOTALL | re.MULTILINE
        )
        
        # Also ensure sideboard content doesn't overlap resize handle
        old_content_div = r'<div className="sideboard-content">'
        new_content_div = '''<div className="sideboard-content" style={{ paddingLeft: '12px' }}>'''
        
        content = content.replace(old_content_div, new_content_div)
        
        with open('src/components/SideboardArea.tsx', 'w', encoding='utf-8') as f:
            f.write(content)
            
        print("✅ SideboardArea.tsx resize handle fixed")
        return True
        
    except Exception as e:
        print(f"❌ Error fixing SideboardArea.tsx: {e}")
        return False

def fix_css_resize_handles():
    """Clean up MTGOLayout.css resize handle definitions and z-index conflicts"""
    
    try:
        with open('src/components/MTGOLayout.css', 'r', encoding='utf-8') as f:
            content = f.read()
        
        print("🔧 Cleaning up MTGOLayout.css resize handle definitions...")
        
        # Remove redundant/conflicting resize handle sections
        # Keep only the clean, consolidated version
        
        # Remove old conflicting definitions
        content = re.sub(
            r'/\* ===== ENHANCED RESIZE HANDLES.*?===== END ENHANCED RESIZE HANDLES ===== \*/',
            '',
            content,
            flags=re.DOTALL
        )
        
        # Remove nuclear z-index overrides that are breaking things
        content = re.sub(
            r'/\* ===== NUCLEAR Z-INDEX OVERRIDE.*?===== END NUCLEAR Z-INDEX OVERRIDE ===== \*/',
            '',
            content,
            flags=re.DOTALL
        )
        
        # Remove the resize handle width fix that might be conflicting
        content = re.sub(
            r'/\* RESIZE HANDLE WIDTH FIX.*?left: -10px !important;\s*}',
            '',
            content,
            flags=re.DOTALL
        )
        
        # Add clean, consistent resize handle definition
        clean_resize_css = '''
/* ===== CLEAN RESIZE HANDLES - 20px HIT ZONES ===== */

/* Base resize handle styles */
.resize-handle {
  position: absolute !important;
  background-color: transparent !important;
  transition: background-color 0.2s ease !important;
  z-index: 1500 !important; /* Below dropdowns but above content */
  pointer-events: auto !important;
}

.resize-handle:hover {
  background-color: rgba(59, 130, 246, 0.3) !important;
}

.resize-handle:active {
  background-color: rgba(59, 130, 246, 0.5) !important;
}

/* Large hit zone resize handles - 20px wide/tall for easy interaction */
.resize-handle-right {
  top: 0 !important;
  right: -10px !important; /* Centered on border */
  width: 20px !important; /* LARGE hit zone */
  height: 100% !important;
  cursor: ew-resize !important;
}

.resize-handle-left {
  top: 0 !important;
  left: -10px !important; /* Centered on border */
  width: 20px !important; /* LARGE hit zone */
  height: 100% !important;
  cursor: ew-resize !important;
}

.resize-handle-bottom {
  bottom: -10px !important; /* Centered on border */
  left: 0 !important;
  right: 0 !important;
  height: 20px !important; /* LARGE hit zone */
  cursor: ns-resize !important;
}

.resize-handle-vertical {
  top: -10px !important; /* Centered on border */
  left: 0 !important;
  right: 0 !important;
  height: 20px !important; /* LARGE hit zone */
  cursor: ns-resize !important;
}

/* ===== END CLEAN RESIZE HANDLES ===== */
'''
        
        # Insert clean resize handle CSS before the end of the file
        content = content.rstrip() + '\n' + clean_resize_css + '\n'
        
        with open('src/components/MTGOLayout.css', 'w', encoding='utf-8') as f:
            f.write(content)
            
        print("✅ MTGOLayout.css resize handles cleaned up")
        return True
        
    except Exception as e:
        print(f"❌ Error fixing MTGOLayout.css: {e}")
        return False

def fix_overflow_menu_zindex():
    """Fix overflow menu z-index to appear above sideboard"""
    
    try:
        with open('src/components/MTGOLayout.css', 'r', encoding='utf-8') as f:
            content = f.read()
        
        print("🔧 Fixing overflow menu z-index...")
        
        # Add clean z-index fix for overflow menu
        overflow_zindex_fix = '''
/* ===== OVERFLOW MENU Z-INDEX FIX ===== */

/* Ensure overflow menu appears above all content */
.overflow-menu-container {
  z-index: 2000 !important;
  position: relative !important;
}

.overflow-menu {
  z-index: 2001 !important;
  position: fixed !important;
}

/* ViewModeDropdown in overflow menu */
.overflow-menu .view-mode-dropdown {
  z-index: 2002 !important;
}

.overflow-menu .view-dropdown-menu {
  z-index: 2003 !important;
  position: fixed !important;
}

/* Force sideboard to lower z-index */
.mtgo-sideboard-panel {
  z-index: 100 !important;
}

.sideboard-content {
  z-index: 100 !important;
}

/* ===== END OVERFLOW MENU Z-INDEX FIX ===== */
'''
        
        # Add the fix to the end of the file
        content = content.rstrip() + '\n' + overflow_zindex_fix + '\n'
        
        with open('src/components/MTGOLayout.css', 'w', encoding='utf-8') as f:
            f.write(content)
            
        print("✅ Overflow menu z-index fixed")
        return True
        
    except Exception as e:
        print(f"❌ Error fixing overflow menu z-index: {e}")
        return False

def main():
    """Execute all fixes"""
    print("🚀 Starting resize handle and overflow menu fixes...")
    print()
    
    success_count = 0
    
    if fix_sideboard_resize_handle():
        success_count += 1
    
    if fix_css_resize_handles():
        success_count += 1
        
    if fix_overflow_menu_zindex():
        success_count += 1
    
    print()
    if success_count == 3:
        print("✅ ALL FIXES COMPLETED SUCCESSFULLY!")
        print()
        print("Changes made:")
        print("1. Fixed SideboardArea.tsx resize handle - removed 6px width override")
        print("2. Cleaned up conflicting CSS resize handle definitions")
        print("3. Fixed overflow menu z-index to appear above sideboard")
        print()
        print("Next steps:")
        print("1. Test resize handle functionality (should be easy to find cursor)")
        print("2. Test overflow menu (should appear above sideboard)")
        print("3. Verify no regressions in core functionality")
    else:
        print(f"⚠️ Only {success_count}/3 fixes completed successfully")
        print("Check error messages above for details")

if __name__ == "__main__":
    main()
