# MTG Deck Builder - Code Organization Guide

**Created:** June 7, 2025 | **Performance Optimized:** June 9, 2025 | **Enhanced:** June 12, 2025  
**Purpose:** Streamlined reference for codebase organization, integration points, and proven development patterns  
**Repository:** https://github.com/abaeckst/mtg-deck-builder  

## 🎯 Quick Reference - Development Decision Tree

### Adding Search Features
**Spec:** Request Search & Filtering System specification for design intent and performance standards  
**Files:** `useSearch.ts` (extracted hook + performance optimized) → `scryfallApi.ts` (API + Load More) → `SearchAutocomplete.tsx` → `search.ts` (types)  
**Pattern:** API changes → useSearch updates → useCards coordination → component integration  
**Performance:** Apply timing analysis, clean parameter management, wildcard optimization

### Adding Filter Features  
**Spec:** Request Search & Filtering System specification for coordination patterns and UX standards  
**Files:** `useFilters.ts` (excellent example) → `FilterPanel.tsx` → `CollapsibleSection.tsx` → `scryfallApi.ts`  
**Pattern:** Filter state → UI components → API integration → useCards coordination  
**Reactivity:** Clean search triggers on filter changes

### Adding Card Display Features
**Spec:** Request Card Display & Loading System specification for progressive loading and display standards  
**Files:** `MagicCard.tsx` (base + lazy loading) → `LazyImage.tsx` (progressive loading) → `DraggableCard.tsx` (enhanced UX) → `card.ts` (types)  
**Pattern:** Base component → progressive loading → interactive wrapper → type support  
**Performance:** Intersection Observer, consistent normal-size images, 3x preview scaling

### Adding Pagination Features
**Spec:** Request Search & Filtering System specification for pagination coordination patterns  
**Files:** `usePagination.ts` (extracted) → `useSearch.ts` (state coordination) → `scryfallApi.ts` (422 prevention)  
**Pattern:** Pagination state → search coordination → API decision logic  
**Performance:** Stored pagination state, Smart Card Append for scroll preservation

### Adding Hook Features
**Files:** Review `useCards.ts` (250 lines coordinator) → assess if new hook needed → extract if growing large  
**Pattern:** Assess responsibility → extract focused hooks → maintain clean APIs  
**Performance:** Monitor re-render loops, stable dependencies, proper memoization

### Adding Layout/State Features
**Spec:** Request Layout & State Management System specification for unified state patterns and responsive design  
**Files:** `useLayout.ts` (unified state) → `DeckArea.tsx`/`SideboardArea.tsx` → `MTGOLayout.tsx` (coordinator)  
**Pattern:** Single state source → component synchronization → coordinator integration  
**Advanced:** Automatic migration, constraint systems, responsive overflow

### Adding Export Features
**Spec:** Request Export & Formatting System specification for format standards and quality requirements  
**Files:** `deckFormatting.ts` → `screenshotUtils.ts` (850 lines - complex) → modal components  
**Pattern:** Utility functions → modal components → main layout integration

### Adding Drag & Drop Features
**Spec:** Request Drag & Drop System specification for visual feedback standards and interaction patterns  
**Files:** `useDragAndDrop.ts` (445 lines - complex) → `DraggableCard.tsx` → `DropZone.tsx`  
**Pattern:** Drag logic → card behavior → drop targets  
**Enhanced:** 3x transform scaling, zone-relative centering, component isolation

## 📁 Complete File Organization Matrix

### 🎨 Components Layer (`src/components/`) - 20 Files

#### Core Layout (Extracted Architecture)
| File | Size | Responsibility | Status |
|------|------|----------------|--------|
| `MTGOLayout.tsx` | 450 lines | **Simplified coordinator** (refactored from 925) | ✅ Excellent |
| `MTGOLayout.css` | 1,450 lines | **Complete styling foundation** | ✅ Working |
| `CollectionArea.tsx` | ~200 lines | Collection logic + Load More (extracted) | ✅ Good |
| `DeckArea.tsx` | ~200 lines | Unified controls + responsive overflow (extracted) | ✅ Good |
| `SideboardArea.tsx` | ~200 lines | Simplified header + unified state (extracted) | ✅ Excellent |
| `FilterPanel.tsx` | 368 lines | Professional filter interface | ✅ Good |
| `AdaptiveHeader.tsx` | 201 lines | Responsive header controls | ✅ Excellent |
| `CollapsibleSection.tsx` | 52 lines | Reusable collapsible UI | ✅ Excellent |

#### Card Display & Interaction (Performance Enhanced)
| File | Size | Responsibility | Status |
|------|------|----------------|--------|
| `MagicCard.tsx` | 312 lines | Base card display + lazy loading | ✅ Enhanced |
| `LazyImage.tsx` | ~100 lines | Progressive image loading (new) | ✅ Excellent |
| `DraggableCard.tsx` | 276 lines | Interactive cards + 3x preview | ✅ Enhanced |
| `ListView.tsx` | 318 lines | Universal tabular view | ✅ Good |
| `PileView.tsx` | 289 lines | MTGO-style pile organization | ✅ Good |
| `PileColumn.tsx` | 156 lines | Individual pile column | ✅ Good |

#### Advanced UI Components
| File | Size | Responsibility | Status |
|------|------|----------------|--------|
| `ViewModeDropdown.tsx` | ~150 lines | Context-aware MTGO dropdown (new) | ✅ Excellent |
| `DropZone.tsx` | 203 lines | Enhanced drop zones + centered feedback | ✅ Enhanced |
| `DragPreview.tsx` | 84 lines | 3x larger visual drag preview | ✅ Enhanced |
| `SearchAutocomplete.tsx` | 114 lines | Enhanced search input | ✅ Good |
| `SubtypeInput.tsx` | 191 lines | Autocomplete multi-select | ✅ Good |

### 🔧 Hooks Layer (`src/hooks/`) - 11 Files

#### Core Data Management (Refactored + Performance Optimized)
| File | Size | Responsibility | Status |
|------|------|----------------|--------|
| `useCards.ts` | 250 lines | **Coordination hub** (refactored from 580) | ✅ Excellent |
| `useSearch.ts` | 350 lines | Core search + API + stored state | ✅ Enhanced |
| `usePagination.ts` | 120 lines | Progressive loading (extracted) | ✅ Excellent |
| `useCardSelection.ts` | 50 lines | Selection state (extracted) | ✅ Excellent |
| `useSearchSuggestions.ts` | 70 lines | Autocomplete + history (extracted) | ✅ Excellent |
| `useFilters.ts` | 120 lines | Filter state (pre-existing excellent example) | ✅ Excellent |

#### UI State Management
| File | Size | Responsibility | Status |
|------|------|----------------|--------|
| `useLayout.ts` | 305 lines | Unified deck/sideboard state | ✅ Enhanced |
| `useSelection.ts` | 310 lines | Dual selection system | ⚠️ Complex |
| `useDragAndDrop.ts` | 445 lines | Complete drag & drop | ⚠️ Very Complex |
| `useSorting.ts` | 270 lines | **Sorting + performance optimized** | ✅ Enhanced |
| `useContextMenu.ts` | 165 lines | Context menu state | ✅ Good |

### 🛠️ Services & Utils Layer - 7 Files

| File | Size | Responsibility | Status |
|------|------|----------------|--------|
| `scryfallApi.ts` | 575 lines | **Complete Scryfall abstraction + Load More** | ✅ Enhanced |
| `deckFormatting.ts` | 180 lines | Deck export utilities | ✅ Good |
| `screenshotUtils.ts` | 850 lines | Advanced screenshot generation | ⚠️ Extremely Complex |
| `deviceDetection.ts` | 145 lines | Device capability detection | ✅ Excellent |
| `card.ts` | 520 lines | **Foundation types + consistent images** | ✅ Enhanced |
| `search.ts` | 120 lines | Enhanced search types | ✅ Good |

## 🔗 Critical Integration Points

### Primary Data Flow (Performance Optimized)
```
Search Input → useCards (coordinator) → useSearch (clean params) → scryfallApi (wildcard opt) → API
     ↓
API Response → useSearch (stored state) → useCards → Components (Smart Card Append)
     ↓
Filter Changes → useCards (clean triggers) → useSearch (fresh params) → <1 second response
     ↓
Load More → usePagination → useSearch (stored state) → scryfallApi (422 prevention) → Success
```

### Key Coordination Patterns

**useCards Hub (250 lines):**
- Coordinates 5 extracted hooks: useSearch, usePagination, useCardSelection, useSearchSuggestions, useFilters
- Clean parameter management prevents search accumulation
- Performance optimized through stable hook dependencies

**useSearch Enhanced (350 lines):**
- Stored pagination state for Load More 422 prevention
- Clean parameter coordination with useCards
- Wildcard optimization with scryfallApi

**useLayout Unified (305 lines):**
- Single state controlling deck + sideboard
- Automatic legacy state migration
- Constraint systems for different contexts

**MTGOLayout Simplified (450 lines):**
- Orchestrates extracted area components
- Clean hook integration patterns
- Responsive design coordination

## 🚀 Performance Optimization Patterns

### Search Performance (Proven Effective)
**Problem:** 2-7+ second searches despite fast API  
**Solution:** Hook re-render loop elimination in useSorting  
**Pattern:** Timing analysis → stable dependencies → memoized returns → <1 second response

### Load More Reliability (Comprehensive Fix)
**Problem:** 422 errors during pagination  
**Solution:** Stored pagination state management  
**Pattern:** Store full page data → comprehensive decision logic → use stored vs fetch → zero errors

### Image Loading Optimization (Progressive Enhancement)
**Problem:** 75 cards loading simultaneously  
**Solution:** Intersection Observer + consistent normal images  
**Pattern:** Lazy loading → viewport detection → progressive display → better perceived performance

### API Efficiency (Wildcard Optimization)
**Problem:** Expensive enhancement for simple queries  
**Solution:** Early wildcard detection in scryfallApi  
**Pattern:** Query analysis → bypass enhancement → let Scryfall handle efficiently

## ⚠️ Current Technical Debt & Refactoring Priorities

### High Priority
1. **scryfallApi.ts (575 lines)** - Apply extraction methodology if growth continues
2. **card.ts (520 lines)** - Separate types from utilities when beneficial
3. **screenshotUtils.ts (850 lines)** - Extract algorithm modules if maintenance needed

### Medium Priority  
4. **Complex Hooks:** useDragAndDrop (445 lines), useSelection (310 lines) - Monitor for extraction opportunities
5. **CSS Architecture:** MTGOLayout.css (1,450 lines) - Future modernization when requirements clear

### Excellent Architecture Examples
- **Hook Extraction Success:** useCards (580→250) + 5 focused hooks
- **Component Extraction Success:** MTGOLayout (925→450) + 3 area components  
- **Performance Optimization Success:** useSorting re-render elimination
- **State Management Success:** useLayout unified deck/sideboard with migration

## 📚 Quick Reference Cards

### "Optimize search performance"
**Spec:** Request Search & Filtering System specification for performance standards  
**Files:** `useSorting.ts` → `useSearch.ts` → `useCards.ts`  
**Pattern:** Timing analysis → fix re-render loops → stable dependencies → memoization

### "Fix Load More issues"  
**Spec:** Request Search & Filtering System specification for pagination patterns  
**Files:** `useSearch.ts` → `scryfallApi.ts` → `usePagination.ts`  
**Pattern:** Store pagination state → decision logic → use stored data → prevent 422 errors

### "Add progressive image loading"
**Spec:** Request Card Display & Loading System specification for loading patterns  
**Files:** `LazyImage.tsx` (new) → `MagicCard.tsx` → `card.ts`  
**Pattern:** Intersection Observer → consistent image strategy → progressive display

### "Extract large component"
**Files:** Target component → create focused components → coordinator pattern  
**Pattern:** Identify areas → extract components → implement coordinator → zero regressions  
**Success:** MTGOLayout (925→450) + CollectionArea + DeckArea + SideboardArea

### "Add unified state management"
**Spec:** Request Layout & State Management System specification for state patterns  
**Files:** `useLayout.ts` → `DeckArea.tsx` → `SideboardArea.tsx`  
**Pattern:** Single state source → coordination functions → component sync → migration support

### "Apply responsive design"
**Spec:** Request Layout & State Management System specification for responsive patterns  
**Files:** `DeckArea.tsx` → `ViewModeDropdown.tsx` → `MTGOLayout.css`  
**Pattern:** Priority ordering → space detection → dynamic hiding → overflow menu

---

**Status:** Enhanced streamlined reference with proven patterns, performance optimization expertise, and feature specification integration  
**Usage:** Reference before development for instant file identification, integration guidance, and system specification requirements