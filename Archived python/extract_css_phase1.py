#!/usr/bin/env python3
"""
CSS Extraction Script - Phase 1: CSS Variables, Mobile Warning, Responsive Design
Manual extraction approach - proven successful in previous session
"""

import os
import re
import shutil
from datetime import datetime

def create_backup():
    """Create backup of original file"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = f"css_phase1_backup_{timestamp}"
    os.makedirs(backup_dir, exist_ok=True)
    
    # Backup original CSS file
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

def extract_css_variables(content):
    """Extract CSS custom properties section"""
    # Find CSS custom properties (lines 3-7)
    css_vars_pattern = r'(\/\* CSS Custom Properties for Dynamic Resizing \*\/\s*:root\s*\{[^}]+\})'
    
    match = re.search(css_vars_pattern, content, re.DOTALL)
    if match:
        extracted = match.group(1).strip()
        remaining = content.replace(match.group(1), '', 1).strip()
        return extracted, remaining
    
    return None, content

def extract_mobile_warning(content):
    """Extract mobile warning section"""
    # Find mobile warning section (lines 21-37)
    mobile_pattern = r'(\/\* Mobile Warning \*\/.*?(?=\/\* [A-Z]))'
    
    match = re.search(mobile_pattern, content, re.DOTALL)
    if match:
        extracted = match.group(1).strip()
        remaining = content.replace(match.group(1), '', 1).strip()
        return extracted, remaining
    
    return None, content

def extract_responsive_design(content):
    """Extract all responsive design media queries"""
    # Find all @media queries
    media_queries = []
    
    # Pattern to match @media blocks
    media_pattern = r'(@media[^{]+\{(?:[^{}]*\{[^{}]*\})*[^{}]*\})'
    
    matches = re.finditer(media_pattern, content, re.DOTALL)
    for match in matches:
        media_queries.append(match.group(1).strip())
    
    if media_queries:
        # Combine all media queries
        extracted = '\n\n'.join(media_queries)
        
        # Remove from original content
        remaining = content
        for query in media_queries:
            remaining = remaining.replace(query, '', 1)
        
        remaining = re.sub(r'\n\s*\n\s*\n', '\n\n', remaining)  # Clean up extra newlines
        return extracted, remaining
    
    return None, content

def update_imports(tsx_content):
    """Update imports in MTGOLayout.tsx"""
    # Add new imports after the existing CSS imports
    import_lines = [
        "import './CSSVariables.css';",
        "import './MobileWarning.css';",
        "import './ResponsiveDesign.css';"
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
    print("🚀 Starting CSS Phase 1 Extraction")
    print("📋 Target: CSS Variables, Mobile Warning, Responsive Design")
    print()
    
    # Create backup
    backup_dir = create_backup()
    
    # Read original CSS content
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
    
    # Extract CSS Variables
    print("🔧 Extracting CSS Variables...")
    css_vars, css_content = extract_css_variables(css_content)
    if css_vars:
        css_vars_content = f"""/* CSS Custom Properties for Dynamic Resizing */
/* Extracted from MTGOLayout.css - Phase 1 */

{css_vars}
"""
        write_file("src/components/CSSVariables.css", css_vars_content)
        print(f"   ✅ CSS Variables extracted: {len(css_vars.splitlines())} lines")
    else:
        print("   ❌ CSS Variables section not found")
    
    # Extract Mobile Warning
    print("🔧 Extracting Mobile Warning...")
    mobile_warning, css_content = extract_mobile_warning(css_content)
    if mobile_warning:
        mobile_content = f"""/* Mobile Warning Styles */
/* Extracted from MTGOLayout.css - Phase 1 */

{mobile_warning}
"""
        write_file("src/components/MobileWarning.css", mobile_content)
        print(f"   ✅ Mobile Warning extracted: {len(mobile_warning.splitlines())} lines")
    else:
        print("   ❌ Mobile Warning section not found")
    
    # Extract Responsive Design
    print("🔧 Extracting Responsive Design...")
    responsive_design, css_content = extract_responsive_design(css_content)
    if responsive_design:
        responsive_content = f"""/* Responsive Design Media Queries */
/* Extracted from MTGOLayout.css - Phase 1 */

{responsive_design}
"""
        write_file("src/components/ResponsiveDesign.css", responsive_content)
        print(f"   ✅ Responsive Design extracted: {len(responsive_design.splitlines())} lines")
    else:
        print("   ❌ Responsive Design section not found")
    
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
    print("✅ Phase 1 Extraction Complete!")
    print("🧪 Next steps:")
    print("   1. Test the application: npm start")
    print("   2. Verify all functionality works identically")
    print("   3. Check console for any CSS errors")
    print("   4. If issues occur, restore from backup:", backup_dir)
    print()
    print("📁 Created files:")
    print("   - src/components/CSSVariables.css")
    print("   - src/components/MobileWarning.css")
    print("   - src/components/ResponsiveDesign.css")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        print("❌ Extraction failed!")
        exit(1)
