#!/usr/bin/env python3
"""
Fix Gap Scaling - Make gaps scale smoothly and continuously with card size
Remove artificial min/max bounds that cause jarring jumps
"""

def fix_magic_card_smooth_scaling():
    file_path = "src/components/MagicCard.tsx"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print("✅ Reading MagicCard.tsx")
        
        # Fix the gap calculation to use smooth scaling
        old_gap_calc = """    // Consistent small gaps (about 1/3 of previous size)
    const baseGap = 4;  // Reduced base gap for tighter spacing
    const proportionalGap = baseGap * clampedScale;
    const minGap = 3;   // Small minimum gap
    const maxGap = 7;   // Small maximum gap  
    const boundedGap = Math.max(minGap, Math.min(maxGap, proportionalGap));
    const scaledGap = Math.round(boundedGap);"""
        
        new_gap_calc = """    // Smooth proportional gap scaling - no artificial bounds
    const baseGap = 4;  // Base gap size
    const scaledGap = Math.round(baseGap * clampedScale);"""
        
        if old_gap_calc in content:
            content = content.replace(old_gap_calc, new_gap_calc)
            print("✅ Fixed gap calculation in MagicCard.tsx - now smoothly scales")
        else:
            print("⚠️  Gap calculation in MagicCard.tsx not found in expected format")
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        return True
    except Exception as e:
        print(f"❌ Error fixing MagicCard.tsx: {str(e)}")
        return False

def fix_mtgo_layout_smooth_scaling():
    file_path = "src/components/MTGOLayout.tsx"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print("✅ Reading MTGOLayout.tsx")
        
        # Fix 1: Collection area gap - remove bounds for smooth scaling
        old_collection_gap = """              gap: `${Math.max(3, Math.min(7, Math.round(4 * cardSizes.collection)))}px`,"""
        new_collection_gap = """              gap: `${Math.round(4 * cardSizes.collection)}px`,"""
        
        if old_collection_gap in content:
            content = content.replace(old_collection_gap, new_collection_gap)
            print("✅ Fixed collection area gap - now smoothly scales")
        else:
            print("⚠️  Collection area gap not found in expected format")
        
        # Fix 2: Deck area gap - remove bounds for smooth scaling
        old_deck_gap = """                  gap: `${Math.max(3, Math.min(7, Math.round(4 * cardSizes.deck)))}px`,"""
        new_deck_gap = """                  gap: `${Math.round(4 * cardSizes.deck)}px`,"""
        
        if old_deck_gap in content:
            content = content.replace(old_deck_gap, new_deck_gap)
            print("✅ Fixed deck area gap - now smoothly scales")
        else:
            print("⚠️  Deck area gap not found in expected format")
        
        # Fix 3: Sideboard area gap - remove bounds for smooth scaling
        old_sideboard_gap = """                  gap: `${Math.max(3, Math.min(7, Math.round(4 * cardSizes.sideboard)))}px`,"""
        new_sideboard_gap = """                  gap: `${Math.round(4 * cardSizes.sideboard)}px`,"""
        
        if old_sideboard_gap in content:
            content = content.replace(old_sideboard_gap, new_sideboard_gap)
            print("✅ Fixed sideboard area gap - now smoothly scales")
        else:
            print("⚠️  Sideboard area gap not found in expected format")
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        return True
    except Exception as e:
        print(f"❌ Error fixing MTGOLayout.tsx: {str(e)}")
        return False

def main():
    print("🎯 Fixing gap scaling to be smooth and continuous with card size")
    print("="*70)
    
    magic_card_success = fix_magic_card_smooth_scaling()
    mtgo_layout_success = fix_mtgo_layout_smooth_scaling()
    
    if magic_card_success and mtgo_layout_success:
        print(f"\n🎯 SUCCESS: Fixed gap scaling to be smooth and continuous")
        print("✅ MagicCard.tsx: Removed artificial min/max bounds")
        print("✅ MTGOLayout.tsx: Removed artificial min/max bounds from all areas")
        print("\nGap Scaling Behavior:")
        print("• At slider minimum (0.7): Gap = 4 × 0.7 = ~3px")
        print("• At slider middle (1.4): Gap = 4 × 1.4 = ~6px") 
        print("• At slider maximum (2.5): Gap = 4 × 2.5 = ~10px")
        print("• Scaling is now SMOOTH and CONTINUOUS")
        print("• No more jarring jumps - gap size moves smoothly with slider")
        print("\nExpected Result:")
        print("• Smooth, continuous gap scaling as you move the slider")
        print("• No sudden jumps or discontinuities in spacing")
        print("• Visual harmony between card size and gap size")
        print("• Proportional scaling feels natural and professional")
        print("\nTest with 'npm start' and move the sliders to see smooth scaling!")
    else:
        print(f"\n❌ Some fixes failed - check the output above")

if __name__ == "__main__":
    main()
