#!/usr/bin/env python3

import os
import sys

def simple_console_test(filename):
    """Add simple console.log to MTGOLayout to verify code execution"""
    
    if not os.path.exists(filename):
        print(f"Error: {filename} not found")
        return False
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find a simple place to add a console log - at the start of the component
    old_component_start = '''const MTGOLayout: React.FC<MTGOLayoutProps> = () => {
  const { layout, updatePanelDimensions, updateDeckAreaHeightByPixels, updateViewMode, constraints } = useLayout();'''

    new_component_start = '''const MTGOLayout: React.FC<MTGOLayoutProps> = () => {
  console.log('🟢 MTGO LAYOUT COMPONENT EXECUTING - START');
  
  const { layout, updatePanelDimensions, updateDeckAreaHeightByPixels, updateViewMode, constraints } = useLayout();'''

    if old_component_start in content:
        content = content.replace(old_component_start, new_component_start)
        print("✅ Added simple console.log to component start")
    else:
        print("❌ Could not find component start")
        return False

    # Also add console log at useSorting call location
    # Look for the existing diagnostic code we added or the original line
    if 'console.log(\'🟡 MTGO LAYOUT: About to call useSorting hook\');' in content:
        # Our diagnostic is already there, add a simpler one before it
        old_diagnostic = '''  console.log('🟡 MTGO LAYOUT: About to call useSorting hook');'''
        new_diagnostic = '''  console.log('🟢 MTGO LAYOUT: Reached useSorting section');
  console.log('🟡 MTGO LAYOUT: About to call useSorting hook');'''
        
        content = content.replace(old_diagnostic, new_diagnostic)
        print("✅ Added additional console.log before useSorting call")
    else:
        print("ℹ️  Previous diagnostic not found, code may have compilation issues")

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Successfully added simple diagnostics to {filename}")
    return True

if __name__ == "__main__":
    success = simple_console_test("src/components/MTGOLayout.tsx")
    sys.exit(0 if success else 1)
