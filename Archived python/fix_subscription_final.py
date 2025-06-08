#!/usr/bin/env python3

import os
import sys

def fix_subscription_final(filename):
    """Fix subscription useEffect to run by removing all unstable dependencies"""
    
    if not os.path.exists(filename):
        print(f"Error: {filename} not found")
        return False
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix the subscription useEffect to only depend on stable functions
    old_subscription_effect = """  // Subscribe to collection sort changes - FIXED DEPENDENCIES
  useEffect(() => {
    console.log('🔔 SUBSCRIPTION SETUP STARTED - useCards mounting');
    console.log('🔔 Available dependencies:', {
      hasSubscribe: typeof subscribe,
      hasUnsubscribe: typeof unsubscribe,
      subscribeFunction: subscribe?.toString().substring(0, 100) + '...'
    });
    
    try {
      const subscriptionId = subscribe((area: AreaType, sortState) => {
        console.log('📢 SORT SUBSCRIPTION EVENT RECEIVED:', { 
          area, 
          sortState,
          timestamp: new Date().toISOString(),
          eventId: Math.random().toString(36).substr(2, 9)
        });
        
        if (area === 'collection') {
          console.log('🔄 Collection sort changed:', sortState);
          // Access current metadata directly from state at event time
          setState(currentState => {
            console.log('🔍 Current search metadata:', currentState.lastSearchMetadata);
            
            if (currentState.lastSearchMetadata) {
              console.log('✅ Triggering handleCollectionSortChange with:', {
                criteria: sortState.criteria,
                direction: sortState.direction
              });
              
              // Call the sort handler with current metadata
              const metadata = currentState.lastSearchMetadata;
              const shouldUseServerSort = metadata.totalCards > 75;
              
              console.log('🤔 Sort decision analysis:', {
                criteria: sortState.criteria,
                direction: sortState.direction,
                totalCards: metadata.totalCards,
                loadedCards: metadata.loadedCards,
                threshold: 75,
                shouldUseServerSort,
                reason: shouldUseServerSort ? 'Large dataset - trigger server-side sort' : 'Small dataset - use client-side sort'
              });

              if (shouldUseServerSort) {
                console.log('🌐 TRIGGERING SERVER-SIDE SORT - new Scryfall search');
                
                // Get sort parameters and trigger search
                const sortParams = getScryfallSortParams('collection');
                console.log('🔧 Using sort params for re-search:', sortParams);
                
                searchWithPagination(metadata.query, metadata.filters).catch(error => {
                  console.error('❌ Sort-triggered search failed:', error);
                });
              } else {
                console.log('🏠 Using CLIENT-SIDE sorting - handled by UI components');
              }
            } else {
              console.log('❌ No search metadata - cannot trigger sort change');
            }
            
            return currentState; // No state change needed
          });
        } else {
          console.log('ℹ️ Sort change for non-collection area:', area);
        }
      });

      console.log('🔔 Sort subscription established with ID:', subscriptionId);
      console.log('🔔 SUBSCRIPTION SETUP COMPLETE');

      return () => {
        console.log('🔕 Unsubscribing from sort changes:', subscriptionId);
        unsubscribe(subscriptionId);
      };
    } catch (error) {
      console.error('❌ SUBSCRIPTION SETUP FAILED:', error);
      return () => {}; // Empty cleanup function
    }
  }, [subscribe, unsubscribe, getScryfallSortParams, searchWithPagination]); // FIXED: Removed circular dependencies"""

    new_subscription_effect = """  // Subscribe to collection sort changes - MINIMAL STABLE DEPENDENCIES
  useEffect(() => {
    console.log('🔔 SUBSCRIPTION SETUP STARTED - useCards mounting');
    console.log('🔔 Available dependencies:', {
      hasSubscribe: typeof subscribe,
      hasUnsubscribe: typeof unsubscribe,
      subscribeFunction: subscribe?.toString().substring(0, 100) + '...'
    });
    
    try {
      const subscriptionId = subscribe((area: AreaType, sortState) => {
        console.log('📢 SORT SUBSCRIPTION EVENT RECEIVED:', { 
          area, 
          sortState,
          timestamp: new Date().toISOString(),
          eventId: Math.random().toString(36).substr(2, 9)
        });
        
        if (area === 'collection') {
          console.log('🔄 Collection sort changed:', sortState);
          
          // Access current state and trigger search using window.currentSearchFunction
          setState(currentState => {
            console.log('🔍 Current search metadata:', currentState.lastSearchMetadata);
            
            if (currentState.lastSearchMetadata) {
              console.log('✅ Triggering server-side sort logic:', {
                criteria: sortState.criteria,
                direction: sortState.direction
              });
              
              const metadata = currentState.lastSearchMetadata;
              const shouldUseServerSort = metadata.totalCards > 75;
              
              console.log('🤔 Sort decision analysis:', {
                criteria: sortState.criteria,
                direction: sortState.direction,
                totalCards: metadata.totalCards,
                loadedCards: metadata.loadedCards,
                threshold: 75,
                shouldUseServerSort,
                reason: shouldUseServerSort ? 'Large dataset - trigger server-side sort' : 'Small dataset - use client-side sort'
              });

              if (shouldUseServerSort) {
                console.log('🌐 TRIGGERING SERVER-SIDE SORT - new Scryfall search');
                
                // Use global reference to avoid dependency issues
                if ((window as any).triggerSearch) {
                  console.log('🔧 Using global search trigger');
                  (window as any).triggerSearch(metadata.query, metadata.filters);
                } else {
                  console.log('❌ Global search trigger not available');
                }
              } else {
                console.log('🏠 Using CLIENT-SIDE sorting - handled by UI components');
              }
            } else {
              console.log('❌ No search metadata - cannot trigger sort change');
            }
            
            return currentState; // No state change needed
          });
        } else {
          console.log('ℹ️ Sort change for non-collection area:', area);
        }
      });

      console.log('🔔 Sort subscription established with ID:', subscriptionId);
      console.log('🔔 SUBSCRIPTION SETUP COMPLETE');

      return () => {
        console.log('🔕 Unsubscribing from sort changes:', subscriptionId);
        unsubscribe(subscriptionId);
      };
    } catch (error) {
      console.error('❌ SUBSCRIPTION SETUP FAILED:', error);
      return () => {}; // Empty cleanup function
    }
  }, [subscribe, unsubscribe]); // MINIMAL DEPENDENCIES - only stable functions"""

    if old_subscription_effect in content:
        content = content.replace(old_subscription_effect, new_subscription_effect)
        print("✅ Fixed subscription useEffect to use minimal stable dependencies")
    else:
        print("❌ Could not find subscription useEffect to fix")
        return False
    
    # Add global search trigger function setup
    old_search_with_pagination = """  // Enhanced search with pagination support
  const searchWithPagination = useCallback(async (query: string, filters: SearchFilters = {}) => {"""

    new_search_with_pagination = """  // Enhanced search with pagination support
  const searchWithPagination = useCallback(async (query: string, filters: SearchFilters = {}) => {"""

    # Add global function exposure after searchWithPagination definition
    global_function_setup = """
  // Expose search function globally for subscription system
  useEffect(() => {
    (window as any).triggerSearch = searchWithPagination;
    console.log('🌐 Global search trigger function available');
    return () => {
      delete (window as any).triggerSearch;
    };
  }, [searchWithPagination]);"""

    # Find where to insert the global function setup (after searchWithPagination callback)
    search_callback_end = """  }, [clearError, setLoading, resetPagination, getScryfallSortParams]);"""
    
    if search_callback_end in content:
        content = content.replace(search_callback_end, search_callback_end + global_function_setup)
        print("✅ Added global search trigger function")
    else:
        print("❌ Could not find location to add global search trigger")
        return False
    
    # Write the updated content
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Successfully fixed subscription system with minimal dependencies in {filename}")
    return True

if __name__ == "__main__":
    success = fix_subscription_final("src/hooks/useCards.ts")
    sys.exit(0 if success else 1)