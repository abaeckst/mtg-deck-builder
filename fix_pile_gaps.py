#!/usr/bin/env python3
"""
Fix pile view column gaps - Final 5% of Phase 3D
Target: Ensure 6-8px gaps between pile columns
"""

import re

def fix_pile_view_gaps():
    """Fix the pile view column gap issue by updating CSS with higher specificity"""
    
    # Read the current CSS file
    try:
        with open('src/components/MTGOLayout.css', 'r', encoding='utf-8') as f:
            css_content = f.read()
            print("✅ Successfully read MTGOLayout.css")
    except FileNotFoundError:
        print("❌ Error: Could not find src/components/MTGOLayout.css")
        return False
    except Exception as e:
        print(f"❌ Error reading CSS file: {e}")
        return False

    # STEP 1: Find and fix the pile-columns-container gap issue
    # The current CSS has gap: 8px but it might be overridden or not specific enough
    
    # Look for the existing pile-columns-container rule
    pile_container_pattern = r'(\.pile-columns-container\s*\{[^}]*?)(\})'
    
    if re.search(pile_container_pattern, css_content, re.DOTALL):
        print("🔍 Found existing .pile-columns-container rule")
        
        # Replace the existing rule with a more specific and explicit one
        def replace_pile_container(match):
            # Extract the existing content but rebuild it with explicit gap
            return """.pile-columns-container {
  flex: 1;
  display: flex !important;
  overflow-x: auto;
  overflow-y: auto;
  padding: 4px;
  gap: 8px !important; /* CRITICAL: 8px breathing room between columns */
  align-items: flex-start;
  max-height: 100%;
}"""
        
        css_content = re.sub(pile_container_pattern, replace_pile_container, css_content, flags=re.DOTALL)
        print("✅ Updated .pile-columns-container with explicit gap and !important")
    else:
        print("⚠️ Warning: Could not find existing .pile-columns-container rule")
        return False

    # STEP 2: Ensure pile columns themselves don't have conflicting margins/padding
    pile_column_pattern = r'(\.pile-column\s*\{[^}]*?)(\})'
    
    if re.search(pile_column_pattern, css_content, re.DOTALL):
        print("🔍 Found existing .pile-column rule")
        
        def replace_pile_column(match):
            return """.pile-column {
  min-width: 120px;
  background-color: transparent;
  border: none;
  display: flex;
  flex-direction: column;
  flex-shrink: 0;
  height: fit-content;
  position: relative;
  margin: 0 !important; /* CRITICAL: No margin to not interfere with gap */
}"""
        
        css_content = re.sub(pile_column_pattern, replace_pile_column, css_content, flags=re.DOTALL)
        print("✅ Updated .pile-column to remove any margin conflicts")
    else:
        print("⚠️ Warning: Could not find existing .pile-column rule")

    # STEP 3: Add a backup rule with highest specificity at the end
    # This ensures the gap is applied even if there are other conflicting rules
    backup_css = """

/* PHASE 3D FINAL FIX: Pile Column Gaps - Highest Specificity */
.mtgo-layout .pile-view .pile-columns-container {
  gap: 8px !important; /* FORCE 8px gaps between columns */
}

.mtgo-layout .pile-view .pile-column {
  margin: 0 !important; /* FORCE no margins to avoid gap conflicts */
  padding: 0 !important; /* FORCE no padding on column itself */
}

/* End Phase 3D gap fix */"""
    
    # Add the backup rules at the very end of the CSS file
    css_content += backup_css
    print("✅ Added high-specificity backup gap rules")

    # Write the updated CSS back to the file
    try:
        with open('src/components/MTGOLayout.css', 'w', encoding='utf-8') as f:
            f.write(css_content)
        print("✅ Successfully wrote updated CSS file")
        return True
    except Exception as e:
        print(f"❌ Error writing CSS file: {e}")
        return False

def main():
    """Main execution function"""
    print("🚀 Starting Pile View Gap Fix - Phase 3D Final Polish")
    print("=" * 60)
    
    success = fix_pile_view_gaps()
    
    print("=" * 60)
    if success:
        print("✅ PILE VIEW GAP FIX COMPLETE!")
        print("🎯 Changes made:")
        print("   • Updated .pile-columns-container with explicit 8px gap")
        print("   • Removed margin conflicts from .pile-column")
        print("   • Added high-specificity backup rules")
        print("")
        print("🧪 Test instructions:")
        print("   1. Run: npm start")
        print("   2. Add cards to deck or sideboard")
        print("   3. Switch to 'Pile' view")
        print("   4. Verify 8px breathing room between columns")
        print("")
        print("✨ Phase 3D should now be 100% complete!")
    else:
        print("❌ Gap fix failed - manual intervention needed")
        print("🔧 Try using browser dev tools to inspect .pile-columns-container")
    
    return success

if __name__ == "__main__":
    main()
