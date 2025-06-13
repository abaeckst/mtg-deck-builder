#!/usr/bin/env python3
"""
MTG Deck Builder - Documentation Library Reorganization
Cleans up and organizes the existing Documentation Library structure
"""

import os
import shutil
from pathlib import Path
from datetime import datetime

def reorganize_documentation_library():
    """Reorganize the existing Documentation Library structure"""
    
    # Define the specific path for Documentation Library\docs
    docs_dir = Path(r"C:\Users\abaec\Development\mtg-deck-builder\Documentation Library\docs")
    
    print(f"Reorganizing documentation structure in: {docs_dir}")
    
    # Check if the directory exists
    if not docs_dir.exists():
        print(f"❌ Directory not found: {docs_dir}")
        return False
    
    # Show current structure
    print("\n📁 Current structure:")
    for item in docs_dir.iterdir():
        if item.is_dir():
            print(f"   📁 {item.name}")
        else:
            print(f"   📄 {item.name}")
    
    # Define our target structure (keeping what aligns, renaming what doesn't)
    target_folders = {
        "specs": "specs",  # New folder for feature specifications
        "methodology": "methodology",  # Keep existing
        "completed": "completed",  # Keep existing  
        "sessions": "sessions",  # New folder for session archives
        "reference": "reference",  # Keep existing but clarify purpose
        "planning": "archive_planning",  # Rename to clarify it's archived planning
        "current_platform_archive": "archive_platform"  # Rename to clarify it's archived
    }
    
    # Create new folders and rename existing ones
    for old_name, new_name in target_folders.items():
        old_path = docs_dir / old_name
        new_path = docs_dir / new_name
        
        if old_path.exists() and old_name != new_name:
            # Rename existing folder
            old_path.rename(new_path)
            print(f"🔄 Renamed: {old_name} → {new_name}")
        elif not new_path.exists():
            # Create new folder
            new_path.mkdir(parents=True, exist_ok=True)
            print(f"✅ Created: {new_name}")
        else:
            print(f"✅ Kept: {new_name}")
    
    # Create README files for the reorganized structure
    readme_contents = {
        "README.md": """# Documentation Library - Strategic Archives

This directory contains strategic knowledge for complex MTG Deck Builder development challenges.

## Structure
- `/specs/` - System-level feature specifications (Search, Drag&Drop, Layout, etc.)
- `/methodology/` - Reusable development patterns and debugging approaches  
- `/completed/` - Implementation case studies with technical details
- `/sessions/` - Detailed development session archives (organized by date)
- `/reference/` - Reference materials and external documentation
- `/archive_planning/` - Archived planning documents (historical context)
- `/archive_platform/` - Archived platform documentation (historical context)

## Usage Pattern
- **Active development:** Use Code Organization Guide (in Claude's memory) primarily
- **System work:** Request relevant feature specifications from `/specs/`
- **Complex problems:** Request strategic archive retrieval for methodology replication
- **Historical context:** Reference archived materials when needed

## Maintenance
- **Active documents:** Maintained in Claude's memory, updated through reconciliation
- **Strategic archives:** Created on-demand based on development session recommendations
- **Historical archives:** Preserved for context but not actively maintained
""",
        
        "specs/README.md": """# Feature Specifications

System-level specifications for major MTG Deck Builder systems.

## Priority for Creation:
- **HIGH:** Search & Filtering System, Drag & Drop System
- **MEDIUM:** Layout & State Management, Card Display & Loading System
- **LOW:** Export & Formatting System

## Specifications to Create:
- `search_filtering_system.md` - Multi-field search, performance optimization, filter coordination
- `drag_drop_system.md` - Visual feedback, interaction patterns, 3x preview scaling
- `layout_state_management.md` - Unified state, responsive design, automatic migration
- `card_display_loading.md` - Progressive loading, intersection observer, consistent display
- `export_formatting_system.md` - MTGO format compliance, screenshot generation

## Creation Process:
1. Development session identifies need for system specification
2. Session log captures "spec update recommendations"  
3. User creates specification during reconciliation using Feature Specification Template
4. Spec guides future development consistency and system understanding

## Template:
Use Feature Specification Template from Claude's active project knowledge.
""",
        
        "methodology/README.md": """# Methodology Patterns

Reusable development patterns and systematic approaches for complex challenges.

## Current Proven Methodologies:
- **Component Extraction** - Proven with MTGOLayout (925→450 lines) + 3 focused components
- **Performance Optimization** - Search optimization (<1 second), Load More fixes, image loading
- **Hook Architecture** - useCards coordinator (580→250 lines) + 5 extracted hooks
- **Unified State Management** - Complex state coordination with automatic migration
- **Advanced Debugging** - Systematic React/TypeScript problem resolution approaches

## When to Archive New Methodologies:
- Multi-session complex problems that were solved systematically
- Approaches that could be reapplied to similar future problems
- Technical implementations with non-obvious solutions
- Debugging patterns that worked well for complex integration issues

## Retrieval:
Request when facing similar problems to past solutions - "How did we solve X?"
""",
        
        "completed/README.md": """# Implementation Case Studies

Detailed case studies of completed major features and architectural work.

## Current Case Studies Available:
- **Phase 1-4B Development** - Complete deck builder implementation journey
- **Performance Optimization** - Search, Load More, and image loading improvements
- **Architecture Overhaul** - useCards coordination hub and hook extraction
- **Component Extraction** - MTGOLayout refactoring methodology and results
- **UI/UX Enhancement** - Unified state implementation and responsive design

## When to Archive New Case Studies:
- Major feature implementations with complex technical details
- Architectural decisions with significant trade-offs and context
- Implementation approaches that solved difficult integration challenges
- Performance work with measurable before/after improvements

## Retrieval:
Request when implementing similar features - "How did we build X feature?"
""",
        
        "sessions/README.md": """# Session Archives

Detailed development session logs with full technical context and decision history.

## Organization:
- Date-based folders: `YYYY-MM-DD/`
- Individual session logs within date folders
- Multi-session projects may have dedicated sub-folders

## Content Examples:
- Technical decisions and implementation rationale
- Debugging processes and breakthrough solutions
- Integration challenges and resolution approaches
- Performance work with timing analysis and measurements
- Architectural evolution with trade-off analysis

## Archival Process:
1. Session logs created as artifacts during development
2. During reconciliation, user processes valuable sessions
3. Archive sessions with complex problem resolution or methodology development
4. Most session value captured in methodology patterns and case studies

## Retrieval:
Rarely needed directly - most value extracted into methodology and case study archives.
""",
        
        "reference/README.md": """# Reference Materials

External documentation, guidelines, and reference materials for MTG Deck Builder development.

## Purpose:
- External API documentation and integration guides
- Development standards and coding guidelines  
- Design system references and UI/UX standards
- Third-party library documentation and examples
- MTGO interface references and authenticity standards

## Content Types:
- API documentation and integration examples
- Design standards and visual references
- Code style guides and best practices
- External tool documentation and setup guides
- Research materials and competitive analysis

## Usage:
Reference materials that don't fit into methodology, case studies, or specifications.
Stable documentation that doesn't evolve with the project.
""",
        
        "archive_planning/README.md": """# Archived Planning Documents

Historical planning documents preserved for context and decision history.

## Purpose:
- Preserve planning decisions and rationale for future reference
- Maintain context for why certain approaches were chosen
- Historical roadmaps and feature priority decisions
- Original project scope and evolution tracking

## Content:
- Early project planning and scope decisions
- Feature roadmaps and priority matrices
- Architecture planning and technology choices
- Historical decision context and trade-off analysis

## Usage:
- Reference when questions arise about "why did we do X?"
- Context for understanding project evolution
- Historical perspective on decision rationale
- Not actively maintained - preserved for context only
""",
        
        "archive_platform/README.md": """# Archived Platform Documentation

Historical platform documentation preserved for context and reference.

## Purpose:
- Preserve historical platform states and capabilities
- Maintain context for platform evolution decisions  
- Reference for understanding "how did we get here?"
- Historical technical specifications and requirements

## Content:
- Previous platform capabilities and limitations
- Historical technical specifications
- Evolution context and upgrade rationale
- Legacy system documentation and integration notes

## Usage:
- Reference for understanding platform evolution
- Context for technical debt and architectural decisions
- Historical perspective on capability development
- Not actively maintained - preserved for context only
"""
    }
    
    # Create README files
    for file_path, content in readme_contents.items():
        full_path = docs_dir / file_path
        # Create parent directory if it doesn't exist
        full_path.parent.mkdir(parents=True, exist_ok=True)
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"📝 Created: {file_path}")
    
    # Create today's session folder
    today = datetime.now().strftime("%Y-%m-%d")
    session_folder = docs_dir / f"sessions/{today}"
    session_folder.mkdir(parents=True, exist_ok=True)
    print(f"📅 Created today's session folder: sessions/{today}")
    
    print("\n🎉 Documentation Library reorganized successfully!")
    print(f"\n📁 Final structure in: {docs_dir}")
    for item in sorted(docs_dir.iterdir()):
        if item.is_dir():
            print(f"   📁 {item.name}")
        else:
            print(f"   📄 {item.name}")
    
    print("\n🚀 Next steps:")
    print("1. Review the README files in each reorganized folder")
    print("2. Create feature specifications in /specs/ as development requires them")
    print("3. Archive valuable session logs in /sessions/ during reconciliation")
    print("4. Use /methodology/ and /completed/ for strategic archive retrieval")
    
    return True

if __name__ == "__main__":
    reorganize_documentation_library()
