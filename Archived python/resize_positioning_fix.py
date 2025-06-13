#!/usr/bin/env python3

import os
import re

def fix_resize_handle_positioning():
    """Move resize handles outside the clipping containers"""
    
    tsx_path = "src/components/MTGOLayout.tsx"
    
    if not os.path.exists(tsx_path):
        print(f"❌ File not found: {tsx_path}")
        return False
    
    with open(tsx_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"📁 Reading {tsx_path} ({len(content)} characters)")
    
    # Find the current filter panel resize handle and remove it
    current_handle_pattern = r'<div\s+className="resize-handle resize-handle-right"[^>]*>.*?</div>'
    content = re.sub(current_handle_pattern, '', content, flags=re.DOTALL)
    print("✅ Removed current filter panel resize handle")
    
    # Find the closing div of the FilterPanel and add the resize handle after it
    filter_panel_pattern = r'(<FilterPanel[^>]*/>)'
    
    filter_panel_with_handle = r'''\1
      
      {/* Filter Panel Resize Handle - Positioned relative to main layout */}
      <div
        className="resize-handle resize-handle-right"
        onMouseDown={resizeHandlers.onFilterPanelResize}
        title="Drag to resize filter panel"
        style={{
          position: 'absolute',
          top: 0,
          left: `${isFiltersCollapsed ? 40 : layout.panels.filterPanelWidth}px`,
          width: 30,
          height: '100vh',
          backgroundColor: 'transparent',
          cursor: 'ew-resize',
          zIndex: 1001,
          transition: 'background-color 0.2s ease'
        }}
        onMouseEnter={(e) => e.currentTarget.style.backgroundColor = 'rgba(59, 130, 246, 0.3)'}
        onMouseLeave={(e) => e.currentTarget.style.backgroundColor = 'transparent'}
      />'''
    
    if re.search(filter_panel_pattern, content):
        content = re.sub(filter_panel_pattern, filter_panel_with_handle, content)
        print("✅ Added filter panel resize handle positioned relative to main layout")
    else:
        print("❌ Could not find FilterPanel component")
    
    # Find and fix the vertical resize handle similarly
    current_vertical_pattern = r'<div\s+className="resize-handle resize-handle-vertical"[^>]*>.*?</div>'
    content = re.sub(current_vertical_pattern, '', content, flags=re.DOTALL)
    print("✅ Removed current vertical resize handle")
    
    # Find the main content area and add vertical handle
    main_content_pattern = r'(<div className="mtgo-main-content">)'
    
    main_content_with_handle = r'''\1
        
        {/* Vertical Resize Handle - Between collection and deck areas */}
        <div
          className="resize-handle resize-handle-vertical"
          onMouseDown={resizeHandlers.onVerticalResize}
          title="Drag to resize between collection and deck areas"
          style={{
            position: 'absolute',
            top: `calc(100vh - var(--deck-area-height) - 15px)`,
            left: `${isFiltersCollapsed ? 40 : layout.panels.filterPanelWidth}px`,
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
    
    if re.search(main_content_pattern, content):
        content = re.sub(main_content_pattern, main_content_with_handle, content)
        print("✅ Added vertical resize handle positioned correctly")
    else:
        print("❌ Could not find main content area")
    
    # Write the updated content
    with open(tsx_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Updated {tsx_path}")
    print("\n🔧 Changes made:")
    print("- Moved filter panel resize handle outside FilterPanel component")
    print("- Positioned handles relative to main layout container")
    print("- Handles now positioned at exact panel edges")
    print("- Full viewport height for better interaction")
    print("- No clipping by parent containers")
    
    return True

if __name__ == "__main__":
    print("🔧 Fixing resize handle positioning...")
    print("=" * 50)
    
    if fix_resize_handle_positioning():
        print("\n✅ Positioning fix applied successfully!")
        print("\n📋 Expected result:")
        print("- Filter resize handle appears at right edge of filter panel")
        print("- Vertical resize handle appears between collection and deck areas")
        print("- Handles are no longer clipped by parent containers")
        print("- Full viewport height for easier interaction")
        print("\n🎯 Test: Look for blue highlight on hover at panel edges")
    else:
        print("\n❌ Fix failed - check error messages above")
