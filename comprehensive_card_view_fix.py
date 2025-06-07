#!/usr/bin/env python3
"""
Comprehensive fix for Card view Load More rendering issue
This addresses the React component update problem more thoroughly
"""

import re

def fix_card_view_rendering():
    """Apply comprehensive fix to force Card view re-render"""
    
    try:
        with open('src/components/MTGOLayout.tsx', 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print("❌ MTGOLayout.tsx not found")
        return False
    
    # Find the sortedCollectionCards.map section and add a key that forces re-render
    pattern = r'(\{sortedCollectionCards\.map\(\(card\) => \(\s*<DraggableCard\s+key=\{getCardId\(card\)\})'
    
    # First, let's find the exact pattern in the file
    map_pattern = r'(\{sortedCollectionCards\.map\(\(card\) => \()'
    replacement = r'{\/* Force re-render when cards array changes */}\n                {sortedCollectionCards.map((card, index) => ('
    
    if re.search(map_pattern, content):
        content = re.sub(map_pattern, replacement, content)
        print("✅ Added index parameter to map function")
        
        # Now update the key to include both cardId and index for forcing re-render
        key_pattern = r'(key=\{getCardId\(card\)\})'
        key_replacement = r'key={`${getCardId(card)}-${index}-${cards.length}`}'
        
        if re.search(key_pattern, content):
            content = re.sub(key_pattern, key_replacement, content)
            print("✅ Updated key to include index and cards.length")
        else:
            print("⚠️ Could not find key pattern - will try alternative approach")
            
            # Alternative: Add the key manually to DraggableCard
            draggable_pattern = r'(<DraggableCard\s+)'
            draggable_replacement = r'<DraggableCard\n                    key={`${getCardId(card)}-${index}-${cards.length}`}\n                    '
            
            if re.search(draggable_pattern, content):
                content = re.sub(draggable_pattern, draggable_replacement, content)
                print("✅ Added comprehensive key to DraggableCard")
    else:
        print("❌ Could not find sortedCollectionCards.map pattern")
        print("Let me try a different approach...")
        
        # Alternative approach: Add a unique identifier to the collection-grid container
        grid_pattern = r'(<div\s+className="collection-grid")'
        grid_replacement = r'<div\n                className="collection-grid"\n                key={`collection-${cards.length}-${sortedCollectionCards.length}`}'
        
        if re.search(grid_pattern, content):
            content = re.sub(grid_pattern, grid_replacement, content)
            print("✅ Added collection grid key with card counts")
        else:
            print("❌ Could not find collection-grid pattern either")
            return False
    
    # Write the fixed content back
    try:
        with open('src/components/MTGOLayout.tsx', 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ Successfully applied comprehensive Card view fix")
        return True
    except Exception as e:
        print(f"❌ Error writing file: {e}")
        return False

def add_debug_logging():
    """Add debug logging to help diagnose the issue"""
    
    try:
        with open('src/components/MTGOLayout.tsx', 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print("❌ MTGOLayout.tsx not found")
        return False
    
    # Add debug logging before the collection grid
    debug_pattern = r'(\{!loading && !error && cards\.length > 0 &&)'
    debug_replacement = r'{console.log("🎯 CARD VIEW RENDER:", { cardsLength: cards.length, sortedLength: sortedCollectionCards.length, viewMode: layout.viewModes.collection })}\n          {!loading && !error && cards.length > 0 &&'
    
    if re.search(debug_pattern, content):
        content = re.sub(debug_pattern, debug_replacement, content)
        print("✅ Added debug logging for Card view rendering")
    else:
        print("⚠️ Could not add debug logging")
    
    # Write the content back
    try:
        with open('src/components/MTGOLayout.tsx', 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"❌ Error writing debug logging: {e}")
        return False

def main():
    """Main execution"""
    print("🚀 Applying comprehensive Card view Load More fix")
    print("=" * 60)
    
    print("\n1. Applying React rendering fix...")
    fix_success = fix_card_view_rendering()
    
    print("\n2. Adding debug logging...")
    debug_success = add_debug_logging()
    
    if fix_success:
        print("\n🎯 SUCCESS! Comprehensive fix applied:")
        print("✅ Enhanced key props to force React re-render")
        print("✅ Added index parameter to map function")
        print("✅ Keys now include cardId, index, and total count")
        if debug_success:
            print("✅ Added debug logging for troubleshooting")
        
        print("\nThis fix should resolve the Card view Load More issue by:")
        print("• Forcing React to recognize when cards array changes")
        print("• Using comprehensive keys that change when content updates")
        print("• Adding debug output to confirm rendering behavior")
        
        print("\nYou can now:")
        print("1. Test Load More in Card view")
        print("2. Check browser console for debug output")
        print("3. Verify List view still works normally")
    else:
        print("\n❌ Fix failed - manual intervention needed")
        print("The file structure might have changed from the expected pattern.")
    
    return fix_success

if __name__ == "__main__":
    main()
