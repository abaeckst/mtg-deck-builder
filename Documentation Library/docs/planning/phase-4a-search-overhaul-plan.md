# Implementation Plan: Phase 4A - Search System Overhaul

## 📋 Session Goal: Fix Critical Search Limitations

**Addressing Priority Issues:**

1. **Multi-Word Search** - Fix "lightning bolt" to find cards with both words in name/text/type
2. **Pagination + Sorting** - Add server-side sorting with "Load All Results" for true comprehensive results
3. **Architecture Cleanup** - Extract filters to separate hook for better maintainability
4. **Color Filter Default** - Change to "at most these colors" behavior
5. **Search Progress** - Add loading indicators for better UX

---

## 🔧 Technical Implementation Plan

### **Phase 4A-1: Multi-Word Search Fix (Session 1)**

**Goal:** Natural multi-word search that works with names, text, and types while preserving quote functionality

**Files to Modify:**

- `src/services/scryfallApi.ts` - Simplify and fix `buildEnhancedSearchQuery`
- `src/hooks/useCards.ts` - Update to use improved search

**Implementation Approach:**

typescript

```typescript
// New simplified multi-word search logic:
// "lightning bolt" → (name:lightning OR o:lightning OR type:lightning) (name:bolt OR o:bolt OR type:bolt)
// "lightning bolt" → Preserves exact phrase search
// Single words work as before
```

**Success Criteria:**

- [ ] "lightning bolt" finds Lightning Bolt card
- [ ] "flying creature" finds creatures with flying
- [ ] `"exact phrase"` still works for exact matches
- [ ] Single word searches work as before

### **Phase 4A-2: Server-Side Sorting + Load All Results (Session 2)**

**Goal:** Add proper server-side sorting with comprehensive pagination

**Files to Modify:**

- `src/services/scryfallApi.ts` - Add progressive pagination functions
- `src/hooks/useCards.ts` - Add load all results functionality
- `src/components/MTGOLayout.tsx` - Add "Load All Results" button

**New API Functions:**

typescript

```typescript
interface PaginatedSearchState {
  initialResults: ScryfallCard[];
  totalCards: number;
  hasMore: boolean;
  isLoadingAll: boolean;
  allResultsLoaded: boolean;
}

// New functions:
searchCardsWithServerSorting(query, filters, sortOrder)
loadAllResultsProgressively(searchParams, onProgress)
```

**UI Changes:**

- Add "Load All Results (X more cards)" button at bottom of collection
- Show progress indicator during full load
- Disable sorting controls until all results loaded OR add warning
