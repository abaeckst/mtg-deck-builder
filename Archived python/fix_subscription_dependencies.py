#!/usr/bin/env python3

import os
import sys

def fix_subscription_dependencies(filename):
    """Fix circular dependency in useCards subscription useEffect"""
    
    if not os.path.exists(filename):
        print(f"Error: {filename} not found")
        return False
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix the subscription useEffect dependency array
    old_subscription_effect = """  // Subscribe to collection sort changes with comprehensive debugging
  useEffect(() => {
    console.log('🔔 SUBSCRIPTION SETUP STARTED - useCards mounting');
    console.log('🔔 Available dependencies:', {
      hasSubscribe: typeof subscribe,
      hasUnsubscribe: typeof unsubscribe,
      hasHandleCollectionSortChange: typeof handleCollectionSortChange,
      hasSearchMetadata: !!state.lastSearchMetadata,
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
          console.log('🔍 Current search metadata:', state.lastSearchMetadata);
          console.log('🔍 Available functions:', {
            hasHandleCollectionSortChange: typeof handleCollectionSortChange,
            hasMetadata: !!state.lastSearchMetadata
          });
          
          if (state.lastSearchMetadata) {
            console.log('✅ Triggering handleCollectionSortChange with:', {
              criteria: sortState.criteria,
              direction: sortState.direction
            });
            handleCollectionSortChange(sortState.criteria, sortState.direction);
          } else {
            console.log('❌ No search metadata - cannot trigger sort change');
          }
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
  }, [subscribe, unsubscribe, state.lastSearchMetadata, handleCollectionSortChange]);"""

    new_subscription_effect = """  // Subscribe to collection sort changes - FIXED DEPENDENCIES
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

    if old_subscription_effect in content:
        content = content.replace(old_subscription_effect, new_subscription_effect)
        print("✅ Fixed subscription useEffect dependencies")
    else:
        print("❌ Could not find subscription useEffect to fix")
        return False
    
    # Write the updated content
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Successfully fixed subscription dependencies in {filename}")
    return True

if __name__ == "__main__":
    success = fix_subscription_dependencies("src/hooks/useCards.ts")
    sys.exit(0 if success else 1)