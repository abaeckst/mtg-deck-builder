#!/usr/bin/env python3
"""
Direct fix for collection-grid div - add ref and key props
"""

import re

def fix_collection_grid():
    """Add ref and key to collection-grid div"""
    print("🔧 Applying direct collection-grid fix...")
    
    try:
        # Read the file
        with open('src/components/MTGOLayout.tsx', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find and replace the collection-grid div with exact match
        pattern = r'(<div\s+className="collection-grid"\s+data-cards-loaded=\{cards\.length\})'
        
        replacement = r'''<div 
                className="collection-grid"
                ref={collectionGridRef}
                key={`collection-grid-${cards.length}`}
                data-cards-loaded={cards.length}'''
        
        if re.search(pattern, content):
            content = re.sub(pattern, replacement, content)
            print("✅ Added ref and key to collection-grid")
        else:
            print("❌ Could not find collection-grid pattern")
            return False
        
        # Write the fixed content
        with open('src/components/MTGOLayout.tsx', 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("\n🎯 SUCCESS! Collection-grid div now has:")
        print("1. ✅ ref={collectionGridRef}")
        print("2. ✅ key={`collection-grid-${cards.length}`}")
        print("\nThis will force React to re-render when cards.length changes!")
        print("Test Load More in Card view now - it should work!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    fix_collection_grid()
