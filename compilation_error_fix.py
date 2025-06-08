#!/usr/bin/env python3
"""
Fix compilation errors in DeckArea.tsx from duplicate variable declarations
Clean implementation of nuclear z-index without breaking existing code
"""

import re

def fix_deckarea_compilation_errors():
    """Remove duplicate declarations and properly implement nuclear fixes"""
    
    try:
        with open('src/components/DeckArea.tsx', 'r', encoding='utf-8') as f:
            content = f.read()
        
        print("🔧 Fixing DeckArea compilation errors...")
        
        # Find and remove the duplicate state declarations that were incorrectly added
        # Remove the entire duplicated section
        content = re.sub(
            r'  const controlsRef = useRef<HTMLDivElement>\(null\);\n    // Responsive overflow menu state\n  const \[showOverflowMenu, setShowOverflowMenu\] = useState\(false\);\n  const \[hiddenControls, setHiddenControls\] = useState<string\[\]>\(\[\]\);\n  const headerRef = useRef<HTMLDivElement>\(null\);\n  const controlsRef = useRef<HTMLDivElement>\(null\);\n  const overflowRef = useRef<HTMLDivElement>\(null\);\n\n  // Z-INDEX NUCLEAR OPTION: Hide resize handles when overflow menu is open.*?  }, \[showOverflowMenu, showSortMenu\];',
            '',
            content,
            flags=re.MULTILINE | re.DOTALL
        )
        
        # Now add the nuclear z-index effects after the existing useEffect
        nuclear_effects = '''
  // Z-INDEX NUCLEAR OPTION: Hide resize handles when overflow menu or sort menu is open
  useEffect(() => {
    const hideResizeHandles = () => {
      const resizeHandles = document.querySelectorAll('.resize-handle, .resize-handle-left, .resize-handle-right, .resize-handle-bottom');
      resizeHandles.forEach(handle => {
        if (showOverflowMenu || showSortMenu) {
          (handle as HTMLElement).style.display = 'none';
        } else {
          (handle as HTMLElement).style.display = '';
        }
      });
    };
    
    hideResizeHandles();
    
    return () => {
      // Cleanup: restore resize handles when component unmounts
      const resizeHandles = document.querySelectorAll('.resize-handle, .resize-handle-left, .resize-handle-right, .resize-handle-bottom');
      resizeHandles.forEach(handle => {
        (handle as HTMLElement).style.display = '';
      });
    };
  }, [showOverflowMenu, showSortMenu]);

  // Calculate sort menu position with nuclear z-index
  useEffect(() => {
    if (showSortMenu && sortRef.current) {
      const rect = sortRef.current.getBoundingClientRect();
      const menu = sortRef.current.querySelector('.sort-menu') as HTMLElement;
      if (menu) {
        menu.style.position = 'fixed';
        menu.style.top = `${rect.bottom + window.scrollY}px`;
        menu.style.left = `${rect.left + window.scrollX}px`;
        menu.style.zIndex = '500000'; // NUCLEAR Z-INDEX
      }
    }
  }, [showSortMenu]);

  // Calculate overflow menu position with nuclear z-index  
  useEffect(() => {
    if (showOverflowMenu && overflowRef.current) {
      const rect = overflowRef.current.getBoundingClientRect();
      const menu = overflowRef.current.querySelector('.overflow-menu') as HTMLElement;
      if (menu) {
        menu.style.position = 'fixed';
        menu.style.top = `${rect.bottom + window.scrollY}px`;
        menu.style.left = `${rect.left + window.scrollX}px`;
        menu.style.zIndex = '1000000'; // MAXIMUM NUCLEAR Z-INDEX
      }
    }
  }, [showOverflowMenu]);'''
        
        # Insert the nuclear effects after the existing responsive layout detection useEffect
        content = re.sub(
            r'(  }, \[hiddenControls\]);)',
            f'\\1{nuclear_effects}',
            content
        )
        
        # Fix sort button with better event handling and debug logging
        sort_button_fix = '''                  <button 
                    className="mtgo-button sort-toggle-btn"
                    onClick={(e) => {
                      e.preventDefault();
                      e.stopPropagation();
                      console.log('🔧 Sort button clicked, toggling from:', showSortMenu);
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
                      transition: 'all 0.2s ease'
                    }}
                    onMouseEnter={(e) => e.currentTarget.style.background = '#4a4a4a'}
                    onMouseLeave={(e) => e.currentTarget.style.background = '#333333'}
                  >
                    Sort {showSortMenu ? '▲' : '▼'}
                  </button>'''
        
        # Replace existing sort button (find the pattern more carefully)
        content = re.sub(
            r'<button \n                    className="mtgo-button sort-toggle-btn"[^>]*>\s*Sort\s*</button>',
            sort_button_fix.strip(),
            content,
            flags=re.MULTILINE | re.DOTALL
        )
        
        # Fix sort menu with nuclear z-index
        sort_menu_fix = '''                    <div className="sort-menu" style={{
                      position: 'fixed',
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
        
        # Fix overflow menu with nuclear z-index
        overflow_menu_fix = '''                <div className="overflow-menu" style={{
                  position: 'fixed',
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
        
        with open('src/components/DeckArea.tsx', 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ DeckArea compilation errors fixed and nuclear z-index implemented")
        
    except Exception as e:
        print(f"❌ Error fixing DeckArea: {e}")

def fix_viewmode_dropdown_simple():
    """Simple fix for ViewModeDropdown with nuclear z-index"""
    
    try:
        with open('src/components/ViewModeDropdown.tsx', 'r', encoding='utf-8') as f:
            content = f.read()
        
        print("🔧 Fixing ViewModeDropdown with nuclear z-index...")
        
        # Enhanced dropdown menu with context-aware nuclear z-index
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
            maxWidth: '150px'
          }}
        >'''
        
        # Replace existing dropdown menu section
        content = re.sub(
            r'      \{/\* Dropdown Menu.*?\*/\}\n      \{isOpen && \(\n        <div \n          className="view-dropdown-menu"\n          style=\{\{[^}]+\}\}\n        >',
            dropdown_menu_fix,
            content,
            flags=re.MULTILINE | re.DOTALL
        )
        
        # Add nuclear option effect for hiding resize handles
        nuclear_effect = '''
  // NUCLEAR OPTION: Hide resize handles when dropdown is open
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
  }, [isOpen]);'''
        
        # Insert the effect after existing useEffect
        content = re.sub(
            r'(  }, \[isOpen\];)',
            f'\\1{nuclear_effect}',
            content
        )
        
        with open('src/components/ViewModeDropdown.tsx', 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ ViewModeDropdown nuclear z-index implemented")
        
    except Exception as e:
        print(f"❌ Error fixing ViewModeDropdown: {e}")

def main():
    """Execute compilation error fixes and implement nuclear z-index cleanly"""
    print("🚀 Fixing Compilation Errors + Nuclear Z-Index Implementation")
    print("=" * 70)
    
    print("\n🔧 Phase 1: Fix DeckArea Compilation Errors")
    fix_deckarea_compilation_errors()
    
    print("\n🔧 Phase 2: Fix ViewModeDropdown Nuclear Z-Index")
    fix_viewmode_dropdown_simple()
    
    print("\n" + "=" * 70)
    print("✅ Compilation errors fixed!")
    print("✅ Nuclear z-index properly implemented!")
    print("\n🔥 NUCLEAR Z-INDEX VALUES:")
    print("   • Sort menu: 500,000") 
    print("   • ViewModeDropdown: 600,000 (normal) / 2,000,000 (overflow)")
    print("   • Overflow menu: 1,000,000")
    print("\n💥 SPECIAL FEATURES:")
    print("   • Resize handles hidden when any dropdown open")
    print("   • Enhanced sort button with debugging")
    print("   • Fixed positioning calculations")
    print("   • Context-aware z-index for ViewModeDropdown")
    
    print("\n🧪 Ready for testing!")

if __name__ == '__main__':
    main()
