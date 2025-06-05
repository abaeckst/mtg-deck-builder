Dynamic Screenshot Layout Implementation Plan & Handoff
Date: June 3, 2025
Session: Screenshot Dynamic Sizing Implementation
Status: 📋 READY FOR IMPLEMENTATION
Priority: HIGH - Complete responsive screenshot layout
🎯 Project Goals
Primary Objective: Create a dynamic screenshot modal that automatically sizes cards to fit all deck cards (60 main + 15 sideboard) on screen without scrolling, while maintaining card name readability.
Secondary Objective: Provide user override controls (S/M/L) for fine-tuning when automatic sizing isn't perfect.
📋 Current Status Analysis
What's Working ✅
Modal opens correctly with proper fullscreen layout
Card arrangement logic distributes cards properly (5 columns main, 2 columns sideboard)
Card images display in preview (CORS issue resolved for preview, just not download)
Basic spacing and structure in place
What Needs Implementation 🔧
Dynamic size calculation based on available viewport space
Minimum readability constraints to ensure card names are readable
S/M/L override controls for user fine-tuning
Scrolling fallback when cards would be too small to read
Responsive behavior for different screen sizes
🏗️ Technical Implementation Plan
Phase 1: Dynamic Size Calculation Engine (60-90 minutes)
Step 1: Viewport Measurement Utilities
Create functions to measure available space:
typescriptinterface ViewportDimensions {
 modalWidth: number;
 modalHeight: number;
 availableWidth: number;
 availableHeight: number;
 headerHeight: number;
 controlsHeight: number;
 marginsTotal: number;
}
const measureAvailableSpace = (): ViewportDimensions => {
 // Measure actual modal dimensions
 // Account for headers, controls, margins
 // Return usable card area dimensions
};
Step 2: Card Layout Mathematics
Calculate optimal card dimensions:
typescriptinterface CardLayoutCalculation {
 cardsPerMainColumn: number;
 cardsPerSideboardColumn: number;
 maxCardsPerColumn: number;
 optimalCardHeight: number;
 optimalCardWidth: number;
 calculatedScale: number;
 needsScrolling: boolean;
}
const calculateOptimalCardSize = (
 mainDeckCount: number,
 sideboardCount: number,
 availableSpace: ViewportDimensions
): CardLayoutCalculation => {
 // Main deck: 5 columns, distribute cards evenly
 // Sideboard: 2 columns, distribute cards evenly
 // Find tallest column to determine height requirements
 // Calculate largest card size that fits without scrolling
 // Check against minimum readability threshold
};
Step 3: Readability Constraints
Define minimum card sizes for readability:
typescriptconst READABILITY_CONSTRAINTS = {
 minCardWidth: 100, // Minimum width for readable card names
 minCardHeight: 140, // Minimum height for readable card names
 minScaleFactor: 0.5, // Never go below 50% of normal size
 maxScaleFactor: 2.0, // Never go above 200% of normal size
};
Phase 2: Size Override Controls (30-45 minutes)
User Control Interface
Add S/M/L controls below modal header:
typescriptinterface SizeOverride {
 mode: 'auto' | 'small' | 'medium' | 'large';
 scaleFactor: number;
}
const SIZE_OVERRIDES = {
 small: 0.6, // 60% of normal card size
 medium: 0.8, // 80% of normal card size 
large: 1.0, // 100% of normal card size
};
Control Integration
jsx<div className="screenshot-size-controls">
 <span>Size:</span>
 <button className={sizeMode === 'auto' ? 'active' : ''} onClick={() => setSizeMode('auto')}>Auto</button>
 <button className={sizeMode === 'small' ? 'active' : ''} onClick={() => setSizeMode('small')}>S</button>
 <button className={sizeMode === 'medium' ? 'active' : ''} onClick={() => setSizeMode('medium')}>M</button>
 <button className={sizeMode === 'large' ? 'active' : ''} onClick={() => setSizeMode('large')}>L</button>

</div>
Phase 3: Scrolling Fallback System (30 minutes)
Scrolling Decision Logic
typescriptconst determineScrollingNeeded = (
 calculatedScale: number,
 overrideScale: number | null
): boolean => {
 const finalScale = overrideScale || calculatedScale;
 return finalScale < READABILITY_CONSTRAINTS.minScaleFactor;
};
Scrollable Container Implementation
jsx<div 
className="screenshot-preview"
 style={{
 maxHeight: needsScrolling ? '90vh' : 'auto',
 overflowY: needsScrolling ? 'auto' : 'hidden',
 padding: needsScrolling ? '12px' : '8px'
 }}
>
 {/* Card layout content */}
</div>
Phase 4: Integration & Polish (30-45 minutes)
React State Management
typescriptconst [sizeMode, setSizeMode] = useState<'auto' | 'small' | 'medium' | 'large'>('auto');
const [viewportDimensions, setViewportDimensions] = useState<ViewportDimensions | null>(null);
const [cardLayout, setCardLayout] = useState<CardLayoutCalculation | null>(null);
// Recalculate on mount and window resize
useEffect(() => {
 const handleResize = () => {
 const dimensions = measureAvailableSpace();
 const layout = calculateOptimalCardSize(mainDeck.length, sideboard.length, dimensions);
 setViewportDimensions(dimensions);
 setCardLayout(layout);
 };

handleResize();
 window.addEventListener('resize', handleResize);
 return () => window.removeEventListener('resize', handleResize);
}, [mainDeck.length, sideboard.length]);
Final Card Rendering
typescriptconst getFinalCardProps = () => {
 if (!cardLayout) return { size: 'normal', scaleFactor: 1.0 };

let finalScale = cardLayout.calculatedScale;

if (sizeMode !== 'auto') {
 finalScale = SIZE_OVERRIDES[sizeMode];
 }

return {
 size: finalScale > 0.8 ? 'normal' : 'small',
 scaleFactor: finalScale
 };
};
📋 Files to Modify/Create
Files to Update:
src/components/ScreenshotModal.tsx - Main modal component with dynamic sizing
src/utils/screenshotUtils.ts - Add viewport measurement and calculation utilities
New Functions to Add:
typescript// In screenshotUtils.ts
export const measureAvailableSpace = (): ViewportDimensions;
export const calculateOptimalCardSize = (...): CardLayoutCalculation;
export const determineScrollingNeeded = (...): boolean;
// In ScreenshotModal.tsx 
const handleSizeModeChange = (mode: string) => void;
const getFinalCardProps = () => CardProps;
🎨 Visual Design Specifications
Size Controls Styling
css.screenshot-size-controls {
 display: flex;
 align-items: center;
 gap: 8px;
 margin-bottom: 12px;
 font-size: 14px;
 color: #e0e0e0;
}
.screenshot-size-controls button {
 padding: 4px 8px;
 background: #2a2a2a;
 border: 1px solid #444;
 border-radius: 4px;
 color: #e0e0e0;
 cursor: pointer;
}
.screenshot-size-controls button.active {
 background: #3b82f6;
 border-color: #3b82f6;
}
Scrollable Container Styling
css.screenshot-preview {
 background: #1a1a1a;
 border-radius: 8px;
 border: 1px solid #333;
}
.screenshot-preview::-webkit-scrollbar {
 width: 8px;
}
.screenshot-preview::-webkit-scrollbar-track {
 background: #2a2a2a;
 border-radius: 4px;
}
.screenshot-preview::-webkit-scrollbar-thumb {
 background: #555;
 border-radius: 4px;
}
🧪 Testing Strategy
Phase 1 Testing:
Test calculation accuracy with different deck sizes (20, 40, 60, 75 cards)
Verify card readability at calculated sizes
Test viewport measurement on different screen sizes
Phase 2 Testing:
Test S/M/L override controls
Verify scaling applies correctly to all cards
Test mode switching behavior
Phase 3 Testing:
Test scrolling triggers at appropriate thresholds
Verify scrolling performance with large decks
Test edge cases (very small screens, very large decks)
Integration Testing:
Test modal opening/closing
Test window resizing behavior
Test with empty decks, partial decks, full decks
Test control responsiveness and visual feedback
📊 Success Criteria
Functional Requirements:
 Cards automatically size to fit all deck cards on screen
 Card names are clearly readable at calculated sizes
 S/M/L override controls work correctly
 Scrolling activates when cards would be too small
 Layout responsive to window resizing
 Performance remains smooth with large decks
User Experience Requirements:
 Default "auto" sizing works well for most screen sizes
 Override controls are intuitive and responsive
 Scrolling feels natural when needed
 Visual feedback for active size mode
 No layout jumping or flashing during size changes
Technical Requirements:
 Clean TypeScript compilation with proper types
 Efficient calculations that don't impact performance
 Proper React state management and useEffect usage
 Responsive design works on standard screen ratios
🚀 Handoff Instructions for Next Session
Session Start Protocol:
Verify current state - Ensure screenshot modal still opens and displays cards
