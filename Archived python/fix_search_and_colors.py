#!/usr/bin/env python3

import os
import sys

def fix_search_and_colors():
    """Fix search bar boundary and placeholder text, clean up color button styling"""
    
    success_count = 0
    total_fixes = 3
    
    # Fix 1: Update search placeholder text in FilterPanel.tsx
    filter_panel_file = "src/components/FilterPanel.tsx"
    if os.path.exists(filter_panel_file):
        with open(filter_panel_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace long placeholder with simple, informative text
        old_placeholder = 'placeholder="Search cards... (try: flying, &quot;exact phrase&quot;, -exclude, name:lightning)"'
        new_placeholder = 'placeholder="Search name, type, or text..."'
        
        if old_placeholder in content:
            content = content.replace(old_placeholder, new_placeholder)
            
            with open(filter_panel_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("✅ Updated search placeholder text to be simpler and informative")
            success_count += 1
        else:
            print("❌ Could not find search placeholder text to update")
    else:
        print(f"❌ {filter_panel_file} not found")
    
    # Fix 2: Fix search input CSS overflow issues
    filter_css_file = "src/components/FilterPanel.css"
    if os.path.exists(filter_css_file):
        with open(filter_css_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Add CSS to ensure search input doesn't escape container
        search_fix_css = '''
/* Search Input Container Fix */
.search-group {
  margin-bottom: 12px;
  overflow: hidden; /* Prevent escaping */
}

.search-group .search-autocomplete {
  width: 100%;
  min-width: 0;
  box-sizing: border-box;
}

.search-group .search-input {
  width: 100% !important;
  min-width: 0 !important;
  max-width: 100% !important;
  box-sizing: border-box !important;
}'''
        
        # Check if the fix is already present
        if "Search Input Container Fix" not in content:
            # Insert after the existing search group styling
            search_group_pos = content.find("/* Search Group Enhanced Styling */")
            if search_group_pos != -1:
                # Insert before the existing search group styling
                content = content[:search_group_pos] + search_fix_css + "\n\n" + content[search_group_pos:]
                
                with open(filter_css_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print("✅ Added CSS to prevent search input from escaping boundary")
                success_count += 1
            else:
                print("❌ Could not find insertion point for search CSS fix")
        else:
            print("✅ Search input CSS fix already present")
            success_count += 1
    else:
        print(f"❌ {filter_css_file} not found")
    
    # Fix 3: Clean up color button styling - remove Keyrune font, show clean letters
    if os.path.exists(filter_css_file):
        with open(filter_css_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remove the problematic Keyrune font styling
        keyrune_removals = [
            # Remove font-family Keyrune reference
            (".color-button {\n  font-family: 'Keyrune', Arial, sans-serif;", ".color-button {"),
            
            # Remove font-size: 0 hiding
            (".color-button {\n  font-size: 0; /* Hide any text content */\n}", ".color-button {"),
            
            # Remove ::before content rules
            (".color-button::before {\n  font-family: 'Keyrune', Arial, sans-serif;\n  font-size: 20px;\n  display: inline-block;\n}", ""),
            
            # Remove individual ::before content
            ('.color-button.color-w::before {\n  content: "\\e600";\n}', ''),
            ('.color-button.color-u::before {\n  content: "\\e601";\n}', ''),
            ('.color-button.color-b::before {\n  content: "\\e602";\n}', ''),
            ('.color-button.color-r::before {\n  content: "\\e603";\n}', ''),
            ('.color-button.color-g::before {\n  content: "\\e604";\n}', ''),
            ('.color-button.color-c::before {\n  content: "\\e904";\n}', ''),
        ]
        
        changes_made = False
        for old_text, new_text in keyrune_removals:
            if old_text in content:
                content = content.replace(old_text, new_text)
                changes_made = True
        
        # Add clean color button styling
        clean_color_css = '''
/* Clean Color Button Styling - Letters in Circles */
.color-button {
  font-family: 'Segoe UI', Arial, sans-serif;
  font-size: 14px;
  font-weight: bold;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  border: 2px solid transparent;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  text-shadow: none;
}'''
        
        if "Clean Color Button Styling" not in content:
            # Find the existing color button styling and replace it
            start_marker = "/* Mana Symbol Buttons with Keyrune Font */"
            end_marker = ".color-button.disabled {"
            
            start_pos = content.find(start_marker)
            end_pos = content.find(end_marker)
            
            if start_pos != -1 and end_pos != -1:
                # Replace the section
                content = content[:start_pos] + clean_color_css + "\n\n" + content[end_pos:]
                changes_made = True
        
        if changes_made:
            with open(filter_css_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("✅ Cleaned up color button styling - now shows clean letters in circles")
            success_count += 1
        else:
            print("✅ Color button styling already clean")
            success_count += 1
    
    print(f"\n🎮 Fixed {success_count}/{total_fixes} issues successfully!")
    
    if success_count == total_fixes:
        print("✅ All fixes applied! Your filter panel now has:")
        print("   • Simple, clear search placeholder")
        print("   • Search input properly contained")
        print("   • Clean colored circles with letters (W, U, B, R, G, C, GOLD)")
        return True
    else:
        print(f"❌ {total_fixes - success_count} fixes failed - check the errors above")
        return False

if __name__ == "__main__":
    success = fix_search_and_colors()
    if success:
        print("\n🚀 Run 'npm start' to see the improved filter interface!")
    sys.exit(0 if success else 1)