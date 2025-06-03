#!/usr/bin/env python3
"""
Fix ListView column minimum widths to allow better resizing
This script reduces the minimum column widths so users can resize them much smaller.
"""

import os
import sys

def fix_listview_columns():
    """Fix ListView column minimum widths"""
    
    file_path = "src/components/ListView.tsx"
    
    if not os.path.exists(file_path):
        print(f"❌ Error: {file_path} not found!")
        print("Make sure you're running this script from the project root directory.")
        return False
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"📖 Reading {file_path}...")
        
        # Find and replace the column definitions with much smaller minimum widths
        old_column_definitions = '''// Column definitions with minimum widths - Quantity first!
const COLUMN_DEFINITIONS: ColumnDefinition[] = [
  { id: 'quantity', title: 'Qty', minWidth: 80, sortable: false, visible: true },
  { id: 'name', title: 'Name', minWidth: 200, sortable: true, visible: true },
  { id: 'mana', title: 'Mana', minWidth: 80, sortable: true, visible: true },
  { id: 'type', title: 'Type', minWidth: 150, sortable: true, visible: true },
  { id: 'power', title: 'Power', minWidth: 60, sortable: true, visible: true },
  { id: 'toughness', title: 'Toughness', minWidth: 60, sortable: true, visible: true },
  { id: 'color', title: 'Color', minWidth: 80, sortable: true, visible: true },
  { id: 'text', title: 'Text', minWidth: 250, sortable: true, visible: true },
];'''

        new_column_definitions = '''// Column definitions with minimum widths - Much smaller for better resizing
const COLUMN_DEFINITIONS: ColumnDefinition[] = [
  { id: 'quantity', title: 'Qty', minWidth: 40, sortable: false, visible: true },
  { id: 'name', title: 'Name', minWidth: 60, sortable: true, visible: true },
  { id: 'mana', title: 'Mana', minWidth: 35, sortable: true, visible: true },
  { id: 'type', title: 'Type', minWidth: 50, sortable: true, visible: true },
  { id: 'power', title: 'Power', minWidth: 30, sortable: true, visible: true },
  { id: 'toughness', title: 'Toughness', minWidth: 30, sortable: true, visible: true },
  { id: 'color', title: 'Color', minWidth: 35, sortable: true, visible: true },
  { id: 'text', title: 'Text', minWidth: 80, sortable: true, visible: true },
];'''
        
        if old_column_definitions in content:
            print("🔧 Updating column minimum widths...")
            content = content.replace(old_column_definitions, new_column_definitions)
        else:
            print("⚠️  Warning: Could not find exact column definitions to replace")
            print("Trying alternative approach...")
            
            # Try replacing just the values
            replacements = [
                ("minWidth: 80,", "minWidth: 40,"),  # quantity
                ("minWidth: 200,", "minWidth: 60,"),  # name  
                ("minWidth: 80,", "minWidth: 35,"),   # mana (second occurrence)
                ("minWidth: 150,", "minWidth: 50,"),  # type
                ("minWidth: 60,", "minWidth: 30,"),   # power (first occurrence)
                ("minWidth: 60,", "minWidth: 30,"),   # toughness (second occurrence) 
                ("minWidth: 80,", "minWidth: 35,"),   # color (third occurrence)
                ("minWidth: 250,", "minWidth: 80,"),  # text
            ]
            
            # Update the comment as well
            content = content.replace(
                "// Column definitions with minimum widths - Quantity first!",
                "// Column definitions with minimum widths - Much smaller for better resizing"
            )
            
            # Apply replacements in order, being careful about duplicates
            # Replace each specific line pattern
            content = content.replace(
                "{ id: 'quantity', title: 'Qty', minWidth: 80, sortable: false, visible: true },",
                "{ id: 'quantity', title: 'Qty', minWidth: 40, sortable: false, visible: true },"
            )
            content = content.replace(
                "{ id: 'name', title: 'Name', minWidth: 200, sortable: true, visible: true },",
                "{ id: 'name', title: 'Name', minWidth: 60, sortable: true, visible: true },"
            )
            content = content.replace(
                "{ id: 'mana', title: 'Mana', minWidth: 80, sortable: true, visible: true },",
                "{ id: 'mana', title: 'Mana', minWidth: 35, sortable: true, visible: true },"
            )
            content = content.replace(
                "{ id: 'type', title: 'Type', minWidth: 150, sortable: true, visible: true },",
                "{ id: 'type', title: 'Type', minWidth: 50, sortable: true, visible: true },"
            )
            content = content.replace(
                "{ id: 'power', title: 'Power', minWidth: 60, sortable: true, visible: true },",
                "{ id: 'power', title: 'Power', minWidth: 30, sortable: true, visible: true },"
            )
            content = content.replace(
                "{ id: 'toughness', title: 'Toughness', minWidth: 60, sortable: true, visible: true },",
                "{ id: 'toughness', title: 'Toughness', minWidth: 30, sortable: true, visible: true },"
            )
            content = content.replace(
                "{ id: 'color', title: 'Color', minWidth: 80, sortable: true, visible: true },",
                "{ id: 'color', title: 'Color', minWidth: 35, sortable: true, visible: true },"
            )
            content = content.replace(
                "{ id: 'text', title: 'Text', minWidth: 250, sortable: true, visible: true },",
                "{ id: 'text', title: 'Text', minWidth: 80, sortable: true, visible: true },"
            )
        
        # Also update the validation in the resize function
        old_resize_validation = '''      const newWidth = Math.max(
        COLUMN_DEFINITIONS.find(col => col.id === resizing.columnId)?.minWidth || 100,
        resizing.startWidth + deltaX
      );'''
        
        new_resize_validation = '''      const newWidth = Math.max(
        COLUMN_DEFINITIONS.find(col => col.id === resizing.columnId)?.minWidth || 30,
        resizing.startWidth + deltaX
      );'''
        
        if old_resize_validation in content:
            print("🔧 Updating resize validation fallback...")
            content = content.replace(old_resize_validation, new_resize_validation)
        
        # Write the updated content back to the file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ Successfully updated ListView.tsx")
        print("🎯 Reduced minimum column widths for better user control")
        return True
        
    except Exception as e:
        print(f"❌ Error updating {file_path}: {str(e)}")
        return False

def main():
    """Main function"""
    print("🔧 MTG Deck Builder - Fix ListView Column Widths")
    print("=" * 50)
    
    if fix_listview_columns():
        print("\n✅ All fixes applied successfully!")
        print("\n📋 Changes made:")
        print("   • Quantity: 80px → 40px minimum width")
        print("   • Name: 200px → 60px minimum width")
        print("   • Mana: 80px → 35px minimum width")
        print("   • Type: 150px → 50px minimum width")
        print("   • Power: 60px → 30px minimum width")
        print("   • Toughness: 60px → 30px minimum width")
        print("   • Color: 80px → 35px minimum width")
        print("   • Text: 250px → 80px minimum width")
        print("   • Updated resize validation fallback: 100px → 30px")
        print("\n🚀 Next steps:")
        print("   1. Test the application with npm start")
        print("   2. Switch to List view in deck/sideboard areas")
        print("   3. Try resizing columns by dragging the borders")
        print("   4. Verify columns can now be resized much smaller")
    else:
        print("\n❌ Fix failed! Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
