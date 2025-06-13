#!/usr/bin/env python3

import os
import re

def fix_resize_handles():
    """Fix resize handle visibility by removing conflicting inline styles"""
    
    tsx_path = "src/components/MTGOLayout.tsx"
    
    if not os.path.exists(tsx_path):
        print(f"❌ File not found: {tsx_path}")
        return False
    
    with open(tsx_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"📁 Reading {tsx_path} ({len(content)} characters)")
    
    # Fix 1: Remove inline styles from filter panel resize handle
    filter_handle_pattern = r'style=\{\{\s*position:\s*["\']absolute["\']\s*,\s*top:\s*0\s*,\s*right:\s*-3\s*,\s*width:\s*6\s*,\s*height:\s*["\']100%["\']\s*,\s*background:\s*["\'][^"\']*["\']\s*,\s*zIndex:\s*1001\s*,\s*opacity:\s*0\.7\s*,\s*transition:\s*["\'][^"\']*["\']\s*\}\}'
    
    if re.search(filter_handle_pattern, content):
        content = re.sub(filter_handle_pattern, '', content)
        print("✅ Removed filter panel resize handle inline styles")
    
    # Fix 2: Remove inline styles from vertical resize handle  
    vertical_handle_pattern = r'style=\{\{\s*position:\s*["\']absolute["\']\s*,\s*top:\s*-3\s*,\s*left:\s*0\s*,\s*width:\s*["\']100%["\']\s*,\s*height:\s*6\s*,\s*background:\s*["\'][^"\']*["\']\s*,\s*zIndex:\s*1001\s*,\s*opacity:\s*0\.7\s*,\s*transition:\s*["\'][^"\']*["\']\s*\}\}'
    
    if re.search(vertical_handle_pattern, content):
        content = re.sub(vertical_handle_pattern, '', content)
        print("✅ Removed vertical resize handle inline styles")
    
    # Fix 3: Simplify resize handle elements to use CSS classes only
    content = re.sub(
        r'<div\s+className="resize-handle resize-handle-right"\s+onMouseDown=\{resizeHandlers\.onFilterPanelResize\}\s+title="[^"]*"\s+style=\{[^}]*\}\s*/>',
        '<div className="resize-handle resize-handle-right" onMouseDown={resizeHandlers.onFilterPanelResize} title="Drag to resize filter panel" />',
        content
    )
    
    content = re.sub(
        r'<div\s+className="resize-handle resize-handle-vertical"\s+onMouseDown=\{resizeHandlers\.onVerticalResize\}\s+title="[^"]*"\s+style=\{[^}]*\}\s*/>',
        '<div className="resize-handle resize-handle-vertical" onMouseDown={resizeHandlers.onVerticalResize} title="Drag to resize between collection and deck areas" />',
        content
    )
    
    # Fix 4: Clean up any lingering onMouseEnter/onMouseLeave inline style handlers
    content = re.sub(
        r'onMouseEnter=\{[^}]*e\.currentTarget\.style\.opacity[^}]*\}',
        '',
        content
    )
    
    content = re.sub(
        r'onMouseLeave=\{[^}]*e\.currentTarget\.style\.opacity[^}]*\}',
        '',
        content
    )
    
    # Write the updated content
    with open(tsx_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Updated {tsx_path}")
    print("\n🔧 Changes made:")
    print("- Removed all inline styles from resize handles")
    print("- Resize handles now use CSS classes exclusively")
    print("- CSS classes provide proper 30px width and hover effects")
    
    return True

def update_css_for_better_visibility():
    """Ensure CSS resize handles are highly visible"""
    
    css_path = "src/components/MTGOLayout.css"
    
    if not os.path.exists(css_path):
        print(f"❌ CSS file not found: {css_path}")
        return False
    
    with open(css_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find and enhance resize handle CSS
    resize_handle_css = '''
/* Enhanced Resize Handles - Larger hit zones with better visibility */
.resize-handle {
  position: absolute;
  background-color: transparent;
  transition: background-color 0.2s ease;
  z-index: 1001;
}

.resize-handle:hover {
  background-color: rgba(59, 130, 246, 0.3) !important;
}

.resize-handle:active {
  background-color: rgba(59, 130, 246, 0.5) !important;
}

.resize-handle-right {
  top: 0;
  right: -15px;
  width: 30px;
  height: 100%;
  cursor: ew-resize;
}

.resize-handle-left {
  top: 0;
  left: -15px;
  width: 30px;
  height: 100%;
  cursor: ew-resize;
}

.resize-handle-bottom {
  bottom: -15px;
  left: 0;
  right: 0;
  height: 30px;
  cursor: ns-resize;
}

.resize-handle-vertical {
  top: -15px;
  left: 0;
  right: 0;
  height: 30px;
  cursor: ns-resize;
}
'''
    
    # Replace existing resize handle CSS
    pattern = r'/\*\s*Enhanced Resize Handles[^*]*\*/.*?/\*\s*===.*?===\s*\*/'
    if re.search(pattern, content, re.DOTALL):
        content = re.sub(pattern, resize_handle_css.strip(), content, flags=re.DOTALL)
    else:
        # Find a good place to insert the CSS
        if '/* Enhanced Resize Handles' in content:
            # Replace existing section
            pattern = r'/\*\s*Enhanced Resize Handles[^}]*\}[^}]*\}[^}]*\}[^}]*\}[^}]*\}[^}]*\}[^}]*\}'
            content = re.sub(pattern, resize_handle_css.strip(), content, flags=re.DOTALL)
        else:
            # Add to end of file
            content += '\n' + resize_handle_css
    
    with open(css_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Updated {css_path} with enhanced resize handle visibility")
    
    return True

if __name__ == "__main__":
    print("🔧 Fixing resize handle visibility issues...")
    print("=" * 50)
    
    success = True
    
    # Fix the TSX file to remove inline styles
    if not fix_resize_handles():
        success = False
    
    # Enhance CSS for better visibility
    if not update_css_for_better_visibility():
        success = False
    
    if success:
        print("\n✅ All fixes applied successfully!")
        print("\n📋 What was fixed:")
        print("1. Removed 6px width inline styles")
        print("2. Resize handles now use CSS 30px width")
        print("3. Enhanced hover visibility with blue background")
        print("4. Proper cursor types (ew-resize, ns-resize)")
        print("\n🎯 Result: Resize handles should now be visible and functional")
    else:
        print("\n❌ Some fixes failed - check error messages above")
