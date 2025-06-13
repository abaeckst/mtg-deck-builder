# Drag & Drop System Specification

**Status:** Implemented/Enhanced  
**Last Updated:** June 12, 2025  
**Primary Files:** useDragAndDrop.ts (445 lines), DraggableCard.tsx (276 lines), DropZone.tsx (203 lines), DragPreview.tsx (84 lines)  
**Dependencies:** Card Display System, Layout Management, Selection System  
**Performance Targets:** 60fps animations, <150ms drag initiation, smooth visual feedback with requestAnimationFrame

## Purpose & Intent
**Core Functionality:** Provides professional drag-and-drop card movement with sophisticated interaction detection, timing-based behavior differentiation, and MTGO-authentic visual feedback. Handles complex scenarios including rapid double-clicks, multi-card selection, and fast drag movements.  
**Design Philosophy:** Advanced interaction system that distinguishes between clicks, double-clicks, and drag operations through timing and movement analysis. Every interaction should feel predictable with immediate visual feedback while preventing unintended actions.  
**MTGO Authenticity Requirements:** Maintains professional MTG interface standards with 3x drag previews, green/neutral feedback system (no red), subtle animations, and familiar interaction patterns that feel natural to experienced MTG players.

## Technical Architecture

### File Organization
**Core Files:**
- `useDragAndDrop.ts` (445 lines) - Complex interaction system with 5 timing constants, advanced state management, global event tracking, and functional state updates
- `DraggableCard.tsx` (276 lines) - Sophisticated mouse event orchestration with interaction state tracking, instance vs card routing, and visual feedback systems  
- `DropZone.tsx` (203 lines) - Enhanced drop detection with global mouse tracking, boundary buffering, timeout-based leave detection, and centered feedback overlays
- `DragPreview.tsx` (84 lines) - 3x scaled preview with rotation effects, card stacking visualization, and cursor-offset positioning

**Integration Points:**
- **Card Display System:** Uses MagicCard component for consistent rendering with card/instance conversion logic
- **Layout Management:** Coordinates with MTGOLayout areas through zone-based routing and drop validation
- **Selection System:** Supports multi-card operations through selectedCards integration and unified drag handling
- **API Layer:** No direct API integration - operates on local state with deck building validation callbacks

### State Management Patterns
**State Architecture:** Centralized DragState with distributed interaction tracking through refs for performance  
**Data Flow:** Mouse events → Timing analysis → State updates → Visual feedback → Drop validation → Callback execution → State cleanup  
**Performance Optimizations:** RequestAnimationFrame for smooth drag updates, throttled global mouse tracking, ref-based drop zone capture, functional state updates  
**Error Handling:** Escape key cancellation, timeout cleanup, invalid drop prevention, interaction state reset on drag end

### Key Implementation Decisions
**Advanced Timing System:** Five interaction timing constants (double-click: 500ms, rapid-click: 800ms, drag-start: 150ms, movement threshold: 5px, click protection: 300ms) for precise behavior differentiation  
**Functional State Updates:** Critical fix using functional setState to capture current drop zones before reset, preventing drop failures  
**3x Preview Scaling:** Enhanced visual feedback with transform scale(3) and cursor offset positioning for professional feel  
**Global Mouse Tracking:** Document-level listeners with boundary buffering (10px) for fast drag detection across zones  
**Component Isolation:** Drag state managed separately with isBeingDragged flags to prevent interference between card instances  
**No Red Feedback:** Professional design using only green (valid) and neutral (invalid) visual states, avoiding aggressive red styling

## User Experience Design

### Core Functionality
**Primary Use Cases:**
1. **Rapid Double-Click:** User rapidly clicks collection cards to add multiple copies to deck with timing protection preventing drag initiation
2. **Drag & Drop Movement:** User holds card briefly then drags to different zone with 3x preview scaling and real-time drop zone feedback
3. **Multi-Card Operations:** User selects multiple cards then drags group with unified preview showing count indicators and stacked visualization

**Interaction Patterns:**
- **Click Detection:** Event.detail checking + timing analysis distinguishes single clicks from double-clicks immediately on mouseDown
- **Drag Initiation:** 150ms minimum hold OR 5px movement threshold triggers drag mode with immediate 3x preview scaling
- **Fast Drag Handling:** Global mouse tracking with 10px boundary buffer catches fast movements between zones with 30-50ms leave delays
- **Drop Feedback:** Centered overlays with subtle pulse animation appear only for valid drop zones (green) with neutral styling for invalid zones

### Visual Design Standards
**MTGO Authenticity:**
- **Color Scheme:** Dark theme integration using rgba(16,185,129,0.15) for valid drops, rgba(156,163,175,0.01) for neutral zones
- **Typography:** Consistent with 16px bold white text on green backgrounds for drop indicators, 12px for count badges
- **Spacing & Layout:** Maintains grid alignment with 2px card stacking offsets, 2deg rotation effects, and centered drop zone positioning

**Visual Feedback:**
- **Hover States:** Subtle opacity (0.4) and scale(0.95) + rotate(2deg) for cards being dragged with brightness(1.1) filter
- **Active States:** 3x scale drag previews with transform origin top-left, card stacking with 2px offsets and rotation
- **Loading States:** Immediate drag initiation with requestAnimationFrame smooth positioning, no loading delays
- **Error States:** Neutral styling with 1px dashed borders and near-transparent backgrounds, no aggressive red feedback

**Animation & Transitions:**
- **Performance Requirements:** RequestAnimationFrame for 60fps drag tracking, passive event listeners for smooth global tracking
- **Timing Standards:** 0.15s ease transitions for zone highlighting, 0.2s ease for card drag transforms, 1.5s subtle-pulse for drop indicators
- **Accessibility:** Escape key cancellation, no motion-sensitive animations, clear visual state distinctions

### Responsive Design
**Breakpoint Behavior:**
- **Desktop (1200px+):** Full drag & drop functionality with 3x previews, multi-card selection, and complex interaction timing
- **Tablet (768-1199px):** Maintained drag functionality with touch-friendly 10px boundary buffers and simplified timing
- **Mobile (767px-):** Essential drag operations with larger touch targets and reduced complexity interactions

**Adaptive Patterns:** Boundary buffer scaling (10px base, potentially larger for touch), simplified multi-card handling on smaller screens

## Performance & Quality Standards

### Performance Benchmarks
**Response Times:**
- **Drag Initiation:** <150ms maximum delay with movement-based immediate triggering for responsiveness
- **Preview Updates:** 60fps through requestAnimationFrame with throttled global mouse tracking
- **Zone Detection:** <30ms boundary checking with 50ms leave delays for smooth fast movements

**Resource Usage:**
- **Memory:** Cleanup all timeouts and listeners on unmount, ref-based state to prevent unnecessary re-renders
- **CPU:** RequestAnimationFrame throttling, passive event listeners, isolated component re-rendering during drag
- **Network:** No network operations - pure client-side state management with callback-based integrations

### Quality Assurance
**Testing Priorities:**
- **HIGH Risk:** Double-click vs drag differentiation, multi-card selection coordination, drop zone capture during fast movements
- **MEDIUM Risk:** Visual feedback timing, keyboard cancellation, card instance vs base card routing
- **LOW Risk:** Animation smoothness, cursor styling, preview positioning refinements

**Regression Prevention:**
- **Core Functionality:** Timing constants must remain stable, functional state updates for drop zone capture, cleanup patterns
- **Integration Points:** Card/instance routing, selection system coordination, zone validation callbacks
- **Performance Baselines:** 60fps drag tracking, <150ms initiation, smooth zone transitions

## Evolution & Context

### Design Evolution
**Initial Implementation:** Basic drag & drop with simple state management and standard HTML5 drag events
**Enhancement Phase:** Added sophisticated timing system with 5 interaction constants, advanced state management with functional updates, 3x preview scaling
**Optimization Phase:** Implemented global mouse tracking for fast drag detection, ref-based drop zone capture fix, professional visual design with green/neutral feedback

**Key Changes & Rationale:**
- **Timing-Based Interaction System:** Needed to distinguish rapid double-clicks from drag attempts - implemented 5 different timing constants for precise behavior control
- **Functional State Updates:** Critical bug fix where drop zones were reset to null before endDrag could read them - added ref-based capture system
- **3x Preview Scaling:** Enhanced visual feedback making dragged cards more visible and professional feeling - improved user confidence in drag operations
- **Global Mouse Tracking:** Fast drag movements were missing zone boundaries - added document-level listeners with boundary buffering for reliable detection

### Current Challenges & Future Considerations
**Known Limitations:** 
- Complex timing system requires maintenance when adding new interaction types
- Global mouse tracking adds event listeners that need careful cleanup
- Multi-card preview stacking can become visually cluttered with >3 cards

**Future Enhancement Opportunities:** 
- Touch gesture support for mobile devices
- Customizable timing constants for user preferences  
- Advanced preview layouts for large multi-card selections
- Haptic feedback integration for supported devices

**Architectural Considerations:** 
- Consider extracting timing constants to configuration system
- Evaluate performance impact of global mouse tracking on low-end devices
- Plan for future gesture-based interactions while maintaining current mouse precision

### Decision Context
**Why This Approach:** 
- **Timing-Based Detection:** HTML5 drag events insufficient for distinguishing clicks vs drags - custom system provides precise control
- **Functional State Updates:** React's asynchronous state updates caused drop failures - functional updates ensure current state access
- **Global Mouse Tracking:** Component-level events miss fast movements - document listeners with buffering provide reliable zone detection
- **3x Preview Scaling:** Standard drag previews too small for complex card games - enhanced scaling provides professional feedback

**Alternatives Considered:** 
- HTML5 drag API (insufficient timing control)
- Pure CSS transforms (performance limitations)  
- Touch-first design (desktop precision requirements)
- Immediate drag initiation (conflicts with double-click functionality)

**Trade-offs Accepted:** 
- **Complexity vs Reliability:** Accepted sophisticated timing system for robust interaction handling
- **Memory vs Performance:** Added ref tracking for smooth state management over pure functional approaches
- **Global Events vs Encapsulation:** Global mouse tracking for reliable fast drag detection over pure component encapsulation

---

**Current Achievement:** Highly sophisticated drag & drop system with advanced interaction detection, professional visual feedback, and MTGO-authentic user experience  
**Technical Depth:** Complex timing-based state management with performance optimizations and comprehensive error handling  
**User Experience:** Professional-grade interactions with immediate feedback, smooth animations, and intuitive behavior patterns