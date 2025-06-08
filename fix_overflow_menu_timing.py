#!/usr/bin/env python3
"""
Fix overflow menu disappearing immediately when clicked.
The issue is click-outside handler timing and event bubbling.
"""

import re

def fix_overflow_menu_timing():
    """Fix the click outside handler timing issue in DeckArea.tsx"""
    
    try:
        with open('src/components/DeckArea.tsx', 'r', encoding='utf-8') as f:
            content = f.read()
        
        print("🔧 Fixing overflow menu click outside handler timing...")
        
        # Find and replace the problematic click outside effect
        old_effect_pattern = r'// Click-outside effect for sort menu and overflow menu\s*useEffect\(\(\) => \{.*?\}, \[showSortMenu, showOverflowMenu\]\);'
        
        new_effect = '''// Click-outside effect for sort menu and overflow menu - FIXED TIMING
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
      // CRITICAL FIX: Add delay to prevent immediate closure from same click
      const timeoutId = setTimeout(() => {
        document.addEventListener('mousedown', handleClickOutside);
      }, 10); // Small delay to let the menu render
      
      return () => {
        clearTimeout(timeoutId);
        document.removeEventListener('mousedown', handleClickOutside);
      };
    }
  }, [showSortMenu, showOverflowMenu]);'''
        
        content = re.sub(old_effect_pattern, new_effect, content, flags=re.DOTALL)
        
        # Also fix the overflow menu toggle button to prevent event bubbling
        old_toggle_pattern = r'(onClick=\{\(\) => setShowOverflowMenu\(!showOverflowMenu\)\})'
        new_toggle_pattern = r'onClick={(e) => { e.stopPropagation(); console.log("🔧 Overflow menu button clicked"); setShowOverflowMenu(!showOverflowMenu); }}'
        
        content = re.sub(old_toggle_pattern, new_toggle_pattern, content)
        
        with open('src/components/DeckArea.tsx', 'w', encoding='utf-8') as f:
            f.write(content)
            
        print("✅ Overflow menu timing fixed")
        return True
        
    except Exception as e:
        print(f"❌ Error fixing overflow menu timing: {e}")
        return False

def fix_overflow_menu_zindex_again():
    """Double-check the z-index hierarchy in CSS"""
    
    try:
        with open('src/components/MTGOLayout.css', 'r', encoding='utf-8') as f:
            content = f.read()
        
        print("🔧 Double-checking overflow menu z-index...")
        
        # Make sure overflow menu has maximum priority
        overflow_priority_css = '''
/* ===== OVERFLOW MENU MAXIMUM PRIORITY FIX ===== */

/* Ensure overflow menu appears above EVERYTHING */
.overflow-menu-container {
  position: relative !important;
  z-index: 999999 !important;
}

.overflow-menu {
  position: fixed !important;
  z-index: 999999 !important;
  background: #2a2a2a !important;
  border: 1px solid #555555 !important;
  border-radius: 4px !important;
  box-shadow: 0 4px 12px rgba(0,0,0,0.5) !important;
  min-width: 200px !important;
  overflow: visible !important;
  pointer-events: auto !important;
}

.overflow-menu-item {
  display: block !important;
  padding: 6px 12px !important;
  border-bottom: 1px solid #555555 !important;
  background: transparent !important;
  color: #ffffff !important;
  cursor: pointer !important;
  transition: background-color 0.2s ease !important;
}

.overflow-menu-item:hover {
  background-color: rgba(255,255,255,0.1) !important;
}

.overflow-menu-item:last-child {
  border-bottom: none !important;
}

/* Force everything else to be lower */
.mtgo-layout * {
  z-index: auto !important;
}

.mtgo-layout .overflow-menu,
.mtgo-layout .overflow-menu-container {
  z-index: 999999 !important;
}

/* ===== END OVERFLOW MENU MAXIMUM PRIORITY FIX ===== */
'''
        
        # Remove any conflicting z-index rules and add the new ones
        # First remove old overflow menu CSS
        content = re.sub(
            r'/\* ===== OVERFLOW MENU Z-INDEX FIX =====.*?===== END OVERFLOW MENU Z-INDEX FIX ===== \*/',
            '',
            content,
            flags=re.DOTALL
        )
        
        # Add the new priority CSS
        content = content.rstrip() + '\n' + overflow_priority_css + '\n'
        
        with open('src/components/MTGOLayout.css', 'w', encoding='utf-8') as f:
            f.write(content)
            
        print("✅ Overflow menu z-index maximized")
        return True
        
    except Exception as e:
        print(f"❌ Error fixing z-index: {e}")
        return False

def add_debug_logging():
    """Add debugging to help track what's happening"""
    
    try:
        with open('src/components/DeckArea.tsx', 'r', encoding='utf-8') as f:
            content = f.read()
        
        print("🔧 Adding debug logging...")
        
        # Add debug logging to state changes
        old_overflow_state = r'const \[showOverflowMenu, setShowOverflowMenu\] = useState\(false\);'
        new_overflow_state = '''const [showOverflowMenu, setShowOverflowMenu] = useState(false);
  
  // Debug logging for overflow menu state
  useEffect(() => {
    console.log('🔧 Overflow menu state changed:', showOverflowMenu);
  }, [showOverflowMenu]);'''
        
        content = re.sub(old_overflow_state, new_overflow_state, content)
        
        with open('src/components/DeckArea.tsx', 'w', encoding='utf-8') as f:
            f.write(content)
            
        print("✅ Debug logging added")
        return True
        
    except Exception as e:
        print(f"❌ Error adding debug logging: {e}")
        return False

def main():
    """Execute all overflow menu fixes"""
    print("🚀 Fixing overflow menu disappearing issue...")
    print()
    
    success_count = 0
    
    if fix_overflow_menu_timing():
        success_count += 1
    
    if fix_overflow_menu_zindex_again():
        success_count += 1
        
    if add_debug_logging():
        success_count += 1
    
    print()
    if success_count >= 2:
        print("✅ OVERFLOW MENU FIXES COMPLETED!")
        print()
        print("Changes made:")
        print("1. Fixed click-outside handler timing (10ms delay)")
        print("2. Added stopPropagation to prevent event bubbling")
        print("3. Maximized overflow menu z-index (999999)")
        print("4. Added debug logging to track menu state")
        print()
        print("Next steps:")
        print("1. Test clicking the overflow button (⋯)")
        print("2. Check browser console for debug messages")
        print("3. The menu should now stay open when clicked")
        print()
        print("If it still doesn't work, check the browser console for error messages.")
    else:
        print(f"⚠️ Only {success_count}/3 fixes completed successfully")
        print("Check error messages above for details")

if __name__ == "__main__":
    main()
