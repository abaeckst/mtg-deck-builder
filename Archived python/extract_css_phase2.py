#!/usr/bin/env python3
"""
CSS Extraction Script - Phase 2: Drag & Drop, Panel Resizing, Component Styles
Extracting well-defined feature sections with clear boundaries
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
        print(f"✅ Created: {filepath}")
        return True
    except Exception as e:
        print(f"❌ Error writing {filepath}: {e}")
        return False

def extract_drag_drop_styles(content):
    """Extract drag and drop styles section"""
    # Find the drag and drop section - starts with "/* DRAG AND DROP STYLES */"
    start_pattern = r'\/\* DRAG AND DROP STYLES \*\/'
    
    # Find the end - next major section comment or specific end marker
    end_patterns = [
        r'\/\* SMOOTH SLIDER SCALING',
        r'\/\* Enhanced grid container',
        r'\/\* Smooth slider handle',
        r'\/\* Reduced motion support',
        r'\/\* Responsive Design for Smaller Screens'
    ]
    
    start_match = re.search(start_pattern, content)
    if not start_match:
        return None, content
    
    start_pos = start_match.start()
    
    # Find the earliest end pattern
    end_pos = None
    for pattern in end_patterns:
        match = re.search(pattern, content[start_pos:])
        if match:
            current_end = start_pos + match.start()
            if end_pos is None or current_end < end_pos:
                end_pos = current_end
    
    if end_pos is None:
        # If no end pattern found, take to end of file
        end_pos = len(content)
    
    # Extract the section
    extracted = content[start_pos:end_pos].strip()
    
    # Remove from original content
    remaining = content[:start_pos] + content[end_pos:]
    remaining = re.sub(r'\n\s*\n\s*\n', '\n\n', remaining)  # Clean up extra newlines
    
    return extracted, remaining

def extract_component_styles(content):
    """Extract component styles (buttons, headers, controls)"""
    component_sections = []
    
    # Define component style patterns to extract
    patterns = [
        r'(\/\* Panel Headers[^\/]*?(?=\/\* [A-Z]))',  # Panel Headers
        r'(\/\* View Controls[^\/]*?(?=\/\* [A-Z]))',  # View Controls  
        r'(\/\* PHASE 3B-1: Size slider styles[^\/]*?(?=\/\* [A-Z]))',  # Size sliders
        r'(\/\* Deck Controls[^\/]*?(?=\/\* [A-Z]))',  # Deck Controls
        r'(\/\* Sideboard Controls[^\/]*?(?=\/\* [A-Z]))',  # Sideboard Controls
        r'(\/\* Quick Actions[^\/]*?(?=\/\* [A-Z]))',  # Quick Actions
    ]
    
    remaining = content
    
    for pattern in patterns:
        matches = re.finditer(pattern, remaining, re.DOTALL)
        for match in matches:
            section = match.group(1).strip()
            if section and section not in component_sections:
                component_sections.append(section)
                remaining = remaining.replace(match.group(1), '', 1)
    
    if component_sections:
        extracted = '\n\n'.join(component_sections)
        remaining = re.sub(r'\n\s*\n\s*\n', '\n\n', remaining)  # Clean up extra newlines
        return extracted, remaining
    
    return None, content

def extract_panel_resizing(content):
    """Extract panel resizing and resize handle styles"""
    # Look for resize handle sections
    patterns = [
        r'(\/\* Enhanced Resize Handles[^\/]*?(?=\/\* [A-Z]))',  # Enhanced resize handles
        r'(\/\* ===== EXTENDED PANEL RESIZING[^\/]*?(?=\/\* ===== END EXTENDED PANEL RESIZING))',  # Extended panel resizing
    ]
    
    resize_sections = []
    remaining = content
    
    for pattern in patterns:
        matches = re.finditer(pattern, remaining, re.DOTALL)
        for match in matches:
            section = match.group(1).strip()
            if section and section not in resize_sections:
                resize_sections.append(section)
                remaining = remaining.replace(match.group(1), '', 1)
    
    if resize_sections:
        extracted = '\n\n'.join(resize_sections)
        remaining = re.sub(r'\n\s*\n\s*\n', '\n\n', remaining)  # Clean up extra newlines
        return extracted, remaining
    
    return None, content

def update_imports(tsx_content):
    """Update imports in MTGOLayout.tsx"""
    # Add new imports after the existing CSS imports
    import_lines = [
        "import './DragAndDropStyles.css';",
        "import './ComponentStyles.css';", 
        "import './PanelResizing.css';"
    ]
    
    # Find the existing CSS imports section
    for import_line in import_lines:
        if import_line not in tsx_content:
            # Add after the MTGOLayout.css import
            tsx_content = tsx_content.replace(
                "import './MTGOLayout.css';",
                f"import './MTGOLayout.css';\n{import_line}"
            )
    
    return tsx_content

def main():
    """Main extraction function"""
    print("🚀 Starting CSS Phase 2 Extraction")
    print("📋 Target: Drag & Drop, Panel Resizing, Component Styles")
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
    
    # Extract Drag and Drop Styles
    print("🔧 Extracting Drag and Drop Styles...")
    drag_drop, css_content = extract_drag_drop_styles(css_content)
    if drag_drop:
        drag_drop_content = f"""/* Drag and Drop Styles */
/* Extracted from MTGOLayout.css - Phase 2 */

{drag_drop}
"""
        write_file("src/components/DragAndDropStyles.css", drag_drop_content)
        print(f"   ✅ Drag & Drop extracted: {len(drag_drop.splitlines())} lines")
    else:
        print("   ❌ Drag & Drop section not found")
    
    # Extract Component Styles
    print("🔧 Extracting Component Styles...")
    components, css_content = extract_component_styles(css_content)
    if components:
        components_content = f"""/* Component Styles - Buttons, Headers, Controls */
/* Extracted from MTGOLayout.css - Phase 2 */

{components}
"""
        write_file("src/components/ComponentStyles.css", components_content)
        print(f"   ✅ Component Styles extracted: {len(components.splitlines())} lines")
    else:
        print("   ❌ Component Styles section not found")
    
    # Extract Panel Resizing
    print("🔧 Extracting Panel Resizing...")
    resizing, css_content = extract_panel_resizing(css_content)
    if resizing:
        resizing_content = f"""/* Panel Resizing and Resize Handle Styles */
/* Extracted from MTGOLayout.css - Phase 2 */

{resizing}
"""
        write_file("src/components/PanelResizing.css", resizing_content)
        print(f"   ✅ Panel Resizing extracted: {len(resizing.splitlines())} lines")
    else:
        print("   ❌ Panel Resizing section not found")
    
    # Update original CSS file
    remaining_lines = len(css_content.splitlines())
    print(f"📊 Remaining in MTGOLayout.css: {remaining_lines} lines")
    print(f"📊 Extracted: {original_lines - remaining_lines} lines")
    
    if write_file("src/components/MTGOLayout.css", css_content):
        print("   ✅ Updated MTGOLayout.css")
    
    # Update TSX imports
    print("🔧 Updating MTGOLayout.tsx imports...")
    updated_tsx = update_imports(tsx_content)
    if write_file("src/components/MTGOLayout.tsx", updated_tsx):
        print("   ✅ Updated MTGOLayout.tsx imports")
    
    print()
    print("✅ Phase 2 Extraction Complete!")
    print("🧪 Next steps:")
    print("   1. Test the application: npm start")
    print("   2. Verify drag & drop functionality works perfectly")
    print("   3. Test all panel resizing handles")
    print("   4. Check all buttons, headers, and controls")
    print("   5. If issues occur, restore from backup:", backup_dir)
    print()
    print("📁 Created files:")
    print("   - src/components/DragAndDropStyles.css")
    print("   - src/components/ComponentStyles.css")
    print("   - src/components/PanelResizing.css")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        print("❌ Extraction failed!")
        exit(1)
