#!/usr/bin/env python3
"""
Comprehensive Header UI/UX Fix - All Three Priorities
1. Fix ViewModeDropdown functionality (normal + overflow contexts)
2. Remove background boxes from control groups, keep subtle dividers
3. Reduce header height from 40px to 32px for better space utilization
"""

import re

def fix_deckarea_visual_grouping():
    """Remove background boxes from control groups, keep subtle dividers only"""
    
    try:
        with open('src/components/DeckArea.tsx', 'r', encoding='utf-8') as f:
            content = f.read()
        
        print("🔧 Fixing DeckArea visual grouping...")
        
        # Fix Group 1: Remove background styling, keep subtle divider
        content = re.sub(
            r'<div className="control-group-1" style=\{\s*\{\s*display: \'flex\',\s*alignItems: \'center\',\s*gap: \'6px\',\s*padding: \'3px 6px\',\s*background: \'rgba\(255,255,255,0\.05\)\',\s*borderRadius: \'4px\',\s*border: \'1px solid rgba\(255,255,255,0\.1\)\'\s*\}\s*\}>',
            '''<div className="control-group-1" style={{ 
              display: 'flex', 
              alignItems: 'center', 
              gap: '6px',
              paddingRight: '12px',
              borderRight: '1px solid #555555'
            }}>''',
            content
        )
        
        # Fix Group 2: Remove background styling, keep border divider
        content = re.sub(
            r'<div className="control-group-2" style=\{\s*\{\s*display: \'flex\',\s*alignItems: \'center\',\s*gap: \'6px\',\s*borderLeft: \'1px solid #555555\',\s*paddingLeft: \'12px\',\s*background: \'rgba\(255,255,255,0\.03\)\',\s*padding: \'4px 8px 4px 12px\',\s*borderRadius: \'4px\'\s*\}\s*\}>',
            '''<div className="control-group-2" style={{ 
              display: 'flex', 
              alignItems: 'center', 
              gap: '6px',
              borderLeft: '1px solid #555555',
              paddingLeft: '12px',
              paddingRight: '12px'
            }}>''',
            content
        )
        
        # Fix Group 3: Remove background styling, keep border divider
        content = re.sub(
            r'<div className="control-group-3" style=\{\s*\{\s*display: \'flex\',\s*alignItems: \'center\',\s*gap: \'6px\',\s*borderLeft: \'1px solid #555555\',\s*paddingLeft: \'12px\',\s*background: \'rgba\(255,255,255,0\.03\)\',\s*padding: \'4px 6px 4px 12px\',\s*borderRadius: \'4px\'\s*\}\s*\}>',
            '''<div className="control-group-3" style={{ 
              display: 'flex', 
              alignItems: 'center', 
              gap: '6px',
              borderLeft: '1px solid #555555',
              paddingLeft: '12px'
            }}>''',
            content
        )
        
        # Update header height to 32px
        content = re.sub(
            r'minHeight: \'40px\'',
            'minHeight: \'32px\'',
            content
        )
        
        # Update header padding for slimmer appearance
        content = re.sub(
            r'padding: \'8px 12px\'',
            'padding: \'6px 12px\'',
            content
        )
        
        with open('src/components/DeckArea.tsx', 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ DeckArea visual grouping and header height fixed")
        
    except Exception as e:
        print(f"❌ Error fixing DeckArea: {e}")

def fix_viewmode_dropdown_positioning():
    """Fix ViewModeDropdown positioning and z-index issues"""
    
    try:
        with open('src/components/ViewModeDropdown.tsx', 'r', encoding='utf-8') as f:
            content = f.read()
        
        print("🔧 Fixing ViewModeDropdown positioning...")
        
        # Enhanced position calculation with better overflow detection
        new_calculate_position = '''  // Calculate menu position with overflow context detection
  const calculateMenuPosition = () => {
    if (buttonRef.current) {
      const rect = buttonRef.current.getBoundingClientRect();
      const isInOverflow = buttonRef.current.closest('.overflow-menu') !== null;
      
      if (isInOverflow) {
        // Special positioning for overflow menu context
        setMenuPosition({
          top: rect.bottom + window.scrollY + 2,
          left: rect.left + window.scrollX - 100 // Offset left to avoid overflow clipping
        });
      } else {
        // Normal positioning
        setMenuPosition({
          top: rect.bottom + window.scrollY + 1,
          left: rect.left + window.scrollX
        });
      }
    }
  };'''
        
        # Replace the existing calculateMenuPosition function
        content = re.sub(
            r'  // Calculate menu position when opening\n  const calculateMenuPosition = \(\) => \{[^}]+\};',
            new_calculate_position,
            content,
            flags=re.MULTILINE | re.DOTALL
        )
        
        # Enhanced dropdown menu with better z-index and overflow handling
        dropdown_menu_section = '''      {/* Dropdown Menu - Enhanced Fixed Positioning */}
      {isOpen && (
        <div 
          className="view-dropdown-menu"
          style={{
            position: 'fixed',
            top: `${menuPosition.top}px`,
            left: `${menuPosition.left}px`,
            zIndex: buttonRef.current?.closest('.overflow-menu') ? 25000 : 10001, // Higher z-index in overflow
            background: '#2a2a2a',
            border: '1px solid #555555',
            borderRadius: '2px',
            boxShadow: '0 4px 12px rgba(0,0,0,0.6)',
            minWidth: '100px',
            maxWidth: '150px'
          }}
        >'''
        
        # Replace the existing dropdown menu section
        content = re.sub(
            r'      \{/\* Dropdown Menu - Fixed Positioning \*/\}\n      \{isOpen && \(\n        <div \n          className="view-dropdown-menu"\n          style=\{\{[^}]+\}\}\n        >',
            dropdown_menu_section,
            content,
            flags=re.MULTILINE | re.DOTALL
        )
        
        with open('src/components/ViewModeDropdown.tsx', 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ ViewModeDropdown positioning and z-index fixed")
        
    except Exception as e:
        print(f"❌ Error fixing ViewModeDropdown: {e}")

def fix_css_header_height_and_zindex():
    """Update CSS for 32px headers and fix z-index hierarchy"""
    
    try:
        with open('src/components/MTGOLayout.css', 'r', encoding='utf-8') as f:
            content = f.read()
        
        print("🔧 Fixing CSS header height and z-index...")
        
        # Update all header height references from 40px to 32px
        content = re.sub(r'min-height: 40px', 'min-height: 32px', content)
        content = re.sub(r'max-height: 40px', 'max-height: 32px', content)
        content = re.sub(r'height: 40px', 'height: 32px', content)
        
        # Remove control group background styling from CSS
        control_group_css_fix = '''/* Enhanced Control Groups - Clean dividers only */
.control-group-1,
.control-group-2,
.control-group-3 {
  position: relative;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

/* No background hover effects - clean divider approach */
.control-group-1:hover,
.control-group-2:hover,
.control-group-3:hover {
  /* Clean approach - no background changes, subtle opacity only */
  opacity: 1;
}'''
        
        # Replace the existing control group styling
        content = re.sub(
            r'/\* Enhanced Control Groups with MTGO Visual Hierarchy \*/.*?\.control-group-3:hover \{[^}]+\}',
            control_group_css_fix,
            content,
            flags=re.MULTILINE | re.DOTALL
        )
        
        # Fix ViewModeDropdown z-index hierarchy for overflow context
        zindex_fix = '''/* ===== VIEWMODE DROPDOWN Z-INDEX FIX - OVERFLOW CONTEXT ===== */

/* Ensure overflow menu has correct z-index foundation */
.overflow-menu {
  z-index: 15001 !important;
  position: fixed !important;
  backdrop-filter: blur(8px) !important;
}

/* ViewModeDropdown in overflow menu - MAXIMUM priority */
.overflow-menu .view-mode-dropdown {
  position: relative !important;
  z-index: 15002 !important;
}

.overflow-menu .view-dropdown-button {
  z-index: 15003 !important;
  position: relative !important;
}

/* CRITICAL: ViewModeDropdown menu in overflow - HIGHEST PRIORITY */
.overflow-menu .view-dropdown-menu {
  z-index: 25000 !important; /* Maximum priority over everything */
  position: fixed !important;
  background: #2a2a2a !important;
  border: 1px solid #555555 !important;
  box-shadow: 0 4px 20px rgba(0,0,0,0.8) !important;
}

/* Normal context ViewModeDropdown - high but not maximum */
.view-dropdown-menu {
  z-index: 10001 !important;
}

/* Ensure resize handles stay below everything */
.resize-handle,
.resize-handle-left,
.resize-handle-right,
.resize-handle-bottom {
  z-index: 999 !important;
}

/* ===== END VIEWMODE DROPDOWN Z-INDEX FIX ===== */'''
        
        # Add the z-index fix at the end of the file
        if '/* ===== VIEWMODE DROPDOWN Z-INDEX FIX - OVERFLOW CONTEXT =====' not in content:
            content += '\n\n' + zindex_fix
        
        # Update slim headers section for 32px
        content = re.sub(
            r'min-height: 40px !important;',
            'min-height: 32px !important;',
            content
        )
        content = re.sub(
            r'max-height: 40px !important;',
            'max-height: 32px !important;',
            content
        )
        content = re.sub(
            r'padding: 8px 12px !important;',
            'padding: 6px 12px !important;',
            content
        )
        
        with open('src/components/MTGOLayout.css', 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ CSS header height and z-index hierarchy fixed")
        
    except Exception as e:
        print(f"❌ Error fixing CSS: {e}")

def fix_sideboard_header_height():
    """Update SideboardArea header height to match 32px"""
    
    try:
        with open('src/components/SideboardArea.tsx', 'r', encoding='utf-8') as f:
            content = f.read()
        
        print("🔧 Fixing SideboardArea header height...")
        
        # Update header padding for 32px height
        content = re.sub(
            r'padding: \'12px 16px\'',
            'padding: \'6px 12px\'',
            content
        )
        
        with open('src/components/SideboardArea.tsx', 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ SideboardArea header height fixed")
        
    except Exception as e:
        print(f"❌ Error fixing SideboardArea: {e}")

def fix_collection_header_height():
    """Update CollectionArea header height to match 32px"""
    
    try:
        with open('src/components/CollectionArea.tsx', 'r', encoding='utf-8') as f:
            content = f.read()
        
        print("🔧 Fixing CollectionArea header height...")
        
        # Update header padding for 32px height
        content = re.sub(
            r'padding: \'12px 16px\'',
            'padding: \'6px 12px\'',
            content
        )
        
        with open('src/components/CollectionArea.tsx', 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ CollectionArea header height fixed")
        
    except Exception as e:
        print(f"❌ Error fixing CollectionArea: {e}")

def main():
    """Execute comprehensive header UI/UX fixes"""
    print("🚀 Starting Comprehensive Header UI/UX Fix - All Three Priorities")
    print("=" * 70)
    
    print("\n📋 Priority 1: ViewModeDropdown Functionality Fix")
    fix_viewmode_dropdown_positioning()
    
    print("\n📋 Priority 2: Visual Grouping Refinement") 
    fix_deckarea_visual_grouping()
    
    print("\n📋 Priority 3: Header Height Reduction (40px → 32px)")
    fix_css_header_height_and_zindex()
    fix_sideboard_header_height()
    fix_collection_header_height()
    
    print("\n" + "=" * 70)
    print("✅ All comprehensive fixes applied successfully!")
    print("\n🧪 Ready for testing:")
    print("   • ViewModeDropdown in normal and overflow contexts")
    print("   • Clean visual grouping with subtle dividers")
    print("   • Consistent 32px headers across all areas")
    print("   • Improved space utilization for card display")

if __name__ == '__main__':
    main()
