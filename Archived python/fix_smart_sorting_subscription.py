#!/usr/bin/env python3

import os
import sys

def fix_smart_sorting_subscription():
    """
    Targeted fix for smart sorting subscription system.
    The issue is that sort change events aren't being triggered properly.
    """
    
    filepath = "src/hooks/useCards.ts"
    
    if not os.path.exists(filepath):
        print(f"Error: {filepath} not found")
        return False
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find and fix the subscription useEffect dependency array
    # The issue might be that handleCollectionSortChange isn't being called when sort state changes
    
    # First, let's ensure the subscription debug is comprehensive
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

    new_subscription_effect = """  // Subscribe to collection sort changes with enhanced debugging
  useEffect(() => {
    console.log('🔔 Setting up sort subscription for collection area');
    console.log('🔔 Subscription dependencies:', {
      hasSubscribe: typeof subscribe,
      hasUnsubscribe: typeof unsubscribe,
      hasHandleCollectionSortChange: typeof handleCollectionSortChange,
      hasSearchMetadata: !!state.lastSearchMetadata
    });
    
    const subscriptionId = subscribe((area: AreaType, sortState) => {
      console.log('📢 SORT SUBSCRIPTION EVENT RECEIVED:', { 
        area, 
        sortState,
        timestamp: new Date().toISOString() 
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

    return () => {
      console.log('🔕 Unsubscribing from sort changes:', subscriptionId);
      unsubscribe(subscriptionId);
    };
  }, [subscribe, unsubscribe, state.lastSearchMetadata, handleCollectionSortChange]);"""

    if old_subscription_effect in content:
        content = content.replace(old_subscription_effect, new_subscription_effect)
        print("✅ Enhanced subscription debugging")
    else:
        print("❌ Could not find subscription useEffect pattern")
        return False
    
    # Also add a debugging function to manually test the subscription
    debug_function = """
  // Debug function to test sort subscription manually
  const testSortSubscription = useCallback(() => {
    console.log('🧪 MANUAL SORT TEST TRIGGERED');
    console.log('🧪 Testing subscription system:', {
      hasSubscribe: typeof subscribe,
      hasUnsubscribe: typeof unsubscribe,
      hasHandleCollectionSortChange: typeof handleCollectionSortChange,
      currentMetadata: state.lastSearchMetadata
    });
    
    // Manually trigger a sort change to test
    if (state.lastSearchMetadata) {
      console.log('🧪 Manually triggering sort change...');
      handleCollectionSortChange('name', 'desc');
    } else {
      console.log('🧪 No metadata available for manual test');
    }
  }, [subscribe, unsubscribe, handleCollectionSortChange, state.lastSearchMetadata]);

  // Expose test function globally for debugging
  useEffect(() => {
    (window as any).testSortSubscription = testSortSubscription;
    console.log('🧪 Test function available: window.testSortSubscription()');
  }, [testSortSubscription]);
"""

    # Add the debug function before the return statement
    return_statement_start = content.find("  return {")
    if return_statement_start !== -1:
        content = content[:return_statement_start] + debug_function + content[return_statement_start:]
        print("✅ Added debug test function")
    else:
        print("❌ Could not find return statement to add debug function")
        return False
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Smart sorting subscription fix applied!")
    print("\n🧪 Testing Instructions:")
    print("1. Run: npm start")
    print("2. Wait for app to load completely")
    print("3. Look for: '🔔 Setting up sort subscription for collection area'")
    print("4. Try changing sort criteria and watch for: '📢 SORT SUBSCRIPTION EVENT RECEIVED'")
    print("5. If still not working, open browser console and run: window.testSortSubscription()")
    print("\n🔍 Debug Analysis:")
    print("• Enhanced logging will show subscription setup details")
    print("• Manual test function allows direct subscription testing")
    print("• Should reveal why sort events aren't firing")
    
    return True

if __name__ == "__main__":
    success = fix_smart_sorting_subscription()
    
    if success:
        print("\n🎯 Expected Results:")
        print("• More detailed subscription debug logs")
        print("• Manual test function for debugging")
        print("• Clear indication of where subscription fails")
        print("• Should help identify root cause of missing sort events")
    else:
        print("\n❌ Failed to apply subscription fix")
        print("Manual investigation needed to identify subscription issue")
    
    sys.exit(0 if success else 1)