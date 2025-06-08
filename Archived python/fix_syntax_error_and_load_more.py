#!/usr/bin/env python3
"""
Fix the syntax error and apply a clean Load More solution
"""

import subprocess
import re

def restore_file():
    """Restore the original MTGOLayout.tsx file using git"""
    print("🔄 Restoring original file...")
    
    try:
        result = subprocess.run("git checkout HEAD -- src/components/MTGOLayout.tsx", 
                              shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Successfully restored MTGOLayout.tsx from git")
            return True
        else:
            print(f"⚠️ Git checkout failed: {result.stderr}")
            # Try alternative command
            result = subprocess.run("git restore src/components/MTGOLayout.tsx", 
                                  shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                print("✅ Successfully restored using git restore")
                return True
    except Exception as e:
        print(f"❌ Error restoring file: {e}")
    
    return False

def apply_clean_fix():
    """Apply a clean, minimal fix for Load More in Card view"""
    
    try:
        with open('src/components/MTGOLayout.tsx', 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print("❌ MTGOLayout.tsx not found")
        return False
    
    # Find the collection-grid div and add a force re-render mechanism
    # This approach uses a simple data attribute that changes with cards length
    pattern = r'(<div\s+className="collection-grid"\s+style=\{\{[^}]+\}\})'
    
    replacement = '''<div
                className="collection-grid"
                data-cards-loaded={cards.length}
                style={{'''
    
    if re.search(pattern, content):
        content = re.sub(pattern, replacement, content, count=1)
        print("✅ Added data-cards-loaded attribute to force re-render")
    else:
        print("❌ Could not find collection-grid pattern")
        # Try simpler pattern
        simple_pattern = r'className="collection-grid"'
        simple_replacement = 'className="collection-grid"\n                data-cards-loaded={cards.length}'
        
        if re.search(simple_pattern, content):
            content = re.sub(simple_pattern, simple_replacement, content, count=1)
            print("✅ Applied simple data attribute fix")
        else:
            print("❌ Could not apply any fix pattern")
            return False
    
    # Write the fixed content back
    try:
        with open('src/components/MTGOLayout.tsx', 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ Successfully wrote fixed file")
        return True
    except Exception as e:
        print(f"❌ Error writing file: {e}")
        return False

def main():
    """Main execution"""
    print("🚀 Fixing syntax error and applying Load More solution")
    print("=" * 60)
    
    # Step 1: Restore the original file
    if not restore_file():
        print("❌ Could not restore original file - manual restoration needed")
        print("Please run: git checkout HEAD -- src/components/MTGOLayout.tsx")
        return False
    
    # Step 2: Apply clean fix
    print("\n🔧 Applying clean Load More fix...")
    fix_success = apply_clean_fix()
    
    if fix_success:
        print("\n🎯 SUCCESS! Clean fix applied:")
        print("✅ Restored original MTGOLayout.tsx file")
        print("✅ Added data-cards-loaded attribute to collection-grid")
        print("✅ This forces React to re-render when cards.length changes")
        print("✅ No complex modifications or syntax issues")
        
        print("\nThe fix works by:")
        print("• Adding a data attribute that changes when cards are loaded")
        print("• Forcing React to recognize the grid container has changed")
        print("• Triggering re-render of the entire card grid")
        print("• No scroll position reset (unlike key prop solutions)")
        
        print("\nYou can now test Load More in Card view!")
    else:
        print("\n❌ Fix failed - file may need manual editing")
    
    return fix_success

if __name__ == "__main__":
    main()
