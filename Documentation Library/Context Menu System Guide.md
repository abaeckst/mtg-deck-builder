# Context Menu System Guide

**Last Updated:** January 14, 2025 
**Status:** Working with professional zone-aware actions and intelligent positioning 
**Complexity:** Medium-High - Cross-system integration, professional positioning, dynamic action generation, MTGO-authentic styling

## 🎯 System Definition

### Purpose

**What this system does:** Professional context menu system providing zone-aware deck building actions with intelligent positioning, multi-selection support, and comprehensive MTGO-style interaction patterns 
**Why it exists:** Enables efficient deck building through context-sensitive right-click actions, providing professional UX with dynamic action generation based on card location and selection state 
**System boundaries:** Handles right-click event coordination, context menu positioning, action generation, and professional styling; integrates with selection, drag & drop, and data management systems through callback interfaces

### Core Files (Always Work Together)

#### **Context Menu Engine:**

- `useContextMenu.ts` (6,938 bytes) - **CRITICAL:** Zone-aware action generation with comprehensive DeckManagementCallbacks interface, multi-selection support, quantity validation, dynamic labeling
  
  #### **Professional UI Layer:**
- `ContextMenu.tsx` (3,135 bytes) - **PROFESSIONAL:** Intelligent viewport positioning with boundary detection, professional event handling (click-outside + Escape), high z-index strategy
- `ContextMenu.css` (977 bytes) - **MTGO-AUTHENTIC:** Complete professional styling with dark theme integration, hover effects, interaction feedback, typography standards
  
  ### Integration Points
  
  **Receives data from:**
- **Selection System:** Selected cards array for multi-selection operations, selection state coordination for context-aware actions
- **Data Management System:** Card objects (ScryfallCard, DeckCard, DeckCardInstance), zone information, quantity validation through callback interface
- **Drag & Drop System:** Zone information (DropZone type), event timing coordination, interaction state management
  **Provides data to:**
- **Data Management System:** Deck building operations through DeckManagementCallbacks interface (add, remove, move operations)
- **UI Systems:** Professional context menu overlay with MTGO-authentic styling and interaction patterns
- **Event System:** Right-click event handling coordination with proper event prevention and cleanup
  **Coordinates with:**
- **Component Integration System:** Callback orchestration through MTGOLayout central hub, prop distribution coordination
- **Event Management:** Click-outside detection, Escape key handling, professional event cleanup patterns
- **Professional UI Standards:** MTGO theme consistency, z-index management, professional interaction feedback
  
  ## 🔄 Critical Data Flows
  
  ### Primary Flow: Zone-Aware Context Menu Generation & Professional Positioning
  
  ```
  Right-Click Event → useContextMenu.showContextMenu → Event coordinate capture → Zone detection
  ↓
  Context State Update → targetCard + targetZone + selectedCards → Action generation trigger
  ↓
  getContextMenuActions() → Zone-specific logic → Dynamic action generation → Multi-selection awareness
  ↓
  [Collection] Add to deck/sideboard (1 or 4), Fill operations → Professional action labels
  ↓
  [Deck] Add more/Remove/Move to sideboard (with quantity validation) → Context-aware actions
  ↓
  [Sideboard] Add more/Remove/Move to deck (with quantity validation) → Zone-specific behavior
  ```
  
  ### Advanced Flow: Intelligent Positioning & Viewport Boundary Detection
  
  ```
  Context Menu Display → ContextMenu.getAdjustedPosition() → Viewport measurement → Boundary detection
  ↓
  Position Calculation → rect.width/height vs viewport dimensions → Overflow detection → Position adjustment
  ↓
  [X Overflow] adjustedX = viewportWidth - rect.width - 10 → Right edge protection
  ↓
  [Y Overflow] adjustedY = viewportHeight - rect.height - 10 → Bottom edge protection
  ↓
  Minimum Position Enforcement → Math.max(10, adjustedX/Y) → 10px margin guarantee → Fixed positioning
  ```
  
  ### Complex Flow: Multi-Selection Action Generation & Dynamic Labeling
  
  ```
  Action Generation Request → selectedCards.length analysis → Multi-selection detection
  ↓
  [Single Selection] Standard action labels → "Add 1 to Deck", "Remove 1 from Deck"
  ↓
  [Multi-Selection] Dynamic count labels → "Add 3 cards to Deck", "Remove 3 from Deck"
  ↓
  cardsToAct Determination → isMultiSelection ? selectedCards : [targetCard] → Action target selection
  ↓
  Quantity Validation → getDeckQuantity/getSideboardQuantity → Basic land exceptions → Disabled state calculation
  ```
  
  ### Professional Flow: Event Handling & Cross-System Coordination
  
  ```
  Right-Click Detection → preventDefault/stopPropagation → Event coordinate extraction → Context state update
  ↓
  Professional Event Management → Click-outside detection → Escape key handling → Document listener management
  ↓
  Action Execution → onClick callback → Action execution → Auto-close trigger → State cleanup
  ↓
  Cross-System Integration → DeckManagementCallbacks → State updates → UI synchronization
  ```
  
  ### Integration Flow: Callback Interface & State Coordination
  
  ```
  DeckManagementCallbacks Interface → 8 operation functions → External system integration
  ↓
  Add Operations → addToDeck/addToSideboard → Quantity parameter → Multi-card support
  ↓
  Remove Operations → removeFromDeck/removeFromSideboard → Quantity validation → State updates
  ↓
  Move Operations → moveDeckToSideboard/moveSideboardToDeck → Cross-zone transfers → Professional coordination
  ↓
  Query Operations → getDeckQuantity/getSideboardQuantity → Validation support → Disabled state calculation
  ```
  
  ## 🐛 Problem Diagnosis
  
  ### Context Menu Positioning Issues
  
  **"Context menu appearing off-screen or in wrong position"**
- **Root Cause:** Viewport boundary detection failure or position calculation issues
- **Check Files:** `ContextMenu.tsx` (getAdjustedPosition function) → viewport measurement → boundary detection logic
- **Debug Pattern:** Verify getBoundingClientRect() → check viewport dimension calculation → validate position adjustment logic → confirm 10px margin enforcement
  **"Context menu z-index conflicts with other UI elements"**
- **Root Cause:** Z-index strategy insufficient or overlay conflicts
- **Check Files:** `ContextMenu.tsx` (z-index: 9999 strategy) → overlay positioning → fixed positioning coordination
- **Debug Pattern:** Check z-index value effectiveness → verify fixed positioning → validate overlay conflicts → confirm positioning strategy
  
  ### Action Generation & Zone Logic Issues
  
  **"Wrong actions appearing for cards in different zones"**
- **Root Cause:** Zone detection failure or action generation logic issues
- **Check Files:** `useContextMenu.ts` (getContextMenuActions, zone-specific logic) → zone detection → action generation patterns
- **Debug Pattern:** Verify targetZone detection → check zone-specific action logic → validate action generation → confirm label accuracy
  **"Actions disabled when they should be enabled or vice versa"**
- **Root Cause:** Quantity validation failure or disabled state calculation issues
- **Check Files:** `useContextMenu.ts` (quantity validation, getDeckQuantity/getSideboardQuantity) → disabled state logic → basic land exceptions
- **Debug Pattern:** Check quantity validation functions → verify disabled state calculation → validate basic land exceptions → confirm 4-copy limits
  **"Multi-selection not working correctly"**
- **Root Cause:** selectedCards coordination failure or multi-selection logic issues
- **Check Files:** `useContextMenu.ts` (multi-selection logic, dynamic labeling) → selectedCards handling → cardsToAct determination
- **Debug Pattern:** Verify selectedCards array → check multi-selection detection → validate dynamic labeling → confirm cardsToAct logic
  
  ### Event Handling & Professional Interaction Issues
  
  **"Context menu not closing on click-outside or Escape"**
- **Root Cause:** Event listener failure or cleanup issues
- **Check Files:** `ContextMenu.tsx` (event listener management, cleanup) → click-outside detection → Escape key handling
- **Debug Pattern:** Check event listener setup → verify click-outside logic → validate Escape key handling → confirm cleanup execution
  **"Context menu interfering with drag operations"**
- **Root Cause:** Event timing conflicts or coordination issues with drag & drop system
- **Check Files:** `useContextMenu.ts` (event prevention) → drag & drop integration → timing coordination patterns
- **Debug Pattern:** Check preventDefault/stopPropagation → verify drag timing coordination → validate event isolation → confirm cross-system coordination
  
  ### Styling & Professional Appearance Issues
  
  **"Context menu styling not matching MTGO theme"**
- **Root Cause:** CSS styling inconsistencies or theme integration failures
- **Check Files:** `ContextMenu.css` (MTGO theme integration, color coordination) → professional styling patterns
- **Debug Pattern:** Verify MTGO color consistency (#2a2a2a, #555, #0078d4) → check hover effects → validate typography standards → confirm professional appearance
  **"Context menu separator or disabled states not working"**
- **Root Cause:** CSS styling or action configuration issues
- **Check Files:** `ContextMenu.css` (separator styling, disabled states) → `ContextMenu.tsx` (separator rendering, disabled handling)
- **Debug Pattern:** Check separator CSS → verify disabled state styling → validate action configuration → confirm visual feedback
  
  ### Cross-System Integration Issues
  
  **"Deck building actions not executing correctly"**
- **Root Cause:** DeckManagementCallbacks integration failure or callback coordination issues
- **Check Files:** `useContextMenu.ts` (callback interface) → external callback implementation → integration patterns
- **Debug Pattern:** Verify callback interface implementation → check callback execution → validate parameter passing → confirm state updates
  **"Context menu actions not reflecting current deck state"**
- **Root Cause:** Quantity validation failure or state synchronization issues
- **Check Files:** `useContextMenu.ts` (getDeckQuantity/getSideboardQuantity) → state synchronization → validation coordination
- **Debug Pattern:** Check quantity validation functions → verify state synchronization → validate callback coordination → confirm real-time updates
  
  ### Debugging Starting Points
  
  **Positioning issues:** Start with `ContextMenu.tsx` getAdjustedPosition → viewport measurement → boundary detection → position calculation validation 
  **Action generation issues:** Start with `useContextMenu.ts` getContextMenuActions → zone logic → action generation → disabled state validation 
  **Event handling issues:** Start with `ContextMenu.tsx` event listeners → click-outside detection → Escape handling → cleanup validation 
  **Multi-selection issues:** Start with `useContextMenu.ts` selectedCards logic → multi-selection detection → dynamic labeling → cardsToAct determination 
  **Styling issues:** Start with `ContextMenu.css` theme consistency → hover effects → disabled states → professional appearance validation 
  **Integration issues:** Start with `useContextMenu.ts` DeckManagementCallbacks → callback execution → state coordination → cross-system integration
  
  ## 🔧 Architecture Details
  
  ### State Management Pattern
  
  **How state is organized:** Simple useState pattern in useContextMenu with ContextMenuState (coordinates, targetCard, targetZone, selectedCards) coordinated with external DeckManagementCallbacks interface for professional dependency injection 
  **State flow:** Right-click event → coordinate capture → context state update → action generation → UI display → action execution → state cleanup → external callback execution 
  **Key state variables:** Context visibility (visible), coordinates (x, y), target context (targetCard, targetZone), selection state (selectedCards), callback integration (DeckManagementCallbacks)
  
  ### Critical Functions & Hooks
  
  #### **Professional Context Management (useContextMenu.ts):**
  
  **showContextMenu:** Event coordinate capture with preventDefault/stopPropagation, state update with targetCard/targetZone/selectedCards coordination 
  **getContextMenuActions:** Zone-aware action generation with dynamic labeling, multi-selection support, quantity validation, disabled state calculation 
  **hideContextMenu:** Clean state reset to INITIAL_STATE with proper cleanup patterns 
  **DeckManagementCallbacks interface:** 8 operation functions (add/remove/move for deck/sideboard, quantity validation functions) enabling external system integration
  
  #### **Zone-Specific Action Logic:**
  
  **Collection zone actions:** Add 1/4 to deck, Add 1/4 to sideboard, Fill operations for multiple copies with professional labeling 
  **Deck zone actions:** Add more (4-copy limit validation), Remove 1/all copies, Move to sideboard (1/all) with quantity-aware disabled states 
  **Sideboard zone actions:** Add more (4-copy limit validation), Remove 1/all copies, Move to deck (1/all) with quantity-aware disabled states 
  **Multi-selection intelligence:** Dynamic labeling ("Add 1" vs "Add 3 cards"), cardsToAct determination (selectedCards vs [targetCard])
  
  #### **Intelligent Positioning System (ContextMenu.tsx):**
  
  **getAdjustedPosition:** Comprehensive viewport boundary detection with rect.width/height calculation, overflow protection, 10px margin enforcement 
  **Professional event handling:** Click-outside detection with menuRef.contains(), Escape key handling, document listener management with proper cleanup 
  **High z-index strategy:** Fixed z-index: 9999 for reliable overlay positioning independent of complex UI hierarchies 
  **Action execution coordination:** Auto-close on action execution, disabled state handling, professional interaction patterns
  
  #### **Professional MTGO Styling (ContextMenu.css):**
  
  **MTGO theme integration:** #2a2a2a background, #555 borders, professional shadows (0 4px 12px rgba(0,0,0,0.6)) 
  **Professional interaction feedback:** #0078d4 hover (MTGO blue), #106ebe active, #808080 disabled with proper transitions 
  **Typography standards:** Segoe UI font family, 13px sizing, professional spacing (8px 16px padding) 
  **Component structure:** Separator styling, disabled state management, professional button reset
  
  ### Component Hierarchy
  
  ```
  Context Menu System
  ├── useContextMenu Hook (Zone-Aware Action Engine):
  │ ├── ContextMenuState Management:
  │ │ ├── Coordinate Capture (x, y from event.clientX/Y)
  │ │ ├── Target Context (targetCard, targetZone from showContextMenu)
  │ │ ├── Selection Integration (selectedCards array from external systems)
  │ │ └── Visibility State (visible boolean with INITIAL_STATE reset)
  │ ├── DeckManagementCallbacks Interface (8 Operations):
  │ │ ├── Add Operations (addToDeck, addToSideboard with quantity parameters)
  │ │ ├── Remove Operations (removeFromDeck, removeFromSideboard with quantity validation)
  │ │ ├── Move Operations (moveDeckToSideboard, moveSideboardToDeck with cross-zone coordination)
  │ │ └── Query Operations (getDeckQuantity, getSideboardQuantity for validation support)
  │ ├── Zone-Specific Action Generation:
  │ │ ├── Collection Zone Logic (add to deck/sideboard, fill operations with 1/4 quantity options)
  │ │ ├── Deck Zone Logic (add more, remove 1/all, move to sideboard with 4-copy limit validation)
  │ │ ├── Sideboard Zone Logic (add more, remove 1/all, move to deck with quantity validation)
  │ │ └── Multi-Selection Intelligence (dynamic labeling, cardsToAct determination)
  │ ├── Professional Action Labeling:
  │ │ ├── Dynamic Count Labels ("Add 1" vs "Add 3 cards" based on selection)
  │ │ ├── Context-Aware Descriptions ("Fill Deck With This" vs "Fill Deck With These")
  │ │ ├── Quantity Validation (4-copy limits with basic land exceptions)
  │ │ └── Disabled State Calculation (quantity-based with professional UX)
  │ └── Event Coordination:
  │ ├── Right-Click Capture (preventDefault, stopPropagation, coordinate extraction)
  │ ├── Selection Integration (selectedCards array coordination)
  │ ├── Zone Detection (DropZone type integration with drag & drop system)
  │ └── Cross-System Coordination (callback interface execution)
  ├── Professional UI Layer:
  │ ├── ContextMenu Component (Intelligent Positioning + Event Handling):
  │ │ ├── Viewport Boundary Detection:
  │ │ │ ├── Dynamic Position Calculation (getBoundingClientRect coordination)
  │ │ │ ├── Overflow Protection (x/y boundary detection with rect.width/height)
  │ │ │ ├── Position Adjustment (viewportWidth/Height - rect dimensions - 10px margin)
  │ │ │ └── Minimum Position Enforcement (Math.max(10, adjustedX/Y) for margin guarantee)
  │ │ ├── Professional Event Management:
  │ │ │ ├── Click-Outside Detection (menuRef.contains with document listener)
  │ │ │ ├── Escape Key Handling (keydown event with proper cleanup)
  │ │ │ ├── Document Listener Management (addEventListener/removeEventListener coordination)
  │ │ │ └── Action Execution Auto-Close (onClick → action execution → onClose trigger)
  │ │ ├── High Z-Index Strategy:
  │ │ │ ├── Fixed Positioning (position: 'fixed' with calculated coordinates)
  │ │ │ ├── Reliable Overlay (z-index: 9999 for complex UI hierarchy management)
  │ │ │ ├── Professional Layering (independent of scroll state and container hierarchies)
  │ │ │ └── Overlay Coordination (reliable positioning across all UI contexts)
  │ │ └── Action Rendering:
  │ │ ├── Dynamic Action Loop (actions.map with separator support)
  │ │ ├── Disabled State Handling (disabled prop with CSS coordination)
  │ │ ├── Professional Button Reset (width: 100%, text-align: left, cursor management)
  │ │ └── Separator Integration (context-menu-separator with margin coordination)
  │ └── Professional MTGO Styling (ContextMenu.css):
  │ ├── MTGO Theme Integration:
  │ │ ├── Dark Background (#2a2a2a with #555 borders for authentic appearance)
  │ │ ├── Professional Shadows (0 4px 12px rgba(0,0,0,0.6) for depth and premium feel)
  │ │ ├── Authentic Color Palette (#e0e0e0 text, #0078d4 hover, #106ebe active)
  │ │ └── Consistent Styling (4px border-radius, 4px 0 padding for professional appearance)
  │ ├── Professional Interaction Feedback:
  │ │ ├── Hover Effects (#0078d4 background with white text for MTGO consistency)
  │ │ ├── Active States (#106ebe for pressed feedback with professional timing)
  │ │ ├── Disabled Styling (#808080 with cursor: default for clear state indication)
  │ │ └── Smooth Transitions (0.1s ease for professional feel without distraction)
  │ ├── Typography Standards:
  │ │ ├── Font Family (Segoe UI for system consistency and professional appearance)
  │ │ ├── Size Standards (13px for readability and interface consistency)
  │ │ ├── Spacing Coordination (8px 16px padding for comfortable interaction)
  │ │ └── Text Management (white-space: nowrap, user-select: none for professional UX)
  │ └── Component Structure:
  │ ├── Menu Container (min-width: 180px, professional sizing with border-radius)
  │ ├── Item Styling (width: 100%, professional button reset patterns)
  │ ├── Separator Management (1px #555 with 4px margin for visual hierarchy)
  │ └── Professional Layout (display: block, padding coordination, interaction optimization)
  └── Cross-System Integration:
  ├── Selection System Integration (selectedCards array coordination with multi-card operations)
  ├── Drag & Drop Coordination (DropZone type integration with event timing management)
  ├── Data Management Integration (card type support across ScryfallCard/DeckCard/DeckCardInstance)
  ├── Component Integration Coordination (MTGOLayout callback orchestration and prop distribution)
  └── Professional Event Coordination (click-outside detection, Escape handling, cleanup patterns)
  ```
  
  ### Performance Considerations
  
  **Critical paths:** Zone-aware action generation (getContextMenuActions), intelligent positioning (getAdjustedPosition), professional event handling (click-outside + Escape), multi-selection coordination (selectedCards processing), viewport boundary detection (rect calculation), callback interface execution (DeckManagementCallbacks) 
  **Optimization patterns:** Simple useState management, viewport calculation efficiency, event listener cleanup, action generation memoization through useCallback, professional positioning algorithm optimization, MTGO styling performance 
  **Known bottlenecks:** Dynamic action generation complexity, viewport boundary calculations, multi-selection processing overhead, callback interface coordination, event listener management, professional positioning algorithm performance
  
  ## ⚠️ Current System Status
  
  ### Working Functionality
- ✅ **Zone-Aware Action Generation:** Complete context-sensitive actions for collection/deck/sideboard with proper quantity validation and basic land exceptions
- ✅ **Intelligent Positioning:** Comprehensive viewport boundary detection with 10px margin enforcement ensuring menu never appears off-screen
- ✅ **Professional Event Handling:** Click-outside detection and Escape key support with proper document listener cleanup
- ✅ **Multi-Selection Support:** Dynamic action labeling with count-aware descriptions and proper cardsToAct determination
- ✅ **High Z-Index Strategy:** Reliable overlay positioning with z-index: 9999 ensuring menu appears above complex UI hierarchies
- ✅ **MTGO-Authentic Styling:** Complete professional theming with authentic colors, hover effects, and interaction feedback
- ✅ **Callback Interface Integration:** Comprehensive DeckManagementCallbacks with 8 operations enabling professional cross-system coordination
- ✅ **Quantity Validation:** Sophisticated disabled state calculation with 4-copy limits and basic land exceptions
- ✅ **Professional UX Patterns:** Auto-close on action execution, separator support, disabled state management, smooth transitions
- ✅ **Cross-System Integration:** Selection system coordination, drag & drop event timing, data management callback execution
  
  ### Known Issues
- ⚠️ **Simple State Management:** useState pattern works well but could benefit from more sophisticated state management for complex interactions
- ⚠️ **Fixed Z-Index Strategy:** 9999 value works reliably but indicates potential need for systematic z-index management
- ⚠️ **Action Generation Complexity:** getContextMenuActions function handles multiple responsibilities that could benefit from extraction
- ⚠️ **Viewport Calculation Performance:** getAdjustedPosition performs calculations on every render which could be optimized
- ⚠️ **Event Listener Management:** Document listeners added/removed frequently could benefit from optimization
- ⚠️ **Callback Interface Dependency:** Requires comprehensive callback implementation from parent systems
  
  ### Technical Debt
  
  **Priority Items:**
- **P3:** Action generation complexity in getContextMenuActions - multiple zone logic could be extracted to focused functions
- **P3:** Viewport positioning calculation optimization - could benefit from memoization or throttling
- **P3:** Event listener management efficiency - frequent add/remove patterns could be optimized
- **P4:** Fixed z-index strategy - 9999 value works but indicates systematic z-index management need
- **P4:** State management simplicity - useState pattern sufficient but could benefit from useReducer for complex interactions
- **P4:** Callback interface dependency - requires comprehensive implementation from external systems
  
  ### Recent Changes
  
  **Professional implementation:** Zone-aware action generation with intelligent positioning and MTGO-authentic styling 
  **Cross-system integration:** DeckManagementCallbacks interface with comprehensive operation support and validation 
  **Professional UX enhancement:** Multi-selection support with dynamic labeling and sophisticated disabled state management
  
  ## 🚀 Development Patterns
  
  ### Common Change Patterns
  
  #### **Adding Context Menu Actions:**
1. **Start with:** `useContextMenu.ts` → getContextMenuActions function → zone-specific logic implementation
2. **Consider integration:** Action labeling consistency → quantity validation → disabled state calculation → callback coordination
3. **Test by:** Action generation accuracy → multi-selection behavior → disabled state validation → callback execution verification
   
   #### **Adding Professional Positioning Features:**
4. **Start with:** `ContextMenu.tsx` → getAdjustedPosition function → viewport boundary detection → position calculation enhancement
5. **Consider performance:** Positioning calculation efficiency → viewport measurement optimization → boundary detection accuracy
6. **Test by:** Position accuracy across viewport sizes → boundary detection effectiveness → performance monitoring
   
   #### **Adding Professional Styling Features:**
7. **Start with:** `ContextMenu.css` → MTGO theme integration → interaction feedback → professional styling enhancement
8. **Consider consistency:** Color coordination with MTGO theme → typography standards → interaction feedback timing
9. **Test by:** MTGO authenticity validation → interaction feedback responsiveness → professional appearance verification
   
   #### **Adding Cross-System Integration:**
10. **Start with:** `useContextMenu.ts` → DeckManagementCallbacks interface → callback coordination → external system integration
11. **Consider complexity:** Callback interface expansion → state coordination → error handling → integration patterns
12. **Test by:** Callback execution accuracy → state synchronization → cross-system coordination → error handling validation
    
    #### **Adding Event Handling Features:**
13. **Start with:** `ContextMenu.tsx` → event listener management → professional event handling → coordination enhancement
14. **Consider performance:** Event listener efficiency → cleanup patterns → coordination with other systems
15. **Test by:** Event handling accuracy → cleanup verification → cross-system coordination → performance monitoring
    
    #### **Adding Multi-Selection Features:**
16. **Start with:** `useContextMenu.ts` → multi-selection logic → dynamic labeling → cardsToAct determination
17. **Consider UX:** Dynamic labeling accuracy → selection coordination → professional interaction patterns
18. **Test by:** Multi-selection behavior → dynamic labeling verification → selection coordination → UX validation
    
    ### File Modification Order
    
    #### **For action generation changes:** `useContextMenu.ts` (getContextMenuActions) → zone logic implementation → callback coordination → testing validation
    
    #### **For positioning changes:** `ContextMenu.tsx` (getAdjustedPosition) → viewport detection → boundary calculation → position testing
    
    #### **For styling changes:** `ContextMenu.css` (MTGO theme) → interaction feedback → professional appearance → visual validation
    
    #### **For event handling changes:** `ContextMenu.tsx` (event listeners) → coordination patterns → cleanup implementation → event testing
    
    #### **For integration changes:** `useContextMenu.ts` (callback interface) → external coordination → state management → integration testing
    
    ### Testing Strategy
    
    **Critical to test:** Zone-aware action generation accuracy (collection/deck/sideboard), intelligent positioning effectiveness (viewport boundary detection), professional event handling (click-outside + Escape), multi-selection coordination (dynamic labeling), callback interface execution (deck building operations), MTGO styling authenticity (theme consistency) 
    **Integration tests:** Selection system coordination with multi-card operations, drag & drop event timing coordination, data management callback execution, component integration through MTGOLayout, cross-system state synchronization 
    **Performance validation:** Action generation efficiency, positioning calculation performance, event listener management, callback execution timing, styling rendering performance, cross-system coordination efficiency

---

**System Guide Notes:**

- useContextMenu provides professional zone-aware action generation with comprehensive DeckManagementCallbacks interface supporting 8 deck building operations
- ContextMenu component implements intelligent viewport positioning with boundary detection ensuring menu never appears off-screen
- Professional MTGO styling provides authentic dark theme integration with proper hover effects and interaction feedback
- High z-index strategy (9999) ensures reliable overlay positioning across complex UI hierarchies
- Multi-selection support provides dynamic labeling and sophisticated cardsToAct determination for professional UX
- Cross-system integration includes selection coordination, drag & drop event timing, and data management callback execution
- Quantity validation includes 4-copy limits with basic land exceptions and sophisticated disabled state calculation
- Professional event handling includes click-outside detection, Escape key support, and proper document listener cleanup
- Zone-specific action logic provides different action sets for collection/deck/sideboard with context-aware labeling
- Intelligent positioning algorithm prevents off-screen menus with comprehensive viewport boundary detection and 10px margin enforcement
