#!/usr/bin/env python3
"""
Conservative CSS Extraction Script - Load More Results Section
Extract the smallest, most isolated CSS section as a proof-of-concept
"""

import os
import shutil
from datetime import datetime

def create_backup():
    """Create backup of original files"""
    backup_dir = f"css_extraction_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    os.makedirs(backup_dir, exist_ok=True)
    
    # Backup original files
    if os.path.exists('src/components/MTGOLayout.css'):
        shutil.copy2('src/components/MTGOLayout.css', f'{backup_dir}/MTGOLayout.css')
    if os.path.exists('src/components/MTGOLayout.tsx'):
        shutil.copy2('src/components/MTGOLayout.tsx', f'{backup_dir}/MTGOLayout.tsx')
    
    print(f"✅ Backup created: {backup_dir}")
    return backup_dir

def extract_load_more_section():
    """Extract Load More Results section to separate file"""
    
    # Load More Results CSS content (manually identified section)
    load_more_css = """/* ===== LOAD MORE RESULTS FUNCTIONALITY ===== */

/* Load More Results Functionality */
.load-more-section {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
  border-top: 1px solid #3a3a3a;
  background-color: #1e1e1e;
  margin-top: 8px;
}

.load-more-results-btn {
  background: linear-gradient(135deg, #2d5aa0 0%, #1e3d72 100%);
  color: white;
  border: 1px solid #4a7bc8;
  padding: 12px 24px;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.load-more-results-btn:hover:not(:disabled) {
  background: linear-gradient(135deg, #3d6ab0 0%, #2e4d82 100%);
  border-color: #5a8bd8;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.4);
  transform: translateY(-1px);
}

.load-more-results-btn:active:not(:disabled) {
  transform: translateY(0);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.load-more-results-btn:disabled {
  background: #444;
  border-color: #555;
  color: #888;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.loading-progress {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  width: 300px;
}

.progress-bar {
  width: 100%;
  height: 8px;
  background-color: #333;
  border-radius: 4px;
  overflow: hidden;
  box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.3);
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #2d5aa0 0%, #4a7bc8 50%, #2d5aa0 100%);
  background-size: 200% 100%;
  animation: progressPulse 2s ease-in-out infinite;
  transition: width 0.3s ease;
}

@keyframes progressPulse {
  0%, 100% { background-position: 200% 0; }
  50% { background-position: 0% 0; }
}

.progress-text {
  color: #ccc;
  font-size: 13px;
  font-weight: 500;
}

.pagination-info {
  color: #888;
  font-weight: normal;
  font-size: 0.9em;
}

/* ===== END LOAD MORE RESULTS STYLES ===== */
"""
    
    # Write the new LoadMoreStyles.css file
    with open('src/components/LoadMoreStyles.css', 'w', encoding='utf-8') as f:
        f.write(load_more_css)
    
    print("✅ Created src/components/LoadMoreStyles.css")

def update_mtgo_layout_tsx():
    """Add import for new LoadMoreStyles.css"""
    
    with open('src/components/MTGOLayout.tsx', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Add the new import after the existing MTGOLayout.css import
    old_import = "import './MTGOLayout.css';"
    new_import = "import './MTGOLayout.css';\nimport './LoadMoreStyles.css';"
    
    if old_import in content:
        updated_content = content.replace(old_import, new_import)
        
        with open('src/components/MTGOLayout.tsx', 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        print("✅ Updated MTGOLayout.tsx with LoadMoreStyles.css import")
    else:
        print("❌ Could not find MTGOLayout.css import to update")

def remove_load_more_from_main_css():
    """Remove Load More section from main MTGOLayout.css"""
    
    with open('src/components/MTGOLayout.css', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find and remove the Load More section
    start_marker = "/* ===== LOAD MORE RESULTS FUNCTIONALITY ===== */"
    end_marker = "/* ===== END LOAD MORE RESULTS STYLES ===== */"
    
    start_index = content.find(start_marker)
    end_index = content.find(end_marker)
    
    if start_index != -1 and end_index != -1:
        # Remove the entire Load More section including the end marker
        updated_content = content[:start_index] + content[end_index + len(end_marker):]
        
        # Clean up any extra newlines
        updated_content = updated_content.rstrip() + '\n'
        
        with open('src/components/MTGOLayout.css', 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        print("✅ Removed Load More section from MTGOLayout.css")
        print(f"   Removed {end_index + len(end_marker) - start_index} characters")
    else:
        print("❌ Could not find Load More section markers in MTGOLayout.css")

def main():
    """Execute conservative CSS extraction"""
    print("🚀 Starting Conservative CSS Extraction - Load More Results Section")
    print("=" * 60)
    
    # Step 1: Create backup
    backup_dir = create_backup()
    
    # Step 2: Extract Load More section to new file
    extract_load_more_section()
    
    # Step 3: Update MTGOLayout.tsx imports
    update_mtgo_layout_tsx()
    
    # Step 4: Remove Load More section from main CSS
    remove_load_more_from_main_css()
    
    print("\n✅ EXTRACTION COMPLETE")
    print("=" * 60)
    print("Next Steps:")
    print("1. Test the application: npm start")
    print("2. Verify Load More button functionality works identically")
    print("3. If any issues, restore from backup:")
    print(f"   - Copy files from {backup_dir}/ back to src/components/")
    print("4. If successful, this validates the incremental approach!")

if __name__ == "__main__":
    main()
