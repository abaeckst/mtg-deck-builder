#!/usr/bin/env python3
"""
Remove Filter Panel Resize Functionality - Clean Triage Approach
Remove problematic resize feature while keeping working functionality intact
"""

import re

def remove_filter_panel_resize():
    """Remove filter panel resize handle and related code"""
    
    print("🧹 Removing filter panel resize functionality...")
    
    # 1. Remove resize handle from MTGOLayout.tsx
    with open('src/components/MTGOLayout.tsx', 'r', encoding='utf-8') as f:
        layout_content = f.read()
    
    print(f"   📄 Processing MTGOLayout.tsx ({len(layout_content)} characters)")
    
    # Remove the Enhanced Resize Handle section (lines ~516-544)
    # Pattern matches the comment through the entire conditional block
    resize_handle_pattern = r'\s*{/\* Enhanced Resize Handle \*/}[\s\S]*?{!isFiltersCollapsed && \([\s\S]*?</div>[\s\S]*?\)}'
    
    layout_content = re.sub(resize_handle_pattern, '', layout_content, flags=re.DOTALL)
    
    with open('src/components/MTGOLayout.tsx', 'w', encoding='utf-8') as f:
        f.write(layout_content)
    
    print("   ✅ Removed filter panel resize handle from MTGOLayout.tsx")
    
    # 2. Clean up useResize.ts - remove filter panel resize logic
    with open('src/hooks/useResize.ts', 'r', encoding='utf-8') as f:
        resize_content = f.read()
    
    print(f"   📄 Processing useResize.ts ({len(resize_content)} characters)")
    
    # Remove filter panel from ResizeHandlers interface
    resize_content = resize_content.replace(
        'interface ResizeHandlers {\n  onFilterPanelResize: (event: React.MouseEvent) => void;\n  onDeckAreaResize: (event: React.MouseEvent) => void;\n  onSideboardResize: (event: React.MouseEvent) => void;\n  onVerticalResize: (event: React.MouseEvent) => void;\n}',
        'interface ResizeHandlers {\n  onDeckAreaResize: (event: React.MouseEvent) => void;\n  onSideboardResize: (event: React.MouseEvent) => void;\n  onVerticalResize: (event: React.MouseEvent) => void;\n}'
    )
    
    # Remove filter panel from resize type union
    resize_content = resize_content.replace(
        "resizeType: 'filterPanel' | 'deckArea' | 'sideboard' | 'vertical' | null;",
        "resizeType: 'deckArea' | 'sideboard' | 'vertical' | null;"
    )
    
    # Remove filter panel case from handleMouseMove switch statement
    filter_case_pattern = r"\s*case 'filterPanel': \{[\s\S]*?\s*break;\s*\}"
    resize_content = re.sub(filter_case_pattern, '', resize_content, flags=re.DOTALL)
    
    # Remove onFilterPanelResize handler creation
    resize_content = re.sub(
        r'\s*const onFilterPanelResize = useCallback\(createResizeHandler\(\'filterPanel\', \'ew-resize\'\), \[createResizeHandler\]\);',
        '', resize_content
    )
    
    # Remove onFilterPanelResize from handlers object
    resize_content = resize_content.replace(
        '  const handlers: ResizeHandlers = {\n    onFilterPanelResize,\n    onDeckAreaResize,\n    onSideboardResize,\n    onVerticalResize,\n  };',
        '  const handlers: ResizeHandlers = {\n    onDeckAreaResize,\n    onSideboardResize,\n    onVerticalResize,\n  };'
    )
    
    with open('src/hooks/useResize.ts', 'w', encoding='utf-8') as f:
        f.write(resize_content)
    
    print("   ✅ Cleaned up useResize.ts - removed filter panel logic")
    
    # 3. Clean up ResizeHandles.css - remove horizontal resize handle styles
    with open('src/components/ResizeHandles.css', 'r', encoding='utf-8') as f:
        css_content = f.read()
    
    print(f"   📄 Processing ResizeHandles.css ({len(css_content)} characters)")
    
    # Remove horizontal resize handle base styles
    css_content = re.sub(
        r'/\* Horizontal resize handles \*/\s*\.resize-handle-right,\s*\.resize-handle-left \{[^}]*\}',
        '/* Horizontal resize handles - REMOVED */',
        css_content,
        flags=re.DOTALL
    )
    
    # Remove specific right handle styles
    css_content = re.sub(
        r'\.resize-handle-right \{[^}]*\}',
        '', css_content,
        flags=re.DOTALL
    )
    
    # Remove specific left handle styles  
    css_content = re.sub(
        r'\.resize-handle-left \{[^}]*\}',
        '', css_content,
        flags=re.DOTALL
    )
    
    # Remove horizontal hover effects
    css_content = re.sub(
        r'\.resize-handle-right:hover,\s*\.resize-handle-left:hover \{[^}]*\}',
        '',
        css_content,
        flags=re.DOTALL
    )
    
    # Remove horizontal active states
    css_content = re.sub(
        r'\.resize-handle-right:active,\s*\.resize-handle-left:active,\s*\.resize-handle-right\.dragging,\s*\.resize-handle-left\.dragging \{[^}]*\}',
        '',
        css_content,
        flags=re.DOTALL
    )
    
    # Remove responsive horizontal handle styles
    css_content = re.sub(
        r'@media \(max-width: 1200px\) \{[^}]*\.resize-handle-right,\s*\.resize-handle-left \{[^}]*\}[^}]*\}',
        '',
        css_content,
        flags=re.DOTALL
    )
    
    # Remove touch device horizontal handle styles
    css_content = re.sub(
        r'@media \(hover: none\) and \(pointer: coarse\) \{[^}]*\.resize-handle-right,\s*\.resize-handle-left \{[^}]*\}[^}]*\}',
        '',
        css_content,
        flags=re.DOTALL
    )
    
    with open('src/components/ResizeHandles.css', 'w', encoding='utf-8') as f:
        f.write(css_content)
    
    print("   ✅ Cleaned up ResizeHandles.css - removed horizontal handle styles")
    
    print("\n🎯 Filter panel resize functionality removed successfully!")
    print("✅ Preserved working functionality:")
    print("   - Vertical resize (collection/deck areas)")
    print("   - Sideboard resize") 
    print("   - Filter panel width state (for future use)")
    print("   - Filter panel collapse/expand")
    print("\n💡 Codebase is now cleaner and more maintainable")
    print("\n⚠️  Remember to test:")
    print("   - Vertical resize still works")
    print("   - Sideboard resize still works")
    print("   - Filter panel collapse/expand still works")

if __name__ == "__main__":
    remove_filter_panel_resize()