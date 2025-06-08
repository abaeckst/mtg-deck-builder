#!/usr/bin/env python3

import os
import sys

def fix_debug_compilation_error():
    """Remove the problematic debug console.log that's breaking compilation"""
    
    filename = "src/components/MTGOLayout.tsx"
    
    if not os.path.exists(filename):
        print(f"Error: {filename} not found")
        return False
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove the problematic JSX debug code
    problematic_code = '''            {/* DEBUG: Pagination state logging */}
            {console.log('🔍 PAGINATION DEBUG:', {
              hasMore: pagination.hasMore,
              totalCards: pagination.totalCards,
              loadedCards: pagination.loadedCards,
              isLoadingMore: pagination.isLoadingMore,
              currentPage: pagination.currentPage,
              loading: loading,
              error: error
            })}'''
    
    if problematic_code in content:
        content = content.replace(problematic_code, '')
        print("✅ Removed problematic debug JSX code")
    else:
        # Try to find and remove any similar debug patterns
        lines = content.split('\n')
        new_lines = []
        skip_next = False
        
        for i, line in enumerate(lines):
            if 'DEBUG: Pagination state logging' in line:
                # Skip this comment line and look for the console.log block
                continue
            elif '{console.log(' in line and 'PAGINATION DEBUG' in line:
                # Found the start of the console.log block, skip until we find the closing
                j = i
                brace_count = line.count('{') - line.count('}')
                while j < len(lines) and brace_count > 0:
                    j += 1
                    if j < len(lines):
                        brace_count += lines[j].count('{') - lines[j].count('}')
                # Skip all these lines
                i = j
                continue
            else:
                new_lines.append(line)
        
        if len(new_lines) < len(lines):
            content = '\n'.join(new_lines)
            print("✅ Removed debug code block")
        else:
            print("ℹ️  No problematic debug code found")
    
    # Add a simple, safe console.log after the collection header for debugging
    # Find the collection header
    header_pattern = '''            <h3>Collection ({cards.length.toLocaleString()} {pagination.totalCards > pagination.loadedCards && (<span className="pagination-info">of {pagination.totalCards.toLocaleString()}</span>)} cards)</h3>'''
    
    if header_pattern in content:
        # Add a useEffect with console.log instead of inline JSX
        new_header = header_pattern + '''
            {/* Safe pagination debug - check browser console */}
            {(() => {
              console.log('🔍 Pagination Debug:', {
                hasMore: pagination.hasMore,
                totalCards: pagination.totalCards,
                loadedCards: pagination.loadedCards,
                isLoadingMore: pagination.isLoadingMore,
                cardsDisplayed: cards.length
              });
              return null;
            })()}'''
        
        content = content.replace(header_pattern, new_header)
        print("✅ Added safe console.log for debugging")
    
    # Write the fixed content back
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Fixed compilation error")
    return True

if __name__ == "__main__":
    success = fix_debug_compilation_error()
    if success:
        print("\n✅ COMPILATION FIX COMPLETE")
        print("\n📋 Next steps:")
        print("1. Run: npm start")
        print("2. Verify compilation succeeds")
        print("3. Open browser console (F12)")
        print("4. Search for anything (like 'creature')")
        print("5. Look for '🔍 Pagination Debug:' messages in console")
        print("6. Report back what the pagination values show")
    else:
        print("\n❌ Fix failed")
    
    sys.exit(0 if success else 1)