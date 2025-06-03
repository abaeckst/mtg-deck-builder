#!/usr/bin/env python3
"""
Fix variable naming conflicts in useCards.ts
"""

def fix_variable_conflicts():
    file_path = 'src/hooks/useCards.ts'
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print('Fixing variable naming conflicts...')
    
    # Replace the first 'win' with 'windowRef'
    old_first_win = '''    // Prevent duplicate searches within 1 second
    const win = window as any;
    if (win.lastSearchKey === searchKey && win.lastSearchTime && (currentTime - win.lastSearchTime) < 1000) {
      console.log('SEARCH SKIPPED - Duplicate:', { query, format, searchKey });
      return;
    }
    
    win.lastSearchKey = searchKey;
    win.lastSearchTime = currentTime;'''

    new_first_win = '''    // Prevent duplicate searches within 1 second
    const windowRef = window as any;
    if (windowRef.lastSearchKey === searchKey && windowRef.lastSearchTime && (currentTime - windowRef.lastSearchTime) < 1000) {
      console.log('SEARCH SKIPPED - Duplicate:', { query, format, searchKey });
      return;
    }
    
    windowRef.lastSearchKey = searchKey;
    windowRef.lastSearchTime = currentTime;'''

    # Replace the second 'win' with 'winTracker' and fix TypeScript errors
    old_second_win = '''    // Initialize API tracking if not exists
    const win = window as any;
    if (!win.apiCallHistory) {
      win.apiCallHistory = [];
      win.searchCounter = 0;
    }
    
    win.searchCounter++;
    const searchId = `search-${win.searchCounter}`;'''

    new_second_win = '''    // Initialize API tracking if not exists
    const winTracker = window as any;
    if (!winTracker.apiCallHistory) {
      winTracker.apiCallHistory = [];
      winTracker.searchCounter = 0;
    }
    
    winTracker.searchCounter++;
    const searchId = `search-${winTracker.searchCounter}`;'''

    # Update the tracking code to use winTracker
    old_tracking = '''      // Track this API call
      const apiCallData = {
        searchId: searchId,
        searchNumber: win.searchCounter,
        query: query,
        format: format || 'none',
        duration: apiCallDuration,
        resultCount: response.data.length,
        totalCards: response.total_cards,
        hasMore: response.has_more,
        timestamp: new Date().toISOString(),
        firstCardName: response.data[0]?.name || 'NO_CARDS',
        // Check if results seem suspicious
        suspicious: response.data.length > 100 && query.length < 6
      };
      
      win.apiCallHistory.push(apiCallData);'''

    new_tracking = '''      // Track this API call
      const apiCallData = {
        searchId: searchId,
        searchNumber: winTracker.searchCounter,
        query: query,
        format: format || 'none',
        duration: apiCallDuration,
        resultCount: response.data.length,
        totalCards: response.total_cards,
        hasMore: response.has_more,
        timestamp: new Date().toISOString(),
        firstCardName: response.data[0]?.name || 'NO_CARDS',
        // Check if results seem suspicious
        suspicious: response.data.length > 100 && query.length < 6
      };
      
      winTracker.apiCallHistory.push(apiCallData);'''

    # Fix the pattern analysis code with proper TypeScript types
    old_pattern = '''      // Check for patterns indicating API issues
      if (win.apiCallHistory.length >= 3) {
        const recent = win.apiCallHistory.slice(-3);
        const avgDuration = recent.reduce((sum, call) => sum + call.duration, 0) / recent.length;
        const suspiciousCount = recent.filter(call => call.suspicious).length;'''

    new_pattern = '''      // Check for patterns indicating API issues
      if (winTracker.apiCallHistory.length >= 3) {
        const recent = winTracker.apiCallHistory.slice(-3);
        const avgDuration = recent.reduce((sum: number, call: any) => sum + call.duration, 0) / recent.length;
        const suspiciousCount = recent.filter((call: any) => call.suspicious).length;'''

    # Fix the error tracking
    old_error_track = '''        previousSuccessfulSearches: win.apiCallHistory.filter(call => call.resultCount > 0).length'''
    new_error_track = '''        previousSuccessfulSearches: winTracker.apiCallHistory.filter((call: any) => call.resultCount > 0).length'''

    # Apply all fixes
    if old_first_win in content:
        content = content.replace(old_first_win, new_first_win)
        print('✅ Fixed first window variable conflict')
    
    if old_second_win in content:
        content = content.replace(old_second_win, new_second_win)
        print('✅ Fixed second window variable conflict')
    
    if old_tracking in content:
        content = content.replace(old_tracking, new_tracking)
        print('✅ Fixed tracking variable references')
    
    if old_pattern in content:
        content = content.replace(old_pattern, new_pattern)
        print('✅ Fixed pattern analysis with TypeScript types')
    
    if old_error_track in content:
        content = content.replace(old_error_track, new_error_track)
        print('✅ Fixed error tracking variable')

    # Write the fixed content
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print('✅ All variable conflicts resolved')
    print('🧪 Try npm start now - should compile without errors')
    return True

if __name__ == '__main__':
    print('🚀 Fixing Variable Naming Conflicts')
    print('=' * 50)
    fix_variable_conflicts()
