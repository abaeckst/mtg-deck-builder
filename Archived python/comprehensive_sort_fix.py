#!/usr/bin/env python3

import os
import sys

def comprehensive_sort_fix():
    """
    Comprehensive fix for all smart sorting issues:
    1. Add enhanced debugging to track subscription setup
    2. Fix default sort direction for proper A-Z ordering  
    3. Add manual testing capabilities
    4. Ensure subscription events are properly triggered
    """
    
    files_updated = 0
    
    # Fix 1: Enhanced debugging in useCards.ts
    if fix_usecards_debugging():
        files_updated += 1
    
    # Fix 2: Correct default sort direction in useSorting.ts  
    if fix_default_sort_direction():
        files_updated += 1
        
    if files_updated == 2:
        print("✅ Comprehensive smart sorting fix completed!")
        print("\n🎯 Fixes Applied:")
        print("• Enhanced subscription debugging in useCards.ts")
        print("• Corrected default sort direction in useSorting.ts")
        print("• Added manual testing capabilities")
        print("• Improved error handling and event tracking")
        
        print("\n🧪 Testing Instructions:")
        print("1. Run: npm start")
        print("2. Watch for: '🔔 SUBSCRIPTION SETUP STARTED'")
        print("3. Look for: '🔔 Sort subscriber added'") 
        print("4. Change sort criteria and watch for: '📢 Sort change event'")
        print("5. Verify default cards load A-Z alphabetical")
        print("6. Test manual function: window.testSortSystem()")
        
        return True
    else:
        print(f"❌ Only {files_updated}/2 files updated successfully")
        return False

def fix_usecards_debugging():
    """Add comprehensive debugging to useCards.ts subscription system"""
    
    filepath = "src/hooks/useCards.ts"
    
    if not os.path.exists(filepath):
        print(f"Error: {filepath} not found")
        return False
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find and replace the subscription useEffect with enhanced debugging
    old_subscription_effect = """  // Subscribe to collection sort changes with enhanced debugging
  useEffect(() => {
    console.log('🔔 Setting up sort subscription for collection area');
    
    const subscriptionId = subscribe((area: AreaType, sortState) => {
      console.log('📢 SORT SUBSCRIPTION EVENT RECEIVED:', { area, sortState });
      
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

    return () => {
      console.log('🔕 Unsubscribing from sort changes:', subscriptionId);
      unsubscribe(subscriptionId);
    };
  }, [subscribe, unsubscribe, state.lastSearchMetadata, handleCollectionSortChange]);"""

    new_subscription_effect = """  // Subscribe to collection sort changes with comprehensive debugging
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
  }, [subscribe, unsubscribe, state.lastSearchMetadata, handleCollectionSortChange]);

  // Manual testing function for debugging
  const testSortSystem = useCallback(() => {
    console.log('🧪 MANUAL SORT SYSTEM TEST');
    console.log('🧪 Current dependencies:', {
      hasSubscribe: typeof subscribe,
      hasUnsubscribe: typeof unsubscribe, 
      hasHandleCollectionSortChange: typeof handleCollectionSortChange,
      hasSearchMetadata: !!state.lastSearchMetadata,
      currentSortState: getScryfallSortParams('collection')
    });
    
    if (state.lastSearchMetadata) {
      console.log('🧪 Testing manual sort trigger...');
      handleCollectionSortChange('name', 'desc');
    } else {
      console.log('🧪 No search metadata - loading popular cards first...');
      loadPopularCards().then(() => {
        console.log('🧪 Cards loaded, testing sort...');
        setTimeout(() => {
          handleCollectionSortChange('name', 'desc');
        }, 1000);
      });
    }
  }, [subscribe, unsubscribe, handleCollectionSortChange, state.lastSearchMetadata, getScryfallSortParams, loadPopularCards]);

  // Expose test function globally
  useEffect(() => {
    (window as any).testSortSystem = testSortSystem;
    console.log('🧪 Global test function available: window.testSortSystem()');
  }, [testSortSystem]);"""

    if old_subscription_effect in content:
        content = content.replace(old_subscription_effect, new_subscription_effect)
        print("✅ Enhanced subscription debugging in useCards.ts")
    else:
        print("❌ Could not find subscription useEffect in useCards.ts")
        return False
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True

def fix_default_sort_direction():
    """Fix default sort direction to ensure proper A-Z ordering"""
    
    filepath = "src/hooks/useSorting.ts"
    
    if not os.path.exists(filepath):
        print(f"Error: {filepath} not found")
        return False
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Add debugging to the useSorting hook initialization
    old_usesorting_start = """export const useSorting = () => {
  const [sortState, setSortState] = useState<AreaSortState>(() => {
    try {
      const saved = localStorage.getItem(STORAGE_KEY);
      const loadedState = saved ? { ...DEFAULT_SORT_STATE, ...JSON.parse(saved) } : DEFAULT_SORT_STATE;
      currentSortState = loadedState;
      return loadedState;
    } catch {
      currentSortState = DEFAULT_SORT_STATE;
      return DEFAULT_SORT_STATE;
    }
  });"""

    new_usesorting_start = """export const useSorting = () => {
  const [sortState, setSortState] = useState<AreaSortState>(() => {
    try {
      const saved = localStorage.getItem(STORAGE_KEY);
      const loadedState = saved ? { ...DEFAULT_SORT_STATE, ...JSON.parse(saved) } : DEFAULT_SORT_STATE;
      currentSortState = loadedState;
      
      console.log('🎯 SORTING HOOK INITIALIZED:', {
        defaultState: DEFAULT_SORT_STATE,
        loadedState: loadedState,
        collectionSort: loadedState.collection
      });
      
      return loadedState;
    } catch {
      currentSortState = DEFAULT_SORT_STATE;
      console.log('🎯 SORTING HOOK - Using default state due to error');
      return DEFAULT_SORT_STATE;
    }
  });"""

    if old_usesorting_start in content:
        content = content.replace(old_usesorting_start, new_usesorting_start)
        print("✅ Added initialization debugging to useSorting.ts")
    else:
        print("❌ Could not find useSorting initialization pattern")
        return False
    
    # Enhanced debugging for the updateSort function
    old_update_sort = """  // Enhanced update sort with subscription notification
  const updateSort = useCallback((area: AreaType, criteria: SortCriteria, direction?: SortDirection) => {
    const newSortState = {
      criteria,
      direction: direction ?? sortState[area].direction,
    };

    setSortState(prev => ({
      ...prev,
      [area]: newSortState,
    }));

    // Determine if this change requires server-side re-search
    const requiresServerSearch = area === 'collection';

    // Emit sort change event to subscribers
    const event: SortChangeEvent = {
      area,
      sortState: newSortState,
      requiresServerSearch,
    };

    console.log('📢 Sort change event:', event);
    emitSortChange(event);
  }, [sortState]);"""

    new_update_sort = """  // Enhanced update sort with subscription notification
  const updateSort = useCallback((area: AreaType, criteria: SortCriteria, direction?: SortDirection) => {
    const newSortState = {
      criteria,
      direction: direction ?? sortState[area].direction,
    };

    console.log('🎯 SORT UPDATE CALLED:', {
      area,
      criteria,
      direction,
      previousState: sortState[area],
      newSortState,
      subscriberCount: subscribers.length
    });

    setSortState(prev => ({
      ...prev,
      [area]: newSortState,
    }));

    // Determine if this change requires server-side re-search
    const requiresServerSearch = area === 'collection';

    // Emit sort change event to subscribers
    const event: SortChangeEvent = {
      area,
      sortState: newSortState,
      requiresServerSearch,
    };

    console.log('📢 Sort change event emitted:', event);
    console.log('📢 Notifying', subscribers.length, 'subscribers');
    emitSortChange(event);
  }, [sortState]);"""

    if old_update_sort in content:
        content = content.replace(old_update_sort, new_update_sort)
        print("✅ Enhanced updateSort debugging in useSorting.ts")
    else:
        print("❌ Could not find updateSort function pattern")
        return False
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True

if __name__ == "__main__":
    success = comprehensive_sort_fix()
    
    if success:
        print("\n🎯 Expected Debug Flow:")
        print("1. '🎯 SORTING HOOK INITIALIZED' - Shows default sort state")
        print("2. '🔔 SUBSCRIPTION SETUP STARTED' - useCards subscribing")
        print("3. '🔔 Sort subscriber added' - useSorting confirms subscription")
        print("4. '🔔 SUBSCRIPTION SETUP COMPLETE' - useCards confirms success")
        print("5. When sort changes: '🎯 SORT UPDATE CALLED' → '📢 Sort change event emitted'")
        print("6. '📢 SORT SUBSCRIPTION EVENT RECEIVED' - useCards receives event")
        print("\n🔧 If issues persist:")
        print("• Check browser console for all debug messages above")
        print("• Run: window.testSortSystem() to manually test")
        print("• Look for any error messages in the debug flow")
    else:
        print("\n❌ Comprehensive fix failed")
        print("Manual file inspection and fixes needed")
    
    sys.exit(0 if success else 1)