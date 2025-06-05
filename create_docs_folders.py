#!/usr/bin/env python3
"""
Create folder structure for MTG Deck Builder documentation archive
Run this script from the project root directory (where package.json is located)
"""

import os

def create_folder_structure():
    """Create the complete documentation folder structure"""
    
    # Base documentation path
    base_path = "Documentation Library"
    
    # Folder structure to create
    folders = [
        # Completed phases
        "docs/completed/phase-1",
        "docs/completed/phase-2", 
        "docs/completed/phase-3",
        
        # Methodology evolution
        "docs/methodology",
        
        # Planning (for future phases - stays active)
        "docs/planning"
    ]
    
    print("Creating MTG Deck Builder documentation folder structure...")
    print(f"Base path: {base_path}")
    print()
    
    # Create base Documentation Library folder if it doesn't exist
    if not os.path.exists(base_path):
        os.makedirs(base_path)
        print(f"✅ Created: {base_path}")
    else:
        print(f"📁 Exists: {base_path}")
    
    # Create all subfolders
    created_count = 0
    existing_count = 0
    
    for folder in folders:
        full_path = os.path.join(base_path, folder)
        
        if not os.path.exists(full_path):
            os.makedirs(full_path)
            print(f"✅ Created: {full_path}")
            created_count += 1
        else:
            print(f"📁 Exists: {full_path}")
            existing_count += 1
    
    print()
    print("📋 Folder structure creation complete!")
    print(f"   Created: {created_count} new folders")
    print(f"   Existing: {existing_count} folders")
    print()
    
    # Create placeholder README files for organization
    readme_files = [
        ("docs/completed/README.md", 
         "# Completed Phase Documentation\n\nThis folder contains completion documents for all finished development phases.\n\nEach phase folder includes:\n- Requirements document (pre-implementation planning)\n- Completion document (post-implementation technical summary)\n"),
        
        ("docs/methodology/README.md",
         "# Development Methodology Evolution\n\nThis folder contains documentation about architectural decisions and development approaches that evolved during the project.\n\nThese documents capture:\n- Technical architecture patterns\n- Development methodology changes\n- Key decision rationale\n"),
        
        ("docs/planning/README.md",
         "# Active Planning Documents\n\nThis folder contains planning documents for future development phases.\n\nNote: These documents remain active in project knowledge until implementation is complete.\n")
    ]
    
    print("Creating organizational README files...")
    for readme_path, content in readme_files:
        full_readme_path = os.path.join(base_path, readme_path)
        
        if not os.path.exists(full_readme_path):
            with open(full_readme_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"📝 Created: {full_readme_path}")
        else:
            print(f"📝 Exists: {full_readme_path}")
    
    print()
    print("🎯 Documentation structure ready for archival process!")
    print()
    print("Next steps:")
    print("1. Create completion documents for Phases 1-3H")
    print("2. Move planning documents to appropriate archive folders")
    print("3. Update Documentation Catalog with archive locations")
    print("4. Clean project knowledge to focus on current status")

if __name__ == "__main__":
    try:
        # Verify we're in the right directory
        if not os.path.exists("package.json"):
            print("❌ Error: This script should be run from the project root directory")
            print("   (The directory containing package.json)")
            print()
            print("   Current directory:", os.getcwd())
            print("   Please navigate to your MTG deck builder project folder and run again.")
            exit(1)
        
        create_folder_structure()
        
    except Exception as e:
        print(f"❌ Error creating folder structure: {e}")
        print("Please check permissions and try again.")
        exit(1)