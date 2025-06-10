// src/components/LazyImage.tsx - Progressive/Lazy Image Loading Component
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
            // PERFORMANCE: Optimize rendering for images
            imageRendering: 'auto',
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

export default LazyImage;