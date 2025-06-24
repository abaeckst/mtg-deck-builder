// src/hooks/useContextMenu.ts
import { useState, useCallback } from 'react';
import { ScryfallCard, DeckCard, DeckCardInstance, getCardId } from '../types/card';
import { DropZone } from '../hooks/useDragAndDrop';
import { ContextMenuAction } from '../components/ContextMenu';

export interface ContextMenuState {
  visible: boolean;
  x: number;
  y: number;
  targetCard: ScryfallCard | DeckCard | DeckCardInstance | null;
  targetZone: DropZone | null;
  selectedCards: (ScryfallCard | DeckCard | DeckCardInstance)[];
}

export interface DeckManagementCallbacks {
  addToDeck: (cards: (ScryfallCard | DeckCard | DeckCardInstance)[], quantity?: number) => void;
  removeFromDeck: (cards: (ScryfallCard | DeckCard | DeckCardInstance)[], quantity?: number) => void;
  addToSideboard: (cards: (ScryfallCard | DeckCard | DeckCardInstance)[], quantity?: number) => void;
  removeFromSideboard: (cards: (ScryfallCard | DeckCard | DeckCardInstance)[], quantity?: number) => void;
  moveDeckToSideboard: (cards: (ScryfallCard | DeckCard | DeckCardInstance)[], quantity?: number) => void;
  moveSideboardToDeck: (cards: (ScryfallCard | DeckCard | DeckCardInstance)[], quantity?: number) => void;
  getDeckQuantity: (cardId: string) => number;
  getSideboardQuantity: (cardId: string) => number;
}

const INITIAL_STATE: ContextMenuState = {
  visible: false,
  x: 0,
  y: 0,
  targetCard: null,
  targetZone: null,
  selectedCards: [],
};

export const useContextMenu = (callbacks: DeckManagementCallbacks) => {
  const [state, setState] = useState<ContextMenuState>(INITIAL_STATE);

  // Show context menu
  const showContextMenu = useCallback((
    event: React.MouseEvent,
    card: ScryfallCard | DeckCard | DeckCardInstance,
    zone: DropZone,
    selectedCards: (ScryfallCard | DeckCard | DeckCardInstance)[] = []
  ) => {
    event.preventDefault();
    event.stopPropagation();

    setState({
      visible: true,
      x: event.clientX,
      y: event.clientY,
      targetCard: card,
      targetZone: zone,
      selectedCards: selectedCards,
    });
  }, []);

  // Hide context menu
  const hideContextMenu = useCallback(() => {
    setState(INITIAL_STATE);
  }, []);

  // Generate context menu actions based on zone and selection
  const getContextMenuActions = useCallback((): ContextMenuAction[] => {
    if (!state.targetCard || !state.targetZone) return [];

    const { targetCard, targetZone, selectedCards } = state;
    const isMultiSelection = selectedCards.length > 1;
    const cardCount = isMultiSelection ? selectedCards.length : 1;
    const cardsToAct = isMultiSelection ? selectedCards : [targetCard];
    
    // Get current quantities for the target card using the utility function
    const cardId = getCardId(targetCard);
    const deckQuantity = callbacks.getDeckQuantity(cardId);
    const sideboardQuantity = callbacks.getSideboardQuantity(cardId);

    const actions: ContextMenuAction[] = [];

    if (targetZone === 'collection') {
      // Collection context menu
      actions.push({
        label: `Add ${cardCount > 1 ? `${cardCount} cards` : '1'} to Deck`,
        onClick: () => callbacks.addToDeck(cardsToAct, 1),
      });

      actions.push({
        label: `Fill Deck With ${cardCount > 1 ? 'These' : 'This'} (Up to 4 each)`,
        onClick: () => callbacks.addToDeck(cardsToAct, 4),
      });

      actions.push({ separator: true, label: '', onClick: () => {} });

      actions.push({
        label: `Add ${cardCount > 1 ? `${cardCount} cards` : '1'} to Sideboard`,
        onClick: () => callbacks.addToSideboard(cardsToAct, 1),
      });

      actions.push({
        label: `Fill Sideboard With ${cardCount > 1 ? 'These' : 'This'} (Up to 4 each)`,
        onClick: () => callbacks.addToSideboard(cardsToAct, 4),
      });

    } else if (targetZone === 'deck') {
      // Deck context menu
      actions.push({
        label: `Add ${cardCount > 1 ? `${cardCount} more` : '1 more'} to Deck`,
        onClick: () => callbacks.addToDeck(cardsToAct, 1),
        disabled: !isMultiSelection && deckQuantity >= 4 && !targetCard.type_line?.includes('Basic Land'),
      });

      actions.push({
        label: `Remove ${cardCount > 1 ? `${cardCount}` : '1'} from Deck`,
        onClick: () => callbacks.removeFromDeck(cardsToAct, 1),
        disabled: !isMultiSelection && deckQuantity <= 0,
      });

      if (!isMultiSelection) {
        actions.push({
          label: 'Remove All Copies from Deck',
          onClick: () => callbacks.removeFromDeck([targetCard], deckQuantity),
          disabled: deckQuantity <= 0,
        });
      }

      actions.push({ separator: true, label: '', onClick: () => {} });

      actions.push({
        label: `Move ${cardCount > 1 ? `${cardCount}` : '1'} to Sideboard`,
        onClick: () => callbacks.moveDeckToSideboard(cardsToAct, 1),
        disabled: !isMultiSelection && deckQuantity <= 0,
      });

      if (!isMultiSelection) {
        actions.push({
          label: 'Move All Copies to Sideboard',
          onClick: () => callbacks.moveDeckToSideboard([targetCard], deckQuantity),
          disabled: deckQuantity <= 0,
        });
      }

    } else if (targetZone === 'sideboard') {
      // Sideboard context menu
      actions.push({
        label: `Add ${cardCount > 1 ? `${cardCount} more` : '1 more'} to Sideboard`,
        onClick: () => callbacks.addToSideboard(cardsToAct, 1),
        disabled: !isMultiSelection && sideboardQuantity >= 4 && !targetCard.type_line?.includes('Basic Land'),
      });

      actions.push({
        label: `Remove ${cardCount > 1 ? `${cardCount}` : '1'} from Sideboard`,
        onClick: () => callbacks.removeFromSideboard(cardsToAct, 1),
        disabled: !isMultiSelection && sideboardQuantity <= 0,
      });

      if (!isMultiSelection) {
        actions.push({
          label: 'Remove All Copies from Sideboard',
          onClick: () => callbacks.removeFromSideboard([targetCard], sideboardQuantity),
          disabled: sideboardQuantity <= 0,
        });
      }

      actions.push({ separator: true, label: '', onClick: () => {} });

      actions.push({
        label: `Move ${cardCount > 1 ? `${cardCount}` : '1'} to Deck`,
        onClick: () => callbacks.moveSideboardToDeck(cardsToAct, 1),
        disabled: !isMultiSelection && sideboardQuantity <= 0,
      });

      if (!isMultiSelection) {
        actions.push({
          label: 'Move All Copies to Deck',
          onClick: () => callbacks.moveSideboardToDeck([targetCard], sideboardQuantity),
          disabled: sideboardQuantity <= 0,
        });
      }
    }

    return actions;
  }, [state, callbacks]);

  return {
    contextMenuState: state,
    showContextMenu,
    hideContextMenu,
    getContextMenuActions,
  };
};