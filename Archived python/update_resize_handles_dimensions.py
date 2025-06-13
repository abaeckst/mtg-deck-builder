#!/usr/bin/env python3
"""
Fix Resize Handle Dimensions - Update ResizeHandles.css with proper functional sizes
Root cause: CSS defines 6px handles which are too small to be functional
Solution: Update to 30px handles with proper positioning
"""

def fix_resize_handle_dimensions():
    """Update ResizeHandles.css with larger, more functional handle dimensions"""
    
    # Read the current ResizeHandles.css file
    with open('src/components/ResizeHandles.css', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix horizontal handle dimensions
    content = content.replace(
        '.resize-handle-right,\n.resize-handle-left {\n  cursor: ew-resize;\n  width: 6px;\n}',
        '.resize-handle-right,\n.resize-handle-left {\n  cursor: ew-resize;\n  width: 30px;\n  height: 100%;\n}'
    )
    
    # Fix right handle positioning
    content = content.replace(
        '.resize-handle-right {\n  right: -3px;',
        '.resize-handle-right {\n  right: -15px;'
    )
    
    # Fix left handle positioning  
    content = content.replace(
        '.resize-handle-left {\n  left: -3px;',
        '.resize-handle-left {\n  left: -15px;'
    )
    
    # Fix vertical handle dimensions
    content = content.replace(
        '.resize-handle-bottom,\n.resize-handle-vertical {\n  cursor: ns-resize;\n  height: 6px;\n  width: 100%;\n}',
        '.resize-handle-bottom,\n.resize-handle-vertical {\n  cursor: ns-resize;\n  height: 30px;\n  width: 100%;\n}'
    )
    
    # Fix bottom handle positioning
    content = content.replace(
        '.resize-handle-bottom {\n  bottom: -3px;',
        '.resize-handle-bottom {\n  bottom: -15px;'
    )
    
    # Fix vertical handle positioning
    content = content.replace(
        '.resize-handle-vertical {\n  top: -3px;',
        '.resize-handle-vertical {\n  top: -15px;'
    )
    
    # Update responsive dimensions for consistency
    content = content.replace(
        '  .resize-handle-right,\n  .resize-handle-left {\n    width: 8px;\n  }',
        '  .resize-handle-right,\n  .resize-handle-left {\n    width: 32px;\n  }'
    )
    
    content = content.replace(
        '  .resize-handle-bottom,\n  .resize-handle-vertical {\n    height: 8px;\n  }',
        '  .resize-handle-bottom,\n  .resize-handle-vertical {\n    height: 32px;\n  }'
    )
    
    # Update touch device dimensions
    content = content.replace(
        '  .resize-handle {\n    opacity: 0.8;\n    width: 12px;\n    height: 12px;\n  }',
        '  .resize-handle {\n    opacity: 0.8;\n  }'
    )
    
    content = content.replace(
        '  .resize-handle-right,\n  .resize-handle-left {\n    width: 12px;\n  }',
        '  .resize-handle-right,\n  .resize-handle-left {\n    width: 36px;\n  }'
    )
    
    content = content.replace(
        '  .resize-handle-bottom,\n  .resize-handle-vertical {\n    height: 12px;\n  }',
        '  .resize-handle-bottom,\n  .resize-handle-vertical {\n    height: 36px;\n  }'
    )
    
    # Write the updated content back
    with open('src/components/ResizeHandles.css', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Resize handle dimensions fixed:")
    print("   - Horizontal handles: 6px → 30px width")
    print("   - Vertical handles: 6px → 30px height") 
    print("   - Positioning: -3px → -15px (centered)")
    print("   - Responsive dimensions updated")
    print("   - Touch device support updated")
    print("\n🎯 Root cause resolved: CSS now defines functional handle sizes!")

if __name__ == "__main__":
    fix_resize_handle_dimensions()
