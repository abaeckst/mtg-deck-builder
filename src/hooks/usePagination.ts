// src/hooks/usePagination.ts - Simplified state management for progressive loading
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
  const [paginationState, setPaginationState] = useState<PaginatedSearchState | null>(null); // eslint-disable-line @typescript-eslint/no-unused-vars
  
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
