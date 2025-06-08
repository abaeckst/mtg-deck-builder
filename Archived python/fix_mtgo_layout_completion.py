#!/usr/bin/env python3

import os
import sys

def fix_mtgo_layout_complete():
    """Fix the incomplete MTGOLayout.tsx file by completing the missing sections"""
    
    filename = "src/components/MTGOLayout.tsx"
    
    if not os.path.exists(filename):
        print(f"Error: {filename} not found")
        return False
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the incomplete line and complete the file
    incomplete_pattern = """                          instanceId={"""
    
    if incomplete_pattern in content:
        # Replace from the incomplete line to end with the complete ending
        cut_index = content.find(incomplete_pattern)
        
        # Keep everything before the incomplete line
        before_incomplete = content[:cut_index]
        
        # Add the complete ending
        complete_ending = """                          instanceId={representativeCard.instanceId}
                          isInstance={true}
                          onInstanceClick={handleStackInstanceClick}
                          onEnhancedDoubleClick={handleDoubleClick}
                          onRightClick={handleRightClick}
                          onDragStart={handleStackDragStart}
                          showQuantity={true}
                          quantity={quantity}
                          selected={isAnySelected}
                          selectable={true}
                          isDragActive={dragState.isDragging}
                          isBeingDragged={dragState.draggedCards.some(dc => 
                            instances.some(inst => 
                              'instanceId' in dc ? dc.instanceId === inst.instanceId : dc.id === inst.cardId
                            )
                          )}
                          selectedCards={getSelectedCardObjects()}
                        />
                      );
                    });
                  })()}
                  
                  {sideboard.length === 0 && (
                    <div className="empty-sideboard-message">
                      Drag cards here for your sideboard
                    </div>
                  )}
                </div>
              )}
            </div>
            
            {/* Resize Handle */}
            <div 
              className="resize-handle resize-handle-left"
              onMouseDown={resizeHandlers.onSideboardResize}
              title="Drag to resize sideboard"
              style={{
                position: 'absolute',
                top: 0,
                left: -3,
                width: 6,
                height: '100%',
                cursor: 'ew-resize',
                background: 'linear-gradient(90deg, transparent 0%, #555555 50%, transparent 100%)',
                zIndex: 1001,
                opacity: 0.7,
                transition: 'opacity 0.2s ease'
              }}
              onMouseEnter={(e) => e.currentTarget.style.opacity = '1'}
              onMouseLeave={(e) => e.currentTarget.style.opacity = '0.7'}
            />
          </DropZoneComponent>
        </div>
      </div>

      {/* Export Modals */}
      <TextExportModal
        isOpen={showTextExportModal}
        onClose={handleCloseTextExport}
        mainDeck={mainDeck}
        sideboard={sideboard}
        format={activeFilters.format}
        deckName="Untitled Deck"
      />
      
      <ScreenshotModal
        isOpen={showScreenshotModal}
        onClose={handleCloseScreenshot}
        mainDeck={mainDeck}
        sideboard={sideboard}
        deckName="Untitled Deck"
      />

      {/* Context Menu */}
      <ContextMenu
        visible={contextMenuState.visible}
        x={contextMenuState.x}
        y={contextMenuState.y}
        actions={getContextMenuActions()}
        onClose={hideContextMenu}
      />
    </div>
  );
};

export default MTGOLayout;"""
        
        # Combine the parts
        new_content = before_incomplete + complete_ending
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print("✅ Successfully completed the MTGOLayout.tsx file")
        return True
    else:
        print("❌ Could not find the incomplete pattern")
        return False

if __name__ == "__main__":
    success = fix_mtgo_layout_complete()
    sys.exit(0 if success else 1)