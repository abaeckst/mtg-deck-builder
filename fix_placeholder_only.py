#!/usr/bin/env python3
"""
Fix only the placeholder string issue in MTGOLayout.tsx
"""

import os
import re

def fix_mtgo_layout_placeholder():
    """Fix the placeholder string escaping issue in MTGOLayout.tsx"""
    file_path = "src/components/MTGOLayout.tsx"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print("🔍 Looking for placeholder issues...")
        
        # Find any line containing the problematic placeholder
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if 'placeholder=' in line and 'exact phrase' in line:
                print(f"Found problematic line {i+1}: {line.strip()}")
                
                # Fix the escaping issue - replace \" with proper JSX escaping
                if '\\"exact phrase\\"' in line:
                    # Replace the backslash-escaped quotes with proper JSX
                    fixed_line = line.replace('\\"exact phrase\\"', '&quot;exact phrase&quot;')
                    lines[i] = fixed_line
                    print(f"Fixed to: {fixed_line.strip()}")
                elif '"exact phrase"' in line:
                    # If it's just regular quotes, escape them properly for JSX
                    fixed_line = line.replace('"exact phrase"', '&quot;exact phrase&quot;')
                    lines[i] = fixed_line
                    print(f"Fixed to: {fixed_line.strip()}")
        
        # Also fix the dependency array issue
        for i, line in enumerate(lines):
            if 'searchWithAllFilters, searchText, activeFilters' in line:
                print(f"Found dependency issue on line {i+1}")
                lines[i] = line.replace('searchWithAllFilters', 'enhancedSearch')
                print(f"Fixed dependency array")
        
        # Reconstruct the content
        fixed_content = '\n'.join(lines)
        
        # Write the updated content
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(fixed_content)
        
        print("✅ Fixed MTGOLayout.tsx placeholder and dependencies")
        return True
        
    except Exception as e:
        print(f"❌ Error fixing MTGOLayout.tsx: {e}")
        return False

def main():
    """Run the placeholder fix"""
    print("🔧 Fixing MTGOLayout.tsx placeholder string")
    print("=" * 45)
    
    # Check if we're in the right directory
    if not os.path.exists("src/components/MTGOLayout.tsx"):
        print("❌ Error: Please run this script from your project root directory")
        return False
    
    if fix_mtgo_layout_placeholder():
        print("=" * 45)
        print("🎉 MTGOLayout.tsx should now compile correctly!")
        print("\n🔧 Next Steps:")
        print("1. Run 'npm start' to verify compilation")
        print("2. Test the enhanced search functionality")
    else:
        print("❌ Fix failed. Please check the error above.")
        return False
    
    return True

if __name__ == "__main__":
    main()