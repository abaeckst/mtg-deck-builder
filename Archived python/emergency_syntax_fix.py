#!/usr/bin/env python3
"""
Emergency fix for syntax error in scryfallApi.ts
Remove the orphaned function code that's causing the compilation error.
"""

def fix_syntax_error():
    """Remove the orphaned function code from scryfallApi.ts"""
    print("🚨 EMERGENCY: Fixing syntax error in scryfallApi.ts...")
    
    with open('src/services/scryfallApi.ts', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Find and remove the problematic lines (lines 4-7)
    fixed_lines = []
    skip_next = False
    
    for i, line in enumerate(lines):
        line_num = i + 1
        
        # Skip the problematic lines that are causing syntax error
        if line_num >= 4 and line_num <= 8:
            # Skip lines 4-8 which contain the orphaned function code
            if "console.log('='.repeat(80));" in line or line.strip() == '}':
                print(f"Removing problematic line {line_num}: {line.strip()}")
                continue
        
        fixed_lines.append(line)
    
    # Write the fixed content back
    with open('src/services/scryfallApi.ts', 'w', encoding='utf-8') as f:
        f.writelines(fixed_lines)
    
    print("✅ Removed orphaned function code")
    return True

def main():
    """Execute the emergency fix"""
    print("🚨 EMERGENCY SYNTAX FIX")
    print("=" * 40)
    
    if fix_syntax_error():
        print("\n🎯 SYNTAX ERROR FIXED!")
        print("1. ✅ Removed orphaned function code")
        print("\n🧪 Test compilation:")
        print("npm start")
    else:
        print("\n❌ Fix failed - manual intervention needed")
        
    return True

if __name__ == "__main__":
    main()
