// src/hooks/useSelection.ts
import { useState, useCallback, useRef, useEffect } from 'react';
import { ScryfallCard } from '../types/card';

export interface SelectionState {
  selectedCards: Set<string>; // Set of card IDs
  lastSelectedId: string | null;
  selectionMode: 'single' | 'multiple';
  dragSelection: {
    active: boolean;
    startPoint: { x: number; y: number } | null;
    currentPoint: { x: number; y: number } | null;
  };
}

export interface SelectionActions {
  selectCard: (cardId: string, card: ScryfallCard, ctrlKey?: boolean) => void;
  deselectCard: (cardId: string) => void;
  toggleCard: (cardId: string, card: ScryfallCard) => void;
  selectAll: (cardIds: string[]) => void;
  clearSelection: () => void;
  isSelected: (cardId: string) => boolean;
  getSelectedCards: () => string[];
  getSelectedCount: () => number;
  startDragSelection: (point: { x: number; y: number }) => void;
  updateDragSelection: (point: { x: number; y: number }) => void;
  endDragSelection: (cardIds: string[]) => void;
}

const INITIAL_STATE: SelectionState = {
  selectedCards: new Set(),
  lastSelectedId: null,
  selectionMode: 'single',
  dragSelection: {
    active: false,
    startPoint: null,
    currentPoint: null,
  },
};

export const useSelection = () => {
  const [state, setState] = useState<SelectionState>(INITIAL_STATE);
  const selectedCardsRef = useRef<Map<string, ScryfallCard>>(new Map());

  // Clear selection when filters change (from external trigger)
  const clearOnFilterChange = useCallback(() => {
    setState(prev => ({
      ...prev,
      selectedCards: new Set(),
      lastSelectedId: null,
      selectionMode: 'single',
    }));
    selectedCardsRef.current.clear();
  }, []);

  // Select a single card or add to multi-selection
  const selectCard = useCallback((cardId: string, card: ScryfallCard, ctrlKey = false) => {
    setState(prev => {
      if (ctrlKey || prev.selectionMode === 'multiple') {
        // Multi-selection mode
        const newSelected = new Set(prev.selectedCards);
        
        if (newSelected.has(cardId)) {
          // Deselect if already selected
          newSelected.delete(cardId);
          selectedCardsRef.current.delete(cardId);
        } else {
          // Add to selection
          newSelected.add(cardId);
          selectedCardsRef.current.set(cardId, card);
        }

        return {
          ...prev,
          selectedCards: newSelected,
          lastSelectedId: cardId,
          selectionMode: newSelected.size > 1 ? 'multiple' : 'single',
        };
      } else {
        // Single selection mode
        selectedCardsRef.current.clear();
        selectedCardsRef.current.set(cardId, card);
        
        return {
          ...prev,
          selectedCards: new Set([cardId]),
          lastSelectedId: cardId,
          selectionMode: 'single',
        };
      }
    });
  }, []);

  // Deselect a specific card
  const deselectCard = useCallback((cardId: string) => {
    setState(prev => {
      const newSelected = new Set(prev.selectedCards);
      newSelected.delete(cardId);
      selectedCardsRef.current.delete(cardId);

      return {
        ...prev,
        selectedCards: newSelected,
        lastSelectedId: newSelected.size > 0 ? Array.from(newSelected)[0] : null,
        selectionMode: newSelected.size > 1 ? 'multiple' : 'single',
      };
    });
  }, []);

  // Toggle card selection
  const toggleCard = useCallback((cardId: string, card: ScryfallCard) => {
    setState(prev => {
      const newSelected = new Set(prev.selectedCards);
      
      if (newSelected.has(cardId)) {
        newSelected.delete(cardId);
        selectedCardsRef.current.delete(cardId);
      } else {
        newSelected.add(cardId);
        selectedCardsRef.current.set(cardId, card);
      }

      return {
        ...prev,
        selectedCards: newSelected,
        lastSelectedId: cardId,
        selectionMode: newSelected.size > 1 ? 'multiple' : 'single',
      };
    });
  }, []);

  // Select all provided cards
  const selectAll = useCallback((cardIds: string[]) => {
    setState(prev => ({
      ...prev,
      selectedCards: new Set(cardIds),
      lastSelectedId: cardIds.length > 0 ? cardIds[cardIds.length - 1] : null,
      selectionMode: cardIds.length > 1 ? 'multiple' : 'single',
    }));
    // Note: selectedCardsRef would need card objects to be fully populated
    // This is a simplified version - in real usage, you'd pass card objects too
  }, []);

  // Clear all selections
  const clearSelection = useCallback(() => {
    setState(prev => ({
      ...prev,
      selectedCards: new Set(),
      lastSelectedId: null,
      selectionMode: 'single',
    }));
    selectedCardsRef.current.clear();
  }, []);

  // Check if a card is selected
  const isSelected = useCallback((cardId: string) => {
    return state.selectedCards.has(cardId);
  }, [state.selectedCards]);

  // Get array of selected card IDs
  const getSelectedCards = useCallback(() => {
    return Array.from(state.selectedCards);
  }, [state.selectedCards]);

  // Get count of selected cards
  const getSelectedCount = useCallback(() => {
    return state.selectedCards.size;
  }, [state.selectedCards]);

  // Start drag selection rectangle
  const startDragSelection = useCallback((point: { x: number; y: number }) => {
    setState(prev => ({
      ...prev,
      dragSelection: {
        active: true,
        startPoint: point,
        currentPoint: point,
      },
    }));
  }, []);

  // Update drag selection rectangle
  const updateDragSelection = useCallback((point: { x: number; y: number }) => {
    setState(prev => ({
      ...prev,
      dragSelection: {
        ...prev.dragSelection,
        currentPoint: point,
      },
    }));
  }, []);

  // End drag selection and select cards within rectangle
  const endDragSelection = useCallback((cardIds: string[]) => {
    setState(prev => {
      const newSelected = new Set(cardIds);
      
      return {
        ...prev,
        selectedCards: newSelected,
        lastSelectedId: cardIds.length > 0 ? cardIds[cardIds.length - 1] : null,
        selectionMode: cardIds.length > 1 ? 'multiple' : 'single',
        dragSelection: {
          active: false,
          startPoint: null,
          currentPoint: null,
        },
      };
    });
  }, []);

  // Keyboard event handler for selection shortcuts
  useEffect(() => {
    const handleKeyboard = (event: KeyboardEvent) => {
      // Ctrl+A to select all (would need to be implemented by parent component)
      // Escape to clear selection
      if (event.key === 'Escape') {
        clearSelection();
      }
    };

    document.addEventListener('keydown', handleKeyboard);
    return () => document.removeEventListener('keydown', handleKeyboard);
  }, [clearSelection]);

  const actions: SelectionActions = {
    selectCard,
    deselectCard,
    toggleCard,
    selectAll,
    clearSelection,
    isSelected,
    getSelectedCards,
    getSelectedCount,
    startDragSelection,
    updateDragSelection,
    endDragSelection,
  };

  return {
    ...state,
    ...actions,
    clearOnFilterChange,
    // Access to the actual card objects (for context menus, etc.)
    getSelectedCardObjects: () => Array.from(selectedCardsRef.current.values()),
  };
};