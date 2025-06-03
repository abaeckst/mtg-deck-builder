#!/usr/bin/env python3
"""
Fix Gap Sizes - Make consistent small gaps (about 1/3 of current size)
Updates both MagicCard.tsx and MTGOLayout.tsx to use smaller, consistent gaps
"""

def fix_magic_card_gaps():
    file_path = "src/components/MagicCard.tsx"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print("✅ Reading MagicCard.tsx")
        
        # Fix the gap calculation in CardGrid component
        old_gap_calc = """    // Improved gap calculation with better minimum spacing
    const baseGap = 10;  // Increased base gap for better spacing
    const proportionalGap = baseGap * clampedScale;
    const minGap = 8;   // Increased minimum gap (was 4px)
    const maxGap = 20;  // Increased maximum gap (was 16px)
    const boundedGap = Math.max(minGap, Math.min(maxGap, proportionalGap));
    const scaledGap = Math.round(boundedGap);"""
        
        new_gap_calc = """    // Consistent small gaps (about 1/3 of previous size)
    const baseGap = 4;  // Reduced base gap for tighter spacing
    const proportionalGap = baseGap * clampedScale;
    const minGap = 3;   // Small minimum gap
    const maxGap = 7;   // Small maximum gap  
    const boundedGap = Math.max(minGap, Math.min(maxGap, proportionalGap));
    const scaledGap = Math.round(boundedGap);"""
        
        if old_gap_calc in content:
            content = content.replace(old_gap_calc, new_gap_calc)
            print("✅ Fixed gap calculation in MagicCard.tsx")
        else:
            print("⚠️  Gap calculation in MagicCard.tsx not found in expected format")
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        return True
    except Exception as e:
        print(f"❌ Error fixing MagicCard.tsx: {str(e)}")
        return False

def fix_mtgo_layout_gaps():
    file_path = "src/components/MTGOLayout.tsx"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print("✅ Reading MTGOLayout.tsx")
        
        # Fix 1: Collection area gap
        old_collection_gap = """              gap: `${Math.max(8, Math.min(20, Math.round(10 * cardSizes.collection)))}px`,"""
        new_collection_gap = """              gap: `${Math.max(3, Math.min(7, Math.round(4 * cardSizes.collection)))}px`,"""
        
        if old_collection_gap in content:
            content = content.replace(old_collection_gap, new_collection_gap)
            print("✅ Fixed collection area gap")
        else:
            print("⚠️  Collection area gap not found in expected format")
        
        # Fix 2: Deck area gap
        old_deck_gap = """                  gap: `${Math.max(8, Math.min(20, Math.round(10 * cardSizes.deck)))}px`,"""
        new_deck_gap = """                  gap: `${Math.max(3, Math.min(7, Math.round(4 * cardSizes.deck)))}px`,"""
        
        if old_deck_gap in content:
            content = content.replace(old_deck_gap, new_deck_gap)
            print("✅ Fixed deck area gap")
        else:
            print("⚠️  Deck area gap not found in expected format")
        
        # Fix 3: Sideboard area gap
        old_sideboard_gap = """                  gap: `${Math.max(8, Math.min(20, Math.round(10 * cardSizes.sideboard)))}px`,"""
        new_sideboard_gap = """                  gap: `${Math.max(3, Math.min(7, Math.round(4 * cardSizes.sideboard)))}px`,"""
        
        if old_sideboard_gap in content:
            content = content.replace(old_sideboard_gap, new_sideboard_gap)
            print("✅ Fixed sideboard area gap")
        else:
            print("⚠️  Sideboard area gap not found in expected format")
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        return True
    except Exception as e:
        print(f"❌ Error fixing MTGOLayout.tsx: {str(e)}")
        return False

def main():
    print("🎯 Fixing gap sizes to be consistent and about 1/3 current size")
    print("="*60)
    
    magic_card_success = fix_magic_card_gaps()
    mtgo_layout_success = fix_mtgo_layout_gaps()
    
    if magic_card_success and mtgo_layout_success:
        print(f"\n🎯 SUCCESS: Fixed gap sizes in both files")
        print("✅ MagicCard.tsx: Updated CardGrid gap calculation")
        print("✅ MTGOLayout.tsx: Updated all three area gap calculations")
        print("\nGap Size Changes:")
        print("• Previous range: 8px - 20px")
        print("• New range: 3px - 7px (about 1/3 the size)")
        print("• All areas now use consistent gap formula")
        print("\nExpected Result:")
        print("• Much tighter spacing between cards")
        print("• More cards visible in each area")
        print("• Consistent gaps across collection, deck, and sideboard")
        print("\nTest with 'npm start' to see the tighter card spacing!")
    else:
        print(f"\n❌ Some fixes failed - check the output above")

if __name__ == "__main__":
    main()
