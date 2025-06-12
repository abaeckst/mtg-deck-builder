#!/usr/bin/env python3
"""
Simple fix: Change resize handle width from 6px to 20px
Root cause identified: handles are too narrow to find easily
"""

import re

def fix_resize_width():
    css_file = "src/components/MTGOLayout.css"
    
    try:
        with open(css_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print("🔧 Simple resize handle width fix...")
        
        # Find and replace the resize handle CSS that's creating 6px width
        # Look for the width: 6px pattern in resize handle definitions
        patterns_to_fix = [
            (r'(\.resize-handle-right[^}]*?)width:\s*6px', r'\1width: 20px'),
            (r'(\.resize-handle-left[^}]*?)width:\s*6px', r'\1width: 20px'),
            (r'(\.resize-handle-right[^}]*?)left:\s*-3px', r'\1left: -10px'),
            (r'(\.resize-handle-left[^}]*?)left:\s*-3px', r'\1left: -10px'),
            (r'(\.resize-handle-right[^}]*?)right:\s*-3px', r'\1right: -10px'),
        ]
        
        changes_made = 0
        for pattern, replacement in patterns_to_fix:
            if re.search(pattern, content):
                content = re.sub(pattern, replacement, content)
                changes_made += 1
                print(f"✅ Fixed: {pattern}")
        
        if changes_made == 0:
            print("⚠️ No 6px patterns found, adding manual CSS fix...")
            # If we can't find the exact patterns, add a simple override
            manual_fix = """
/* RESIZE HANDLE WIDTH FIX - Override narrow handles */
.resize-handle-right {
    width: 20px !important;
    right: -10px !important;
}

.resize-handle-left {
    width: 20px !important;
    left: -10px !important;
}
"""
            content += manual_fix
            changes_made = 1
        
        # Write the updated CSS
        with open(css_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Resize handle fix completed! ({changes_made} changes)")
        print("🔧 Width changed: 6px → 20px")
        print("🔧 Position adjusted for centering")
        
        return True
        
    except FileNotFoundError:
        print(f"❌ Error: {css_file} not found")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    fix_resize_width()