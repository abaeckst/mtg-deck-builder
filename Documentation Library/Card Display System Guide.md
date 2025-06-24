# Card Display System Guide

**Last Updated:** January 14, 2025 
**Status:** Working with complete display ecosystem and 3D flip functionality 
**Complexity:** High - Multiple display modes, view coordination, 3D animations, progressive loading, sophisticated interaction systems

## 🎯 System Definition

### Purpose

**What this system does:** Comprehensive card display ecosystem with three major view modes (card, pile, list), 3D flip animations for double-faced cards, view mode coordination, and seamless integration with drag/drop, dual selection, and layout systems 
**Why it exists:** Provides complete MTGO-style card display experience with performance optimization, professional UX, and sophisticated multi-mode interaction management 
**System boundaries:** Handles all card rendering, view mode switching, and display coordination; integrates with drag system, dual selection system, resize system, layout coordination, and export functionality

### Core Files (Always Work Together)

#### **Primary Display Components:**

- `MagicCard.tsx` (312 lines) - Base card display component with standard img tags and quantity badges
- `FlipCard.tsx` (350+ lines) - 3D animation wrapper for double-faced cards with hardware acceleration and container stabilization
- `DraggableCard.tsx` (276 lines) - Interactive wrapper with enhanced double-click detection and conditional FlipCard rendering
  
  #### **View Mode Components (Major Display Systems):**
- `PileView.tsx` (289 lines) - **CRITICAL:** Complete MTGO-style pile organization with mana/color/rarity/type sorting, manual arrangements, sophisticated performance optimizations
- `PileColumn.tsx` (156 lines) - **CRITICAL:** Individual pile columns with tight MTGO-style card stacking (~14% visible overlap), drop zone handling, instance-based selection
- `ListView.tsx` (318 lines) - **CRITICAL:** Universal tabular display with sortable/resizable columns, quantity management, extensive debugging for data properties
- `ViewModeDropdown.tsx` (150 lines) - **CRITICAL:** View mode coordinator with nuclear z-index strategy (2,000,000), context-aware positioning
  
  #### **Specialized Display Components:**
- `ScreenshotModal.tsx` (large file) - **EXPORT INTEGRATION:** Mathematical layout optimization, dynamic sizing, full-viewport card rendering for export
- `useCardSizing.ts` (149 lines) - **SIZING CONTROL:** Dedicated card size management with localStorage persistence (separate from layout system)
  
  ### Secondary Files
- `LazyImage.tsx` (100 lines) - **STANDALONE:** Progressive image loading component (not integrated with MagicCard.tsx)
- `card.ts` (520 lines) - Type definitions, face detection utilities (`isDoubleFacedCard`, `getCardFaceImageUri`), instance conversion functions
- `deviceDetection.ts` (145 lines) - Device capability detection with 250ms throttling optimization
  
  ### Integration Files
  
  #### **State Management:**
- `useSelection.ts` (310 lines) - **PRIMARY:** Dual selection system (instances vs cards) with mutual exclusion and drag rectangle selection
- `useDragAndDrop.ts` (445 lines) - Sophisticated interaction system with precise timing constants and advanced event coordination
- `useResize.ts` (149 lines) - Container stabilization context, percentage-based calculations, CSS custom property coordination
- `useLayout.ts` (305 lines) - Panel dimensions and view modes (separate from card sizing)
- `useCards.ts` (250 lines) - Coordination hub managing card data flow and selection state integration
  
  #### **Styling & Layout:**
- `MTGOLayout.css` (1,450 lines) - Complete styling foundation with significant technical debt and complex grid systems
- `ResponsiveDesign.css` - Media queries for card display responsiveness across view modes
- `ComponentStyles.css` - Professional button and control styling for view mode components
- `modal.css` - Screenshot modal styling for export functionality
- `ContextMenu.css` - Card right-click context menu styling
- `PanelResizing.css` - Resize handle styling affecting card display areas
  
  ### Integration Points
  
  **Receives data from:**
- **Card Sizing System:** useCardSizing.ts provides scaleFactor to all display components (independent of layout state)
- **Layout State System:** useLayout.ts provides view modes, panel dimensions, and responsive behavior through unified layout state
- **Data Management System:** Card data, dual selection state, deck/sideboard organization through useCards coordinator
- **Search & Filtering System:** Filtered card collections, search results, pagination state for all view modes
  **Provides data to:**
- **Drag & Drop System:** Draggable card instances with enhanced preview scaling, sophisticated timing coordination, and view-specific drag handling
- **Dual Selection System:** Click handling for both card-based (collection) and instance-based (deck/sideboard) selection across all view modes
- **Export System:** ScreenshotModal with mathematical layout optimization and full card rendering
- **View Mode Coordination:** ViewModeDropdown manages switching between card/pile/list displays
  **Coordinates with:**
- **Resize System:** Container stabilization patterns, CSS custom property updates, percentage-based layout calculations affecting all view modes
- **Performance System:** Image loading optimization, 3D animation hardware acceleration, view-specific interaction timing coordination
- **Context Menu System:** Right-click card interactions across all display modes
  
  ## 🔄 Critical Data Flows
  
  ### Primary Flow: View Mode Coordination & Display
  
  ```
  View Mode Selection → ViewModeDropdown → Layout state update → Component switching
  ↓
  Card Display Mode: MagicCard → DraggableCard → Direct card rendering
  Pile Display Mode: PileView → PileColumn → MTGO-style stacking → Card rendering
  List Display Mode: ListView → Tabular rows → Card data display
  ↓
  Card Sizing: useCardSizing.ts → scaleFactor props → All display components
  ↓
  Selection Coordination: useSelection.ts → Dual selection → Cross-view mode consistency
  ↓
  Responsive Behavior: useResize.ts → CSS custom properties → Container stabilization
  ```
  
  ### Secondary Flow: 3D Flip Animation (Hardware Accelerated)
  
  ```
  Double-faced card → FlipCard wrapper → Professional flip button (↻) → User click → stopPropagation()
  ↓
  Rotation state update → 3D transform (rotateY + 180°) → Hardware acceleration (will-change: transform)
  ↓
  Face selection → createFaceCard() → Face-specific image URI → MagicCard rendering → 400ms animation
  ↓
  Event Isolation → Advanced timing coordination → Drag protection periods → State preservation
  ```
  
  ### Advanced Flow: Pile Organization & Stacking
  
  ```
  Card Collection → PileView sorting (mana/color/rarity/type) → Column organization → Performance optimization
  ↓
  PileColumn rendering → MTGO-style stacking (14% visible overlap) → Instance-based cards → Drag handling
  ↓
  Manual arrangements → Card movement between columns → State persistence → Visual feedback
  ↓
  Empty column handling → Drop zone integration → Professional pile management
  ```
  
  ### Complex Flow: Tabular Display & Column Management
  
  ```
  Card Collection → ListView → Column definitions → Sortable/resizable headers → Performance optimization
  ↓
  Row rendering → Card property extraction → Type checking → Quantity controls → Instance handling
  ↓
  Column resizing → Mouse event handling → Width calculations → Layout preservation
  ↓
  Sorting coordination → Header clicks → Sort criteria changes → Data reordering
  ```
  
  ### Integration Flow: Export & Screenshot Display
  
  ```
  Export request → ScreenshotModal → Mathematical layout optimization → Dynamic column calculation
  ↓
  Card grouping → Instance organization → Quantity calculation → Grid layout generation
  ↓
  Full-viewport rendering → Size mode selection → Hardware acceleration → Professional export display
  ```
  
  ## 🐛 Problem Diagnosis
  
  ### View Mode & Coordination Issues
  
  **"View mode dropdown not working or showing wrong option"**
- **Root Cause:** ViewModeDropdown state synchronization or nuclear z-index conflicts
- **Check Files:** `ViewModeDropdown.tsx` (z-index: 2,000,000, context detection) → `useLayout.ts` (view mode state) → component rendering logic
- **Debug Pattern:** Verify ViewModeDropdown state → check z-index context detection → validate view mode propagation
  **"Pile view not organizing cards correctly"**
- **Root Cause:** PileView sorting logic or column organization failures
- **Check Files:** `PileView.tsx` (sorting criteria: mana/color/rarity/type) → column organization functions → performance optimization memoization
- **Debug Pattern:** Verify sort criteria → check column organization logic → validate memoization dependencies
  **"List view columns not working or showing wrong data"**
- **Root Cause:** ListView column definitions or card property extraction issues
- **Check Files:** `ListView.tsx` (column definitions, card property debugging) → type checking → responsive column handling
- **Debug Pattern:** Check column definitions → verify card property extraction → validate type checking logic
  
  ### Card Display & Rendering Issues
  
  **"Cards not displaying correct size across view modes"**
- **Root Cause:** useCardSizing.ts state not propagating or view-specific sizing conflicts
- **Check Files:** `useCardSizing.ts` (dedicated sizing state) → view mode components (PileView, ListView, card view) → scaleFactor application
- **Debug Pattern:** Verify useCardSizing state → check scaleFactor prop flow across all view modes → validate size calculations
  **"Card stacking not working in pile view"**
- **Root Cause:** PileColumn stacking calculations or MTGO-style overlap issues
- **Check Files:** `PileColumn.tsx` (14% visible overlap calculations, stack offset math) → card height calculations → z-index stacking
- **Debug Pattern:** Verify stack offset calculations → check card height estimates → validate z-index progression
  **"LazyImage not working with cards"**
- **Root Cause:** Architectural misunderstanding - LazyImage is standalone, not integrated with MagicCard
- **Check Files:** `MagicCard.tsx` (uses standard img tags) → `LazyImage.tsx` (standalone component for separate use cases)
- **Debug Pattern:** Understand LazyImage is separate component → Check if LazyImage is being used correctly in its own context
  
  ### 3D Animation & Advanced Display Issues
  
  **"3D flip animations not working or glitchy"**
- **Root Cause:** Hardware acceleration missing, container positioning conflicts, or event propagation issues
- **Check Files:** `FlipCard.tsx` (hardware acceleration, container stabilization) → `MTGOLayout.css` (3D styles, `will-change` properties) → `DraggableCard.tsx` (conditional rendering logic)
- **Debug Pattern:** Verify `will-change: transform` applied → check container stabilization (explicit dimensions) → validate conditional FlipCard rendering
  **"Drag interactions conflicting across view modes"**
- **Root Cause:** Event propagation conflicts between sophisticated interaction systems and view-specific handling
- **Check Files:** `useDragAndDrop.ts` (timing constants, event isolation) → view mode components (PileView, ListView drag handling) → `DraggableCard.tsx` (enhanced interaction detection)
- **Debug Pattern:** Check timing constants in useDragAndDrop → verify view-specific drag handling → validate interaction timing coordination
  
  ### Export & Screenshot Issues
  
  **"Screenshot modal not rendering cards correctly"**
- **Root Cause:** ScreenshotModal layout optimization or mathematical calculation failures
- **Check Files:** `ScreenshotModal.tsx` (mathematical layout, dynamic sizing) → export utility integration → card conversion logic
- **Debug Pattern:** Verify mathematical layout calculations → check card grouping logic → validate export rendering
  
  ### Selection & Integration Issues
  
  **"Selection system not working correctly across view modes"**
- **Root Cause:** Dual selection system complexity or cross-view mode synchronization issues
- **Check Files:** `useSelection.ts` (primary dual selection system) → view mode components (selection handling) → `useCards.ts` (selection integration)
- **Debug Pattern:** Verify useSelection.ts is being used (not useCardSelection.ts) → check view-specific selection handling → validate cross-view mode consistency
  **"CSS Grid positioning issues affecting display"**
- **Root Cause:** Container stabilization not working or resize system conflicts affecting view modes
- **Check Files:** `useResize.ts` (container stabilization patterns) → view mode component styling → `MTGOLayout.css` (complex grid systems)
- **Debug Pattern:** Check useResize.ts percentage calculations → verify view mode container stabilization → validate CSS Grid positioning context
  
  ### Debugging Starting Points
  
  **View mode problems:** Start with `ViewModeDropdown.tsx` → nuclear z-index strategy → `useLayout.ts` view mode state → component switching logic 
  **Display rendering issues:** Start with `useCardSizing.ts` → size state verification → view mode components → scaleFactor application 
  **Pile organization problems:** Start with `PileView.tsx` → sorting logic → `PileColumn.tsx` stacking calculations → manual arrangement state 
  **List display issues:** Start with `ListView.tsx` → column definitions → card property extraction → type checking logic 
  **3D animation problems:** Start with `FlipCard.tsx` → hardware acceleration → container stabilization → `MTGOLayout.css` CSS Grid context 
  **Selection issues:** Start with `useSelection.ts` → dual selection logic → view-specific selection handling → cross-view consistency 
  **Export problems:** Start with `ScreenshotModal.tsx` → mathematical layout optimization → card grouping → rendering logic
  
  ## 🔧 Architecture Details
  
  ### State Management Pattern
  
  **How state is organized:** Multi-system coordination across view modes - useCardSizing.ts manages card dimensions, useSelection.ts manages dual selection (instances vs cards), useDragAndDrop.ts manages sophisticated interactions, useResize.ts manages container stabilization, ViewModeDropdown coordinates display switching 
  **State flow:** useCardSizing.ts → scaleFactor props → All view mode components, coordinated with useSelection.ts dual selection, useDragAndDrop.ts timing, useResize.ts container stabilization, and ViewModeDropdown view coordination 
  **Key state variables:** Card size scaling (useCardSizing), dual selection state (useSelection instances/cards), view mode (ViewModeDropdown/useLayout), pile arrangements (PileView manual state), column widths (ListView resizable), flip rotation (FlipCard local), interaction timing (useDragAndDrop), container dimensions (useResize)
  
  ### Critical Functions & Hooks
  
  #### **View Mode Coordination:**
  
  **ViewModeDropdown:** Nuclear z-index strategy (2,000,000), context-aware positioning, overflow menu detection, view mode switching coordination 
  **PileView organization functions:** organizeByManaValue(), organizeByColor(), organizeByRarity(), organizeByType() with performance memoization 
  **ListView column management:** Resizable column system, sortable headers, card property extraction with extensive debugging 
  **useCardSizing.ts:** Dedicated card size state management with localStorage persistence (separate from layout system)
  
  #### **Display Rendering:**
  
  **isDoubleFacedCard() (FlipCard.tsx):** Detects double-faced cards using `card_faces && Array.isArray(card_faces) && card_faces.length >= 2` 
  **createFaceCard() (FlipCard.tsx):** Creates face-specific card objects for MagicCard rendering with proper type conversion and image URI resolution 
  **getCardFaceImageUri() (FlipCard.tsx):** Resolves face-specific image URLs, prioritizes PNG format, handles ScryfallCard/DeckCard/DeckCardInstance types 
  **PileColumn stacking calculations:** MTGO-style tight stacking with 14% visible overlap, dynamic height calculations, z-index progression
  
  #### **Advanced Systems:**
  
  **useSelection.ts:** Primary dual selection system with instance-based (deck/sideboard) and card-based (collection) selection with mutual exclusion across view modes 
  **useDragAndDrop.ts:** Sophisticated interaction system with timing constants (DRAG_START_DELAY: 150ms, CLICK_TO_DRAG_PROTECTION: 300ms, etc.) coordinated across view modes 
  **useResize.ts:** Container stabilization through percentage-based calculations and CSS custom property coordination affecting all display modes 
  **ScreenshotModal mathematical optimization:** Dynamic column calculation, size mode selection, layout optimization for export display 
  **Hardware acceleration setup (FlipCard.tsx):** `will-change: transform`, `perspective: 1000px`, GPU rendering for smooth 60fps animations
  
  ### Component Hierarchy
  
  ```
  ViewModeDropdown (nuclear z-index coordinator + context detection)
  ├── View Mode Selection (card/pile/list switching)
  └── Display Mode Routing:
  ├── [Card Mode] Collection/Deck card grid display
  │ └── DraggableCard (conditional FlipCard logic + sophisticated timing)
  │ ├── Enhanced interaction handling (useDragAndDrop timing, useSelection coordination)
  │ ├── Conditional 3D rendering:
  │ │ ├── [Double-faced] FlipCard (3D animation wrapper)
  │ │ │ ├── Professional flip button (↻) with hardware acceleration
  │ │ │ ├── 3D container (perspective: 1000px, transform-style: preserve-3d)
  │ │ │ │ ├── Front face (rotateY: 0deg) → MagicCard → Standard img tags
  │ │ │ │ └── Back face (rotateY: 180deg) → MagicCard → Standard img tags
  │ │ │ └── Stabilized container (explicit width/height for CSS Grid compatibility)
  │ │ └── [Single-faced] MagicCard directly → Standard img tags
  │ └── Dual selection integration (useSelection.ts instance vs card selection)
  ├── [Pile Mode] PileView (sophisticated organization + performance optimization)
  │ ├── Sorting coordination (mana/color/rarity/type with memoization)
  │ ├── Manual arrangement state management
  │ └── PileColumn[] (MTGO-style stacking)
  │ ├── Column header (number/type display)
  │ ├── Card stacking (14% visible overlap, z-index progression)
  │ ├── Drop zone integration (manual movement support)
  │ └── DraggableCard instances (quantity handling, instance-based selection)
  ├── [List Mode] ListView (tabular display + column management)
  │ ├── Resizable column system (mouse event handling, width persistence)
  │ ├── Sortable headers (criteria switching, direction indication)
  │ ├── Card property extraction (extensive debugging, type checking)
  │ ├── Quantity controls (instance vs card quantity handling)
  │ └── Row rendering (drag handling, selection coordination)
  └── [Export Mode] ScreenshotModal (mathematical layout optimization)
  ├── Dynamic sizing calculations (mathematical optimization)
  ├── Card grouping (instance organization, quantity calculation)
  ├── Grid layout generation (column optimization, space utilization)
  └── Full-viewport rendering (hardware acceleration, professional display)
  ```
  
  ### Performance Considerations
  
  **Critical paths:** View mode coordination (ViewModeDropdown nuclear z-index), card sizing coordination (useCardSizing.ts), dual selection management (useSelection.ts across view modes), pile organization (PileView memoization), list display (ListView column management), sophisticated interaction timing (useDragAndDrop.ts), 3D animations (hardware acceleration), container stabilization (useResize.ts), export optimization (ScreenshotModal mathematical calculations) 
  **Optimization patterns:** View mode switching coordination, dedicated card sizing state, dual selection mutual exclusion, pile sorting memoization, column resize performance, interaction timing constants, GPU rendering, percentage-based resize calculations, device detection throttling, mathematical export layout optimization 
  **Known bottlenecks:** CSS coordination complexity (1,450-line MTGOLayout.css), view mode nuclear z-index strategy, sophisticated interaction timing coordination across view modes, dual selection system complexity, pile organization performance with large collections, list view column management overhead, export mathematical calculations
  
  ## ⚠️ Current System Status
  
  ### Working Functionality
- ✅ **View Mode Coordination:** ViewModeDropdown working with nuclear z-index strategy (2,000,000) and context detection
- ✅ **Card Size Management:** useCardSizing.ts working with localStorage persistence across all view modes
- ✅ **Pile Organization:** PileView working with mana/color/rarity/type sorting, manual arrangements, performance optimization
- ✅ **MTGO-Style Stacking:** PileColumn 14% visible overlap calculations, instance-based selection, drop zone integration
- ✅ **Tabular Display:** ListView working with resizable/sortable columns, quantity management, extensive card property debugging
- ✅ **3D Flip Animations:** Hardware-accelerated 400ms rotations with professional flip button styling across view modes
- ✅ **Sophisticated Interactions:** useDragAndDrop.ts timing constants prevent conflicts across view modes, enhanced double-click detection
- ✅ **Dual Selection System:** useSelection.ts managing instance vs card selection with mutual exclusion across display modes
- ✅ **Container Stabilization:** useResize.ts percentage calculations and CSS custom property coordination affecting all view modes
- ✅ **Export Display:** ScreenshotModal mathematical layout optimization with dynamic sizing and professional rendering
- ✅ **Face-Specific Images:** `getCardFaceImageUri()` correctly resolves front/back face images across all contexts
- ✅ **Advanced Event Isolation:** Multi-system coordination prevents interaction conflicts across view modes
  
  ### Known Issues
- ⚠️ **Nuclear Z-Index Strategy:** ViewModeDropdown uses extreme z-index values (2,000,000) which work but indicate architectural constraint
- ⚠️ **CSS Grid Positioning:** Container stabilization in FlipCard prevents most positioning conflicts, but useResize.ts reveals complex dependencies across view modes
- ⚠️ **View Mode State Complexity:** Cross-view mode state synchronization requires careful coordination between ViewModeDropdown and component switching
- ⚠️ **Type Conversion Complexity:** DraggableCard's cardForFlipCard conversion handles multiple card types across view modes but adds architectural complexity
- ⚠️ **Pile Manual Arrangements:** Manual card movement between pile columns works but requires complex state management for persistence
- ⚠️ **List Column Management:** ListView column resizing works but involves complex mouse event coordination and width calculations
  
  ### Technical Debt
  
  **Priority Items:**
- **P1:** CSS coordination complexity (1,450-line MTGOLayout.css) with sophisticated resize system dependencies affecting all view modes
- **P1:** Nuclear z-index strategy (2,000,000) indicates need for systematic z-index management architecture
- **P2:** Multi-view mode state coordination could benefit from centralized state management architecture
- **P2:** Large card.ts file (520 lines) contains multiple concerns: types, utilities, conversions used across all view modes
- **P2:** Dual sizing systems (useCardSizing vs useLayout) could be confusing but serve different purposes across view modes
- **P3:** Sophisticated interaction coordination (useDragAndDrop + useSelection + useResize + ViewModeDropdown) requires careful timing management
- **P3:** PileView manual arrangements complexity could benefit from simplified state management patterns
- **P3:** ListView column management complexity could benefit from extraction to dedicated hook
- **P4:** Enhanced browser compatibility testing for 3D animations and view mode switching across different hardware contexts
  
  ### Recent Changes
  
  **January 13, 2025:** Complete 3D flip system implementation with FlipCard component, hardware acceleration optimization, and container stabilization for CSS Grid compatibility across all view modes 
  **Performance optimization:** Device detection render storm fix with 250ms throttling, sophisticated interaction timing coordination across view modes 
  **Architecture refinement:** DraggableCard conditional FlipCard rendering, enhanced double-click detection using event.detail, useCardSizing.ts separation from layout state, useSelection.ts dual selection system with mutual exclusion across display modes, useResize.ts container stabilization patterns, ViewModeDropdown nuclear z-index strategy, PileView performance optimization with memoization, ListView extensive card property debugging
  
  ## 🚀 Development Patterns
  
  ### Common Change Patterns
  
  #### **Adding View Mode Features:**
1. **Start with:** `ViewModeDropdown.tsx` → view mode coordination → nuclear z-index strategy
2. **Consider state:** `useLayout.ts` → view mode state management → component switching logic
3. **Test coordination:** Cross-view mode functionality, state synchronization, z-index conflicts
   
   #### **Adding Card Display Features:**
4. **Start with:** `MagicCard.tsx` → base display logic and prop integration across view modes
5. **Consider sizing:** `useCardSizing.ts` → independent card size management across all display modes
6. **Test by:** Visual verification in all view modes (card/pile/list), dual selection testing, sophisticated interaction validation
   
   #### **Adding Pile Organization Features:**
7. **Start with:** `PileView.tsx` → sorting logic (mana/color/rarity/type) → performance optimization with memoization
8. **Then modify:** `PileColumn.tsx` → MTGO-style stacking calculations → manual arrangement integration
9. **Test by:** Pile organization accuracy, stacking visual verification, manual movement functionality
   
   #### **Adding List Display Features:**
10. **Start with:** `ListView.tsx` → column definitions → card property extraction with debugging
11. **Consider management:** Column resizing logic, sorting coordination, quantity controls
12. **Test by:** Column functionality, data display accuracy, responsive behavior
    
    #### **Adding Export Features:**
13. **Start with:** `ScreenshotModal.tsx` → mathematical layout optimization → dynamic sizing calculations
14. **Consider integration:** Card grouping logic, instance organization, viewport rendering
15. **Test by:** Export layout accuracy, professional display quality, mathematical optimization verification
    
    #### **Adding 3D Animation Features:**
16. **Start with:** `FlipCard.tsx` → animation logic and hardware acceleration across view modes
17. **Then modify:** `MTGOLayout.css` → 3D styling and container stabilization via useResize patterns
18. **Test by:** Flip animation smoothness across view modes, event isolation, sophisticated interaction coordination
    
    ### File Modification Order
    
    #### **For view mode changes:** `ViewModeDropdown.tsx` (coordination) → `useLayout.ts` (state) → view mode components (PileView/ListView/card display) → cross-view testing
    
    #### **For display changes:** `useCardSizing.ts` (size state) → view mode components (sizing application) → `MagicCard.tsx` (base display) → `MTGOLayout.css` (styling via useResize coordination)
    
    #### **For pile features:** `PileView.tsx` (organization + performance) → `PileColumn.tsx` (stacking + manual movement) → interaction coordination testing
    
    #### **For list features:** `ListView.tsx` (columns + debugging) → card property handling → responsive coordination testing
    
    #### **For 3D effects:** `FlipCard.tsx` (animation + container) → `MTGOLayout.css` (hardware acceleration via useResize patterns) → view mode integration testing
    
    #### **For export features:** `ScreenshotModal.tsx` (mathematical optimization) → card grouping logic → professional display validation
    
    #### **For interaction fixes:** `useDragAndDrop.ts` (timing constants) → `useSelection.ts` (dual selection) → view mode coordination → interaction timing validation across all display modes
    
    #### **For sizing issues:** `useCardSizing.ts` (dedicated sizing) → component prop flow across view modes → avoid useLayout.ts confusion
    
    #### **For container positioning:** `useResize.ts` (stabilization patterns) → view mode components (container dimensions) → CSS Grid compatibility validation
    
    ### Testing Strategy
    
    **Critical to test:** View mode switching (card/pile/list coordination), 3D flip animations (smoothness, hardware acceleration), sophisticated interaction coordination across view modes (timing constants, event isolation), dual selection system (instance vs card mutual exclusion), pile organization (sorting accuracy, stacking visual quality), list display (column management, data accuracy), export functionality (mathematical layout optimization), container stabilization (CSS Grid positioning across view modes) 
    **Integration tests:** ViewModeDropdown switching preserves state across modes, flip button clicks don't trigger sophisticated drag system across view modes, card sizing responds to useCardSizing.ts changes in all display modes, dual selection mutual exclusion working across view transitions, pile manual arrangements persist correctly, list column resizing works reliably, face-specific images load correctly across all contexts, export rendering matches display quality 
    **Performance validation:** 60fps animations across view modes, sophisticated interaction timing coordination, percentage-based resize calculations, no interaction conflicts between complex systems, pile organization performance with large collections, list column management responsiveness, export mathematical calculation efficiency, nuclear z-index strategy stability

---

**System Guide Notes:**

- ViewModeDropdown coordinates all display modes with nuclear z-index strategy (2,000,000)
- useCardSizing.ts handles card scaling independently across all view modes
- useSelection.ts is the primary dual selection system working across card/pile/list modes
- useDragAndDrop.ts provides sophisticated interaction timing coordination across all display modes
- useResize.ts explains container stabilization patterns affecting all view mode positioning
- PileView provides complete MTGO-style pile organization with performance optimization
- PileColumn handles tight card stacking (14% visible overlap) and manual arrangements
- ListView manages tabular display with resizable/sortable columns and extensive card property debugging
- FlipCard component conditionally wraps MagicCard for double-faced cards across all view modes
- ScreenshotModal provides mathematical layout optimization for professional export display
- Hardware acceleration critical for smooth 3D animations across view mode contexts
- Advanced event isolation prevents sophisticated interaction system conflicts across display modes
- Container stabilization via useResize.ts patterns solves CSS Grid positioning challenges across view modes
- LazyImage.tsx exists as standalone component, not integrated with MagicCard.tsx
- MTGOLayout.css technical debt stems from resize system complexity and sophisticated grid coordination affecting all display modes
