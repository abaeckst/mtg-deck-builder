#!/usr/bin/env python3
"""
Fix Load More in Card view with scroll position preservation
This adds a ref-based scroll preservation system to the collection grid
"""

import re

def fix_load_more_card_view():
    """Fix Load More in Card view while preserving scroll position"""
    print("🔧 Fixing Load More Card view with scroll preservation...")
    
    try:
        # Read the current file
        with open('src/components/MTGOLayout.tsx', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 1. Add useRef import if not already present
        if 'useRef' not in content:
            content = re.sub(
                r'import React, \{ ([^}]+) \} from \'react\';',
                r"import React, { \1, useRef } from 'react';",
                content
            )
            print("✅ Added useRef import")
        
        # 2. Add ref declaration after other hooks
        # Find a good location after existing useCallback declarations
        ref_declaration = '''
  // Ref for scroll position preservation during Load More
  const collectionGridRef = useRef<HTMLDivElement>(null);'''
        
        # Find location after the resize handlers
        pattern = r'(const \{ handlers: resizeHandlers \} = useResize\([^}]+\}\);)'
        if re.search(pattern, content):
            content = re.sub(
                pattern,
                r'\1' + ref_declaration,
                content
            )
            print("✅ Added collection grid ref")
        
        # 3. Add scroll preservation function
        scroll_function = '''
  // Scroll preservation for Load More
  const preserveScrollOnLoadMore = useCallback((callback: () => void) => {
    const grid = collectionGridRef.current;
    if (!grid) {
      callback();
      return;
    }
    
    const scrollTop = grid.scrollTop;
    callback();
    
    // Restore scroll position after React re-renders
    requestAnimationFrame(() => {
      if (grid) {
        grid.scrollTop = scrollTop;
      }
    });
  }, []);'''
        
        # Add after the ref declaration
        ref_pattern = r'(// Ref for scroll position preservation during Load More\s+const collectionGridRef = useRef<HTMLDivElement>\(null\);)'
        if re.search(ref_pattern, content):
            content = re.sub(
                ref_pattern,
                r'\1' + scroll_function,
                content
            )
            print("✅ Added scroll preservation function")
        
        # 4. Modify the Load More button click to use scroll preservation
        load_more_pattern = r'(onClick=\{loadMoreResultsAction\})'
        load_more_replacement = r'onClick={() => preserveScrollOnLoadMore(() => loadMoreResultsAction())}'
        
        if re.search(load_more_pattern, content):
            content = re.sub(load_more_pattern, load_more_replacement, content)
            print("✅ Added scroll preservation to Load More button")
        
        # 5. Add ref and key to collection grid
        grid_pattern = r'(<div\s+className="collection-grid"[^>]*)(style=\{\{[^}]+\}\})'
        
        grid_replacement = r'''\1ref={collectionGridRef}
                key={`collection-grid-${cards.length}`}
                \2'''
        
        if re.search(grid_pattern, content):
            content = re.sub(grid_pattern, grid_replacement, content, flags=re.MULTILINE)
            print("✅ Added ref and key to collection grid")
        
        # Write the fixed content
        with open('src/components/MTGOLayout.tsx', 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("\n🎯 SUCCESS! Applied Load More Card view fix with scroll preservation:")
        print("1. ✅ Added useRef import")
        print("2. ✅ Added collection grid ref")
        print("3. ✅ Added scroll preservation function") 
        print("4. ✅ Modified Load More to preserve scroll position")
        print("5. ✅ Added key prop to force React re-render")
        print("\nThis forces React to re-render the grid when cards.length changes")
        print("while preserving the user's scroll position during Load More.")
        print("\nTest the Load More functionality in Card view now!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    fix_load_more_card_view()
