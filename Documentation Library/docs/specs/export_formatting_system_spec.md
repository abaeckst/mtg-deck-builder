# Export & Formatting System Specification

**Status:** Implemented/Enhanced  
**Last Updated:** June 12, 2025  
**Primary Files:** `deckFormatting.ts` (180 lines), `screenshotUtils.ts` (850 lines), `TextExportModal.tsx`, `ScreenshotModal.tsx`  
**Dependencies:** Card Display & Loading System, Layout & State Management System  
**Performance Targets:** <1 second text export, <5 seconds screenshot generation, responsive UI during operations

## Purpose & Intent
**Core Functionality:** Professional deck export capabilities supporting both MTGO-compatible text format and high-quality screenshot generation for deck sharing and archival  
**Design Philosophy:** Dual export approach balancing professional tournament requirements (text format) with modern sharing expectations (visual screenshots)  
**MTGO Authenticity Requirements:** Text exports must be 100% MTGO-compatible with proper formatting, card grouping, and metadata inclusion

## Technical Architecture

### File Organization
**Core Files:**
- `deckFormatting.ts` (180 lines) - Text export utilities with MTGO format compliance, card grouping, and clipboard integration
- `screenshotUtils.ts` (850 lines) - Advanced screenshot generation with aggressive space optimization, mathematical layout calculation, and html2canvas integration
- `TextExportModal.tsx` - Modal interface for text export with auto-copy functionality and clipboard status feedback
- `ScreenshotModal.tsx` - Full-viewport screenshot modal with dynamic card sizing and layout optimization

**Integration Points:**
- **Card Display System:** Uses MagicCard component for consistent visual rendering in screenshots
- **Layout System:** Integrates with MTGOLayout via export button handlers and modal state management
- **Drag & Drop System:** Independent of drag operations, focuses on static deck representation
- **API Layer:** No external dependencies, operates entirely on local deck state

### State Management Patterns
**State Architecture:** Modal-based with local state management for export operations, no persistent state required  
**Data Flow:** Deck instances → Formatting utilities → Export output (text/image) → User delivery (clipboard/download)  
**Performance Optimizations:** Aggressive space utilization algorithms, progressive image loading, CORS-handling fallbacks  
**Error Handling:** Comprehensive fallback systems for clipboard operations, canvas generation, and cross-origin image issues

### Key Implementation Decisions
**Text Export Approach:** MTGO-native format with card grouping, alphabetical sorting, and comprehensive metadata  
**Screenshot Strategy:** Mathematical optimization prioritizing maximum card size within viewport constraints  
**Canvas Generation:** Multiple configuration fallbacks (CORS/non-CORS) ensuring screenshot success across environments  
**User Experience:** Auto-copy on text modal open, full-viewport screenshot view, immediate feedback systems

## User Experience Design

### Core Functionality
**Primary Use Cases:**
1. **MTGO Import:** Text export with exact format compliance for direct import into Magic Online
2. **Deck Sharing:** High-quality screenshot generation for social media, forums, and deck database submission  
3. **Archival:** Professional documentation of deck configurations with complete card visibility

**Interaction Patterns:**
- **Text Export:** Single-click export → Auto-copy to clipboard → Immediate feedback → Manual copy fallback
- **Screenshot Generation:** Full-screen preview → Automatic optimization → Visual verification → Close when satisfied
- **Modal Management:** Non-blocking operation, escape key support, overlay click handling

### Visual Design Standards
**MTGO Authenticity:**
- **Text Format:** Exact MTGO compliance with card quantities, alphabetical sorting, and sideboard separation
- **Screenshot Layout:** Professional grid arrangement with consistent card sizing and optimal space utilization
- **Color Scheme:** Dark theme consistency (#1a1a1a background) with professional card presentation

**Visual Feedback:**
- **Copy Status:** Real-time clipboard operation feedback (Copying... → Copied! → Copy Failed)
- **Generation Progress:** Non-blocking UI with error state display for failed operations
- **Layout Optimization:** Dynamic card sizing with mathematical precision for maximum visibility
- **Modal States:** Full-viewport screenshot mode with centered close button and smooth transitions

**Animation & Transitions:**
- **Performance Requirements:** Smooth modal transitions, no animation during canvas generation for performance
- **Timing Standards:** Immediate feedback (<100ms), clipboard operations complete within 1 second
- **Accessibility:** Escape key support, click-outside-to-close, keyboard navigation

### Responsive Design
**Breakpoint Behavior:**
- **Desktop (1200px+):** Full functionality with aggressive space optimization and maximum card sizes
- **Tablet (768-1199px):** Responsive modal sizing with adjusted card layout algorithms
- **Mobile (767px-):** Text export only (screenshot generation requires larger screens for optimal results)

**Adaptive Patterns:** Screenshot modal uses full viewport dimensions for maximum space utilization regardless of screen size

## Performance & Quality Standards

### Performance Benchmarks
**Text Export Operations:**
- **Format Generation:** <100ms for typical 75-card deck, <500ms for maximum size decks
- **Clipboard Operations:** <1 second including fallback attempts, immediate user feedback
- **Modal Rendering:** <50ms modal appearance, instant text display

**Screenshot Generation:**
- **Layout Calculation:** <200ms mathematical optimization for any deck size combination
- **Canvas Generation:** <5 seconds including image loading, CORS handling, and fallback attempts
- **Memory Management:** Proper URL.revokeObjectURL cleanup, canvas disposal after generation

**Resource Usage:**
- **Memory:** Efficient card grouping algorithms, temporary canvas creation only during generation
- **CPU:** Mathematical layout optimization with smart configuration generation (not brute force)
- **Network:** Zero network dependencies during export operations, works entirely offline

### Quality Assurance
**Testing Priorities:**
- **HIGH Risk:** MTGO format compliance, clipboard operations across browsers, canvas generation fallbacks
- **MEDIUM Risk:** Screenshot layout optimization, modal interaction patterns, error state handling
- **LOW Risk:** Visual polish, animation timing, modal positioning

**Regression Prevention:**
- **Core Functionality:** Text format must remain MTGO-compatible, screenshot must handle all deck size combinations
- **Integration Points:** Modal state management, export button handlers, deck state access
- **Performance Baselines:** Text export <1s, screenshot calculation <200ms, no memory leaks

## Evolution & Context

### Design Evolution
**Initial Implementation:** Basic text export with simple card listing and manual clipboard copying
**Enhancement Phase:** Added MTGO format compliance, card type counting, automatic clipboard operations, and comprehensive error handling
**Optimization Phase:** Implemented aggressive screenshot space optimization with mathematical layout calculation replacing heuristic approaches

**Key Changes & Rationale:**
- **Mathematical Layout Optimization:** Replaced heuristic algorithms with comprehensive space utilization calculation for maximum card visibility
- **CORS Handling:** Added multiple canvas configuration fallbacks to handle cross-origin card images reliably
- **Auto-Copy Functionality:** Eliminated manual copy step for text exports, improving user workflow efficiency

### Current Challenges & Future Considerations
**Known Limitations:** Screenshot generation requires desktop/laptop for optimal results, limited mobile support for complex layouts  
**Future Enhancement Opportunities:** Direct social media integration, multiple export formats (.dec, .dek), batch export operations  
**Architectural Considerations:** Screenshot utility complexity (850 lines) suggests potential for modular extraction if additional export formats added

### Decision Context
**Why This Approach:** Dual export strategy serves both competitive players (MTGO text) and casual sharers (screenshots) with professional quality standards  
**Alternatives Considered:** Single export format, third-party screenshot services, simplified layout algorithms  
**Trade-offs Accepted:** Screenshot utility complexity for maximum space optimization, auto-copy behavior for streamlined workflow, full-viewport modal for maximum card visibility

---

## Advanced Technical Details

### Screenshot Layout Algorithm
**Mathematical Optimization Process:**
1. **Configuration Generation:** Comprehensive layout options prioritizing fewer rows (maximum width utilization)
2. **Binary Search Scaling:** Find maximum scale factor that fits viewport without scrolling
3. **Space Utilization Scoring:** Primary metric is card size (bigger cards always win among fitting layouts)
4. **DOM Verification:** Post-render validation with automatic scale reduction if overflow detected

**Layout Constraints:**
- **Card Size Limits:** 0.5x minimum scale (readability), 4.0x maximum scale (practical limits)
- **Column Distribution:** Dynamic columns based on unique card estimation (60% main deck, 70% sideboard)
- **Responsive Adaptation:** Full viewport utilization with priority-based space allocation

### Text Export Format Structure
**MTGO Compliance Requirements:**
```
// Deck Name: [Name]
// Format: [Format]
// [Card Type Summary]

[Quantity] [Card Name]
[...sorted alphabetically...]

Sideboard:
[Quantity] [Card Name]
[...sorted alphabetically...]
```

**Card Processing Pipeline:**
1. **Grouping:** Map-based card aggregation by name with quantity counting
2. **Type Analysis:** Card type classification with comprehensive type line parsing
3. **Sorting:** Alphabetical within groups, maintaining MTGO import compatibility
4. **Formatting:** Professional metadata inclusion with format display names

### Error Handling & Fallback Systems
**Clipboard Operation Fallbacks:**
1. **Modern API:** navigator.clipboard.writeText() for secure contexts
2. **Legacy Fallback:** document.execCommand('copy') with temporary textarea
3. **Manual Fallback:** User instruction display with pre-selected text

**Canvas Generation Fallbacks:**
1. **CORS-Enabled:** useCORS: true, allowTaint: false, 2x scale
2. **Permissive:** useCORS: false, allowTaint: true, 2x scale  
3. **Minimal:** Basic configuration with logging, 1x scale

---

**Current Achievement:** Professional dual-export system with mathematical layout optimization and 100% MTGO format compliance  
**Development Status:** Feature-complete with advanced optimization algorithms and comprehensive error handling  
**Architecture Quality:** Well-structured utilities with clear separation between text and visual export concerns