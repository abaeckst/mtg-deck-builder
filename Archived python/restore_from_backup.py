#!/usr/bin/env python3
"""
Quick restoration script to restore from Phase 2 backup
"""

import os
import shutil
import glob

def find_latest_backup():
    """Find the most recent Phase 2 backup directory"""
    backup_dirs = glob.glob("css_phase2_backup_*")
    if not backup_dirs:
        print("❌ No Phase 2 backup directories found")
        return None
    
    # Sort by name (which includes timestamp)
    backup_dirs.sort(reverse=True)
    latest = backup_dirs[0]
    print(f"📁 Found latest backup: {latest}")
    return latest

def restore_files(backup_dir):
    """Restore files from backup"""
    try:
        # Restore MTGOLayout.css
        if os.path.exists(f"{backup_dir}/MTGOLayout.css"):
            shutil.copy2(f"{backup_dir}/MTGOLayout.css", "src/components/MTGOLayout.css")
            print("✅ Restored MTGOLayout.css")
        
        # Restore MTGOLayout.tsx
        if os.path.exists(f"{backup_dir}/MTGOLayout.tsx"):
            shutil.copy2(f"{backup_dir}/MTGOLayout.tsx", "src/components/MTGOLayout.tsx")
            print("✅ Restored MTGOLayout.tsx")
        
        # Remove any partial extraction files
        partial_files = [
            "src/components/DragAndDropStyles.css",
            "src/components/ComponentStyles.css", 
            "src/components/PanelResizing.css"
        ]
        
        for file in partial_files:
            if os.path.exists(file):
                os.remove(file)
                print(f"🗑️  Removed partial file: {file}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error restoring files: {e}")
        return False

def main():
    """Main restoration function"""
    print("🔄 Restoring from Phase 2 backup...")
    print()
    
    backup_dir = find_latest_backup()
    if not backup_dir:
        return False
    
    if restore_files(backup_dir):
        print()
        print("✅ Restoration complete!")
        print("🧪 Test the application: npm start")
        print("📋 Ready to debug and retry Phase 2 extraction")
        return True
    else:
        print("❌ Restoration failed!")
        return False

if __name__ == "__main__":
    success = main()
    if not success:
        exit(1)
