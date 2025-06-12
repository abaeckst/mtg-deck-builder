#!/usr/bin/env python3

import re

def fix_deckarea_compilation_errors():
    """
    Fix duplicate variable declarations in DeckArea.tsx
    """
    
    file_path = "src/components/DeckArea.tsx"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        print(f"🔧 Fixing compilation errors in {file_path}")
        
        # Split content into lines for precise editing
        lines = content.split('\n')
        
        # Find and remove duplicate declarations
        # We'll keep the first occurrence and remove subsequent duplicates
        seen_declarations = set()
        filtered_lines = []
        skip_line = False
        
        for i, line in enumerate(lines):
            stripped = line.strip()
            
            # Check for useState declarations we want to deduplicate
            useState_patterns = [
                r'const \[showOverflowMenu, setShowOverflowMenu\]',
                r'const \[hiddenControls, setHiddenControls\]'
            ]
            
            # Check for useRef declarations we want to deduplicate  
            useRef_patterns = [
                r'const headerRef = useRef',
                r'const controlsRef = useRef'
            ]
            
            all_patterns = useState_patterns + useRef_patterns
            
            is_duplicate = False
            for pattern in all_patterns:
                if re.search(pattern, stripped):
                    if pattern in seen_declarations:
                        is_duplicate = True
                        print(f"🗑️  Removing duplicate line {i+1}: {stripped[:60]}...")
                        break
                    else:
                        seen_declarations.add(pattern)
                        break
            
            # Skip duplicate lines and malformed comment lines that got mixed in
            if not is_duplicate:
                # Also clean up any malformed comment lines that might have been created
                if stripped.startswith('// Responsive overflow menu state') and i > 90:
                    # Skip redundant comment if it appears after the actual declarations
                    continue
                
                filtered_lines.append(line)
        
        # Rejoin the content
        fixed_content = '\n'.join(filtered_lines)
        
        # Write the fixed content back to file
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(fixed_content)
        
        print(f"✅ Fixed compilation errors in {file_path}")
        print("🔧 Removed duplicate variable declarations")
        
        return True
        
    except FileNotFoundError:
        print(f"❌ File not found: {file_path}")
        return False
    except Exception as e:
        print(f"❌ Error fixing compilation errors: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 Starting DeckArea compilation error fix...")
    
    success = fix_deckarea_compilation_errors()
    
    if success:
        print("\n✅ Compilation error fix completed!")
        print("\n📋 Next steps:")
        print("1. Run 'npm start' to check compilation")
        print("2. Test sort button and ViewModeDropdown functionality") 
        print("3. Verify nuclear z-index implementation working")
        print("4. Test overflow menu context")
    else:
        print("\n❌ Fix failed - manual intervention needed")
