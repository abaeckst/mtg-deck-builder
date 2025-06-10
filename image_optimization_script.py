#!/usr/bin/env python3
"""
Image Loading Performance Optimization Script
- Reduces Scryfall image size requests (faster loading)
- Implements progressive/lazy loading with Intersection Observer
- Maintains visual quality through CSS scaling
"""

import os
import re

def update_card_types():
    """Update card.ts to consistently use normal Scryfall image sizes"""
    card_types_path = "src/types/card.ts"
    
    print(f"📝 Updating {card_types_path}...")
    
    with open(card_types_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the getCardImageUri function and update it
    updated_content = re.sub(
        r'export const getCardImageUri = \(card: ScryfallCard, size: \'small\' \| \'normal\' \| \'large\' = \'normal\'\): string => \{[^}]+\};',
        '''export const getCardImageUri = (card: ScryfallCard, size: 'small' | 'normal' | 'large' = 'normal'): string => {
  // CONSISTENCY OPTIMIZATION: Always use 'normal' Scryfall images for consistent quality
  // This provides good quality at reasonable file sizes (~150KB vs ~20KB small or ~400KB large)
  
  if (!card.image_uris) {
    return '';
  }
  
  // Always use 'normal' Scryfall images for consistent quality across all card sizes
  // Visual size is still controlled by CSS, but we get better quality for scaling
  return card.image_uris.normal || card.image_uris.large || card.image_uris.small || '';
};''',
        content,
        flags=re.DOTALL
    )
    
    with open(card_types_path, 'w', encoding='utf-8') as f:
        f.write(updated_content)
    
    print("✅ Updated card.ts to consistently use normal image sizes")

def create_lazy_image_component():
    """Create a new LazyImage component with Intersection Observer"""
    component_path = "src/components/LazyImage.tsx"
    
    print(f"📝 Creating {component_path}...")
    
    lazy_image_content = '''// src/components/LazyImage.tsx - Progressive/Lazy Image Loading Component
import React, { useState, useRef, useEffect, useCallback } from 'react';

interface LazyImageProps {
  src: string;
  alt: string;
  style?: React.CSSProperties;
  onLoad?: () => void;
  onError?: () => void;
  className?: string;
  threshold?: number;
  rootMargin?: string;
}

/**
 * Lazy loading image component using Intersection Observer
 * Only loads images when they're about to become visible
 */
export const LazyImage: React.FC<LazyImageProps> = ({
  src,
  alt,
  style,
  onLoad,
  onError,
  className = '',
  threshold = 0.1,
  rootMargin = '50px',
}) => {
  const [isLoaded, setIsLoaded] = useState(false);
  const [isError, setIsError] = useState(false);
  const [shouldLoad, setShouldLoad] = useState(false);
  const imgRef = useRef<HTMLImageElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);

  // Intersection Observer to detect when image should start loading
  useEffect(() => {
    const container = containerRef.current;
    if (!container || shouldLoad) return;

    const observer = new IntersectionObserver(
      (entries) => {
        const [entry] = entries;
        if (entry.isIntersecting) {
          console.log('🖼️ Image entering viewport, starting load:', alt);
          setShouldLoad(true);
          observer.unobserve(container);
        }
      },
      {
        threshold,
        rootMargin,
      }
    );

    observer.observe(container);

    return () => {
      observer.unobserve(container);
    };
  }, [shouldLoad, threshold, rootMargin, alt]);

  const handleLoad = useCallback(() => {
    console.log('✅ Image loaded successfully:', alt);
    setIsLoaded(true);
    setIsError(false);
    onLoad?.();
  }, [alt, onLoad]);

  const handleError = useCallback(() => {
    console.log('❌ Image failed to load:', alt);
    setIsLoaded(false);
    setIsError(true);
    onError?.();
  }, [alt, onError]);

  return (
    <div 
      ref={containerRef}
      style={{ 
        width: '100%', 
        height: '100%', 
        position: 'relative',
        overflow: 'hidden',
        ...style
      }}
      className={className}
    >
      {shouldLoad && (
        <img
          ref={imgRef}
          src={src}
          alt={alt}
          style={{
            width: '100%',
            height: '100%',
            objectFit: 'cover',
            display: isLoaded ? 'block' : 'none',
            // PERFORMANCE: Optimize rendering for small images scaled up
            imageRendering: 'auto',
            WebkitImageRendering: 'auto',
          }}
          onLoad={handleLoad}
          onError={handleError}
        />
      )}
      
      {/* Loading placeholder */}
      {!isLoaded && !isError && (
        <div style={{
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          backgroundColor: '#2a2a2a',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          fontSize: '12px',
          color: '#888888',
        }}>
          {shouldLoad ? 'Loading...' : 'Preparing...'}
        </div>
      )}
      
      {/* Error state */}
      {isError && (
        <div style={{
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          backgroundColor: '#2a2a2a',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          fontSize: '10px',
          color: '#888888',
          textAlign: 'center',
          padding: '4px',
        }}>
          Failed to load
        </div>
      )}
    </div>
  );
};

export default LazyImage;'''
    
    with open(component_path, 'w', encoding='utf-8') as f:
        f.write(lazy_image_content)
    
    print("✅ Created LazyImage.tsx component")

def update_magic_card_component():
    """Update MagicCard.tsx to use LazyImage component"""
    magic_card_path = "src/components/MagicCard.tsx"
    
    print(f"📝 Updating {magic_card_path}...")
    
    with open(magic_card_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Add LazyImage import
    if "import LazyImage from './LazyImage';" not in content:
        content = content.replace(
            "import React, { useState, useCallback } from 'react';",
            "import React, { useState, useCallback } from 'react';\nimport LazyImage from './LazyImage';"
        )
    
    # Replace the image rendering section with LazyImage
    updated_content = re.sub(
        r'        {!imageError && imageUri \? \(\s*<img[^>]+onError=\{handleImageError\}\s*/>\s*\) : null}',
        '''        {!imageError && imageUri ? (
          <LazyImage
            src={imageUri}
            alt={card.name}
            style={{
              width: '100%',
              height: '100%',
              borderRadius: '6px',
            }}
            onLoad={handleImageLoad}
            onError={handleImageError}
            threshold={0.1}
            rootMargin="100px"
          />
        ) : null}''',
        content,
        flags=re.DOTALL
    )
    
    # Update the loading/error state to work with LazyImage
    updated_content = re.sub(
        r'        {/\* Loading/Error State \*/}\s*{.*?} : null}',
        '''        {/* Error State - LazyImage handles loading states */}
        {imageError ? (
          <div style={{
            position: 'absolute',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            backgroundColor: '#2a2a2a',
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            padding: '8px',
            textAlign: 'center',
          }}>
            <div style={{
              fontSize: sizeStyles.fontSize,
              color: '#ffffff',
              fontWeight: 'bold',
              marginBottom: '4px',
              lineHeight: '1.2',
              wordBreak: 'break-word',
            }}>
              {card.name}
            </div>
            <div style={{
              fontSize: Math.max(8, parseInt(sizeStyles.fontSize) - 2),
              color: '#888888',
              lineHeight: '1.1',
            }}>
              {card.type_line}
            </div>
            {card.mana_cost && (
              <div style={{
                fontSize: Math.max(8, parseInt(sizeStyles.fontSize) - 2),
                color: '#cccccc',
                marginTop: '2px',
              }}>
                {card.mana_cost}
              </div>
            )}
          </div>
        ) : null}''',
        content,
        flags=re.DOTALL
    )
    
    with open(magic_card_path, 'w', encoding='utf-8') as f:
        f.write(updated_content)
    
    print("✅ Updated MagicCard.tsx to use LazyImage")

def main():
    """Main execution function"""
    print("🚀 Starting Image Loading Performance Optimization...")
    print()
    
    try:
        # Step 1: Update image size optimization
        update_card_types()
        print()
        
        # Step 2: Create LazyImage component
        create_lazy_image_component()
        print()
        
        # Step 3: Update MagicCard to use LazyImage
        update_magic_card_component()
        print()
        
        print("✅ IMAGE LOADING OPTIMIZATION COMPLETE!")
        print()
        print("📊 Expected Performance Improvements:")
        print("   • Consistent image quality across all card sizes")
        print("   • Progressive loading (only visible cards load)")
        print("   • Better perceived performance")
        print("   • Reduced browser memory usage")
        print("   • Smooth loading experience with lazy loading")
        print()
        print("🧪 Testing Steps:")
        print("   1. npm start")
        print("   2. Search for cards")
        print("   3. Check browser Network tab - should see 'normal' image URLs consistently")
        print("   4. Scroll through results - images should load as they come into view")
        print("   5. Check console for lazy loading logs")
        print("   6. Test card resizing - should maintain quality at all sizes")
        
    except Exception as e:
        print(f"❌ Error during optimization: {e}")
        return False
    
    return True

if __name__ == "__main__":
    main()
