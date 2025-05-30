#!/usr/bin/env python3
"""
Fix API degradation and race conditions based on console log analysis
Implement proper request queuing, rate limiting, and API health detection
"""

def fix_api_degradation():
    file_path = 'src/hooks/useCards.ts'
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print('Implementing comprehensive API degradation fix...')
    
    # Replace the entire searchForCards function with a robust version
    old_search_function_start = '  // Search for cards with query and optional format filter - DEDUPLICATED'
    old_search_function_end = '  }, [clearError, setLoading]);'
    
    start_idx = content.find(old_search_function_start)
    end_idx = content.find(old_search_function_end, start_idx) + len(old_search_function_end)
    
    if start_idx == -1 or end_idx == -1:
        print('❌ Could not find searchForCards function to replace')
        return False
    
    new_search_function = '''  // Search for cards with query and optional format filter - API DEGRADATION FIX
  const searchForCards = useCallback(async (query: string, format?: string) => {
    if (!query.trim()) {
      setState(prev => ({ 
        ...prev, 
        cards: [], 
        searchQuery: '', 
        totalCards: 0,
        selectedCards: new Set() // Clear selection when clearing search
      }));
      return;
    }

    // Initialize API health tracking
    const winTracker = window as any;
    if (!winTracker.apiHealth) {
      winTracker.apiHealth = {
        requestQueue: [],
        activeRequest: null,
        avgResponseTime: 500,
        degradationLevel: 0,
        lastRequestTime: 0,
        requestCounter: 0
      };
    }

    // Create search request
    const searchRequest = {
      id: ++winTracker.requestCounter,
      query: query,
      format: format || '',
      timestamp: Date.now(),
      searchKey: `${query}|${format || ''}`
    };

    console.log('🔍 SEARCH QUEUED:', {
      requestId: searchRequest.id,
      query: query,
      format: format,
      queueLength: winTracker.apiHealth.requestQueue.length,
      activeRequest: winTracker.apiHealth.activeRequest?.id || 'none',
      degradationLevel: winTracker.apiHealth.degradationLevel
    });

    // Add to queue
    winTracker.apiHealth.requestQueue.push(searchRequest);

    // Process queue if no active request
    if (!winTracker.apiHealth.activeRequest) {
      await processSearchQueue();
    }

    async function processSearchQueue() {
      while (winTracker.apiHealth.requestQueue.length > 0) {
        // Get next request
        const currentRequest = winTracker.apiHealth.requestQueue.shift();
        winTracker.apiHealth.activeRequest = currentRequest;

        // Skip if this is an old request (user typed ahead)
        const isStale = Date.now() - currentRequest.timestamp > 2000;
        if (isStale) {
          console.log('⏭️ SKIPPING STALE REQUEST:', { requestId: currentRequest.id, age: Date.now() - currentRequest.timestamp });
          continue;
        }

        // Rate limiting based on API health
        const timeSinceLastRequest = Date.now() - winTracker.apiHealth.lastRequestTime;
        const minDelay = Math.max(100, winTracker.apiHealth.degradationLevel * 500); // Increase delay when degraded
        
        if (timeSinceLastRequest < minDelay) {
          const waitTime = minDelay - timeSinceLastRequest;
          console.log('⏳ RATE LIMITING:', { waitMs: waitTime, degradationLevel: winTracker.apiHealth.degradationLevel });
          await new Promise(resolve => setTimeout(resolve, waitTime));
        }

        try {
          console.log('🚀 EXECUTING SEARCH:', {
            requestId: currentRequest.id,
            query: currentRequest.query,
            format: currentRequest.format,
            degradationLevel: winTracker.apiHealth.degradationLevel
          });

          clearError();
          setLoading(true);

          const requestStart = performance.now();
          winTracker.apiHealth.lastRequestTime = Date.now();

          // Execute API call
          const response = currentRequest.format && currentRequest.format !== '' 
            ? await searchCardsWithFilters(currentRequest.query, { 
                format: currentRequest.format === 'custom-standard' ? 'standard' : currentRequest.format 
              })
            : await searchCards(currentRequest.query);

          const requestDuration = performance.now() - requestStart;

          // Update API health metrics
          winTracker.apiHealth.avgResponseTime = (winTracker.apiHealth.avgResponseTime * 0.7) + (requestDuration * 0.3);
          
          // Detect API degradation
          const isSlow = requestDuration > 2000;
          const isSuspicious = response.data.length > 100 && currentRequest.query.length < 4;
          const isHealthy = requestDuration < 1000 && !isSuspicious;

          if (isHealthy && winTracker.apiHealth.degradationLevel > 0) {
            winTracker.apiHealth.degradationLevel = Math.max(0, winTracker.apiHealth.degradationLevel - 1);
          } else if (isSlow || isSuspicious) {
            winTracker.apiHealth.degradationLevel = Math.min(5, winTracker.apiHealth.degradationLevel + 1);
          }

          console.log('✅ SEARCH SUCCESS:', {
            requestId: currentRequest.id,
            query: currentRequest.query,
            duration: Math.round(requestDuration),
            resultCount: response.data.length,
            avgResponseTime: Math.round(winTracker.apiHealth.avgResponseTime),
            degradationLevel: winTracker.apiHealth.degradationLevel,
            suspicious: isSuspicious,
            firstCard: response.data[0]?.name || 'NO_RESULTS'
          });

          // Only update state if this is still the current search intent
          const isCurrentSearch = currentRequest.query === query && currentRequest.format === (format || '');
          if (isCurrentSearch) {
            setState(prev => ({
              ...prev,
              cards: response.data,
              searchQuery: currentRequest.query,
              totalCards: response.total_cards,
              hasMore: response.has_more,
              selectedCards: new Set(), // Clear selection on new search
            }));
          } else {
            console.log('🚫 IGNORING OUTDATED RESULT:', { 
              requestId: currentRequest.id, 
              requestQuery: currentRequest.query, 
              currentQuery: query 
            });
          }

        } catch (error) {
          const errorMessage = error instanceof Error ? error.message : 'Failed to search cards';
          
          // Increase degradation on errors
          winTracker.apiHealth.degradationLevel = Math.min(5, winTracker.apiHealth.degradationLevel + 2);
          
          console.error('❌ SEARCH ERROR:', {
            requestId: currentRequest.id,
            query: currentRequest.query,
            error: errorMessage,
            degradationLevel: winTracker.apiHealth.degradationLevel
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
          winTracker.apiHealth.activeRequest = null;
        }
      }
    }
  }, [clearError, setLoading]);'''

    # Replace the function
    before_function = content[:start_idx]
    after_function = content[end_idx:]
    content = before_function + new_search_function + after_function

    # Write the updated content
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print('✅ API degradation fix implemented!')
    print('\n🔧 Features Added:')
    print('   • Request queuing - Only one search at a time')
    print('   • Adaptive rate limiting - Slows down when API is degraded') 
    print('   • API health detection - Monitors response times and quality')
    print('   • Stale request filtering - Ignores old searches')
    print('   • Smart result validation - Detects suspicious responses')
    print('\n🧪 Testing Instructions:')
    print('   1. Refresh the page')
    print('   2. Type rapidly (e.g., "angel" character by character)')
    print('   3. Check console logs - should see:')
    print('      • 🔍 SEARCH QUEUED - Multiple requests queued')
    print('      • 🚀 EXECUTING SEARCH - Only one at a time')
    print('      • ✅ SEARCH SUCCESS - With health metrics')
    print('      • ⏳ RATE LIMITING - When API slows down')
    print('\n🎯 Expected Results:')
    print('   • No more race conditions')
    print('   • Consistent search results')
    print('   • Automatic slowdown when API degrades')
    print('   • Only latest search results displayed')
    
    return True

if __name__ == '__main__':
    print('🚀 Fixing API Degradation and Race Conditions')
    print('=' * 60)
    fix_api_degradation()
