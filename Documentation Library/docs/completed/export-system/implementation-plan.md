Text Export & Screenshot Mode Implementation Plan
Date: June 3, 2025
Session Type: New Feature Development
Estimated Time: 4-6 hours (2-3 sessions)
Dependencies: html2canvas library (~100KB)
🎯 Feature Overview
Text Export Feature:
Location: Button in main deck header (before "Save Deck" and "Clear All")
Functionality: Modal with MTGO format text, auto-copy to clipboard
Format: Deck name placeholder, format info, card type counts, standard MTGO list format
Screenshot Mode Feature:
Location: Button in main deck header area
Functionality: Modal with visual deck layout, image generation and download
Layout: 5 columns (round-robin by mana cost), sideboard in 2 columns below
Quality: High resolution using card large images
🏗️ Implementation Architecture
New Components to Create:
src/components/Modal.tsx - Reusable modal component
src/components/Modal.css - Modal styling
src/components/TextExportModal.tsx - Text export functionality
src/components/ScreenshotModal.tsx - Screenshot generation functionality
src/utils/deckFormatting.ts - Text formatting utilities
src/utils/screenshotUtils.ts - Image generation utilities
Files to Modify:
src/components/MTGOLayout.tsx - Add export buttons and modal integration
package.json - Add html2canvas dependency
📋 Implementation Phases
Phase 1: Dependency & Modal Foundation (45 minutes)
Add html2canvas dependency:
bashnpm install html2canvas @types/html2canvas
Create reusable Modal component:
Large centered modal with overlay
Click-outside-to-close functionality
Escape key handling
Size variants (small/medium/large/fullscreen)
MTGO-style dark theming
Modal Features:
Smooth fade-in/out animations
Proper z-index management
Responsive design
Accessibility (focus management, ARIA labels)
Phase 2: Text Export Implementation (90 minutes)
Create deckFormatting.ts utility:
typescriptinterface DeckExportData {
 deckName: string;
 format: string;
 mainDeck: DeckCardInstance[];
 sideboard: DeckCardInstance[];
}
interface CardTypeCounts {
 creatures: number;
 instants: number;
 sorceries: number;
 artifacts: number;
 enchantments: number;
 planeswalkers: number;
 lands: number;
}
// Functions:
// - formatDeckForMTGO(data: DeckExportData): string
// - calculateCardTypeCounts(cards: DeckCardInstance[]): CardTypeCounts
// - groupCardsByName(cards: DeckCardInstance[]): Map<string, number>
Create TextExportModal component:
Display formatted deck text in textarea
Auto-copy to clipboard on modal open
Copy button with feedback ("Copied!" state)
Card type counts in header
Format information display
Proper MTGO formatting:
// Deck Name: [Placeholder - Untitled Deck]
// Format: Custom Standard
// Creatures: 24, Instants: 8, Sorceries: 4, Lands: 24
4 Lightning Bolt
3 Counterspell
2 Island
Sideboard:
2 Pyroblast
1 Blue Elemental Blast
Integration with MTGOLayout:
Add "Export Text" button in main deck header
Wire up modal state management
Pass current deck data to modal
Phase 3: Screenshot Mode Implementation (120 minutes)
Create screenshotUtils.ts utility:
typescriptinterface ScreenshotLayout {
 mainDeckColumns: DeckCardInstance[][];
 sideboardColumns: DeckCardInstance[][];
}
// Functions:
// - arrangeCardsForScreenshot(mainDeck, sideboard): ScreenshotLayout
// - generateDeckImage(elementId: string): Promise<Blob>
// - downloadImage(blob: Blob, filename: string): void
// - groupUniqueCards(cards: DeckCardInstance[]): Map<string, DeckCardInstance[]>
Create ScreenshotModal component:
Visual deck layout display
5 main deck columns (round-robin by mana cost)
2 sideboard columns below main deck
High-resolution card images (large size)
Quantity indicators on card stacks
Dark MTGO styling background
"Save Image" button with html2canvas integration
Loading state during image generation
Card Layout Logic:
Group cards by unique name
Sort by mana cost, then alphabetically
Distribute round-robin across 5 columns
Display with quantity indicators
Use large resolution card images
No empty slots shown
Integration with MTGOLayout:
Add "Screenshot" button in main deck header
Wire up modal state and image generation
Phase 4: UI Integration & Polish (45 minutes)
Update MTGOLayout.tsx:
Add both export buttons to main deck header
Position "Export Text" before existing buttons
Position "Screenshot" in appropriate location
Manage modal state for both features
Pass deck data to modals
Button Styling:
Match existing MTGO button styles
Appropriate icons or text labels
Hover states and transitions
Proper spacing in header layout
Error Handling:
Clipboard API fallback for older browsers
html2canvas error handling
Empty deck state handling
Loading states and user feedback
🎨 Design Specifications
Modal Design:
Background: Dark MTGO styling (#1a1a1a with overlay)
Size: Large centered modal (80% viewport width/height)
Animation: Smooth fade-in/out (0.3s ease)
Typography: Match existing MTGO font styles
Text Export Modal:
Layout: Title, card counts, textarea, copy button
Textarea: Full deck text, read-only, monospace font
Copy Feedback: Button text changes to "Copied!" for 2 seconds
Screenshot Modal:
Layout: Deck preview area, save button
Card Display: Large images with quantity badges
Columns: 5 for main deck, 2 for sideboard
Spacing: Proper gaps between cards and columns
🧪 Testing Strategy
Text Export Testing:
Various deck sizes (empty, partial, full 60-card)
Different card types and mana costs
Clipboard functionality across browsers
Modal open/close behavior
Screenshot Testing:
Different deck compositions
Large collections (60+ cards)
Empty sideboard scenarios
Image quality and download functionality
Performance with html2canvas
Integration Testing:
Button placement and styling
Modal state management
Data flow from MTGOLayout to modals
Responsive behavior
📊 Success Criteria
Text Export:
 Button appears in correct location in main deck header
 Modal displays properly formatted MTGO text
 Auto-copy to clipboard works on modal open
 Manual copy button works with visual feedback
 Card type counts display correctly
 Format information shows current filter setting
Screenshot Mode:
 Button appears in main deck header area
 Modal displays visual deck layout correctly
 Cards arranged in 5 columns by mana cost round-robin
 Sideboard shows in 2 columns below main deck
 Quantity indicators display on card stacks
 High-resolution images load properly
 Image generation and download works
 Loading states provide good user feedback
General Quality:
 No regressions in existing functionality
 Professional MTGO-style appearance
 Smooth animations and transitions
 Proper error handling and edge cases
 Clean TypeScript compilation
 Responsive design works on different screen sizes
