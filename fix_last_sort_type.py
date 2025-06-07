#!/usr/bin/env python3

import os

def read_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return None

def write_file(filepath, content):
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed: {filepath}")
        return True
    except Exception as e:
        print(f"Error writing {filepath}: {e}")
        return False

def fix_last_sort_type():
    filepath = "src/hooks/useSearch.ts"
    content = read_file(filepath)
    
    if not content:
        return False
    
    # Fix the lastSort type issue - provide a default sort object instead of null
    old_sort = 'lastSort: null,'
    new_sort = 'lastSort: { order: "name", dir: "asc" },'
    
    content = content.replace(old_sort, new_sort)
    
    return write_file(filepath, content)

def main():
    print("🔧 Fixing lastSort type error in useSearch.ts...")
    
    if not os.path.exists("src/hooks"):
        print("❌ Error: Not in project root directory.")
        return False
    
    if fix_last_sort_type():
        print("✅ lastSort type error fixed!")
        print("📋 Changed: lastSort: null → lastSort: { order: 'name', dir: 'asc' }")
        print()
        print("🧪 Try running 'npm start' again")
        return True
    else:
        print("❌ Failed to fix lastSort type error")
        return False

if __name__ == "__main__":
    main()
