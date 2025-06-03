#!/usr/bin/env python3
"""
Restore the useCards export that got accidentally removed
"""

def restore_useCards_export():
    file_path = 'src/hooks/useCards.ts'
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    print('🔧 Restoring useCards export...')
    
    # The useCards function should be exported
    # Find the useCards function definition and make sure it's exported
    if 'export const useCards' not in content:
        # Replace 'const useCards' with 'export const useCards'
        if 'const useCards = ():' in content:
            content = content.replace('const useCards = ():', 'export const useCards = ():')
            print('✅ Added export to useCards function')
        elif 'export const useCards' in content:
            print('✅ useCards already exported')
        else:
            print('❌ Could not find useCards function to export')
            return False
    else:
        print('✅ useCards is already exported')
    
    # Remove any empty export at the end if we added one
    if content.strip().endswith('export {};'):
        content = content.replace('export {};', '').strip()
        print('✅ Removed unnecessary empty export')
    
    # Write the fixed content
    with open(file_path, 'w') as f:
        f.write(content)
    
    print('✅ Fixed useCards export')
    print('🧪 Try running npm start now')
    return True

if __name__ == '__main__':
    print('🚀 Restoring useCards Export')
    print('=' * 50)
    restore_useCards_export()
