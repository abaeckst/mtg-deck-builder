# ClaudeRules.md - MTG Deck Builder Project Guidelines

**Project:** Professional React TypeScript MTG Deck Builder  
**Status:** Phase 4B+ Production-Ready with Enhanced Performance  
**Architecture:** Sophisticated component-based system with progressive loading, 3D animations, and unified state management

---

## 🎯 Project Context & Architecture

### Core Technologies
- **Frontend:** React 18+ with TypeScript 4.9+, Vite build system
- **State Management:** Unified state patterns with progressive loading coordination
- **Performance:** LazyImage progressive loading, 3D hardware-accelerated animations, viewport optimization
- **Styling:** MTGO-authentic theming with clean CSS/JavaScript coordination patterns
- **API:** Scryfall integration with stored pagination state and wildcard optimization

### Current Capabilities ✅
- **3D Card Flip System** - Hardware-accelerated double-faced card animations with CSS Grid compatibility
- **Progressive Loading** - Intersection Observer-based image loading eliminating performance issues
- **Enhanced Performance** - Search <1 second, Load More 422-error prevention, React.memo optimization
- **Professional UI** - MTGO-style 4-panel layout with responsive design and nuclear z-index strategies
- **Advanced Features** - Multi-view modes (card/pile/list), sophisticated filtering, export capabilities

---

## 🚨 Critical Development Constraints

### File Modification Protocols
- **NEVER modify project knowledge documents** (`/docs/*`, session templates, guides)
- **ONLY modify project source code** (`/src/*`, CSS files, config files)
- **Wait for reconciliation signal** before updating any documentation files
- **Follow filename protocols** for Python scripts: state name FIRST, verify exact match

### Code Quality Standards
- **Zero TypeScript errors** - Maintain clean compilation at all times
- **Performance first** - No degradation of <1 second search, 60fps animations
- **MTGO authenticity** - Preserve professional MTG interface standards
- **Cross-system integration** - Maintain coordination between all major systems

### Testing Philosophy
- **Smart testing only** - Focus on HIGH risk features (5min max testing sessions)
- **Risk-based approach** - Test critical paths, skip low-impact changes
- **Regression prevention** - Validate cross-system coordination after changes
- **Performance validation** - Measure impact on search speed, animation smoothness

---

## 📁 Project Architecture Patterns

### Established File Organization
```
src/
├── components/           # UI components with extraction patterns
│   ├── MagicCard.tsx    # Base card display + LazyImage integration
│   ├── FlipCard.tsx     # 3D animation wrapper for double-faced cards
│   ├── LazyImage.tsx    # Progressive loading component
│   └── DraggableCard.tsx # Interactive wrapper with FlipCard integration
├── hooks/               # Extracted focused hooks (5 specialized hooks)
│   ├── useCards.ts      # Central coordinator (250 lines, refactored from 580)
│   ├── useSearch.ts     # Search engine with performance optimization
│   └── useLayout.ts     # Unified deck/sideboard state management
├── services/            # API and utilities
│   ├── scryfallApi.ts   # Complete Scryfall abstraction with pagination
│   └── card.ts          # Types and utilities with 3D support
└── styles/              # CSS architecture with clean coordination
    ├── MTGOLayout.css   # Foundation styling (1,450 lines)
    └── LazyImage.css    # Progressive loading styles
```

### Proven Development Patterns

#### Component Extraction Methodology
**When to Extract:**
1. **Reusability:** Used in 3+ locations
2. **Size:** Component >200 lines with multiple responsibilities
3. **Performance:** Opportunity for memoization or lazy loading
4. **Testing:** Can be tested independently

**How to Extract:**
1. Identify focused responsibility boundaries
2. Create TypeScript interface with proper generics
3. Implement with performance optimizations (React.memo, useMemo, useCallback)
4. Preserve cross-system integration points
5. Test HIGH risk functionality only

#### Performance Optimization Patterns
**Progressive Loading (LazyImage):**
- Intersection Observer with 50px rootMargin
- Viewport-based loading preventing simultaneous requests
- Professional loading states with crisp-edges rendering
- Integration with all card display modes

**3D Animation Optimization:**
- Hardware acceleration with `will-change: transform`
- Container stabilization for CSS Grid compatibility
- Event isolation preventing system conflicts
- 60fps target with 400ms smooth animations

**React Performance:**
- React.memo for components that re-render frequently
- Stable dependencies in hooks to prevent re-render loops
- Memoized returns and callback functions
- Device detection throttling (250ms) for responsive behavior

#### State Management Patterns
**Unified State Architecture:**
- Single source of truth for deck/sideboard coordination
- Automatic migration from legacy separate state systems
- Constraint systems for different contexts
- Clean CSS custom property coordination

**Hook Coordination:**
- useCards as central coordinator managing 5 specialized hooks
- Clean separation of concerns with focused responsibilities
- Pass-through patterns for component integration
- Effect-based reactivity with stable dependencies

---

## 🛠️ Development Workflows

### Adding New Features

#### Search & Filter Features
**Files:** `useSearch.ts` → `scryfallApi.ts` → `SearchAutocomplete.tsx` → `search.ts`
**Pattern:** API changes → useSearch updates → useCards coordination → component integration
**Performance:** Apply timing analysis, wildcard optimization, stored pagination state

#### Card Display Features  
**Files:** `MagicCard.tsx` → `LazyImage.tsx` → `FlipCard.tsx` → `DraggableCard.tsx` → `card.ts`
**Pattern:** Base component → Progressive loading → 3D animation (conditional) → Interactive wrapper
**Performance:** Intersection Observer, hardware acceleration, event isolation

#### Progressive Loading Features
**Files:** `LazyImage.tsx` → `MagicCard.tsx` → view components → `card.ts`
**Pattern:** Viewport detection → progressive rendering → performance optimization
**Performance:** 50px rootMargin, crisp-edges rendering, loading state management

### Debugging Methodologies

#### Visual/Functional Integration Issues
**Pattern:** Systematic DOM investigation → CSS coordination analysis → cross-system impact
**Steps:**
1. Element existence verification
2. CSS class application confirmation  
3. Computed style analysis with DevTools
4. Visual appearance validation
5. Functional interaction testing
6. Integration impact assessment

#### Performance Investigation  
**Pattern:** Timing analysis → re-render detection → optimization implementation
**Steps:**
1. Measure actual vs expected performance
2. Identify unnecessary component updates
3. Verify stable dependencies and memoization
4. Apply progressive loading optimization
5. Validate integration point coordination

#### 3D Animation Debugging
**Pattern:** Hardware acceleration verification → positioning context validation → event isolation
**Steps:**
1. Check `will-change` and GPU rendering
2. Verify transform calculations and perspective
3. Ensure container stabilization working
4. Confirm stopPropagation() prevents conflicts
5. Validate 60fps performance monitoring

---

## ⚠️ Technical Debt Awareness

### Priority Classification
**P1 (Critical):** *Currently: No P1 items - all critical functionality working*

**P2 (High Maintenance Impact):**
- Large utility files: scryfallApi.ts (575 lines), card.ts (520 lines)
- Callback complexity: 30+ callbacks in MTGOLayout requiring systematic management
- ✅ **RESOLVED:** CSS coordination conflicts through clean separation patterns

**P3 (Medium - Architectural Improvements):**
- Nuclear z-index strategy: Extreme values (2,000,000) need systematic approach
- CSS architecture size: MTGOLayout.css (1,450 lines) approaching maintainability limits
- Complex hook patterns: useDragAndDrop (445 lines), useSelection (310 lines)

**P4 (Low - Nice-to-have):**
- Enhanced browser compatibility for 3D animations
- Progressive enhancement patterns for older devices

### Resolution Examples ✅
- **Hook Extraction Success:** useCards (580→250) + 5 focused hooks
- **Component Extraction Success:** MTGOLayout (925→450) + 3 area components
- **Performance Optimization Success:** Search (<1 second), progressive loading, device detection throttling
- **CSS Coordination Resolution:** Clean CSS/JavaScript separation patterns established

---

## 🔧 Essential Commands & Scripts

### Development
```bash
npm start                    # Launch development server
npm run build               # Production build
npm run type-check          # TypeScript validation
npm run test:high-risk      # Smart testing (HIGH priority only)
```

### Quality Assurance
```bash
npm run analyze             # Bundle analysis for performance
npm run test:integration    # Cross-system coordination testing
npm run performance         # Animation and loading performance testing
```

### Debugging
```bash
npm run debug:search        # Search performance analysis
npm run debug:render        # React render loop detection
npm run debug:3d           # 3D animation hardware acceleration testing
```

---

## 🎯 Session Management Protocols

### Mandatory Session Workflow
1. **File Identification:** Reference Code Organization Guide patterns for instant location
2. **Pattern Application:** Apply documented methodologies (extraction, performance, unified state)
3. **Session Documentation:** Create artifact-based logs during development
4. **Quality Assurance:** Risk-based testing focusing on HIGH priority features
5. **Verification:** Confirm cross-system integration preserved

### Anti-Patterns (NEVER DO)
- ❌ Modify project knowledge documents during active development
- ❌ Skip Code Organization Guide reference (causes efficiency loss)
- ❌ Test everything instead of risk-based approach (HIGH priority only)
- ❌ Make destructive changes without explicit permission
- ❌ Continue debugging >3 attempts without requesting additional context
- ❌ Skip proven pattern application when relevant opportunity exists

### Success Criteria
- ✅ Zero TypeScript compilation errors maintained
- ✅ Performance benchmarks preserved (search <1 second, 60fps animations)
- ✅ Cross-system integration coordination maintained
- ✅ MTGO authenticity standards upheld
- ✅ Technical debt priorities respected and systematically addressed

---

## 📚 Key Reference Patterns

### Component Extraction
**Trigger:** 200+ lines with multiple responsibilities
**Process:** Boundary identification → Interface creation → Performance optimization → Integration preservation
**Example:** MTGOLayout (925→450) + CollectionArea + DeckArea + SideboardArea

### Performance Optimization  
**Trigger:** >1 second response times, <60fps animations, memory issues
**Process:** Timing analysis → Bottleneck identification → Optimization implementation → Validation
**Example:** Progressive loading implementation, React.memo optimization, device detection throttling

### Unified State Management
**Trigger:** Duplicate state, synchronization issues, complex coordination
**Process:** Single source identification → Migration implementation → Component synchronization → Validation
**Example:** Unified deck/sideboard state with automatic legacy migration

### 3D Animation Integration
**Trigger:** Double-faced cards, visual enhancement needs, interactive experiences
**Process:** Hardware acceleration setup → Container stabilization → Event isolation → Performance validation
**Example:** FlipCard component with CSS Grid compatibility and cross-system coordination

---

**Project Philosophy:** Systematic development with proven patterns, performance-first implementation, and architectural integrity preservation through established methodologies and comprehensive technical debt management.