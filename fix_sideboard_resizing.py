#!/usr/bin/env python3

import os
import sys

def fix_sideboard_resizing(filename):
    """Fix sideboard resizing and sizing issues in MTGOLayout component"""
    
    if not os.path.exists(filename):
        print(f"Error: {filename} not found")
        return False
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix 1: Change CSS class from mtgo-sideboard-area to mtgo-sideboard-panel
    old_class = 'className="mtgo-sideboard-area"'
    new_class = 'className="mtgo-sideboard-panel"'
    
    if old_class in content:
        content = content.replace(old_class, new_class)
        print("✅ Fixed CSS class: mtgo-sideboard-area → mtgo-sideboard-panel")
    else:
        print("❌ Could not find CSS class to fix")
        return False
    
    # Fix 2: Add dynamic width styling and move resize handle inside sideboard
    old_sideboard_start = '''          {/* Sideboard Area */}
          <DropZoneComponent
            zone="sideboard"
            onDragEnter={handleDragEnter}
            onDragLeave={handleDragLeave}
            canDrop={canDropInZone('sideboard', dragState.draggedCards)}
            isDragActive={dragState.isDragging}
            className="mtgo-sideboard-panel"
          >'''
    
    new_sideboard_start = '''          {/* Sideboard Area */}
          <DropZoneComponent
            zone="sideboard"
            onDragEnter={handleDragEnter}
            onDragLeave={handleDragLeave}
            canDrop={canDropInZone('sideboard', dragState.draggedCards)}
            isDragActive={dragState.isDragging}
            className="mtgo-sideboard-panel"
            style={{ width: `${layout.panels.sideboardWidth}px` }}
          >
            {/* Horizontal Resize Handle */}
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
            />'''
    
    if old_sideboard_start in content:
        content = content.replace(old_sideboard_start, new_sideboard_start)
        print("✅ Added dynamic width styling and horizontal resize handle")
    else:
        print("❌ Could not find sideboard start section")
        return False
    
    # Fix 3: Remove the duplicate resize handle that was added to the deck area
    old_deck_resize = '''            {/* Resize Handle */}
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
            />
          </DropZoneComponent>'''
    
    new_deck_end = '''          </DropZoneComponent>'''
    
    if old_deck_resize in content:
        content = content.replace(old_deck_resize, new_deck_end)
        print("✅ Removed duplicate resize handle from deck area")
    else:
        print("❌ Could not find duplicate deck resize handle")
        return False
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Successfully fixed sideboard resizing in {filename}")
    return True

if __name__ == "__main__":
    success = fix_sideboard_resizing("src/components/MTGOLayout.tsx")
    sys.exit(0 if success else 1)