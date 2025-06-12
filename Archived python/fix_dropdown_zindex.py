#!/usr/bin/env python3
"""
Fix ViewModeDropdown z-index conflict with list view headers
Increase dropdown z-index to appear above sticky table headers.
"""

def fix_dropdown_zindex():
    """Update MTGOLayout.css to fix z-index conflict"""
    print("=== Fixing ViewModeDropdown Z-index Conflict ===")
    
    try:
        # Read current MTGOLayout.css
        with open("src/components/MTGOLayout.css", "r", encoding="utf-8") as f:
            content = f.read()
        
        # Find and replace the dropdown z-index values
        # Update z-index from 9999 to 10001 (higher than sticky headers)
        updated_content = content.replace(
            "z-index: 9999 !important;", 
            "z-index: 10001 !important;"
        )
        
        # Also update any inline z-index in ViewModeDropdown component
        if "z-index: 9999" in updated_content:
            updated_content = updated_content.replace(
                "z-index: 9999", 
                "z-index: 10001"
            )
        
        # Write the updated CSS
        with open("src/components/MTGOLayout.css", "w", encoding="utf-8") as f:
            f.write(updated_content)
        
        print("✅ Updated dropdown z-index from 9999 to 10001 in MTGOLayout.css")
        return True
        
    except Exception as e:
        print(f"❌ Error updating CSS: {e}")
        return False

def fix_component_zindex():
    """Update ViewModeDropdown component z-index"""
    print("\n=== Updating ViewModeDropdown Component Z-index ===")
    
    try:
        # Read current component
        with open("src/components/ViewModeDropdown.tsx", "r", encoding="utf-8") as f:
            content = f.read()
        
        # Replace z-index values in component
        updated_content = content.replace("zIndex: 9999", "zIndex: 10001")
        
        # Write updated component
        with open("src/components/ViewModeDropdown.tsx", "w", encoding="utf-8") as f:
            f.write(updated_content)
        
        print("✅ Updated dropdown z-index from 9999 to 10001 in ViewModeDropdown.tsx")
        return True
        
    except Exception as e:
        print(f"❌ Error updating component: {e}")
        return False

def add_additional_css_fix():
    """Add additional CSS to ensure dropdown appears above everything"""
    print("\n=== Adding Additional Z-index CSS Rules ===")
    
    additional_css = """

/* ===== DROPDOWN Z-INDEX FIX ===== */

/* Ensure ViewModeDropdown appears above sticky table headers */
.view-dropdown-menu {
  z-index: 10001 !important; /* Higher than sticky headers (z-index: 10) */
}

/* Ensure list view headers don't interfere with dropdowns */
.list-view-header-row {
  z-index: 9 !important; /* Lower than dropdown menu */
}

/* Ensure no other elements interfere */
.mtgo-layout .view-mode-dropdown {
  z-index: 10002 !important; /* Container even higher */
}

/* ===== END DROPDOWN Z-INDEX FIX ===== */
"""
    
    try:
        # Read current MTGOLayout.css
        with open("src/components/MTGOLayout.css", "r", encoding="utf-8") as f:
            current_css = f.read()
        
        # Check if fix already exists
        if "DROPDOWN Z-INDEX FIX" in current_css:
            print("✅ Z-index fix already exists in MTGOLayout.css")
            return True
        
        # Add additional CSS
        updated_css = current_css + additional_css
        
        # Write updated CSS
        with open("src/components/MTGOLayout.css", "w", encoding="utf-8") as f:
            f.write(updated_css)
        
        print("✅ Added additional z-index CSS rules to MTGOLayout.css")
        print("📋 Added rules:")
        print("   - Dropdown menu z-index: 10001 (above sticky headers)")
        print("   - List view headers z-index: 9 (below dropdown)")
        print("   - Dropdown container z-index: 10002 (highest)")
        
        return True
        
    except Exception as e:
        print(f"❌ Error adding CSS: {e}")
        return False

def main():
    """Apply all z-index fixes"""
    print("🔧 Fixing ViewModeDropdown Z-index Conflict with List View Headers")
    print("=" * 70)
    
    # Apply all fixes
    css_success = fix_dropdown_zindex()
    component_success = fix_component_zindex()
    additional_success = add_additional_css_fix()
    
    if css_success and component_success and additional_success:
        print("\n" + "=" * 70)
        print("✅ ALL Z-INDEX FIXES APPLIED SUCCESSFULLY!")
        print("\n🎯 What was fixed:")
        print("- Increased dropdown z-index from 9999 to 10001")
        print("- Reduced list view header z-index to 9")
        print("- Added comprehensive z-index hierarchy")
        print("\n💡 Z-index hierarchy now:")
        print("- Dropdown container: 10002 (highest)")
        print("- Dropdown menu: 10001") 
        print("- List view headers: 9 (lowest)")
        print("\n🧪 Test:")
        print("1. Click the View dropdown in deck area")
        print("2. Dropdown should now appear ABOVE the table headers")
        print("3. No more overlapping with QTY/NAME/MANA headers")
    else:
        print("\n❌ Some fixes failed - check error messages above")

if __name__ == "__main__":
    main()