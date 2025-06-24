# System Guide Template & Project System List

**Purpose:** Template for creating system-specific architectural guides with complete file identification and flow understanding 
**Created:** January 14, 2025 
**Usage:** Create focused guides that replace generic file identification with deep system understanding

---

## 📋 System Guide Template

```markdown
# [System Name] Guide
**Last Updated:** [Date] 
**Status:** [Current system status - working/partial/broken] 
**Complexity:** [Low/Medium/High] - [Brief complexity reasoning]
## 🎯 System Definition
### Purpose
**What this system does:** [Core functionality and user-facing behavior] 
**Why it exists:** [Problem this system solves] 
**System boundaries:** [What's included vs. what's handled by other systems]
### Core Files (Always Work Together)
**Primary Files:**
- `[filename.tsx]` ([size] lines) - [specific responsibility + critical patterns]
- `[filename.ts]` ([size] lines) - [specific responsibility + key functions]
- `[filename.css]` ([size] lines) - [styling patterns + responsive behavior]
**Secondary Files:**
- `[filename.tsx]` ([size] lines) - [supporting functionality + integration role]
- `[filename.ts]` ([size] lines) - [utilities + helper functions]
**Integration Files:**
- `[filename.tsx]` ([size] lines) - [coordination with other systems]
### Integration Points
**Receives data from:**
- **[System A]:** [What data, how it's passed, critical dependencies]
- **[System B]:** [Props/state/callbacks, integration patterns]
**Provides data to:**
- **[System C]:** [What data, interface patterns, state sharing]
- **[System D]:** [Integration mechanisms, coordination approaches]
**Coordinates with:**
- **[System E]:** [Shared state, event coordination, mutual dependencies]
## 🔄 Critical Data Flows
### Primary Flow: [Main User Action/Data Path]
```

[Starting Point] → [Component/Function] → [Processing] → [State Change] → [UI Update]
 ↓
[Integration Point] → [Other System] → [Side Effects] → [Completion]

```
**Key Decision Points:**
- **[Conditional 1]:** [When this executes vs. alternative path]
- **[Conditional 2]:** [Critical if/else logic that affects behavior]
### Secondary Flow: [Important Alternative Path]
```

[Alternative Start] → [Different Processing] → [Different Outcome]

```
### Integration Flow: [Cross-System Coordination]
```

[This System] ↔️ [Other System] → [Coordination Pattern] → [Shared Result]

```
## 🐛 Problem Diagnosis
### Common Issues & File Locations
**"[Specific Problem Description]"**
- **Root Cause:** [Why this happens technically]
- **Check Files:** [Specific files in order of likelihood]
- **Debug Pattern:** [How to investigate this issue]
**"[Another Problem]"**
- **Root Cause:** [Technical explanation]
- **Check Files:** [File investigation order]
- **Debug Pattern:** [Debugging approach]
**"[Integration Issue]"**
- **Root Cause:** [Cross-system problem explanation]
- **Check Files:** [Files in multiple systems]
- **Debug Pattern:** [Cross-system debugging approach]
### Debugging Starting Points
**[Symptom 1]:** Start with `[filename.tsx]` → [specific function/component] → [what to look for] 
**[Symptom 2]:** Start with `[filename.ts]` → [specific logic] → [validation steps] 
**[Symptom 3]:** Start with integration between `[file1]` and `[file2]` → [coordination check]
## 🔧 Architecture Details
### State Management Pattern
**How state is organized:** [Centralized/distributed/coordinated approach] 
**State flow:** [How changes propagate through the system] 
**Key state variables:** [Critical state that drives system behavior]
### Critical Functions & Hooks
**[FunctionName/HookName]:** [What it does, when it's called, what it returns] 
**[AnotherFunction]:** [Purpose, parameters, side effects, integration points] 
**[KeyHook]:** [Responsibility, dependencies, state management approach]
### Component Hierarchy
```

[ParentComponent]
├── [ChildA] (handles [specific responsibility])
├── [ChildB] (manages [specific function])
└── [ChildC] (coordinates [specific integration])

```
### Performance Considerations
**Critical paths:** [Performance-sensitive operations] 
**Optimization patterns:** [How performance is maintained] 
**Known bottlenecks:** [Current performance limitations]
## ⚠️ Current System Status
### Working Functionality
- ✅ **[Feature 1]:** [What works correctly + verification approach]
- ✅ **[Feature 2]:** [Working behavior + test method]
### Known Issues
- ❌ **[Issue 1]:** [What's broken + impact + file location]
- ⚠️ **[Issue 2]:** [Partial functionality + limitations + workaround]
### Technical Debt
**Priority Items:**
- **P1:** [Critical debt item + impact + file location]
- **P2:** [Important debt + technical details + solution path]
### Recent Changes
**[Date]:** [What was changed + files affected + impact on system] 
**[Date]:** [Recent modification + integration effects + testing done]
## 🚀 Development Patterns
### Common Change Patterns
**Adding [Type of Feature]:**
1. **Start with:** `[filename]` → [specific function/component]
2. **Then modify:** `[other files]` → [integration points]
3. **Test by:** [Verification approach]
**Debugging [Type of Issue]:**
1. **Check:** `[filename]` → [specific area] → [what to validate]
2. **If not found:** `[filename]` → [alternative investigation]
3. **Integration check:** [Cross-system validation approach]
### File Modification Order
**For [Change Type]:** [filename1] → [filename2] → [filename3] (with reasoning) 
**For [Debug Type]:** [investigation order] → [validation sequence]
### Testing Strategy
**Critical to test:** [High-risk functionality that must work] 
**Integration tests:** [Cross-system functionality to validate] 
**Performance validation:** [What to measure + acceptable thresholds]
---
**Template Notes:**
- Replace all [bracketed items] with system-specific details
- Focus on actual implementation reality, not intended behavior
- Include specific file lines/functions where critical logic lives
- Emphasize conditional flows and decision points
- Map problems to exact file locations for efficient debugging
```

---

## 🎯 MTG Deck Builder System Guide Priority List

### Tier 1: Critical Systems (Address card sizing failure patterns)

**1. Card Display System Guide**

- **Files:** MagicCard.tsx, FlipCard.tsx, LazyImage.tsx, DraggableCard.tsx, card.ts
- **Priority:** Highest - Core to card sizing failures
- **Focus:** Image resolution logic, size application, 3D flip integration
  **2. Layout State System Guide** 
- **Files:** useLayout.ts, MTGOLayout.tsx, deviceDetection.ts
- **Priority:** Highest - State management coordination failures
- **Focus:** Unified state patterns, prop flow, state persistence
  **3. Component Integration System Guide**
- **Files:** MTGOLayout.tsx, DeckArea.tsx, SideboardArea.tsx, CollectionArea.tsx, AdaptiveHeader.tsx
- **Priority:** High - Cross-component prop flow issues
- **Focus:** Prop passing patterns, unified controls, responsive coordination
  
  ### Tier 2: Major Feature Systems
  
  **4. Search & Filtering System Guide**
- **Files:** useSearch.ts, useFilters.ts, usePagination.ts, SearchAutocomplete.tsx, FilterPanel.tsx, scryfallApi.ts
- **Priority:** Medium-High - Complex coordination system
- **Focus:** Search coordination, pagination state, API integration
  **5. Drag & Drop System Guide**
- **Files:** useDragAndDrop.ts, DraggableCard.tsx, DropZone.tsx, DragPreview.tsx
- **Priority:** Medium-High - Complex interaction system
- **Focus:** Visual feedback, interaction detection, state management
  **6. Data Management System Guide**
- **Files:** useCards.ts, useCardSelection.ts, useSearchSuggestions.ts, scryfallApi.ts
- **Priority:** Medium - Core data coordination
- **Focus:** Hook coordination, API integration, state management
  
  ### Tier 3: Specialized Systems
  
  **7. Export & Formatting System Guide**
- **Files:** deckFormatting.ts, screenshotUtils.ts, modal components
- **Priority:** Medium - Specialized functionality
- **Focus:** Format standards, screenshot generation, utility patterns
  **8. View & Display System Guide**
- **Files:** ListView.tsx, PileView.tsx, PileColumn.tsx, ViewModeDropdown.tsx, useSorting.ts
- **Priority:** Low-Medium - UI display coordination
- **Focus:** View mode coordination, sorting patterns, responsive display
  
  ### Tier 4: Supporting Systems
  
  **9. UI Components System Guide**
- **Files:** CollapsibleSection.tsx, SubtypeInput.tsx, context menu components
- **Priority:** Low - Reusable component patterns
- **Focus:** Reusable patterns, integration approaches
  **10. Performance & Optimization System Guide**
- **Files:** Performance optimization patterns across systems
- **Priority:** Low - Cross-cutting concerns
- **Focus:** Optimization patterns, performance debugging

---

## 📋 Implementation Strategy

### Phase 1: Address Card Sizing Gaps (Immediate)

- **Create:** Card Display System Guide
- **Create:** Layout State System Guide 
- **Create:** Component Integration System Guide
- **Goal:** Eliminate file identification inconsistency and architectural understanding gaps
  
  ### Phase 2: Major Systems (Next)
- **Create:** Search & Filtering System Guide
- **Create:** Drag & Drop System Guide
- **Create:** Data Management System Guide
- **Goal:** Complete coverage of major development areas
  
  ### Phase 3: Specialized Coverage (Later)
- **Create:** Remaining system guides as needed
- **Goal:** Complete architectural understanding for all project systems
  
  ### Quality Criteria
  
  **Each guide must provide:**
- ✅ Complete file list for system work
- ✅ Critical data flow understanding
- ✅ Problem-to-file mapping for debugging
- ✅ Integration point clarity
- ✅ Current reality vs. intended behavior

---

**Template Status:** Ready for system guide creation 
**Priority Focus:** Tier 1 guides to address card sizing architectural understanding gaps 
**Success Metric:** Consistent file identification and accurate architectural understanding across development sessions
