#!/usr/bin/env python3
"""
Fix the real issues:
1. Z-index inconsistency (Handle 1 has z-index 50, should be 500+)
2. Sideboard content overlapping resize handle area
3. Sideboard covering overflow menu
"""

import re

def fix_overlap_and_zindex():
    css_file = "src/components/MTGOLayout.css"
    
    try:
        with open(css_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print("🔧 Fixing resize handle overlap and z-index issues...")
        
        # 1. Fix z-index inconsistency - ensure ALL resize handles have high z-index
        zindex_fixes = [
            (r'(\.resize-handle[^}]*?)z-index:\s*50\s*!important', r'\1z-index: 1500 !important'),
            (r'(\.resize-handle[^}]*?)z-index:\s*500\s*!important', r'\1z-index: 1500 !important'),
        ]
        
        for pattern, replacement in zindex_fixes:
            content = re.sub(pattern, replacement, content)
        
        # 2. Fix sideboard content overlapping resize handle
        # Add CSS to prevent sideboard content from overlapping resize areas
        overlap_fix = """
/* FIX: Prevent sideboard content from overlapping resize handles */
.mtgo-sideboard-panel {
    z-index: 100 !important; /* Lower than resize handles (1500) */
}

.sideboard-content {
    padding-left: 15px !important; /* Create space for left resize handle */
    z-index: 100 !important; /* Lower than resize handles */
}

/* FIX: Ensure resize handles are always on top of content */
.resize-handle,
.resize-handle-left,
.resize-handle-right,
.resize-handle-bottom {
    z-index: 1500 !important; /* Higher than all content */
    pointer-events: auto !important;
}

/* FIX: Overflow menu z-index to be above sideboard */
.overflow-menu {
    z-index: 10000000 !important; /* Much higher than sideboard */
}
"""
        
        # Insert the fix before the nuclear z-index section
        nuclear_section = content.find('/* ===== NUCLEAR Z-INDEX HIERARCHY')
        if nuclear_section != -1:
            content = content[:nuclear_section] + overlap_fix + '\n\n' + content[nuclear_section:]
        else:
            content += overlap_fix
        
        # Write the fixed CSS
        with open(css_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ Resize handle overlap fix completed!")
        print("🔧 Fixed:")
        print("   - Z-index consistency (all handles → 1500)")
        print("   - Sideboard content padding to avoid overlap")
        print("   - Sideboard z-index below resize handles")
        print("   - Overflow menu z-index above sideboard")
        
        return True
        
    except FileNotFoundError:
        print(f"❌ Error: {css_file} not found")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    fix_overlap_and_zindex()
