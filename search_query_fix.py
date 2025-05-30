#!/usr/bin/env python3
"""
Fix Search Query Building Issues
Fixes color identity syntax and enhanced search query building
"""

import re
import os

def fix_search_issues():
    file_path = "src/services/scryfallApi.ts"
    
    if not os.path.exists(file_path):
        print(f"❌ ERROR: File {file_path} not found!")
        return False
    
    print(f"🔧 Reading {file_path}...")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        print("🔧 Applying fixes...")
        
        # Fix 1: Color identity syntax - change 'id' to 'identity'
        print("🎨 Fix 1: Correcting color identity syntax...")
        
        # Replace all instances of id= with identity=
        content = content.replace(' id=C', ' identity=C')
        content = content.replace(' id=${colorQuery}', ' identity=${colorQuery}')
        content = content.replace(' id<=${colorQuery}', ' identity<=${colorQuery}')
        content = content.replace(' id:${colorQuery}', ' identity:${colorQuery}')
        content = content.replace(' (id=C OR id=${otherColors})', ' (identity=C OR identity=${otherColors})')
        content = content.replace(' id<=${otherColors}C', ' identity<=${otherColors}C')
        content = content.replace(' (id:C OR id:${otherColors})', ' (identity:C OR identity:${otherColors})')
        
        print("✅ Fixed color identity syntax to use 'identity' instead of 'id'")
        
        # Fix 2: Enhanced search query building - fix the full-text search logic
        print("🔍 Fix 2: Fixing enhanced search query building...")
        
        old_enhanced_function = '''function buildEnhancedSearchQuery(query: string): string {
  // For simple queries without operators, enable full-text search
  // This searches across name, oracle text, and type line
  if (!query.includes('"') && !query.includes('-') && !query.includes(':')) {
    return `(name:"${query}" OR oracle:"${query}" OR type:"${query}")`;
  }'''
        
        new_enhanced_function = '''function buildEnhancedSearchQuery(query: string): string {
  // For simple queries without operators, enable full-text search
  // This searches across name, oracle text, and type line
  if (!query.includes('"') && !query.includes('-') && !query.includes(':')) {
    return `(name:${query} OR oracle:${query} OR type:${query})`;
  }'''
        
        if old_enhanced_function in content:
            content = content.replace(old_enhanced_function, new_enhanced_function)
            print("✅ Fixed enhanced search to remove problematic quotes")
        else:
            print("⚠️  Could not find exact enhanced search pattern, trying alternative...")
            # Try to fix just the problematic line
            content = content.replace(
                'return `(name:"${query}" OR oracle:"${query}" OR type:"${query}")`;',
                'return `(name:${query} OR oracle:${query} OR type:${query})`;'
            )
            print("✅ Applied alternative fix for enhanced search")
        
        # Fix 3: Also fix the full-text search in the remaining terms section
        old_fulltext = '''parts.push(`(name:"${fullTextSearch}" OR oracle:"${fullTextSearch}" OR type:"${fullTextSearch}")`);'''
        new_fulltext = '''parts.push(`(name:${fullTextSearch} OR oracle:${fullTextSearch} OR type:${fullTextSearch})`);'''
        
        if old_fulltext in content:
            content = content.replace(old_fulltext, new_fulltext)
            print("✅ Fixed full-text search in remaining terms")
        
        # Fix 4: Make sure custom-standard format query is correctly formatted
        print("🏛️ Fix 3: Ensuring custom-standard format query is correct...")
        
        old_custom_standard = '''      searchQuery += ` (legal:standard OR set:FIN)`;'''
        new_custom_standard = '''      searchQuery += ` (legal:standard OR set:fin)`;'''
        
        if old_custom_standard in content:
            content = content.replace(old_custom_standard, new_custom_standard)
            print("✅ Fixed custom-standard to use lowercase 'fin'")
        
        # Write the updated content back to file
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        
        print(f"\n✅ SUCCESS: All search fixes applied to {file_path}")
        print("\n🧪 Test these scenarios:")
        print("   1. Type 'lightning' in search - should return Lightning Bolt, etc.")
        print("   2. Select Red (R) color filter - should return red cards")
        print("   3. Try 'Custom Standard' format - should include standard + final fantasy")
        print("   4. Try combined search + filter - should work together")
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR: Failed to process {file_path}: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 MTG Deck Builder - Fix Search Query Building Issues")
    print("=" * 60)
    print("This script fixes the search and filter query building problems.\n")
    
    success = fix_search_issues()
    
    if success:
        print("\n🎉 Search fixes completed successfully!")
        print("📋 Next steps:")
        print("   1. Run 'npm start' to test the fixes")
        print("   2. Try searching for 'lightning' - should work now")
        print("   3. Try color filters - should return results now")
        print("   4. Test all filter combinations")
    else:
        print("\n❌ Search fixes failed. Please check the error messages above.")
