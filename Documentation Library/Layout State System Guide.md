# Layout State System Guide

**Last Updated:** January 14, 2025 
**Status:** Working with complex percentage-based layout and unified deck/sideboard state 
**Complexity:** High - Sophisticated state management, CSS custom property coordination, dual update paths, extensive responsive behavior

## 🎯 System Definition

### Purpose

**What this system does:** Comprehensive layout state management with unified deck/sideboard controls, percentage-based responsive layout, automatic migration from legacy systems, and sophisticated CSS custom property coordination 
**Why it exists:** Provides MTGO-style resizable interface with unified state patterns, device detection integration, and professional responsive behavior across all screen sizes 
**System boundaries:** Handles all layout dimensions, view mode coordination, panel resizing, and CSS variable management; integrates with all major systems through state coordination

### Core Files (Always Work Together)

#### **Foundation State Management (Always Start Here):**

- `useLayout.ts` (12,867 bytes) - **CRITICAL:** Unified deck/sideboard state, percentage-based calculations, automatic migration, CSS custom property coordination
- `useResize.ts` (7,313 bytes) - **CRITICAL:** Container stabilization, real-time CSS coordination, percentage/pixel conversion, resize event handling
- `deviceDetection.ts` (9,680 bytes) - **PERFORMANCE:** 250ms throttling, change detection, cached device info, responsive trigger system
  
  #### **Layout Coordination (State Integration):**
- `MTGOLayout.tsx` (28,194 bytes) - **CRITICAL:** Main state coordinator, unified state consumption, component orchestration, CSS delegation
- `ViewModeDropdown.tsx` (4,394 bytes) - **INTEGRATION:** Nuclear z-index strategy (600k-2M), view mode coordination, context detection
  
  #### **CSS Architecture (Styling Foundation):**
- `MTGOLayout.css` (43,662 bytes) - **CRITICAL:** Complete styling foundation, CSS custom property integration, complex responsive patterns, technical debt source
- `PanelResizing.css` (2,783 bytes) - **TECHNICAL DEBT:** P2 CSS coordination conflicts, resize handle styling, 6px vs 30px width coordination issues
- `CSSVariables.css` (379 bytes) - **FOUNDATION:** CSS custom property definitions updated by both useLayout and useResize
  
  ### Integration Points
  
  **Receives data from:**
- **Device Detection System:** deviceDetection.ts provides throttled device capability changes triggering layout responsive behavior
- **Card Display System:** View mode coordination requires layout state integration for unified deck/sideboard display
- **Component Systems:** All area components (DeckArea, SideboardArea, CollectionArea) receive layout state for responsive coordination
  **Provides data to:**
- **Component Integration System:** Unified `deckSideboard` view mode and size state to DeckArea (with controls) and SideboardArea (inherited only)
- **CSS Rendering System:** Real-time CSS custom property updates (`--deck-area-height-percent`, `--deck-area-height`, `--collection-area-height`)
- **Responsive Systems:** Device-aware layout adaptation and priority-based content hiding through AdaptiveHeader patterns
- **View Mode Systems:** ViewModeDropdown state coordination with nuclear z-index strategy, responsive header control coordination
  **Coordinates with:**
- **Card Sizing System:** useCardSizing.ts operates independently for collection size, useLayout handles unified deck/sideboard size
- **Performance System:** Device detection throttling prevents layout system overload during resize operations
- **CSS Architecture:** Complex coordination between JavaScript state updates and CSS custom property rendering
  
  ## 🔄 Critical Data Flows
  
  ### Primary Flow: Unified Deck/Sideboard State Management
  
  ```
  User Action → updateDeckSideboardViewMode() → useLayout state update → MTGOLayout consumption
  ↓
  DeckArea + SideboardArea → layout.viewModes.deckSideboard → Synchronized view mode display
  ↓
  Card Size Change → updateDeckSideboardCardSize() → layout.cardSizes.deckSideboard → Unified sizing
  ↓
  State Persistence → saveLayout() → localStorage → Automatic migration support
  ```
  
  ### Secondary Flow: Percentage-Based Layout System
  
  ```
  Panel Resize → useResize drag events → Pixel to percentage conversion → updateDeckAreaHeightByPixels()
  ↓
  useLayout.ts → updateCSSVariables() → CSS custom properties → Grid layout updates
  ↓
  Viewport Changes → Window resize → Percentage recalculation → CSS variable updates
  ↓
  Responsive Behavior → Content hiding based on CSS custom property values → Professional adaptation
  ```
  
  ### Complex Flow: Dual CSS Update Path Coordination
  
  ```
  Layout State Change → useLayout.ts updateCSSVariables() → CSS custom properties update
  ↓ ↑
  Resize Operation → useResize.ts updateCSSVariables() --------→ SAME CSS properties updated
  ↓
  Real-time Updates → requestAnimationFrame → Smooth resize coordination → CSS Grid rendering
  ```
  
  ### Advanced Flow: Device Detection Responsive Integration
  
  ```
  Device Change → deviceDetection throttling (250ms) → Change detection → Layout responsive triggers
  ↓
  Screen Size Changes → useLayout responsive calculations → CSS custom property updates
  ↓
  Capability Detection → DeviceCapabilities integration → MTGOLayout advanced interface decisions
  ↓
  Performance Protection → Throttled updates prevent layout system overload → Smooth performance
  ```
  
  ### Application Layer Flow: Perfect Unified State Inheritance
  
  ```
  DeckArea Controls → onViewModeChange() → updateDeckSideboardViewMode() → useLayout unified state update
  ↓ ↓
  SideboardArea (NO controls) ← viewMode prop ← MTGOLayout consumption ← layout.viewModes.deckSideboard
  ↓
  Same rendering logic (pile/list/card) → Same cardSize prop → Perfect synchronized behavior
  ```
  
  ### Nuclear Z-Index Escalation Flow (Technical Debt Pattern)
  
  ```
  ViewModeDropdown: 600,000-2,000,000 (context detection)
  ↓
  DeckArea sort menu: 500,000 (NUCLEAR Z-INDEX)
  ↓ 
  DeckArea overflow menu: 1,000,000 (MAXIMUM NUCLEAR Z-INDEX)
  ↓
  Manual resize handle hiding → CSS coordination complexity → Technical debt accumulation
  ```
  
  ### Responsive Header Coordination Flow
  
  ```
  Device Detection → AdaptiveHeader patterns → Priority-based control hiding → Overflow menu creation
  ↓ ↓
  DeckArea responsive header → Control priority calculation → Hidden controls → Nuclear z-index strategy
  ↓
  SideboardArea simplified header → No controls → Inherited behavior → Clean integration
  ```
  
  ## 🐛 Problem Diagnosis
  
  ### Unified State Issues
  
  **"Deck and sideboard showing different view modes"**
- **Root Cause:** Unified state not being used correctly or legacy state migration failure
- **Check Files:** `useLayout.ts` (migration logic lines 80-120) → `MTGOLayout.tsx` (unified state consumption) → component integration
- **Debug Pattern:** Verify `updateDeckSideboardViewMode()` usage → check `layout.viewModes.deckSideboard` propagation → validate component prop flow
  **"Card sizes not synchronized between deck and sideboard"**
- **Root Cause:** useCardSizing.ts vs useLayout.ts confusion or incorrect function usage
- **Check Files:** `MTGOLayout.tsx` (dual sizing system integration) → `useLayout.ts` (unified size management) → component size prop application
- **Debug Pattern:** Confirm `updateDeckSideboardCardSize()` usage → avoid useCardSizing for deck/sideboard → validate unified size application
  
  ### CSS Coordination Issues (P2 Technical Debt)
  
  **"Resize handles not working or showing wrong dimensions"**
- **Root Cause:** CSS class vs inline style coordination conflicts, 6px vs 30px width issues
- **Check Files:** `PanelResizing.css` (resize handle styling) → `MTGOLayout.tsx` (inline resize handle styles) → CSS coordination patterns
- **Debug Pattern:** Check CSS class application → verify inline style coordination → validate hit zone vs visual zone dimensions
  **"CSS custom properties not updating during resize"**
- **Root Cause:** Dual CSS update paths from useLayout.ts and useResize.ts creating conflicts
- **Check Files:** `useLayout.ts` (`updateCSSVariables()` function) → `useResize.ts` (`updateCSSVariables()` function) → CSS custom property conflicts
- **Debug Pattern:** Verify both hooks aren't fighting over same CSS properties → check update timing → validate CSS variable application
  **"Layout breaking during percentage calculations"**
- **Root Cause:** Percentage/pixel conversion issues or viewport change handling
- **Check Files:** `useResize.ts` (percentage calculation logic) → `useLayout.ts` (pixel helper functions) → `MTGOLayout.css` (CSS Grid integration)
- **Debug Pattern:** Check percentage conversion math → verify pixel helper usage → validate CSS Grid template coordination
  
  ### Responsive Design Issues
  
  **"Content not hiding correctly when panels are small"**
- **Root Cause:** Complex CSS content hiding patterns not working with actual CSS custom property values
- **Check Files:** `MTGOLayout.css` (content hiding patterns lines 1000+) → CSS custom property value coordination → responsive adaptation logic
- **Debug Pattern:** Check CSS custom property values → verify content hiding CSS patterns → validate size threshold coordination
  **"Device detection causing layout performance issues"**
- **Root Cause:** Device detection not properly throttled or change detection failure
- **Check Files:** `deviceDetection.ts` (throttling logic) → layout responsive integration → performance optimization patterns
- **Debug Pattern:** Verify 250ms throttling working → check change detection logic → validate performance optimization
  
  ### View Mode Coordination Issues
  
  **"ViewModeDropdown not showing correct state or not opening"**
- **Root Cause:** Nuclear z-index strategy conflicts or view mode state synchronization issues
- **Check Files:** `ViewModeDropdown.tsx` (nuclear z-index context detection) → `MTGOLayout.tsx` (view mode state propagation) → CSS z-index conflicts
- **Debug Pattern:** Check z-index context detection → verify view mode state synchronization → validate dropdown positioning
  
  ### Application Layer Integration Issues
  
  **"DeckArea controls working but SideboardArea not responding"**
- **Root Cause:** Perfect by design - SideboardArea inherits unified state without controls
- **Check Files:** `SideboardArea.tsx` (verify no controls, inherited props) → `DeckArea.tsx` (verify control functionality) → unified state propagation
- **Debug Pattern:** Confirm SideboardArea receives same `viewMode`/`cardSize` props → verify inherited behavior → validate unified state synchronization
  **"Overflow menu not opening or conflicting with other UI"**
- **Root Cause:** Nuclear z-index escalation conflicts or responsive calculation issues
- **Check Files:** `DeckArea.tsx` (overflow menu z-index: 1,000,000) → `ViewModeDropdown.tsx` (nuclear z-index conflicts) → responsive calculation logic
- **Debug Pattern:** Check z-index escalation conflicts → verify responsive width calculations → validate overflow menu positioning
  **"Responsive header controls not hiding correctly"**
- **Root Cause:** Priority-based control hiding calculation errors or AdaptiveHeader integration issues
- **Check Files:** `DeckArea.tsx` (responsive logic) → `AdaptiveHeader.tsx` (priority patterns) → responsive calculation integration
- **Debug Pattern:** Verify priority calculations → check available width detection → validate control hiding logic
  **"Resize handles disappearing when menus are open"**
- **Root Cause:** Manual resize handle hiding in DeckArea indicating CSS coordination complexity
- **Check Files:** `DeckArea.tsx` (manual handle hiding code) → CSS coordination conflicts → nuclear z-index strategy impact
- **Debug Pattern:** Check manual resize handle hiding logic → verify CSS coordination complexity → validate z-index conflict resolution
  
  ### Debugging Starting Points
  
  **Unified state problems:** Start with `useLayout.ts` migration logic → `MTGOLayout.tsx` unified state consumption → `DeckArea.tsx` controls → `SideboardArea.tsx` inheritance verification 
  **CSS coordination issues:** Start with `PanelResizing.css` → `MTGOLayout.tsx` inline styles → `DeckArea.tsx` manual resize handle hiding → dual CSS update path analysis 
  **Responsive problems:** Start with `deviceDetection.ts` throttling → `useLayout.ts` responsive calculations → `DeckArea.tsx` responsive header → `AdaptiveHeader.tsx` priority patterns 
  **Nuclear z-index issues:** Start with `ViewModeDropdown.tsx` (600k-2M) → `DeckArea.tsx` sort menu (500k) → overflow menu (1M) → z-index escalation analysis 
  **Performance issues:** Start with `deviceDetection.ts` change detection → resize system throttling → `DeckArea.tsx` responsive calculations → CSS update coordination 
  **View mode issues:** Start with `ViewModeDropdown.tsx` nuclear z-index → `useLayout.ts` view mode state → `DeckArea.tsx` controls → `SideboardArea.tsx` inheritance 
  **Percentage system issues:** Start with `useResize.ts` percentage calculations → `useLayout.ts` pixel helpers → `MTGOLayout.css` CSS Grid integration → application layer grid calculations
  
  ## 🔧 Architecture Details
  
  ### State Management Pattern
  
  **How state is organized:** Unified deck/sideboard state architecture through useLayout.ts with automatic migration from legacy separate deck/sideboard systems, coordinated with useResize.ts for container stabilization and deviceDetection.ts for responsive behavior 
  **State flow:** useLayout.ts manages unified state → MTGOLayout.tsx consumes state → Components receive unified props → CSS custom properties updated by both useLayout and useResize → Real-time rendering coordination 
  **Key state variables:** `deckSideboard` view mode (unified), `deckSideboard` card size (unified), `deckAreaHeightPercent` (percentage-based), panel dimensions, device detection state, CSS custom property coordination
  
  ### Critical Functions & Hooks
  
  #### **Foundation State Management:**
  
  **useLayout.ts unified functions:** `updateDeckSideboardViewMode()`, `updateDeckSideboardCardSize()` - central unified state management replacing separate deck/sideboard functions 
  **useLayout.ts CSS coordination:** `updateCSSVariables()`, `getCalculatedHeights()` - percentage-based calculations and CSS custom property management 
  **useLayout.ts migration:** Automatic migration logic for legacy pixel-based and separate deck/sideboard state with comprehensive backward compatibility 
  **useResize.ts coordination:** `updateCSSVariables()` (conflicts with useLayout), percentage/pixel conversion helpers, container stabilization patterns
  
  #### **Device Integration:**
  
  **deviceDetection.ts performance:** 250ms throttling with change detection to prevent layout system overload during device transitions 
  **deviceDetection.ts capabilities:** DeviceCapabilities.canUseAdvancedInterface() for layout complexity decisions integrated with MTGOLayout.tsx
  
  #### **CSS Architecture:**
  
  **MTGOLayout.css coordination:** CSS custom property integration with complex responsive patterns and content hiding based on size thresholds 
  **PanelResizing.css conflicts:** P2 technical debt from 6px visual styling vs 30px hit zone coordination requiring CSS class and inline style coordination 
  **CSS Grid integration:** Complex grid template patterns coordinated with CSS custom properties for percentage-based layout system
  
  #### **Component Coordination:**
  
  **MTGOLayout.tsx state delegation:** Clean delegation of CSS variable management to foundation hooks, unified state consumption patterns 
  **ViewModeDropdown.tsx nuclear strategy:** Nuclear z-index (600k-2M) with context detection for dropdown reliability in complex layout hierarchy
  
  ### Component Hierarchy
  
  ```
  useLayout.ts (unified state foundation)
  ├── Unified State Management:
  │ ├── deckSideboard view mode (single state for both areas)
  │ ├── deckSideboard card size (single state for both areas)
  │ ├── deckAreaHeightPercent (percentage-based layout)
  │ └── Automatic migration (legacy pixel/separate state support)
  ├── CSS Custom Property Coordination:
  │ ├── --deck-area-height-percent (percentage value)
  │ ├── --deck-area-height (calculated pixel value)
  │ └── --collection-area-height (calculated pixel value)
  └── Integration Coordination:
  ├── useResize.ts (container stabilization + CSS coordination)
  ├── deviceDetection.ts (throttled responsive triggers)
  └── MTGOLayout.tsx (state consumption + component orchestration)
  ├── DeckArea (unified state CONTROLS + nuclear z-index escalation)
  │ ├── Responsive Header (priority-based control hiding)
  │ ├── View Mode Controls (onViewModeChange → updateDeckSideboardViewMode)
  │ ├── Card Size Controls (onCardSizeChange → updateDeckSideboardCardSize)
  │ ├── Sort Menu (z-index: 500,000)
  │ ├── Overflow Menu (z-index: 1,000,000 - MAXIMUM NUCLEAR)
  │ └── Manual Resize Handle Hiding (CSS coordination complexity)
  ├── SideboardArea (unified state INHERITANCE + clean integration)
  │ ├── Title-Only Header (no controls - inherited behavior)
  │ ├── Same View Mode Rendering (inherited from unified state)
  │ ├── Same Card Size Application (inherited from unified state)
  │ └── Clean State Consumption (perfect unified state proof)
  ├── CollectionArea (layout state integration)
  └── ViewModeDropdown (nuclear z-index + view mode coordination)
  └── Context Detection (600k-2M z-index values)
  ```
  
  ### Performance Considerations
  
  **Critical paths:** Unified state management (useLayout.ts), dual CSS update coordination (useLayout + useResize), device detection throttling (250ms), percentage/pixel conversion (useResize.ts), CSS custom property updates (real-time), nuclear z-index escalation (ViewModeDropdown 600k-2M → DeckArea 500k-1M), responsive header calculations (DeckArea priority-based hiding), manual CSS coordination (resize handle hiding) 
  **Optimization patterns:** Device detection change detection and throttling, percentage-based calculations over pixel-based, CSS custom property coordination, unified state to eliminate duplicate systems, automatic migration for backward compatibility, responsive control priority systems, nuclear z-index strategies for dropdown reliability 
  **Known bottlenecks:** Dual CSS update paths creating coordination complexity, CSS coordination between class definitions and inline styles, complex content hiding patterns based on CSS custom property values, nuclear z-index escalation across components (ViewModeDropdown → DeckArea), responsive calculation overhead in DeckArea, manual resize handle coordination indicating CSS architectural strain
  
  ## ⚠️ Current System Status
  
  ### Working Functionality
- ✅ **Unified Deck/Sideboard State:** `updateDeckSideboardViewMode()` and `updateDeckSideboardCardSize()` working correctly with automatic migration
- ✅ **Perfect State Inheritance:** DeckArea controls affect both deck and sideboard, SideboardArea inherits without controls, proving unified state architecture
- ✅ **Percentage-Based Layout:** CSS custom property coordination working with real-time percentage calculations and viewport responsiveness
- ✅ **Device Detection Performance:** 250ms throttling with change detection preventing layout system overload during device transitions
- ✅ **Nuclear Z-Index Strategy:** ViewModeDropdown context detection working with 600k-2M z-index values ensuring dropdown reliability
- ✅ **Nuclear Z-Index Escalation:** DeckArea sort menu (500k) and overflow menu (1M) working with coordinated z-index strategy
- ✅ **Responsive Header Controls:** Priority-based control hiding with overflow menu coordination providing professional responsive behavior
- ✅ **CSS Grid Integration:** Complex grid template coordination with CSS custom properties providing professional responsive layout
- ✅ **Container Stabilization:** useResize.ts percentage/pixel conversion and CSS custom property updates providing smooth resize operations
- ✅ **Manual CSS Coordination:** DeckArea resize handle hiding when menus open preventing z-index conflicts (workaround functioning)
- ✅ **Automatic Migration:** Legacy pixel-based and separate deck/sideboard state conversion working with comprehensive backward compatibility
  
  ### Known Issues
- ⚠️ **P2 CSS Coordination Conflicts:** PanelResizing.css 6px visual styling vs 30px hit zone coordination requires complex CSS class and inline style coordination
- ⚠️ **Dual CSS Update Paths:** Both useLayout.ts and useResize.ts independently update same CSS custom properties creating potential coordination complexity
- ⚠️ **Nuclear Z-Index Escalation:** ViewModeDropdown (600k-2M) → DeckArea sort menu (500k) → overflow menu (1M) indicating systematic z-index management need
- ⚠️ **Manual CSS Coordination Required:** DeckArea manually hides resize handles when menus open, indicating CSS architectural strain requiring workarounds
- ⚠️ **Responsive Calculation Overhead:** DeckArea complex responsive header calculations with priority-based hiding creating performance considerations
- ⚠️ **CSS Architecture Size:** MTGOLayout.css 1,450+ lines with complex responsive patterns approaching maintainability limits
- ⚠️ **Complex Content Hiding:** Size-based CSS patterns require extensive coordination between CSS custom property values and responsive behavior
  
  ### Technical Debt
  
  **Priority Items:**
- **P1:** CSS coordination complexity - dual CSS update paths from useLayout.ts and useResize.ts updating same CSS custom properties
- **P2:** PanelResizing.css conflicts - 6px visual styling vs 30px hit zone coordination requiring CSS class and inline style coordination
- **P2:** Nuclear z-index escalation across components requiring systematic z-index management architecture (ViewModeDropdown 600k-2M → DeckArea 500k-1M)
- **P2:** Manual CSS coordination workarounds - DeckArea resize handle hiding indicates CSS architectural strain requiring manual interventions
- **P3:** MTGOLayout.css size and complexity (1,450+ lines) with extensive responsive patterns and content hiding logic
- **P3:** Responsive calculation overhead in DeckArea with complex priority-based control hiding and overflow menu coordination
- **P3:** Complex content hiding patterns based on CSS custom property values requiring extensive size threshold coordination
- **P4:** Dual sizing systems (useCardSizing vs useLayout) creating potential confusion despite serving different purposes
  
  ### Recent Changes
  
  **January 13, 2025:** Enhanced device detection throttling with 250ms optimization and change detection preventing layout render storms 
  **Performance optimization:** CSS custom property coordination improvements, percentage-based layout system implementation, container stabilization patterns 
  **Architecture enhancement:** Unified deck/sideboard state implementation with automatic migration, nuclear z-index strategy implementation, complex responsive patterns integration
  
  ## 🚀 Development Patterns
  
  ### Common Change Patterns
  
  #### **Adding Unified State Features:**
1. **Start with:** `useLayout.ts` → unified state functions → automatic migration support integration
2. **Then modify:** `MTGOLayout.tsx` → unified state consumption → component prop flow coordination
3. **Test by:** Verify unified state synchronization, automatic migration accuracy, component integration consistency
   
   #### **Adding CSS Coordination Features:**
4. **Start with:** `CSSVariables.css` → CSS custom property definitions → `useLayout.ts` and `useResize.ts` integration
5. **Consider coordination:** Avoid dual CSS update paths, coordinate CSS class vs inline style usage, verify CSS custom property timing
6. **Test by:** CSS custom property updates, real-time coordination accuracy, resize operation smoothness
   
   #### **Adding Responsive Features:**
7. **Start with:** `deviceDetection.ts` → throttling and change detection → layout integration patterns
8. **Then modify:** `AdaptiveHeader.tsx` → priority-based patterns → `DeckArea.tsx` responsive header integration → `MTGOLayout.css` responsive patterns
9. **Test by:** Device transition smoothness, throttling effectiveness, responsive adaptation accuracy, priority-based control hiding
   
   #### **Adding Nuclear Z-Index Features:**
10. **Start with:** `ViewModeDropdown.tsx` → nuclear z-index strategy → context detection logic
11. **Consider escalation:** `DeckArea.tsx` → sort menu (500k) → overflow menu (1M) → manual resize handle hiding coordination
12. **Test by:** Dropdown positioning reliability, z-index conflict avoidance, menu interaction coordination, resize handle conflicts
    
    #### **Adding Layout Dimension Features:**
13. **Start with:** `useLayout.ts` → percentage-based calculations → constraint application
14. **Then modify:** `useResize.ts` → percentage/pixel conversion → container stabilization patterns 
15. **Test by:** Resize operation accuracy, percentage calculation correctness, container stabilization effectiveness
    
    #### **Adding View Mode Features:**
16. **Start with:** `ViewModeDropdown.tsx` → nuclear z-index strategy → context detection logic
17. **Consider integration:** `useLayout.ts` view mode state coordination → component state propagation
18. **Test by:** Dropdown positioning reliability, z-index conflict avoidance, view mode state synchronization
    
    ### File Modification Order
    
    #### **For unified state changes:** `useLayout.ts` (unified functions) → `MTGOLayout.tsx` (state consumption) → `DeckArea.tsx` (controls) + `SideboardArea.tsx` (inheritance) → unified state testing
    
    #### **For CSS coordination changes:** `CSSVariables.css` (definitions) → `useLayout.ts` + `useResize.ts` (coordination) → `DeckArea.tsx` (manual workarounds) → `MTGOLayout.css` (integration) → coordination testing
    
    #### **For responsive changes:** `deviceDetection.ts` (throttling) → `AdaptiveHeader.tsx` (patterns) → `DeckArea.tsx` (responsive header) → `useLayout.ts` (responsive calculations) → `MTGOLayout.css` (responsive patterns) → responsive testing
    
    #### **For nuclear z-index changes:** `ViewModeDropdown.tsx` (600k-2M) → `DeckArea.tsx` (500k-1M escalation) → manual coordination → z-index testing
    
    #### **For resize system changes:** `useResize.ts` (percentage calculations) → `PanelResizing.css` (styling coordination) → `DeckArea.tsx` (manual handle hiding) → `MTGOLayout.tsx` (integration) → resize operation testing
    
    #### **For percentage system changes:** `useLayout.ts` (calculations) → `useResize.ts` (conversion) → `MTGOLayout.css` (CSS Grid integration) → percentage system testing
    
    ### Testing Strategy
    
    **Critical to test:** Unified deck/sideboard state synchronization, CSS custom property coordination accuracy, device detection throttling effectiveness, percentage-based layout calculations, nuclear z-index strategy reliability, automatic migration accuracy, container stabilization during resize operations 
    **Integration tests:** useLayout + useResize CSS custom property coordination, device detection + layout responsive integration, ViewModeDropdown z-index + view mode state synchronization, percentage calculations + CSS Grid rendering, unified state + component integration accuracy 
    **Performance validation:** Device detection throttling (250ms), CSS custom property update timing, resize operation smoothness, responsive pattern efficiency, nuclear z-index strategy stability, automatic migration performance

---

**System Guide Notes:**

- useLayout.ts provides unified deck/sideboard state management replacing separate systems with automatic migration
- useResize.ts coordinates with useLayout.ts but creates dual CSS update paths requiring careful coordination
- deviceDetection.ts uses 250ms throttling with change detection for performance optimization
- MTGOLayout.tsx cleanly delegates CSS variable management to foundation hooks while consuming unified state
- DeckArea.tsx implements unified state controls with complex responsive header and nuclear z-index escalation (500k-1M)
- SideboardArea.tsx provides perfect unified state inheritance proof with no controls, same rendering logic, inherited sizing
- ViewModeDropdown.tsx uses nuclear z-index strategy (600k-2M) with context detection for dropdown reliability
- AdaptiveHeader.tsx provides reusable responsive patterns with priority-based control hiding
- MTGOLayout.css contains complex responsive patterns and content hiding logic creating 1,450+ line maintainability challenge
- PanelResizing.css contains P2 technical debt from CSS class vs inline style coordination conflicts
- CSS custom properties bridge JavaScript state and CSS rendering but are updated by both useLayout and useResize
- Percentage-based layout system replaces legacy pixel-based approach with automatic migration support
- Nuclear z-index escalation across components (ViewModeDropdown → DeckArea) indicates need for systematic z-index management
- Manual CSS coordination workarounds (resize handle hiding) indicate CSS architectural strain requiring systematic solutions
- Perfect unified state inheritance demonstrated by DeckArea (controls) → SideboardArea (inherited) → synchronized behavior
