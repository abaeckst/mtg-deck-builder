#!/usr/bin/env python3
"""
CSS Extraction Script - Phase 2 IMPROVED: Better validation and debugging
Extracting Drag & Drop, Panel Resizing, Component Styles with careful validation
"""

import os
import re
import shutil
from datetime import datetime

def create_backup():
    """Create backup of current files"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = f"css_phase2_backup_{timestamp}"
    os.makedirs(backup_dir, exist_ok=True)
    
    # Backup current CSS file
    shutil.copy2("src/components/MTGOLayout.css", f"{backup_dir}/MTGOLayout.css")
    # Backup TSX file
    shutil.copy2("src/components/MTGOLayout.tsx", f"{backup_dir}/MTGOLayout.tsx")
    
    print(f"✅ Backup created: {backup_dir}/")
    return backup_dir

def read_file(filepath):
    """Read file content"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"❌ Error reading {filepath}: {e}")
        return None

def write_file(filepath, content):
    """Write content to file"""
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Created: {filepath} ({len(content.splitlines())} lines)")
        return True
    except Exception as e:
        print(f"❌ Error writing {filepath}: {e}")
        return False

def find_section_boundaries(content, start_marker, debug=False):
    """Find section boundaries more carefully"""
    if debug:
        print(f"🔍 Looking for section: {start_marker}")
    
    # Find start position
    start_match = re.search(re.escape(start_marker), content)
    if not start_match:
        if debug:
            print(f"   ❌ Start marker not found: {start_marker}")
        return None, None
    
    start_pos = start_match.start()
    if debug:
        print(f"   ✅ Found start at position: {start_pos}")
    
    # Find end by looking for next major section comment
    remaining_content = content[start_pos:]
    
    # Look for next comment section that starts with /* and capital letter
    next_section_patterns = [
        r'\n\s*\/\* [A-Z]',  # Next major section
        r'\n\s*\/\* ===== [A-Z]',  # Major section with =====
        r'\n\s*\/\* PHASE',  # Phase sections
    ]
    
    end_pos = None
    for pattern in next_section_patterns:
        matches = list(re.finditer(pattern, remaining_content))
        if matches:
            # Take the first match that's not too close to start
            for match in matches:
                if match.start() > 50:  # At least 50 chars from start
                    candidate_end = start_pos + match.start()
                    if end_pos is None or candidate_end < end_pos:
                        end_pos = candidate_end
                    break
    
    if end_pos is None:
        # No clear end found, estimate based on content
        lines = remaining_content.split('\n')
        estimated_lines = min(300, len(lines))  # Cap at 300 lines
        estimated_content = '\n'.join(lines[:estimated_lines])
        end_pos = start_pos + len(estimated_content)
    
    if debug:
        print(f"   ✅ Section end at position: {end_pos}")
        section_length = end_pos - start_pos
        print(f"   📏 Section length: {section_length} chars")
    
    return start_pos, end_pos

def extract_drag_drop_styles(content):
    """Extract drag and drop styles section with validation"""
    print("🔧 Extracting Drag and Drop Styles...")
    
    start_pos, end_pos = find_section_boundaries(content, "/* DRAG AND DROP STYLES */", debug=True)
    
    if start_pos is None:
        print("   ❌ Drag & Drop section not found")
        return None, content
    
    # Extract the section
    extracted = content[start_pos:end_pos].strip()
    
    # Validate extraction
    if len(extracted) < 100:
        print(f"   ⚠️  Extracted section seems too small: {len(extracted)} chars")
        return None, content
    
    if "drag" not in extracted.lower():
        print("   ⚠️  Extracted section doesn't contain 'drag' - might be wrong section")
        return None, content
    
    # Remove from original content
    remaining = content[:start_pos] + content[end_pos:]
    remaining = re.sub(r'\n\s*\n\s*\n', '\n\n', remaining)  # Clean up extra newlines
    
    print(f"   ✅ Drag & Drop extracted: {len(extracted.splitlines())} lines")
    return extracted, remaining

def extract_component_styles(content):
    """Extract component styles with specific section hunting"""
    print("🔧 Extracting Component Styles...")
    
    # Look for specific component sections
    component_markers = [
        "/* Panel Headers - Consistent across all panels */",
        "/* View Controls */", 
        "/* PHASE 3B-1: Size slider styles",
        "/* Deck Controls */",
        "/* Sideboard Controls */"
    ]
    
    extracted_sections = []
    remaining = content
    
    for marker in component_markers:
        start_pos, end_pos = find_section_boundaries(remaining, marker, debug=False)
        if start_pos is not None:
            section = remaining[start_pos:end_pos].strip()
            if len(section) > 50:  # Only if section has substantial content
                extracted_sections.append(section)
                remaining = remaining[:start_pos] + remaining[end_pos:]
                print(f"   ✅ Found: {marker[:30]}... ({len(section.splitlines())} lines)")
    
    if extracted_sections:
        extracted = '\n\n'.join(extracted_sections)
        remaining = re.sub(r'\n\s*\n\s*\n', '\n\n', remaining)  # Clean up extra newlines
        print(f"   ✅ Component Styles extracted: {len(extracted.splitlines())} lines total")
        return extracted, remaining
    
    print("   ❌ No component sections found")
    return None, content

def extract_panel_resizing(content):
    """Extract panel resizing styles"""
    print("🔧 Extracting Panel Resizing...")
    
    # Look for resizing sections
    resize_markers = [
        "/* Enhanced Resize Handles",
        "/* ===== EXTENDED PANEL RESIZING"
    ]
    
    extracted_sections = []
    remaining = content
    
    for marker in resize_markers:
        start_pos, end_pos = find_section_boundaries(remaining, marker, debug=True)
        if start_pos is not None:
            section = remaining[start_pos:end_pos].strip()
            if len(section) > 50:
                extracted_sections.append(section)
                remaining = remaining[:start_pos] + remaining[end_pos:]
                print(f"   ✅ Found: {marker[:30]}... ({len(section.splitlines())} lines)")
    
    if extracted_sections:
        extracted = '\n\n'.join(extracted_sections)
        remaining = re.sub(r'\n\s*\n\s*\n', '\n\n', remaining)  # Clean up extra newlines
        print(f"   ✅ Panel Resizing extracted: {len(extracted.splitlines())} lines total")
        return extracted, remaining
    
    print("   ❌ No panel resizing sections found")
    return None, content

def update_imports(tsx_content, successful_extractions):
    """Update imports only for successful extractions"""
    import_mapping = {
        'drag_drop': "import './DragAndDropStyles.css';",
        'components': "import './ComponentStyles.css';",
        'resizing': "import './PanelResizing.css';"
    }
    
    for extraction_type in successful_extractions:
        import_line = import_mapping.get(extraction_type)
        if import_line and import_line not in tsx_content:
            tsx_content = tsx_content.replace(
                "import './MTGOLayout.css';",
                f"import './MTGOLayout.css';\n{import_line}"
            )
    
    return tsx_content

def main():
    """Main extraction function with comprehensive validation"""
    print("🚀 Starting CSS Phase 2 Extraction (IMPROVED)")
    print("📋 Target: Drag & Drop, Component Styles, Panel Resizing")
    print("🔍 Using improved pattern matching with validation")
    print()
    
    # Create backup
    backup_dir = create_backup()
    
    # Read current CSS content
    css_content = read_file("src/components/MTGOLayout.css")
    if not css_content:
        return False
    
    # Read TSX content
    tsx_content = read_file("src/components/MTGOLayout.tsx")
    if not tsx_content:
        return False
    
    original_lines = len(css_content.splitlines())
    print(f"📊 Original CSS file: {original_lines} lines")
    print()
    
    successful_extractions = []
    
    # Extract Drag and Drop Styles
    drag_drop, css_content = extract_drag_drop_styles(css_content)
    if drag_drop:
        drag_drop_content = f"""/* Drag and Drop Styles */
/* Extracted from MTGOLayout.css - Phase 2 */

{drag_drop}
"""
        if write_file("src/components/DragAndDropStyles.css", drag_drop_content):
            successful_extractions.append('drag_drop')
    
    # Extract Component Styles
    components, css_content = extract_component_styles(css_content)
    if components:
        components_content = f"""/* Component Styles - Buttons, Headers, Controls */
/* Extracted from MTGOLayout.css - Phase 2 */

{components}
"""
        if write_file("src/components/ComponentStyles.css", components_content):
            successful_extractions.append('components')
    
    # Extract Panel Resizing
    resizing, css_content = extract_panel_resizing(css_content)
    if resizing:
        resizing_content = f"""/* Panel Resizing and Resize Handle Styles */
/* Extracted from MTGOLayout.css - Phase 2 */

{resizing}
"""
        if write_file("src/components/PanelResizing.css", resizing_content):
            successful_extractions.append('resizing')
    
    # Only proceed if we had some successful extractions
    if not successful_extractions:
        print()
        print("❌ No sections were successfully extracted!")
        print("🔍 Consider examining the CSS file structure manually")
        return False
    
    # Update original CSS file
    remaining_lines = len(css_content.splitlines())
    print(f"📊 Remaining in MTGOLayout.css: {remaining_lines} lines")
    print(f"📊 Extracted: {original_lines - remaining_lines} lines")
    
    if write_file("src/components/MTGOLayout.css", css_content):
        print("   ✅ Updated MTGOLayout.css")
    
    # Update TSX imports only for successful extractions
    print("🔧 Updating MTGOLayout.tsx imports...")
    updated_tsx = update_imports(tsx_content, successful_extractions)
    if write_file("src/components/MTGOLayout.tsx", updated_tsx):
        print("   ✅ Updated MTGOLayout.tsx imports")
    
    print()
    print("✅ Phase 2 Extraction Complete!")
    print(f"📊 Successfully extracted: {len(successful_extractions)} sections")
    
    print("🧪 Next steps:")
    print("   1. Test the application: npm start")
    print("   2. Verify extracted functionality works")
    print("   3. If issues occur, restore from backup:", backup_dir)
    print()
    print("📁 Successfully created files:")
    for extraction_type in successful_extractions:
        file_mapping = {
            'drag_drop': 'DragAndDropStyles.css',
            'components': 'ComponentStyles.css',
            'resizing': 'PanelResizing.css'
        }
        print(f"   - src/components/{file_mapping[extraction_type]}")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        print("❌ Extraction failed!")
        exit(1)
