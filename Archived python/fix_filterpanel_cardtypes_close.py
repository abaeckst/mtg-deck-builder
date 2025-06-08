#!/usr/bin/env python3

import os
import sys

def fix_filterpanel_cardtypes_close():
    """Fix the Card Types collapsible section closure in FilterPanel.tsx"""
    
    filename = "src/components/FilterPanel.tsx"
    
    if not os.path.exists(filename):
        print(f"Error: {filename} not found")
        return False
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find and fix the Card Types section closure
    updates = [
        # Look for the end of the Card Types button mapping and close the section
        (
            '                  autoExpandSection(\'types\');\n                }}\n              >\n                {type}\n              </button>\n            ))}\n          </div>\n        </div>',
            '                  autoExpandSection(\'types\');\n                }}\n              >\n                {type}\n              </button>\n            ))}\n          </div>\n        </CollapsibleSection>',
            "Close Card Types collapsible section"
        ),
        
        # Alternative pattern if the above doesn't match
        (
            '              </button>\n            ))}\n          </div>\n        </div>\n\n        {/* More Types (Subtypes) Group - Collapsible */}',
            '              </button>\n            ))}\n          </div>\n        </CollapsibleSection>\n\n        {/* More Types (Subtypes) Group - Collapsible */}',
            "Close Card Types section (alternative pattern)"
        ),
        
        # Also need to close the Mana Value section properly
        (
            '              className="range-input"\n            />\n          </div>\n          </div>\n        </CollapsibleSection>',
            '              className="range-input"\n            />\n          </div>\n        </CollapsibleSection>',
            "Fix Mana Value section closure (remove extra div)"
        ),
    ]
    
    for old_str, new_str, desc in updates:
        if old_str in content:
            content = content.replace(old_str, new_str)
            print(f"✅ {desc}")
        else:
            print(f"ℹ️ Pattern not found: {desc}")
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Successfully updated {filename}")
    return True

if __name__ == "__main__":
    success = fix_filterpanel_cardtypes_close()
    sys.exit(0 if success else 1)