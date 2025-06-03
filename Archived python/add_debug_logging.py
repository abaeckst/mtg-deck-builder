#!/usr/bin/env python3
"""
Add debug logging to search function to diagnose the "light" search issue
"""

def add_debug_logging():
    file_path = 'src/hooks/useCards.ts'
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    print('🔧 Adding debug logging to search function...')
    
    # Add debug logging right before the API call
    old_api_call = '''    try {
      // Use format-aware search if format is specified
      const response = format && format !== '' 
        ? await searchCardsWithFilters(query, { format: format === 'custom-standard' ? 'standard' : format })
        : await searchCards(query);'''

    new_api_call = '''    try {
      console.log('🔍 SEARCH DEBUG:', { 
        query: query, 
        format: format, 
        timestamp: new Date().toISOString() 
      });
      
      // Use format-aware search if format is specified
      const response = format && format !== '' 
        ? await searchCardsWithFilters(query, { format: format === 'custom-standard' ? 'standard' : format })
        : await searchCards(query);
      
      console.log('📊 SEARCH RESULTS:', { 
        query: query, 
        resultCount: response.data.length, 
        firstCards: response.data.slice(0, 5).map(card => card.name),
        timestamp: new Date().toISOString() 
      });'''

    if old_api_call in content:
        content = content.replace(old_api_call, new_api_call)
        with open(file_path, 'w') as f:
            f.write(content)
        print('✅ Added debug logging to useCards.ts')
        print('\n🧪 Testing Instructions:')
        print('1. Refresh your browser page (important!)')
        print('2. Open Console (F12)')
        print('3. Search for "light"')
        print('4. Check console for 🔍 SEARCH DEBUG and 📊 SEARCH RESULTS messages')
        print('\n📋 This will show us:')
        print('   • Exact query being sent to API')
        print('   • What results are actually returned')
        print('   • Whether multiple searches are happening')
        return True
    else:
        print('❌ Could not find the API call pattern to update')
        return False

if __name__ == '__main__':
    print('🚀 Adding Debug Logging for Search Issue')
    print('=' * 50)
    add_debug_logging()
