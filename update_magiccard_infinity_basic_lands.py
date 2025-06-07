#!/usr/bin/env python3

import os
import sys

def update_magiccard_infinity_basic_lands(filename):
    """Update MagicCard.tsx to show infinity symbol for basic lands in collection area"""
    
    if not os.path.exists(filename):
        print(f"Error: {filename} not found")
        return False
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Make replacements with exact string matching
    updates = [
        # Add isBasicLand import
        (
            "import { ScryfallCard, DeckCard, getCardImageUri } from '../types/card';",
            "import { ScryfallCard, DeckCard, getCardImageUri, isBasicLand } from '../types/card';",
            "Added isBasicLand import"
        ),
        
        # Replace availableQuantity display logic to show infinity for basic lands
        (
            """            {/* Available Quantity (Collection) - Blue badge */}
            {availableQuantity !== undefined && (
              <div style={{
                position: 'absolute',
                top: '4px',
                right: '4px',
                backgroundColor: '#1e40af',
                color: 'white',
                borderRadius: '50%',
                width: size === 'small' ? '16px' : '20px',
                height: size === 'small' ? '16px' : '20px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontSize: size === 'small' ? '10px' : '12px',
                fontWeight: 'bold',
                border: '1px solid rgba(255,255,255,0.3)',
                zIndex: 10,
              }}>
                {availableQuantity}
              </div>
            )}""",
            """            {/* Available Quantity (Collection) - Blue badge */}
            {availableQuantity !== undefined && (
              <div style={{
                position: 'absolute',
                top: '4px',
                right: '4px',
                backgroundColor: '#1e40af',
                color: 'white',
                borderRadius: '50%',
                width: size === 'small' ? '16px' : '20px',
                height: size === 'small' ? '16px' : '20px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontSize: size === 'small' ? '10px' : '12px',
                fontWeight: 'bold',
                border: '1px solid rgba(255,255,255,0.3)',
                zIndex: 10,
              }}>
                {isBasicLand(card) ? '∞' : availableQuantity}
              </div>
            )}""",
            "Updated collection quantity display to show infinity symbol for basic lands"
        )
    ]
    
    for old_str, new_str, desc in updates:
        if old_str in content:
            content = content.replace(old_str, new_str)
            print(f"✅ {desc}")
        else:
            print(f"❌ Could not find: {desc}")
            return False
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Successfully updated {filename}")
    return True

if __name__ == "__main__":
    success = update_magiccard_infinity_basic_lands("src/components/MagicCard.tsx")
    sys.exit(0 if success else 1)