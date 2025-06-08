#!/usr/bin/env python3

import os
import sys

def fix_typescript_errors():
    """Fix TypeScript compilation errors from the nuclear React fix"""
    
    # Fix 1: Add sortChangeId to the UseCardsState interface
    filename1 = "src/hooks/useCards.ts"
    
    if not os.path.exists(filename1):
        print(f"Error: {filename1} not found")
        return False
    
    with open(filename1, 'r', encoding='utf-8') as f:
        content1 = f.read()
    
    # Add sortChangeId to the interface
    old_interface = """export interface UseCardsState {
  cards: ScryfallCard[];
  loading: boolean;
  error: string | null;
  hasMore: boolean;
  selectedCards: Set<string>;
  searchQuery: string;
  totalCards: number;
  
  // Enhanced search state
  searchSuggestions: string[];
  showSuggestions: boolean;
  recentSearches: string[];

  // Progressive loading pagination state
  pagination: {
    totalCards: number;
    loadedCards: number;
    hasMore: boolean;
    isLoadingMore: boolean;
    currentPage: number;
  };

  // Sort integration state
  lastSearchMetadata: {
    query: string;
    filters: any;
    totalCards: number;
    loadedCards: number;
  } | null;"""

    new_interface = """export interface UseCardsState {
  cards: ScryfallCard[];
  loading: boolean;
  error: string | null;
  hasMore: boolean;
  selectedCards: Set<string>;
  searchQuery: string;
  totalCards: number;
  
  // Enhanced search state
  searchSuggestions: string[];
  showSuggestions: boolean;
  recentSearches: string[];

  // Progressive loading pagination state
  pagination: {
    totalCards: number;
    loadedCards: number;
    hasMore: boolean;
    isLoadingMore: boolean;
    currentPage: number;
  };

  // Sort integration state
  lastSearchMetadata: {
    query: string;
    filters: any;
    totalCards: number;
    loadedCards: number;
  } | null;
  
  // Force React updates on sort changes
  sortChangeId: number;"""

    if old_interface in content1:
        content1 = content1.replace(old_interface, new_interface)
        print("✅ Added sortChangeId to UseCardsState interface")
    else:
        print("❌ Could not find UseCardsState interface")
        return False

    # Write the updated useCards.ts
    with open(filename1, 'w', encoding='utf-8') as f:
        f.write(content1)
    
    # Fix 2: Fix variable declaration order in MTGOLayout.tsx
    filename2 = "src/components/MTGOLayout.tsx"
    
    if not os.path.exists(filename2):
        print(f"Error: {filename2} not found")
        return False
    
    with open(filename2, 'r', encoding='utf-8') as f:
        content2 = f.read()
    
    # Move the debug effects to after sortedCollectionCards is declared
    # First, remove the misplaced debug effects
    debug_effects_to_remove = """  // Debug effect to track when sortedCollectionCards changes
  useEffect(() => {
    if (sortedCollectionCards.length > 0) {
      console.log('🎯 SORTED COLLECTION CARDS CHANGED:', {
        sortedLength: sortedCollectionCards.length,
        sortedFirst: sortedCollectionCards[0]?.name || 'None',
        sortedLast: sortedCollectionCards[sortedCollectionCards.length - 1]?.name || 'None',
        changeTracker: cardsChangeTracker,
        timestamp: Date.now()
      });
    }
  }, [sortedCollectionCards, cardsChangeTracker]);

  // SIMPLE SORT TEST FUNCTION
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

  // Global debug function for manual testing
  useEffect(() => {
    const debugRender = () => {
      console.log('🧪 MANUAL RENDER DEBUG:', {
        cardsLength: cards.length,
        sortedCardsLength: sortedCollectionCards.length,
        firstCard: cards[0]?.name || 'None',
        sortedFirstCard: sortedCollectionCards[0]?.name || 'None',
        changeTracker: cardsChangeTracker,
        viewMode: layout.viewModes.collection
      });
      
      // Force a manual re-render by updating a dummy state
      setSearchText(prev => prev === '' ? ' ' : prev === ' ' ? '' : prev);
    };
    
    (window as any).debugRender = debugRender;
    console.log('🧪 Global debug function available: window.debugRender()');
    
    return () => {
      delete (window as any).debugRender;
    };
  }, [cards, sortedCollectionCards, cardsChangeTracker, layout.viewModes.collection]);

"""

    if debug_effects_to_remove in content2:
        content2 = content2.replace(debug_effects_to_remove, "")
        print("✅ Removed misplaced debug effects")
    else:
        print("❌ Could not find debug effects to remove")

    # Find where sortedMainDeck is declared and add our effects after that
    insertion_point = """  const sortedSideboard = useMemo((): DeckCardInstance[] => {
    return layout.viewModes.sideboard === 'pile' ? sideboard : sortCards(sideboard as any, sideboardSort.criteria, sideboardSort.direction) as DeckCardInstance[];
  }, [sideboard, sideboardSort.criteria, sideboardSort.direction, layout.viewModes.sideboard, sortCards]);"""

    debug_effects_correct_place = """  const sortedSideboard = useMemo((): DeckCardInstance[] => {
    return layout.viewModes.sideboard === 'pile' ? sideboard : sortCards(sideboard as any, sideboardSort.criteria, sideboardSort.direction) as DeckCardInstance[];
  }, [sideboard, sideboardSort.criteria, sideboardSort.direction, layout.viewModes.sideboard, sortCards]);

  // Debug effect to track when sortedCollectionCards changes
  useEffect(() => {
    if (sortedCollectionCards.length > 0) {
      console.log('🎯 SORTED COLLECTION CARDS CHANGED:', {
        sortedLength: sortedCollectionCards.length,
        sortedFirst: sortedCollectionCards[0]?.name || 'None',
        sortedLast: sortedCollectionCards[sortedCollectionCards.length - 1]?.name || 'None',
        changeTracker: cardsChangeTracker,
        timestamp: Date.now()
      });
    }
  }, [sortedCollectionCards, cardsChangeTracker]);

  // SIMPLE SORT TEST FUNCTION
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

  // Global debug function for manual testing
  useEffect(() => {
    const debugRender = () => {
      console.log('🧪 MANUAL RENDER DEBUG:', {
        cardsLength: cards.length,
        sortedCardsLength: sortedCollectionCards.length,
        firstCard: cards[0]?.name || 'None',
        sortedFirstCard: sortedCollectionCards[0]?.name || 'None',
        changeTracker: cardsChangeTracker,
        viewMode: layout.viewModes.collection
      });
      
      // Force a manual re-render by updating a dummy state
      setSearchText(prev => prev === '' ? ' ' : prev === ' ' ? '' : prev);
    };
    
    (window as any).debugRender = debugRender;
    console.log('🧪 Global debug function available: window.debugRender()');
    
    return () => {
      delete (window as any).debugRender;
    };
  }, [cards, sortedCollectionCards, cardsChangeTracker, layout.viewModes.collection]);"""

    if insertion_point in content2:
        content2 = content2.replace(insertion_point, debug_effects_correct_place)
        print("✅ Moved debug effects to correct location")
    else:
        print("❌ Could not find insertion point for debug effects")
        return False

    # Write the updated MTGOLayout.tsx
    with open(filename2, 'w', encoding='utf-8') as f:
        f.write(content2)
    
    print(f"✅ Successfully fixed TypeScript errors in {filename1} and {filename2}")
    return True

if __name__ == "__main__":
    success = fix_typescript_errors()
    sys.exit(0 if success else 1)