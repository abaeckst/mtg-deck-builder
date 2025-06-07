#!/usr/bin/env python3

import os
import sys

def fix_typescript_error_viewmode(filename):
    """Fix the TypeScript error in updateViewMode function"""
    
    if not os.path.exists(filename):
        print(f"Error: {filename} not found")
        return False
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove the incorrectly placed debug logging
    wrong_debug = """    console.log('🔧 View mode update:', { area, mode, before: prev.viewModes[area] });"""
    
    if wrong_debug in content:
        content = content.replace(wrong_debug, "")
        print("✅ Removed incorrectly placed debug logging")
    
    # Fix the updateViewMode function with correct debug placement
    old_updateViewMode = """  const updateViewMode = useCallback((area: keyof LayoutState['viewModes'], mode: string) => {
    setLayout(prev => {
      const newLayout = {
        ...prev,
        viewModes: {
          ...prev.viewModes,
          [area]: mode,
        },
      };
      saveLayout(newLayout);
      return newLayout;
    });
  }, [saveLayout]);"""

    new_updateViewMode = """  const updateViewMode = useCallback((area: keyof LayoutState['viewModes'], mode: string) => {
    console.log('🔧 View mode update:', { area, mode, current: layout.viewModes[area] });
    setLayout(prev => {
      console.log('🔧 View mode changing from:', prev.viewModes[area], 'to:', mode);
      const newLayout = {
        ...prev,
        viewModes: {
          ...prev.viewModes,
          [area]: mode,
        },
      };
      saveLayout(newLayout);
      return newLayout;
    });
  }, [saveLayout, layout.viewModes]);"""
    
    if old_updateViewMode in content:
        content = content.replace(old_updateViewMode, new_updateViewMode)
        print("✅ Fixed updateViewMode function with proper debug logging")
    else:
        print("❌ Could not find updateViewMode function to fix")
        return False
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Successfully fixed {filename}")
    return True

if __name__ == "__main__":
    success = fix_typescript_error_viewmode("src/hooks/useLayout.ts")
    sys.exit(0 if success else 1)