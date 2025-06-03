#!/usr/bin/env python3
"""
Investigate potential Scryfall API degradation after repeated searches
Track API response patterns, timing, and potential rate limiting issues
"""

def add_comprehensive_api_debugging():
    file_path = 'src/hooks/useCards.ts'
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print('Adding comprehensive API debugging...')
    
    # Add comprehensive API tracking
    old_search_debug = '''    console.log('SEARCH DEBUG:', { 
      query: query, 
      format: format, 
      searchKey: searchKey,
      timestamp: new Date().toISOString() 
    });'''

    new_search_debug = '''    // Initialize API tracking if not exists
    const win = window as any;
    if (!win.apiCallHistory) {
      win.apiCallHistory = [];
      win.searchCounter = 0;
    }
    
    win.searchCounter++;
    const searchId = `search-${win.searchCounter}`;
    
    console.log('🔍 SEARCH START:', { 
      searchId: searchId,
      searchNumber: win.searchCounter,
      query: query, 
      format: format, 
      searchKey: searchKey,
      timestamp: new Date().toISOString(),
      totalPreviousSearches: win.apiCallHistory.length
    });'''

    if old_search_debug in content:
        content = content.replace(old_search_debug, new_search_debug)
        print('✅ Enhanced search start logging')
    else:
        print('❌ Could not find search debug to enhance')
        return False

    # Enhance the API call logging
    old_api_call = '''    try {
      // Use format-aware search if format is specified
      const response = format && format !== '' 
        ? await searchCardsWithFilters(query, { format: format === 'custom-standard' ? 'standard' : format })
        : await searchCards(query);'''

    new_api_call = '''    try {
      const apiCallStart = performance.now();
      
      // Use format-aware search if format is specified
      const response = format && format !== '' 
        ? await searchCardsWithFilters(query, { format: format === 'custom-standard' ? 'standard' : format })
        : await searchCards(query);
      
      const apiCallEnd = performance.now();
      const apiCallDuration = apiCallEnd - apiCallStart;
      
      // Track this API call
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
      
      win.apiCallHistory.push(apiCallData);
      
      console.log('📊 API RESPONSE:', apiCallData);
      
      // Check for patterns indicating API issues
      if (win.apiCallHistory.length >= 3) {
        const recent = win.apiCallHistory.slice(-3);
        const avgDuration = recent.reduce((sum, call) => sum + call.duration, 0) / recent.length;
        const suspiciousCount = recent.filter(call => call.suspicious).length;
        
        console.log('📈 API PATTERN ANALYSIS:', {
          recentSearches: recent.length,
          averageResponseTime: Math.round(avgDuration),
          suspiciousResults: suspiciousCount,
          patternWarning: suspiciousCount >= 2 ? 'POTENTIAL_API_DEGRADATION' : 'NORMAL'
        });
      }'''

    if old_api_call in content:
        content = content.replace(old_api_call, new_api_call)
        print('✅ Enhanced API call tracking')
    else:
        print('❌ Could not find API call to enhance')
        return False

    # Add error tracking
    old_catch_block = '''    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Failed to search cards';
      setState(prev => ({
        ...prev,
        error: errorMessage,
        cards: [],
        totalCards: 0,
        hasMore: false,
      }));
    } finally {
      setLoading(false);
    }'''

    new_catch_block = '''    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Failed to search cards';
      
      // Track API errors
      console.error('❌ API ERROR:', {
        searchId: searchId,
        searchNumber: win.searchCounter,
        query: query,
        format: format,
        error: errorMessage,
        timestamp: new Date().toISOString(),
        previousSuccessfulSearches: win.apiCallHistory.filter(call => call.resultCount > 0).length
      });
      
      setState(prev => ({
        ...prev,
        error: errorMessage,
        cards: [],
        totalCards: 0,
        hasMore: false,
      }));
    } finally {
      setLoading(false);
      
      // Log search completion
      console.log('✅ SEARCH COMPLETE:', {
        searchId: searchId,
        query: query,
        timestamp: new Date().toISOString()
      });
    }'''

    if old_catch_block in content:
        content = content.replace(old_catch_block, new_catch_block)
        print('✅ Enhanced error tracking')
    else:
        print('❌ Could not find catch block to enhance')
        return False

    # Write the updated content
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print('✅ Comprehensive API debugging added')
    print('\n🧪 Investigation Plan:')
    print('1. Refresh the page')
    print('2. Do 5-10 searches (mix of terms and formats)')
    print('3. Watch console for:')
    print('   • 📊 API RESPONSE - response times and result patterns')
    print('   • 📈 API PATTERN ANALYSIS - degradation warnings')
    print('   • ❌ API ERROR - any API failures')
    print('4. Look for patterns:')
    print('   • Response times increasing over time?')
    print('   • "suspicious" results (too broad) after multiple searches?')
    print('   • "POTENTIAL_API_DEGRADATION" warnings?')
    print('\n📋 This will help identify:')
    print('   • Rate limiting issues')
    print('   • API response degradation')
    print('   • Timing patterns')
    print('   • Result quality changes over time')
    
    return True

if __name__ == '__main__':
    print('🚀 Investigating Scryfall API Degradation')
    print('=' * 50)
    add_comprehensive_api_debugging()
