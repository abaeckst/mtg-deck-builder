#!/usr/bin/env python3

import os
import sys

def fix_phase4b_regression():
    """Fix the subscription system broken during Phase 4B filter implementation"""
    
    useCards_path = "src/hooks/useCards.ts"
    
    if not os.path.exists(useCards_path):
        print(f"Error: {useCards_path} not found")
        return False

    with open(useCards_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # The most likely issue: Phase 4B filter state changes affecting component lifecycle
    # Let's check if the subscription useEffect is getting the enhanced filter dependencies
    
    # Find the current subscription useEffect
    current_subscription = '''  // Subscribe to collection sort changes - MINIMAL STABLE DEPENDENCIES
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
  }, [subscribe, unsubscribe]); // MINIMAL DEPENDENCIES - only stable functions'''

    if current_subscription not in content:
        print("❌ Could not find current subscription useEffect - may have different format")
        print("Let me try alternative approach...")
        
        # Alternative: Look for the subscription setup pattern
        subscription_pattern = "useEffect(() => {"
        subscription_start = content.find("// Subscribe to collection sort changes")
        
        if subscription_start == -1:
            print("❌ Could not find subscription setup at all")
            return False
        
        # Find the full useEffect
        useEffect_start = content.find("useEffect(() => {", subscription_start)
        if useEffect_start == -1:
            print("❌ Could not find subscription useEffect")
            return False
        
        # Find the end of this useEffect (look for closing bracket and dependency array)
        brace_count = 0
        pos = useEffect_start + len("useEffect(() => {")
        in_useEffect = True
        
        while pos < len(content) and in_useEffect:
            char = content[pos]
            if char == '{':
                brace_count += 1
            elif char == '}':
                if brace_count == 0:
                    # Look for the dependency array after this
                    remaining = content[pos:]
                    dep_array_match = remaining.find("}, [")
                    if dep_array_match != -1:
                        # Find the closing bracket of dependency array
                        dep_end = remaining.find(");", dep_array_match)
                        if dep_end != -1:
                            useEffect_end = pos + dep_end + 2
                            break
                else:
                    brace_count -= 1
            pos += 1
        else:
            print("❌ Could not find end of subscription useEffect")
            return False
        
        # Extract the current useEffect
        current_useEffect = content[subscription_start:useEffect_end]
        print("✅ Found subscription useEffect, analyzing...")
        
        # The fix: Ensure the subscription system runs immediately after component mount
        # The issue is likely that Phase 4B state changes are causing re-renders that prevent proper subscription
        fixed_useEffect = '''  // Subscribe to collection sort changes - FIXED: Immediate setup after mount
  useEffect(() => {
    console.log('🔔 SUBSCRIPTION SETUP STARTED - useCards mounting');
    console.log('🔔 Component mount state:', {
      hasSubscribe: typeof subscribe === 'function',
      hasUnsubscribe: typeof unsubscribe === 'function',
      componentMountTime: Date.now()
    });
    
    // Immediate subscription setup to avoid Phase 4B filter state interference
    if (typeof subscribe !== 'function') {
      console.error('❌ Subscribe function not available');
      return () => {};
    }
    
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
          
          // Get current search metadata directly from window global
          const triggerSearchFn = (window as any).triggerSearch;
          if (!triggerSearchFn) {
            console.log('❌ Global search trigger not available yet');
            return;
          }
          
          // Access last search metadata from the global reference
          setState(currentState => {
            const metadata = currentState.lastSearchMetadata;
            console.log('🔍 Current search metadata:', metadata);
            
            if (metadata && metadata.totalCards > 75) {
              console.log('🌐 TRIGGERING SERVER-SIDE SORT for large dataset');
              console.log('🔧 Sort parameters:', { criteria: sortState.criteria, direction: sortState.direction });
              
              // Trigger new search with current sort state
              setTimeout(() => {
                triggerSearchFn(metadata.query, metadata.filters);
              }, 10);
            } else {
              console.log('🏠 Using CLIENT-SIDE sorting');
            }
            
            return currentState; // No state change needed
          });
        }
      });

      console.log('✅ Sort subscription established with ID:', subscriptionId);
      console.log('✅ SUBSCRIPTION SETUP COMPLETE');

      return () => {
        console.log('🔕 Unsubscribing from sort changes:', subscriptionId);
        unsubscribe(subscriptionId);
      };
    } catch (error) {
      console.error('❌ SUBSCRIPTION SETUP FAILED:', error);
      return () => {};
    }
  }, []); // EMPTY DEPS - run once on mount, avoid Phase 4B state interference'''

        # Replace the subscription useEffect
        updated_content = content[:subscription_start] + fixed_useEffect + content[useEffect_end:]
        
    else:
        # Replace with the regression fix
        fixed_useEffect = '''  // REGRESSION FIX: Restore working subscription system
  useEffect(() => {
    console.log('🔔 SUBSCRIPTION SETUP - Post Phase 4B Fix');
    
    if (typeof subscribe !== 'function') {
      console.error('❌ Subscribe function not available');
      return () => {};
    }
    
    try {
      const subscriptionId = subscribe((area: AreaType, sortState) => {
        console.log('📢 SORT EVENT:', { area, sortState });
        
        if (area === 'collection') {
          // Direct approach - use the global search function immediately
          const searchFn = (window as any).triggerSearch;
          if (searchFn) {
            setState(currentState => {
              const metadata = currentState.lastSearchMetadata;
              if (metadata && metadata.totalCards > 75) {
                console.log('🌐 SERVER-SIDE SORT:', sortState);
                setTimeout(() => searchFn(metadata.query, metadata.filters), 10);
              }
              return currentState;
            });
          }
        }
      });

      console.log('✅ Subscription restored:', subscriptionId);
      return () => unsubscribe(subscriptionId);
    } catch (error) {
      console.error('❌ Subscription failed:', error);
      return () => {};
    }
  }, []); // EMPTY DEPS - avoid Phase 4B filter state conflicts'''

        updated_content = content.replace(current_subscription, fixed_useEffect)
    
    if updated_content == content:
        print("❌ No changes made - pattern not found")
        return False

    # Write the updated file
    with open(useCards_path, 'w', encoding='utf-8') as f:
        f.write(updated_content)

    print("✅ Applied regression fix for Phase 4B subscription system")
    print("✅ Simplified subscription setup to avoid filter state conflicts")
    print("✅ Using empty dependency array to run once on mount")
    print("✅ Direct global function approach to avoid state closure issues")
    print("")
    print("🧪 Test the fix:")
    print("1. npm start")
    print("2. Look for '🔔 SUBSCRIPTION SETUP - Post Phase 4B Fix'")
    print("3. Load >75 cards and test sort changes")
    print("4. Should see '📢 SORT EVENT' and '🌐 SERVER-SIDE SORT'")
    
    return True

if __name__ == "__main__":
    success = fix_phase4b_regression()
    sys.exit(0 if success else 1)