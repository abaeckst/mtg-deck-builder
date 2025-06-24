# Layout & State Management System Specification

**Status:** Implemented/Enhanced  
**Last Updated:** June 12, 2025  
**Primary Files:** useLayout.ts (305 lines), MTGOLayout.tsx (450 lines), DeckArea.tsx (~200 lines), SideboardArea.tsx (~200 lines), AdaptiveHeader.tsx (201 lines)  
**Dependencies:** Card Display System, Drag & Drop System, Search & Filtering System  
**Performance Targets:** <16ms layout updates, smooth resize operations, instant responsive breakpoints

## Purpose & Intent
**Core Functionality:** Unified state management system for deck builder layout with responsive design and professional MTGO interface consistency  
**Design Philosophy:** Single source of truth for shared UI state (deck/sideboard view modes and sizes), percentage-based responsive layout, and priority-based responsive control hiding  
**MTGO Authenticity Requirements:** Professional dark theme, consistent header styling, MTGO-style control grouping, and authentic visual hierarchy

## Technical Architecture

### File Organization
**Core Files:**
- `useLayout.ts` (305 lines) - Percentage-based layout state with unified deck/sideboard management and automatic migration
- `MTGOLayout.tsx` (450 lines) - Main coordinator orchestrating 5 hook systems and 4 area components with complex integration
- `DeckArea.tsx` (~200 lines) - Enhanced area component with sophisticated responsive header and overflow menu systems
- `SideboardArea.tsx` (~200 lines) - Simplified area component inheriting unified state without duplicate controls  
- `AdaptiveHeader.tsx` (201 lines) - Priority-based responsive control system with dynamic width calculation

**Integration Points:**
- **State System:** useLayout provides unified state → DeckArea/SideboardArea consume → MTGOLayout coordinates
- **Component System:** MTGOLayout orchestrates → Area components render → AdaptiveHeader handles responsive controls
- **Persistence Layer:** LocalStorage integration with automatic migration and error handling

### State Management Patterns
**State Architecture:** Unified state pattern - single view mode and card size controls both deck and sideboard simultaneously  
**Data Flow:** useLayout (state) → MTGOLayout (coordination) → Area components (consumption) → User interactions (callbacks)  
**Performance Optimizations:** Percentage-based calculations, CSS variable updates, stable callback references, constraint validation  
**Error Handling:** LocalStorage fallbacks, migration error recovery, constraint enforcement, device capability detection

### Key Implementation Decisions
**Unified State Management:** Single `deckSideboard` view mode and card size instead of separate deck/sideboard controls - reduces UI complexity and ensures visual consistency  
**Percentage-Based Layout:** Viewport percentage calculations instead of fixed pixels - better responsive behavior and cross-device compatibility  
**Priority-Based Responsive Design:** Controls have priority levels (1=highest, 5=lowest) for systematic hiding - maintains functionality on small screens  
**Nuclear Z-Index Strategy:** Dropdown menus use extremely high z-index values (500000, 1000000) - ensures visibility over all UI elements including resize handles

## User Experience Design

### Core Functionality
**Primary Use Cases:**
1. **Unified View Control:** User changes view mode in deck area → both deck and sideboard update simultaneously → consistent visual experience
2. **Responsive Layout:** User resizes window → controls hide based on priority → overflow menu provides access to hidden functionality → no loss of features
3. **Professional Deck Building:** User interacts with MTGO-style interface → authentic dark theme and control grouping → familiar MTG experience

**Interaction Patterns:**
- **Unified Controls:** Single set of view/size controls affects both deck and sideboard - reduces cognitive load and UI clutter
- **Responsive Adaptation:** Controls dynamically hide/show based on available space - maintains functionality across screen sizes
- **Professional Feedback:** MTGO-authentic styling with proper hover states and visual grouping - familiar interface for MTG players

### Visual Design Standards
**MTGO Authenticity:**
- **Color Scheme:** Professional dark theme (#2a2a2a to #1a1a1a gradients, #444 borders, #ffffff text) matching MTGO interface
- **Typography:** 13-15px font sizes with 600 weight for headers, consistent text shadows for depth
- **Spacing & Layout:** 6-12px gaps, professional border grouping, visual hierarchy through control sectioning

**Visual Feedback:**
- **Hover States:** Background transitions (#333333 to #4a4a4a), subtle transform effects (translateY, scale), smooth 0.2s ease timing
- **Active States:** Enhanced button styling with box shadows, visual grouping through borders and spacing
- **Loading States:** Percentage-based layout updates, smooth CSS transitions, preserved scroll positions
- **Error States:** Device capability detection with fallback messaging, LocalStorage error recovery

**Animation & Transitions:**
- **Performance Requirements:** CSS-based transitions, hardware acceleration, 60fps target for resize operations
- **Timing Standards:** 0.2s ease for hover states, immediate response for layout changes, smooth dropdown animations
- **Accessibility:** Consistent transition timing, focus management, keyboard navigation support

### Responsive Design
**Breakpoint Behavior:**
- **Desktop (1200px+):** Full control visibility, optimal spacing, complete feature access
- **Tablet (768-1199px):** Priority-based control hiding, overflow menu activation, maintained functionality
- **Mobile (767px-):** Device capability detection with fallback message, desktop-only interface protection

**Adaptive Patterns:** Priority-based control hiding (View/Sort priority 4/3, Size priority 2, Actions priority 1), dynamic overflow menu generation, visual grouping preservation

## Performance & Quality Standards

### Performance Benchmarks
**Response Times:**
- **Layout Updates:** <16ms for smooth 60fps performance during resize operations
- **State Changes:** Immediate response for view mode/size changes with CSS transition smoothing
- **Responsive Breakpoints:** Instant control hiding/showing without visual flicker

**Resource Usage:**
- **Memory:** Efficient state management with stable references, proper cleanup of event listeners
- **CPU:** CSS-based animations, percentage calculations cached, minimal re-renders through callback stability
- **Network:** LocalStorage persistence only, no network dependencies for layout state

### Quality Assurance
**Testing Priorities:**
- **HIGH Risk:** Unified state coordination between deck/sideboard, responsive control hiding accuracy, LocalStorage migration, resize handle functionality
- **MEDIUM Risk:** Overflow menu positioning, z-index conflicts, percentage calculation accuracy, CSS class vs inline style coordination
- **LOW Risk:** Visual styling consistency, animation smoothness, hover state timing

**Regression Prevention:**
- **Core Functionality:** Unified state must affect both deck and sideboard simultaneously
- **Integration Points:** Area component coordination with MTGOLayout, proper callback propagation
- **Performance Baselines:** Smooth resize operations, instant responsive breakpoints, stable percentage calculations
- **Style Coordination:** Verify CSS classes take precedence over conflicting inline styles

**Debugging Methodology:**
- **Visual/Functional Integration Issues:** Use DevTools to inspect DOM elements, verify computed styles vs intended styles, check element dimensions and positioning
- **CSS Conflicts:** Compare inline styles vs CSS class definitions, identify override patterns, validate box model calculations
- **Systematic Investigation:** Element existence → style application → visual visibility → functional interaction → integration coordination

## Evolution & Context

### Design Evolution
**Initial Implementation:** Separate deck/sideboard controls with pixel-based layout - led to UI complexity and inconsistent user experience  
**Enhancement Phase:** Unified state system with percentage-based responsive design - simplified UX and improved cross-device compatibility  
**Optimization Phase:** Advanced responsive control system with priority-based hiding - maintained functionality while supporting smaller screens

**Key Changes & Rationale:**
- **Unified State Migration:** Converted from separate deck/sideboard view modes to single `deckSideboard` state - reduces UI complexity and ensures visual consistency
- **Percentage-Based Layout:** Replaced pixel calculations with viewport percentages - better responsive behavior and device compatibility  
- **Priority-Based Responsive:** Implemented systematic control hiding with overflow menus - maintains full functionality on constrained screens

### Current Challenges & Future Considerations
**Known Limitations:** 
- Nuclear z-index approach for dropdown visibility over complex layouts
- Complex responsive detection logic with priority-based control hiding
- Device capability restrictions limiting mobile interface access
- **Resize Handle Technical Debt:** CSS class vs inline style conflicts causing handles to be too small (6px vs intended 30px width), affecting usability

**Future Enhancement Opportunities:** 
- CSS Grid modernization for more efficient responsive layouts
- Advanced animation systems with better performance characteristics
- Improved mobile support with touch-optimized interfaces
- **Resize Handle Architecture:** Resolve CSS coordination conflicts and implement consistent handle sizing

**Architectural Considerations:** 
- Potential CSS-in-JS migration for better style coordination
- Component library integration for standardized UI components
- Performance monitoring systems for layout operation tracking
- **Style Coordination Strategy:** Develop systematic approach for CSS class vs inline style management

### Decision Context
**Why This Approach:** Unified state reduces cognitive load and ensures visual consistency, percentage-based layout provides better responsive behavior, priority-based hiding maintains functionality across screen sizes  
**Alternatives Considered:** Separate deck/sideboard controls (rejected for complexity), fixed pixel layout (rejected for poor responsive behavior), simple responsive breakpoints (rejected for functionality loss)  
**Trade-offs Accepted:** Increased initial complexity for better long-term maintainability, nuclear z-index approach for reliable dropdown visibility, desktop-only interface limiting mobile accessibility