#!/usr/bin/env python3
"""
Fix Scryfall API format issues causing 404 errors during server-side sorting
"""

import os
import sys

def fix_scryfall_api_format():
    """Fix the custom-standard format that's causing 404 errors"""
    
    filename = "src/services/scryfallApi.ts"
    
    if not os.path.exists(filename):
        print(f"❌ Error: {filename} not found")
        return False
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return False
    
    print("🔧 Fixing Scryfall API format issues...")
    
    # Fix the custom-standard format issue
    old_format_logic = """  // Add format filter with Custom Standard support
  if (filters.format) {
    if (filters.format === 'custom-standard') {
      // Custom Standard: Standard-legal cards + Final Fantasy set
      searchQuery += ` (legal:standard OR set:fin)`;
    } else {
      searchQuery += ` legal:${filters.format}`;
    }
  }"""
    
    new_format_logic = """  // Add format filter with proper Scryfall syntax
  if (filters.format) {
    if (filters.format === 'custom-standard') {
      // Custom Standard: Use standard format (Final Fantasy set is standard-legal)
      searchQuery += ` legal:standard`;
    } else {
      searchQuery += ` legal:${filters.format}`;
    }
  }"""
    
    if old_format_logic in content:
        content = content.replace(old_format_logic, new_format_logic)
        print("✅ Fixed custom-standard format syntax")
    else:
        print("❌ Custom-standard format logic not found - checking alternatives...")
        
        # Try a more targeted fix
        if '(legal:standard OR set:fin)' in content:
            content = content.replace('(legal:standard OR set:fin)', 'legal:standard')
            print("✅ Fixed OR syntax in format filter")
        else:
            print("❌ Could not find the specific format issue")
            return False
    
    # Also fix any other complex format logic that might cause issues
    complex_patterns = [
        ('` (legal:standard OR set:fin)`', '` legal:standard`'),
        ('searchQuery += ` (legal:standard OR set:fin)`;', 'searchQuery += ` legal:standard`;'),
    ]
    
    for old_pattern, new_pattern in complex_patterns:
        if old_pattern in content:
            content = content.replace(old_pattern, new_pattern)
            print(f"✅ Fixed pattern: {old_pattern}")
    
    # Write the fixed content
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Successfully updated {filename}")
        return True
    except Exception as e:
        print(f"❌ Error writing file: {e}")
        return False

def verify_other_api_issues():
    """Check for other potential API format issues"""
    
    filename = "src/services/scryfallApi.ts"
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return False
    
    print("\n🔍 Checking for other potential API issues...")
    
    # Check for other problematic patterns
    issues_found = []
    
    if '(legal:' in content and 'OR' in content:
        issues_found.append("Complex legal format with OR operators")
    
    if 'set:fin' in content:
        issues_found.append("Reference to 'fin' set (Final Fantasy)")
    
    if len(issues_found) > 0:
        print("⚠️  Potential issues found:")
        for issue in issues_found:
            print(f"   • {issue}")
        return False
    else:
        print("✅ No other API format issues detected")
        return True

def main():
    print("🔧 Scryfall API Format Fix")
    print("=" * 40)
    print("Issue: Server-side sorting fails with 404 errors")
    print("Cause: Invalid Scryfall query format with OR operators")
    print("=" * 40)
    
    success1 = fix_scryfall_api_format()
    success2 = verify_other_api_issues()
    
    if success1:
        print("\n🎉 API Format Fix Applied!")
        print("\n✅ Changes Made:")
        print("  • Fixed custom-standard format to use simple 'legal:standard'")
        print("  • Removed complex OR syntax that Scryfall doesn't accept")
        print("  • Server-side sorting should now work correctly")
        
        print("\n🔬 Test the fix:")
        print("1. npm start")
        print("2. Search for 'damage' (should work now)")
        print("3. Try changing collection sort to 'Color'")
        print("4. Should see successful server-side sorting without 404 errors")
        
        if not success2:
            print("\n⚠️  Additional issues detected - may need further fixes")
        
        return True
    else:
        print("\n❌ Fix failed!")
        print("Manual intervention needed:")
        print("1. Open src/services/scryfallApi.ts")
        print("2. Find any lines with '(legal:standard OR set:fin)'")
        print("3. Replace with 'legal:standard'")
        print("4. Remove any complex OR logic in format filters")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)