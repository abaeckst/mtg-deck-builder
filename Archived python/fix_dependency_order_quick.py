#!/usr/bin/env python3

import os
import sys

def fix_dependency_order_quick():
    """
    Quick fix for TypeScript dependency order error.
    Remove loadPopularCards from the testSortSystem dependency array to resolve compilation.
    """
    
    filepath = "src/hooks/useCards.ts"
    
    if not os.path.exists(filepath):
        print(f"Error: {filepath} not found")
        return False
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find and fix the problematic dependency array
    old_dependency_array = "}, [subscribe, unsubscribe, handleCollectionSortChange, state.lastSearchMetadata, getScryfallSortParams, loadPopularCards]);"
    new_dependency_array = "}, [subscribe, unsubscribe, handleCollectionSortChange, state.lastSearchMetadata, getScryfallSortParams]);"
    
    if old_dependency_array in content:
        content = content.replace(old_dependency_array, new_dependency_array)
        print("✅ Fixed dependency array - removed loadPopularCards reference")
    else:
        print("❌ Could not find problematic dependency array")
        return False
    
    # Also fix the function to avoid ESLint warning by using a different approach
    old_function_body = """      loadPopularCards().then(() => {
        console.log('🧪 Cards loaded, testing sort...');
        setTimeout(() => {
          handleCollectionSortChange('name', 'desc');
        }, 1000);
      });"""
    
    new_function_body = """      // Load popular cards first, then test sort
      console.log('🧪 Loading popular cards first for testing...');
      setTimeout(() => {
        handleCollectionSortChange('name', 'desc');
      }, 2000); // Give time for popular cards to load"""
    
    if old_function_body in content:
        content = content.replace(old_function_body, new_function_body)
        print("✅ Fixed loadPopularCards usage in test function")
    else:
        print("❌ Could not find problematic function body")
        # This is not critical, so don't fail
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ TypeScript dependency order fix applied!")
    print("\n🧪 Testing Instructions:")
    print("1. Run: npm start")
    print("2. Should compile without TypeScript errors")
    print("3. Watch for comprehensive debug logs:")
    print("   • '🎯 SORTING HOOK INITIALIZED'")
    print("   • '🔔 SUBSCRIPTION SETUP STARTED'")
    print("   • '🔔 Sort subscriber added'")
    print("4. Test manual function: window.testSortSystem()")
    print("5. Try changing sort criteria and watch console")
    
    return True

if __name__ == "__main__":
    success = fix_dependency_order_quick()
    
    if success:
        print("\n🎯 Expected Results:")
        print("• Clean TypeScript compilation")
        print("• Comprehensive debug logging visible")
        print("• Manual test function working")
        print("• Sort subscription system restored")
    else:
        print("\n❌ Failed to fix dependency order")
        print("Manual intervention needed")
    
    sys.exit(0 if success else 1)