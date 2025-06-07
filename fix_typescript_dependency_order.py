#!/usr/bin/env python3

import os
import sys

def fix_typescript_dependency_order():
    """
    Fix TypeScript dependency order issue by moving handleCollectionSortChange
    declaration BEFORE the useEffect that references it.
    """
    
    filepath = "src/hooks/useCards.ts"
    
    if not os.path.exists(filepath):
        print(f"Error: {filepath} not found")
        return False
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the useEffect subscription block that references handleCollectionSortChange
    subscription_useeffect_start = content.find("// Subscribe to collection sort changes with enhanced debugging")
    if subscription_useeffect_start == -1:
        print("❌ Could not find subscription useEffect block")
        return False
    
    # Find the end of this useEffect
    subscription_useeffect_end = content.find("}, [subscribe, unsubscribe, state.lastSearchMetadata, handleCollectionSortChange]);", subscription_useeffect_start)
    if subscription_useeffect_end == -1:
        print("❌ Could not find end of subscription useEffect block")
        return False
    
    subscription_useeffect_end = content.find("];", subscription_useeffect_end) + 2
    
    # Find the handleCollectionSortChange function declaration
    handle_function_start = content.find("// Handle collection sort changes - ENHANCED DEBUGGING AND SMART LOGIC")
    if handle_function_start == -1:
        print("❌ Could not find handleCollectionSortChange function")
        return False
    
    # Find the end of handleCollectionSortChange function
    handle_function_end = content.find("}, [state.lastSearchMetadata, getScryfallSortParams, searchWithPagination]);", handle_function_start)
    if handle_function_end == -1:
        print("❌ Could not find end of handleCollectionSortChange function")
        return False
    
    handle_function_end = content.find("];", handle_function_end) + 2
    
    # Extract the blocks
    subscription_block = content[subscription_useeffect_start:subscription_useeffect_end + 1]
    handle_function_block = content[handle_function_start:handle_function_end + 1]
    
    # Remove both blocks from their current positions
    content_without_blocks = (
        content[:subscription_useeffect_start] + 
        content[subscription_useeffect_end + 1:handle_function_start] + 
        content[handle_function_end + 1:]
    )
    
    # Find where to insert them - after searchWithPagination function but before other useEffect hooks
    # Look for the end of searchWithPagination function
    search_with_pagination_end = content_without_blocks.find("}, [clearError, setLoading, resetPagination, getScryfallSortParams]);")
    if search_with_pagination_end == -1:
        print("❌ Could not find searchWithPagination function end")
        return False
    
    search_with_pagination_end = content_without_blocks.find("];", search_with_pagination_end) + 2
    
    # Insert handleCollectionSortChange FIRST, then the subscription useEffect
    insertion_point = search_with_pagination_end + 1
    
    new_content = (
        content_without_blocks[:insertion_point] + 
        "\n\n  " + handle_function_block.strip() + 
        "\n\n  " + subscription_block.strip() + 
        "\n" +
        content_without_blocks[insertion_point:]
    )
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("✅ Fixed TypeScript dependency order:")
    print("  1. Moved handleCollectionSortChange declaration before useEffect")
    print("  2. Preserved all enhanced debugging and functionality")
    print("  3. Maintained proper React hook ordering")
    
    return True

if __name__ == "__main__":
    success = fix_typescript_dependency_order()
    
    if success:
        print("\n🎯 TypeScript compilation should now succeed!")
        print("\n🧪 Next Steps:")
        print("1. Run: npm start")
        print("2. Verify no TypeScript errors")
        print("3. Test smart sorting functionality")
        print("4. Watch browser console for comprehensive sort debugging")
    else:
        print("\n❌ Failed to fix dependency order. Manual intervention needed.")
        print("\n🔧 Manual Fix Required:")
        print("1. Move 'handleCollectionSortChange' function declaration")
        print("2. Place it BEFORE the useEffect that references it")
        print("3. Ensure proper React hook ordering")
    
    sys.exit(0 if success else 1)