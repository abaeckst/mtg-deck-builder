#!/usr/bin/env python3

import os
import sys

def fix_load_more_button():
    """Add missing Load More Results section to MTGOLayout.tsx collection area"""
    
    filename = "src/components/MTGOLayout.tsx"
    
    if not os.path.exists(filename):
        print(f"Error: {filename} not found")
        return False
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the collection grid section end
    search_pattern = """              </div>
            )
          )}
          
          {/* PHASE 3A: Enhanced Resize Handle with larger hit zone and visibility */}"""
    
    # Insert the Load More section before the resize handle
    load_more_section = """              </div>
            )
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
          
          {/* PHASE 3A: Enhanced Resize Handle with larger hit zone and visibility */}"""
    
    if search_pattern in content:
        content = content.replace(search_pattern, load_more_section)
        print("✅ Added Load More Results section to collection area")
    else:
        print("❌ Could not find collection grid end pattern")
        return False
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Successfully restored Load More Results button in {filename}")
    return True

if __name__ == "__main__":
    success = fix_load_more_button()
    sys.exit(0 if success else 1)