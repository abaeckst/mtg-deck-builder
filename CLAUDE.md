# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Professional React TypeScript MTG (Magic: The Gathering) Deck Builder with MTGO-authentic interface. Production-ready application with text export capabilities and basic screenshot functionality.

**Tech Stack**: React 19.1.0, TypeScript 4.9.5, Create React App, Scryfall API integration, html2canvas

## Essential Commands

### Development
```bash
npm start                    # Launch development server
npm run build               # Production build  
npm test                    # Run test suite
```

### Deployment
```bash
npm run predeploy           # Pre-deployment build
npm run deploy              # Deploy to GitHub Pages
```

### Extended Commands (from project documentation)
```bash
npm run type-check          # TypeScript validation
npm run test:high-risk      # Smart testing (HIGH priority only)
npm run analyze             # Bundle analysis for performance
npm run test:integration    # Cross-system coordination testing  
npm run performance         # Animation and loading performance testing
```

## Code Architecture

### Core Structure
```
src/
├── components/           # React components (40+ specialized components)
│   ├── MTGOLayout.tsx   # Main 4-panel MTGO interface
│   ├── MagicCard.tsx    # Base card display with LazyImage integration
│   ├── FlipCard.tsx     # 3D animation wrapper for double-faced cards
│   ├── DraggableCard.tsx # Interactive wrapper with drag/drop
│   ├── Modal.tsx        # Reusable modal system
│   ├── TextExportModal.tsx # MTGO-format text export
│   └── ScreenshotModal.tsx # Screenshot generation (needs optimization)
├── hooks/               # Custom React hooks (15+ specialized hooks)
│   ├── useCards.ts      # Central coordinator (250 lines, refactored from 580)
│   ├── useSearch.ts     # Search engine with performance optimization  
│   ├── useLayout.ts     # Unified deck/sideboard state management
│   ├── useDragAndDrop.ts # Complete drag system (445 lines)
│   └── useSelection.ts  # Dual selection system (310 lines)
├── services/            # API and utilities
│   └── scryfallApi.ts   # Complete Scryfall abstraction (575 lines)
├── types/              # TypeScript definitions
│   └── card.ts         # Complete type interfaces (520 lines)
├── utils/              # Utility functions
│   ├── deckFormatting.ts # Text export utilities
│   └── screenshotUtils.ts # Screenshot optimization
└── styles/             # CSS architecture
    └── MTGOLayout.css  # Foundation styling (1,450 lines)
```

### Key Architectural Patterns

**Component Extraction Methodology**:
- Extract when component >200 lines with multiple responsibilities
- Used in 3+ locations, or needs independent testing
- Apply React.memo, useMemo, useCallback for performance
- Preserve cross-system integration points

**Performance Optimization**:
- Progressive loading with LazyImage component using Intersection Observer
- 3D hardware acceleration with `will-change: transform`
- React.memo for frequently re-rendering components
- Device detection throttling (250ms)

**State Management**:
- Unified state architecture with single source of truth
- Hook coordination via useCards as central coordinator
- Clean separation of concerns with focused responsibilities
- Effect-based reactivity with stable dependencies

## Development Workflows

### Adding Search & Filter Features
**Pattern**: API changes → useSearch updates → useCards coordination → component integration  
**Files**: `useSearch.ts` → `scryfallApi.ts` → `SearchAutocomplete.tsx`  
**Performance**: Apply timing analysis, wildcard optimization, stored pagination state

### Adding Card Display Features  
**Pattern**: Base component → Progressive loading → 3D animation → Interactive wrapper  
**Files**: `MagicCard.tsx` → `LazyImage.tsx` → `FlipCard.tsx` → `DraggableCard.tsx`  
**Performance**: Intersection Observer, hardware acceleration, event isolation

### Working with the MTGO Interface
**Files**: `MTGOLayout.tsx` (main interface), area components (`CollectionArea.tsx`, `DeckArea.tsx`, `SideboardArea.tsx`)  
**Pattern**: 4-panel layout with resizable panels, professional drag & drop, context menus  
**Styling**: MTGO-authentic theming with clean CSS/JavaScript coordination

## Current Capabilities

**Production-Ready Features**:
- Complete deck building with deck/sideboard management
- Multi-word search with Scryfall API integration
- Professional MTGO-style 4-panel interface
- Multiple view modes (card, pile, list) in all areas
- Universal sorting and filtering system
- Drag & drop with multi-selection support
- Context menus with zone-appropriate actions
- Text export in MTGO format with clipboard integration
- Basic screenshot functionality (layout optimization needed)

**Performance Benchmarks**:
- Search response: <1 second
- 3D animations: 60fps target
- Progressive loading prevents simultaneous API requests
- React.memo optimization prevents unnecessary re-renders

## Key Constraints & Standards

### Code Quality Requirements
- Zero TypeScript compilation errors at all times
- Performance-first approach (no degradation of <1 second search, 60fps animations)
- MTGO authenticity in UI/UX design
- Cross-system integration coordination must be maintained

### Testing Philosophy
- Smart testing: Focus on HIGH risk features only (5min max sessions)
- Risk-based approach: Test critical paths, skip low-impact changes
- Regression prevention: Validate cross-system coordination after changes
- Performance validation: Measure impact on search speed and animation smoothness

### File Modification Protocols
- NEVER modify project knowledge documents (`/Documentation Library/*`, guides)
- ONLY modify project source code (`/src/*`, CSS files, config files)
- Follow proven extraction patterns for component/hook refactoring
- Apply performance optimizations using established patterns

## Technical Debt Awareness

**High Priority Items**:
- Large utility files: scryfallApi.ts (575 lines), card.ts (520 lines)
- Complex hook patterns: useDragAndDrop (445 lines), useSelection (310 lines)
- CSS architecture size: MTGOLayout.css (1,450 lines) approaching maintainability limits

**Successfully Resolved**:
- Hook extraction: useCards (580→250 lines) + 5 focused hooks
- Component extraction: MTGOLayout (925→450 lines) + 3 area components
- Performance optimization: Search, progressive loading, device detection throttling
- CSS coordination: Clean CSS/JavaScript separation patterns established

## Special Notes

**Export Features Status**:
- Text Export: Production-ready with professional formatting and clipboard integration
- Screenshot Export: Basic functionality working, layout optimization algorithm needs refinement

**Known Issue**: Screenshot layout optimization may select suboptimal configurations for certain deck sizes. Future work involves refining the layout selection algorithm and adding user controls for manual layout override.

**API Integration**: Uses Scryfall API with rate limiting, error handling, and wildcard optimization. Includes support for "Custom Standard" format (Standard + Final Fantasy cards).

**3D Animation System**: Hardware-accelerated double-faced card animations with CSS Grid compatibility, container stabilization, and event isolation to prevent system conflicts.