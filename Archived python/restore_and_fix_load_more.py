#!/usr/bin/env python3
"""
Complete fix: Restore MTGOLayout.tsx and apply targeted Load More fix
This script will handle both the syntax errors and the Load More issue
"""

import subprocess
import os
import re

def run_git_command(command):
    """Run a git command and return success status"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def restore_file():
    """Restore the original MTGOLayout.tsx file using git"""
    print("🔄 Attempting to restore MTGOLayout.tsx...")
    
    # Try to restore from git
    success, stdout, stderr = run_git_command("git checkout HEAD -- src/components/MTGOLayout.tsx")
    
    if success:
        print("✅ Successfully restored MTGOLayout.tsx from git")
        return True
    else:
        print(f"⚠️ Git restore failed: {stderr}")
        
        # Try alternative git command
        success, stdout, stderr = run_git_command("git restore src/components/MTGOLayout.tsx")
        
        if success:
            print("✅ Successfully restored MTGOLayout.tsx using git restore")
            return True
        else:
            print(f"❌ Could not restore file automatically: {stderr}")
            return False

def apply_targeted_fix():
    """Apply the minimal fix for Load More in Card view"""
    print("🔧 Applying targeted Load More fix...")
    
    # Read the restored file
    try:
        with open('src/components/MTGOLayout.tsx', 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print("❌ MTGOLayout.tsx not found. Please ensure the file exists.")
        return False
    
    # Apply the minimal fix: add key to collection-grid
    # This is a very safe change that only adds a key prop
    pattern = r'(<div\s+className="collection-grid"\s+style=\{\{)'
    
    replacement = '''<div 
                className="collection-grid"
                key={`collection-grid-${cards.length}`}
                style={{'''
    
    if re.search(pattern, content):
        content = re.sub(pattern, replacement, content)
        print("✅ Applied key prop to collection-grid")
    else:
        print("⚠️ Could not find collection-grid pattern - checking alternative patterns...")
        
        # Try alternative pattern
        alt_pattern = r'(className="collection-grid")'
        alt_replacement = r'className="collection-grid"\n                key={`collection-grid-${cards.length}`}'
        
        if re.search(alt_pattern, content):
            content = re.sub(alt_pattern, alt_replacement, content)
            print("✅ Applied key prop using alternative pattern")
        else:
            print("❌ Could not find collection-grid to apply fix")
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
    print("🚀 Starting MTGOLayout.tsx restoration and Load More fix")
    print("=" * 60)
    
    # Step 1: Restore the original file
    if not restore_file():
        print("\n❌ MANUAL ACTION REQUIRED:")
        print("Could not restore file automatically. Please run one of these commands manually:")
        print("  git checkout HEAD -- src/components/MTGOLayout.tsx")
        print("  git restore src/components/MTGOLayout.tsx")
        print("  git checkout src/components/MTGOLayout.tsx")
        print("\nThen run this script again.")
        return False
    
    # Step 2: Apply the targeted fix
    if not apply_targeted_fix():
        print("\n❌ Fix application failed")
        return False
    
    print("\n🎯 SUCCESS! Changes applied:")
    print("1. ✅ Restored original MTGOLayout.tsx (fixing syntax errors)")
    print("2. ✅ Added key prop to collection-grid (fixing Load More in Card view)")
    print("\nThe fix forces React to re-render the grid when cards.length changes,")
    print("which should resolve the Load More display issue in Card view.")
    print("\nYou can now test the Load More functionality in Card view!")
    
    return True

if __name__ == "__main__":
    main()
