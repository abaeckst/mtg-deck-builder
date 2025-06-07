#!/usr/bin/env python3

import os
import sys

def fix_collection_viewmode_comprehensive(filename):
    """Comprehensive fix for collection view mode defaulting to list instead of grid"""
    
    if not os.path.exists(filename):
        print(f"Error: {filename} not found")
        return False
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    fixes_applied = []
    
    # Fix 1: Ensure DEFAULT_LAYOUT has correct view mode
    old_default = """  viewModes: {
    collection: 'grid',
    deck: 'card',
    sideboard: 'card',
  },"""
    
    # Check if it's somehow set to 'list'
    wrong_default = """  viewModes: {
    collection: 'list',
    deck: 'card',
    sideboard: 'card',
  },"""
    
    if wrong_default in content:
        content = content.replace(wrong_default, old_default)
        fixes_applied.append("Fixed DEFAULT_LAYOUT collection view mode from 'list' to 'grid'")
    
    # Fix 2: Add explicit localStorage clearing for debugging
    storage_clear_code = """  // Clear problematic localStorage for collection view mode (debugging)
  useEffect(() => {
    const savedLayout = localStorage.getItem(STORAGE_KEY);
    if (savedLayout) {
      try {
        const parsed = JSON.parse(savedLayout);
        if (parsed.viewModes && parsed.viewModes.collection === 'list') {
          console.warn('Found collection view mode set to list in localStorage, forcing to grid');
          parsed.viewModes.collection = 'grid';
          localStorage.setItem(STORAGE_KEY, JSON.stringify(parsed));
          setLayout(prev => ({
            ...prev,
            viewModes: { ...prev.viewModes, collection: 'grid' }
          }));
        }
      } catch (error) {
        console.warn('Error processing saved layout:', error);
      }
    }
  }, []);"""
    
    # Insert this after the first useEffect (around line 90-100)
    if "// Load layout from localStorage on mount" in content and storage_clear_code not in content:
        insertion_point = content.find("  }, []);", content.find("// Load layout from localStorage on mount"))
        if insertion_point != -1:
            insertion_point = content.find("\n", insertion_point) + 1
            content = content[:insertion_point] + "\n" + storage_clear_code + "\n" + content[insertion_point:]
            fixes_applied.append("Added localStorage collection view mode correction")
    
    # Fix 3: Add debug logging to updateViewMode
    debug_logging = """    console.log('🔧 View mode update:', { area, mode, before: prev.viewModes[area] });"""
    
    update_viewmode_pattern = "const updateViewMode = useCallback((area: keyof LayoutState['viewModes'], mode: string) => {"
    if update_viewmode_pattern in content and debug_logging not in content:
        insertion_point = content.find("{", content.find(update_viewmode_pattern)) + 1
        content = content[:insertion_point] + "\n    " + debug_logging.strip() + content[insertion_point:]
        fixes_applied.append("Added debug logging to updateViewMode")
    
    if not fixes_applied:
        print("❌ No fixes needed or patterns not found")
        return False
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    for fix in fixes_applied:
        print(f"✅ {fix}")
    
    print(f"✅ Successfully updated {filename}")
    print("ℹ️  Additional step: You may need to clear browser localStorage manually")
    print("ℹ️  In browser console, run: localStorage.removeItem('mtg-deckbuilder-layout')")
    
    return True

def add_clear_storage_script():
    """Create a simple HTML file to clear localStorage"""
    clear_script = """<!DOCTYPE html>
<html>
<head>
    <title>Clear MTG Deck Builder Layout</title>
</head>
<body>
    <h1>Clear Layout Storage</h1>
    <button onclick="clearStorage()">Clear Saved Layout</button>
    <div id="result"></div>
    
    <script>
        function clearStorage() {
            localStorage.removeItem('mtg-deckbuilder-layout');
            document.getElementById('result').innerHTML = '<p style="color: green;">Layout storage cleared! Refresh your MTG app.</p>';
            console.log('Cleared mtg-deckbuilder-layout from localStorage');
        }
        
        // Check current storage
        const current = localStorage.getItem('mtg-deckbuilder-layout');
        if (current) {
            const parsed = JSON.parse(current);
            console.log('Current layout storage:', parsed);
            if (parsed.viewModes) {
                console.log('Current view modes:', parsed.viewModes);
            }
        }
    </script>
</body>
</html>"""
    
    with open('clear-layout.html', 'w') as f:
        f.write(clear_script)
    
    print("✅ Created clear-layout.html - open this file in browser to clear storage")

if __name__ == "__main__":
    success = fix_collection_viewmode_comprehensive("src/hooks/useLayout.ts")
    
    # Also create the storage clearing script
    add_clear_storage_script()
    
    if success:
        print("\n🎯 NEXT STEPS:")
        print("1. The useLayout.ts file has been updated with fixes")
        print("2. Open clear-layout.html in your browser and click 'Clear Saved Layout'")
        print("3. Refresh your MTG Deck Builder application")
        print("4. The collection should now default to Card view (grid)")
    
    sys.exit(0 if success else 1)