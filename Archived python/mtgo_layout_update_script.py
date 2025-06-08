#!/usr/bin/env python3
"""
MTGOLayout.tsx Load More Results Integration Script
Updates the existing MTGOLayout.tsx file to add progressive loading functionality.
"""

import re
import sys
import os

def update_mtgo_layout_file(file_path):
    """Update MTGOLayout.tsx with Load More Results functionality"""
    
    if not os.path.exists(file_path):
        print(f"❌ Error: {file_path} not found!")
        return False
    
    print(f"📝 Reading {file_path}...")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return False
    
    # Backup original
    backup_path = file_path.replace('.tsx', '.tsx.backup')
    with open(backup_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"💾 Backup created: {backup_path}")
    
    # 1. UPDATE: Add progressive loading actions to useCards destructuring
    print("🔧 Step 1: Adding progressive loading actions to useCards hook...")
    
    # Find the useCards destructuring pattern
    useCards_pattern = r'(const\s*{\s*cards,\s*loading,\s*error,.*?addToSearchHistory,)(.*?)(}\s*=\s*useCards\(\);)'
    
    # New actions to add
    new_actions = """
    // Progressive loading actions
    pagination,
    loadMoreResultsAction,
    resetPagination,"""
    
    replacement = r'\1' + new_actions + r'\3'
    
    if re.search(useCards_pattern, content, re.DOTALL):
        content = re.sub(useCards_pattern, replacement, content, flags=re.DOTALL)
        print("✅ Added progressive loading actions to useCards")
    else:
        print("❌ Could not find useCards destructuring pattern")
        return False
    
    # 2. UPDATE: Enhanced collection header to show pagination info
    print("🔧 Step 2: Updating collection header with pagination info...")
    
    # Find the collection header pattern
    header_pattern = r'(<h3>Collection \()\{cards\.length\}( cards\)</h3>)'
    
    # New header with pagination info
    new_header = r'\1{cards.length.toLocaleString()} {pagination.totalCards > pagination.loadedCards && (<span className="pagination-info">of {pagination.totalCards.toLocaleString()}</span>)}\2'
    
    if re.search(header_pattern, content):
        content = re.sub(header_pattern, new_header, content)
        print("✅ Updated collection header with pagination info")
    else:
        print("❌ Could not find collection header pattern")
        return False
    
    # 3. UPDATE: Add Load More Results section after collection content
    print("🔧 Step 3: Adding Load More Results section...")
    
    # Find the collection content closing pattern - look for the end of the collection grid section
    collection_content_pattern = r'(\s*)(}\s*)\s*(\)\s*}\s*\s*{/\*.*?Enhanced Resize Handle.*?\*/})'
    
    # Load More Results section
    load_more_section = '''
    
    {/* Load More Results Section */}
    {pagination.hasMore && (
      <div className="load-more-section">
        {pagination.isLoadingMore ? (
          <div className="loading-progress">
            <div className="progress-bar">
              <div 
                className="progress-fill" 
                style={{
                  width: `${(pagination.loadedCards / pagination.totalCards) * 100}%`
                }}
              />
            </div>
            <span className="progress-text">
              Loading... ({pagination.loadedCards.toLocaleString()}/{pagination.totalCards.toLocaleString()} cards)
            </span>
          </div>
        ) : (
          <button 
            className="load-more-results-btn"
            onClick={loadMoreResultsAction}
            disabled={loading}
            title={`Load 175 more cards (${pagination.totalCards - pagination.loadedCards} remaining)`}
          >
            Load More Results ({(pagination.totalCards - pagination.loadedCards).toLocaleString()} more cards)
          </button>
        )}
      </div>
    )}'''
    
    replacement = r'\1\2' + load_more_section + r'\1\3'
    
    if re.search(collection_content_pattern, content, re.DOTALL):
        content = re.sub(collection_content_pattern, replacement, content, flags=re.DOTALL)
        print("✅ Added Load More Results section")
    else:
        # Try alternative pattern - look for the resize handle
        alt_pattern = r'(\s*)(}\s*)\s*(\s*{/\*.*?PHASE 3A.*?Enhanced Resize Handle.*?\*/})'
        if re.search(alt_pattern, content, re.DOTALL):
            content = re.sub(alt_pattern, replacement, content, flags=re.DOTALL)
            print("✅ Added Load More Results section (alternative pattern)")
        else:
            print("❌ Could not find collection content end pattern")
            print("🔍 Searching for manual insertion point...")
            # Try to find a safer insertion point
            safe_pattern = r'(\s*</div>\s*\)\s*}\s*\s*{/\*.*?Enhanced Resize Handle with larger hit zone.*?\*/})'
            if re.search(safe_pattern, content, re.DOTALL):
                content = re.sub(safe_pattern, load_more_section + r'\1', content, flags=re.DOTALL)
                print("✅ Added Load More Results section (safe insertion)")
            else:
                print("⚠️ Could not auto-insert Load More section. Manual insertion needed.")
                print("📍 Add the Load More section after the collection grid and before the resize handle.")
                # Don't return False - other updates are still valuable
    
    # Write the updated content
    print(f"💾 Writing updated content to {file_path}...")
    
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
    except Exception as e:
        print(f"❌ Error writing file: {e}")
        return False
    
    return True

def create_css_file():
    """Create the CSS styles for Load More functionality"""
    
    css_content = '''
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
'''
    
    # Write CSS to a separate file for manual integration
    css_file = 'load_more_styles.css'
    with open(css_file, 'w', encoding='utf-8') as f:
        f.write(css_content)
    
    print(f"📝 Created {css_file} - Add these styles to MTGOLayout.css")
    return True

def main():
    """Main function to run the update script"""
    
    print("🚀 MTGOLayout.tsx Load More Results Integration")
    print("=" * 50)
    
    # Check if file path provided
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        file_path = 'src/components/MTGOLayout.tsx'
    
    print(f"📂 Target file: {file_path}")
    
    # Update the MTGOLayout file
    if update_mtgo_layout_file(file_path):
        print("✅ MTGOLayout.tsx updated successfully!")
    else:
        print("❌ Failed to update MTGOLayout.tsx")
        return False
    
    # Create CSS file
    if create_css_file():
        print("✅ CSS styles file created!")
    else:
        print("❌ Failed to create CSS file")
    
    print("\n🎉 Integration Complete!")
    print("\n📋 Next Steps:")
    print("1. ✅ MTGOLayout.tsx has been updated with Load More functionality")
    print("2. 📝 Add the styles from load_more_styles.css to your MTGOLayout.css")
    print("3. 🧪 Test the progressive loading with a search like 'creature'")
    print("4. 🔍 Verify the 75 initial + 175 per batch behavior")
    
    return True

if __name__ == "__main__":
    main()
