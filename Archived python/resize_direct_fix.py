#!/usr/bin/env python3

import os
import re

def apply_direct_resize_fix():
    """Apply direct inline styles to fix resize handle visibility"""
    
    tsx_path = "src/components/MTGOLayout.tsx"
    
    if not os.path.exists(tsx_path):
        print(f"❌ File not found: {tsx_path}")
        return False
    
    with open(tsx_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"📁 Reading {tsx_path} ({len(content)} characters)")
    
    # Find the filter panel resize handle and replace with working inline styles
    filter_handle_pattern = r'<div\s+className="resize-handle resize-handle-right"\s+onMouseDown=\{resizeHandlers\.onFilterPanelResize\}\s+title="[^"]*"\s*/>'
    
    filter_handle_replacement = '''<div 
          className="resize-handle resize-handle-right"
          onMouseDown={resizeHandlers.onFilterPanelResize}
          title="Drag to resize filter panel"
          style={{
            position: 'absolute',
            top: 0,
            right: -15,
            width: 30,
            height: '100%',
            backgroundColor: 'transparent',
            cursor: 'ew-resize',
            zIndex: 1001,
            transition: 'background-color 0.2s ease'
          }}
          onMouseEnter={(e) => e.currentTarget.style.backgroundColor = 'rgba(59, 130, 246, 0.3)'}
          onMouseLeave={(e) => e.currentTarget.style.backgroundColor = 'transparent'}
        />'''
    
    if re.search(filter_handle_pattern, content):
        content = re.sub(filter_handle_pattern, filter_handle_replacement, content)
        print("✅ Applied direct inline styles to filter panel resize handle")
    else:
        print("❌ Could not find filter panel resize handle pattern")
    
    # Find the vertical resize handle and replace with working inline styles
    vertical_handle_pattern = r'<div\s+className="resize-handle resize-handle-vertical"\s+onMouseDown=\{resizeHandlers\.onVerticalResize\}\s+title="[^"]*"\s*/>'
    
    vertical_handle_replacement = '''<div 
          className="resize-handle resize-handle-vertical"
          onMouseDown={resizeHandlers.onVerticalResize}
          title="Drag to resize between collection and deck areas"
          style={{
            position: 'absolute',
            top: -15,
            left: 0,
            right: 0,
            height: 30,
            backgroundColor: 'transparent',
            cursor: 'ns-resize',
            zIndex: 1001,
            transition: 'background-color 0.2s ease'
          }}
          onMouseEnter={(e) => e.currentTarget.style.backgroundColor = 'rgba(59, 130, 246, 0.3)'}
          onMouseLeave={(e) => e.currentTarget.style.backgroundColor = 'transparent'}
        />'''
    
    if re.search(vertical_handle_pattern, content):
        content = re.sub(vertical_handle_pattern, vertical_handle_replacement, content)
        print("✅ Applied direct inline styles to vertical resize handle")
    else:
        print("❌ Could not find vertical resize handle pattern")
    
    # Write the updated content
    with open(tsx_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Updated {tsx_path}")
    print("\n🔧 Changes made:")
    print("- Applied correct 30px width to filter panel handle")
    print("- Applied correct 30px height to vertical handle") 
    print("- Added hover effects with blue background")
    print("- Set proper cursor types (ew-resize, ns-resize)")
    print("- Positioned handles correctly (-15px offset)")
    
    return True

if __name__ == "__main__":
    print("🔧 Applying direct resize handle fix...")
    print("=" * 50)
    
    if apply_direct_resize_fix():
        print("\n✅ Direct fix applied successfully!")
        print("\n📋 Expected result:")
        print("- Filter panel resize handle: 30px wide, positioned at right edge")
        print("- Vertical resize handle: 30px tall, positioned between areas")
        print("- Blue hover effect when mouse is over handles")
        print("- Proper resize cursors (horizontal/vertical arrows)")
        print("\n🎯 Test: Move mouse to right edge of filter panel - should see resize cursor")
    else:
        print("\n❌ Fix failed - check error messages above")
