#!/usr/bin/env python3
"""
Fix remaining 'win' variable references that weren't caught
"""

def fix_remaining_win_references():
    file_path = 'src/hooks/useCards.ts'
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print('Fixing remaining win variable references...')
    
    # Fix the console.log with win.searchCounter
    old_search_start_log = '''    console.log('🔍 SEARCH START:', { 
      searchId: searchId,
      searchNumber: win.searchCounter,
      query: query, 
      format: format, 
      searchKey: searchKey,
      timestamp: new Date().toISOString(),
      totalPreviousSearches: win.apiCallHistory.length
    });'''

    new_search_start_log = '''    console.log('🔍 SEARCH START:', { 
      searchId: searchId,
      searchNumber: winTracker.searchCounter,
      query: query, 
      format: format, 
      searchKey: searchKey,
      timestamp: new Date().toISOString(),
      totalPreviousSearches: winTracker.apiCallHistory.length
    });'''

    # Fix the error logging with win.searchCounter
    old_error_log = '''      console.error('❌ API ERROR:', {
        searchId: searchId,
        searchNumber: win.searchCounter,
        query: query,
        format: format,
        error: errorMessage,
        timestamp: new Date().toISOString(),
        previousSuccessfulSearches: winTracker.apiCallHistory.filter((call: any) => call.resultCount > 0).length
      });'''

    new_error_log = '''      console.error('❌ API ERROR:', {
        searchId: searchId,
        searchNumber: winTracker.searchCounter,
        query: query,
        format: format,
        error: errorMessage,
        timestamp: new Date().toISOString(),
        previousSuccessfulSearches: winTracker.apiCallHistory.filter((call: any) => call.resultCount > 0).length
      });'''

    # Apply fixes
    if old_search_start_log in content:
        content = content.replace(old_search_start_log, new_search_start_log)
        print('✅ Fixed search start logging win references')
    else:
        # Try a more flexible approach
        content = content.replace('win.searchCounter', 'winTracker.searchCounter')
        content = content.replace('win.apiCallHistory', 'winTracker.apiCallHistory')
        print('✅ Fixed win references with flexible replacement')
    
    if old_error_log in content:
        content = content.replace(old_error_log, new_error_log)
        print('✅ Fixed error logging win references')

    # Write the fixed content
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print('✅ All remaining win references fixed')
    print('🧪 Try npm start now - should compile successfully')
    return True

if __name__ == '__main__':
    print('🚀 Fixing Remaining Win Variable References')
    print('=' * 50)
    fix_remaining_win_references()
