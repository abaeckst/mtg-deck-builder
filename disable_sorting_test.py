#!/usr/bin/env python3
"""
Temporarily disable useSorting hook to test if it's causing the performance issue
"""

import os
import shutil

def disable_sorting_hook():
    file_path = "src/hooks/useSorting.ts"
    backup_path = "src/hooks/useSorting.ts.backup"
    
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found!")
        return False
    
    # Create backup
    shutil.copy2(file_path, backup_path)
    print(f"✅ Backup created: {backup_path}")
    
    # Create minimal replacement that does nothing
    minimal_hook = '''// TEMPORARILY DISABLED FOR PERFORMANCE TESTING
import { useState } from 'react';

export const useSorting = () => {
  console.log('🟢 MINIMAL SORTING HOOK - NO PROCESSING');
  
  return {
    updateSort: () => console.log('🟢 Sort update ignored (testing mode)'),
    getSortKey: () => 'name',
    getSortDirection: () => 'asc',
    sortCards: (cards) => cards, // Return unsorted
    // All other methods return no-ops or defaults
    resetSort: () => {},
    currentSort: { key: 'name', direction: 'asc' },
    sortOptions: [],
  };
};

export default useSorting;
'''
    
    # Write minimal replacement
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(minimal_hook)
    
    print(f"✅ useSorting hook temporarily disabled")
    print("\nNOW TEST SEARCH PERFORMANCE:")
    print("1. Restart your app: npm start")
    print("2. Search for 'fear of missin'")
    print("3. Check console timing - should be much faster!")
    print("\nTO RESTORE:")
    print(f"Copy {backup_path} back to {file_path}")
    
    return True

def restore_sorting_hook():
    file_path = "src/hooks/useSorting.ts"
    backup_path = "src/hooks/useSorting.ts.backup"
    
    if os.path.exists(backup_path):
        shutil.copy2(backup_path, file_path)
        os.remove(backup_path)
        print(f"✅ useSorting hook restored from backup")
        print("Restart your app to use the restored hook")
        return True
    else:
        print(f"❌ Backup file {backup_path} not found!")
        return False

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "restore":
        print("Restoring useSorting hook...")
        restore_sorting_hook()
    else:
        print("Disabling useSorting hook for performance testing...")
        print("=" * 50)
        disable_sorting_hook()
        print("\n" + "=" * 50)
        print("RUN: python disable_sorting_hook_test.py restore")
        print("     to restore the original hook when done testing")
