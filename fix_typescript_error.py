#!/usr/bin/env python3

import os
import sys

def fix_useLayout_typescript_error():
    """Fix the TypeScript error in useLayout.ts line 245 where 'prev' is used before declaration"""
    
    filename = "src/hooks/useLayout.ts"
    
    if not os.path.exists(filename):
        print(f"Error: {filename} not found")
        return False
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix the TypeScript error by removing the incorrect console.log line
    old_code = """  // Update view modes
  const updateViewMode = useCallback((area: keyof LayoutState['viewModes'], mode: string) => {
    console.log('🔧 View mode update:', { area, mode, before: prev.viewModes[area] });
    setLayout(prev => {"""
    
    new_code = """  // Update view modes
  const updateViewMode = useCallback((area: keyof LayoutState['viewModes'], mode: string) => {
    setLayout(prev => {
      console.log('🔧 View mode update:', { area, mode, before: prev.viewModes[area] });"""
    
    if old_code in content:
        content = content.replace(old_code, new_code)
        print("✅ Fixed TypeScript error: moved console.log inside setLayout callback")
    else:
        print("❌ Could not find the problematic code pattern")
        return False
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Successfully fixed TypeScript error in {filename}")
    return True

if __name__ == "__main__":
    success = fix_useLayout_typescript_error()
    sys.exit(0 if success else 1)