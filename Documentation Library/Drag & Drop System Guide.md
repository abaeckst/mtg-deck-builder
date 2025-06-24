# Drag & Drop System Guide

**Last Updated:** January 14, 2025 
**Status:** Working with sophisticated interaction system, single handler architecture, and cross-system integration 
**Complexity:** Extremely High - Advanced timing constants, interaction detection, single handler coordination, view mode integration, central callback orchestration

## 🎯 System Definition

### Purpose

**What this system does:** Sophisticated drag & drop interaction system with advanced timing constants, professional visual feedback, view mode coordination, single handler architecture, and comprehensive cross-system orchestration through central callback management 
**Why it exists:** Provides professional MTGO-style drag operations with precise interaction detection, smooth visual feedback, seamless multi-view coordination, and robust integration with selection, layout, and context menu systems 
**System boundaries:** Handles all drag interactions, timing detection, visual feedback, drop zone management, and cross-system coordination; integrates with every major system through sophisticated callback orchestration

### Core Files (Always Work Together)

#### **Central Drag Logic (Extremely Complex):**

- `useDragAndDrop.ts` (18,164 bytes) - **CRITICAL:** Sophisticated timing system with 5 interaction constants, advanced interaction detection, last valid drop zone capture, rapid click handling, global event coordination
- `DraggableCard.tsx` (14,013 bytes) - **COMPLEX:** Interactive wrapper with single handler architecture, conditional FlipCard integration, instance vs card handling, sophisticated mouse interaction management
  
  #### **Drop Zone & Visual System:**
- `DropZone.tsx` (8,934 bytes) - **ENHANCED:** Professional drop zones with 10px buffer zones, fast drag detection, global mouse tracking, centered visual feedback, no-red policy
- `DragPreview.tsx` (3,613 bytes) - **VISUAL:** 3x scaled preview with card stacking, count indicators, color-coded feedback, professional positioning
- `DragAndDropStyles.css` (507 bytes) - **MINIMAL:** Performance-optimized animations with subtle pulse and float effects
  
  #### **View Mode Integration:**
- `PileView.tsx` (13,787 bytes) - **COORDINATION:** Pile-specific drag handling with manual card movement between columns, performance optimization, state persistence
- `ListView.tsx` (17,648 bytes) - **COORDINATION:** Row-based drag operations with quantity management, column coordination, multi-selection support
  
  #### **Selection System Integration:**
- `useSelection.ts` (14,927 bytes) - **DUAL SYSTEM:** Instance vs card selection with mutual exclusion, drag rectangle support, legacy compatibility, object storage coordination
  
  #### **Central Orchestration:**
- `MTGOLayout.tsx` (28,194 bytes) - **HUB:** Central coordination with enhanced handler distribution, multi-hook integration, sophisticated callback orchestration, deck state management
  
  ### Integration Points
  
  **Receives data from:**
- **Selection System:** useSelection.ts provides dual selection state (instances vs cards) with mutual exclusion and drag rectangle coordination
- **Layout System:** View mode state, panel dimensions, responsive behavior triggers affecting drag behavior across different display modes
- **Card Display System:** Card data, FlipCard integration, display context requiring conditional rendering and interaction coordination
- **Device Detection:** Capability detection for advanced interface support and interaction optimization
  **Provides data to:**
- **All View Systems:** Drag state, interaction feedback, drop zone validation through sophisticated callback distribution
- **Context Menu System:** Right-click coordination with drag state prevention and interaction timing management
- **Selection System:** Multi-card drag operations with proper selection type handling (card vs instance)
- **Layout System:** Drop feedback requiring responsive adaptation and visual state coordination
  **Coordinates with:**
- **FlipCard System:** Event isolation preventing drag interference with 3D animations and conditional rendering integration
- **Performance System:** requestAnimationFrame coordination, global event handling, timer management, device detection throttling
- **State Management:** Complex multi-system state coordination through MTGOLayout central hub
- **All Major Systems:** Through comprehensive callback orchestration and sophisticated integration patterns
  
  ## 🔄 Critical Data Flows
  
  ### Primary Flow: Sophisticated Interaction Detection & Single Handler Architecture
  
  ```
  Mouse Down → Enhanced Detection (event.detail, timing analysis) → Single Handler Decision Logic
  ↓
  [Double-click] → Enhanced handler ONLY (onEnhancedDoubleClick) → Card movement → 300ms drag prevention
  ↓
  [Single click] → Instance/card routing → Selection system coordination → Visual feedback
  ↓ 
  [Drag initiation] → 150ms minimum hold + 5px movement threshold → Global tracking → Drop coordination
  ↓
  Timer Management → DRAG_START_DELAY, CLICK_TO_DRAG_PROTECTION → Sophisticated event prevention
  ```
  
  **Critical Timing Constants:**
- **DOUBLE_CLICK_MAX_INTERVAL:** 500ms for rapid click detection
- **RAPID_CLICK_MAX_INTERVAL:** 800ms for multi-click sequences 
- **DRAG_START_DELAY:** 150ms minimum hold before drag initiation
- **DRAG_MOVEMENT_THRESHOLD:** 5px movement required for intentional drag
- **CLICK_TO_DRAG_PROTECTION:** 300ms post-click drag prevention
  
  ### Advanced Flow: Last Valid Drop Zone Capture & Coordination
  
  ```
  Drop Zone Entry → lastValidDropZoneRef capture → State coordination → Visual feedback
  ↓
  Fast Exit Detection → 30-50ms delay tolerance → Buffer zone calculation → Zone validation
  ↓
  Drop Operation → Last valid zone fallback → Card movement execution → State cleanup
  ↓
  Global Mouse Tracking → 10px buffer zones → Fast entry/exit detection → Professional feedback
  ```
  
  ### Complex Flow: View Mode Coordination & Integration
  
  ```
  [Card View] DraggableCard → Conditional FlipCard rendering → Instance vs card detection → Selection coordination
  ↓
  [Pile View] PileView → Manual column movement → handleManualMove() → State persistence → Performance optimization
  ↓
  [List View] ListView → Row-based drag → Quantity management → Column coordination → Multi-selection support
  ↓
  Cross-View Coordination → MTGOLayout orchestration → Enhanced handler distribution → Callback management
  ```
  
  ### Sophisticated Flow: Dual Selection System Integration
  
  ```
  Card Selection (Collection) → selectCard() → Clear instances → Card-based drag operations
  ↓
  Instance Selection (Deck/Sideboard) → selectInstance() → Clear cards → Instance-based drag operations
  ↓
  Mutual Exclusion → selectedCards vs selectedInstances → Legacy compatibility (isSelected) → Object storage (refs)
  ↓
  Drag Rectangle → startDragSelection → coordinate tracking → endDragSelection → Type-aware selection
  ```
  
  ### Performance Flow: Global Event Handling & Optimization
  
  ```
  Mouse Events → Global listeners (passive) → requestAnimationFrame → Smooth preview updates
  ↓
  Timer Management → Cleanup on unmount → Memory leak prevention → Performance optimization
  ↓
  Event Isolation → stopPropagation coordination → FlipCard integration → Multi-system timing
  ↓
  Memoization → PileView column rendering → ListView row operations → Selection state optimization
  ```
  
  ### Integration Flow: Central Callback Orchestration (MTGOLayout) - Single Handler Architecture
  
  ```
  Double-Click Operations → onEnhancedDoubleClick ONLY → createDeckInstance utility → Deck state updates
  ↓
  Drag Operations → onCardMove callback → Single card vs selection logic → State coordination
  ↓
  Multi-Hook Integration → useLayout + useSelection + useDragAndDrop + useCards + others → State synchronization
  ↓
  Enhanced Handler Distribution → Clean prop distribution → Single source of truth → Cross-system integration
  ```
  
  ### Advanced Flow: Professional Visual Feedback & 3x Scaling
  
  ```
  Drag Start → DragPreview creation → 3x scale transform → Card stacking (max 3 visible)
  ↓
  Position Calculation → Cursor offset (10px, -20px) → transformOrigin: 'top left' → Professional positioning
  ↓
  Visual State → Green/red borders → Grayscale filters → Count indicators → "+X more" labels
  ↓
  Drop Zone Feedback → Centered indicators → Subtle pulse animation → NO RED policy → Green valid drops only
  ```
  
  ## 🐛 Problem Diagnosis
  
  ### Single Handler Architecture Issues
  
  **"Double-click operations executing multiple times or not working"**
- **Root Cause:** Handler architecture confusion or enhanced handler prop flow failure
- **Check Files:** `useDragAndDrop.ts` (handleDoubleClick, enhanced handler only) → `DraggableCard.tsx` (single handler consumption) → component prop flow validation
- **Debug Pattern:** Verify enhanced handler prop flow → check single handler architecture → validate timing constants coordination → confirm cross-system integration
  **"Legacy handler references or dual execution paths"**
- **Root Cause:** Incomplete dual handler elimination or prop flow issues
- **Check Files:** Component interfaces → MTGOLayout prop distribution → legacy handler removal validation
- **Debug Pattern:** Search for onCardDoubleClick references → verify enhanced handler only → validate prop flow → confirm single execution
  
  ### Sophisticated Timing & Interaction Issues
  
  **"Double-click not working or triggering drag instead"**
- **Root Cause:** Enhanced timing detection failing or timing constant conflicts
- **Check Files:** `useDragAndDrop.ts` (handleDoubleClick, timing constants) → `DraggableCard.tsx` (mouseDown detection, event.detail logic) → timing coordination validation
- **Debug Pattern:** Verify event.detail detection → check timing constants (500ms, 800ms, 300ms) → validate preventDragUntil logic → confirm enhanced handler coordination
  **"Drag starting too early or not starting at all"**
- **Root Cause:** Movement threshold or hold time detection failures
- **Check Files:** `useDragAndDrop.ts` (DRAG_START_DELAY 150ms, DRAG_MOVEMENT_THRESHOLD 5px) → early movement detection → timer management
- **Debug Pattern:** Check 150ms minimum hold time → verify 5px movement threshold → validate timer cleanup → confirm global event listeners
  **"Click protection not working after double-click"**
- **Root Cause:** CLICK_TO_DRAG_PROTECTION timing or preventDragUntil logic failure
- **Check Files:** `useDragAndDrop.ts` (preventDragUntil management, 300ms protection) → `DraggableCard.tsx` (preventNextClick coordination)
- **Debug Pattern:** Verify 300ms protection period → check preventDragUntil state → validate timing coordination → confirm click prevention logic
  
  ### Drop Zone & Visual Feedback Issues
  
  **"Drop zones not detecting drag or showing wrong feedback"**
- **Root Cause:** Fast drag detection or buffer zone calculation failure
- **Check Files:** `DropZone.tsx` (global mouse tracking, 10px buffer zones) → fast entry/exit detection → timeout management
- **Debug Pattern:** Verify 10px buffer zone calculation → check global mouse move listeners → validate 30-50ms delay tolerance → confirm zone boundary detection
  **"Drag preview not showing or wrong size/position"**
- **Root Cause:** 3x scaling or positioning calculation issues
- **Check Files:** `DragPreview.tsx` (3x scale transform, cursor offset) → `useDragAndDrop.ts` (preview state management) → coordinate calculation
- **Debug Pattern:** Check 3x scale transform application → verify cursor offset (10px, -20px) → validate transformOrigin: 'top left' → confirm preview state coordination
  **"Drop indicators not appearing or wrong colors"**
- **Root Cause:** NO RED policy not working or canDrop state coordination failure
- **Check Files:** `DropZone.tsx` (green feedback only, centered indicators) → canDrop state → visual feedback logic
- **Debug Pattern:** Verify NO RED policy implementation → check canDrop state propagation → validate centered indicator positioning → confirm green-only feedback
  
  ### View Mode Coordination Issues
  
  **"Drag not working correctly in pile view"**
- **Root Cause:** Manual column movement or pile-specific coordination failure
- **Check Files:** `PileView.tsx` (handleManualMove, pass-through handlers) → `PileColumn.tsx` → drag coordination patterns
- **Debug Pattern:** Check handleManualMove implementation → verify pass-through handler coordination → validate manual arrangements state → confirm performance optimization impact
  **"List view drag not selecting multiple rows"**
- **Root Cause:** Row-based drag or multi-selection coordination failure
- **Check Files:** `ListView.tsx` (handleRowDragStart, selected cards coordination) → selection state integration → quantity management
- **Debug Pattern:** Verify handleRowDragStart logic → check selected cards coordination → validate left mouse button detection → confirm multi-selection support
  **"View mode switching breaking drag state"**
- **Root Cause:** Cross-view coordination or state preservation failure
- **Check Files:** `MTGOLayout.tsx` (view mode coordination) → state preservation → drag state cleanup → view transition handling
- **Debug Pattern:** Check view mode state coordination → verify drag state preservation → validate state cleanup → confirm transition handling
  
  ### Dual Selection System Issues
  
  **"Selection not working or wrong type selected"**
- **Root Cause:** Mutual exclusion or card vs instance detection failure
- **Check Files:** `useSelection.ts` (selectedCards vs selectedInstances, mutual exclusion) → `DraggableCard.tsx` (instance vs card routing)
- **Debug Pattern:** Verify mutual exclusion logic → check card vs instance detection → validate selection type routing → confirm legacy compatibility (isSelected)
  **"Drag rectangle selection not working"**
- **Root Cause:** Coordinate tracking or selection completion failure
- **Check Files:** `useSelection.ts` (startDragSelection, updateDragSelection, endDragSelection) → coordinate management → type-aware selection
- **Debug Pattern:** Check coordinate tracking logic → verify drag rectangle calculation → validate endDragSelection type handling → confirm selection state updates
  **"Context menu interfering with drag operations"**
- **Root Cause:** Event coordination or interaction timing conflicts
- **Check Files:** `useSelection.ts` (object storage in refs) → `MTGOLayout.tsx` (context menu integration) → event timing coordination
- **Debug Pattern:** Verify context menu state coordination → check event timing conflicts → validate object storage in refs → confirm interaction isolation
  
  ### Central Orchestration Issues
  
  **"Enhanced handler not firing or wrong data passed"**
- **Root Cause:** MTGOLayout enhanced handler distribution or prop flow failure
- **Check Files:** `MTGOLayout.tsx` (enhanced handler distribution, callback management) → multi-hook integration → state coordination
- **Debug Pattern:** Check enhanced handler prop distribution → verify multi-hook integration → validate state coordination → confirm callback orchestration
  **"Cross-system integration broken"**
- **Root Cause:** Multi-hook coordination or state synchronization failure
- **Check Files:** `MTGOLayout.tsx` (useLayout + useSelection + useDragAndDrop + others) → state synchronization patterns → integration points
- **Debug Pattern:** Verify multi-hook integration → check state synchronization → validate integration point coordination → confirm callback orchestration
  
  ### Performance & Memory Issues
  
  **"Drag operations causing performance issues"**
- **Root Cause:** Global event handling or timer management problems
- **Check Files:** `useDragAndDrop.ts` (global listeners, timer cleanup) → `PileView.tsx` (memoization) → `ListView.tsx` (column coordination)
- **Debug Pattern:** Check global event listener management → verify timer cleanup → validate memoization effectiveness → confirm performance optimization patterns
  **"Memory leaks or timer issues"**
- **Root Cause:** Timer cleanup or event listener removal failure
- **Check Files:** `useDragAndDrop.ts` (useEffect cleanup, timer management) → global listener cleanup → memory management
- **Debug Pattern:** Verify useEffect cleanup → check timer cancellation → validate global listener removal → confirm memory leak prevention
  
  ### Debugging Starting Points
  
  **Single handler architecture issues:** Start with component prop flow → `MTGOLayout.tsx` enhanced handler distribution → `DraggableCard.tsx` consumption validation 
  **Timing and interaction issues:** Start with `useDragAndDrop.ts` timing constants → `DraggableCard.tsx` interaction detection → timing coordination validation 
  **Drop zone and visual issues:** Start with `DropZone.tsx` buffer zones → `DragPreview.tsx` scaling logic → visual feedback coordination 
  **View mode coordination issues:** Start with `PileView.tsx`/`ListView.tsx` view-specific handling → `MTGOLayout.tsx` coordination → callback orchestration 
  **Selection system issues:** Start with `useSelection.ts` dual selection logic → `DraggableCard.tsx` instance vs card routing → mutual exclusion validation 
  **Central orchestration issues:** Start with `MTGOLayout.tsx` multi-hook integration → enhanced handler distribution → state synchronization patterns 
  **Performance issues:** Start with `useDragAndDrop.ts` global event handling → view component memoization → timer management verification 
  **FlipCard integration issues:** Start with `DraggableCard.tsx` conditional rendering → `FlipCard.tsx` event isolation → advanced event coordination 
  **Context menu conflicts:** Start with `useSelection.ts` object storage → `MTGOLayout.tsx` context integration → event timing coordination
  
  ## 🔧 Architecture Details
  
  ### State Management Pattern
  
  **How state is organized:** Sophisticated multi-layer coordination through useDragAndDrop (interaction state), useSelection (dual selection with mutual exclusion), view components (view-specific handling), and MTGOLayout (central orchestration with single handler architecture) with advanced timing management and cross-system integration 
  **State flow:** useDragAndDrop manages interaction timing → useSelection coordinates dual selection → View components handle mode-specific behavior → MTGOLayout orchestrates enhanced handlers → Cross-system integration through clean prop distribution 
  **Key state variables:** dragState (interaction), selectedCards/selectedInstances (dual selection), lastValidDropZoneRef (drop coordination), timing refs (interaction management), manual arrangements (view-specific), enhanced handler coordination (central hub)
  
  ### Critical Functions & Hooks
  
  #### **Sophisticated Timing System (useDragAndDrop.ts):**
  
  **Enhanced interaction tracking:** Complex interactionRef managing click sequences, drag timing, movement detection, and event prevention with 5 critical timing constants 
  **Last valid drop zone capture:** lastValidDropZoneRef prevents drop failures through advanced drop zone management and coordinate fallback logic 
  **Rapid click detection:** Enhanced sequence handling for multiple quick operations with timing analysis and click counting coordination 
  **Global event coordination:** Document-level mouse tracking with passive listeners, requestAnimationFrame optimization, and timer cleanup management 
  **Single handler architecture:** handleDoubleClick as single source of truth for all double-click operations across the application
  
  #### **Professional Visual Feedback (DragPreview.tsx + DropZone.tsx):**
  
  **3x Scale Transform:** `transform: 'rotate(-5deg) scale(3)'` with `transformOrigin: 'top left'` for professional drag preview positioning 
  **Smart Card Stacking:** Max 3 visible cards with 2px offsets, rotation effects, count indicators, and "+X more" labels for large selections 
  **NO RED Policy:** Green feedback only for valid drops (`rgba(16, 185, 129, 0.15)`), neutral styling for invalid zones, centered drop indicators 
  **Fast Drag Detection:** 10px buffer zones, global mouse tracking, 30-50ms delay tolerance for rapid movements, enhanced boundary detection 
  **Professional Animations:** Subtle pulse effects, hardware-accelerated transitions, performance-optimized keyframes
  
  #### **View Mode Coordination:**
  
  **PileView Integration:** handleManualMove() for column-based card organization, performance optimization through memoized column rendering, manual arrangement state persistence 
  **ListView Integration:** handleRowDragStart() with quantity management, multi-selection support, column coordination during drag operations 
  **Cross-View State Preservation:** Drag state maintained across view mode transitions, view-specific optimization patterns, responsive drag behavior
  
  #### **Dual Selection System Integration (useSelection.ts):**
  
  **Mutual Exclusion Architecture:** selectedCards vs selectedInstances Sets with automatic clearing, type-aware selection logic, legacy compatibility through isSelected() 
  **Drag Rectangle Support:** startDragSelection → coordinate tracking → endDragSelection with type-aware selection completion 
  **Object Storage Coordination:** Ref-based storage for context menu operations, selection object access, memory management patterns 
  **Advanced Selection Logic:** Multi-selection with Ctrl key support, single vs multiple mode detection, selection type routing
  
  #### **Central Callback Orchestration (MTGOLayout.tsx) - Single Handler Architecture:**
  
  **Enhanced Handler Distribution:** onEnhancedDoubleClick distributed to all components, onCardMove coordination, drag state management, unified callback patterns 
  **Multi-Hook Integration:** useLayout + useSelection + useResize + useDragAndDrop + useContextMenu + useCards + useSorting + useCardSizing coordination 
  **Sophisticated Callback Management:** createDeckInstance utility, deck state management, enhanced handler coordination, context menu integration 
  **State Synchronization:** Cross-system state management, clean prop flow coordination, single handler orchestration patterns
  
  #### **Advanced Integration Patterns:**
  
  **FlipCard Coordination:** Conditional rendering in DraggableCard based on card_faces detection, event isolation through stopPropagation, 3D animation integration 
  **Performance Optimization:** requestAnimationFrame for smooth updates, memoized rendering in view components, global event passive listeners, timer cleanup patterns 
  **Device Detection Integration:** Advanced interface capability detection, responsive drag behavior, performance adaptation patterns
  
  ### Component Hierarchy
  
  ```
  useDragAndDrop (Sophisticated Timing Engine + Single Handler Architecture)
  ├── Interaction Detection System:
  │ ├── 5 Critical Timing Constants (DOUBLE_CLICK_MAX_INTERVAL: 500ms, RAPID_CLICK_MAX_INTERVAL: 800ms, 
  │ │ DRAG_START_DELAY: 150ms, DRAG_MOVEMENT_THRESHOLD: 5px, CLICK_TO_DRAG_PROTECTION: 300ms)
  │ ├── Enhanced Interaction Tracking (lastClickTime, clickCount, mouseDownTime, mouseDownPosition, isDragInitiated, preventNextClick, preventDragUntil)
  │ ├── Movement-Based Drag Initiation (5px threshold + 150ms minimum hold with early movement detection)
  │ ├── Global Mouse Event Handling (document listeners, passive optimization, requestAnimationFrame coordination)
  │ ├── Last Valid Drop Zone Capture (lastValidDropZoneRef fallback preventing drop failures)
  │ └── Single Handler Architecture (handleDoubleClick as single source of truth for all double-click operations)
  ├── Professional Visual Feedback Layer:
  │ ├── DragPreview.tsx (3x Scale Transform + Card Stacking)
  │ │ ├── 3x Scale: transform: 'rotate(-5deg) scale(3)' with transformOrigin: 'top left'
  │ │ ├── Smart Card Stacking (max 3 visible, 2px offsets, rotation effects)
  │ │ ├── Count Indicators (circular badges, "+X more" labels)
  │ │ └── Color-Coded Feedback (green/red borders, grayscale filters based on canDrop)
  │ ├── DropZone.tsx (Enhanced Detection + NO RED Policy)
  │ │ ├── 10px Buffer Zones (easier targeting during fast drag operations)
  │ │ ├── Global Mouse Tracking (fast entry/exit detection beyond component boundaries)
  │ │ ├── 30-50ms Delay Tolerance (rapid movement tolerance)
  │ │ ├── Centered Drop Indicators (position: absolute, top: 50%, left: 50%, transform: translate(-50%, -50%))
  │ │ ├── NO RED Policy (green feedback only: rgba(16, 185, 129, 0.15), neutral for invalid)
  │ │ └── Subtle Pulse Animation (professional feedback without distraction)
  │ └── DragAndDropStyles.css (Performance-Optimized Animations)
  │ ├── dropIndicatorPulse keyframe (scale and opacity coordination)
  │ └── dragPreviewFloat keyframe (subtle vertical movement)
  ├── View Mode Coordination Layer:
  │ ├── DraggableCard.tsx (Interactive Wrapper + Single Handler Architecture)
  │ │ ├── Single Handler Consumption (onEnhancedDoubleClick ONLY, no legacy handlers)
  │ │ ├── Enhanced Double-Click Detection (event.detail >= 2 immediate detection in mouseDown)
  │ │ ├── Conditional FlipCard Integration (double-faced card detection → FlipCard vs MagicCard rendering)
  │ │ ├── Instance vs Card Handling (cardIsInstance detection, dual click routing)
  │ │ ├── Advanced Interaction Management (mouseDownTime, mouseDownPosition, hasMoved, isDoubleClick, preventNextClick)
  │ │ ├── Multi-Selection Indicator (count badges, animation for 3+ selection)
  │ │ └── Enhanced Event Coordination (sophisticated preventDefault/stopPropagation management)
  │ ├── PileView.tsx (Column-Based Manual Movement)
  │ │ ├── Manual Arrangements State (Map<cardId, columnId> persistence)
  │ │ ├── handleManualMove() (card movement between columns)
  │ │ ├── Performance Optimization (memoized column rendering, organizeByX() functions)
  │ │ ├── Pass-Through Handlers (all drag handlers to PileColumn components)
  │ │ └── Empty Column Management (manual drop target with isEmpty flag)
  │ ├── ListView.tsx (Row-Based Drag + Quantity Management)
  │ │ ├── handleRowDragStart() (left mouse detection, multi-selection support)
  │ │ ├── Quantity Management Integration (instance vs DeckCard quantity handling)
  │ │ ├── Column Coordination (resizable columns maintained during drag)
  │ │ ├── Click-Outside Detection (doesn't interfere with drag events)
  │ │ └── Sort Operations (coordinated with drag state preservation)
  │ └── Cross-View State Preservation (drag state maintained across view transitions)
  ├── Dual Selection System Integration:
  │ ├── useSelection.ts (Mutual Exclusion Architecture)
  │ │ ├── Dual Selection Sets (selectedInstances: Set<string>, selectedCards: Set<string>)
  │ │ ├── Mutual Exclusion Logic (instances clear cards, cards clear instances)
  │ │ ├── Type-Aware Selection (selectInstance vs selectCard with proper object storage)
  │ │ ├── Legacy Compatibility (isSelected() checks both sets)
  │ │ ├── Drag Rectangle Support (startDragSelection → coordinate tracking → endDragSelection)
  │ │ ├── Object Storage (selectedCardsRef, selectedInstancesRef for context menu operations)
  │ │ └── Keyboard Shortcuts (Escape to clear selection)
  │ └── Selection Integration Patterns (card vs instance routing in DraggableCard)
  ├── Central Coordination Hub - Single Handler Architecture:
  │ ├── MTGOLayout.tsx (Enhanced Handler Distribution + Multi-Hook Integration)
  │ │ ├── Multi-Hook Coordination:
  │ │ │ ├── useLayout (unified state, panel dimensions, view mode coordination)
  │ │ │ ├── useSelection (dual selection management)
  │ │ │ ├── useResize (container stabilization, CSS coordination)
  │ │ │ ├── useDragAndDrop (sophisticated interaction system)
  │ │ │ ├── useContextMenu (right-click coordination)
  │ │ │ ├── useCards (data management, filter coordination)
  │ │ │ ├── useSorting (sort criteria coordination)
  │ │ │ └── useCardSizing (card scaling coordination)
  │ │ ├── Single Handler Architecture Distribution:
  │ │ │ ├── Enhanced Handler (onEnhancedDoubleClick to all components)
  │ │ │ ├── Drag Coordination (onDragStart, onDragEnter, onDragLeave, canDropInZone)
  │ │ │ ├── State Management (dragState, isSelected, selectedCards, clearSelection)
  │ │ │ ├── Utility Functions (getSelectedCardObjects, getTotalCopies, quantity management)
  │ │ │ └── Clean Prop Distribution (eliminated legacy handler proliferation)
  │ │ ├── Sophisticated Callback Management:
  │ │ │ ├── createDeckInstance() (pure instance creation utility)
  │ │ │ ├── onCardMove() (comprehensive card movement logic)
  │ │ │ ├── Deck State Management (mainDeck, sideboard state coordination)
  │ │ │ └── Context Menu Integration (deckManagementCallbacks)
  │ │ ├── State Synchronization (cross-system state management)
  │ │ └── Performance Coordination (callback memoization, state optimization)
  │ └── Cross-System Integration (FlipCard, Layout, Context Menu, Device Detection)
  └── Advanced Integration Patterns:
  ├── FlipCard Event Isolation (conditional rendering, stopPropagation coordination)
  ├── Context Menu Timing (interaction coordination, state management)
  ├── Performance Optimization (requestAnimationFrame, global listeners, timer cleanup)
  ├── Device Detection Integration (capability-based behavior, responsive patterns)
  ├── Memory Management (timer cleanup, event listener removal, ref management)
  └── Single Handler Architecture (enhanced handler as single source of truth across all systems)
  ```
  
  ### Performance Considerations
  
  **Critical paths:** Sophisticated timing system (5 constants coordination), global event handling (passive listeners), dual selection coordination (mutual exclusion), view mode integration (memoized rendering), central orchestration (enhanced handler distribution), visual feedback system (3x scaling + requestAnimationFrame), drop zone detection (10px buffers + global tracking), cross-system integration (multi-hook coordination) 
  **Optimization patterns:** requestAnimationFrame for smooth drag updates, passive event listeners for performance, memoized column rendering in PileView, timer cleanup and memory management, ref-based object storage for context menu, sophisticated interaction timing coordination, hardware-accelerated animations, global mouse tracking optimization, view-specific performance patterns, single handler architecture eliminating duplicate processing 
  **Known bottlenecks:** useDragAndDrop.ts complexity (18,164 bytes with sophisticated timing), MTGOLayout.tsx orchestration overhead (28,194 bytes with enhanced handler distribution), useSelection.ts dual system coordination (14,927 bytes), global event handling performance, multi-hook integration complexity, cross-system state synchronization overhead, advanced interaction detection complexity, sophisticated callback orchestration patterns
  
  ## ⚠️ Current System Status
  
  ### Working Functionality
- ✅ **Single Handler Architecture:** Complete elimination of dual handler patterns with enhanced handler as single source of truth for all double-click operations
- ✅ **Sophisticated Timing System:** 5 critical timing constants providing professional interaction detection with enhanced double-click handling and drag prevention
- ✅ **Professional Visual Feedback:** 3x scaled drag preview with card stacking, color-coded feedback, and centered drop indicators following NO RED policy
- ✅ **Advanced Drop Zone Detection:** 10px buffer zones with global mouse tracking, fast entry/exit detection, and 30-50ms delay tolerance
- ✅ **Last Valid Drop Zone Capture:** lastValidDropZoneRef preventing drop failures through sophisticated fallback logic and coordinate management
- ✅ **Conditional FlipCard Integration:** Smart double-faced card detection with event isolation and seamless 3D animation coordination
- ✅ **View Mode Coordination:** Different drag handling for card/pile/list views with manual arrangements, column management, and row-based operations
- ✅ **Dual Selection System:** Mutual exclusion between card and instance selection with drag rectangle support and legacy compatibility
- ✅ **Central Callback Orchestration:** MTGOLayout distributing enhanced handlers with multi-hook integration and sophisticated state synchronization
- ✅ **Enhanced Interaction Detection:** Movement-based drag initiation (5px threshold + 150ms hold) with global event coordination
- ✅ **Performance Optimization:** requestAnimationFrame updates, passive listeners, memoized rendering, timer cleanup, memory management
- ✅ **Cross-System Integration:** Seamless coordination with FlipCard, selection, layout, context menu, and device detection systems
- ✅ **Advanced Event Management:** Global mouse tracking, keyboard shortcuts (Escape), sophisticated event prevention and timing
- ✅ **Technical Debt Resolution:** Eliminated callback proliferation (P2) through single handler architecture and clean prop distribution
  
  ### Known Issues
- ⚠️ **useDragAndDrop.ts Complexity:** 18,164 bytes with extremely sophisticated timing system and interaction detection creating maintenance complexity
- ⚠️ **MTGOLayout.tsx Orchestration Overhead:** 28,194 bytes with enhanced handler distribution and multi-hook coordination creating performance considerations
- ⚠️ **useSelection.ts Dual System Complexity:** 14,927 bytes with mutual exclusion logic and advanced selection patterns creating architectural complexity
- ⚠️ **Global Event Handling Performance:** Document-level mouse tracking and passive listeners requiring careful memory management
- ⚠️ **Timing Constant Coordination:** 5 critical timing values requiring precise coordination across multiple interaction types
- ⚠️ **Cross-System State Synchronization:** Complex multi-system coordination requiring sophisticated callback orchestration
- ⚠️ **View Mode Integration Complexity:** Different drag behavior across card/pile/list views requiring view-specific optimization
- ⚠️ **Advanced Interaction Detection Overhead:** Sophisticated timing and movement detection creating CPU overhead during interaction
- ⚠️ **Memory Management Requirements:** Timer cleanup, event listener removal, and ref management requiring careful lifecycle handling
  
  ### Technical Debt
  
  **Priority Items:**
- **P2:** useDragAndDrop.ts size and complexity (18,164 bytes) - extremely sophisticated timing system could benefit from extraction or simplification
- **P2:** MTGOLayout.tsx orchestration complexity (28,194 bytes) - enhanced handler distribution and multi-hook coordination creates maintenance overhead
- **P2:** useSelection.ts dual system complexity (14,927 bytes) - mutual exclusion and advanced patterns could benefit from architectural simplification
- **P2:** Global event handling performance - document-level tracking and passive listeners require ongoing optimization monitoring
- **P3:** Timing constant coordination complexity - 5 critical values requiring precise interaction across multiple systems
- **P3:** Cross-system integration complexity - sophisticated multi-system coordination requiring careful maintenance
- **P3:** View mode specific optimization - different drag behavior patterns across card/pile/list views creating code duplication
- **P3:** Advanced interaction detection overhead - sophisticated timing and movement detection creating performance considerations
- **P4:** Memory management complexity - timer cleanup, event listener removal, and ref management requiring ongoing vigilance
- **P4:** Central orchestration scaling - enhanced handler distribution pattern may require optimization with additional systems
  
  ### Recent Changes
  
  **✅ Single Handler Architecture Implementation (P2 Resolution):** Complete elimination of dual handler patterns with enhanced handler as single source of truth 
  **✅ Enhanced timing system:** 5 critical timing constants with sophisticated interaction detection and enhanced double-click handling 
  **✅ Professional visual feedback:** 3x scaling with NO RED policy, centered indicators, and performance-optimized animations 
  **✅ Cross-system integration:** Comprehensive coordination with FlipCard, selection, layout, and context menu systems through central orchestration 
  **✅ Technical Debt Resolution:** Eliminated callback proliferation through systematic prop flow cleanup and single handler architecture
  
  ## 🚀 Development Patterns
  
  ### Common Change Patterns
  
  #### **Eliminating Dual Handler Anti-Patterns:**
1. **Start with:** Component interface analysis → identify dual handler paths → systematic elimination planning
2. **Consider integration:** Leverage existing sophisticated timing system → preserve cross-system coordination → maintain performance optimization
3. **Test by:** Verify single execution per operation → validate timing constants preservation → confirm cross-system integration integrity
   
   #### **Adding Single Handler Architecture Features:**
4. **Start with:** `useDragAndDrop.ts` → enhanced handler system → `MTGOLayout.tsx` → prop distribution coordination
5. **Consider patterns:** Single source of truth principles → clean prop flow → sophisticated timing integration
6. **Test by:** Handler execution accuracy → prop flow validation → cross-system coordination verification
   
   #### **Adding Timing & Interaction Features:**
7. **Start with:** `useDragAndDrop.ts` → timing constants modification → interaction detection logic → global event coordination
8. **Consider integration:** `DraggableCard.tsx` → interaction wrapper coordination → event handling patterns → timing validation
9. **Test by:** Interaction timing verification, cross-system coordination testing, performance impact assessment
   
   #### **Adding Visual Feedback Features:**
10. **Start with:** `DragPreview.tsx` → scaling logic and visual effects → `DropZone.tsx` → feedback coordination → animation integration
11. **Consider performance:** 3x scaling impact, requestAnimationFrame coordination, hardware acceleration utilization
12. **Test by:** Visual feedback accuracy, animation smoothness, performance monitoring across different hardware
    
    #### **Adding View Mode Integration:**
13. **Start with:** `PileView.tsx` or `ListView.tsx` → view-specific drag handling → coordination patterns → performance optimization
14. **Then modify:** Drag handler pass-through patterns → state management integration → cross-view coordination
15. **Test by:** View mode switching accuracy, drag state preservation, view-specific functionality validation
    
    #### **Adding Selection System Features:**
16. **Start with:** `useSelection.ts` → dual selection logic → mutual exclusion patterns → object storage coordination
17. **Consider integration:** `DraggableCard.tsx` → selection type routing → drag rectangle coordination → legacy compatibility
18. **Test by:** Selection type accuracy, mutual exclusion validation, cross-system selection coordination
    
    #### **Adding Central Orchestration Features:**
19. **Start with:** `MTGOLayout.tsx` → enhanced handler coordination → prop distribution → multi-hook integration patterns
20. **Consider complexity:** Enhanced handler management → state synchronization → performance impact assessment
21. **Test by:** Handler orchestration accuracy, state synchronization validation, multi-system integration testing
    
    #### **Adding Performance Optimization:**
22. **Start with:** `useDragAndDrop.ts` → global event handling → timer management → memory optimization patterns
23. **Consider impact:** requestAnimationFrame coordination → passive listener optimization → memory leak prevention
24. **Test by:** Performance monitoring, memory usage tracking, interaction responsiveness validation
    
    ### File Modification Order
    
    #### **For single handler architecture changes:** Component interface analysis → `MTGOLayout.tsx` (handler distribution) → component implementations → prop flow validation → functionality testing
    
    #### **For timing system changes:** `useDragAndDrop.ts` (timing constants) → `DraggableCard.tsx` (interaction detection) → timing coordination testing → cross-system validation
    
    #### **For visual feedback changes:** `DragPreview.tsx` (scaling/positioning) → `DropZone.tsx` (feedback logic) → `DragAndDropStyles.css` (animations) → visual coordination testing
    
    #### **For view mode changes:** `PileView.tsx`/`ListView.tsx` (view-specific handling) → drag handler coordination → `MTGOLayout.tsx` (orchestration) → cross-view testing
    
    #### **For selection integration changes:** `useSelection.ts` (dual selection logic) → `DraggableCard.tsx` (routing patterns) → `MTGOLayout.tsx` (coordination) → selection testing
    
    #### **For central orchestration changes:** `MTGOLayout.tsx` (enhanced handler management) → multi-hook integration → prop distribution → state synchronization testing
    
    #### **For cross-system integration changes:** Target system files → integration point coordination → `MTGOLayout.tsx` (orchestration) → comprehensive integration testing
    
    ### Testing Strategy
    
    **Critical to test:** Single handler architecture (enhanced handler only), sophisticated timing system (5 constants coordination), dual selection mutual exclusion, view mode coordination, central callback orchestration, visual feedback accuracy, drop zone detection, FlipCard integration, global event handling, performance optimization patterns 
    **Integration tests:** Cross-system coordination (FlipCard + drag, selection + drag, layout + drag), view mode switching with drag state preservation, central orchestration with multi-hook integration, timing coordination across interaction types, memory management and timer cleanup, single handler execution accuracy 
    **Performance validation:** requestAnimationFrame smoothness, global event handling efficiency, 3x scaling performance, memory usage monitoring, interaction responsiveness across different hardware, timer cleanup effectiveness, passive listener optimization, enhanced handler distribution efficiency

---

**System Guide Notes:**

- useDragAndDrop.ts provides extremely sophisticated timing system with 5 critical constants managing interaction detection and single handler architecture
- DraggableCard.tsx coordinates single handler architecture with advanced mouse interaction management and conditional FlipCard integration
- DropZone.tsx implements professional feedback with 10px buffer zones and NO RED policy for enhanced UX
- DragPreview.tsx provides 3x scaled preview with smart card stacking and color-coded visual feedback
- PileView.tsx and ListView.tsx coordinate view-specific drag handling with performance optimization patterns
- useSelection.ts manages dual selection system with mutual exclusion and drag rectangle support
- MTGOLayout.tsx orchestrates enhanced handler distribution with sophisticated multi-hook integration and clean prop flow
- Single handler architecture eliminates dual execution paths and callback proliferation technical debt (P2 resolution)
- Timing constants (500ms, 800ms, 150ms, 5px, 300ms) require precise coordination across all interaction types
- Global event handling uses passive listeners with requestAnimationFrame optimization for smooth performance
- Cross-system integration requires sophisticated state synchronization and callback orchestration patterns
- Performance optimization includes timer cleanup, memory management, and hardware-accelerated animations
- Central orchestration through MTGOLayout enables seamless multi-system coordination with comprehensive enhanced handler management
- Technical debt resolution includes elimination of callback proliferation and establishment of single source of truth architecture
