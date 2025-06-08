#!/usr/bin/env python3

import os
import sys

def add_timestamp_tracking(filename):
    """Add timestamp tracking to useSorting updateSort function"""
    
    if not os.path.exists(filename):
        print(f"Error: {filename} not found")
        return False
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the end of updateSort function and add timestamp tracking
    old_function_end = '''    console.log('🚨 ===== UPDATE SORT FUNCTION COMPLETE =====');
  }, [sortState]);'''

    new_function_end = '''    // Track sort change timing for smart sorting logic in MTGOLayout
    (window as any).lastSortChangeTime = Date.now();
    
    console.log('🚨 ===== UPDATE SORT FUNCTION COMPLETE =====');
  }, [sortState]);'''

    if old_function_end in content:
        content = content.replace(old_function_end, new_function_end)
        print("✅ Added sort change timestamp tracking to useSorting")
    else:
        print("❌ Could not find updateSort function end pattern")
        return False
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Successfully updated {filename}")
    return True

if __name__ == "__main__":
    success = add_timestamp_tracking("src/hooks/useSorting.ts")
    sys.exit(0 if success else 1)