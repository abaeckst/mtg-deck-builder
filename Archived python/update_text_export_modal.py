#!/usr/bin/env python3
"""
Update TextExportModal - Remove deck info section and move copy button to top
"""

import os

def update_text_export_modal():
    """Update the TextExportModal layout"""
    
    modal_file = "src/components/TextExportModal.tsx"
    
    if not os.path.exists(modal_file):
        print(f"❌ {modal_file} not found")
        return False
    
    print("🔧 Updating TextExportModal layout...")
    
    # Read the current file
    with open(modal_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find and replace the JSX structure
    # Look for the section between the modal header and the textarea
    
    # Remove the deck information section completely
    deck_info_start = content.find('<div className="deck-info">')
    deck_info_end = content.find('</div>', deck_info_start) + 6
    
    if deck_info_start != -1 and deck_info_end != -1:
        # Remove the entire deck info section
        before_deck_info = content[:deck_info_start]
        after_deck_info = content[deck_info_end:]
        content = before_deck_info + after_deck_info
        print("  ✅ Removed deck information section")
    
    # Find the copy button section and move it to the top
    copy_button_start = content.find('<div className="copy-section">')
    copy_button_end = content.find('</div>', copy_button_start) + 6
    
    if copy_button_start != -1 and copy_button_end != -1:
        # Extract the copy button section
        copy_section = content[copy_button_start:copy_button_end]
        
        # Remove it from its current location
        before_copy = content[:copy_button_start]
        after_copy = content[copy_button_end:]
        content_without_copy = before_copy + after_copy
        
        # Find where to insert it (after the modal header)
        header_end = content_without_copy.find('</h2>') + 5
        
        if header_end > 4:  # Found the header
            # Insert the copy section right after the header
            before_header = content_without_copy[:header_end]
            after_header = content_without_copy[header_end:]
            content = before_header + '\n\n      ' + copy_section + '\n' + after_header
            print("  ✅ Moved copy button to top of modal")
        else:
            print("  ⚠️  Could not find modal header to position copy button")
            content = content_without_copy  # Keep changes but without repositioning
    
    # Write the updated content back
    with open(modal_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True

def main():
    """Main update function"""
    
    print("=== TEXT EXPORT MODAL LAYOUT UPDATE ===\n")
    
    if not os.path.exists('src'):
        print("❌ ERROR: Not in project root directory")
        return False
    
    if update_text_export_modal():
        print("\n🎉 TextExportModal layout updated!")
        print("\nChanges made:")
        print("  • Removed deck information section")
        print("  • Moved copy button to top of modal")
        print("\nNext steps:")
        print("  1. Test the updated modal layout")
        print("  2. Verify copy functionality still works")
    else:
        print("\n⚠️  Update not completed - check file manually")
    
    return True

if __name__ == "__main__":
    main()