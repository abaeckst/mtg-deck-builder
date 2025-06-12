import re

def fix_resize_handle_overlap():
    """Fix sideboard content overlapping resize handle + update minimum deck size from 8% to 15%"""
    
    print("=== FIXING RESIZE HANDLE OVERLAP + DECK MINIMUM SIZE ===\n")
    
    # 1. Fix sideboard content overlap in CSS
    print("1. Fixing sideboard content overlap in MTGOLayout.css...")
    
    try:
        with open("src/components/MTGOLayout.css", 'r', encoding='utf-8') as f:
            css_content = f.read()
        
        # Find and update sideboard-content padding to prevent overlap
        # Look for existing sideboard-content rule
        sideboard_content_pattern = r'\.sideboard-content\s*\{[^}]*\}'
        
        if re.search(sideboard_content_pattern, css_content):
            # Update existing rule to add left padding
            css_content = re.sub(
                r'(\.sideboard-content\s*\{[^}]*?)(padding[^;]*;)?([^}]*\})',
                r'\1padding: 8px 8px 8px 25px !important; /* Left padding prevents resize handle overlap */\3',
                css_content,
                flags=re.DOTALL
            )
            print("   ✅ Updated existing .sideboard-content rule with left padding")
        else:
            # Add new rule if not found
            css_content += """
/* FIX: Prevent sideboard content from overlapping left resize handle */
.sideboard-content {
  padding: 8px 8px 8px 25px !important; /* 25px left padding for resize handle area */
}
"""
            print("   ✅ Added new .sideboard-content rule with left padding")
        
        # Ensure resize handles have proper z-index and cursor
        resize_handle_css = """
/* ENHANCED: Resize handles with guaranteed visibility and interaction */
.resize-handle-left {
  position: absolute !important;
  top: 0 !important;
  left: -10px !important;
  width: 20px !important;
  height: 100% !important;
  cursor: ew-resize !important;
  z-index: 2000 !important; /* Higher than all content */
  background-color: transparent !important;
  pointer-events: auto !important;
}

.resize-handle-left:hover {
  background-color: rgba(59, 130, 246, 0.3) !important;
}

.resize-handle-left:active {
  background-color: rgba(59, 130, 246, 0.5) !important;
}

/* Ensure all resize handles are visible and accessible */
.resize-handle,
.resize-handle-right,
.resize-handle-vertical {
  z-index: 2000 !important;
  pointer-events: auto !important;
  cursor: inherit !important;
}

.resize-handle:hover,
.resize-handle-right:hover,
.resize-handle-vertical:hover {
  background-color: rgba(59, 130, 246, 0.3) !important;
}
"""
        
        # Add/update resize handle styles
        if ".resize-handle-left" in css_content:
            # Replace existing resize handle rules
            css_content = re.sub(
                r'\.resize-handle-left\s*\{[^}]*\}[^/]*(/\*[^*]*\*/)?',
                resize_handle_css,
                css_content,
                flags=re.DOTALL
            )
            print("   ✅ Updated existing resize handle CSS")
        else:
            css_content += resize_handle_css
            print("   ✅ Added enhanced resize handle CSS")
        
        with open("src/components/MTGOLayout.css", 'w', encoding='utf-8') as f:
            f.write(css_content)
        
        print("   ✅ Updated MTGOLayout.css with sideboard content fix\n")
        
    except Exception as e:
        print(f"   ❌ Error updating CSS: {e}\n")
        return False
    
    # 2. Update minimum deck area size from 8% to 15%
    print("2. Updating minimum deck area size in useLayout.ts...")
    
    try:
        with open("src/hooks/useLayout.ts", 'r', encoding='utf-8') as f:
            layout_content = f.read()
        
        # Find and update the minimum constraint from 8 to 15
        updated_content = re.sub(
            r'deckAreaHeightPercent:\s*\{\s*min:\s*8,',
            'deckAreaHeightPercent: { min: 15,',
            layout_content
        )
        
        if updated_content != layout_content:
            with open("src/hooks/useLayout.ts", 'w', encoding='utf-8') as f:
                f.write(updated_content)
            print("   ✅ Updated minimum deck area height from 8% to 15%\n")
        else:
            print("   ⚠️ Minimum deck area constraint not found or already updated\n")
        
    except Exception as e:
        print(f"   ❌ Error updating useLayout.ts: {e}\n")
        return False
    
    print("=== FIX COMPLETE ===")
    print("✅ Sideboard content now has 25px left padding to avoid resize handle")
    print("✅ Resize handles have enhanced z-index and cursor properties")  
    print("✅ Minimum deck area size updated to 15% for better usability")
    print("\n🔧 Please test:")
    print("1. Look for resize cursor between deck and sideboard panels")
    print("2. Verify deck area cannot be resized below 15% of screen height")
    print("3. Check that sideboard content doesn't overlap resize handle area")
    
    return True

if __name__ == "__main__":
    fix_resize_handle_overlap()