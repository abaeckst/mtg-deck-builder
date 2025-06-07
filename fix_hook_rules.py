#!/usr/bin/env python3
"""
Fix React Hook rules violation in MTGOLayout.tsx
Move all hooks to top level of component before return statement
"""

import re

def fix_hook_rules():
    """Move all hooks to top of component to fix React Hook rules violation"""
    print("🔧 Fixing React Hook rules violation in MTGOLayout.tsx...")
    
    # Read the file
    try:
        with open('src/components/MTGOLayout.tsx', 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print("❌ MTGOLayout.tsx not found")
        return False
    
    lines = content.split('\n')
    
    # Find component start and return statement
    component_start = -1
    return_line = -1
    
    for i, line in enumerate(lines):
        if 'const MTGOLayout: React.FC' in line:
            component_start = i
        if line.strip().startswith('return (') and component_start != -1:
            return_line = i
            break
    
    if component_start == -1 or return_line == -1:
        print("❌ Could not find component structure")
        return False
    
    print(f"📍 Component starts at line {component_start + 1}")
    print(f"📍 Return statement at line {return_line + 1}")
    
    # Extract all hook definitions and their dependencies that come after return
    hooks_to_move = []
    i = return_line + 1
    
    while i < len(lines):
        line = lines[i]
        
        # Look for hook definitions
        if ('useCallback(' in line or 'useMemo(' in line) and ('const ' in line or line.strip().startswith('const ')):
            # This is a hook definition that needs to be moved
            hook_start = i
            hook_lines = [line]
            brace_count = line.count('{') - line.count('}')
            paren_count = line.count('(') - line.count(')')
            
            # Collect the complete hook definition
            j = i + 1
            while j < len(lines) and (brace_count > 0 or paren_count > 0 or not hook_lines[-1].strip().endswith(';')):
                hook_lines.append(lines[j])
                brace_count += lines[j].count('{') - lines[j].count('}')
                paren_count += lines[j].count('(') - lines[j].count(')')
                j += 1
            
            hooks_to_move.append({
                'lines': hook_lines,
                'start': hook_start,
                'end': j - 1
            })
            
            i = j
        else:
            i += 1
    
    if not hooks_to_move:
        print("✅ No hooks found after return statement - may already be fixed")
        return True
    
    print(f"📦 Found {len(hooks_to_move)} hooks to move:")
    for hook in hooks_to_move:
        hook_name = hook['lines'][0].strip()[:60] + "..." if len(hook['lines'][0]) > 60 else hook['lines'][0].strip()
        print(f"  - {hook_name}")
    
    # Remove hooks from their current locations (in reverse order to maintain indices)
    new_lines = lines.copy()
    for hook in reversed(hooks_to_move):
        del new_lines[hook['start']:hook['end'] + 1]
    
    # Find the best insertion point (after existing hooks but before return)
    insertion_point = return_line
    
    # Look backwards from return to find last hook
    for i in range(return_line - 1, component_start, -1):
        if any(hook_keyword in new_lines[i] for hook_keyword in ['useState', 'useEffect', 'useCallback', 'useMemo', 'useRef']):
            insertion_point = i + 1
            break
    
    # Insert all moved hooks at the insertion point
    all_hook_lines = []
    for hook in hooks_to_move:
        all_hook_lines.extend(hook['lines'])
        all_hook_lines.append('')  # Add spacing between hooks
    
    # Insert the moved hooks
    new_lines = new_lines[:insertion_point] + all_hook_lines + new_lines[insertion_point:]
    
    # Write the fixed content
    try:
        with open('src/components/MTGOLayout.tsx', 'w', encoding='utf-8') as f:
            f.write('\n'.join(new_lines))
        
        print("✅ Successfully moved all hooks to top level of component")
        print(f"📍 Moved {len(hooks_to_move)} hooks before return statement")
        print("🎯 React Hook rules violation should now be fixed")
        return True
        
    except Exception as e:
        print(f"❌ Error writing file: {e}")
        return False

if __name__ == "__main__":
    fix_hook_rules()
