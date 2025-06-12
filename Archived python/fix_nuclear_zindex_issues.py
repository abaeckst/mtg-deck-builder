#!/usr/bin/env python3

import re

def fix_viewmode_dropdown_context_detection():
    """
    Fix ViewModeDropdown to properly detect overflow context and use appropriate z-index
    """
    
    file_path = "src/components/ViewModeDropdown.tsx"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        print(f"🔧 Enhancing ViewModeDropdown context detection...")
        
        # Find the dropdown menu style section and enhance it
        enhanced_content = re.sub(
            r'style=\{\{\s*position: \'fixed\',\s*top: `\$\{menuPosition\.top\}px`,\s*left: `\$\{menuPosition\.left\}px`,\s*zIndex: \d+\s*\}\}',
            '''style={{
            position: 'fixed',
            top: `${menuPosition.top}px`,
            left: `${menuPosition.left}px`,
            zIndex: isInOverflowContext() ? 2000000 : 600000 // Nuclear z-index with context detection
          }}''',
            content
        )
        
        # Add context detection function before the return statement
        function_addition = '''  // Detect if dropdown is in overflow menu context
  const isInOverflowContext = () => {
    if (!buttonRef.current) return false;
    
    // Check if button is inside overflow menu
    const overflowMenu = buttonRef.current.closest('.overflow-menu');
    const overflowContainer = buttonRef.current.closest('.overflow-menu-container');
    
    return !!(overflowMenu || overflowContainer);
  };

  // Enhanced positioning for overflow contexts
  const calculateMenuPosition = () => {
    if (buttonRef.current) {
      const rect = buttonRef.current.getBoundingClientRect();
      
      // If in overflow context, adjust positioning
      if (isInOverflowContext()) {
        setMenuPosition({
          top: rect.bottom + window.scrollY + 2,
          left: Math.max(10, rect.left + window.scrollX - 50) // Prevent off-screen
        });
      } else {
        setMenuPosition({
          top: rect.bottom + window.scrollY + 1,
          left: rect.left + window.scrollX
        });
      }
    }
  };

'''
        
        # Insert the enhanced context detection before the return statement
        enhanced_content = re.sub(
            r'(\s+)(console\.log\(\'🔧 ViewModeDropdown render:\'[^}]+\};?\s*)(return)',
            rf'\1{function_addition}\2\3',
            enhanced_content
        )
        
        # Write the enhanced content back
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(enhanced_content)
        
        print(f"✅ Enhanced ViewModeDropdown context detection")
        return True
        
    except Exception as e:
        print(f"❌ Error enhancing ViewModeDropdown: {str(e)}")
        return False

def fix_deckarea_sort_button_integration():
    """
    Fix DeckArea sort button to use proper nuclear z-index and coordination
    """
    
    file_path = "src/components/DeckArea.tsx"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        print(f"🔧 Fixing DeckArea sort button nuclear z-index integration...")
        
        # Fix sort menu z-index to use consistent nuclear values
        content = re.sub(
            r'zIndex: 500000, // NUCLEAR Z-INDEX',
            'zIndex: 500000, // NUCLEAR Z-INDEX - Sort menu',
            content
        )
        
        # Enhance resize handle hiding logic for better coordination
        resize_handle_enhancement = '''  // Enhanced resize handle hiding with nuclear z-index coordination
  useEffect(() => {
    const hideResizeHandles = (hide = false) => {
      const resizeHandles = document.querySelectorAll('.resize-handle, .resize-handle-left, .resize-handle-right, .resize-handle-bottom');
      resizeHandles.forEach(handle => {
        const element = handle as HTMLElement;
        if (hide || showOverflowMenu || showSortMenu) {
          element.style.display = 'none';
          element.style.zIndex = '0'; // Ensure completely below nuclear z-index
        } else {
          element.style.display = '';
          element.style.zIndex = '500'; // Restore normal z-index
        }
      });
    };
    
    // Hide when any dropdown is open
    hideResizeHandles();
    
    return () => {
      // Cleanup: restore resize handles when component unmounts
      if (!showOverflowMenu && !showSortMenu) {
        hideResizeHandles(false);
      }
    };
  }, [showOverflowMenu, showSortMenu]);'''
        
        # Replace the existing useEffect for resize handle hiding
        content = re.sub(
            r'// Z-INDEX NUCLEAR OPTION: Hide resize handles when overflow menu is open\s*useEffect\(\(\) => \{[^}]+\}, \[showOverflowMenu, showSortMenu\]\);',
            resize_handle_enhancement,
            content,
            flags=re.DOTALL
        )
        
        # Write the enhanced content back
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        
        print(f"✅ Enhanced DeckArea sort button integration")
        return True
        
    except Exception as e:
        print(f"❌ Error enhancing DeckArea: {str(e)}")
        return False

def verify_css_nuclear_hierarchy():
    """
    Verify and document the nuclear z-index hierarchy in CSS
    """
    
    file_path = "src/components/MTGOLayout.css"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        print(f"🔧 Verifying CSS nuclear z-index hierarchy...")
        
        # Check for key nuclear z-index values
        nuclear_checks = [
            (r'\.resize-handle[^{]*\{\s*z-index:\s*500', 'Resize handles (500)'),
            (r'\.sort-menu[^{]*\{\s*z-index:\s*500000', 'Sort menu (500000)'),
            (r'\.view-dropdown-menu[^{]*\{\s*z-index:\s*600000', 'ViewModeDropdown (600000)'),
            (r'\.overflow-menu[^{]*\{\s*z-index:\s*1000000', 'Overflow menu (1000000)'),
            (r'\.overflow-menu .view-dropdown-menu[^{]*\{\s*z-index:\s*2000000', 'Overflow dropdown (2000000)')
        ]
        
        hierarchy_verified = True
        for pattern, description in nuclear_checks:
            if not re.search(pattern, content, re.IGNORECASE):
                print(f"⚠️  Missing nuclear z-index: {description}")
                hierarchy_verified = False
            else:
                print(f"✅ Verified: {description}")
        
        if hierarchy_verified:
            print("✅ Nuclear z-index hierarchy verified in CSS")
        else:
            print("⚠️  Nuclear z-index hierarchy needs attention")
        
        return hierarchy_verified
        
    except Exception as e:
        print(f"❌ Error verifying CSS: {str(e)}")
        return False

def main():
    """
    Execute all nuclear z-index fixes
    """
    
    print("🚀 Starting nuclear z-index implementation fixes...")
    print("=" * 60)
    
    results = []
    
    # Fix compilation errors first
    print("\n1. Fixing ViewModeDropdown context detection...")
    results.append(fix_viewmode_dropdown_context_detection())
    
    print("\n2. Fixing DeckArea sort button integration...")
    results.append(fix_deckarea_sort_button_integration())
    
    print("\n3. Verifying CSS nuclear hierarchy...")
    results.append(verify_css_nuclear_hierarchy())
    
    print("\n" + "=" * 60)
    
    if all(results):
        print("✅ All nuclear z-index fixes completed successfully!")
        print("\n📋 Next steps:")
        print("1. Run the compilation error fix script first")
        print("2. Run 'npm start' to test compilation")
        print("3. Test sort button dropdown functionality")
        print("4. Test ViewModeDropdown in both normal and overflow contexts")
        print("5. Verify resize handles are hidden when dropdowns open")
        print("6. Confirm nuclear z-index hierarchy working")
        
        print("\n🧪 Testing priorities:")
        print("- Sort button dropdown in deck area header")
        print("- ViewModeDropdown in normal context")
        print("- ViewModeDropdown in overflow menu context")
        print("- No visual conflicts with resize handles")
        
    else:
        print("⚠️  Some fixes encountered issues - manual review needed")
        
        failed_fixes = []
        if not results[0]: failed_fixes.append("ViewModeDropdown context detection")
        if not results[1]: failed_fixes.append("DeckArea sort button integration")
        if not results[2]: failed_fixes.append("CSS nuclear hierarchy verification")
        
        print(f"❌ Failed fixes: {', '.join(failed_fixes)}")

if __name__ == "__main__":
    main()
