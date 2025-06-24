# Card Display & Loading System Specification

**Status:** Implemented & Enhanced with Double-Faced Card Flip  
**Last Updated:** January 13, 2025  
**Primary Files:** MagicCard.tsx (312 lines), FlipCard.tsx (~350 lines), LazyImage.tsx (~100 lines), DraggableCard.tsx (276 lines), card.ts (520 lines)  
**Dependencies:** Intersection Observer API, Drag & Drop System, Type Architecture, 3D CSS Transforms  
**Performance Targets:** <200ms image loading initiation, eliminate simultaneous loading, 60fps interactions, 400ms smooth flip animations

## Purpose & Intent
**Core Functionality:** Progressive card display with lazy loading, dynamic sizing, sophisticated interaction handling, and professional 3D flip animations for double-faced Magic cards  
**Design Philosophy:** Performance-first approach eliminating "75 cards loading simultaneously" through viewport detection while maintaining professional MTGO visual standards and authentic card flip interactions  
**MTGO Authenticity Requirements:** Dark theme integration, rarity-based styling, professional quantity indicators, smooth interaction feedback, and realistic card flip animations matching physical card behavior

## Technical Architecture

### File Organization
**Core Files:**
- `MagicCard.tsx` (312 lines) - Base display component with dynamic scaling, quantity systems, and MTGO styling
- `FlipCard.tsx` (~350 lines) - 3D flip animation wrapper with double-faced card detection and professional flip button integration
- `LazyImage.tsx` (~100 lines) - Intersection Observer-based progressive loading with viewport detection
- `DraggableCard.tsx` (276 lines) - Interactive wrapper with sophisticated timing detection, dual identity routing, and FlipCard integration
- `card.ts` (520 lines) - Type foundation with dual identity architecture, progressive loading interfaces, and double-faced card utilities

**Integration Points:**
- **Progressive Loading:** LazyImage → MagicCard → viewport detection eliminates simultaneous loading
- **3D Flip System:** FlipCard → MagicCard → face-specific image rendering and state management
- **Drag & Drop System:** DraggableCard → FlipCard → interaction detection → drag system coordination → visual feedback
- **Type Architecture:** Dual identity (card vs instance) → selection routing → deck/collection behavior differentiation
- **Image Management:** PNG format preference → getCardImageUri utility → face-specific image resolution → consistent quality across sizes

### State Management Patterns
**State Architecture:** Component-level loading states with intersection observer coordination, flip state management, and face-specific rendering  
**Data Flow:** Viewport detection → lazy loading initiation → image load management → display state updates → flip state coordination → face changes  
**Performance Optimizations:** Intersection Observer (50px rootMargin), PNG format preference, consistent image sizing, hardware-accelerated 3D transforms  
**Error Handling:** Graceful degradation to card information display, loading state management, retry mechanisms, flip state preservation

### Key Implementation Decisions
**Progressive Loading Choice:** Intersection Observer with 50px rootMargin for smooth loading anticipation  
**Image Format Strategy:** PNG preference (745×1040) for highest quality with fallback chain  
**Dual Identity Architecture:** Separate card-based vs instance-based selection for collection vs deck contexts  
**Dynamic Scaling System:** Clamped scale factors (0.5x-3.0x) with proportional sizing across all components  
**3D Flip Architecture:** FlipCard wrapper component with hardware acceleration and face-specific state management  
**Container Stabilization:** CSS Grid compatibility through explicit container dimensions and stable positioning contexts

## Double-Faced Card Flip System

### Core Functionality
**Automatic Detection:** `isDoubleFacedCard()` utility identifies cards with `card_faces.length >= 2`  
**Professional Flip Button:** MTGO-style ↻ icon with responsive sizing and hover effects positioned in bottom-right corner  
**3D Animation System:** Hardware-accelerated CSS transforms with 400ms smooth rotation and perspective rendering  
**Face-Specific Rendering:** `getCardFaceImageUri()` utility handles front/back face image resolution with proper fallbacks

### Technical Implementation
**FlipCard Component Architecture:**
```typescript
interface FlipCardProps {
  card: ScryfallCard | DeckCard | DeckCardInstance;
  size?: 'small' | 'normal' | 'large';
  // ... other props inherited from MagicCard
}
```

**3D Animation Specifications:**
- **Perspective:** 1000px for realistic depth perception
- **Rotation Timing:** 400ms total duration with ease-in-out timing
- **Hardware Acceleration:** `will-change: transform` and `transform3d` usage
- **Face Change Logic:** Image switching occurs at 90° rotation (invisible moment)

**Container Stabilization Pattern:**
```typescript
const containerStyles: React.CSSProperties = {
  position: 'relative',
  width: '100%',
  height: '100%',
  minWidth: sizeStyles.width,
  minHeight: sizeStyles.height,
  boxSizing: 'border-box',
  isolation: 'isolate',
  contain: 'layout style',
};
```

### Visual Design Standards
**Flip Button Styling:**
- **Size:** 16px-24px responsive sizing based on card size and scale factor
- **Position:** Bottom-right corner with 4px margins, z-index: 20
- **Colors:** `rgba(64, 64, 64, 0.9)` background with `rgba(74, 74, 74, 0.9)` hover
- **Animation:** `scale(1.05)` hover effect with 0.2s transitions
- **Typography:** Monospace ↻ symbol with proper font-weight

**3D Animation Visual Standards:**
- **Smooth Rotation:** Continuous rotation without visual discontinuity
- **Face Orientation:** Both faces display in correct orientation (no mirroring)
- **Professional Timing:** 400ms total duration matching physical card flip behavior
- **Hardware Acceleration:** GPU-rendered transforms for 60fps performance

### Integration Patterns
**Component Hierarchy:**
```
DraggableCard (interactions)
└── FlipCard (3D animation logic)
    └── MagicCard (pure display)
```

**Event Isolation:**
- Flip button clicks use `stopPropagation()` to prevent selection/drag interference
- 3D transform context isolated from button positioning
- Flip state preserved through all existing interactions (drag, selection, context menu)

**CSS Grid Compatibility:**
- Container stabilization prevents CSS Grid coordinate system conflicts
- Explicit dimensions ensure reliable absolute positioning for flip button
- `isolation: isolate` creates clean stacking context for 3D transforms

## User Experience Design

### Core Functionality
**Primary Use Cases:**
1. **Collection Browsing:** Progressive loading prevents simultaneous image requests, smooth scrolling experience
2. **Deck Building:** Instance-based selection with quantity indicators and drag & drop integration  
3. **Card Inspection:** Dynamic sizing from small (60×84) to large (200×279) with quality preservation
4. **Double-Faced Card Interaction:** Intuitive click-to-flip functionality with professional 3D animations

**Interaction Patterns:**
- **Viewport Loading:** Images load 50px before entering viewport for seamless user experience
- **Drag Detection:** Sophisticated timing system distinguishes clicks, drags, and double-clicks
- **Multi-Selection:** Visual indicators with count badges and pulse animations for large selections
- **Quality Scaling:** PNG format maintains text readability even at small sizes with crisp-edges rendering
- **Card Flipping:** Professional 3D rotation with realistic physics and smooth face transitions

### Visual Design Standards
**MTGO Authenticity:**
- **Color Scheme:** Dark theme (#1a1a1a backgrounds) with professional card borders (#404040)
- **Typography:** Dynamic font scaling (10px-14px) with readable sizing across scale factors
- **Spacing & Layout:** Consistent 8px padding with proportional gap scaling in grid layouts
- **Flip Button Integration:** Professional appearance matching MTGO interface standards

**Visual Feedback:**
- **Hover States:** Subtle white overlay (10% opacity) with smooth 0.2s transitions
- **Active States:** Blue selection borders (#3b82f6) with enhanced box shadows
- **Loading States:** Professional loading placeholders with card information fallback
- **Error States:** Graceful degradation showing card name, type, and mana cost
- **Flip Animations:** Smooth 3D rotations with realistic perspective and timing

**Animation & Transitions:**
- **Performance Requirements:** CSS transitions with hardware acceleration, transform-based scaling
- **Timing Standards:** 0.3s cubic-bezier(0.4, 0, 0.2, 1) for smooth professional feel
- **3D Flip Timing:** 400ms total duration with ease-in-out for realistic card physics
- **Accessibility:** Reduced motion considerations for drag effects, pulse animations, and 3D rotations

### Responsive Design
**Breakpoint Behavior:**
- **Desktop (1200px+):** Full functionality with all sizes (small/normal/large), dynamic scaling, and 3D flip animations
- **Tablet (768-1199px):** Optimized card sizing with maintained interaction capabilities including flip functionality
- **Mobile (767px-):** Touch-optimized interactions with appropriate scale factors and simplified flip button sizing

**Adaptive Patterns:** Grid layouts adjust column templates (max-content vs 1fr) based on area context (collection vs deck), flip button scales proportionally

## Performance & Quality Standards

### Performance Benchmarks
**Response Times:**
- **Image Loading Initiation:** <200ms after viewport detection with 50px anticipation margin
- **Intersection Detection:** Real-time viewport tracking with minimal performance impact
- **Drag Interaction Start:** <100ms from mousedown to drag system coordination
- **3D Flip Animation:** 400ms smooth rotation with 60fps performance target

**Resource Usage:**
- **Memory:** Lazy loading prevents simultaneous 75-card image loading (estimated 50MB+ savings)
- **CPU:** Intersection Observer more efficient than scroll event listeners, hardware-accelerated 3D transforms
- **GPU:** 3D flip animations utilize hardware acceleration for optimal performance
- **Network:** Progressive loading distributes image requests, face-specific image loading

### Quality Assurance
**Testing Priorities:**
- **HIGH Risk:** Progressive loading coordination, drag interaction timing, dual identity routing, 3D flip animation integration
- **MEDIUM Risk:** Image quality across scale factors, quantity indicator positioning, flip button positioning
- **LOW Risk:** Error state appearance, loading placeholder text, flip button hover effects

**Regression Prevention:**
- **Core Functionality:** Viewport detection must prevent simultaneous loading
- **Integration Points:** Drag system coordination, selection routing accuracy, flip animation isolation
- **Performance Baselines:** Image loading distribution, interaction responsiveness, 3D animation performance
- **3D Animation Quality:** Smooth rotation without visual discontinuity, correct face orientation

## Evolution & Context

### Design Evolution
**Initial Implementation:** Basic card display with synchronous image loading causing performance issues
**Enhancement Phase:** Intersection Observer integration, progressive loading system, performance optimization
**Optimization Phase:** PNG format preference, dual identity architecture, sophisticated interaction detection
**3D Flip Implementation:** Double-faced card detection, FlipCard wrapper component, professional 3D animations

**Key Changes & Rationale:**
- **Intersection Observer Addition:** Eliminated simultaneous loading of 75+ cards improving perceived performance
- **Dual Identity System:** Separated collection (card-based) vs deck (instance-based) selection for proper behavior
- **PNG Format Preference:** Higher quality images (745×1040) maintain readability at all scale factors
- **FlipCard Component:** Specialized wrapper for 3D flip functionality with clean separation of concerns
- **Container Stabilization:** CSS Grid compatibility solution for reliable absolute positioning

### Current Challenges & Future Considerations
**Known Limitations:** Complex interaction timing in DraggableCard.tsx, large card.ts type file (520 lines), 3D animation browser compatibility  
**Future Enhancement Opportunities:** Virtual scrolling for thousands of cards, WebP format support, card preview system, VR/AR card inspection  
**Architectural Considerations:** Potential virtualization for massive collections, image caching strategies, accessibility improvements, advanced 3D effects

### Decision Context
**Why This Approach:** Progressive loading eliminates performance bottlenecks while maintaining visual quality and professional appearance, 3D flip animations provide authentic card interaction experience  
**Alternatives Considered:** Virtual scrolling (too complex), WebP format (compatibility concerns), synchronous loading (performance issues), 2D flip animations (less authentic), modal card flip (poor UX)  
**Trade-offs Accepted:** Slightly more complex loading logic for significantly better performance and user experience, additional component layer for 3D flip functionality, CSS Grid positioning complexity for authentic interactions

## Implementation Patterns

### Progressive Loading Pattern
```typescript
// Intersection Observer with viewport anticipation
const observer = new IntersectionObserver(
  (entries) => {
    const [entry] = entries;
    if (entry.isIntersecting) {
      setShouldLoad(true);
      observer.unobserve(container);
    }
  },
  { threshold: 0.1, rootMargin: '50px' }
);
```

### Double-Faced Card Detection
```typescript
const isDoubleFacedCard = (card: ScryfallCard | DeckCard | DeckCardInstance): boolean => {
  const scryfallCard = 'card_faces' in card ? card : card.card;
  return scryfallCard.card_faces && scryfallCard.card_faces.length >= 2;
};
```

### Face-Specific Image Resolution
```typescript
const getCardFaceImageUri = (card: ScryfallCard, faceIndex: number = 0, size = 'normal'): string => {
  if (card.card_faces && card.card_faces[faceIndex]) {
    const face = card.card_faces[faceIndex];
    if (face.image_uris) {
      return face.image_uris.png || face.image_uris[size];
    }
  }
  return getCardImageUri(card, size); // Fallback to existing logic
};
```

### 3D Flip Animation
```typescript
const containerStyles: React.CSSProperties = {
  perspective: '1000px',
  transformStyle: 'preserve-3d',
  transition: 'transform 0.4s ease-in-out',
  transform: `rotateY(${flipRotation}deg)`,
  willChange: 'transform',
};
```

### Container Stabilization for CSS Grid Compatibility
```typescript
const containerStyles: React.CSSProperties = {
  position: 'relative',
  width: '100%',
  height: '100%',
  minWidth: sizeStyles.width,
  minHeight: sizeStyles.height,
  boxSizing: 'border-box',
  isolation: 'isolate',
  contain: 'layout style',
};
```

### Dual Identity Architecture
```typescript
// Routing between card-based and instance-based selection
const cardIsInstance = isCardInstance(card) || isInstance;
const cardInstanceId = isCardInstance(card) ? card.instanceId : instanceId;
const selectionId = getSelectionId(card); // Returns instanceId or cardId as appropriate
```

### Dynamic Scaling System
```typescript
// Proportional scaling with reasonable bounds
const getSizeStyles = (size: 'small' | 'normal' | 'large', scaleFactor: number = 1) => {
  const baseSizes = { small: { width: 60, height: 84 }, /* ... */ };
  const clampedScale = Math.max(0.5, Math.min(3.0, scaleFactor));
  return { width: `${Math.round(baseSize.width * clampedScale)}px`, /* ... */ };
};
```

---

**Current Achievement:** High-performance card display system with progressive loading, professional MTGO styling, sophisticated interaction handling, and authentic 3D double-faced card flip animations  
**Architecture Status:** Dual identity system supporting both collection browsing and deck building contexts with specialized FlipCard wrapper for 3D functionality  
**Performance Status:** Intersection Observer eliminates simultaneous loading, PNG format ensures quality across all scale factors, hardware-accelerated 3D animations provide smooth 60fps flip experiences