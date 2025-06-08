#!/usr/bin/env python3

import os
import sys

def fix_default_viewmode(filename):
    """Fix default view mode to be 'grid' instead of 'list' for collection"""
    
    if not os.path.exists(filename):
        print(f"Error: {filename} not found")
        return False
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Look for the default view modes definition in useLayout
    # This pattern should match the DEFAULT_LAYOUT or similar initialization
    old_viewmodes = """viewModes: {
    collection: 'list',
    deck: 'card',
    sideboard: 'card',
  }"""
    
    new_viewmodes = """viewModes: {
    collection: 'grid',
    deck: 'card',
    sideboard: 'card',
  }"""
    
    if old_viewmodes in content:
        content = content.replace(old_viewmodes, new_viewmodes)
        print("✅ Fixed default collection view mode to 'grid'")
    else:
        # Try alternative pattern that might be in the code
        old_alt = """collection: 'list'"""
        new_alt = """collection: 'grid'"""
        
        if old_alt in content and "viewModes" in content:
            content = content.replace(old_alt, new_alt)
            print("✅ Fixed collection view mode to 'grid' (alternative pattern)")
        else:
            print("❌ Could not find view mode initialization pattern")
            print("ℹ️  Please check useLayout.ts for default view mode settings")
            return False
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Successfully fixed {filename}")
    return True

if __name__ == "__main__":
    # Check useLayout.ts first, then MTGOLayout.tsx if needed
    files_to_check = [
        "src/hooks/useLayout.ts",
        "src/components/MTGOLayout.tsx"
    ]
    
    success = False
    for filename in files_to_check:
        if os.path.exists(filename):
            print(f"Checking {filename}...")
            if fix_default_viewmode(filename):
                success = True
                break
        else:
            print(f"File not found: {filename}")
    
    if not success:
        print("❌ Could not fix default view mode in any file")
        print("ℹ️  Manual fix needed: change default collection view mode from 'list' to 'grid'")
    
    sys.exit(0 if success else 1)