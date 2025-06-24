# View & Display System Guide

**Last Updated:** January 14, 2025 
**Status:** Working with sophisticated view coordination and multi-modal display management 
**Complexity:** High - Nuclear z-index strategy, dual sort system, complex view coordination, mathematical stacking, performance optimization patterns

## 🎯 System Definition

### Purpose

**What this system does:** Comprehensive view mode coordination system managing card/pile/list display modes with sophisticated sorting, responsive column management, MTGO-style pile organization, and nuclear z-index strategies for reliable dropdown coordination 
**Why it exists:** Provides professional MTGO-style display flexibility with optimized sorting, mathematical pile stacking, universal tabular display, and reliable view mode switching across complex UI hierarchies 
**System boundaries:** Handles all view mode coordination, display organization, sorting management, and responsive view adaptation; integrates with card display, drag & drop, selection, and data management systems

### Core Files (Always Work Together)

#### **View Coordination & Switching:**

- `ViewModeDropdown.tsx` (4,394 bytes) - **CRITICAL:** Nuclear z-index strategy (600k-2M) with context detection, fixed positioning, click-outside management
  
  #### **Display Mode Components:**
- `ListView.tsx` (17,648 bytes) - **EXTREMELY COMPLEX:** Universal tabular display with resizable columns, sorting integration, quantity management, extensive debugging for data property issues
- `PileView.tsx` (13,787 bytes) - **COMPLEX:** MTGO-style organization with multiple sort modes (mana/color/rarity/type), performance optimization, manual arrangements, dynamic column generation
- `PileColumn.tsx` (7,979 bytes) - **SOPHISTICATED:** Individual pile rendering with mathematical stacking calculations (14% visible overlap), dual selection support, dynamic sizing
  
  #### **Sort Coordination:**
- `useSorting.ts` (5,069 bytes) - **PERFORMANCE OPTIMIZED:** Area-specific sort state (collection/deck/sideboard), dual sort system integration, global window coordination, memoized functions
  
  ### Integration Points
  
  **Receives data from:**
- **Data Management System:** Card collections, sort criteria, selection state through comprehensive data coordination
- **Layout System:** View mode state, responsive behavior triggers, panel dimensions for display adaptation
- **Card Display System:** Individual card rendering, scaling factors, display context for view-specific optimization
  **Provides data to:**
- **Layout System:** Active view mode, display organization state, sorting preferences for cross-system coordination
- **Selection System:** View-specific selection patterns, multi-selection coordination, selection ID routing
- **Drag & Drop System:** View-specific drag handling, drop zone management, interaction patterns
  **Coordinates with:**
- **Search & Filtering System:** Sort criteria coordination through global window integration, server-side sort triggering
- **Performance System:** Memoization patterns, re-render prevention, mathematical calculation optimization
- **UI Systems:** Nuclear z-index management, responsive display adaptation, modal coordination
  
  ## 🔄 Critical Data Flows
  
  ### Primary Flow: View Mode Coordination & Nuclear Z-Index Strategy
  
  ```
  User View Selection → ViewModeDropdown → Context Detection → Z-Index Strategy Selection
  ↓
  [Normal Context] Z-Index: 600,000 → Fixed positioning → Click-outside detection
  ↓
  [Overflow Context] Z-Index: 2,000,000 → Nuclear escalation → Reliable dropdown display
  ↓
  View Change → onViewChange callback → Layout system coordination → Display mode switching
  ```
  
  ### Complex Flow: Area-Specific Sorting & Dual Sort Decision
  
  ```
  Sort Request → useSorting → Area-specific state (collection/deck/sideboard) → Change detection
  ↓
  [Collection <75 cards] Client-side sort → UI component handling → Instant display update
  ↓
  [Collection >75 cards] Server-side coordination → Global window parameters → Search system integration
  ↓
  Scryfall Mapping → SCRYFALL_SORT_MAPPING → Server parameters → API coordination → Fresh results
  ```
  
  ### Advanced Flow: MTGO-Style Pile Organization & Performance Optimization
  
  ```
  Card Collection → PileView sort mode selection → Memoized organization functions
  ↓
  [Mana Sort] organizeByManaValue → CMC columns (0-6, 7+) → Only show populated columns
  ↓
  [Color Sort] organizeByColor → Single colors + multi-color grouping → Dynamic color combinations
  ↓
  [Rarity/Type Sort] Memoized configurations → Standard grouping → Consistent organization
  ↓
  Manual Arrangements → Map<cardId, columnId> → User-moved cards → State persistence → Dynamic columns
  ```
  
  ### Sophisticated Flow: Mathematical Pile Stacking & Visual Coordination
  
  ```
  PileColumn Rendering → Card quantity calculation → MTGO-style stacking coordination
  ↓
  Stack Math: cardHeight = 180 * scaleFactor → visiblePortion = cardHeight * 0.14 → stackOffset = -(cardHeight - visiblePortion)
  ↓
  Individual Card Rendering → Z-index progression → Tight stacking (14% visible) → Professional MTGO appearance
  ↓
  Dynamic Sizing → Column width = Math.max(110, 125 * scaleFactor) → Card containment → Gap visibility
  ```
  
  ### Complex Flow: Universal Tabular Display & Column Management
  
  ```
  ListView Initialization → Area-specific column visibility → Resizable column setup
  ↓
  Column Resize → Mouse event handling → Document listeners → Coordinate tracking → Width updates
  ↓
  Sort Integration → Header click handling → Visual indicators (↑/↓) → External sort coordination
  ↓
  Row Interaction → Multi-selection coordination → Drag initiation → Quantity management (deck/sideboard)
  ```
  
  ### Integration Flow: Cross-System Coordination & Global Communication
  
  ```
  Sort State Changes → useSorting global coordination → Window parameter setting
  ↓
  Server-Side Trigger → (window as any).triggerSearch → Search system integration → Fresh results
  ↓
  View Mode Changes → ViewModeDropdown → Layout system → Display component switching
  ↓
  Selection Coordination → Dual selection support → Card vs instance routing → Cross-view consistency
  ```
  
  ## 🐛 Problem Diagnosis
  
  ### View Coordination & Nuclear Z-Index Issues
  
  **"ViewModeDropdown not opening or conflicting with other UI"**
- **Root Cause:** Nuclear z-index strategy conflicts or context detection failure
- **Check Files:** `ViewModeDropdown.tsx` (nuclear z-index logic, context detection) → overflow menu detection → fixed positioning calculation
- **Debug Pattern:** Verify context detection (`.overflow-menu` parent) → check z-index escalation (600k vs 2M) → validate fixed positioning coordinates
  **"Dropdown menu appearing in wrong position"**
- **Root Cause:** Position calculation failure or fixed positioning coordination issues
- **Check Files:** `ViewModeDropdown.tsx` (calculateMenuPosition function) → button rect calculation → window scroll coordination
- **Debug Pattern:** Check button rect calculation → verify scroll offset coordination → validate fixed positioning application
  
  ### Sorting Coordination Issues
  
  **"Sort not working or showing wrong results across views"**
- **Root Cause:** Area-specific sort state confusion or dual sort system failure
- **Check Files:** `useSorting.ts` (area-specific state management, dual sort logic) → global window coordination → server-side triggering
- **Debug Pattern:** Verify area-specific sort state → check dual sort decision logic (>75 cards) → validate global window parameter setting
  **"Server-side sort not triggering for large collections"**
- **Root Cause:** Global window coordination failure or search system integration issues
- **Check Files:** `useSorting.ts` (global window coordination) → search system integration → server parameter mapping
- **Debug Pattern:** Check `(window as any).lastSearchMetadata` existence → verify `triggerSearch` function availability → validate Scryfall parameter mapping
  
  ### Pile Organization & Stacking Issues
  
  **"Pile view not organizing cards correctly or showing empty columns"**
- **Root Cause:** Organization function failure or memoization issues
- **Check Files:** `PileView.tsx` (organization functions, memoization patterns) → column generation logic → manual arrangements coordination
- **Debug Pattern:** Verify organization function execution → check memoized configuration objects → validate column filtering (only show populated)
  **"Card stacking not appearing correctly or overlapping wrong"**
- **Root Cause:** Mathematical stacking calculation failure or scaling issues
- **Check Files:** `PileColumn.tsx` (stack offset math, z-index progression) → card height calculation → visual stacking coordination
- **Debug Pattern:** Check stack offset calculation `-(cardHeight - visiblePortion)` → verify z-index progression → validate scale factor application
  **"Manual card arrangements not working between pile columns"**
- **Root Cause:** Manual arrangements state management or drag coordination failure
- **Check Files:** `PileView.tsx` (manualArrangements Map state) → card movement handling → state persistence patterns
- **Debug Pattern:** Verify Map state updates → check card movement detection → validate arrangement persistence
  
  ### Tabular Display & Column Issues
  
  **"ListView columns not resizing or showing wrong widths"**
- **Root Cause:** Column resize logic failure or mouse event coordination issues
- **Check Files:** `ListView.tsx` (column resize handling, mouse event coordination) → document listener management → width calculation
- **Debug Pattern:** Check mouse event listener setup → verify resize state management → validate width calculation logic
  **"Table sorting not working or showing wrong indicators"**
- **Root Cause:** Sort integration failure or header click handling issues
- **Check Files:** `ListView.tsx` (header click handling, sort integration) → `useSorting.ts` coordination → visual indicator management
- **Debug Pattern:** Verify header click detection → check sort state coordination → validate visual indicator display (↑/↓)
  **"Quantity controls not working in deck/sideboard list view"**
- **Root Cause:** Quantity management logic failure or instance vs card handling issues
- **Check Files:** `ListView.tsx` (quantity controls, instance vs card handling) → quantity change coordination → deck building integration
- **Debug Pattern:** Check quantity button functionality → verify instance vs card detection → validate quantity change propagation
  
  ### Data Type & Property Issues
  
  **"Cards showing missing properties or (card as any) errors"**
- **Root Cause:** Type system issues or data structure inconsistencies
- **Check Files:** `ListView.tsx` (extensive debug logging, type casting) → card property access → data management integration
- **Debug Pattern:** Check debug console output → verify card property existence → validate type system consistency
  **"Oracle text, power, toughness not displaying"**
- **Root Cause:** Property access failures requiring type casting
- **Check Files:** `ListView.tsx` (property access patterns, debug logging) → card data structure validation → type system coordination
- **Debug Pattern:** Verify property existence on card objects → check alternative property names → validate type casting necessity
  
  ### Performance & Optimization Issues
  
  **"View switching causing performance issues or re-renders"**
- **Root Cause:** Memoization failure or performance optimization breakdown
- **Check Files:** `PileView.tsx` (memoization patterns) → `useSorting.ts` (stable dependencies) → re-render prevention validation
- **Debug Pattern:** Check memoization effectiveness → verify stable dependency arrays → validate re-render prevention
  **"Large pile collections causing slowdowns"**
- **Root Cause:** Organization function performance or column rendering issues
- **Check Files:** `PileView.tsx` (organization performance, column memoization) → mathematical calculation efficiency → rendering optimization
- **Debug Pattern:** Check organization function performance → verify column memoization → validate rendering efficiency patterns
  
  ### Debugging Starting Points
  
  **View coordination issues:** Start with `ViewModeDropdown.tsx` nuclear z-index strategy → context detection → fixed positioning validation 
  **Sorting problems:** Start with `useSorting.ts` area-specific state → dual sort logic → global window coordination verification 
  **Pile organization issues:** Start with `PileView.tsx` organization functions → memoization patterns → manual arrangements validation 
  **Stacking display problems:** Start with `PileColumn.tsx` mathematical calculations → stacking offset → z-index progression validation 
  **Table display issues:** Start with `ListView.tsx` column management → resize handling → sort integration verification 
  **Data property issues:** Start with `ListView.tsx` debug logging → property access patterns → type system validation 
  **Performance issues:** Start with memoization patterns → stable dependencies → re-render prevention verification
  
  ## 🔧 Architecture Details
  
  ### State Management Pattern
  
  **How state is organized:** Multi-component coordination with ViewModeDropdown (nuclear z-index management), useSorting (area-specific state), PileView (manual arrangements + memoized organization), ListView (column widths + resize state), integrated through external layout coordination 
  **State flow:** View mode selection → ViewModeDropdown → Layout system → Display component switching, coordinated with useSorting area-specific state → dual sort decision → client/server coordination 
  **Key state variables:** View mode selection (dropdown), area-specific sort state (useSorting), manual arrangements (PileView Map), column widths (ListView), resize state (ListView), nuclear z-index context (ViewModeDropdown)
  
  ### Critical Functions & Hooks
  
  #### **Nuclear Z-Index Strategy (ViewModeDropdown.tsx):**
  
  **isInOverflowContext:** DOM traversal checking for `.overflow-menu` parent to determine z-index escalation need 
  **Nuclear z-index values:** 600,000 normal context, 2,000,000 overflow context for reliable dropdown positioning 
  **calculateMenuPosition:** Button rect calculation with window scroll coordination for fixed positioning accuracy 
  **Click-outside detection:** Document event listener with proper cleanup for professional dropdown behavior
  
  #### **Area-Specific Sorting (useSorting.ts):**
  
  **Area-specific state management:** collection/deck/sideboard independent sort criteria and direction with change detection 
  **Dual sort system integration:** Server-side triggering for collection >75 cards through global window coordination 
  **Performance optimization patterns:** Stable dependency arrays, memoized return object, no localStorage persistence, change detection preventing re-renders 
  **Scryfall mapping:** SCRYFALL_SORT_MAPPING for server parameter translation with consistent sort coordination
  
  #### **MTGO-Style Pile Organization (PileView.tsx):**
  
  **Multiple organization functions:** organizeByManaValue/Color/Rarity/Type with memoized configurations (colorNameMap, rarityConfig, typeOrderConfig) 
  **Manual arrangements system:** Map<cardId, columnId> state for user-moved cards with dynamic column generation 
  **Performance optimization:** Comprehensive memoization preventing re-renders, stable function dependencies, efficient column filtering 
  **Dynamic column generation:** Only show populated columns + empty column at end for drops, consistent ColumnData interface
  
  #### **Mathematical Stacking Calculations (PileColumn.tsx):**
  
  **MTGO-style stacking math:** `cardHeight = 180 * scaleFactor`, `visiblePortion = cardHeight * 0.14`, `stackOffset = -(cardHeight - visiblePortion)` 
  **Z-index progression:** cardIndex for proper visual layering (last card highest z-index, most visible) 
  **Dynamic sizing:** Column width `Math.max(110, Math.round(125 * scaleFactor))` for card containment with gap visibility 
  **Dual selection support:** Both onClick (cards) and onInstanceClick (instances) with proper ID routing
  
  #### **Universal Tabular Display (ListView.tsx):**
  
  **Resizable column system:** Mouse event handling with document listeners, coordinate tracking, minimum width constraints 
  **Area-specific behavior:** Column visibility (quantity only in deck/sideboard), different interaction patterns 
  **Quantity management:** +/- buttons with instance vs card handling, basic land quantity limits, deck building integration 
  **Extensive debugging:** Detailed property analysis revealing data structure issues, type casting patterns
  
  ### Component Hierarchy
  
  ```
  ViewModeDropdown (Nuclear Z-Index Coordinator)
  ├── Context Detection System:
  │ ├── isInOverflowContext() (DOM traversal for .overflow-menu parent)
  │ ├── Nuclear Z-Index Strategy (600,000 normal → 2,000,000 overflow)
  │ ├── Fixed Positioning (calculateMenuPosition with scroll coordination)
  │ └── Click-Outside Detection (document listener with cleanup)
  ├── View Mode Selection:
  │ ├── card/pile/list options
  │ ├── onViewChange callback coordination
  │ └── Visual feedback (chevron rotation, active states)
  └── Layout System Integration (view mode state coordination)
  ↓
  Display Mode Components:
  ├── ListView (Universal Tabular Display - 17,648 bytes):
  │ ├── Column Management System:
  │ │ ├── Resizable Columns (mouse event handling, document listeners)
  │ │ ├── Area-Specific Visibility (quantity column only in deck/sideboard)
  │ │ ├── Minimum Width Constraints (30-80px per column)
  │ │ └── Dynamic Width Calculation (totalWidth computation)
  │ ├── Sorting Integration:
  │ │ ├── Header Click Handling (sortable column detection)
  │ │ ├── Visual Indicators (↑/↓ direction arrows)
  │ │ ├── External Sort Coordination (useSorting integration)
  │ │ └── Sort State Propagation (criteria + direction)
  │ ├── Row Interaction System:
  │ │ ├── Multi-Selection Coordination (selectedCards array)
  │ │ ├── Drag Initiation (left mouse detection, selected card handling)
  │ │ ├── Context Menu Integration (right-click coordination)
  │ │ └── Double-Click Handling (card action coordination)
  │ ├── Quantity Management (Deck/Sideboard):
  │ │ ├── +/- Button Controls (instance vs card quantity handling)
  │ │ ├── Basic Land Detection (unlimited quantity support)
  │ │ ├── Quantity Limits (4-card maximum for non-basics)
  │ │ └── Deck Building Integration (quantity change propagation)
  │ ├── Data Property Handling:
  │ │ ├── Extensive Type Casting ((card as any) for missing properties)
  │ │ ├── Debug Logging (detailed property analysis)
  │ │ ├── Alternative Property Detection (oracle_text, power, toughness)
  │ │ └── Fallback Patterns (— display for null/undefined values)
  │ └── Professional Table Styling (MTGO-authentic appearance)
  ├── PileView (MTGO-Style Organization - 13,787 bytes):
  │ ├── Multiple Sort Mode System:
  │ │ ├── organizeByManaValue (CMC columns 0-6, 7+)
  │ │ ├── organizeByColor (single colors + multi-color grouping)
  │ │ ├── organizeByRarity (common/uncommon/rare/mythic)
  │ │ └── organizeByType (creatures/instants/sorceries/etc.)
  │ ├── Performance Optimization:
  │ │ ├── Memoized Configurations (colorNameMap, rarityConfig, typeOrderConfig)
  │ │ ├── Comprehensive useMemo/useCallback (preventing re-renders)
  │ │ ├── Stable Function Dependencies (organization function stability)
  │ │ └── Efficient Column Filtering (only show populated columns)
  │ ├── Manual Arrangements System:
  │ │ ├── Map<cardId, columnId> State (user-moved card tracking)
  │ │ ├── Dynamic Column Generation (manual columns + empty drop column)
  │ │ ├── State Persistence (manual arrangements maintained across sorts)
  │ │ └── handleManualMove Integration (drag coordination for column movement)
  │ ├── Column Data Structure:
  │ │ ├── Standardized ColumnData Interface (id/title/cards/sortValue)
  │ │ ├── Dynamic Column Creation (only populated columns visible)
  │ │ ├── Empty Column Management (drop target at end)
  │ │ └── Column Count Display (title with card count)
  │ └── PileColumn Integration (pass-through handlers, scaling coordination)
  ├── PileColumn (Individual Pile Rendering - 7,979 bytes):
  │ ├── MTGO-Style Mathematical Stacking:
  │ │ ├── Stack Calculation (cardHeight = 180 * scaleFactor)
  │ │ ├── Visible Portion (14% of card showing name area)
  │ │ ├── Stack Offset (-(cardHeight - visiblePortion) for tight stacking)
  │ │ └── Z-Index Progression (cardIndex for proper layering)
  │ ├── Dual Selection Support:
  │ │ ├── onClick Handler (card-based selection for collection)
  │ │ ├── onInstanceClick Handler (instance-based selection for deck/sideboard)
  │ │ ├── Selection ID Routing (card.id vs instanceId appropriate handling)
  │ │ └── Multi-Selection Coordination (selectedCards array integration)
  │ ├── Dynamic Sizing System:
  │ │ ├── Column Width Calculation (Math.max(110, 125 * scaleFactor))
  │ │ ├── Card Containment (width ensures cards fit within bounds)
  │ │ ├── Gap Visibility (balanced sizing showing column separation)
  │ │ └── Empty Column Handling (reduced width for drop targets)
  │ ├── Professional Card Rendering:
  │ │ ├── Individual Card Loop (quantity-based rendering for legacy support)
  │ │ ├── DraggableCard Integration (conditional FlipCard, scaling, interaction)
  │ │ ├── Stack Item Styling (relative positioning, margin-top offsets)
  │ │ └── Error Handling (invalid card validation, fallback rendering)
  │ └── Drop Zone Integration (manual card movement between columns)
  └── useSorting (Area-Specific Sort Coordination - 5,069 bytes):
  ├── Area-Specific State Management:
  │ ├── collection/deck/sideboard Independent State (criteria + direction)
  │ ├── Change Detection (prevents unnecessary re-renders)
  │ ├── No localStorage Persistence (session-only sorting)
  │ └── Default State Management (fresh defaults on initialization)
  ├── Dual Sort System Integration:
  │ ├── Collection Sort Logic (>75 cards → server-side, ≤75 → client-side)
  │ ├── Global Window Coordination ((window as any) parameter setting)
  │ ├── Search System Integration (triggerSearch function coordination)
  │ └── Scryfall Parameter Mapping (SCRYFALL_SORT_MAPPING translation)
  ├── Performance Optimization:
  │ ├── Stable Dependency Arrays (preventing hook recreation)
  │ ├── Memoized Return Object (preventing consumer re-renders)
  │ ├── Simplified Server Logic (reduced coordination complexity)
  │ └── Change Detection (state comparison before updates)
  └── API Coordination:
  ├── getScryfallSortParams (server parameter generation)
  ├── isServerSideSupported (criteria validation)
  ├── getGlobalSortState (cross-system state access)
  └── Static Utilities (availableCriteria, scryfallMapping)
  ```
  
  ### Performance Considerations
  
  **Critical paths:** Nuclear z-index strategy (ViewModeDropdown context detection), area-specific sorting (useSorting dual system), MTGO pile organization (PileView memoized functions), mathematical stacking (PileColumn calculations), tabular display (ListView column management), global window coordination (sort system integration) 
  **Optimization patterns:** Comprehensive memoization (PileView configurations), stable dependencies (useSorting), change detection (re-render prevention), mathematical efficiency (stacking calculations), column width caching (ListView), nuclear z-index reliability (dropdown positioning) 
  **Known bottlenecks:** ListView complexity (17,648 bytes with multiple responsibilities), PileView organization calculations (memoized but still complex), global window coordination overhead (sort system), nuclear z-index strategy complexity (context detection), mathematical stacking calculations (per-card overhead), type casting overhead (ListView property access)
  
  ## ⚠️ Current System Status
  
  ### Working Functionality
- ✅ **Nuclear Z-Index Strategy:** ViewModeDropdown context detection working with 600k-2M z-index escalation ensuring reliable dropdown positioning
- ✅ **Area-Specific Sorting:** useSorting managing collection/deck/sideboard independent sort state with change detection optimization
- ✅ **Dual Sort System:** Server-side sort triggering for large collections (>75 cards) through global window coordination
- ✅ **MTGO-Style Pile Organization:** PileView comprehensive organization modes (mana/color/rarity/type) with performance optimization
- ✅ **Mathematical Pile Stacking:** PileColumn 14% visible overlap calculations with proper z-index progression
- ✅ **Manual Pile Arrangements:** Map-based state for user-moved cards between columns with dynamic column generation
- ✅ **Universal Tabular Display:** ListView resizable columns with area-specific behavior and quantity management
- ✅ **Performance Optimization:** Comprehensive memoization patterns preventing re-renders across all components
- ✅ **Responsive Column Management:** Dynamic width calculation with minimum constraints and resize handling
- ✅ **Professional Visual Feedback:** Sort indicators, hover effects, selection states, MTGO-authentic styling
- ✅ **Cross-System Integration:** View mode coordination with layout, drag & drop, selection, and data management systems
  
  ### Known Issues
- ⚠️ **ListView Type System Issues:** Extensive `(card as any)` casting for oracle_text, power, toughness properties indicating data structure inconsistencies
- ⚠️ **Global Window Coordination:** useSorting relies on window globals for search system integration creating architectural coupling
- ⚠️ **Nuclear Z-Index Strategy:** ViewModeDropdown extreme values (600k-2M) indicate systematic z-index management needs
- ⚠️ **Component Size Complexity:** ListView (17,648 bytes) handling table/resize/quantity/drag creating maintenance complexity
- ⚠️ **Debug Code Presence:** Console.log statements in ListView indicating ongoing property access debugging needs
- ⚠️ **Context Detection Complexity:** ViewModeDropdown DOM traversal for overflow menu detection adding architectural overhead
- ⚠️ **Manual Arrangements Complexity:** PileView Map state coordination for user-moved cards creating state management overhead
- ⚠️ **Performance Calculation Overhead:** Mathematical stacking calculations per card in PileColumn creating rendering complexity
  
  ### Technical Debt
  
  **Priority Items:**
- **P2:** ListView size and complexity (17,648 bytes) - consider extraction of resize logic, quantity management, or column coordination
- **P2:** Type system inconsistencies requiring extensive (card as any) casting - data structure alignment needed
- **P2:** Global window coordination in useSorting - architectural coupling with search system needs improvement
- **P2:** Nuclear z-index strategy complexity - systematic z-index management architecture needed
- **P3:** Debug code presence in ListView - property access issues need resolution or proper error handling
- **P3:** Context detection complexity in ViewModeDropdown - DOM traversal overhead could be simplified
- **P3:** Manual arrangements state complexity in PileView - Map-based coordination could benefit from dedicated service
- **P3:** Mathematical calculation overhead in PileColumn - stacking calculations could be optimized or cached
- **P4:** Component responsibility distribution - multiple components handling both display and interaction logic
- **P4:** Performance optimization maintenance - comprehensive memoization requires ongoing dependency monitoring
  
  ### Recent Changes
  
  **Performance optimization:** useSorting stable dependencies and memoized functions, PileView comprehensive memoization patterns 
  **Nuclear z-index implementation:** ViewModeDropdown context detection with extreme z-index values for reliable positioning 
  **Mathematical stacking enhancement:** PileColumn MTGO-style calculations with proper visual layering
  
  ## 🚀 Development Patterns
  
  ### Common Change Patterns
  
  #### **Adding View Mode Features:**
1. **Start with:** `ViewModeDropdown.tsx` → nuclear z-index strategy → context detection → view option integration
2. **Consider coordination:** Layout system integration → view mode state management → display component switching
3. **Test by:** View switching accuracy → dropdown positioning reliability → nuclear z-index effectiveness
   
   #### **Adding Sorting Features:**
4. **Start with:** `useSorting.ts` → area-specific state management → dual sort logic → global window coordination
5. **Consider integration:** Server-side sort triggering → search system coordination → Scryfall parameter mapping
6. **Test by:** Sort functionality across areas → dual sort decision accuracy → server coordination effectiveness
   
   #### **Adding Pile Organization Features:**
7. **Start with:** `PileView.tsx` → organization function implementation → memoization patterns → manual arrangement integration
8. **Consider performance:** Memoized configurations → stable dependencies → re-render prevention → column generation efficiency
9. **Test by:** Organization accuracy → performance monitoring → manual arrangement functionality → column display verification
   
   #### **Adding Table Display Features:**
10. **Start with:** `ListView.tsx` → column management → resize handling → area-specific behavior integration
11. **Consider complexity:** Type casting needs → property access patterns → quantity management coordination
12. **Test by:** Column functionality → resize accuracy → quantity controls → property display verification
    
    #### **Adding Mathematical Stacking Features:**
13. **Start with:** `PileColumn.tsx` → stacking calculation implementation → scaling integration → visual coordination
14. **Consider performance:** Mathematical efficiency → z-index progression → dual selection support → rendering optimization
15. **Test by:** Stacking visual accuracy → scaling responsiveness → selection coordination → performance monitoring
    
    #### **Adding Performance Optimization:**
16. **Start with:** Memoization pattern implementation → stable dependencies → change detection → re-render prevention
17. **Consider impact:** Component coordination → state management efficiency → calculation optimization → memory usage
18. **Test by:** Performance monitoring → re-render tracking → calculation efficiency → memory leak prevention
    
    ### File Modification Order
    
    #### **For view coordination changes:** `ViewModeDropdown.tsx` (nuclear z-index) → layout system integration → display component coordination → view switching testing
    
    #### **For sorting changes:** `useSorting.ts` (area-specific state) → dual sort logic → global coordination → server integration testing
    
    #### **For pile organization changes:** `PileView.tsx` (organization functions) → memoization patterns → `PileColumn.tsx` (stacking) → performance validation
    
    #### **For table display changes:** `ListView.tsx` (column management) → resize handling → property access → quantity management testing
    
    #### **For mathematical stacking changes:** `PileColumn.tsx` (calculations) → scaling integration → visual validation → performance monitoring
    
    #### **For performance optimization changes:** Target component memoization → stable dependencies → change detection → performance validation
    
    ### Testing Strategy
    
    **Critical to test:** Nuclear z-index strategy reliability (ViewModeDropdown positioning), area-specific sorting accuracy (collection/deck/sideboard), dual sort system coordination (client vs server), MTGO pile organization (mathematical stacking), tabular display functionality (column management), performance optimization effectiveness (memoization patterns) 
    **Integration tests:** View mode switching coordination with layout system, sort state coordination across areas, pile organization with manual arrangements, table display with quantity management, mathematical stacking with dual selection, performance patterns across components 
    **Performance validation:** Nuclear z-index context detection efficiency, sort coordination timing, pile organization calculation performance, table column resize responsiveness, mathematical stacking rendering efficiency, memoization effectiveness monitoring

---

**System Guide Notes:**

- ViewModeDropdown implements nuclear z-index strategy (600k-2M) with context detection for reliable dropdown positioning in complex UI hierarchies
- useSorting provides area-specific sort management (collection/deck/sideboard) with dual sort system coordinating client vs server sorting
- PileView offers sophisticated MTGO-style organization with comprehensive memoization patterns and manual arrangement support
- PileColumn implements mathematical stacking calculations (14% visible overlap) with dual selection support and dynamic sizing
- ListView provides universal tabular display with resizable columns but suffers from type system issues requiring extensive casting
- Performance optimization patterns include comprehensive memoization, stable dependencies, change detection, and mathematical efficiency
- Global window coordination in useSorting creates architectural coupling with search system requiring careful maintenance
- Technical debt includes component size complexity, type system inconsistencies, debug code presence, and nuclear z-index strategy complexity
- Manual arrangements system uses Map-based state for user-moved cards between pile columns with dynamic column generation
- Cross-system integration requires coordination with layout, drag & drop, selection, and data management systems
