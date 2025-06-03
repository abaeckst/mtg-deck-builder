# PileView Individual Selection Fix - CORRECTED File Update Script
# This script fixes the compilation errors from the previous attempt

import os
import sys

def find_and_replace_file(file_path, replacements):
    """Apply multiple find-and-replace operations to a file"""
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return False
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        original_content = content
        
        for find_text, replace_text in replacements:
            if find_text not in content:
                print(f"⚠️ Text not found in {file_path}: {find_text[:50]}...")
                continue
            content = content.replace(find_text, replace_text)
            print(f"✅ Replaced text in {file_path}")
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)
            print(f"✅ Successfully updated {file_path}")
            return True
        else:
            print(f"⚠️ No changes made to {file_path}")
            return False
            
    except Exception as e:
        print(f"❌ Error updating {file_path}: {e}")
        return False

def main():
    """Main function to apply corrected pile view individual selection fixes"""
    print("🚀 Starting CORRECTED PileView Individual Selection Implementation...")
    
    # STEP 1: Fix MTGOLayout.tsx - First, need to fix the function naming issue
    mtgo_layout_fixes = [
        # First, fix the missing function definition issue by updating the useLayout import/usage
        (
            """  const { layout, updatePanelDimensions, updateDeckAreaHeightByPixels, updateViewMode, constraints } = useLayout();""",
            """  const { layout, updatePanelDimensions, updateDeckAreaHeightByPixels, updateViewMode, constraints } = useLayout();"""
        ),
        # Fix the function name - use the original updateViewMode with inline clearSelection
        (
            """                onClick={() => updateViewModeWithClearSelection('collection', 'grid')}""",
            """                onClick={() => { clearSelection(); updateViewMode('collection', 'grid'); }}"""
        ),
        (
            """                onClick={() => updateViewModeWithClearSelection('collection', 'list')}""",
            """                onClick={() => { clearSelection(); updateViewMode('collection', 'list'); }}"""
        ),
        (
            """                  onClick={() => updateViewModeWithClearSelection('deck', 'card')}""",
            """                  onClick={() => { clearSelection(); updateViewMode('deck', 'card'); }}"""
        ),
        (
            """                  onClick={() => updateViewModeWithClearSelection('deck', 'pile')}""",
            """                  onClick={() => { clearSelection(); updateViewMode('deck', 'pile'); }}"""
        ),
        (
            """                  onClick={() => updateViewModeWithClearSelection('deck', 'list')}""",
            """                  onClick={() => { clearSelection(); updateViewMode('deck', 'list'); }}"""
        ),
        (
            """                  onClick={() => updateViewModeWithClearSelection('sideboard', 'card')}""",
            """                  onClick={() => { clearSelection(); updateViewMode('sideboard', 'card'); }}"""
        ),
        (
            """                  onClick={() => updateViewModeWithClearSelection('sideboard', 'pile')}""",
            """                  onClick={() => { clearSelection(); updateViewMode('sideboard', 'pile'); }}"""
        ),
        (
            """                  onClick={() => updateViewModeWithClearSelection('sideboard', 'list')}""",
            """                  onClick={() => { clearSelection(); updateViewMode('sideboard', 'list'); }}"""
        ),
        # Remove the erroneous function definition that was added
        (
            """  // Update view modes with selection clearing
  const updateViewModeWithClearSelection = useCallback((area: keyof LayoutState['viewModes'], mode: string) => {
    // Clear selections when switching view modes for better UX
    clearSelection();
    
    setLayout(prev => {
      const newLayout = {
        ...prev,
        viewModes: {
          ...prev.viewModes,
          [area]: mode,
        },
      };
      saveLayout(newLayout);
      return newLayout;
    });
  }, [saveLayout, clearSelection]);""",
            """  // View mode switching with selection clearing is now handled inline"""
        )
    ]
    
    # STEP 2: Fix PileView.tsx - Fix the onClick type mismatch
    pile_view_fixes = [
        # Fix the type issue in PileColumn props
        (
            """        // Pass through all interaction handlers including instance support
        onClick={onInstanceClick || onClick} // Prefer instance click for deck/sideboard""",
            """        // Pass through all interaction handlers
        onClick={onClick}"""
        ),
        # Add proper onInstanceClick passing
        (
            """        onClick={onClick}
        onDoubleClick={onDoubleClick}
        onEnhancedDoubleClick={onEnhancedDoubleClick}
        onRightClick={onRightClick}
        onDragStart={onDragStart}
        isSelected={isSelected}
        selectedCards={selectedCards}
        isDragActive={isDragActive}
        onDragEnter={onDragEnter}
        onDragLeave={onDragLeave}
        canDropInZone={canDropInZone}
        onManualMove={handleManualMove}""",
            """        onClick={onClick}
        onInstanceClick={onInstanceClick}
        onDoubleClick={onDoubleClick}
        onEnhancedDoubleClick={onEnhancedDoubleClick}
        onRightClick={onRightClick}
        onDragStart={onDragStart}
        isSelected={isSelected}
        selectedCards={selectedCards}
        isDragActive={isDragActive}
        onDragEnter={onDragEnter}
        onDragLeave={onDragLeave}
        canDropInZone={canDropInZone}
        onManualMove={handleManualMove}"""
        )
    ]
    
    # STEP 3: Fix PileColumn.tsx - Fix the onInstanceClick type issue
    pile_column_fixes = [
        # Fix the type incompatible issue by properly handling the click handlers
        (
            """                onClick={isInstance ? undefined : onClick} // Use instance click for instances
                onInstanceClick={isInstance ? onClick : undefined} // Pass instance click handler""",
            """                onClick={isInstance ? undefined : onClick} // Use card click for non-instances
                onInstanceClick={isInstance ? onInstanceClick : undefined} // Pass instance click handler
                instanceId={isInstance ? card.instanceId : undefined}
                isInstance={isInstance}"""
        ),
        # Remove the duplicate lines that were added
        (
            """                onInstanceClick={isInstance ? onInstanceClick : undefined} // Pass instance click handler
                instanceId={isInstance ? card.instanceId : undefined}
                isInstance={isInstance}
                instanceId={isInstance ? card.instanceId : undefined}
                isInstance={isInstance}""",
            """                onInstanceClick={isInstance ? onInstanceClick : undefined} // Pass instance click handler"""
        )
    ]
    
    # STEP 4: Simplified approach for individual selection in pile view
    # Let's create a cleaner implementation by updating the DraggableCard onClick logic
    pile_column_simplified_fix = [
        # Fix the renderCards function to use proper click handling
        (
            """          // Determine if this is an instance card and use appropriate selection logic
          const isInstance = 'instanceId' in card;
          const selectionId = isInstance ? card.instanceId : `${card.id}-${i}`;
          
          renderedCards.push(
            <div
              key={selectionId}
              className="pile-card-stack-item"
              style={{
                marginTop: cardIndex > 0 ? `${stackOffset}px` : '0px', // Stack ALL cards, not just same card
                zIndex: cardIndex, // Last card has highest z-index (most visible), first card lowest
                position: 'relative',
              }}
            >
              <DraggableCard
                card={card}
                zone={zone}
                size="normal"
                scaleFactor={scaleFactor}
                onClick={isInstance ? undefined : onClick} // Use card click for non-instances
                onInstanceClick={isInstance ? onInstanceClick : undefined} // Pass instance click handler
                instanceId={isInstance ? card.instanceId : undefined}
                isInstance={isInstance}
                onDoubleClick={onDoubleClick}
                onEnhancedDoubleClick={onEnhancedDoubleClick}
                onRightClick={onRightClick}
                onDragStart={onDragStart}
                showQuantity={false} // Don't show quantity on individual cards
                quantity={1} // Each rendered card represents 1 copy
                selected={isSelected ? isSelected(selectionId) : false}
                selectable={true}
                isDragActive={isDragActive}
                isBeingDragged={isDragActive && selectedCards.some(sc => {
                  if (isInstance) {
                    return 'instanceId' in sc ? sc.instanceId === card.instanceId : false;
                  } else {
                    return getCardId(sc) === getCardId(card);
                  }
                })}
                selectedCards={selectedCards}
              />
            </div>
          );""",
            """          // Determine if this is an instance card and use appropriate selection logic
          const isInstance = 'instanceId' in card;
          const selectionId = isInstance ? card.instanceId : `${card.id}-${i}`;
          
          renderedCards.push(
            <div
              key={selectionId}
              className="pile-card-stack-item"
              style={{
                marginTop: cardIndex > 0 ? `${stackOffset}px` : '0px', // Stack ALL cards, not just same card
                zIndex: cardIndex, // Last card has highest z-index (most visible), first card lowest
                position: 'relative',
              }}
            >
              <DraggableCard
                card={card}
                zone={zone}
                size="normal"
                scaleFactor={scaleFactor}
                onClick={isInstance ? undefined : onClick} // Use regular click for non-instances
                onInstanceClick={isInstance ? onInstanceClick : undefined} // Use instance click for instances
                instanceId={isInstance ? card.instanceId : undefined}
                isInstance={isInstance}
                onDoubleClick={onDoubleClick}
                onEnhancedDoubleClick={onEnhancedDoubleClick}
                onRightClick={onRightClick}
                onDragStart={onDragStart}
                showQuantity={false} // Don't show quantity on individual cards
                quantity={1} // Each rendered card represents 1 copy
                selected={isSelected ? isSelected(selectionId) : false}
                selectable={true}
                isDragActive={isDragActive}
                isBeingDragged={isDragActive && selectedCards.some(sc => {
                  if (isInstance) {
                    return 'instanceId' in sc ? sc.instanceId === card.instanceId : false;
                  } else {
                    return getCardId(sc) === getCardId(card);
                  }
                })}
                selectedCards={selectedCards}
              />
            </div>
          );"""
        )
    ]
    
    # Apply all fixes in order
    success_count = 0
    total_updates = 3
    
    print("\n📋 Step 1: Fixing MTGOLayout.tsx compilation errors...")
    if find_and_replace_file("src/components/MTGOLayout.tsx", mtgo_layout_fixes):
        success_count += 1
        print("✅ MTGOLayout.tsx compilation errors fixed")
    
    print("\n📋 Step 2: Fixing PileView.tsx type mismatches...")
    if find_and_replace_file("src/components/PileView.tsx", pile_view_fixes):
        success_count += 1
        print("✅ PileView.tsx type issues fixed")
    
    print("\n📋 Step 3: Fixing PileColumn.tsx click handler issues...")
    if find_and_replace_file("src/components/PileColumn.tsx", pile_column_fixes + pile_column_simplified_fix):
        success_count += 1
        print("✅ PileColumn.tsx click handler issues fixed")
    
    # Report results
    print(f"\n🎯 Summary:")
    print(f"✅ Successfully fixed: {success_count}/{total_updates} files")
    
    if success_count == total_updates:
        print("\n🚀 All compilation errors fixed!")
        print("\n📋 What was corrected:")
        print("✅ Fixed missing updateViewModeWithClearSelection function")
        print("✅ Fixed onClick/onInstanceClick type mismatches")
        print("✅ Simplified click handler logic for better compatibility")
        print("✅ Selection clearing now works with inline function calls")
        
        print("\n🧪 Testing checklist:")
        print("1. Verify application compiles without TypeScript errors")
        print("2. Test individual card selection in pile view")
        print("3. Test selection clearing when switching view modes")
        print("4. Verify pile view stacking still works correctly")
    else:
        print("\n⚠️ Some fixes failed. Check the error messages above.")
    
    print(f"\n✨ Compilation error fixes complete!")

if __name__ == "__main__":
    main()
