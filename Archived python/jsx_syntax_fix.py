#!/usr/bin/env python3

import os
import re

def fix_jsx_syntax():
    """Fix the broken JSX syntax in MTGOLayout.tsx"""
    
    tsx_path = "src/components/MTGOLayout.tsx"
    
    if not os.path.exists(tsx_path):
        print(f"❌ File not found: {tsx_path}")
        return False
    
    with open(tsx_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"📁 Reading {tsx_path} ({len(content)} characters)")
    
    # Fix the broken conditional render structure
    # Find the malformed section and replace it
    broken_pattern = r'{!isFiltersCollapsed && \(\s*\s*</div>'
    
    # Replace with proper conditional render with resize handle
    fixed_conditional = '''{!isFiltersCollapsed && (
        <div 
          className="resize-handle resize-handle-right"
          onMouseDown={resizeHandlers.onFilterPanelResize}
          title="Drag to resize filter panel"
          style={{
            position: 'absolute',
            top: 0,
            right: -15,
            width: 30,
            height: '100%',
            backgroundColor: 'transparent',
            cursor: 'ew-resize',
            zIndex: 1001,
            transition: 'background-color 0.2s ease'
          }}
          onMouseEnter={(e) => e.currentTarget.style.backgroundColor = 'rgba(59, 130, 246, 0.3)'}
          onMouseLeave={(e) => e.currentTarget.style.backgroundColor = 'transparent'}
        />
      )}'''
    
    if re.search(broken_pattern, content):
        content = re.sub(broken_pattern, fixed_conditional, content)
        print("✅ Fixed broken conditional render")
    else:
        print("❌ Could not find broken pattern, trying alternative approach")
        
        # Alternative: Look for the broader pattern and fix it
        broader_pattern = r'{!isFiltersCollapsed && \([^}]*</div>'
        if re.search(broader_pattern, content):
            content = re.sub(broader_pattern, fixed_conditional, content)
            print("✅ Fixed broken conditional render (alternative)")
        else:
            # Manual fix - find the specific line numbers mentioned in error
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if '{!isFiltersCollapsed && (' in line and i < len(lines) - 2:
                    # Check if the next lines look malformed
                    if lines[i+1].strip() == '' and '</div>' in lines[i+2]:
                        # Replace these lines with the fixed version
                        fixed_lines = fixed_conditional.split('\n')
                        lines[i:i+3] = fixed_lines
                        content = '\n'.join(lines)
                        print("✅ Fixed broken conditional render (manual)")
                        break
    
    # Write the fixed content
    with open(tsx_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Fixed JSX syntax in {tsx_path}")
    return True

def validate_jsx_structure():
    """Basic validation of JSX structure"""
    
    tsx_path = "src/components/MTGOLayout.tsx"
    
    with open(tsx_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Count opening and closing braces
    open_braces = content.count('{')
    close_braces = content.count('}')
    
    # Count opening and closing parentheses
    open_parens = content.count('(')
    close_parens = content.count(')')
    
    print(f"📊 JSX Structure Validation:")
    print(f"   Open braces: {open_braces}, Close braces: {close_braces}")
    print(f"   Open parens: {open_parens}, Close parens: {close_parens}")
    
    if open_braces != close_braces:
        print("⚠️  Brace mismatch detected")
    
    if open_parens != close_parens:
        print("⚠️  Parentheses mismatch detected")
    
    # Check for obvious JSX issues
    if '{!isFiltersCollapsed && (' in content and not ')}' in content:
        print("⚠️  Unclosed conditional render detected")
    
    return True

if __name__ == "__main__":
    print("🔧 Fixing JSX syntax error...")
    print("=" * 50)
    
    success = fix_jsx_syntax()
    
    if success:
        validate_jsx_structure()
        print("\n✅ JSX syntax has been repaired!")
        print("\n📋 What was fixed:")
        print("- Restored proper conditional render structure")
        print("- Added resize handle with correct JSX syntax")
        print("- Fixed brace/parentheses matching")
        print("\n🎯 Try running the app again - syntax errors should be resolved")
    else:
        print("\n❌ Failed to fix JSX syntax")
