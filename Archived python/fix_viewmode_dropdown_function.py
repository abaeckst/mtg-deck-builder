#!/usr/bin/env python3

import re

def fix_viewmode_dropdown_missing_function():
    """
    Add the missing isInOverflowContext function to ViewModeDropdown.tsx
    """
    
    file_path = "src/components/ViewModeDropdown.tsx"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        print(f"🔧 Adding missing isInOverflowContext function...")
        
        # Check if function already exists
        if 'isInOverflowContext' in content and 'const isInOverflowContext =' in content:
            print("✅ Function already exists, no changes needed")
            return True
        
        # Find where to insert the function - before the handleToggle function
        function_definition = '''  // Detect if dropdown is in overflow menu context
  const isInOverflowContext = () => {
    if (!buttonRef.current) return false;
    
    // Check if button is inside overflow menu
    const overflowMenu = buttonRef.current.closest('.overflow-menu');
    const overflowContainer = buttonRef.current.closest('.overflow-menu-container');
    
    return !!(overflowMenu || overflowContainer);
  };

'''
        
        # Insert before handleToggle function
        if 'const handleToggle = () =>' in content:
            content = content.replace('  const handleToggle = () =>', f'{function_definition}  const handleToggle = () =>')
            print("✅ Added function before handleToggle")
        else:
            # Fallback: insert before the return statement
            content = re.sub(
                r'(\s+)(console\.log\([^)]+\);\s*)(return)',
                rf'\1{function_definition}\2\3',
                content
            )
            print("✅ Added function before return statement")
        
        # Write the fixed content back
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        
        print(f"✅ Fixed ViewModeDropdown missing function")
        return True
        
    except Exception as e:
        print(f"❌ Error fixing ViewModeDropdown: {str(e)}")
        return False

def main():
    print("🚀 Fixing ViewModeDropdown missing function...")
    
    success = fix_viewmode_dropdown_missing_function()
    
    if success:
        print("\n✅ ViewModeDropdown function fix completed!")
        print("\n📋 Next steps:")
        print("1. Run the compilation error fix script:")
        print("   python fix_deckarea_compilation_errors.py")
        print("2. Run 'npm start' to test compilation")
        print("3. Test ViewModeDropdown functionality")
    else:
        print("\n❌ Fix failed - manual intervention needed")

if __name__ == "__main__":
    main()
