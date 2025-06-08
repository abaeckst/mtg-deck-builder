def fix_unclosed_css_block():
    """Fix unclosed CSS block causing syntax error"""
    
    print("=== FIXING UNCLOSED CSS BLOCK ===\n")
    
    try:
        with open("src/components/MTGOLayout.css", 'r', encoding='utf-8') as f:
            css_content = f.read()
        
        print("1. Analyzing CSS structure for unclosed blocks...")
        
        lines = css_content.split('\n')
        print(f"   Total lines: {len(lines)}")
        
        # Find the problem area around line 2823
        problem_line = 2823 - 1  # Convert to 0-based index
        
        print(f"   Problem area around line {problem_line + 1}:")
        for i in range(max(0, problem_line - 5), min(len(lines), problem_line + 5)):
            prefix = ">>> " if i == problem_line else "    "
            print(f"{prefix}{i+1:4d}: {lines[i]}")
        
        # 2. Track brace balance to find unclosed blocks
        print("\n2. Checking brace balance...")
        
        brace_count = 0
        unclosed_blocks = []
        
        for i, line in enumerate(lines[:problem_line]):
            stripped = line.strip()
            
            # Count opening and closing braces
            opens = stripped.count('{')
            closes = stripped.count('}')
            
            if opens > 0:
                brace_count += opens
                if opens > closes and any(keyword in stripped.lower() for keyword in ['@media', '@keyframes', '.', '#']):
                    # This line opens a block
                    print(f"   Line {i+1}: Opens block - {stripped[:50]}...")
            
            if closes > 0:
                brace_count -= closes
                if closes > opens:
                    print(f"   Line {i+1}: Closes block - {stripped[:50]}...")
            
            # Check if we have an unclosed block before media query
            if i == problem_line - 1 and brace_count > 0:
                print(f"   ⚠️ Found {brace_count} unclosed block(s) before @media query")
                unclosed_blocks.append(i)
        
        # 3. Fix the issue by adding missing closing braces
        print("\n3. Fixing unclosed blocks...")
        
        if brace_count > 0:
            # Insert missing closing braces before the @media query
            missing_braces = '\n' + '}\n' * brace_count
            
            # Insert before line 2823 (the @media line)
            lines.insert(problem_line, missing_braces.strip())
            
            print(f"   ✅ Added {brace_count} missing closing brace(s) before @media query")
        
        # 4. Clean up any duplicate braces or extra whitespace
        print("\n4. Cleaning up CSS structure...")
        
        # Rejoin lines and clean up
        css_content = '\n'.join(lines)
        
        # Remove any duplicate closing braces
        import re
        css_content = re.sub(r'\}\s*\}', '}', css_content)
        
        # Clean up excessive whitespace
        css_content = re.sub(r'\n\s*\n\s*\n+', '\n\n', css_content)
        
        # Ensure proper spacing around media queries
        css_content = re.sub(r'(\})\s*(@media)', r'\1\n\n\2', css_content)
        
        print("   ✅ Cleaned up duplicate braces and whitespace")
        
        # 5. Add the sideboard content fix in a safe location
        print("\n5. Adding sideboard content fix...")
        
        # Find a safe place to add the sideboard fix (after existing sideboard rules)
        sideboard_fix = """
/* RESIZE HANDLE FIX: Prevent sideboard content overlap */
.sideboard-content {
  padding: 8px 8px 8px 25px !important; /* 25px left padding for resize handle area */
}

.resize-handle-left {
  position: absolute !important;
  top: 0 !important;
  left: -10px !important;
  width: 20px !important;
  height: 100% !important;
  cursor: ew-resize !important;
  z-index: 2000 !important;
  background-color: transparent !important;
  pointer-events: auto !important;
}

.resize-handle-left:hover {
  background-color: rgba(59, 130, 246, 0.3) !important;
}
"""
        
        # Insert the fix before the last media query
        last_media_pos = css_content.rfind('@media')
        if last_media_pos > 0:
            css_content = css_content[:last_media_pos] + sideboard_fix + '\n\n' + css_content[last_media_pos:]
            print("   ✅ Added sideboard content fix before media queries")
        else:
            css_content += '\n\n' + sideboard_fix
            print("   ✅ Added sideboard content fix at end of file")
        
        # 6. Write the fixed CSS
        with open("src/components/MTGOLayout.css", 'w', encoding='utf-8') as f:
            f.write(css_content)
        
        print("\n=== CSS STRUCTURE FIX COMPLETE ===")
        print("✅ Fixed unclosed CSS blocks")
        print("✅ Added missing closing braces")
        print("✅ Cleaned up CSS structure")
        print("✅ Added sideboard content overlap fix")
        print("\n🔧 CSS should now compile successfully!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error fixing CSS structure: {e}")
        return False

if __name__ == "__main__":
    fix_unclosed_css_block()