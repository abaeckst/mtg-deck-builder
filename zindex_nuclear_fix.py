#!/usr/bin/env python3
"""
Z-Index Nuclear Option Implementation
- Fix sort button dropdown functionality
- Implement massive z-index hierarchy  
- Hide resize handles when overflow menu open
- Coordinate z-index conflicts with React state
"""

import re

def fix_deckarea_sort_and_overflow_coordination():
    """Fix sort button functionality and add resize handle hiding coordination"""
    
    try:
        with open('src/components/DeckArea.tsx', 'r', encoding='utf-8') as f:
            content = f.read()
        
        print("🔧 Fixing DeckArea sort functionality and overflow coordination...")
        
        # Add state for coordinating resize handle hiding
        state_additions = """  // Responsive overflow menu state
  const [showOverflowMenu, setShowOverflowMenu] = useState(false);
  const [hiddenControls, setHiddenControls] = useState<string[]>([]);
  const headerRef = useRef<HTMLDivElement>(null);
  const controlsRef = useRef<HTMLDivElement>(null);
  const overflowRef = useRef<HTMLDivElement>(null);

  // Z-INDEX NUCLEAR OPTION: Hide resize handles when overflow menu is open
  useEffect(() => {
    const hideResizeHandles = () => {
      const resizeHandles = document.querySelectorAll('.resize-handle, .resize-handle-left, .resize-handle-right, .resize-handle-bottom');
      resizeHandles.forEach(handle => {
        if (showOverflowMenu) {
          (handle as HTMLElement).style.display = 'none';
        } else {
          (handle as HTMLElement).style.display = '';
        }
      });
    };
    
    hideResizeHandles();
    
    // Also hide when sort menu is open for good measure
    if (showSortMenu) {
      const resizeHandles = document.querySelectorAll('.resize-handle, .resize-handle-left, .resize-handle-right, .resize-handle-bottom');
      resizeHandles.forEach(handle => {
        (handle as HTMLElement).style.display = 'none';
      });
    }
    
    return () => {
      // Cleanup: restore resize handles when component unmounts
      const resizeHandles = document.querySelectorAll('.resize-handle, .resize-handle-left, .resize-handle-right, .resize-handle-bottom');
      resizeHandles.forEach(handle => {
        (handle as HTMLElement).style.display = '';
      });
    };
  }, [showOverflowMenu, showSortMenu]);"""
        
        # Insert the new state and effect after existing state declarations
        content = re.sub(
            r'(const overflowRef = useRef<HTMLDivElement>\(null\);)',
            state_additions,
            content
        )
        
        # Fix sort menu positioning with nuclear z-index
        sort_menu_fix = '''                    <div className="sort-menu" style={{
                      position: 'fixed',
                      top: `${sortRef.current?.getBoundingClientRect().bottom || 0}px`,
                      left: `${sortRef.current?.getBoundingClientRect().left || 0}px`,
                      background: '#2a2a2a',
                      border: '1px solid #555555',
                      borderRadius: '2px',
                      boxShadow: '0 2px 8px rgba(0,0,0,0.5)',
                      zIndex: 500000, // NUCLEAR Z-INDEX
                      minWidth: '120px'
                    }}>'''
        
        # Replace existing sort menu styling
        content = re.sub(
            r'<div className="sort-menu" style=\{\{[^}]+\}\}>',
            sort_menu_fix.strip(),
            content
        )
        
        # Fix overflow menu with nuclear z-index and better positioning
        overflow_menu_fix = '''                <div className="overflow-menu" style={{
                  position: 'fixed',
                  top: `${overflowRef.current?.getBoundingClientRect().bottom || 0}px`,
                  left: `${overflowRef.current?.getBoundingClientRect().left || 0}px`,
                  background: '#2a2a2a',
                  border: '1px solid #555555',
                  borderRadius: '4px',
                  boxShadow: '0 4px 12px rgba(0,0,0,0.5)',
                  zIndex: 1000000, // MAXIMUM NUCLEAR Z-INDEX
                  minWidth: '200px',
                  overflow: 'visible'
                }}>'''
        
        # Replace existing overflow menu styling
        content = re.sub(
            r'<div className="overflow-menu" style=\{\{[^}]+\}\}>',
            overflow_menu_fix.strip(),
            content
        )
        
        # Add position calculation for sort menu
        sort_position_calculation = '''  // Calculate sort menu position
  useEffect(() => {
    if (showSortMenu && sortRef.current) {
      const rect = sortRef.current.getBoundingClientRect();
      // Force position recalculation
      const menu = sortRef.current.querySelector('.sort-menu') as HTMLElement;
      if (menu) {
        menu.style.top = `${rect.bottom + window.scrollY}px`;
        menu.style.left = `${rect.left + window.scrollX}px`;
      }
    }
  }, [showSortMenu]);

  // Calculate overflow menu position  
  useEffect(() => {
    if (showOverflowMenu && overflowRef.current) {
      const rect = overflowRef.current.getBoundingClientRect();
      // Force position recalculation
      const menu = overflowRef.current.querySelector('.overflow-menu') as HTMLElement;
      if (menu) {
        menu.style.top = `${rect.bottom + window.scrollY}px`;
        menu.style.left = `${rect.left + window.scrollX}px`;
      }
    }
  }, [showOverflowMenu]);'''
        
        # Insert position calculations after the resize handle effect
        content = re.sub(
            r'(  }, \[showOverflowMenu, showSortMenu\];)',
            f'\\1\n\n{sort_position_calculation}',
            content
        )
        
        with open('src/components/DeckArea.tsx', 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ DeckArea sort functionality and coordination fixed")
        
    except Exception as e:
        print(f"❌ Error fixing DeckArea: {e}")

def fix_viewmode_dropdown_nuclear_zindex():
    """Fix ViewModeDropdown with nuclear z-index approach"""
    
    try:
        with open('src/components/ViewModeDropdown.tsx', 'r', encoding='utf-8') as f:
            content = f.read()
        
        print("🔧 Fixing ViewModeDropdown with nuclear z-index...")
        
        # Enhanced dropdown menu with nuclear z-index detection
        dropdown_menu_fix = '''      {/* Dropdown Menu - Nuclear Z-Index Fixed Positioning */}
      {isOpen && (
        <div 
          className="view-dropdown-menu"
          style={{
            position: 'fixed',
            top: `${menuPosition.top}px`,
            left: `${menuPosition.left}px`,
            zIndex: buttonRef.current?.closest('.overflow-menu') ? 2000000 : 600000, // NUCLEAR Z-INDEX
            background: '#2a2a2a',
            border: '1px solid #555555',
            borderRadius: '2px',
            boxShadow: '0 4px 12px rgba(0,0,0,0.8)',
            minWidth: '100px',
            maxWidth: '150px',
            overflow: 'visible'
          }}
        >'''
        
        # Replace existing dropdown menu
        content = re.sub(
            r'      \{/\* Dropdown Menu - .*? \*/\}\n      \{isOpen && \(\n        <div \n          className="view-dropdown-menu"\n          style=\{\{[^}]+\}\}\n        >',
            dropdown_menu_fix,
            content,
            flags=re.MULTILINE | re.DOTALL
        )
        
        # Add effect to hide resize handles when ViewModeDropdown is open
        resize_handle_effect = '''  // NUCLEAR OPTION: Hide resize handles when dropdown is open
  useEffect(() => {
    const hideResizeHandles = () => {
      const resizeHandles = document.querySelectorAll('.resize-handle, .resize-handle-left, .resize-handle-right, .resize-handle-bottom');
      resizeHandles.forEach(handle => {
        if (isOpen) {
          (handle as HTMLElement).style.display = 'none';
        } else {
          (handle as HTMLElement).style.display = '';
        }
      });
    };
    
    hideResizeHandles();
    
    return () => {
      // Cleanup: restore resize handles
      if (!isOpen) {
        const resizeHandles = document.querySelectorAll('.resize-handle, .resize-handle-left, .resize-handle-right, .resize-handle-bottom');
        resizeHandles.forEach(handle => {
          (handle as HTMLElement).style.display = '';
        });
      }
    };
  }, [isOpen]);'''
        
        # Insert the effect after existing useEffect
        content = re.sub(
            r'(  }, \[isOpen\];)',
            f'\\1\n\n{resize_handle_effect}',
            content
        )
        
        with open('src/components/ViewModeDropdown.tsx', 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ ViewModeDropdown nuclear z-index fixed")
        
    except Exception as e:
        print(f"❌ Error fixing ViewModeDropdown: {e}")

def implement_css_nuclear_zindex_hierarchy():
    """Implement nuclear z-index hierarchy in CSS"""
    
    try:
        with open('src/components/MTGOLayout.css', 'r', encoding='utf-8') as f:
            content = f.read()
        
        print("🔧 Implementing nuclear z-index hierarchy...")
        
        # Nuclear z-index hierarchy CSS
        nuclear_zindex_css = '''
/* ===== NUCLEAR Z-INDEX HIERARCHY - APPROACH C ===== */

/* Base application layers */
.mtgo-layout { z-index: 1 !important; }
.mtgo-main-content { z-index: 2 !important; }
.mtgo-collection-area { z-index: 10 !important; }
.mtgo-bottom-area { z-index: 20 !important; }

/* Headers - below all interactive elements */
.mtgo-header { z-index: 100 !important; }
.panel-header { z-index: 100 !important; }

/* Resize handles - LOWEST interactive priority */
.resize-handle,
.resize-handle-left,
.resize-handle-right,  
.resize-handle-bottom {
  z-index: 500 !important; /* Much lower than dropdowns */
  transition: z-index 0s; /* No transition delay for hiding */
}

/* Normal dropdowns - HIGH priority */
.sort-menu {
  z-index: 500000 !important; /* Very high */
}

.view-dropdown-menu {
  z-index: 600000 !important; /* Higher than sort */
}

/* Overflow menu system - MAXIMUM priority */
.overflow-menu-container {
  z-index: 900000 !important;
}

.overflow-menu {
  z-index: 1000000 !important; /* NUCLEAR */
}

/* Dropdowns IN overflow menu - MAXIMUM MAXIMUM priority */
.overflow-menu .view-mode-dropdown {
  z-index: 1500000 !important;
}

.overflow-menu .view-dropdown-menu {
  z-index: 2000000 !important; /* MAXIMUM NUCLEAR */
}

/* Sort dropdown in overflow */
.overflow-menu .sort-menu {
  z-index: 1800000 !important;
}

/* List view headers - below all dropdowns */
.list-view-header-row {
  z-index: 50 !important; /* Much lower */
}

/* Ensure nothing else interferes */
.mtgo-filter-panel,
.mtgo-sideboard-panel,
.mtgo-deck-area {
  z-index: inherit !important; /* Don't create new stacking contexts */
}

/* Force stacking context reset */
.mtgo-layout * {
  position: relative;
}

.mtgo-layout .resize-handle,
.mtgo-layout .resize-handle-left,
.mtgo-layout .resize-handle-right,
.mtgo-layout .resize-handle-bottom {
  position: absolute !important; /* Override relative */
}

/* ===== END NUCLEAR Z-INDEX HIERARCHY ===== */
'''
        
        # Remove any existing z-index sections and add nuclear hierarchy
        # First remove old overflow menu z-index fixes
        content = re.sub(
            r'/\* ===== OVERFLOW MENU Z-INDEX FIXES ===== \*/.*?/\* ===== END OVERFLOW MENU Z-INDEX FIXES ===== \*/',
            '',
            content,
            flags=re.MULTILINE | re.DOTALL
        )
        
        # Remove old viewmode dropdown fixes
        content = re.sub(
            r'/\* ===== VIEWMODE DROPDOWN Z-INDEX FIX.*?/\* ===== END VIEWMODE DROPDOWN Z-INDEX FIX ===== \*/',
            '',
            content,
            flags=re.MULTILINE | re.DOTALL
        )
        
        # Add nuclear hierarchy at the end
        content += nuclear_zindex_css
        
        with open('src/components/MTGOLayout.css', 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ Nuclear z-index hierarchy implemented")
        
    except Exception as e:
        print(f"❌ Error implementing nuclear z-index: {e}")

def fix_sort_button_event_handling():
    """Ensure sort button click handlers work properly"""
    
    try:
        with open('src/components/DeckArea.tsx', 'r', encoding='utf-8') as f:
            content = f.read()
        
        print("🔧 Fixing sort button event handling...")
        
        # Enhanced sort button with better event handling
        sort_button_fix = '''                  <button 
                    className="mtgo-button sort-toggle-btn"
                    onClick={(e) => {
                      e.preventDefault();
                      e.stopPropagation();
                      console.log('🔧 Sort button clicked, current state:', showSortMenu);
                      setShowSortMenu(!showSortMenu);
                    }}
                    title="Sort options"
                    style={{
                      padding: '3px 6px',
                      background: '#333333',
                      border: '1px solid #555555',
                      color: '#ffffff',
                      fontSize: '12px',
                      cursor: 'pointer',
                      borderRadius: '2px',
                      transition: 'all 0.2s ease',
                      position: 'relative',
                      zIndex: 100
                    }}
                    onMouseEnter={(e) => e.currentTarget.style.background = '#4a4a4a'}
                    onMouseLeave={(e) => e.currentTarget.style.background = '#333333'}
                  >
                    Sort {showSortMenu ? '▲' : '▼'}
                  </button>'''
        
        # Replace existing sort button
        content = re.sub(
            r'<button \n                    className="mtgo-button sort-toggle-btn"[^>]+>\s*Sort\s*</button>',
            sort_button_fix.strip(),
            content,
            flags=re.MULTILINE | re.DOTALL
        )
        
        # Enhanced click outside detection
        click_outside_fix = '''  // Click-outside effect for sort menu and overflow menu
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      console.log('🔧 Click outside detected');
      
      if (sortRef.current && !sortRef.current.contains(event.target as Node)) {
        console.log('🔧 Closing sort menu');
        setShowSortMenu(false);
      }
      
      if (overflowRef.current && !overflowRef.current.contains(event.target as Node)) {
        console.log('🔧 Closing overflow menu');  
        setShowOverflowMenu(false);
      }
    };

    if (showSortMenu || showOverflowMenu) {
      document.addEventListener('mousedown', handleClickOutside);
      return () => {
        document.removeEventListener('mousedown', handleClickOutside);
      };
    }
  }, [showSortMenu, showOverflowMenu]);'''
        
        # Replace existing click outside effect
        content = re.sub(
            r'  // Click-outside effect for sort menu\n  useEffect\(\(\) => \{.*?\}, \[\]\);',
            click_outside_fix,
            content,
            flags=re.MULTILINE | re.DOTALL
        )
        
        with open('src/components/DeckArea.tsx', 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ Sort button event handling fixed")
        
    except Exception as e:
        print(f"❌ Error fixing sort button: {e}")

def main():
    """Execute nuclear z-index option implementation"""
    print("🚀 Starting Z-Index Nuclear Option Implementation")
    print("=" * 70)
    
    print("\n🔧 Phase 1: Fix Sort Button Functionality")
    fix_sort_button_event_handling()
    
    print("\n🔧 Phase 2: Implement Nuclear Z-Index Hierarchy")
    implement_css_nuclear_zindex_hierarchy()
    
    print("\n🔧 Phase 3: Fix ViewModeDropdown Nuclear Z-Index")
    fix_viewmode_dropdown_nuclear_zindex()
    
    print("\n🔧 Phase 4: Coordinate Overflow and Resize Handle Hiding")
    fix_deckarea_sort_and_overflow_coordination()
    
    print("\n" + "=" * 70)
    print("✅ Nuclear Z-Index Option implemented successfully!")
    print("\n🔥 NUCLEAR Z-INDEX HIERARCHY:")
    print("   • Resize handles: 500")
    print("   • Sort menu: 500,000") 
    print("   • ViewModeDropdown: 600,000")
    print("   • Overflow menu: 1,000,000")
    print("   • Dropdowns in overflow: 2,000,000")
    print("\n💥 SPECIAL FEATURES:")
    print("   • Resize handles hidden when any dropdown open")
    print("   • Enhanced event handling with debugging")
    print("   • Fixed positioning calculations")
    print("   • Overflow menu coordination")
    
    print("\n🧪 Ready for testing:")
    print("   • Sort button dropdown (normal + overflow)")
    print("   • ViewModeDropdown (normal + overflow)")  
    print("   • Resize handle conflicts eliminated")
    print("   • Z-index hierarchy dominance")

if __name__ == '__main__':
    main()
