#!/usr/bin/env python3

import os
import sys

def update_mtgo_layout():
    """Move Load More button from filter panel to collection area"""
    
    filename = "src/components/MTGOLayout.tsx"
    
    if not os.path.exists(filename):
        print(f"Error: {filename} not found")
        return False
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Step 1: Remove Load More section from filter panel
    old_filter_section = '''    {/* Load More Results Section */}
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
    
    new_filter_section = ''
    
    # Step 2: Add Load More section to collection area (after the grid/list content)
    old_collection_content = '''            )
          )}
          
          {/* PHASE 3A: Enhanced Resize Handle with larger hit zone */}'''
    
    new_collection_content = '''            )
          )}
          
          {/* Load More Results Section */}
          {!loading && !error && pagination.hasMore && (
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
          )}
          
          {/* PHASE 3A: Enhanced Resize Handle with larger hit zone */}'''
    
    # Apply replacements
    updates = [
        (old_filter_section, new_filter_section, "Remove Load More from filter panel"),
        (old_collection_content, new_collection_content, "Add Load More to collection area")
    ]
    
    for old_str, new_str, desc in updates:
        if old_str in content:
            content = content.replace(old_str, new_str)
            print(f"✅ {desc}")
        else:
            print(f"❌ Could not find: {desc}")
            print(f"Looking for: {old_str[:100]}...")
            return False
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Successfully updated {filename}")
    print("✅ Load More button moved to collection area")
    print("✅ Button will now appear at bottom of search results")
    return True

if __name__ == "__main__":
    success = update_mtgo_layout()
    sys.exit(0 if success else 1)