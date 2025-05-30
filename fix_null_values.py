#!/usr/bin/env python3
"""
Fix the null values being added to search queries in scryfallApi.ts
The problem is checking for undefined but not null
"""

import os

def fix_null_filter_values():
    """Fix the null value checks in searchCardsWithFilters"""
    file_path = "src/services/scryfallApi.ts"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Fix CMC filter checks
        fixes = [
            # CMC filters
            ('if (filters.cmc.min !== undefined) {', 'if (filters.cmc.min !== undefined && filters.cmc.min !== null) {'),
            ('if (filters.cmc.max !== undefined) {', 'if (filters.cmc.max !== undefined && filters.cmc.max !== null) {'),
            
            # Power filters  
            ('if (filters.power.min !== undefined) {', 'if (filters.power.min !== undefined && filters.power.min !== null) {'),
            ('if (filters.power.max !== undefined) {', 'if (filters.power.max !== undefined && filters.power.max !== null) {'),
            
            # Toughness filters
            ('if (filters.toughness.min !== undefined) {', 'if (filters.toughness.min !== undefined && filters.toughness.min !== null) {'),
            ('if (filters.toughness.max !== undefined) {', 'if (filters.toughness.max !== undefined && filters.toughness.max !== null) {'),
        ]
        
        changes_made = 0
        for find_text, replace_text in fixes:
            if find_text in content:
                content = content.replace(find_text, replace_text)
                changes_made += 1
                print(f"✅ Fixed: {find_text}")
            else:
                print(f"❌ Not found: {find_text}")
        
        if changes_made > 0:
            # Write the updated content
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Fixed {changes_made} null value checks in scryfallApi.ts")
            return True
        else:
            print("❌ No fixes applied")
            return False
        
    except Exception as e:
        print(f"❌ Error fixing null values: {e}")
        return False

def main():
    """Run the null value fix"""
    print("🔧 Fixing null values in search filters")
    print("=" * 45)
    
    if not os.path.exists("src/services/scryfallApi.ts"):
        print("❌ Error: scryfallApi.ts not found")
        return False
    
    if fix_null_filter_values():
        print("=" * 45)
        print("🎉 Search should now work correctly!")
        print("\\nThe problem was:")
        print("• Filter values of 'null' were being added to queries")
        print("• Scryfall API doesn't understand 'cmc>=null'")
        print("• This caused 404 errors for any search")
        print("\\n🔧 Now try searching for 'lightning' again!")
    else:
        print("❌ Fix failed. Please check the error above.")
    
    return True

if __name__ == "__main__":
    main()