// src/utils/deviceDetection.ts
import { useState, useEffect, useCallback, useRef } from 'react';

export interface DeviceInfo {
  isMobile: boolean;
  isTablet: boolean;
  isDesktop: boolean;
  isTouchDevice: boolean;
  hasMouseSupport: boolean;
  supportsContextMenu: boolean;
  supportsDragAndDrop: boolean;
  screenSize: 'small' | 'medium' | 'large' | 'xlarge';
  orientation: 'portrait' | 'landscape';
}

/**
 * Throttle function to limit how often a function can be called
 */
const throttle = (func: (...args: any[]) => void, delay: number) => {
  let timeoutId: NodeJS.Timeout | null = null;
  let lastExecTime = 0;
  
  return (...args: any[]) => {
    const currentTime = Date.now();
    
    if (currentTime - lastExecTime > delay) {
      func(...args);
      lastExecTime = currentTime;
    } else {
      if (timeoutId) {
        clearTimeout(timeoutId);
      }
      timeoutId = setTimeout(() => {
        func(...args);
        lastExecTime = Date.now();
      }, delay - (currentTime - lastExecTime));
    }
  };
};

/**
 * Detect if the device is mobile based on user agent and screen size
 */
export const isMobileDevice = (): boolean => {
  // Check user agent for mobile indicators - using string methods instead of regex
  const userAgent = navigator.userAgent.toLowerCase();
  const mobileKeywords = ['android', 'webos', 'iphone', 'ipad', 'ipod', 'blackberry', 'iemobile', 'opera mini'];
  const hasMobileKeyword = mobileKeywords.some(keyword => userAgent.includes(keyword));
  
  // Check screen size (mobile typically < 768px width)
  const isSmallScreen = window.innerWidth < 768;
  
  // Check for touch events support
  const isTouchDevice = 'ontouchstart' in window || navigator.maxTouchPoints > 0;
  
  return hasMobileKeyword || (isSmallScreen && isTouchDevice);
};

/**
 * Detect if the device is a tablet
 */
export const isTabletDevice = (): boolean => {
  const userAgent = navigator.userAgent.toLowerCase();
  const hasIpad = userAgent.includes('ipad');
  const hasTablet = userAgent.includes('tablet');
  const hasAndroidNoMobile = userAgent.includes('android') && !userAgent.includes('mobile');
  
  // Screen size check for tablets (768px - 1024px)
  const isTabletSize = window.innerWidth >= 768 && window.innerWidth <= 1024;
  
  return hasIpad || hasTablet || hasAndroidNoMobile || isTabletSize;
};

/**
 * Enhanced mouse support detection with fallbacks
 */
const detectMouseSupport = (): boolean => {
  // Primary detection: CSS media query
  try {
    if (window.matchMedia && window.matchMedia('(hover: hover) and (pointer: fine)').matches) {
      return true;
    }
  } catch (e) {
    // Fallback if matchMedia fails
  }
  
  // Fallback 1: Check for non-touch desktop indicators
  const userAgent = navigator.userAgent.toLowerCase();
  const desktopKeywords = ['windows nt', 'macintosh', 'x11'];
  const hasDesktopKeyword = desktopKeywords.some(keyword => userAgent.includes(keyword));
  
  // Fallback 2: Screen size and touch combination
  const isLargeScreen = window.innerWidth >= 1024;
  const hasLimitedTouch = navigator.maxTouchPoints <= 1;
  
  // Fallback 3: Assume mouse support for non-mobile devices with large screens
  const isMobile = isMobileDevice();
  
  return hasDesktopKeyword || ((isLargeScreen && hasLimitedTouch) || (!isMobile && window.innerWidth >= 768));
};

/**
 * Get comprehensive device information
 */
export const getDeviceInfo = (): DeviceInfo => {
  const isMobile = isMobileDevice();
  const isTablet = isTabletDevice();
  const isDesktop = !isMobile && !isTablet;
  
  // Touch support detection
  const isTouchDevice = 'ontouchstart' in window || 
    navigator.maxTouchPoints > 0 || 
    ((window as any).DocumentTouch && document instanceof (window as any).DocumentTouch);
  
  // Enhanced mouse support detection
  const hasMouseSupport = detectMouseSupport();
  
  // Context menu support (right-click) - be more permissive for desktop
  const supportsContextMenu = hasMouseSupport || (isDesktop && window.innerWidth >= 768);
  
  // Drag and drop support - be more permissive
  const supportsDragAndDrop = ('draggable' in document.createElement('div')) && 
    (hasMouseSupport || isDesktop || window.innerWidth >= 768);
  
  // Screen size categories
  let screenSize: DeviceInfo['screenSize'];
  const width = window.innerWidth;
  if (width < 640) {
    screenSize = 'small';
  } else if (width < 1024) {
    screenSize = 'medium';
  } else if (width < 1280) {
    screenSize = 'large';
  } else {
    screenSize = 'xlarge';
  }
  
  // Orientation
  const orientation: DeviceInfo['orientation'] = window.innerHeight > window.innerWidth ? 'portrait' : 'landscape';
  
  return {
    isMobile,
    isTablet,
    isDesktop,
    isTouchDevice,
    hasMouseSupport,
    supportsContextMenu,
    supportsDragAndDrop,
    screenSize,
    orientation,
  };
};

/**
 * Hook for reactive device detection with throttled updates
 */
export const useDeviceDetection = () => {
  const [deviceInfo, setDeviceInfo] = useState<DeviceInfo>(() => getDeviceInfo());
  const throttledUpdateRef = useRef<((...args: any[]) => void) | null>(null);
  
  // Create throttled update function
  const createThrottledUpdate = useCallback(() => {
    return throttle(() => {
      const newDeviceInfo = getDeviceInfo();
      setDeviceInfo(prevInfo => {
        // Only update if something actually changed to prevent unnecessary re-renders
        const hasChanged = (
          prevInfo.screenSize !== newDeviceInfo.screenSize ||
          prevInfo.orientation !== newDeviceInfo.orientation ||
          prevInfo.isMobile !== newDeviceInfo.isMobile ||
          prevInfo.isTablet !== newDeviceInfo.isTablet ||
          prevInfo.isDesktop !== newDeviceInfo.isDesktop
        );
        
        return hasChanged ? newDeviceInfo : prevInfo;
      });
    }, 250); // Throttle to max 4 updates per second
  }, []);
  
  useEffect(() => {
    throttledUpdateRef.current = createThrottledUpdate();
    
    const handleResize = () => {
      if (throttledUpdateRef.current) {
        throttledUpdateRef.current();
      }
    };
    
    const handleOrientationChange = () => {
      // Small delay to allow orientation change to complete, then throttled update
      setTimeout(() => {
        if (throttledUpdateRef.current) {
          throttledUpdateRef.current();
        }
      }, 100);
    };
    
    window.addEventListener('resize', handleResize);
    window.addEventListener('orientationchange', handleOrientationChange);
    
    return () => {
      window.removeEventListener('resize', handleResize);
      window.removeEventListener('orientationchange', handleOrientationChange);
    };
  }, [createThrottledUpdate]);
  
  return deviceInfo;
};

// Cached device info to avoid repeated calculations during resize operations
let cachedDeviceInfo: DeviceInfo | null = null;
let lastCacheTime = 0;
const CACHE_DURATION = 200; // Cache for 200ms

/**
 * Get cached device info to avoid repeated calculations
 */
const getCachedDeviceInfo = (): DeviceInfo => {
  const now = Date.now();
  
  if (!cachedDeviceInfo || (now - lastCacheTime) > CACHE_DURATION) {
    cachedDeviceInfo = getDeviceInfo();
    lastCacheTime = now;
  }
  
  return cachedDeviceInfo;
};

/**
 * Utility functions for feature detection - Now using cached device info
 */
export const DeviceCapabilities = {
  // Check if device supports specific features needed for MTGO interface
  canUseAdvancedInterface: (): boolean => {
    const device = getCachedDeviceInfo(); // Use cached version instead of getDeviceInfo()
    
    // Only log in development and throttle the logging
    if (process.env.NODE_ENV === 'development') {
      const now = Date.now();
      if (!DeviceCapabilities._lastLogTime || (now - DeviceCapabilities._lastLogTime) > 1000) {
        console.log('Device Detection Debug:', {
          supportsContextMenu: device.supportsContextMenu,
          supportsDragAndDrop: device.supportsDragAndDrop,
          screenSize: device.screenSize,
          isDesktop: device.isDesktop,
          hasMouseSupport: device.hasMouseSupport,
          windowWidth: window.innerWidth
        });
        DeviceCapabilities._lastLogTime = now;
      }
    }
    
    // More permissive check - allow if it's a desktop OR has the necessary features
    return device.isDesktop || 
           (device.supportsContextMenu && device.supportsDragAndDrop && device.screenSize !== 'small');
  },
  
  // Check if device should show simplified interface
  shouldShowSimplifiedInterface: (): boolean => {
    const device = getCachedDeviceInfo();
    return device.isMobile || device.screenSize === 'small';
  },
  
  // Check if device should show mobile warning
  shouldShowMobileWarning: (): boolean => {
    const device = getCachedDeviceInfo();
    return device.isMobile || (!device.supportsContextMenu && !device.supportsDragAndDrop);
  },
  
  // Get recommended interaction mode
  getRecommendedInteractionMode: (): 'desktop' | 'touch' | 'hybrid' => {
    const device = getCachedDeviceInfo();
    
    if (device.isDesktop && device.hasMouseSupport && !device.isTouchDevice) {
      return 'desktop';
    } else if (device.isMobile || (device.isTouchDevice && !device.hasMouseSupport)) {
      return 'touch';
    } else {
      return 'hybrid';
    }
  },
  
  // Internal property for tracking last log time
  _lastLogTime: 0 as number,
};