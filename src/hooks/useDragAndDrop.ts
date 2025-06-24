// src/hooks/useDragAndDrop.ts - Phase 3A: Rock-Solid Click/Drag Interaction System
import { useState, useCallback, useRef, useEffect } from 'react';
import { ScryfallCard, DeckCard, DeckCardInstance, getCardId } from '../types/card';

export type DraggedCard = ScryfallCard | DeckCard | DeckCardInstance;
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
  handleDoubleClick: (card: DraggedCard, zone: DropZone, event: React.MouseEvent) => void;
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

// Enhanced interaction timing constants
const INTERACTION_TIMINGS = {
  DOUBLE_CLICK_MAX_INTERVAL: 500,  // Max time between clicks for double-click
  RAPID_CLICK_MAX_INTERVAL: 800,   // Max time for rapid click sequence
  DRAG_START_DELAY: 150,           // Minimum hold time before drag starts
  DRAG_MOVEMENT_THRESHOLD: 5,      // Minimum pixel movement to start drag
  CLICK_TO_DRAG_PROTECTION: 300,   // Protection time after click before drag
};

export const useDragAndDrop = (callbacks: DragCallbacks) => {
  const [dragState, setDragState] = useState<DragState>(INITIAL_DRAG_STATE);
  const dragOffsetRef = useRef<{ x: number; y: number }>({ x: 0, y: 0 });
  
  // CRITICAL FIX: Capture last valid drop zone before it gets reset to null
  const lastValidDropZoneRef = useRef<{ zone: DropZone | null; canDrop: boolean }>({ zone: null, canDrop: false });
  
  // Enhanced interaction tracking
  const interactionRef = useRef<{
    // Click tracking
    lastClickTime: number;
    lastClickCard: string | null;
    clickCount: number;
    rapidClickTimer: NodeJS.Timeout | null;
    
    // Drag tracking
    mouseDownTime: number;
    mouseDownPosition: { x: number; y: number };
    isDragInitiated: boolean;
    dragStartTimer: NodeJS.Timeout | null;
    
    // Event prevention
    preventNextClick: boolean;
    preventDragUntil: number;
  }>({
    lastClickTime: 0,
    lastClickCard: null,
    clickCount: 0,
    rapidClickTimer: null,
    mouseDownTime: 0,
    mouseDownPosition: { x: 0, y: 0 },
    isDragInitiated: false,
    dragStartTimer: null,
    preventNextClick: false,
    preventDragUntil: 0,
  });

  // Fixed rapid double-click handler with processing debounce
  const handleDoubleClick = useCallback((card: DraggedCard, zone: DropZone, event: React.MouseEvent) => {
    console.log(`🔧 DOUBLE-CLICK DEBUG: handleDoubleClick called for ${card.name} in ${zone}`);
    
    event.preventDefault();
    event.stopPropagation();
    
    // Prevent any drag attempts for the next period
    interactionRef.current.preventDragUntil = Date.now() + INTERACTION_TIMINGS.CLICK_TO_DRAG_PROTECTION;
    
    const now = Date.now();
    const timeDiff = now - interactionRef.current.lastClickTime;
    const cardId = getCardId(card); // Use utility function
    const isSameCard = interactionRef.current.lastClickCard === cardId;
    
    console.log(`🖱️ Double-click handler: ${card.name} in ${zone}`);
    console.log(`📊 Timing: ${timeDiff}ms since last, same card: ${isSameCard}, event.detail: ${event.detail}`);
    
    // CRITICAL FIX: Prevent processing if we just processed this card very recently
    const PROCESSING_DEBOUNCE = 100; // ms
    if (isSameCard && timeDiff < PROCESSING_DEBOUNCE) {
      console.log(`🚫 Debounced rapid double-click on ${card.name} (${timeDiff}ms since last)`);
      return;
    }
    
    // Clear any existing rapid click timer
    if (interactionRef.current.rapidClickTimer) {
      clearTimeout(interactionRef.current.rapidClickTimer);
      interactionRef.current.rapidClickTimer = null;
    }
    
    // FIXED: Update timing BEFORE processing to establish debounce
    interactionRef.current.lastClickTime = now;
    interactionRef.current.lastClickCard = cardId;
    
    // Process the card move once per debounce period
    try {
      console.log(`🎯 Processing double-click move for ${card.name}`);
      if (zone === 'collection') {
        callbacks.onCardMove([card], 'collection', 'deck');
        console.log(`✅ Added ${card.name} to deck`);
      } else if (zone === 'deck' || zone === 'sideboard') {
        callbacks.onCardMove([card], zone, 'collection');
        console.log(`✅ Removed ${card.name} from ${zone}`);
      }
    } catch (error) {
      console.error('❌ Error processing double-click:', error);
    }
    
  }, [callbacks]);

  // Enhanced drag start with proper click-and-hold detection
  const startDrag = useCallback((
    cards: DraggedCard[], 
    from: DropZone, 
    event: React.MouseEvent
  ) => {
    console.log(`🔧 DRAG DEBUG: startDrag called with ${cards.length} cards from ${from}`);
    console.log(`🔧 DRAG DEBUG: startDrag received cards:`, cards.map(c => c.name));
    console.log(`🔧 DRAG DEBUG: Call stack:`, new Error().stack?.split('\\n').slice(1, 6));
    console.log(`🔧 DRAG DEBUG: Event detail:`, event.detail);
    // Complete prevention of drag during double-click protection period
    const now = Date.now();
    if (now < interactionRef.current.preventDragUntil) {
      console.log('Drag prevented: within double-click protection period');
      return;
    }
    
    // Don't start drag on double-click events
    if (event.detail >= 2) {
      console.log('Drag prevented: double-click detected');
      event.preventDefault();
      event.stopPropagation();
      return;
    }
    
    // Clear any drag start timer
    if (interactionRef.current.dragStartTimer) {
      clearTimeout(interactionRef.current.dragStartTimer);
      interactionRef.current.dragStartTimer = null;
    }
    
    // Record mouse down position and time
    interactionRef.current.mouseDownTime = now;
    interactionRef.current.mouseDownPosition = { x: event.clientX, y: event.clientY };
    interactionRef.current.isDragInitiated = false;
    
    console.log(`Mouse down recorded at (${event.clientX}, ${event.clientY}) for potential drag`);
    
    // Get element reference safely
    const element = event.currentTarget as HTMLElement;
    if (!element) {
      console.log('Drag cancelled: no element reference');
      return;
    }
    
    // Calculate drag offset
    const rect = element.getBoundingClientRect();
    dragOffsetRef.current = {
      x: event.clientX - rect.left,
      y: event.clientY - rect.top,
    };
    
    // Set up timer for minimum hold time
    interactionRef.current.dragStartTimer = setTimeout(() => {
      // Additional check: ensure we haven't moved into double-click territory
      const finalTimeSinceMouseDown = Date.now() - interactionRef.current.mouseDownTime;
      if (finalTimeSinceMouseDown < INTERACTION_TIMINGS.DRAG_START_DELAY) {
        console.log('Drag cancelled: insufficient hold time');
        return;
      }
      
      // Check we're still not in double-click protection
      if (Date.now() < interactionRef.current.preventDragUntil) {
        console.log('Drag cancelled: double-click protection still active');
        return;
      }
      
      console.log(`Initiating drag for ${cards.length} cards from ${from}`);
      interactionRef.current.isDragInitiated = true;
      
      // Set initial drag state
      setDragState({
        isDragging: true,
        draggedCards: cards,
        draggedFrom: from,
        dragPreview: {
          x: interactionRef.current.mouseDownPosition.x - dragOffsetRef.current.x,
          y: interactionRef.current.mouseDownPosition.y - dragOffsetRef.current.y,
          visible: true,
        },
        dropZone: null,
        canDrop: false,
      });

      callbacks.onDragStart?.(cards, from);
      document.body.style.userSelect = 'none';
    }, INTERACTION_TIMINGS.DRAG_START_DELAY);
    
    // Set up mouse move listener for movement-based drag initiation
    const handleEarlyMouseMove = (moveEvent: MouseEvent) => {
      const deltaX = Math.abs(moveEvent.clientX - interactionRef.current.mouseDownPosition.x);
      const deltaY = Math.abs(moveEvent.clientY - interactionRef.current.mouseDownPosition.y);
      const movement = Math.sqrt(deltaX * deltaX + deltaY * deltaY);
      
      // If significant movement detected and minimum time passed, start drag immediately
      if (movement > INTERACTION_TIMINGS.DRAG_MOVEMENT_THRESHOLD) {
        const holdTime = Date.now() - interactionRef.current.mouseDownTime;
        if (holdTime >= INTERACTION_TIMINGS.DRAG_START_DELAY && !interactionRef.current.isDragInitiated) {
          console.log(`Movement-triggered drag: ${movement}px movement after ${holdTime}ms hold`);
          
          // Clear the timer since we're starting drag now
          if (interactionRef.current.dragStartTimer) {
            clearTimeout(interactionRef.current.dragStartTimer);
            interactionRef.current.dragStartTimer = null;
          }
          
          // Start drag immediately
          interactionRef.current.isDragInitiated = true;
          
          setDragState({
            isDragging: true,
            draggedCards: cards,
            draggedFrom: from,
            dragPreview: {
              x: moveEvent.clientX - dragOffsetRef.current.x,
              y: moveEvent.clientY - dragOffsetRef.current.y,
              visible: true,
            },
            dropZone: null,
            canDrop: false,
          });

          callbacks.onDragStart?.(cards, from);
          document.body.style.userSelect = 'none';
        }
      }
    };
    
    const handleEarlyMouseUp = () => {
      // Clear drag initiation if mouse released before drag started
      if (interactionRef.current.dragStartTimer) {
        clearTimeout(interactionRef.current.dragStartTimer);
        interactionRef.current.dragStartTimer = null;
      }
      
      document.removeEventListener('mousemove', handleEarlyMouseMove);
      document.removeEventListener('mouseup', handleEarlyMouseUp);
      
      console.log('Mouse released before drag initiated - treating as click');
    };
    
    // Add temporary listeners for early movement detection
    document.addEventListener('mousemove', handleEarlyMouseMove);
    document.addEventListener('mouseup', handleEarlyMouseUp);
    
  }, [callbacks]);

  // Update drag position with smooth performance
  const updateDrag = useCallback((event: React.MouseEvent) => {
    if (!dragState.isDragging) return;

    requestAnimationFrame(() => {
      setDragState(prev => ({
        ...prev,
        dragPreview: {
          ...prev.dragPreview,
          x: event.clientX - dragOffsetRef.current.x,
          y: event.clientY - dragOffsetRef.current.y,
        },
      }));
    });
  }, [dragState.isDragging]);

  // FINAL FIX: End dragging with proper drop zone handling
  const endDrag = useCallback(() => {
    // Use functional state update to get current state
    setDragState(currentDragState => {
      if (!currentDragState.isDragging) {
        console.log('⚠️ endDrag called but not currently dragging');
        return currentDragState;
      }

      const { draggedCards, draggedFrom } = currentDragState;
      let success = false;

      // CRITICAL FIX: Use the last valid drop zone if current one is null
      const dropZone = currentDragState.dropZone || lastValidDropZoneRef.current.zone;
      const canDrop = currentDragState.canDrop || lastValidDropZoneRef.current.canDrop;

      console.log(`🔍 DEBUGGING endDrag conditions (FINAL FIX):`);
      console.log(`   current dropZone: ${currentDragState.dropZone}`);
      console.log(`   last valid dropZone: ${lastValidDropZoneRef.current.zone}`);
      console.log(`   using dropZone: ${dropZone} (${typeof dropZone})`);
      console.log(`   canDrop: ${canDrop} (${typeof canDrop})`);
      console.log(`   draggedFrom: ${draggedFrom} (${typeof draggedFrom})`);
      console.log(`   dropZone !== draggedFrom: ${dropZone !== draggedFrom}`);
      console.log(`   All conditions: ${!!(dropZone && canDrop && draggedFrom && dropZone !== draggedFrom)}`);

      // Execute drop if valid
      if (dropZone && canDrop && draggedFrom && dropZone !== draggedFrom) {
        console.log(`✅ CONDITIONS MET - Moving ${draggedCards.length} cards from ${draggedFrom} to ${dropZone}`);
        callbacks.onCardMove(draggedCards, draggedFrom, dropZone);
        success = true;
      } else {
        console.log('❌ CONDITIONS NOT MET - Drop cancelled');
        if (!dropZone) console.log('   - No dropZone');
        if (!canDrop) console.log('   - Cannot drop');
        if (!draggedFrom) console.log('   - No draggedFrom');
        if (dropZone === draggedFrom) console.log('   - Same zone');
      }

      // Callback for drag end
      callbacks.onDragEnd?.(draggedCards, success);

      // Reset interaction state
      interactionRef.current.isDragInitiated = false;
      
      // Reset last valid drop zone
      lastValidDropZoneRef.current = { zone: null, canDrop: false };

      // Restore text selection
      document.body.style.userSelect = '';
      
      console.log(`🏁 Drag ended: ${success ? 'successful drop' : 'cancelled'}`);

      // Return reset state
      return INITIAL_DRAG_STATE;
    });
  }, [callbacks]);

  // FIXED: Set current drop zone and capture valid ones
  const setDropZone = useCallback((zone: DropZone | null, canDrop: boolean) => {
    // Capture the last valid drop zone before it gets reset
    if (zone !== null) {
      lastValidDropZoneRef.current = { zone, canDrop };
      console.log(`📍 Captured valid drop zone: ${zone}, canDrop: ${canDrop}`);
    }
    
    setDragState(prev => ({
      ...prev,
      dropZone: zone,
      canDrop: canDrop,
    }));
  }, []);

  // Enhanced drop zone validation
  const canDropInZone = useCallback((zone: DropZone, cards: DraggedCard[]): boolean => {
    // If not currently dragging, allow all drops
    if (!dragState.isDragging || !dragState.draggedFrom) return true;
    
    // Can't drop in the same zone you're dragging from
    if (zone === dragState.draggedFrom) return false;

    // All zones accept cards for this implementation
    switch (zone) {
      case 'deck':
      case 'sideboard':
        // Accept all cards (deck limits handled in callback)
        return true;
      
      case 'collection':
        // Can ALWAYS move cards back to collection
        return true;
      
      default:
        return false;
    }
  }, [dragState.draggedFrom, dragState.isDragging]);

  // Enhanced global mouse event handlers
  useEffect(() => {
    if (!dragState.isDragging) return;

    const handleMouseMove = (event: MouseEvent) => {
      requestAnimationFrame(() => {
        setDragState(prev => ({
          ...prev,
          dragPreview: {
            ...prev.dragPreview,
            x: event.clientX - dragOffsetRef.current.x,
            y: event.clientY - dragOffsetRef.current.y,
          },
        }));
      });
    };

    const handleMouseUp = () => {
      endDrag();
    };

    // Add global listeners
    document.addEventListener('mousemove', handleMouseMove, { passive: true });
    document.addEventListener('mouseup', handleMouseUp);

    return () => {
      document.removeEventListener('mousemove', handleMouseMove);
      document.removeEventListener('mouseup', handleMouseUp);
    };
  }, [dragState.isDragging, endDrag]);

  // Keyboard shortcuts for enhanced UX
  useEffect(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.key === 'Escape' && dragState.isDragging) {
        console.log('Drag cancelled by Escape key');
        callbacks.onDragEnd?.(dragState.draggedCards, false);
        setDragState(INITIAL_DRAG_STATE);
        document.body.style.userSelect = '';
      }
    };

    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, [dragState.isDragging, dragState.draggedCards, callbacks]);

  // Cleanup timers on unmount
  useEffect(() => {
    return () => {
      if (interactionRef.current.rapidClickTimer) {
        clearTimeout(interactionRef.current.rapidClickTimer);
      }
      if (interactionRef.current.dragStartTimer) {
        clearTimeout(interactionRef.current.dragStartTimer);
      }
    };
  }, []);

  const actions: DragAndDropActions = {
    startDrag,
    updateDrag,
    endDrag,
    setDropZone,
    canDropInZone,
    handleDoubleClick,
  };

  return {
    dragState,
    ...actions,
  };
};