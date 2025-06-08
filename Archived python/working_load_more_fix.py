#!/usr/bin/env python3

import os
import re

def read_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"File not found: {filepath}")
        return None
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return None

def write_file(filepath, content):
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated: {filepath}")
        return True
    except Exception as e:
        print(f"Error writing {filepath}: {e}")
        return False

def fix_useSearch_hook():
    filepath = "src/hooks/useSearch.ts"
    content = read_file(filepath)
    
    if not content:
        return False
    
    # Add loadMoreCards method before the return statement
    load_more_method = '''  // Load more cards for progressive loading
  const loadMoreCards = useCallback(async (): Promise<ScryfallCard[]> => {
    console.log('🔄 useSearch.loadMoreCards called');
    
    const metadata = state.lastSearchMetadata;
    if (!metadata) {
      console.log('❌ No search metadata available for load more');
      throw new Error('No search metadata available');
    }

    try {
      console.log('📡 Loading more cards via API...');
      
      // Use the existing pagination state to load more
      const currentPaginationState = {
        totalCards: metadata.totalCards,
        loadedCards: metadata.loadedCards,
        hasMore: metadata.loadedCards < metadata.totalCards,
        isLoadingMore: false,
        currentPage: Math.floor(metadata.loadedCards / 75) + 1,
        nextUrl: null,
        query: metadata.query,
        filters: metadata.filters,
      };

      const { loadMoreResults } = await import('../services/scryfallApi');
      const newCards = await loadMoreResults(currentPaginationState);
      
      console.log('✅ Load more API successful:', {
        newCardsCount: newCards.length,
        previousTotal: state.cards.length
      });

      // Update local state with appended cards
      setState(prev => {
        const updatedCards = [...prev.cards, ...newCards];
        console.log('🔄 Updating useSearch cards state:', {
          previousCount: prev.cards.length,
          newCardsCount: newCards.length,
          finalCount: updatedCards.length
        });
        
        return {
          ...prev,
          cards: updatedCards,
          lastSearchMetadata: prev.lastSearchMetadata ? {
            ...prev.lastSearchMetadata,
            loadedCards: updatedCards.length
          } : null
        };
      });

      // Update pagination through callback
      onPaginationUpdate({
        loadedCards: state.cards.length + newCards.length,
        hasMore: (state.cards.length + newCards.length) < metadata.totalCards,
        isLoadingMore: false,
        currentPage: Math.floor((state.cards.length + newCards.length) / 75) + 1,
      });

      return newCards;
      
    } catch (error) {
      console.error('❌ Load more failed in useSearch:', error);
      throw error;
    }
  }, [state.lastSearchMetadata, state.cards.length, onPaginationUpdate]);

'''
    
    # Find return statement and add method before it
    return_index = content.rfind('  return {')
    if return_index != -1:
        content = content[:return_index] + load_more_method + content[return_index:]
    
    # Add to interface
    interface_pattern = r'export interface SearchActions \{([^}]+)\}'
    interface_match = re.search(interface_pattern, content, re.DOTALL)
    
    if interface_match:
        interface_content = interface_match.group(1)
        if 'loadMoreCards:' not in interface_content:
            new_interface_content = interface_content.rstrip() + '\n  loadMoreCards: () => Promise<ScryfallCard[]>;'
            new_interface = f'export interface SearchActions {{\n{new_interface_content}\n}}'
            content = content.replace(interface_match.group(0), new_interface)
    
    # Add to return statement
    return_pattern = r'return \{([^}]+)\};'
    return_match = re.search(return_pattern, content, re.DOTALL)
    
    if return_match:
        return_content = return_match.group(1)
        if 'loadMoreCards,' not in return_content:
            new_return_content = return_content.rstrip() + ',\n    loadMoreCards,'
            new_return = f'return {{\n{new_return_content}\n  }};'
            content = content.replace(return_match.group(0), new_return)
    
    return write_file(filepath, content)

def fix_useCards_coordinator():
    filepath = "src/hooks/useCards.ts"
    content = read_file(filepath)
    
    if not content:
        return False
    
    # Fix pagination initialization
    old_init = '''  // Pagination hook
  const {
    pagination,
    loadMoreResultsAction: originalLoadMore,
    resetPagination,
    setPaginationState,
    updatePagination,
  } = usePagination({
    cards: [], // Will be updated through coordination
    onCardsUpdate: () => {}, // Will be handled by coordination
    onErrorUpdate: () => {}, // Will be handled by coordination
  });'''
    
    new_init = '''  // Pagination hook with proper coordination
  const {
    pagination,
    resetPagination,
    setPaginationState,
    updatePagination,
  } = usePagination();'''
    
    content = content.replace(old_init, new_init)
    
    # Fix search hook destructuring
    old_search = '''  // Search hook with coordination callbacks
  const {
    cards,
    loading,
    error,
    searchQuery,
    totalCards,
    lastSearchMetadata,
    isResorting,
    searchForCards,
    searchWithAllFilters,
    enhancedSearch,
    loadPopularCards,
    loadRandomCard,
    clearCards: clearCardsSearch,
    handleCollectionSortChange,
  } = useSearch({'''
    
    new_search = '''  // Search hook with coordination callbacks
  const {
    cards,
    loading,
    error,
    searchQuery,
    totalCards,
    lastSearchMetadata,
    isResorting,
    searchForCards,
    searchWithAllFilters,
    enhancedSearch,
    loadPopularCards,
    loadRandomCard,
    clearCards: clearCardsSearch,
    handleCollectionSortChange,
    loadMoreCards: searchHookLoadMore,
  } = useSearch({'''
    
    content = content.replace(old_search, new_search)
    
    # Add coordinated load more function after search hook
    coordinated_func = '''
  // Coordinated Load More function
  const coordinatedLoadMore = useCallback(async () => {
    console.log('🎯 useCards coordinated Load More executing');
    
    if (!pagination.hasMore || pagination.isLoadingMore) {
      console.log('🚫 Cannot load more:', { 
        hasMore: pagination.hasMore,
        isLoadingMore: pagination.isLoadingMore
      });
      return;
    }

    console.log('🔄 Setting loading state...');
    updatePagination({ isLoadingMore: true });

    try {
      console.log('📡 Calling search hook loadMoreCards...');
      await searchHookLoadMore();
      console.log('✅ Coordinated Load More successful');
    } catch (error) {
      console.error('❌ Coordinated Load More failed:', error);
      updatePagination({ isLoadingMore: false });
    }
  }, [pagination.hasMore, pagination.isLoadingMore, updatePagination, searchHookLoadMore]);

'''
    
    # Find where to insert after search hook
    search_end = content.find('  });', content.find('addToSearchHistory,')) + 5
    if search_end > 4:
        content = content[:search_end] + coordinated_func + content[search_end:]
    
    # Fix return statement
    content = content.replace(
        'loadMoreResultsAction: originalLoadMore,',
        'loadMoreResultsAction: coordinatedLoadMore,'
    )
    
    return write_file(filepath, content)

def fix_usePagination_hook():
    filepath = "src/hooks/usePagination.ts"
    
    new_content = '''// src/hooks/usePagination.ts - Simplified state management for progressive loading
import { useState, useCallback } from 'react';
import { PaginatedSearchState } from '../types/card';

export interface PaginationState {
  pagination: {
    totalCards: number;
    loadedCards: number;
    hasMore: boolean;
    isLoadingMore: boolean;
    currentPage: number;
  };
}

export interface PaginationActions {
  resetPagination: () => void;
  setPaginationState: (state: PaginatedSearchState | null) => void;
  updatePagination: (update: Partial<PaginationState['pagination']>) => void;
}

export const usePagination = (): PaginationState & PaginationActions => {
  const [paginationState, setPaginationState] = useState<PaginatedSearchState | null>(null);
  
  const [pagination, setPagination] = useState({
    totalCards: 0,
    loadedCards: 0,
    hasMore: false,
    isLoadingMore: false,
    currentPage: 1,
  });

  const resetPagination = useCallback(() => {
    console.log('🔄 usePagination.resetPagination called');
    setPaginationState(null);
    setPagination({
      totalCards: 0,
      loadedCards: 0,
      hasMore: false,
      isLoadingMore: false,
      currentPage: 1,
    });
  }, []);

  const updatePagination = useCallback((update: Partial<typeof pagination>) => {
    console.log('🔄 usePagination.updatePagination called:', update);
    setPagination(prev => ({ ...prev, ...update }));
  }, []);

  const setPaginationStateCallback = useCallback((state: PaginatedSearchState | null) => {
    console.log('🔄 usePagination.setPaginationState called:', state ? 'with state' : 'null');
    setPaginationState(state);
  }, []);

  return {
    pagination,
    resetPagination,
    setPaginationState: setPaginationStateCallback,
    updatePagination,
  };
};
'''
    
    return write_file(filepath, new_content)

def main():
    print("🚀 Fixing Load More coordination between extracted hooks...")
    print()
    
    if not os.path.exists("src/hooks"):
        print("❌ Error: Not in project root directory.")
        return False
    
    success = True
    
    print("1️⃣ Adding loadMoreCards method to useSearch hook...")
    if fix_useSearch_hook():
        print("   ✅ useSearch hook updated successfully")
    else:
        print("   ❌ Failed to update useSearch hook")
        success = False
    
    print()
    
    print("2️⃣ Simplifying usePagination hook...")
    if fix_usePagination_hook():
        print("   ✅ usePagination hook updated successfully")
    else:
        print("   ❌ Failed to update usePagination hook")
        success = False
    
    print()
    
    print("3️⃣ Fixing useCards coordinator...")
    if fix_useCards_coordinator():
        print("   ✅ useCards coordinator updated successfully")
    else:
        print("   ❌ Failed to update useCards coordinator")
        success = False
    
    print()
    
    if success:
        print("🎉 All Load More coordination fixes applied successfully!")
        print()
        print("📋 Next steps:")
        print("   1. Run 'npm start' to verify compilation")
        print("   2. Test Load More button functionality")
        print("   3. Verify no regressions in other features")
    else:
        print("❌ Some fixes failed.")
    
    return success

if __name__ == "__main__":
    main()
