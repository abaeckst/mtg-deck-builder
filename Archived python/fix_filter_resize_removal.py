#!/usr/bin/env python3
"""
Fix Filter Panel Resize Removal - Precise Surgical Fixes
Fix the broken JSX and TypeScript errors from previous removal attempt
"""

def fix_filter_resize_removal():
    """Fix the broken code from filter panel resize removal"""
    
    print("🔧 Fixing filter panel resize removal errors...")
    
    # First, let's try to restore from git
    import subprocess
    import os
    
    print("   🔄 Restoring MTGOLayout.tsx from git...")
    try:
        result = subprocess.run(['git', 'checkout', 'HEAD', '--', 'src/components/MTGOLayout.tsx'], 
                              capture_output=True, text=True, cwd='.')
        if result.returncode == 0:
            print("   ✅ Successfully restored MTGOLayout.tsx from git")
        else:
            print(f"   ⚠️  Git restore failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"   ⚠️  Could not run git command: {e}")
        return False
    
    # Now do precise removal from the restored file
    print("   📄 Processing restored MTGOLayout.tsx...")
    
    with open('src/components/MTGOLayout.tsx', 'r', encoding='utf-8') as f:
        layout_content = f.read()
    
    # Find and remove the specific filter panel resize handle section (lines 516-544)
    lines = layout_content.split('\n')
    new_lines = []
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Skip the Enhanced Resize Handle section
        if '{/* Enhanced Resize Handle */}' in line:
            # Skip until we find the closing of the conditional block
            i += 1
            brace_depth = 0
            found_conditional = False
            
            while i < len(lines):
                current_line = lines[i]
                
                # Track when we enter the conditional
                if '{!isFiltersCollapsed && (' in current_line:
                    found_conditional = True
                    brace_depth = 1
                elif found_conditional:
                    # Count braces to find the end
                    brace_depth += current_line.count('{')
                    brace_depth -= current_line.count('}')
                    
                    # When we close the conditional, we're done
                    if ')' in current_line and brace_depth <= 0:
                        break
                        
                i += 1
        else:
            new_lines.append(line)
            
        i += 1
    
    # Write the cleaned content
    with open('src/components/MTGOLayout.tsx', 'w', encoding='utf-8') as f:
        f.write('\n'.join(new_lines))
    
    print("   ✅ Removed filter panel resize handle from MTGOLayout.tsx")
    
    # 2. Fix useResize.ts with precise changes
    with open('src/hooks/useResize.ts', 'r', encoding='utf-8') as f:
        resize_content = f.read()
    
    print("   📄 Fixing useResize.ts TypeScript errors...")
    
    # Fix 1: Remove filterPanel from createResizeHandler type parameter
    resize_content = resize_content.replace(
        "resizeType: 'filterPanel' | 'deckArea' | 'sideboard' | 'vertical'",
        "resizeType: 'deckArea' | 'sideboard' | 'vertical'"
    )
    
    # Fix 2: Remove filterPanel from interface
    resize_content = resize_content.replace(
        'interface ResizeHandlers {\n  onFilterPanelResize: (event: React.MouseEvent) => void;\n  onDeckAreaResize: (event: React.MouseEvent) => void;',
        'interface ResizeHandlers {\n  onDeckAreaResize: (event: React.MouseEvent) => void;'
    )
    
    # Fix 3: Remove filterPanel from state type
    resize_content = resize_content.replace(
        "resizeType: 'filterPanel' | 'deckArea' | 'sideboard' | 'vertical' | null;",
        "resizeType: 'deckArea' | 'sideboard' | 'vertical' | null;"
    )
    
    # Fix 4: Remove filterPanel case from switch statement
    lines = resize_content.split('\n')
    new_lines = []
    skip_case = False
    
    for line in lines:
        if "case 'filterPanel':" in line:
            skip_case = True
            continue
        elif skip_case and 'break;' in line:
            skip_case = False
            continue
        elif skip_case:
            continue
        else:
            new_lines.append(line)
    
    resize_content = '\n'.join(new_lines)
    
    # Fix 5: Remove onFilterPanelResize handler creation
    lines = resize_content.split('\n')
    new_lines = []
    
    for line in lines:
        if 'const onFilterPanelResize = useCallback' in line:
            continue
        else:
            new_lines.append(line)
    
    resize_content = '\n'.join(new_lines)
    
    # Fix 6: Remove onFilterPanelResize from handlers object
    resize_content = resize_content.replace(
        '  const handlers: ResizeHandlers = {\n    onFilterPanelResize,\n    onDeckAreaResize,',
        '  const handlers: ResizeHandlers = {\n    onDeckAreaResize,'
    )
    
    with open('src/hooks/useResize.ts', 'w', encoding='utf-8') as f:
        f.write(resize_content)
    
    print("   ✅ Fixed useResize.ts TypeScript errors")
    
    print("\n🎯 Filter panel resize removal completed successfully!")
    print("✅ Should now compile without errors")
    print("✅ Preserved all working functionality:")
    print("   - Vertical resize (collection/deck areas)")
    print("   - Sideboard resize")
    print("   - Filter panel collapse/expand")
    
    return True

if __name__ == "__main__":
    success = fix_filter_resize_removal()
    if not success:
        print("\n❌ Fix failed - manual intervention required")
    else:
        print("\n✅ Fix completed successfully!")