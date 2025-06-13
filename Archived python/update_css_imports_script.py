#!/usr/bin/env python3
"""
CSS Import Update Script
Automatically finds and updates CSS import statements to use the new modular structure
"""

import os
import re
from pathlib import Path

class CSSImportUpdater:
    def __init__(self):
        self.src_dir = Path("src")
        self.updated_files = []
        self.backup_dir = Path("css_migration_backups")
        
    def update_all_imports(self):
        """Find and update all CSS imports in the project"""
        print("🔄 Updating CSS imports to use new modular structure...")
        
        # Create backup directory
        self.create_backups()
        
        # Find all relevant files
        files_to_check = self.find_files_with_css_imports()
        
        # Update imports in each file
        for file_path in files_to_check:
            self.update_file_imports(file_path)
        
        # Summary report
        self.generate_update_report()
        
        print("✅ CSS import updates complete!")
        
    def create_backups(self):
        """Create backups of files before modification"""
        print("  💾 Creating backups...")
        
        self.backup_dir.mkdir(exist_ok=True)
        
        # Find all files that might have CSS imports
        files_to_backup = []
        for ext in ['*.tsx', '*.ts', '*.jsx', '*.js']:
            files_to_backup.extend(self.src_dir.rglob(ext))
        
        for file_path in files_to_backup:
            if self.file_contains_css_import(file_path):
                # Create backup
                backup_path = self.backup_dir / file_path.name
                backup_path.write_text(file_path.read_text(encoding='utf-8'), encoding='utf-8')
        
        print(f"    ✅ Created backups for {len([f for f in files_to_backup if self.file_contains_css_import(f)])} files")
    
    def find_files_with_css_imports(self):
        """Find all files that import CSS"""
        print("  🔍 Finding files with CSS imports...")
        
        files_with_imports = []
        
        # Search through TypeScript/JavaScript files
        for ext in ['*.tsx', '*.ts', '*.jsx', '*.js']:
            for file_path in self.src_dir.rglob(ext):
                if self.file_contains_css_import(file_path):
                    files_with_imports.append(file_path)
        
        print(f"    📄 Found {len(files_with_imports)} files with CSS imports")
        return files_with_imports
    
    def file_contains_css_import(self, file_path):
        """Check if file contains CSS imports we need to update"""
        try:
            content = file_path.read_text(encoding='utf-8')
            
            # Look for MTGOLayout.css imports or other CSS imports
            css_import_patterns = [
                r"import\s+['\"].*MTGOLayout\.css['\"]",
                r"import\s+['\"].*\.css['\"]"
            ]
            
            for pattern in css_import_patterns:
                if re.search(pattern, content):
                    return True
            return False
            
        except Exception:
            return False
    
    def update_file_imports(self, file_path):
        """Update CSS imports in a specific file"""
        print(f"  🔧 Updating: {file_path.relative_to(self.src_dir)}")
        
        try:
            content = file_path.read_text(encoding='utf-8')
            original_content = content
            
            # Pattern to match CSS imports
            import_patterns = [
                # Direct MTGOLayout.css imports
                (r"import\s+['\"](\./)?MTGOLayout\.css['\"];?", "import '../styles/main.css';"),
                (r"import\s+['\"](\.\./components/)?MTGOLayout\.css['\"];?", "import '../styles/main.css';"),
                
                # Component-specific CSS imports that should now use main.css
                (r"import\s+['\"]\./(components/)?MTGOLayout\.css['\"];?", "import '../styles/main.css';"),
            ]
            
            updates_made = []
            
            for pattern, replacement in import_patterns:
                matches = re.finditer(pattern, content)
                for match in matches:
                    old_import = match.group(0)
                    updates_made.append(f"    {old_import} → {replacement}")
                    content = re.sub(pattern, replacement, content)
            
            # Handle relative path adjustments based on file location
            content = self.adjust_relative_paths(content, file_path)
            
            # Only write if changes were made
            if content != original_content:
                file_path.write_text(content, encoding='utf-8')
                self.updated_files.append({
                    'file': file_path,
                    'updates': updates_made
                })
                
                if updates_made:
                    for update in updates_made:
                        print(update)
                else:
                    print("    📝 Path adjustments made")
            else:
                print("    ℹ️ No updates needed")
                
        except Exception as e:
            print(f"    ❌ Error updating {file_path}: {e}")
    
    def adjust_relative_paths(self, content, file_path):
        """Adjust relative paths based on file location"""
        # Calculate the relative path from this file to src/styles/main.css
        src_root = Path("src")
        
        # Get the directory containing the current file
        file_dir = file_path.parent
        
        # Calculate relative path to styles directory
        try:
            rel_path_to_src = os.path.relpath(src_root, file_dir)
            styles_path = os.path.join(rel_path_to_src, "styles", "main.css").replace("\\", "/")
            
            # Update the import path if it's currently pointing to main.css with wrong relative path
            content = re.sub(
                r"import\s+['\"]\.\.?/?styles/main\.css['\"];?",
                f"import '{styles_path}';",
                content
            )
            
        except Exception as e:
            print(f"    ⚠️ Could not adjust relative path: {e}")
        
        return content
    
    def generate_update_report(self):
        """Generate a report of all updates made"""
        print("  📋 Generating update report...")
        
        report_content = "# CSS Import Update Report\n\n"
        report_content += f"**Files Updated:** {len(self.updated_files)}\n"
        report_content += f"**Backup Location:** {self.backup_dir}\n\n"
        
        if self.updated_files:
            report_content += "## Files Modified\n\n"
            
            for update_info in self.updated_files:
                file_path = update_info['file']
                updates = update_info['updates']
                
                report_content += f"### {file_path.relative_to(self.src_dir)}\n"
                
                if updates:
                    for update in updates:
                        report_content += f"- {update.strip()}\n"
                else:
                    report_content += "- Path adjustments made\n"
                
                report_content += "\n"
        else:
            report_content += "## No Updates Required\n\n"
            report_content += "All CSS imports are already using the correct paths.\n"
        
        report_content += "\n## Next Steps\n\n"
        report_content += "1. Test your application: `npm start`\n"
        report_content += "2. Verify all styles are working correctly\n"
        report_content += "3. Run validation script: `python validate_css_migration.py`\n"
        report_content += "4. If issues occur, restore from backups in `css_migration_backups/`\n"
        
        # Save report
        report_path = Path("CSS_IMPORT_UPDATE_REPORT.md")
        report_path.write_text(report_content, encoding='utf-8')
        
        print(f"    📄 Report saved: {report_path}")
    
    def find_main_layout_component(self):
        """Try to automatically find the main layout component"""
        print("  🎯 Searching for main layout component...")
        
        # Common patterns for main layout files
        layout_patterns = [
            "**/MTGOLayout.tsx",
            "**/MTGOLayout.ts", 
            "**/App.tsx",
            "**/App.ts",
            "**/Layout.tsx",
            "**/Layout.ts",
            "**/MainLayout.tsx",
            "**/MainLayout.ts"
        ]
        
        found_files = []
        for pattern in layout_patterns:
            found_files.extend(self.src_dir.glob(pattern))
        
        # Look for files that import MTGOLayout.css
        layout_files = []
        for file_path in found_files:
            try:
                content = file_path.read_text(encoding='utf-8')
                if 'MTGOLayout.css' in content:
                    layout_files.append(file_path)
            except Exception:
                continue
        
        if layout_files:
            print(f"    📄 Found potential layout files: {[f.name for f in layout_files]}")
            return layout_files
        else:
            print("    ℹ️ No specific layout files found, will search all files")
            return []

def main():
    """Main execution function"""
    print("🔄 MTG Deck Builder - CSS Import Updater")
    print("=" * 50)
    
    # Check if new CSS structure exists
    styles_dir = Path("src/styles")
    main_css = styles_dir / "main.css"
    
    if not main_css.exists():
        print("❌ New CSS structure not found!")
        print("   Please run the CSS extraction script first:")
        print("   python extract_css_components.py")
        return
    
    print("✅ New CSS structure found, proceeding with import updates...")
    
    updater = CSSImportUpdater()
    updater.update_all_imports()
    
    print("\n🎉 Import updates complete!")
    print("\nNext steps:")
    print("1. Test your application: npm start")
    print("2. Verify styles are working: Check the UI looks identical")
    print("3. Run validation: python validate_css_migration.py")
    print("4. If issues occur: Restore from css_migration_backups/")

if __name__ == "__main__":
    main()
