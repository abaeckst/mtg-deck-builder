#!/usr/bin/env python3
"""
Fix Card Grid Spacing Issues:
1. Collection area: Fix "one card per row" by using max-content instead of 1fr
2. Deck/Sideboard areas: Fix card overlap with improved gap calculations
"""

def fix_magic_card_component():
    file_path = "src/components/MagicCard.tsx"
    
    try:
        # Read the current file
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print("✅ Successfully read MagicCard.tsx")
        
        # Fix 1: Update CardGrid props interface to include area type
        old_card_grid_props = """export const CardGrid: React.FC<{
  cards: (ScryfallCard | DeckCard)[];
  cardSize?: 'small' | 'normal' | 'large';
  scaleFactor?: number;
  onCardClick?: (card: ScryfallCard | DeckCard) => void;
  onCardDoubleClick?: (card: ScryfallCard | DeckCard) => void;
  showQuantities?: boolean;
  selectedCards?: Set<string>;
  className?: string;
  style?: React.CSSProperties;
}> = ({"""
        
        new_card_grid_props = """export const CardGrid: React.FC<{
  cards: (ScryfallCard | DeckCard)[];
  cardSize?: 'small' | 'normal' | 'large';
  scaleFactor?: number;
  onCardClick?: (card: ScryfallCard | DeckCard) => void;
  onCardDoubleClick?: (card: ScryfallCard | DeckCard) => void;
  showQuantities?: boolean;
  selectedCards?: Set<string>;
  className?: string;
  style?: React.CSSProperties;
  area?: 'collection' | 'deck' | 'sideboard';
}> = ({"""
        
        if old_card_grid_props in content:
            content = content.replace(old_card_grid_props, new_card_grid_props)
            print("✅ Fix 1: Added area prop to CardGrid interface")
        else:
            print("⚠️  Fix 1: CardGrid props interface not found in expected format")
        
        # Fix 2: Update CardGrid destructuring to include area prop
        old_destructuring = """  cards,
  cardSize = 'normal',
  scaleFactor = 1,
  onCardClick,
  onCardDoubleClick,
  showQuantities = false,
  selectedCards = new Set(),
  className = '',
  style,
}) => {"""
        
        new_destructuring = """  cards,
  cardSize = 'normal',
  scaleFactor = 1,
  onCardClick,
  onCardDoubleClick,
  showQuantities = false,
  selectedCards = new Set(),
  className = '',
  style,
  area = 'collection',
}) => {"""
        
        if old_destructuring in content:
            content = content.replace(old_destructuring, new_destructuring)
            print("✅ Fix 2: Updated CardGrid destructuring to include area prop")
        else:
            print("⚠️  Fix 2: CardGrid destructuring not found in expected format")
        
        # Fix 3: Replace the entire getGridSettings function with improved version
        old_get_grid_settings = """  // Calculate dynamic grid column size and gap with proper bounds
  const getGridSettings = () => {
    const baseSizes = {
      small: 70,
      normal: 130, 
      large: 210
    };
    const baseSize = baseSizes[cardSize] || baseSizes.normal;
    const clampedScale = Math.max(0.7, Math.min(2.5, scaleFactor));
    const scaledSize = Math.round(baseSize * clampedScale);
    
    // Proportional gap with minimum and maximum bounds
    const baseGap = 8;
    const proportionalGap = baseGap * clampedScale;
    const minGap = 4;  // Never less than 4px
    const maxGap = 16; // Never more than 16px
    const boundedGap = Math.max(minGap, Math.min(maxGap, proportionalGap));
    const scaledGap = Math.round(boundedGap);
    
    return {
      columnSize: `${scaledSize}px`,
      gap: `${scaledGap}px`
    };
  };"""
        
        new_get_grid_settings = """  // Calculate dynamic grid column size and gap with area-specific behavior
  const getGridSettings = () => {
    const baseSizes = {
      small: 70,
      normal: 130, 
      large: 210
    };
    const baseSize = baseSizes[cardSize] || baseSizes.normal;
    const clampedScale = Math.max(0.7, Math.min(2.5, scaleFactor));
    const scaledSize = Math.round(baseSize * clampedScale);
    
    // Improved gap calculation with better minimum spacing
    const baseGap = 10;  // Increased base gap for better spacing
    const proportionalGap = baseGap * clampedScale;
    const minGap = 8;   // Increased minimum gap (was 4px)
    const maxGap = 20;  // Increased maximum gap (was 16px)
    const boundedGap = Math.max(minGap, Math.min(maxGap, proportionalGap));
    const scaledGap = Math.round(boundedGap);
    
    // Area-specific grid template behavior
    let gridTemplate;
    if (area === 'collection') {
      // Collection: Use max-content to prevent cards from expanding
      gridTemplate = `repeat(auto-fill, minmax(${scaledSize}px, max-content))`;
    } else {
      // Deck/Sideboard: Use 1fr for flexible sizing
      gridTemplate = `repeat(auto-fill, minmax(${scaledSize}px, 1fr))`;
    }
    
    return {
      columnSize: `${scaledSize}px`,
      gap: `${scaledGap}px`,
      gridTemplate: gridTemplate
    };
  };"""
        
        if old_get_grid_settings in content:
            content = content.replace(old_get_grid_settings, new_get_grid_settings)
            print("✅ Fix 3: Updated getGridSettings with area-specific behavior and improved gaps")
        else:
            print("⚠️  Fix 3: getGridSettings function not found in expected format")
        
        # Fix 4: Update grid styles to use the new gridTemplate
        old_grid_styles = """  const { columnSize, gap } = getGridSettings();

  const gridStyles: React.CSSProperties = {
    display: 'grid',
    gridTemplateColumns: `repeat(auto-fill, minmax(${columnSize}, 1fr))`,
    gap: gap,
    padding: '8px',
    ...style,
  };"""
        
        new_grid_styles = """  const { columnSize, gap, gridTemplate } = getGridSettings();

  const gridStyles: React.CSSProperties = {
    display: 'grid',
    gridTemplateColumns: gridTemplate,
    gap: gap,
    padding: '8px',
    ...style,
  };"""
        
        if old_grid_styles in content:
            content = content.replace(old_grid_styles, new_grid_styles)
            print("✅ Fix 4: Updated gridStyles to use area-specific gridTemplate")
        else:
            print("⚠️  Fix 4: gridStyles definition not found in expected format")
        
        # Write the updated content back to the file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"\n🎯 SUCCESS: Fixed MagicCard.tsx grid spacing issues")
        print("✅ Collection area: Will now show multiple cards per row (max-content)")
        print("✅ Deck/Sideboard areas: Improved gap spacing to prevent overlap")
        print("✅ Added area-aware grid behavior")
        print("✅ Increased minimum gaps from 4px to 8px")
        print("✅ Increased maximum gaps from 16px to 20px")
        
    except FileNotFoundError:
        print(f"❌ ERROR: Could not find {file_path}")
        print("Please make sure you're in the correct directory")
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")

def update_mtgo_layout_calls():
    """
    We also need to update the MTGOLayout.tsx file to pass the area prop to CardGrid components
    """
    print("\n" + "="*60)
    print("IMPORTANT: MTGOLayout.tsx also needs updates!")
    print("="*60)
    print("\nAfter running this script, you'll need to update MTGOLayout.tsx to pass the 'area' prop:")
    print("\nFor Collection area CardGrid:")
    print("  <CardGrid ... area='collection' />")
    print("\nFor Deck area CardGrid:")
    print("  <CardGrid ... area='deck' />")
    print("\nFor Sideboard area CardGrid:")
    print("  <CardGrid ... area='sideboard' />")
    print("\nWould you like me to see the MTGOLayout.tsx file to make these updates automatically?")

if __name__ == "__main__":
    fix_magic_card_component()
    update_mtgo_layout_calls()
