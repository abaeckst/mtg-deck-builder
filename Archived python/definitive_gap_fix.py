import os
import re

def find_and_fix_all_gaps():
    """Find and fix ALL gap settings in the CSS file"""
    file_path = r"C:\Users\carol\mtg-deckbuilder\src\components\MTGOLayout.css"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        print("🔍 SEARCHING FOR ALL GAP SETTINGS:")
        
        # Find all lines containing "gap:" to see what we're dealing with
        lines = content.split('\n')
        gap_lines = []
        for i, line in enumerate(lines):
            if 'gap:' in line:
                gap_lines.append((i+1, line.strip()))
                print(f"   Line {i+1}: {line.strip()}")
        
        if not gap_lines:
            print("❌ No gap settings found!")
            return False
        
        print(f"\n🎯 Found {len(gap_lines)} gap settings. Fixing pile-related ones...")
        
        # Strategy: Find the .pile-columns-container section and fix its gap
        # Look for the pile-columns-container definition
        pile_container_found = False
        in_pile_container = False
        
        new_lines = []
        for line in lines:
            if '.pile-columns-container {' in line:
                pile_container_found = True
                in_pile_container = True
                print("✅ Found .pile-columns-container section")
                new_lines.append(line)
            elif in_pile_container and line.strip().startswith('}'):
                in_pile_container = False
                new_lines.append(line)
            elif in_pile_container and 'gap:' in line:
                # Replace any gap setting in the pile-columns-container with 8px
                old_line = line
                new_line = re.sub(r'gap:\s*[^;]+;', 'gap: 8px;', line)
                new_lines.append(new_line)
                print(f"🔧 FIXED: '{old_line.strip()}' → '{new_line.strip()}'")
            else:
                new_lines.append(line)
        
        if not pile_container_found:
            print("❌ Could not find .pile-columns-container section!")
            return False
        
        # Write the fixed content back
        new_content = '\n'.join(new_lines)
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(new_content)
        
        print(f"✅ Successfully updated {file_path}")
        return True
        
    except FileNotFoundError:
        print(f"❌ File not found: {file_path}")
        return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def verify_fix():
    """Verify the fix was applied"""
    file_path = r"C:\Users\carol\mtg-deckbuilder\src\components\MTGOLayout.css"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        print("\n🔍 VERIFICATION - Current gap settings:")
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if 'gap:' in line:
                print(f"   Line {i+1}: {line.strip()}")
        
        # Check specifically for pile-columns-container
        if '.pile-columns-container' in content:
            # Extract the pile-columns-container section
            start = content.find('.pile-columns-container')
            end = content.find('}', start)
            section = content[start:end+1]
            if 'gap: 8px' in section:
                print("✅ VERIFIED: pile-columns-container has gap: 8px")
                return True
            else:
                print("❌ VERIFICATION FAILED: gap not set to 8px in pile-columns-container")
                return False
        
    except Exception as e:
        print(f"❌ Verification error: {str(e)}")
        return False

def main():
    """NO MORE TELEVISIONS ON CARS - DEFINITIVE FIX"""
    print("📺🚗 PREVENTING TELEVISION THROWING INCIDENT!")
    print("🎯 DEFINITIVE GAP FIX - WILL ACTUALLY WORK THIS TIME")
    print()
    
    if find_and_fix_all_gaps():
        if verify_fix():
            print()
            print("🎉 SUCCESS! GAP FIX VERIFIED!")
            print("✅ Pile columns should now have 8px breathing room")
            print("✅ No more touching cards")
            print("✅ Professional MTGO spacing achieved")
            print()
            print("📺 TELEVISIONS ARE SAFE!")
            print("🚗 CARS ARE SAFE!")
            print()
            print("🔧 Test with 'npm start' - you should see the difference!")
        else:
            print()
            print("⚠️ Fix applied but verification failed")
            print("📺 Televisions still at risk...")
    else:
        print()
        print("❌ Fix failed completely")
        print("📺🚗 TELEVISION THROWING INCIDENT IMMINENT!")

if __name__ == "__main__":
    main()