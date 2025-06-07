#!/usr/bin/env python3

import os
import sys

def fix_jsx_loadmore(filename):
    """Fix JSX syntax error by properly wrapping ListView and Load More in container"""
    
    if not os.path.exists(filename):
        print(f"Error: {filename} not found")
        return False
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # First, let's remove the broken JSX that was added
    updates = [
        # 1. Remove the broken JSX section that was added after ListView
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
              )}""",
         """              <>
                <ListView
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
                )}
              </>"""),
        
        # 2. Also fix the card grid section that might have similar issues
        ("""                ))}
                
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
    success_count = 0
    for old_str, new_str in updates:
        if old_str in content:
            content = content.replace(old_str, new_str)
            success_count += 1
            print(f"✅ Fixed JSX structure for element {success_count}")
        else:
            print(f"⚠️ Could not find JSX pattern {success_count + 1} - may already be fixed")
    
    if success_count == 0:
        print("❌ No JSX patterns found to fix - file may have different structure")
        return False
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Successfully fixed JSX syntax in {filename}")
    print(f"✅ Fixed {success_count} JSX structure issues")
    return True

if __name__ == "__main__":
    success = fix_jsx_loadmore("src/components/MTGOLayout.tsx")
    sys.exit(0 if success else 1)