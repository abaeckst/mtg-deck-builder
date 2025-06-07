#!/usr/bin/env python3

import os
import sys

def update_collection_loadmore(filename):
    """Update MTGOLayout.tsx to integrate Load More button into collection content areas"""
    
    if not os.path.exists(filename):
        print(f"Error: {filename} not found")
        return False
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Make replacements to integrate load more button into collection content
    updates = [
        # 1. Remove the standalone load-more-section after collection content
        ("""          )}
          
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
          )}""",
         """          )}"""),
        
        # 2. Add load more button to ListView
        ("""              <ListView
                cards={sortedCollectionCards}
                area="collection"
                scaleFactor={cardSizes.collection}
                sortCriteria={collectionSort.criteria}
                sortDirection={collectionSort.direction}
                onSortChange={(criteria, direction) => {
                  updateSort('collection', criteria, direction);
                }}
                onClick={handleCardClick}
                onDoubleClick={handleAddToDeck}
                onRightClick={handleRightClick}
                onDragStart={handleDragStart}
                isSelected={isSelected}
                selectedCards={getSelectedCardObjects()}
                isDragActive={dragState.isDragging}
              />""",
         """              <ListView
                cards={sortedCollectionCards}
                area="collection"
                scaleFactor={cardSizes.collection}
                sortCriteria={collectionSort.criteria}
                sortDirection={collectionSort.direction}
                onSortChange={(criteria, direction) => {
                  updateSort('collection', criteria, direction);
                }}
                onClick={handleCardClick}
                onDoubleClick={handleAddToDeck}
                onRightClick={handleRightClick}
                onDragStart={handleDragStart}
                isSelected={isSelected}
                selectedCards={getSelectedCardObjects()}
                isDragActive={dragState.isDragging}
              />
              
              {/* Load More Results integrated into List View */}
              {!loading && !error && pagination.hasMore && (
                <div className="load-more-section-integrated">
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
              )}"""),
        
        # 3. Add load more button to card grid view
        ("""                ))}
              </div>""",
         """                ))}
                
                {/* Load More Results integrated into Card Grid */}
                {!loading && !error && pagination.hasMore && (
                  <div className="load-more-section-integrated" style={{
                    gridColumn: '1 / -1',
                    display: 'flex',
                    justifyContent: 'center',
                    padding: '20px',
                    marginTop: '10px'
                  }}>
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
              </div>""")
    ]
    
    # Apply all updates
    for old_str, new_str in updates:
        if old_str in content:
            content = content.replace(old_str, new_str)
            print(f"✅ Updated load more button integration")
        else:
            print(f"❌ Could not find target section for load more integration")
            return False
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Successfully updated {filename}")
    return True

if __name__ == "__main__":
    success = update_collection_loadmore("src/components/MTGOLayout.tsx")
    sys.exit(0 if success else 1)