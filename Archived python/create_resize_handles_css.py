#!/usr/bin/env python3

import os
import sys

def create_resize_handles_css():
    """Create ResizeHandles.css for professional resize handle styling"""
    
    filename = "src/components/ResizeHandles.css"
    
    css_content = '''/* src/components/ResizeHandles.css - Professional resize handle styling */

/* Base resize handle styling */
.resize-handle {
  position: absolute;
  z-index: 1001;
  transition: opacity 0.2s ease, background-color 0.2s ease;
}

/* Horizontal resize handles */
.resize-handle-right,
.resize-handle-left {
  cursor: ew-resize;
  width: 6px;
}

.resize-handle-right {
  right: -3px;
  background: linear-gradient(90deg, transparent 0%, #555555 40%, #777777 60%, transparent 100%);
}

.resize-handle-left {
  left: -3px;
  background: linear-gradient(90deg, transparent 0%, #777777 40%, #555555 60%, transparent 100%);
}

/* Vertical resize handles */
.resize-handle-bottom,
.resize-handle-vertical {
  cursor: ns-resize;
  height: 6px;
  width: 100%;
}

.resize-handle-bottom {
  bottom: -3px;
  background: linear-gradient(0deg, transparent 0%, #555555 40%, #777777 60%, transparent 100%);
}

.resize-handle-vertical {
  top: -3px;
  background: linear-gradient(0deg, transparent 0%, #777777 40%, #555555 60%, transparent 100%);
}

/* Hover effects */
.resize-handle:hover {
  opacity: 1 !important;
}

.resize-handle-right:hover,
.resize-handle-left:hover {
  background: linear-gradient(90deg, transparent 0%, #3b82f6 40%, #60a5fa 60%, transparent 100%);
}

.resize-handle-bottom:hover,
.resize-handle-vertical:hover {
  background: linear-gradient(0deg, transparent 0%, #3b82f6 40%, #60a5fa 60%, transparent 100%);
}

/* Active/dragging state */
.resize-handle:active,
.resize-handle.dragging {
  opacity: 1 !important;
}

.resize-handle-right:active,
.resize-handle-left:active,
.resize-handle-right.dragging,
.resize-handle-left.dragging {
  background: linear-gradient(90deg, transparent 0%, #1d4ed8 40%, #3b82f6 60%, transparent 100%);
}

.resize-handle-bottom:active,
.resize-handle-vertical:active,
.resize-handle-bottom.dragging,
.resize-handle-vertical.dragging {
  background: linear-gradient(0deg, transparent 0%, #1d4ed8 40%, #3b82f6 60%, transparent 100%);
}

/* Responsive adjustments */
@media (max-width: 1200px) {
  .resize-handle {
    opacity: 0.9;
  }
  
  .resize-handle-right,
  .resize-handle-left {
    width: 8px;
  }
  
  .resize-handle-bottom,
  .resize-handle-vertical {
    height: 8px;
  }
}

/* Accessibility */
.resize-handle:focus-visible {
  outline: 2px solid #3b82f6;
  outline-offset: 2px;
  opacity: 1;
}

/* Touch device support */
@media (hover: none) and (pointer: coarse) {
  .resize-handle {
    opacity: 0.8;
    width: 12px;
    height: 12px;
  }
  
  .resize-handle-right,
  .resize-handle-left {
    width: 12px;
  }
  
  .resize-handle-bottom,
  .resize-handle-vertical {
    height: 12px;
  }
}
'''
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(css_content)
        print(f"✅ Successfully created {filename}")
        return True
    except Exception as e:
        print(f"❌ Failed to create {filename}: {e}")
        return False

if __name__ == "__main__":
    success = create_resize_handles_css()
    sys.exit(0 if success else 1)