#!/usr/bin/env python3
"""
Fix Multi-Word Search Logic in scryfallApi.ts
Changes from exact phrase search to individual word AND search
"""

import os

def fix_multiword_search():
    file_path = "src/services/scryfallApi.ts"
    
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return False
    
    # Read the current file
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("🔧 Fixing multi-word search logic...")
    
    # Fix: Change from exact phrase to individual word search
    old_logic = '''      // Multi-word query: Use oracle text search with proper Scryfall syntax
      console.log('🔍 Multi-word query detected, using oracle text syntax:', query);
      return `o:"${query}";'''
    
    new_logic = '''      // Multi-word query: Search for individual words with AND logic
      console.log('🔍 Multi-word query detected, using individual word search:', query);
      const words = query.trim().split(/\\s+/);
      const oracleTerms = words.map(word => `o:${word}`).join(' ');
      return oracleTerms;'''
    
    if old_logic in content:
        content = content.replace(old_logic, new_logic)
        print("✅ Fixed multi-word search logic: exact phrase → individual words")
        
        # Write the updated content back
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Successfully updated {file_path}")
        return True
    else:
        print("❌ Could not find the multi-word search logic to replace")
        print("📍 Looking for alternative patterns...")
        
        # Check if the function exists
        if 'Multi-word query detected' in content:
            print("✅ Found multi-word detection, but pattern doesn't match exactly")
            print("🔧 Manual fix needed:")
            print("1. Open src/services/scryfallApi.ts")
            print("2. Find the multi-word query section")
            print("3. Replace the logic to split words and use individual o: terms")
        else:
            print("❌ Multi-word query detection not found")
        
        return False

def main():
    print("🔧 Fixing multi-word search logic for better Scryfall compatibility")
    print("📍 Current directory:", os.getcwd())
    print()
    
    success = fix_multiword_search()
    
    print("\n" + "="*60)
    
    if success:
        print("🎉 Multi-word search fix complete!")
        print("\nHow the search now works:")
        print("📝 'deal damage' → 'o:deal o:damage'")
        print("📝 'enters battlefield' → 'o:enters o:battlefield'")
        print("📝 'target creature' → 'o:target o:creature'")
        print("\nThis will find cards with BOTH words anywhere in the oracle text,")
        print("so 'deal 3 damage', 'deal damage equal to', etc. will all match!")
        
        print("\nNext steps:")
        print("1. Run 'npm start' to test")
        print("2. Search 'deal damage' - should find Lightning Bolt, Shock, etc.")
        print("3. Search 'enters battlefield' - should find ETB cards")
        print("4. Verify single words like 'lightning' still work")
        
        print("\nExpected results:")
        print("✅ Lightning Bolt (deal 3 damage)")
        print("✅ Shock (deal 2 damage)")  
        print("✅ Cards with 'deal X damage to target'")
        print("✅ Much better search results!")
        
    else:
        print("❌ Could not apply automatic fix")
        print("\nManual fix instructions:")
        print("1. Open src/services/scryfallApi.ts")
        print("2. Find the buildEnhancedSearchQuery function")
        print("3. In the multi-word section, change:")
        print('   FROM: return `o:"${query}";')
        print("   TO: Split query into words and use individual o: terms")
        print("\nExample manual change:")
        print("const words = query.trim().split(/\\s+/);")
        print("const oracleTerms = words.map(word => `o:${word}`).join(' ');")
        print("return oracleTerms;")

if __name__ == "__main__":
    main()
