#!/usr/bin/env python3
"""
Fix missing loadedCardsCount state and useEffect
"""

import re

def fix_missing_state():
    """Add the missing loadedCardsCount state and useEffect"""
    print("🔧 Fixing missing loadedCardsCount state...")
    
    try:
        # Read the file
        with open('src/components/MTGOLayout.tsx', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if loadedCardsCount already exists
        if 'loadedCardsCount' in content:
            print("⚠️ loadedCardsCount already exists, checking if it's properly declared...")
            
            # Check if it's properly declared as state
            if 'const [loadedCardsCount, setLoadedCardsCount] = useState' in content:
                print("✅ loadedCardsCount state already properly declared")
                return True
            else:
                print("❌ loadedCardsCount exists but not as state, fixing...")
        
        # Find a good location to add the state - after other useState declarations
        # Look for the showScreenshotModal useState
        pattern = r'(const \[showScreenshotModal, setShowScreenshotModal\] = useState\(false\);)'
        
        if re.search(pattern, content):
            # Add the state after showScreenshotModal
            state_addition = r'''\1
  
  // Smart card append: track cards for smooth Load More
  const [loadedCardsCount, setLoadedCardsCount] = useState(0);'''
            
            content = re.sub(pattern, state_addition, content)
            print("✅ Added loadedCardsCount state after showScreenshotModal")
        else:
            # Fallback: look for any useState and add after it
            fallback_pattern = r'(const \[[^]]+\] = useState\([^)]+\);)(?=\s*\n\s*//|\s*\n\s*const|\s*\n\s*\})'
            
            if re.search(fallback_pattern, content):
                state_addition = r'''\1
  
  // Smart card append: track cards for smooth Load More
  const [loadedCardsCount, setLoadedCardsCount] = useState(0);'''
                
                # Only add to the first match
                content = re.sub(fallback_pattern, state_addition, content, count=1)
                print("✅ Added loadedCardsCount state (fallback location)")
            else:
                print("❌ Could not find location to add state")
                return False
        
        # Add the useEffect to sync the count
        # Find location before the return statement but after the mobile check
        effect_pattern = r'(if \(!canUseMTGO\) \{[^}]+\}\s+)(return \()'
        
        if re.search(effect_pattern, content, re.DOTALL):
            effect_addition = r'''\1
  // Sync loaded cards count for smart append
  useEffect(() => {
    if (cards.length > 0) {
      setLoadedCardsCount(cards.length);
    }
  }, [cards.length]);
  
  \2'''
            
            content = re.sub(effect_pattern, effect_addition, content, flags=re.DOTALL)
            print("✅ Added useEffect to sync loadedCardsCount")
        else:
            print("⚠️ Could not find ideal location for useEffect, adding before return")
            # Fallback: add before any return statement
            fallback_effect_pattern = r'(\s+)(return \()'
            
            if re.search(fallback_effect_pattern, content):
                effect_addition = r'''\1// Sync loaded cards count for smart append
\1useEffect(() => {
\1  if (cards.length > 0) {
\1    setLoadedCardsCount(cards.length);
\1  }
\1}, [cards.length]);
\1
\1\2'''
                
                content = re.sub(fallback_effect_pattern, effect_addition, content, count=1)
                print("✅ Added useEffect (fallback location)")
            else:
                print("❌ Could not find location to add useEffect")
                return False
        
        # Write the fixed content
        with open('src/components/MTGOLayout.tsx', 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("\n🎯 SUCCESS! Fixed missing state:")
        print("1. ✅ Added loadedCardsCount state variable")
        print("2. ✅ Added useEffect to sync with cards.length")
        print("\nThe TypeScript errors should now be resolved!")
        print("Try compiling again - Load More should work with scroll preservation!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    fix_missing_state()
