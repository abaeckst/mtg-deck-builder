#!/usr/bin/env python3
"""
Fix Device Detection Logic - Critical CSS Validation Blocker
Fixes DeviceCapabilities.canUseAdvancedInterface() returning false on desktop
"""

import os
import shutil
from datetime import datetime

def fix_device_detection():
    """Fix device detection logic that's incorrectly blocking desktop access"""
    
    # Define file paths
    device_detection_path = os.path.join('src', 'utils', 'deviceDetection.ts')
    backup_path = f"{device_detection_path}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    # Check if file exists
    if not os.path.exists(device_detection_path):
        print(f"❌ ERROR: {device_detection_path} not found!")
        return False
    
    # Create backup
    shutil.copy2(device_detection_path, backup_path)
    print(f"✅ Backup created: {backup_path}")
    
    # Read current file
    with open(device_detection_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix the mouse support detection logic
    # The issue is that window.matchMedia('(hover: hover) and (pointer: fine)') 
    # returns false on some desktop systems
    
    old_mouse_support = """  // Mouse support detection (some devices have both)
  const hasMouseSupport = window.matchMedia('(hover: hover) and (pointer: fine)').matches;"""
    
    new_mouse_support = """  // Mouse support detection (some devices have both)
  // Enhanced detection: check multiple indicators for mouse support
  const hasMouseSupport = window.matchMedia('(hover: hover) and (pointer: fine)').matches ||
    (!isMobile && !isTablet && window.innerWidth >= 1024);"""
    
    # Replace the mouse support detection
    if old_mouse_support in content:
        content = content.replace(old_mouse_support, new_mouse_support)
        print("✅ Fixed mouse support detection logic")
    else:
        print("⚠️  Mouse support detection pattern not found - checking alternative patterns")
    
    # Also improve the canUseAdvancedInterface logic to be more robust
    old_advanced_interface = """  canUseAdvancedInterface: (): boolean => {
    const device = getDeviceInfo();
    return device.supportsContextMenu && device.supportsDragAndDrop && device.screenSize !== 'small';
  },"""
    
    new_advanced_interface = """  canUseAdvancedInterface: (): boolean => {
    const device = getDeviceInfo();
    // Enhanced logic: Desktop systems with reasonable screen size should work
    const isDesktopSize = device.screenSize !== 'small' && window.innerWidth >= 1024;
    const isNotMobile = !device.isMobile;
    const hasBasicCapabilities = device.supportsDragAndDrop;
    
    return isDesktopSize && isNotMobile && hasBasicCapabilities;
  },"""
    
    # Replace the advanced interface check
    if old_advanced_interface in content:
        content = content.replace(old_advanced_interface, new_advanced_interface)
        print("✅ Fixed canUseAdvancedInterface logic")
    else:
        print("⚠️  Advanced interface pattern not found - manual fix may be needed")
    
    # Write the fixed content
    with open(device_detection_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Fixed device detection logic in {device_detection_path}")
    print("✅ Desktop systems should now properly detect advanced interface support")
    
    # Provide testing instructions
    print("\n📋 Testing Instructions:")
    print("1. Start the application: npm start")
    print("2. Verify no 'Desktop Required' warning appears")
    print("3. Test Phase 2 CSS functionality:")
    print("   - Drag and drop interactions")
    print("   - Panel resizing")
    print("   - UI component styling")
    
    return True

def verify_fix():
    """Verify the fix was applied correctly"""
    device_detection_path = os.path.join('src', 'utils', 'deviceDetection.ts')
    
    if not os.path.exists(device_detection_path):
        print("❌ Device detection file not found!")
        return False
    
    with open(device_detection_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if the fixes are present
    has_enhanced_mouse = "window.innerWidth >= 1024" in content
    has_enhanced_interface = "isDesktopSize && isNotMobile && hasBasicCapabilities" in content
    
    print(f"✅ Enhanced mouse detection: {'✓' if has_enhanced_mouse else '✗'}")
    print(f"✅ Enhanced interface detection: {'✓' if has_enhanced_interface else '✗'}")
    
    return has_enhanced_mouse and has_enhanced_interface

if __name__ == "__main__":
    print("🔧 Fixing Device Detection Logic...")
    print("📋 Issue: DeviceCapabilities.canUseAdvancedInterface() returning false on desktop")
    print("🎯 Goal: Enable CSS Phase 2 validation testing")
    
    if fix_device_detection():
        print("\n✅ Device detection fix applied successfully!")
        if verify_fix():
            print("✅ Fix verification passed!")
        else:
            print("⚠️  Fix verification failed - manual review needed")
    else:
        print("\n❌ Device detection fix failed!")
