#!/usr/bin/env python3
"""
Fix quantity indicators not showing in deck/sideboard card view
This script fixes the MagicCard component to properly show quantity badges for deck cards.
"""

import os
import sys

def fix_quantity_indicators():
    """Fix quantity indicators in MagicCard component"""
    
    file_path = "src/components/MagicCard.tsx"
    
    if not os.path.exists(file_path):
        print(f"❌ Error: {file_path} not found!")
        print("Make sure you're running this script from the project root directory.")
        return False
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"📖 Reading {file_path}...")
        
        # Find and replace the quantity indicators section
        old_quantity_section = '''        {/* Quantity Indicators */}
        {showQuantity && (
          <>
            {/* Available Quantity (Collection) */}
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
              }}>
                {availableQuantity}
              </div>
            )}

            {/* Deck Quantity */}
            {quantity !== undefined && quantity > 0 && (
              <div style={{
                position: 'absolute',
                top: availableQuantity !== undefined ? '26px' : '4px',
                right: '4px',
                backgroundColor: '#ca8a04',
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
              }}>
                {quantity}
              </div>
            )}
          </>
        )}'''

        new_quantity_section = '''        {/* Quantity Indicators */}
        {showQuantity && (
          <>
            {/* Available Quantity (Collection) - Blue badge */}
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
            )}

            {/* Deck Quantity - Orange badge, always show if quantity > 0 */}
            {quantity !== undefined && quantity > 0 && (
              <div style={{
                position: 'absolute',
                top: availableQuantity !== undefined ? '26px' : '4px',
                right: '4px',
                backgroundColor: '#ea580c',
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
                boxShadow: '0 2px 4px rgba(0,0,0,0.3)',
              }}>
                {quantity}
              </div>
            )}

            {/* Force quantity display for deck cards when quantity is 1 */}
            {quantity === 1 && availableQuantity === undefined && (
              <div style={{
                position: 'absolute',
                top: '4px',
                right: '4px',
                backgroundColor: '#ea580c',
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
                boxShadow: '0 2px 4px rgba(0,0,0,0.3)',
              }}>
                1
              </div>
            )}
          </>
        )}'''
        
        if old_quantity_section in content:
            print("🔧 Fixing quantity indicators logic...")
            content = content.replace(old_quantity_section, new_quantity_section)
        else:
            print("⚠️  Warning: Could not find exact quantity indicators section to replace")
            print("The file may have been modified. Please check manually.")
            return False
        
        # Write the updated content back to the file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ Successfully updated MagicCard.tsx")
        print("🎯 Fixed quantity indicators to always show '1' badge for deck cards")
        return True
        
    except Exception as e:
        print(f"❌ Error updating {file_path}: {str(e)}")
        return False

def main():
    """Main function"""
    print("🔧 MTG Deck Builder - Fix Quantity Indicators")
    print("=" * 50)
    
    if fix_quantity_indicators():
        print("\n✅ All fixes applied successfully!")
        print("\n📋 Changes made:")
        print("   • Fixed quantity indicators to show '1' badges for deck cards")
        print("   • Enhanced styling with better z-index and shadows")
        print("   • Added explicit logic for deck cards with quantity=1")
        print("\n🚀 Next steps:")
        print("   1. Test the application with npm start")
        print("   2. Verify quantity badges appear in deck/sideboard card view")
        print("   3. Check that collection cards still show available quantities")
    else:
        print("\n❌ Fix failed! Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
