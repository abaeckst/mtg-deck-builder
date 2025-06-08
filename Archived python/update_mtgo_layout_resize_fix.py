#!/usr/bin/env python3

import os
import sys

def update_mtgo_layout_resize_fix():
    """Fix resize handle visibility and functionality in MTGOLayout.tsx"""
    
    filename = "src/components/MTGOLayout.tsx"
    
    if not os.path.exists(filename):
        print(f"Error: {filename} not found")
        return False
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Updates for resize handle fixes
    updates = [
        # 1. Fix filter panel resize handle styling and visibility
        (
            '''      {/* Enhanced Resize Handle */}
      <div 
        className="resize-handle resize-handle-right"
        onMouseDown={resizeHandlers.onFilterPanelResize}
        title="Drag to resize filter panel"
        style={{
          position: 'absolute',
          top: 0,
          right: isFiltersCollapsed ? 25 : layout.panels.filterPanelWidth - 15,
          width: 30,
          height: '100%',
          cursor: 'ew-resize',
          background: 'transparent',
          zIndex: 1001
        }}
      />''',
            '''      {/* Enhanced Resize Handle - Fixed Visibility */}
      {!isFiltersCollapsed && (
        <div 
          className="resize-handle resize-handle-right"
          onMouseDown={resizeHandlers.onFilterPanelResize}
          title="Drag to resize filter panel"
          style={{
            position: 'absolute',
            top: 0,
            right: -3,
            width: 6,
            height: '100%',
            cursor: 'ew-resize',
            background: 'linear-gradient(90deg, transparent 0%, #555555 50%, transparent 100%)',
            zIndex: 1001,
            opacity: 0.7,
            transition: 'opacity 0.2s ease'
          }}
          onMouseEnter={(e) => e.currentTarget.style.opacity = '1'}
          onMouseLeave={(e) => e.currentTarget.style.opacity = '0.7'}
        />
      )}''',
            "Fix filter panel resize handle visibility and styling"
        ),
        
        # 2. Improve resize handle for collection area
        (
            '''          {/* PHASE 3A: Enhanced Resize Handle with larger hit zone */}
          <div 
            className="resize-handle resize-handle-bottom"
            onMouseDown={resizeHandlers.onDeckAreaResize}
            title="Drag to resize collection area"
            style={{
              position: 'absolute',
              left: 0,
              bottom: -15,
              width: '100%',
              height: 30,
              cursor: 'ns-resize',
              background: 'transparent',
              zIndex: 1001
            }}
          />''',
            '''          {/* PHASE 3A: Enhanced Resize Handle with larger hit zone and visibility */}
          <div 
            className="resize-handle resize-handle-bottom"
            onMouseDown={resizeHandlers.onDeckAreaResize}
            title="Drag to resize collection area"
            style={{
              position: 'absolute',
              left: 0,
              bottom: -3,
              width: '100%',
              height: 6,
              cursor: 'ns-resize',
              background: 'linear-gradient(0deg, transparent 0%, #555555 50%, transparent 100%)',
              zIndex: 1001,
              opacity: 0.7,
              transition: 'opacity 0.2s ease'
            }}
            onMouseEnter={(e) => e.currentTarget.style.opacity = '1'}
            onMouseLeave={(e) => e.currentTarget.style.opacity = '0.7'}
          />''',
            "Improve collection area resize handle visibility"
        ),
        
        # 3. Improve vertical resize handle
        (
            '''          {/* PHASE 3A: NEW - Vertical Resize Handle at top of bottom area */}
          <div 
            className="resize-handle resize-handle-vertical"
            onMouseDown={resizeHandlers.onVerticalResize}
            title="Drag to resize between collection and deck areas"
            style={{
              position: 'absolute',
              top: -15,
              left: 0,
              width: '100%',
              height: 30,
              cursor: 'ns-resize',
              background: 'transparent',
              zIndex: 1001
            }}
          />''',
            '''          {/* PHASE 3A: NEW - Vertical Resize Handle at top of bottom area with visibility */}
          <div 
            className="resize-handle resize-handle-vertical"
            onMouseDown={resizeHandlers.onVerticalResize}
            title="Drag to resize between collection and deck areas"
            style={{
              position: 'absolute',
              top: -3,
              left: 0,
              width: '100%',
              height: 6,
              cursor: 'ns-resize',
              background: 'linear-gradient(0deg, transparent 0%, #555555 50%, transparent 100%)',
              zIndex: 1001,
              opacity: 0.7,
              transition: 'opacity 0.2s ease'
            }}
            onMouseEnter={(e) => e.currentTarget.style.opacity = '1'}
            onMouseLeave={(e) => e.currentTarget.style.opacity = '0.7'}
          />''',
            "Improve vertical resize handle visibility"
        ),
        
        # 4. Improve sideboard resize handle
        (
            '''            {/* PHASE 3A: Enhanced Resize Handle with larger hit zone */}
            <div 
              className="resize-handle resize-handle-left"
              onMouseDown={resizeHandlers.onSideboardResize}
              title="Drag to resize sideboard"
              style={{
                position: 'absolute',
                top: 0,
                left: -15,
                width: 30,
                height: '100%',
                cursor: 'ew-resize',
                background: 'transparent',
                zIndex: 1001
              }}
            />''',
            '''            {/* PHASE 3A: Enhanced Resize Handle with visibility */}
            <div 
              className="resize-handle resize-handle-left"
              onMouseDown={resizeHandlers.onSideboardResize}
              title="Drag to resize sideboard"
              style={{
                position: 'absolute',
                top: 0,
                left: -3,
                width: 6,
                height: '100%',
                cursor: 'ew-resize',
                background: 'linear-gradient(90deg, transparent 0%, #555555 50%, transparent 100%)',
                zIndex: 1001,
                opacity: 0.7,
                transition: 'opacity 0.2s ease'
              }}
              onMouseEnter={(e) => e.currentTarget.style.opacity = '1'}
              onMouseLeave={(e) => e.currentTarget.style.opacity = '0.7'}
            />''',
            "Improve sideboard resize handle visibility"
        ),
        
        # 5. Add CSS class for better resize handle styling in layout
        (
            "import './MTGOLayout.css';",
            "import './MTGOLayout.css';\nimport './ResizeHandles.css';",
            "Import resize handles CSS (will create separate file)"
        ),
    ]
    
    for old_str, new_str, desc in updates:
        if old_str in content:
            content = content.replace(old_str, new_str)
            print(f"✅ {desc}")
        else:
            if "ResizeHandles.css" in desc:
                # Skip this one as we'll handle it separately
                print(f"ℹ️ {desc} - will handle separately")
            else:
                print(f"❌ Could not find: {desc}")
                return False
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Successfully updated {filename}")
    return True

if __name__ == "__main__":
    success = update_mtgo_layout_resize_fix()
    sys.exit(0 if success else 1)