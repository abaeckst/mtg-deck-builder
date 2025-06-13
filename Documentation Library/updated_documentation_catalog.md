# MTG Deck Builder - Documentation Catalog

**Purpose:** Strategic knowledge retrieval for complex development challenges  
**Last Updated:** January 13, 2025  
**Repository:** https://github.com/abaeckst/mtg-deck-builder

## 📋 Active Project Knowledge (Claude's Memory)

**Essential References:**
- **Project Status** - Current capabilities, 3D card flip system, comprehensive system documentation, technical debt management, development options
- **Enhanced Code Organization Guide** - Streamlined file identification, 3D component patterns, integration patterns, technical debt awareness, debugging methodologies  
- **Development Session Templates** - Efficient development workflow with system specification integration
- **Feature Specification Template** - System documentation structure (proven through 6 major specs)
- **This Catalog** - Archive retrieval guide

*These documents are maintained in Claude's active memory and updated through reconciliation process.*

## 📚 Strategic Archives (Documentation Library)

**Location:** `C:\Users\abaec\Development\mtg-deck-builder\Documentation Library\docs\`

### 🎯 Feature Specifications (`/specs/`) - ✅ COMPLETE COVERAGE WITH 3D INTEGRATION

**Major System Specifications (All Enhanced January 13, 2025):**

**Search & Filtering System** - `search_filtering_system.md`
- Multi-field search architecture (names, oracle text, type lines)
- Performance optimization patterns (re-render elimination, <1 second response)
- Filter coordination with useCards hub (5 extracted hooks)
- Progressive loading (75+175 cards, Smart Card Append, 422 prevention)
- API efficiency (wildcard optimization, stored pagination state)
- Clean parameter management and filter reactivity systems

**Drag & Drop System** - `drag_drop_system.md`
- Sophisticated interaction detection (5 timing constants, click/drag differentiation)
- Enhanced visual feedback (3x preview scaling, zone-relative centering)
- Professional styling (green/neutral feedback, no red, pulse animations)
- Complex state management (functional updates, ref-based drop capture)
- Advanced interaction handling (double-click protection, movement thresholds)
- Performance optimizations (requestAnimationFrame, throttled events)

**Layout & State Management System** - `layout_state_management.md` ✅ **ENHANCED**
- Unified deck/sideboard state architecture (single view mode and card size controls)
- Percentage-based responsive layout (automatic migration from pixel-based)
- Advanced responsive design (priority-based control hiding, nuclear z-index strategies)
- Professional component coordination (MTGOLayout 450 lines orchestrating 5 systems)
- Sophisticated constraint systems and CSS variable updates
- Automatic legacy state migration with error handling
- **Enhanced:** CSS coordination debugging methodology, resize handle technical debt documentation
- **Enhanced:** Systematic visual/functional integration debugging workflows

**Card Display & Loading System** - `card_display_loading.md` ✅ **ENHANCED WITH 3D FLIP**
- Progressive loading with Intersection Observer (50px rootMargin, viewport detection)
- Dual identity architecture (ScryfallCard vs DeckCardInstance)
- Performance optimization patterns (eliminated simultaneous loading, consistent normal-size images)
- Enhanced interaction integration (instance-based selection, sophisticated timing)
- Professional visual design (PNG preference, rarity styling, quantity indicators)
- Dynamic scaling and MTGO-authentic appearance standards
- **NEW:** Complete Double-Faced Card Flip System documentation
- **NEW:** FlipCard component architecture with 3D animation integration
- **NEW:** Hardware acceleration patterns and CSS Grid compatibility solutions
- **NEW:** Face-specific image resolution and professional flip button standards

**Export & Formatting System** - `export_formatting.md`
- Dual export strategy (MTGO text compliance + modern screenshot sharing)
- Mathematical layout optimization (850 lines screenshotUtils.ts with binary search scaling)
- Advanced space utilization (aggressive waste detection, configuration generation)
- Professional error handling (multiple fallbacks, CORS handling, DOM verification)
- MTGO format compliance (exact formatting, card grouping, metadata generation)
- Cross-browser compatibility (modern clipboard API + legacy fallbacks)

**Component Architecture & Integration System** - `component_architecture_integration.md` ✅ **ENHANCED WITH 3D INTEGRATION**
- Cross-system coordination patterns (30+ callback functions, 5 major hook systems)
- Sophisticated integration architecture (useCards 250-line coordinator hub)
- Nuclear z-index management strategies (500,000-2,000,000 range for dropdown reliability)
- Component extraction success patterns (MTGOLayout 925→450 + 3 area components)
- Unified state inheritance (SideboardArea simplification through shared state)
- Advanced responsive coordination (priority-based systems, overflow management)
- **Enhanced:** CSS class vs inline style coordination patterns and debugging methodologies
- **Enhanced:** Integration debugging workflows with systematic DOM investigation approaches
- **NEW:** FlipCard integration patterns with conditional rendering architecture
- **NEW:** 3D animation integration with existing drag/drop and selection systems
- **NEW:** CSS Grid compatibility solutions and container stabilization techniques

### 📋 Technical Debt Management (`/reference/`) - ✅ **ENHANCED**

**Technical Debt Documentation** - `technical_debt.md` ✅ **ENHANCED WITH 3D INTEGRATION**
- **Priority-based tracking** (P1-P4) for systematic debt management
- **Current inventory** with detailed issue analysis and solution paths
- **Resolution tracking** showing successful debt reduction examples
- **Systematic debugging methodologies** extracted from session work
- **Management process** for ongoing debt identification and resolution
- **Integration with development workflow** for informed decision-making
- **NEW:** CSS Grid positioning solutions and container stabilization patterns
- **NEW:** 3D animation browser compatibility considerations
- **NEW:** Performance optimization examples including device detection throttling

### 🎪 3D Animation Implementation (`/case_studies/`) - ✅ **NEW**

**Double-Faced Card Flip Implementation Case Study** - `3d_flip_implementation.md`
- **Complete implementation methodology** from detection to hardware-accelerated animation
- **CSS Grid compatibility solutions** with container stabilization patterns
- **Event isolation techniques** for complex multi-system integration
- **Performance optimization** with hardware acceleration and 60fps targets
- **Professional visual standards** with MTGO-style flip button design
- **Debugging methodologies** for 3D animation and positioning issues
- **Integration patterns** with existing drag/drop, selection, and context menu systems

### 🔄 Specification Integration Status

**System Coverage:** ✅ 100% Complete - All 6 major systems comprehensively documented with 3D integration  
**Cross-System Integration:** ✅ Complete - Component Architecture spec covers coordination patterns including FlipCard  
**Technical Depth:** ✅ Complete - File organization, implementation details, performance patterns, 3D animation architecture  
**UX Standards:** ✅ Complete - MTGO authenticity, responsive design, interaction patterns, 3D animation quality  
**Evolution Context:** ✅ Complete - Design decisions, trade-offs, future considerations including 3D enhancements  
**Technical Debt Integration:** ✅ Complete - Debugging methodologies, systematic debt management, CSS Grid solutions

**Enhanced Specification Features:**
- **3D Animation Integration:** Complete FlipCard component architecture and implementation patterns
- **CSS Grid Compatibility:** Container stabilization solutions for positioning challenges
- **Hardware Acceleration:** Performance optimization patterns for smooth 3D animations
- **Advanced Event Handling:** Multi-system coordination with event isolation techniques
- **Debugging Methodologies:** Systematic approaches for visual/functional integration issues including 3D contexts
- **Technical Debt Context:** Known limitations with clear solution paths including CSS positioning

### 🔍 Strategic Archive Retrieval

**System-Level Development:**
```
"Working on search improvements → Request Search & Filtering System spec"
"Adding drag feedback → Request Drag & Drop System spec"  
"Layout modifications → Request Layout & State Management System spec"
"Card display changes → Request Card Display & Loading System spec (includes 3D flip)"
"Export functionality → Request Export & Formatting System spec"
"Cross-system integration → Request Component Architecture & Integration System spec"
"3D animation work → Request Card Display & Loading System spec for FlipCard patterns"
```

**Technical Debt Resolution:**
```
"Need to fix CSS coordination issues → Request Technical Debt Documentation for P2 priorities"
"CSS Grid positioning problems → Request Component Architecture spec for container stabilization"
"Debugging visual integration problems → Request Layout/Component Architecture specs for methodologies"
"Complex hook extraction needed → Reference successful extraction examples in Technical Debt doc"
"3D animation positioning issues → Request Card Display spec for CSS Grid compatibility solutions"
```

**Implementation Reference (6+ months later):**
```
"How did we build the 3D card flip system?"
"What were the CSS Grid positioning solutions?"
"How did we achieve hardware-accelerated animations?"
"What was the container stabilization approach?"
"How did we integrate 3D animations with existing systems?"
"What systematic debugging approaches worked for CSS positioning?"
```

**3D Animation Methodology:**
```
"Need to add 3D effects → How did we implement FlipCard component?"
"CSS Grid positioning issues → What container stabilization patterns worked?"
"Event isolation challenges → How did we prevent 3D animation interference?"
"Performance optimization needed → What hardware acceleration patterns succeeded?"
"Multi-system integration → How did we coordinate 3D with drag/selection systems?"
```

**Methodology Replication:**
```
"Component extraction needed - how did we handle MTGOLayout refactoring?"
"Performance optimization required - what systematic approaches worked?"
"Cross-system integration challenges - what coordination patterns succeeded?"
"Complex React debugging needed - what methodologies proved effective?"
"CSS coordination conflicts - what debugging workflows were successful?"
"3D animation integration - what patterns ensured seamless system coordination?"
```

**Archive Categories:**
- **`/specs/`** ✅ - Complete system-level feature specifications (6 major systems with 3D integration enhancements)
- **`/reference/`** ✅ - Technical debt management, systematic debugging approaches, CSS Grid solutions
- **`/case_studies/`** ✅ - 3D flip implementation methodology, CSS positioning solutions, performance optimization examples
- **`/methodology/`** - Reusable development patterns and debugging approaches
- **`/completed/`** - Implementation case studies with technical details including 3D animation work
- **`/sessions/`** - Detailed development session logs (organized by date, including January 13 3D flip implementation)
- **`/archive_planning/`** - Historical planning documents (preserved for context)
- **`/archive_platform/`** - Historical platform documentation (preserved for context)

## 🔄 Workflow Integration

### **During Development Sessions:**

**System Specifications (Primary Reference):**
- **Proactive provision:** Claude provides relevant system specs based on planned work including 3D integration context
- **Reactive request:** "Request [System Name] specification for [specific aspect]"  
- **3D Animation Context:** Card Display & Loading System spec includes complete FlipCard documentation
- **CSS Grid Solutions:** Component Architecture spec includes container stabilization patterns
- **Multi-session tracking:** Session logs track contradictions with "Supersedes" notation
- **Evolution documentation:** System changes and decision rationale captured including 3D enhancements

**Enhanced Development Context:**
- **Technical Architecture:** Complete file organization and implementation patterns including FlipCard component
- **3D Animation Patterns:** Hardware acceleration, event isolation, CSS Grid compatibility solutions
- **Performance Standards:** Benchmarks, optimization approaches, regression prevention including 60fps 3D animations
- **UX Guidelines:** MTGO authenticity requirements, responsive design patterns, 3D interaction standards
- **Integration Points:** Cross-system coordination and callback patterns including 3D animation integration
- **Technical Debt Awareness:** Priority-based understanding of current limitations including CSS positioning
- **Debugging Methodologies:** Systematic approaches for complex integration problems including 3D contexts

**Technical Debt Management (Integrated Reference):**
- **Priority Awareness:** Understanding P1-P4 technical debt when making development decisions
- **CSS Grid Solutions:** Container stabilization patterns and positioning reliability approaches
- **Resolution Guidance:** Reference successful debt reduction examples and proven approaches
- **Debugging Support:** Systematic methodologies for visual/functional integration issues including 3D animation

**Strategic Archives (Secondary Reference):**
- **Problem-based retrieval:** "Facing similar issue to X → Request methodology Y"
- **Implementation guidance:** "Adding feature like Z → Request case study W"
- **3D Animation Reference:** "Need similar 3D effects → Request FlipCard implementation case study"
- **Methodology replication:** Apply proven patterns from archive case studies

### **During Reconciliation:**

**Specification Management:**
- **Status:** ✅ Complete - All 6 major systems documented with 3D integration enhancements
- **Maintenance:** Update specs based on system evolution and development insights including 3D functionality
- **Priority:** Keep current with implementation reality, document architectural changes

**Technical Debt Management:**
- **Priority Review:** Assess technical debt priority changes based on system evolution
- **Resolution Tracking:** Document successful debt reduction and methodology refinement including CSS Grid solutions
- **Integration Updates:** Ensure debugging methodologies reflect latest successful approaches including 3D contexts

**Archive Management:**
- **Session processing:** January 13 3D flip implementation and CSS Grid debugging sessions → Strategic archive addition
- **Methodology extraction:** Cross-system patterns, 3D animation integration, and optimization approaches
- **Implementation case studies:** 3D flip system, CSS positioning solutions, performance optimization, architectural refactoring

## 🎯 Usage Guidelines

### **For Active Development:**
- **Primary:** Enhanced Code Organization Guide for file identification, integration patterns, 3D component architecture, and technical debt awareness
- **Secondary:** System specifications for understanding design intent, technical architecture, UX standards, 3D integration, and debugging methodologies
- **Tertiary:** Technical debt documentation for priority awareness, CSS Grid solutions, and systematic resolution approaches
- **Strategic:** Request archives only when facing similar problems to past solutions including 3D animation challenges

### **For System-Level Work:**
- **Step 1:** Request relevant system specification for complete context, 3D integration patterns, and debugging methodologies
- **Step 2:** Apply Enhanced Code Organization Guide patterns for file identification, FlipCard components, and technical debt awareness
- **Step 3:** Use specification architecture, performance standards, 3D animation patterns, and debugging workflows for implementation
- **Step 4:** Reference technical debt documentation for priority awareness, CSS Grid solutions, and systematic approaches
- **Step 5:** Document system evolution in session logs for future specification updates including 3D enhancements

### **For 3D Animation Work:**
- **Step 1:** Request Card Display & Loading System specification for FlipCard architecture and integration patterns
- **Step 2:** Apply Component Architecture specification for CSS Grid compatibility and container stabilization
- **Step 3:** Reference 3D flip implementation case study for detailed methodology and debugging approaches
- **Step 4:** Use technical debt documentation for CSS positioning solutions and performance considerations

### **For Complex Problems:**
- **Step 1:** Apply Enhanced Code Organization Guide patterns and request relevant system specs including 3D context
- **Step 2:** Use system specifications for technical architecture, proven patterns, 3D integration, and debugging methodologies
- **Step 3:** Reference technical debt documentation for systematic resolution approaches including CSS Grid solutions
- **Step 4:** If still stuck, request strategic archive retrieval for methodology replication including 3D animation patterns

### **For Technical Debt Resolution:**
- **Step 1:** Reference technical debt documentation for priority assessment, CSS Grid solutions, and solution paths
- **Step 2:** Apply system specifications for debugging methodologies, 3D integration context, and integration context
- **Step 3:** Use proven resolution examples, container stabilization patterns, and systematic approaches
- **Step 4:** Document resolution process for future methodology refinement

### **Retrieval Efficiency:**
- **System-specific:** "Request [System Name] specification" for technical architecture, UX context, 3D integration, and debugging methodologies
- **3D Animation-focused:** "Request Card Display & Loading System specification for FlipCard patterns and CSS Grid compatibility"
- **Technical debt-focused:** "Reference technical debt documentation for [specific issue/priority] including CSS positioning solutions"
- **Problem-focused:** "How did we solve [specific challenge including 3D animation]?" vs "what archives exist?"
- **Implementation-focused:** "Need [specific pattern including 3D effects] implementation details" for targeted retrieval

---

**Current Status:** Complete system specification coverage with 3D animation integration, enhanced debugging methodologies, CSS Grid compatibility solutions, and systematic technical debt management  
**Usage Pattern:** Enhanced Code Org Guide (file identification + 3D patterns + tech debt awareness) → System Specs (context/standards/3D integration/debugging) → Tech Debt Doc (priorities/CSS solutions/resolution) → Archives (complex problems + 3D methodology)  
**Location:** `C:\Users\abaec\Development\mtg-deck-builder\Documentation Library\docs\`  
**Achievement:** All 6 major systems comprehensively documented with technical depth, UX context, 3D animation integration, debugging methodologies, CSS Grid solutions, and systematic technical debt management