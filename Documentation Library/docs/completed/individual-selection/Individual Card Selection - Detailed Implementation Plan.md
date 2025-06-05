# Individual Card Selection - Detailed Implementation Plan

**Date:** June 2, 2025 
**Session:** Quality of Life Session 2 - Individual Card Selection Architecture 
**Status:** Planned - Ready for Implementation 
**Priority:** Critical - Core deck building functionality fix 

## 🎯 Project Overview

**Problem:** All copies of the same card are selected when clicking one copy because the selection system uses shared Scryfall IDs instead of unique instance identifiers.
**Solution:** Implement instance-based architecture for deck and sideboard cards while maintaining ID-based system for collection area.
**Impact:** Major architectural change affecting deck state management, selection system, and UI components.

## 🏗️ Architectural Design

### **Core Concept: Dual Identity System**

**Collection Area (Unchanged):**

- Uses `ScryfallCard` objects with shared IDs
- Selection based on card IDs (current behavior)
- Search results and filtering remain unchanged
  **Deck/Sideboard Areas (New):**
- Uses `DeckCardInstance` objects with unique instance IDs
- Selection based on instance IDs (individual card copies)
- Each physical card copy has its own identity
  
  ### **New Type Definitions**
  
  ```typescript
  // New instance-based card type
  export interface DeckCardInstance {
  instanceId: string; // Unique: "cardId-zone-timestamp-random"
  cardId: string; // Original Scryfall ID
  name: string;
  image_uri: string;
  mana_cost?: string;
  cmc: number;
  type_line: string;
  colors: string[];
  color_identity: string[];
  set: string;
  rarity: 'common' | 'uncommon' | 'rare' | 'mythic' | 'special' | 'bonus';
  oracle_text?: string;
  power?: string;
  toughness?: string;
  loyalty?: string;
  zone: 'deck' | 'sideboard'; // Track which zone this instance belongs to
  addedAt: number; // Timestamp for ordering/history
  }
  // Utility functions
  export const generateInstanceId = (cardId: string, zone: string): string => {
  const timestamp = Date.now();
  const random = Math.random().toString(36).substr(2, 5);
  return `${cardId}-${zone}-${timestamp}-${random}`;
  };
  export const scryfallToDeckInstance = (
  card: ScryfallCard, 
  zone: 'deck' | 'sideboard'
  ): DeckCardInstance => {
  return {
  instanceId: generateInstanceId(card.id, zone),
  cardId: card.id,
  name: card.name,
  // ... copy all other properties
  zone,
  addedAt: Date.now()
  };
  };
  ```
  
  ### **State Management Changes**
  
  **Current State:**
  
  ```typescript
  const [mainDeck, setMainDeck] = useState<DeckCard[]>([]); // Quantity-based
  const [sideboard, setSideboard] = useState<DeckCard[]>([]); // Quantity-based
  ```
  
  **New State:**
  
  ```typescript
  const [mainDeck, setMainDeck] = useState<DeckCardInstance[]>([]); // Instance-based
  const [sideboard, setSideboard] = useState<DeckCardInstance[]>([]); // Instance-based
  ```
  
  ## 📋 Implementation Phases
  
  ### **Phase 1: Core Type System & Utilities (45 minutes)**
  
  #### **Files to Modify:**
1. **`src/types/card.ts`**
   - Add `DeckCardInstance` interface
   - Add utility functions for instance management
   - Keep existing types for backward compatibility
     
     #### **New Utility Functions:**
     
     ```typescript
     // Instance management
     export const generateInstanceId = (cardId: string, zone: string): string;
     export const scryfallToDeckInstance = (card: ScryfallCard, zone: 'deck' | 'sideboard'): DeckCardInstance;
     export const getCardQuantityInZone = (instances: DeckCardInstance[], cardId: string): number;
     export const getTotalCardQuantity = (deckInstances: DeckCardInstance[], sideboardInstances: DeckCardInstance[], cardId: string): number;
     export const groupInstancesByCardId = (instances: DeckCardInstance[]): Map<string, DeckCardInstance[]>;
     ```
     
     #### **Success Criteria:**
- [ ] New types compile without errors
- [ ] Utility functions create unique instance IDs
- [ ] Instance creation from ScryfallCard works correctly
  
  ### **Phase 2: Deck State Management Refactor (90 minutes)**
  
  #### **Files to Modify:**
1. **`src/components/MTGOLayout.tsx`** (Major changes)
   - Update state declarations to use `DeckCardInstance[]`
   - Refactor all deck management callbacks
   - Update drag & drop logic
   - Update quantity calculation helpers
     
     #### **Key Changes:**
     
     **State Declaration:**
     
     ```typescript
     const [mainDeck, setMainDeck] = useState<DeckCardInstance[]>([]);
     const [sideboard, setSideboard] = useState<DeckCardInstance[]>([]);
     ```
     
     **New Helper Functions:**
     
     ```typescript
     // Get current quantities by card ID
     const getDeckQuantity = useCallback((cardId: string): number => {
     return mainDeck.filter(instance => instance.cardId === cardId).length;
     }, [mainDeck]);
     const getSideboardQuantity = useCallback((cardId: string): number => {
     return sideboard.filter(instance => instance.cardId === cardId).length;
     }, [sideboard]);
     const getTotalQuantity = useCallback((cardId: string): number => {
     return getDeckQuantity(cardId) + getSideboardQuantity(cardId);
     }, [getDeckQuantity, getSideboardQuantity]);
     ```
     
     **Refactored Deck Management Callbacks:**
     
     ```typescript
     addToDeck: useCallback((cards: (ScryfallCard | DeckCard)[], quantity = 1) => {
     cards.forEach(card => {
     const totalCopies = getTotalQuantity(card.id);
     const isBasic = isBasicLand(card);
     const maxAllowed = isBasic ? Infinity : 4;
     const canAdd = Math.max(0, maxAllowed - totalCopies);
     const actualQuantity = Math.min(quantity, canAdd);
     ```

// Create individual instances
 const newInstances: DeckCardInstance[] = [];
 for (let i = 0; i < actualQuantity; i++) {
 newInstances.push(scryfallToDeckInstance(card as ScryfallCard, 'deck'));
 }

setMainDeck(prev => [...prev, ...newInstances]);
 });
}, [getTotalQuantity]),
removeFromDeck: useCallback((instances: DeckCardInstance[], quantity = 1) => {
 // Remove specific instances or first N instances of a card
 setMainDeck(prev => {
 // Implementation logic for removing specific instances
 });
}, []),

```
#### **Success Criteria:**
- [ ] Deck state uses instance arrays instead of quantity objects
- [ ] All deck management callbacks work with instances
- [ ] 4-copy limit enforcement works correctly
- [ ] Basic land exception works correctly
- [ ] Drag & drop creates/removes individual instances
### **Phase 3: Selection System Overhaul (60 minutes)**
#### **Files to Modify:**
1. **`src/hooks/useSelection.ts`** (Major refactor)
 - Update to work with instance IDs instead of card IDs
 - Support both collection (ID-based) and deck (instance-based) selection
 - Maintain backward compatibility for collection area
#### **New Selection Interface:**
```typescript
export interface SelectionState {
 selectedInstances: Set<string>; // Instance IDs for deck/sideboard
 selectedCards: Set<string>; // Card IDs for collection
 lastSelectedType: 'card' | 'instance';
 // ... other state
}
export interface SelectionActions {
 selectInstance: (instanceId: string, instance: DeckCardInstance) => void;
 selectCard: (cardId: string, card: ScryfallCard) => void; // Collection only
 isInstanceSelected: (instanceId: string) => boolean;
 isCardSelected: (cardId: string) => boolean;
 // ... other actions
}
```

#### **Key Implementation:**

```typescript
const selectInstance = useCallback((instanceId: string, instance: DeckCardInstance, ctrlKey = false) => {
 setState(prev => {
 if (ctrlKey) {
 // Multi-selection mode
 const newSelected = new Set(prev.selectedInstances);
 if (newSelected.has(instanceId)) {
 newSelected.delete(instanceId);
 } else {
 newSelected.add(instanceId);
 }
 return { ...prev, selectedInstances: newSelected, lastSelectedType: 'instance' };
 } else {
 // Single selection mode
 return { ...prev, selectedInstances: new Set([instanceId]), lastSelectedType: 'instance' };
 }
 });
}, []);
```

#### **Success Criteria:**

- [ ] Individual deck card instances can be selected
- [ ] Collection area selection still works (backward compatibility)
- [ ] Multi-selection works for individual instances
- [ ] Selection state properly distinguishes between areas
  
  ### **Phase 4: UI Component Updates (75 minutes)**
  
  #### **Files to Modify:**
1. **`src/components/DraggableCard.tsx`**
   - Update to handle both card IDs and instance IDs
   - Pass instance ID for deck/sideboard cards
   - Keep card ID for collection cards
2. **`src/components/MTGOLayout.tsx`** (UI integration)
   - Update deck/sideboard rendering to use instances
   - Update quantity displays (count instances)
   - Update selection integration
     
     #### **DraggableCard Changes:**
     
     ```typescript
     interface DraggableCardProps {
     card: ScryfallCard | DeckCardInstance;
     zone: DropZone;
     // Add instance-specific props
     instanceId?: string; // For deck/sideboard cards
     isInstance?: boolean; // Flag to determine behavior
     // ... other props
     }
     // In click handler:
     const handleClick = useCallback((event: React.MouseEvent) => {
     if (isInstance && instanceId) {
     // Use instance-based selection
     onInstanceClick?.(instanceId, card as DeckCardInstance, event);
     } else {
     // Use card-based selection (collection)
     onClick?.(card, event);
     }
     }, [isInstance, instanceId, onInstanceClick, onClick]);
     ```
     
     #### **Deck Rendering Changes:**
     
     ```typescript
     // Render individual instances
     {mainDeck.map((instance) => (
     <DraggableCard
     key={instance.instanceId} // Use instance ID as key
     card={instance}
     zone="deck"
     instanceId={instance.instanceId}
     isInstance={true}
     onClick={handleInstanceClick}
     // ... other props
     />
     ))}
     ```
     
     #### **Success Criteria:**
- [ ] Individual deck card instances render correctly
- [ ] Each instance is selectable independently
- [ ] Collection area behavior unchanged
- [ ] Quantity displays show correct counts
  
  ### **Phase 5: Context Menu & Drag Integration (45 minutes)**
  
  #### **Files to Modify:**
1. **`src/hooks/useContextMenu.ts`**
   - Update to work with both cards and instances
   - Handle instance-specific actions
2. **`src/hooks/useDragAndDrop.ts`** 
- Update to handle instance-based dragging
  - Maintain card-based dragging for collection
    
    #### **Context Menu Changes:**
    
    ```typescript
    // Update callbacks to handle instances
    export interface DeckManagementCallbacks {
    addToDeck: (cards: (ScryfallCard | DeckCard)[], quantity?: number) => void;
    removeFromDeck: (instances: DeckCardInstance[], quantity?: number) => void; // Changed
    // ... other callbacks now use instances for deck operations
    }
    ```
    
    #### **Success Criteria:**

- [ ] Right-click context menus work on individual instances
- [ ] Drag & drop works with individual instances
- [ ] Collection area drag & drop unchanged
  
  ### **Phase 6: Quality Display Improvements (30 minutes)**
  
  #### **Files to Modify:**
1. **`src/components/MTGOLayout.tsx`** (Display logic)
   - Update quantity counters in headers
   - Implement card stacking visualization for duplicates
     
     #### **Enhanced Display Features:**
     
     ```typescript
     // Group instances for display
     const groupedDeckCards = useMemo(() => {
     return groupInstancesByCardId(mainDeck);
     }, [mainDeck]);
     // Render with stacking for duplicates
     {Array.from(groupedDeckCards.entries()).map(([cardId, instances]) => (
     instances.length === 1 ? (
     // Single card - render normally
     <DraggableCard key={instances[0].instanceId} ... />
     ) : (
     // Multiple copies - render stacked with count indicator
     <CardStack key={cardId} instances={instances} ... />
     )
     ))}
     ```
     
     #### **Success Criteria:**
- [ ] Quantity displays accurately count instances
- [ ] Visual improvements for multiple copies
- [ ] Performance optimized for large decks
  
  ## 🧪 Testing Strategy
  
  ### **Unit Tests (Phase by Phase)**
1. **Instance Creation**: Verify unique IDs and proper conversion
2. **Deck Management**: Test add/remove with limits and basic lands
3. **Selection Logic**: Test individual vs. multi-selection
4. **UI Integration**: Test rendering and interaction
   
   ### **Integration Tests (Full Workflow)**
5. **Basic Workflow**: Add cards, select individuals, remove specific copies
6. **Limit Enforcement**: Verify 4-copy total limit works with instances
7. **Cross-Zone Operations**: Move individual instances between zones
8. **Performance**: Test with 60+ card decks for responsiveness
   
   ### **User Acceptance Tests**
9. **Individual Selection**: Click one copy, only that copy selected
10. **Multi-Selection**: Ctrl+click to select multiple individual copies
11. **Context Actions**: Right-click works on individual instances
12. **Drag & Drop**: Drag individual instances between zones
    
    ## 📊 Risk Assessment
    
    ### **High Risk Areas**
13. **State Migration**: Converting existing quantity-based state to instances
14. **Performance**: Large decks with many instances
15. **Backward Compatibility**: Ensuring collection area remains unchanged
    
    ### **Mitigation Strategies**
16. **Gradual Migration**: Implement with feature flags for easy rollback
17. **Performance Monitoring**: Add logging for render performance
18. **Comprehensive Testing**: Test both new and existing functionality
    
    ## 🎯 Success Criteria Summary
    
    ### **Core Functionality**
- [ ] Individual deck card instances can be selected independently
- [ ] 4-copy total limit enforcement works correctly with instances
- [ ] Basic land exception allows unlimited copies
- [ ] Collection area behavior unchanged
  
  ### **User Experience**
- [ ] Clicking one card selects only that card
- [ ] Visual feedback clearly shows individual selection
- [ ] Context menus work on individual instances
- [ ] Drag & drop works with individual instances
  
  ### **Technical Quality**
- [ ] TypeScript compilation succeeds with no errors
- [ ] No performance regressions with large decks
- [ ] Clean separation between collection and deck selection systems
- [ ] Comprehensive error handling and edge case coverage
  
  ## 🚀 Post-Implementation
  
  ### **Documentation Updates**

- Update architecture documentation
- Add instance management patterns to development guide
- Document selection system for future developers
  
  ### **Future Enhancements**
- Card history tracking per instance
- Advanced selection patterns (select all copies of a card)
- Instance-based animations and transitions

---

**Estimated Total Time:** 5-6 hours (2-3 development sessions) 
**Complexity Level:** High - Major architectural change 
**Files Modified:** 6-8 core files 
**Impact:** Resolves critical UX issue affecting core deck building functionality
