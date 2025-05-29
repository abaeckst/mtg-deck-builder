// src/hooks/useDragAndDrop.ts
import { useState, useCallback, useRef, useEffect } from 'react';
import { ScryfallCard, DeckCard } from '../types/card';

export type DraggedCard = ScryfallCard | DeckCard;
export type DropZone = 'collection' | 'deck' | 'sideboard';

export interface DragState {
  isDragging: boolean;
  draggedCards: DraggedCard[];
  draggedFrom: DropZone | null;
  dragPreview: {
    x: number;
    y: number;
    visible: boolean;
  };
  dropZone: DropZone | null;
  canDrop: boolean;
}

export interface DragCallbacks {
  onCardMove: (cards: DraggedCard[], from: DropZone, to: DropZone) => void;
  onDragStart?: (cards: DraggedCard[], from: DropZone) => void;
  onDragEnd?: (cards: DraggedCard[], success: boolean) => void;
}

export interface DragAndDropActions {
  startDrag: (cards: DraggedCard[], from: DropZone, event: React.MouseEvent) => void;
  updateDrag: (event: React.MouseEvent) => void;
  endDrag: () => void;
  setDropZone: (zone: DropZone | null, canDrop: boolean) => void;
  canDropInZone: (zone: DropZone, cards: DraggedCard[]) => boolean;
}

const INITIAL_DRAG_STATE: DragState = {
  isDragging: false,
  draggedCards: [],
  draggedFrom: null,
  dragPreview: {
    x: 0,
    y: 0,
    visible: false,
  },
  dropZone: null,
  canDrop: false,
};

export const useDragAndDrop = (callbacks: DragCallbacks) => {
  const [dragState, setDragState] = useState<DragState>(INITIAL_DRAG_STATE);
  const dragOffsetRef = useRef<{ x: number; y: number }>({ x: 0, y: 0 });

  // Start dragging operation
  const startDrag = useCallback((
    cards: DraggedCard[], 
    from: DropZone, 
    event: React.MouseEvent
  ) => {
    event.preventDefault();
    
    // Calculate drag offset from mouse position to top-left of dragged element
    const rect = (event.currentTarget as HTMLElement).getBoundingClientRect();
    dragOffsetRef.current = {
      x: event.clientX - rect.left,
      y: event.clientY - rect.top,
    };

    setDragState({
      isDragging: true,
      draggedCards: cards,
      draggedFrom: from,
      dragPreview: {
        x: event.clientX - dragOffsetRef.current.x,
        y: event.clientY - dragOffsetRef.current.y,
        visible: true,
      },
      dropZone: null,
      canDrop: false,
    });

    // Callback for drag start
    callbacks.onDragStart?.(cards, from);

    // Prevent text selection during drag
    document.body.style.userSelect = 'none';
  }, [callbacks]);

  // Update drag position
  const updateDrag = useCallback((event: React.MouseEvent) => {
    if (!dragState.isDragging) return;

    setDragState(prev => ({
      ...prev,
      dragPreview: {
        ...prev.dragPreview,
        x: event.clientX - dragOffsetRef.current.x,
        y: event.clientY - dragOffsetRef.current.y,
      },
    }));
  }, [dragState.isDragging]);

  // End dragging operation
  const endDrag = useCallback(() => {
    if (!dragState.isDragging) return;

    const { draggedCards, draggedFrom, dropZone, canDrop } = dragState;
    let success = false;

    // Execute drop if valid
    if (dropZone && canDrop && draggedFrom && dropZone !== draggedFrom) {
      callbacks.onCardMove(draggedCards, draggedFrom, dropZone);
      success = true;
    }

    // Callback for drag end
    callbacks.onDragEnd?.(draggedCards, success);

    // Reset drag state
    setDragState(INITIAL_DRAG_STATE);

    // Restore text selection
    document.body.style.userSelect = '';
  }, [dragState, callbacks]);

  // Set current drop zone
  const setDropZone = useCallback((zone: DropZone | null, canDrop: boolean) => {
    setDragState(prev => ({
      ...prev,
      dropZone: zone,
      canDrop: canDrop,
    }));
  }, []);

  // Determine if cards can be dropped in a zone
  const canDropInZone = useCallback((zone: DropZone, cards: DraggedCard[]): boolean => {
    // If not currently dragging, allow all drops (for initial setup)
    if (!dragState.isDragging || !dragState.draggedFrom) return true;
    
    // Can't drop in the same zone you're dragging from
    if (zone === dragState.draggedFrom) return false;

    // Basic validation rules
    switch (zone) {
      case 'deck':
        // Check 4-copy rule for non-basic lands (simplified for now)
        return cards.every(card => {
          const isBasicLand = card.type_line?.includes('Basic Land') || false;
          return isBasicLand || true; // Allow all cards for now - can add deck limit checking later
        });
      
      case 'sideboard':
        // Similar rules as deck (simplified for now)
        return cards.every(card => {
          const isBasicLand = card.type_line?.includes('Basic Land') || false;
          return isBasicLand || true; // Allow all cards for now - can add sideboard limit checking later
        });
      
      case 'collection':
        // Can ALWAYS move cards back to collection (this fixes deck/sideboard → collection)
        return true;
      
      default:
        return false;
    }
  }, [dragState.draggedFrom, dragState.isDragging]);

  // Mouse event handlers for global drag tracking
  useEffect(() => {
    if (!dragState.isDragging) return;

    const handleMouseMove = (event: MouseEvent) => {
      setDragState(prev => ({
        ...prev,
        dragPreview: {
          ...prev.dragPreview,
          x: event.clientX - dragOffsetRef.current.x,
          y: event.clientY - dragOffsetRef.current.y,
        },
      }));
    };

    const handleMouseUp = () => {
      endDrag();
    };

    // Add global mouse listeners
    document.addEventListener('mousemove', handleMouseMove);
    document.addEventListener('mouseup', handleMouseUp);

    // Cleanup
    return () => {
      document.removeEventListener('mousemove', handleMouseMove);
      document.removeEventListener('mouseup', handleMouseUp);
    };
  }, [dragState.isDragging, endDrag]);

  // Keyboard escape to cancel drag
  useEffect(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.key === 'Escape' && dragState.isDragging) {
        // Cancel drag without drop
        callbacks.onDragEnd?.(dragState.draggedCards, false);
        setDragState(INITIAL_DRAG_STATE);
        document.body.style.userSelect = '';
      }
    };

    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, [dragState.isDragging, dragState.draggedCards, callbacks]);

  const actions: DragAndDropActions = {
    startDrag,
    updateDrag,
    endDrag,
    setDropZone,
    canDropInZone,
  };

  return {
    dragState,
    ...actions,
  };
};