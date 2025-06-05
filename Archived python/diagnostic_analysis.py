#!/usr/bin/env python3
"""
Diagnostic Analysis Script for Export Feature Implementation
Analyzes current file structure and identifies compilation issues
"""

import os
import glob

def analyze_project_structure():
    """Analyze current project file structure and identify issues"""
    
    print("=== MTG DECK BUILDER - EXPORT FEATURES DIAGNOSTIC ANALYSIS ===\n")
    
    # Check if we're in the right directory
    if not os.path.exists('src'):
        print("❌ ERROR: Not in project root directory")
        print("Please run this script from: C:\\Users\\carol\\mtg-deckbuilder\n")
        return False
    
    print("✅ Running from correct project directory\n")
    
    # 1. Analyze components directory
    print("1. COMPONENTS DIRECTORY ANALYSIS:")
    print("-" * 40)
    
    components_dir = "src/components"
    if os.path.exists(components_dir):
        files = sorted(os.listdir(components_dir))
        print(f"Files found in {components_dir}:")
        for file in files:
            if file.endswith(('.tsx', '.ts', '.css')):
                print(f"  ✓ {file}")
        
        # Check for casing issues
        modal_files = [f for f in files if 'modal' in f.lower()]
        if modal_files:
            print(f"\nModal-related files found:")
            for file in modal_files:
                print(f"  📁 {file}")
        
    print()
    
    # 2. Analyze utils directory  
    print("2. UTILS DIRECTORY ANALYSIS:")
    print("-" * 30)
    
    utils_dir = "src/utils"
    if os.path.exists(utils_dir):
        files = sorted(os.listdir(utils_dir))
        print(f"Files found in {utils_dir}:")
        for file in files:
            if file.endswith(('.ts', '.js')):
                print(f"  ✓ {file}")
    else:
        print(f"❌ {utils_dir} directory does not exist")
    
    print()
    
    # 3. Check for export-related files
    print("3. EXPORT FEATURE FILES CHECK:")
    print("-" * 35)
    
    expected_files = [
        "src/components/Modal.tsx",
        "src/components/Modal.css", 
        "src/components/TextExportModal.tsx",
        "src/components/ScreenshotModal.tsx",
        "src/utils/deckFormatting.ts",
        "src/utils/screenshotUtils.ts"
    ]
    
    for expected_file in expected_files:
        if os.path.exists(expected_file):
            print(f"  ✅ {expected_file}")
        else:
            # Check for case variations
            dir_path = os.path.dirname(expected_file)
            filename = os.path.basename(expected_file)
            
            if os.path.exists(dir_path):
                actual_files = os.listdir(dir_path)
                case_matches = [f for f in actual_files if f.lower() == filename.lower()]
                
                if case_matches:
                    print(f"  ⚠️  {expected_file} - CASING ISSUE")
                    print(f"      Found: {os.path.join(dir_path, case_matches[0])}")
                else:
                    print(f"  ❌ {expected_file} - MISSING")
            else:
                print(f"  ❌ {expected_file} - DIRECTORY MISSING")
    
    print()
    
    # 4. Check package.json for dependencies
    print("4. DEPENDENCY CHECK:")
    print("-" * 20)
    
    if os.path.exists("package.json"):
        with open("package.json", "r") as f:
            content = f.read()
            
        if "html2canvas" in content:
            print("  ✅ html2canvas found in package.json")
        else:
            print("  ❌ html2canvas missing from package.json")
            print("  💡 Run: npm install html2canvas @types/html2canvas")
    else:
        print("  ❌ package.json not found")
    
    print()
    
    # 5. Identify specific compilation issues
    print("5. COMPILATION ISSUE ANALYSIS:")
    print("-" * 35)
    
    print("Based on error messages:")
    print("  🔍 Issue 1: File casing mismatch")
    print("     - Import: 'Modal.css'") 
    print("     - Actual: 'modal.css'")
    print("     - Fix: Update import to match exact filename on disk")
    print()
    print("  🔍 Issue 2: html2canvas API options")
    print("     - Error: 'scale' property not recognized")
    print("     - Fix: Remove unsupported properties or check API version")
    print()
    
    # 6. Next steps recommendations
    print("6. RECOMMENDED NEXT STEPS:")
    print("-" * 30)
    print("  1. Fix file casing issues in import statements")
    print("  2. Verify html2canvas API compatibility")  
    print("  3. Check for missing utility files")
    print("  4. Test compilation after each fix")
    print("  5. Complete MTGOLayout integration if files compile")
    
    return True

if __name__ == "__main__":
    analyze_project_structure()