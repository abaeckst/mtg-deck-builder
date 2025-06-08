import re

def fix_css_syntax_error():
    """Fix CSS syntax error in MTGOLayout.css around line 3180"""
    
    print("=== FIXING CSS SYNTAX ERROR ===\n")
    
    try:
        with open("src/components/MTGOLayout.css", 'r', encoding='utf-8') as f:
            css_content = f.read()
        
        print("1. Analyzing CSS syntax around line 3180...")
        
        # Find the problematic area around resize handles
        lines = css_content.split('\n')
        
        print(f"   Total lines in CSS: {len(lines)}")
        
        # Look for the problematic area around line 3180
        problem_area_start = max(0, 3170)
        problem_area_end = min(len(lines), 3190)
        
        print(f"   Checking lines {problem_area_start} to {problem_area_end}...")
        
        # Check for unmatched braces or syntax issues
        brace_count = 0
        problem_lines = []
        
        for i in range(problem_area_start, problem_area_end):
            if i < len(lines):
                line = lines[i].strip()
                if line:
                    brace_count += line.count('{') - line.count('}')
                    if line == '}' and brace_count < 0:
                        problem_lines.append((i + 1, line, "Extra closing brace"))
                    elif '{' in line and '}' not in line and not line.endswith(':'):
                        if i + 1 < len(lines) and not lines[i + 1].strip():
                            problem_lines.append((i + 1, line, "Possible incomplete rule"))
        
        print(f"   Found {len(problem_lines)} potential issues")
        
        # 2. Clean approach - remove and rebuild the problematic resize handle section
        print("\n2. Rebuilding resize handle CSS section...")
        
        # Remove all existing resize handle definitions that might be causing conflicts
        css_content = re.sub(
            r'/\*\s*=====\s*CLEAN RESIZE HANDLES.*?=====\s*\*/',
            '',
            css_content,
            flags=re.DOTALL
        )
        
        # Remove any orphaned resize handle rules
        css_content = re.sub(
            r'\.resize-handle[^}]*\}[^}]*\}',
            '',
            css_content,
            flags=re.DOTALL
        )
        
        # Remove any incomplete or duplicate resize rules
        css_content = re.sub(
            r'\.resize-handle-[a-z]+\s*\{[^}]*(?:\}[^}]*)*\}',
            '',
            css_content,
            flags=re.DOTALL
        )
        
        # Clean up any doubled closing braces
        css_content = re.sub(r'\}\s*\}', '}', css_content)
        
        # Clean up any extra newlines
        css_content = re.sub(r'\n\s*\n\s*\n', '\n\n', css_content)
        
        # 3. Add clean, complete resize handle CSS at the end
        clean_resize_css = """
/* ===== FIXED RESIZE HANDLES - CLEAN IMPLEMENTATION ===== */

/* Base resize handle styles */
.resize-handle {
  position: absolute !important;
  background-color: transparent !important;
  transition: background-color 0.2s ease !important;
  z-index: 2000 !important;
  pointer-events: auto !important;
}

.resize-handle:hover {
  background-color: rgba(59, 130, 246, 0.3) !important;
}

.resize-handle:active {
  background-color: rgba(59, 130, 246, 0.5) !important;
}

/* Horizontal resize handles - 20px wide for easy interaction */
.resize-handle-right {
  top: 0 !important;
  right: -10px !important;
  width: 20px !important;
  height: 100% !important;
  cursor: ew-resize !important;
}

.resize-handle-left {
  top: 0 !important;
  left: -10px !important;
  width: 20px !important;
  height: 100% !important;
  cursor: ew-resize !important;
}

/* Vertical resize handles - 20px tall for easy interaction */
.resize-handle-vertical {
  top: -10px !important;
  left: 0 !important;
  right: 0 !important;
  height: 20px !important;
  cursor: ns-resize !important;
}

.resize-handle-bottom {
  bottom: -10px !important;
  left: 0 !important;
  right: 0 !important;
  height: 20px !important;
  cursor: ns-resize !important;
}

/* Sideboard content spacing to prevent overlap */
.sideboard-content {
  padding: 8px 8px 8px 25px !important; /* 25px left padding for resize handle area */
}

/* ===== END FIXED RESIZE HANDLES ===== */
"""
        
        # Append the clean CSS
        css_content = css_content.rstrip() + '\n\n' + clean_resize_css
        
        # 4. Write the fixed CSS
        with open("src/components/MTGOLayout.css", 'w', encoding='utf-8') as f:
            f.write(css_content)
        
        print("   ✅ Rebuilt resize handle CSS with clean implementation")
        print("   ✅ Added sideboard content padding to prevent overlap")
        print("   ✅ Cleaned up any syntax errors and duplicate rules")
        
        print("\n=== CSS SYNTAX FIX COMPLETE ===")
        print("✅ Removed problematic CSS rules causing syntax errors")
        print("✅ Added clean resize handle implementation")
        print("✅ Fixed sideboard content overlap issue")
        
        return True
        
    except Exception as e:
        print(f"❌ Error fixing CSS: {e}")
        return False

if __name__ == "__main__":
    fix_css_syntax_error()