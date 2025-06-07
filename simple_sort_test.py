#!/usr/bin/env python3

import os
import sys

def create_simple_sort_test():
    """Create a simple test to manually verify sorting is working"""
    
    filename = "src/components/MTGOLayout.tsx"
    
    if not os.path.exists(filename):
        print(f"Error: {filename} not found")
        return False
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Add a simple test function
    test_function = """  // SIMPLE SORT TEST FUNCTION
  useEffect(() => {
    const simpleSortTest = () => {
      console.log('🧪 ===== SIMPLE SORT TEST =====');
      console.log('Current cards array:', cards.map(c => c.name).slice(0, 10));
      console.log('Current sortedCollectionCards array:', sortedCollectionCards.map(c => c.name).slice(0, 10));
      console.log('Sort state:', collectionSort);
      console.log('Are arrays different?', cards !== sortedCollectionCards);
      console.log('Are first cards different?', cards[0]?.name !== sortedCollectionCards[0]?.name);
      console.log('Cards length:', cards.length, 'Sorted length:', sortedCollectionCards.length);
      console.log('Change tracker:', cardsChangeTracker);
      console.log('Sort change ID:', sortChangeId);
      console.log('🧪 ===== END SIMPLE SORT TEST =====');
    };
    
    (window as any).simpleSortTest = simpleSortTest;
    console.log('🧪 Simple sort test available: window.simpleSortTest()');
    
    return () => {
      delete (window as any).simpleSortTest;
    };
  }, [cards, sortedCollectionCards, collectionSort, cardsChangeTracker, sortChangeId]);

"""

    # Insert the test function
    insert_point = "  // Global debug function for manual testing"
    if insert_point in content:
        content = content.replace(insert_point, test_function + insert_point)
        print("✅ Added simple sort test function")
    else:
        # Try alternate insertion point
        insert_point = "  // Clear both deck and sideboard functionality"
        if insert_point in content:
            content = content.replace(insert_point, test_function + insert_point)
            print("✅ Added simple sort test function (alternate insertion)")
        else:
            print("❌ Could not find insertion point for test function")
            return False

    # Write the updated content
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Successfully added simple sort test to {filename}")
    return True

if __name__ == "__main__":
    success = create_simple_sort_test()
    sys.exit(0 if success else 1)