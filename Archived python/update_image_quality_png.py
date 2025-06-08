#!/usr/bin/env python3

import os
import sys

def update_image_quality_to_png(filename):
    """Update card.ts to use PNG format for highest quality images"""
    
    if not os.path.exists(filename):
        print(f"Error: {filename} not found")
        return False
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find and replace the getCardImageUri function to use PNG format
    old_function = '''/**
 * Utility function to get the appropriate image URI from a Scryfall card
 */
export const getCardImageUri = (card: ScryfallCard, size: 'small' | 'normal' | 'large' = 'normal'): string => {
  // Handle double-faced cards
  if (card.card_faces && card.card_faces.length > 0) {
    const face = card.card_faces[0];
    if (face.image_uris) {
      return face.image_uris[size];
    }
  }
  
  // Handle normal cards
  if (card.image_uris) {
    return card.image_uris[size];
  }
  
  // Fallback - this shouldn't happen with valid Scryfall data
  return '';
};'''

    new_function = '''/**
 * Utility function to get the appropriate image URI from a Scryfall card
 * Updated to use PNG format for highest quality (745×1040)
 */
export const getCardImageUri = (card: ScryfallCard, size: 'small' | 'normal' | 'large' = 'normal'): string => {
  // Handle double-faced cards
  if (card.card_faces && card.card_faces.length > 0) {
    const face = card.card_faces[0];
    if (face.image_uris) {
      // Use PNG format for highest quality, fallback to requested size
      return face.image_uris.png || face.image_uris[size];
    }
  }
  
  // Handle normal cards
  if (card.image_uris) {
    // Use PNG format for highest quality (745×1040), fallback to requested size
    return card.image_uris.png || card.image_uris[size];
  }
  
  // Fallback - this shouldn't happen with valid Scryfall data
  return '';
};'''

    if old_function in content:
        content = content.replace(old_function, new_function)
        print("✅ Updated getCardImageUri function to use PNG format for highest quality")
    else:
        print("❌ Could not find the exact getCardImageUri function to update")
        print("💡 The function may have been modified. Please check the code manually.")
        return False
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Successfully updated {filename}")
    print("🎯 Image Quality Improvement:")
    print("   • Before: 488×680 normal JPG (medium quality)")
    print("   • After: 745×1040 PNG (highest quality)")
    print("   • Result: Dramatically sharper text and artwork at all sizes")
    print("   • Fallback: Uses original size if PNG not available")
    return True

if __name__ == "__main__":
    success = update_image_quality_to_png("src/types/card.ts")
    
    if success:
        print("\n🚀 Next Steps:")
        print("1. Test the application: npm start")
        print("2. Compare image quality before/after")
        print("3. Try different card sizes with the slider")
        print("4. Your friend should see dramatically improved quality!")
        print("\n📊 Technical Details:")
        print("• PNG format: 745×1040 resolution (highest available)")
        print("• Transparent background for better overlay support")
        print("• Crisp text rendering at any scale factor")
        print("• Automatic fallback for cards without PNG format")
    
    sys.exit(0 if success else 1)
