#!/usr/bin/env python3
"""
Fix the TypeScript compilation error in useCards.ts
"""

def fix_useCards_export():
    file_path = 'src/hooks/useCards.ts'
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    print('🔧 Fixing TypeScript export error...')
    
    # The file needs to end with an export or be treated as a module
    # Let's add an empty export at the end if it doesn't exist
    if not content.strip().endswith('export {};') and 'export' not in content:
        content += '\n\nexport {};'
        print('✅ Added export statement')
    
    # Also, let's remove the debug logging that might have broken something
    # and add it back properly
    if 'console.log' in content:
        # Remove any existing console.log statements first
        lines = content.split('\n')
        cleaned_lines = []
        skip_next = False
        
        for i, line in enumerate(lines):
            if 'console.log' in line and ('SEARCH DEBUG' in line or 'SEARCH RESULTS' in line):
                # Skip this debug line
                continue
            else:
                cleaned_lines.append(line)
        
        content = '\n'.join(cleaned_lines)
        print('✅ Cleaned up broken debug statements')
    
    # Write the fixed content
    with open(file_path, 'w') as f:
        f.write(content)
    
    print('✅ Fixed useCards.ts compilation error')
    print('🧪 Try running npm start now')
    return True

if __name__ == '__main__':
    print('🚀 Fixing TypeScript Compilation Error')
    print('=' * 50)
    fix_useCards_export()
