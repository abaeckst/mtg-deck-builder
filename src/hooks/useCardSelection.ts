// src/hooks/useCardSelection.ts - Card selection state management
import { useState, useCallback } from 'react';
import { ScryfallCard } from '../types/card';

export interface CardSelectionState {
  selectedCards: Set<string>;
}

export interface CardSelectionActions {
  selectCard: (cardId: string) => void;
  deselectCard: (cardId: string) => void;
  clearSelection: () => void;
  isCardSelected: (cardId: string) => boolean;
  getSelectedCardsData: (cards: ScryfallCard[]) => ScryfallCard[];
}

export const useCardSelection = (): CardSelectionState & CardSelectionActions => {
  const [selectedCards, setSelectedCards] = useState<Set<string>>(new Set());

  // Card selection functions
  const selectCard = useCallback((cardId: string) => {
    setSelectedCards(prev => {
      const newSelected = new Set(prev);
      newSelected.add(cardId);
      return newSelected;
    });
  }, []);

  const deselectCard = useCallback((cardId: string) => {
    setSelectedCards(prev => {
      const newSelected = new Set(prev);
      newSelected.delete(cardId);
      return newSelected;
    });
  }, []);

  const clearSelection = useCallback(() => {
    setSelectedCards(new Set());
  }, []);

  const isCardSelected = useCallback((cardId: string): boolean => {
    return selectedCards.has(cardId);
  }, [selectedCards]);

  const getSelectedCardsData = useCallback((cards: ScryfallCard[]): ScryfallCard[] => {
    return cards.filter(card => selectedCards.has(card.id));
  }, [selectedCards]);

  return {
    selectedCards,
    selectCard,
    deselectCard,
    clearSelection,
    isCardSelected,
    getSelectedCardsData,
  };
};