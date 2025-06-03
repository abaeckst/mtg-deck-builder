// src/hooks/useSelection.ts
import { useState, useCallback, useRef, useEffect } from 'react';
import { ScryfallCard, DeckCardInstance } from '../types/card';

export interface SelectionState {
  selectedInstances: Set<string>;     // Instance IDs for deck/sideboard cards
  selectedCards: Set<string>;         // Card IDs for collection cards
  lastSelectedType: 'card' | 'instance';
  lastSelectedId: string | null;
  selectionMode: 'single' | 'multiple';
  dragSelection: {
    active: boolean;
    startPoint: { x: number; y: number } | null;
    currentPoint: { x: number; y: number } | null;
  };
}

export interface SelectionActions {
  // Instance-based selection (for deck/sideboard)
  selectInstance: (instanceId: string, instance: DeckCardInstance, ctrlKey?: boolean) => void;
  deselectInstance: (instanceId: string) => void;
  toggleInstance: (instanceId: string, instance: DeckCardInstance) => void;
  isInstanceSelected: (instanceId: string) => boolean;
  getSelectedInstances: () => string[];
  getSelectedInstanceCount: () => number;
  
  // Card-based selection (for collection)
  selectCard: (cardId: string, card: ScryfallCard, ctrlKey?: boolean) => void;
  deselectCard: (cardId: string) => void;
  toggleCard: (cardId: string, card: ScryfallCard) => void;
  isCardSelected: (cardId: string) => boolean;
  getSelectedCards: () => string[];
  getSelectedCardCount: () => number;
  
  // Legacy compatibility (determines type automatically)
  isSelected: (id: string) => boolean;
  
  // General actions
  selectAll: (ids: string[], type: 'card' | 'instance') => void;
  clearSelection: () => void;
  clearOnFilterChange: () => void;
  
  // Drag selection
  startDragSelection: (point: { x: number; y: number }) => void;
  updateDragSelection: (point: { x: number; y: number }) => void;
  endDragSelection: (ids: string[], type: 'card' | 'instance') => void;
  
  // Access to card/instance objects
  getSelectedCardObjects: () => ScryfallCard[];
  getSelectedInstanceObjects: () => DeckCardInstance[];
}

const INITIAL_STATE: SelectionState = {
  selectedInstances: new Set(),
  selectedCards: new Set(),
  lastSelectedType: 'card',
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
  const selectedInstancesRef = useRef<Map<string, DeckCardInstance>>(new Map());

  // Clear selection when filters change (from external trigger)
  const clearOnFilterChange = useCallback(() => {
    setState(prev => ({
      ...prev,
      selectedInstances: new Set(),
      selectedCards: new Set(),
      lastSelectedId: null,
      lastSelectedType: 'card',
      selectionMode: 'single',
    }));
    selectedCardsRef.current.clear();
    selectedInstancesRef.current.clear();
  }, []);

  // Instance-based selection (for deck/sideboard cards)
  const selectInstance = useCallback((instanceId: string, instance: DeckCardInstance, ctrlKey = false) => {
    setState(prev => {
      if (ctrlKey || prev.selectionMode === 'multiple') {
        // Multi-selection mode
        const newSelectedInstances = new Set(prev.selectedInstances);
        
        if (newSelectedInstances.has(instanceId)) {
          // Deselect if already selected
          newSelectedInstances.delete(instanceId);
          selectedInstancesRef.current.delete(instanceId);
        } else {
          // Add to selection
          newSelectedInstances.add(instanceId);
          selectedInstancesRef.current.set(instanceId, instance);
        }

        return {
          ...prev,
          selectedInstances: newSelectedInstances,
          selectedCards: new Set(), // Clear card selection when selecting instances
          lastSelectedId: instanceId,
          lastSelectedType: 'instance',
          selectionMode: newSelectedInstances.size > 1 ? 'multiple' : 'single',
        };
      } else {
        // Single selection mode
        selectedInstancesRef.current.clear();
        selectedCardsRef.current.clear();
        selectedInstancesRef.current.set(instanceId, instance);
        
        return {
          ...prev,
          selectedInstances: new Set([instanceId]),
          selectedCards: new Set(), // Clear card selection
          lastSelectedId: instanceId,
          lastSelectedType: 'instance',
          selectionMode: 'single',
        };
      }
    });
  }, []);

  // Card-based selection (for collection cards)
  const selectCard = useCallback((cardId: string, card: ScryfallCard, ctrlKey = false) => {
    setState(prev => {
      if (ctrlKey || prev.selectionMode === 'multiple') {
        // Multi-selection mode
        const newSelectedCards = new Set(prev.selectedCards);
        
        if (newSelectedCards.has(cardId)) {
          // Deselect if already selected
          newSelectedCards.delete(cardId);
          selectedCardsRef.current.delete(cardId);
        } else {
          // Add to selection
          newSelectedCards.add(cardId);
          selectedCardsRef.current.set(cardId, card);
        }

        return {
          ...prev,
          selectedCards: newSelectedCards,
          selectedInstances: new Set(), // Clear instance selection when selecting cards
          lastSelectedId: cardId,
          lastSelectedType: 'card',
          selectionMode: newSelectedCards.size > 1 ? 'multiple' : 'single',
        };
      } else {
        // Single selection mode
        selectedCardsRef.current.clear();
        selectedInstancesRef.current.clear();
        selectedCardsRef.current.set(cardId, card);
        
        return {
          ...prev,
          selectedCards: new Set([cardId]),
          selectedInstances: new Set(), // Clear instance selection
          lastSelectedId: cardId,
          lastSelectedType: 'card',
          selectionMode: 'single',
        };
      }
    });
  }, []);

  // Deselect specific instance
  const deselectInstance = useCallback((instanceId: string) => {
    setState(prev => {
      const newSelected = new Set(prev.selectedInstances);
      newSelected.delete(instanceId);
      selectedInstancesRef.current.delete(instanceId);

      return {
        ...prev,
        selectedInstances: newSelected,
        lastSelectedId: newSelected.size > 0 ? Array.from(newSelected)[0] : null,
        selectionMode: newSelected.size > 1 ? 'multiple' : 'single',
      };
    });
  }, []);

  // Deselect specific card
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

  // Toggle instance selection
  const toggleInstance = useCallback((instanceId: string, instance: DeckCardInstance) => {
    setState(prev => {
      const newSelected = new Set(prev.selectedInstances);
      
      if (newSelected.has(instanceId)) {
        newSelected.delete(instanceId);
        selectedInstancesRef.current.delete(instanceId);
      } else {
        newSelected.add(instanceId);
        selectedInstancesRef.current.set(instanceId, instance);
        // Clear card selection when toggling instances
        selectedCardsRef.current.clear();
      }

      return {
        ...prev,
        selectedInstances: newSelected,
        selectedCards: newSelected.size > 0 ? new Set() : prev.selectedCards, // Clear cards if selecting instances
        lastSelectedId: instanceId,
        lastSelectedType: 'instance',
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
        // Clear instance selection when toggling cards
        selectedInstancesRef.current.clear();
      }

      return {
        ...prev,
        selectedCards: newSelected,
        selectedInstances: newSelected.size > 0 ? new Set() : prev.selectedInstances, // Clear instances if selecting cards
        lastSelectedId: cardId,
        lastSelectedType: 'card',
        selectionMode: newSelected.size > 1 ? 'multiple' : 'single',
      };
    });
  }, []);

  // Select all provided items
  const selectAll = useCallback((ids: string[], type: 'card' | 'instance') => {
    setState(prev => {
      if (type === 'instance') {
        return {
          ...prev,
          selectedInstances: new Set(ids),
          selectedCards: new Set(), // Clear card selection
          lastSelectedId: ids.length > 0 ? ids[ids.length - 1] : null,
          lastSelectedType: 'instance',
          selectionMode: ids.length > 1 ? 'multiple' : 'single',
        };
      } else {
        return {
          ...prev,
          selectedCards: new Set(ids),
          selectedInstances: new Set(), // Clear instance selection
          lastSelectedId: ids.length > 0 ? ids[ids.length - 1] : null,
          lastSelectedType: 'card',
          selectionMode: ids.length > 1 ? 'multiple' : 'single',
        };
      }
    });
  }, []);

  // Clear all selections
  const clearSelection = useCallback(() => {
    setState(prev => ({
      ...prev,
      selectedInstances: new Set(),
      selectedCards: new Set(),
      lastSelectedId: null,
      lastSelectedType: 'card',
      selectionMode: 'single',
    }));
    selectedCardsRef.current.clear();
    selectedInstancesRef.current.clear();
  }, []);

  // Legacy compatibility - check both card and instance selection
  const isSelected = useCallback((id: string) => {
    return state.selectedCards.has(id) || state.selectedInstances.has(id);
  }, [state.selectedCards, state.selectedInstances]);

  // Check if instance is selected
  const isInstanceSelected = useCallback((instanceId: string) => {
    return state.selectedInstances.has(instanceId);
  }, [state.selectedInstances]);

  // Check if card is selected
  const isCardSelected = useCallback((cardId: string) => {
    return state.selectedCards.has(cardId);
  }, [state.selectedCards]);

  // Get array of selected instance IDs
  const getSelectedInstances = useCallback(() => {
    return Array.from(state.selectedInstances);
  }, [state.selectedInstances]);

  // Get array of selected card IDs
  const getSelectedCards = useCallback(() => {
    return Array.from(state.selectedCards);
  }, [state.selectedCards]);

  // Get count of selected instances
  const getSelectedInstanceCount = useCallback(() => {
    return state.selectedInstances.size;
  }, [state.selectedInstances]);

  // Get count of selected cards
  const getSelectedCardCount = useCallback(() => {
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

  // End drag selection and select items within rectangle
  const endDragSelection = useCallback((ids: string[], type: 'card' | 'instance') => {
    setState(prev => {
      if (type === 'instance') {
        return {
          ...prev,
          selectedInstances: new Set(ids),
          selectedCards: new Set(), // Clear card selection
          lastSelectedId: ids.length > 0 ? ids[ids.length - 1] : null,
          lastSelectedType: 'instance',
          selectionMode: ids.length > 1 ? 'multiple' : 'single',
          dragSelection: {
            active: false,
            startPoint: null,
            currentPoint: null,
          },
        };
      } else {
        return {
          ...prev,
          selectedCards: new Set(ids),
          selectedInstances: new Set(), // Clear instance selection
          lastSelectedId: ids.length > 0 ? ids[ids.length - 1] : null,
          lastSelectedType: 'card',
          selectionMode: ids.length > 1 ? 'multiple' : 'single',
          dragSelection: {
            active: false,
            startPoint: null,
            currentPoint: null,
          },
        };
      }
    });
  }, []);

  // Get selected card objects
  const getSelectedCardObjects = useCallback(() => {
    return Array.from(selectedCardsRef.current.values());
  }, []);

  // Get selected instance objects
  const getSelectedInstanceObjects = useCallback(() => {
    return Array.from(selectedInstancesRef.current.values());
  }, []);

  // Keyboard event handler for selection shortcuts
  useEffect(() => {
    const handleKeyboard = (event: KeyboardEvent) => {
      // Escape to clear selection
      if (event.key === 'Escape') {
        clearSelection();
      }
    };

    document.addEventListener('keydown', handleKeyboard);
    return () => document.removeEventListener('keydown', handleKeyboard);
  }, [clearSelection]);

  const actions: SelectionActions = {
    // Instance-based actions
    selectInstance,
    deselectInstance,
    toggleInstance,
    isInstanceSelected,
    getSelectedInstances,
    getSelectedInstanceCount,
    
    // Card-based actions
    selectCard,
    deselectCard,
    toggleCard,
    isCardSelected,
    getSelectedCards,
    getSelectedCardCount,
    
    // Legacy compatibility
    isSelected,
    
    // General actions
    selectAll,
    clearSelection,
    clearOnFilterChange,
    
    // Drag selection
    startDragSelection,
    updateDragSelection,
    endDragSelection,
    
    // Object access
    getSelectedCardObjects,
    getSelectedInstanceObjects,
  };

  return {
    ...state,
    ...actions,
  };
};