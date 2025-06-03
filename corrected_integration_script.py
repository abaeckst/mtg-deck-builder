#!/usr/bin/env python3
"""
Corrected script to integrate text export and screenshot features into MTGOLayout.tsx
This script adds the necessary imports, state, and UI buttons for the export features.
"""

import os
import re

def integrate_export_features():
    """Add export features to MTGOLayout.tsx"""
    
    mtgo_layout_path = 'src/components/MTGOLayout.tsx'
    
    if not os.path.exists(mtgo_layout_path):
        print(f"❌ Error: {mtgo_layout_path} not found!")
        return False
    
    # Read the current file
    with open(mtgo_layout_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if already integrated
    if 'TextExportModal' in content:
        print("⚠️  Export features already integrated!")
        return True
    
    # 1. Add new imports at the top (after existing imports)
    import_addition = '''
// Export modal imports
import { TextExportModal } from './TextExportModal';
import { ScreenshotModal } from './ScreenshotModal';
import { getFormatDisplayName } from '../utils/deckFormatting';'''
    
    # Find the AdaptiveHeader import and add after it
    adaptive_header_pattern = r"(import AdaptiveHeader from './AdaptiveHeader';)"
    match = re.search(adaptive_header_pattern, content)
    if match:
        end_pos = match.end()
        content = content[:end_pos] + import_addition + content[end_pos:]
        print("✅ Added import statements")
    else:
        print("❌ Could not find AdaptiveHeader import")
        return False
    
    # 2. Add modal state after existing state declarations
    modal_state = '''
  // Export modal state
  const [showTextExportModal, setShowTextExportModal] = useState(false);
  const [showScreenshotModal, setShowScreenshotModal] = useState(false);'''
    
    # Find after the sideboard state declaration
    sideboard_state_pattern = r"(const \[sideboard, setSideboard\] = useState<DeckCardInstance\[\]>\(\[\]\);)"
    match = re.search(sideboard_state_pattern, content)
    if match:
        end_pos = match.end()
        content = content[:end_pos] + modal_state + content[end_pos:]
        print("✅ Added modal state declarations")
    else:
        print("❌ Could not find sideboard state declaration")
        return False
    
    # 3. Add modal handlers after existing handlers
    modal_handlers = '''
  // Export modal handlers
  const handleTextExport = useCallback(() => {
    setShowTextExportModal(true);
  }, []);
  
  const handleScreenshot = useCallback(() => {
    setShowScreenshotModal(true);
  }, []);
  
  const handleCloseTextExport = useCallback(() => {
    setShowTextExportModal(false);
  }, []);
  
  const handleCloseScreenshot = useCallback(() => {
    setShowScreenshotModal(false);
  }, []);'''
    
    # Find after the handleClearSideboard function
    clear_sideboard_pattern = r"(const handleClearSideboard = useCallback\(\(\) => \{[^}]+\}, \[clearSelection\]\);)"
    match = re.search(clear_sideboard_pattern, content, re.DOTALL)
    if match:
        end_pos = match.end()
        content = content[:end_pos] + modal_handlers + content[end_pos:]
        print("✅ Added modal handler functions")
    else:
        print("❌ Could not find handleClearSideboard function")
        return False
    
    # 4. Add buttons in the deck header (before "Save Deck" button)
    button_addition = '''                <button onClick={handleTextExport} title="Export deck as text for MTGO">
                  Export Text
                </button>
                <button onClick={handleScreenshot} title="Generate deck image">
                  Screenshot
                </button>
                '''
    
    # Find the Save Deck button and add before it
    save_deck_pattern = r'(\s+<button>Save Deck</button>)'
    match = re.search(save_deck_pattern, content)
    if match:
        start_pos = match.start()
        content = content[:start_pos] + button_addition + content[start_pos:]
        print("✅ Added export buttons to deck header")
    else:
        print("❌ Could not find Save Deck button")
        return False
    
    # 5. Add modals at the end of the component (before closing div and ContextMenu)
    modals_addition = '''
      {/* Export Modals */}
      <TextExportModal
        isOpen={showTextExportModal}
        onClose={handleCloseTextExport}
        mainDeck={mainDeck}
        sideboard={sideboard}
        format={activeFilters.format}
        deckName="Untitled Deck"
      />
      
      <ScreenshotModal
        isOpen={showScreenshotModal}
        onClose={handleCloseScreenshot}
        mainDeck={mainDeck}
        sideboard={sideboard}
        deckName="Untitled Deck"
      />
'''
    
    # Find the ContextMenu component and add before it
    context_menu_pattern = r'(\s+{/\* Context Menu \*/})'
    match = re.search(context_menu_pattern, content)
    if match:
        start_pos = match.start()
        content = content[:start_pos] + modals_addition + content[start_pos:]
        print("✅ Added modal components")
    else:
        print("❌ Could not find Context Menu section")
        return False
    
    # Write the updated content back to the file
    try:
        with open(mtgo_layout_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Successfully updated {mtgo_layout_path}")
        return True
    except Exception as e:
        print(f"❌ Error writing file: {e}")
        return False

def main():
    """Main function to run the integration"""
    print("🚀 Integrating text export and screenshot features into MTGOLayout...")
    print()
    
    # Check if we're in the right directory
    if not os.path.exists('src/components'):
        print("❌ Error: This script should be run from the project root directory")
        print("   Expected to find 'src/components' folder")
        return
    
    # Run the integration
    success = integrate_export_features()
    
    print()
    if success:
        print("🎉 Integration completed successfully!")
        print()
        print("Next steps:")
        print("1. Make sure html2canvas is installed: npm install html2canvas @types/html2canvas")
        print("2. Run: npm start")
        print("3. Test the 'Export Text' and 'Screenshot' buttons in the main deck header")
        print()
        print("The new buttons should appear before the 'Save Deck' button.")
    else:
        print("❌ Integration failed. Please check the errors above.")
        print("   You may need to manually add the features or check file structure.")

if __name__ == '__main__':
    main()