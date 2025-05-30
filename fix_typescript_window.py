#!/usr/bin/env python3
"""
Fix TypeScript window property errors by using proper typing
"""

def fix_typescript_window():
    file_path = 'src/hooks/useCards.ts'
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print('Fixing TypeScript window property errors...')
    
    # Replace window properties with proper TypeScript casting
    old_window_check = '''    // Prevent duplicate searches within 1 second
    if (window.lastSearchKey === searchKey && window.lastSearchTime && (currentTime - window.lastSearchTime) < 1000) {
      console.log('SEARCH SKIPPED - Duplicate:', { query, format, searchKey });
      return;
    }
    
    window.lastSearchKey = searchKey;
    window.lastSearchTime = currentTime;'''

    new_window_check = '''    // Prevent duplicate searches within 1 second
    const win = window as any;
    if (win.lastSearchKey === searchKey && win.lastSearchTime && (currentTime - win.lastSearchTime) < 1000) {
      console.log('SEARCH SKIPPED - Duplicate:', { query, format, searchKey });
      return;
    }
    
    win.lastSearchKey = searchKey;
    win.lastSearchTime = currentTime;'''

    if old_window_check in content:
        content = content.replace(old_window_check, new_window_check)
        print('✅ Fixed TypeScript window property errors')
    else:
        print('❌ Could not find window property code to fix')
        return False

    # Write the updated content
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print('✅ TypeScript errors fixed')
    print('🧪 Try npm start now - should compile without errors')
    return True

if __name__ == '__main__':
    print('🚀 Fixing TypeScript Window Property Errors')
    print('=' * 50)
    fix_typescript_window()
