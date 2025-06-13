#!/usr/bin/env python3
"""
CSS Component Extraction Script
Automatically splits the monolithic CSS file into component-based architecture
"""

import re
import json
from pathlib import Path
from collections import defaultdict

class CSSExtractor:
    def __init__(self, css_file_path, analysis_file_path):
        self.css_file_path = Path(css_file_path)
        self.analysis_file_path = Path(analysis_file_path)
        self.css_content = self.css_file_path.read_text(encoding='utf-8')
        
        # Load analysis results
        with open(self.analysis_file_path) as f:
            self.analysis_results = json.load(f)
        
        self.extracted_components = {}
        self.base_styles_dir = Path("src/styles")
        
    def extract_all_components(self):
        """Extract all CSS components based on analysis"""
        print("🔧 Starting CSS component extraction...")
        
        # Create directory structure
        self.create_directory_structure()
        
        # Extract in priority order
        extraction_plan = self.analysis_results.get('extraction_plan', {})
        
        # 1. Extract base styles first
        self.extract_base_styles()
        
        # 2. Extract layout styles
        self.extract_layout_styles()
        
        # 3. Extract component styles
        self.extract_component_styles()
        
        # 4. Extract view styles
        self.extract_view_styles()
        
        # 5. Extract theme styles
        self.extract_theme_styles()
        
        # 6. Generate main CSS file
        self.generate_main_css()
        
        # 7. Create migration validation
        self.create_validation_files()
        
        print("✅ CSS extraction complete!")
        
    def create_directory_structure(self):
        """Create the new CSS directory structure"""
        print("  📁 Creating directory structure...")
        
        directories = [
            "src/styles/base",
            "src/styles/layout", 
            "src/styles/components",
            "src/styles/views",
            "src/styles/themes"
        ]
        
        for directory in directories:
            Path(directory).mkdir(parents=True, exist_ok=True)
        
        print(f"    ✅ Created {len(directories)} directories")
    
    def extract_base_styles(self):
        """Extract base styles (variables, reset, typography)"""
        print("  🎨 Extracting base styles...")
        
        # Extract CSS custom properties
        variables_css = self.generate_variables_css()
        self.write_css_file("base/variables.css", variables_css)
        
        # Extract reset/normalize styles
        reset_css = """/* CSS Reset for MTG Deck Builder */
* {
  box-sizing: border-box;
}

html, body {
  margin: 0;
  padding: 0;
  height: 100%;
}

button {
  background: none;
  border: none;
  padding: 0;
  cursor: pointer;
}

input, select, textarea {
  font-family: inherit;
}

/* Remove default scrollbar styling */
* {
  scrollbar-width: thin;
  scrollbar-color: var(--scrollbar-thumb) var(--scrollbar-track);
}

*::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

*::-webkit-scrollbar-track {
  background-color: var(--scrollbar-track);
  border-radius: 4px;
}

*::-webkit-scrollbar-thumb {
  background-color: var(--scrollbar-thumb);
  border-radius: 4px;
}

*::-webkit-scrollbar-thumb:hover {
  background-color: var(--scrollbar-thumb-hover);
}

*::-webkit-scrollbar-corner {
  background-color: var(--scrollbar-track);
}
"""
        self.write_css_file("base/reset.css", reset_css)
        
        # Extract typography
        typography_css = """/* Typography System */
body {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  color: var(--text-primary);
  font-size: var(--font-size-base);
  line-height: var(--line-height-base);
}

/* Heading styles */
h1, h2, h3, h4, h5, h6 {
  margin: 0;
  font-weight: 600;
  line-height: var(--line-height-tight);
}

h1 { font-size: var(--font-size-2xl); }
h2 { font-size: var(--font-size-xl); }
h3 { font-size: var(--font-size-lg); }
h4 { font-size: var(--font-size-md); }
h5 { font-size: var(--font-size-sm); }
h6 { font-size: var(--font-size-xs); }

/* Text utilities */
.text-primary { color: var(--text-primary); }
.text-secondary { color: var(--text-secondary); }
.text-muted { color: var(--text-muted); }
.text-accent { color: var(--color-accent); }

.font-bold { font-weight: bold; }
.font-medium { font-weight: 500; }
.font-normal { font-weight: 400; }

.text-center { text-align: center; }
.text-left { text-align: left; }
.text-right { text-align: right; }

.uppercase { text-transform: uppercase; }
.lowercase { text-transform: lowercase; }
.capitalize { text-transform: capitalize; }
"""
        self.write_css_file("base/typography.css", typography_css)
        
        print("    ✅ Base styles extracted")
    
    def generate_variables_css(self):
        """Generate CSS custom properties from analysis"""
        variables = []
        
        # Color system from analysis
        if 'hardcoded_values' in self.analysis_results:
            hv = self.analysis_results['hardcoded_values']
            
            # Base color palette
            variables.extend([
                "  /* Color System */",
                "  --color-bg-primary: #1a1a1a;",
                "  --color-bg-secondary: #2a2a2a;",
                "  --color-bg-tertiary: #333333;",
                "  --color-bg-quaternary: #404040;",
                "",
                "  --color-text-primary: #ffffff;",
                "  --color-text-secondary: #cccccc;",
                "  --color-text-muted: #888888;",
                "",
                "  --color-accent: #3b82f6;",
                "  --color-accent-hover: #2563eb;",
                "  --color-accent-active: #1d4ed8;",
                "",
                "  --color-success: #10b981;",
                "  --color-warning: #fbbf24;",
                "  --color-error: #ef4444;",
                "",
                "  --color-border: #555555;",
                "  --color-border-light: #666666;",
                ""
            ])
        
        # Spacing system
        variables.extend([
            "  /* Spacing Scale */",
            "  --space-0: 0;",
            "  --space-1: 4px;",
            "  --space-2: 8px;",
            "  --space-3: 12px;",
            "  --space-4: 16px;",
            "  --space-5: 20px;",
            "  --space-6: 24px;",
            "  --space-8: 32px;",
            "  --space-10: 40px;",
            "",
            "  /* Gap utilities */",
            "  --gap-xs: 4px;",
            "  --gap-sm: 6px;",
            "  --gap-md: 8px;",
            "  --gap-lg: 12px;",
            "  --gap-xl: 16px;",
            ""
        ])
        
        # Component dimensions
        variables.extend([
            "  /* Component Dimensions */",
            "  --header-height: 40px;",
            "  --panel-min-width: 200px;",
            "  --panel-max-width: 500px;",
            "",
            "  /* Card sizes */",
            "  --card-size-sm: 60px;",
            "  --card-size-md: 80px;",
            "  --card-size-lg: 100px;",
            "  --card-size-xl: 120px;",
            "",
            "  /* Border radius scale */",
            "  --radius-sm: 3px;",
            "  --radius-md: 4px;",
            "  --radius-lg: 6px;",
            "  --radius-xl: 8px;",
            "  --radius-2xl: 10px;",
            "  --radius-full: 50%;",
            ""
        ])
        
        # Typography scale
        variables.extend([
            "  /* Typography Scale */",
            "  --font-size-xs: 10px;",
            "  --font-size-sm: 11px;",
            "  --font-size-base: 12px;",
            "  --font-size-md: 13px;",
            "  --font-size-lg: 14px;",
            "  --font-size-xl: 16px;",
            "  --font-size-2xl: 18px;",
            "",
            "  --line-height-tight: 1.2;",
            "  --line-height-base: 1.4;",
            "  --line-height-relaxed: 1.6;",
            ""
        ])
        
        # Layout system
        variables.extend([
            "  /* Layout System */",
            "  --deck-area-height-percent: 30%;",
            "  --deck-area-height: 300px;",
            "  --collection-area-height: 700px;",
            "",
            "  /* Scrollbar styling */",
            "  --scrollbar-width: 8px;",
            "  --scrollbar-track: var(--color-bg-primary);",
            "  --scrollbar-thumb: var(--color-bg-quaternary);",
            "  --scrollbar-thumb-hover: #555555;",
            ""
        ])
        
        # Transitions and animations
        variables.extend([
            "  /* Transitions */",
            "  --transition-fast: 0.15s ease;",
            "  --transition-normal: 0.2s ease;",
            "  --transition-slow: 0.3s ease;",
            "",
            "  --transition-cubic: cubic-bezier(0.4, 0, 0.2, 1);",
            "",
            "  /* Shadows */",
            "  --shadow-sm: 0 2px 4px rgba(0, 0, 0, 0.3);",
            "  --shadow-md: 0 4px 8px rgba(0, 0, 0, 0.4);",
            "  --shadow-lg: 0 6px 12px rgba(0, 0, 0, 0.5);",
            "",
            "  /* Z-index scale */",
            "  --z-dropdown: 1000;",
            "  --z-modal: 10000;",
            "  --z-tooltip: 10001;"
        ])
        
        # Wrap in :root selector
        css_content = ":root {\n" + "\n".join(variables) + "\n}\n"
        
        return css_content
    
    def extract_layout_styles(self):
        """Extract layout-related styles"""
        print("  🏗️ Extracting layout styles...")
        
        # Extract main grid layout
        grid_css = self.extract_styles_by_pattern([
            r'\.mtgo-layout\s*{[^}]+}',
            r'\.mtgo-main-content\s*{[^}]+}',
            r'\.mtgo-collection-area\s*{[^}]+}',
            r'\.mtgo-bottom-area\s*{[^}]+}',
            r'\.mtgo-deck-area\s*{[^}]+}',
            r'\.mtgo-sideboard-panel\s*{[^}]+}',
            r'\.mtgo-filter-panel\s*{[^}]+}'
        ])
        
        # Add utility classes for layout
        grid_css += """
/* Layout Utilities */
.flex { display: flex; }
.flex-col { flex-direction: column; }
.flex-row { flex-direction: row; }

.items-center { align-items: center; }
.items-start { align-items: flex-start; }
.items-end { align-items: flex-end; }
.items-stretch { align-items: stretch; }

.justify-center { justify-content: center; }
.justify-start { justify-content: flex-start; }
.justify-end { justify-content: flex-end; }
.justify-between { justify-content: space-between; }

.flex-1 { flex: 1; }
.flex-none { flex: none; }
.flex-shrink-0 { flex-shrink: 0; }

.relative { position: relative; }
.absolute { position: absolute; }
.fixed { position: fixed; }

.overflow-hidden { overflow: hidden; }
.overflow-auto { overflow: auto; }
.overflow-scroll { overflow: scroll; }
"""
        
        self.write_css_file("layout/grid.css", grid_css)
        
        # Extract panel system
        panels_css = self.extract_styles_by_pattern([
            r'\.panel-header[^{]*{[^}]+}',
            r'\.resize-handle[^{]*{[^}]+}',
            r'\.filter-content[^{]*{[^}]+}',
            r'\.deck-content[^{]*{[^}]+}',
            r'\.sideboard-content[^{]*{[^}]+}'
        ])
        
        self.write_css_file("layout/panels.css", panels_css)
        
        # Extract responsive styles (will be populated later)
        responsive_css = "/* Responsive styles will be consolidated here */\n"
        self.write_css_file("layout/responsive.css", responsive_css)
        
        print("    ✅ Layout styles extracted")
    
    def extract_component_styles(self):
        """Extract component-specific styles"""
        print("  🧩 Extracting component styles...")
        
        # Extract button styles
        buttons_css = self.extract_styles_by_pattern([
            r'[^{]*button[^{]*{[^}]+}',
            r'[^{]*-btn[^{]*{[^}]+}',
            r'\.quick-actions[^{]*{[^}]+}',
            r'\.view-controls[^{]*{[^}]+}'
        ])
        
        # Add button utilities
        buttons_css += """
/* Button Utilities */
.btn {
  background-color: var(--color-bg-quaternary);
  color: var(--color-text-primary);
  border: 1px solid var(--color-border);
  padding: var(--space-1) var(--space-2);
  border-radius: var(--radius-sm);
  font-size: var(--font-size-sm);
  cursor: pointer;
  transition: all var(--transition-normal);
}

.btn:hover {
  background-color: var(--color-bg-quaternary);
  opacity: 0.9;
}

.btn-primary {
  background-color: var(--color-accent);
  border-color: var(--color-accent-hover);
}

.btn-primary:hover {
  background-color: var(--color-accent-hover);
}

.btn-success {
  background-color: var(--color-success);
  border-color: var(--color-success);
}

.btn-error {
  background-color: var(--color-error);
  border-color: var(--color-error);
}

.btn-sm {
  padding: var(--space-1);
  font-size: var(--font-size-xs);
}

.btn-lg {
  padding: var(--space-3) var(--space-4);
  font-size: var(--font-size-lg);
}
"""
        
        self.write_css_file("components/buttons.css", buttons_css)
        
        # Extract form styles
        forms_css = self.extract_styles_by_pattern([
            r'[^{]*input[^{]*{[^}]+}',
            r'[^{]*select[^{]*{[^}]+}',
            r'[^{]*slider[^{]*{[^}]+}',
            r'\.search-input[^{]*{[^}]+}',
            r'\.format-select[^{]*{[^}]+}'
        ])
        
        self.write_css_file("components/forms.css", forms_css)
        
        # Extract card styles
        cards_css = self.extract_styles_by_pattern([
            r'\.collection-card[^{]*{[^}]+}',
            r'\.deck-card[^{]*{[^}]+}',
            r'\.sideboard-card[^{]*{[^}]+}',
            r'\.magic-card[^{]*{[^}]+}'
        ])
        
        self.write_css_file("components/cards.css", cards_css)
        
        # Extract drag and drop styles
        drag_drop_css = self.extract_styles_by_pattern([
            r'[^{]*drag[^{]*{[^}]+}',
            r'[^{]*drop[^{]*{[^}]+}',
            r'\.draggable[^{]*{[^}]+}'
        ])
        
        self.write_css_file("components/drag-drop.css", drag_drop_css)
        
        print("    ✅ Component styles extracted")
    
    def extract_view_styles(self):
        """Extract view-specific styles"""
        print("  👁️ Extracting view styles...")
        
        # Extract pile view styles
        pile_view_css = self.extract_styles_by_pattern([
            r'\.pile-[^{]*{[^}]+}',
            r'pile-view[^{]*{[^}]+}'
        ])
        
        self.write_css_file("views/pile-view.css", pile_view_css)
        
        # Extract list view styles
        list_view_css = self.extract_styles_by_pattern([
            r'\.list-view[^{]*{[^}]+}',
            r'\.list-[^{]*{[^}]+}'
        ])
        
        self.write_css_file("views/list-view.css", list_view_css)
        
        print("    ✅ View styles extracted")
    
    def extract_theme_styles(self):
        """Extract theme-related styles"""
        print("  🎨 Extracting theme styles...")
        
        # Extract color-specific styles
        theme_css = """/* MTGO Dark Theme */

/* Color identity specific styling */
.color-button.color-w { background-color: #fffbd5; color: #000000; }
.color-button.color-u { background-color: #0e68ab; color: #ffffff; }
.color-button.color-b { background-color: #150b00; color: #ffffff; }
.color-button.color-r { background-color: #d3202a; color: #ffffff; }
.color-button.color-g { background-color: #00733e; color: #ffffff; }
.color-button.color-c { background-color: #ccc2c0; color: #000000; }

.color-circle.color-w { background-color: #fffbd5; color: #000000; }
.color-circle.color-u { background-color: #0e68ab; color: #ffffff; }
.color-circle.color-b { background-color: #150b00; color: #ffffff; }
.color-circle.color-r { background-color: #d3202a; color: #ffffff; }
.color-circle.color-g { background-color: #00733e; color: #ffffff; }
.color-circle.color-c { background-color: #ccc2c0; color: #000000; }

/* Rarity colors */
.rarity-button.rarity-common { background-color: #6b7280; }
.rarity-button.rarity-uncommon { background-color: #c0c0c0; color: #000000; }
.rarity-button.rarity-rare { background-color: #fbbf24; color: #000000; }
.rarity-button.rarity-mythic { background-color: #f59e0b; color: #000000; }

/* Special text colors */
.mana-cost {
  font-family: 'Courier New', monospace;
  color: var(--color-warning);
  font-weight: bold;
}

.type-line {
  color: var(--color-text-secondary);
  font-style: italic;
}

.oracle-text {
  color: var(--color-text-secondary);
  font-size: var(--font-size-xs);
  line-height: var(--line-height-base);
}

.power, .toughness {
  font-weight: bold;
  color: var(--color-error);
  text-align: center;
  display: block;
}
"""
        
        self.write_css_file("themes/mtgo-dark.css", theme_css)
        
        print("    ✅ Theme styles extracted")
    
    def generate_main_css(self):
        """Generate the main CSS file that imports all others"""
        print("  📝 Generating main CSS file...")
        
        main_css = """/* MTG Deck Builder - Main CSS File */
/* Import order is important for proper cascading */

/* Base styles first */
@import './base/reset.css';
@import './base/variables.css';
@import './base/typography.css';

/* Layout system */
@import './layout/grid.css';
@import './layout/panels.css';

/* Component styles */
@import './components/buttons.css';
@import './components/forms.css';
@import './components/cards.css';
@import './components/drag-drop.css';

/* View-specific styles */
@import './views/pile-view.css';
@import './views/list-view.css';

/* Theme and responsive last */
@import './themes/mtgo-dark.css';
@import './layout/responsive.css';
"""
        
        self.write_css_file("main.css", main_css)
        
        print("    ✅ Main CSS file generated")
    
    def extract_styles_by_pattern(self, patterns):
        """Extract CSS rules matching given patterns"""
        extracted_css = ""
        
        for pattern in patterns:
            matches = re.finditer(pattern, self.css_content, re.DOTALL | re.IGNORECASE)
            for match in matches:
                extracted_css += match.group(0) + "\n\n"
        
        return extracted_css
    
    def write_css_file(self, relative_path, content):
        """Write CSS content to file"""
        file_path = self.base_styles_dir / relative_path
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Add file header
        header = f"""/* 
 * {relative_path}
 * Generated by CSS extraction script
 * MTG Deck Builder - Component-based architecture
 */

"""
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(header + content)
        
        print(f"    📄 Created: {relative_path}")
    
    def create_validation_files(self):
        """Create files for validation and migration help"""
        print("  ✅ Creating validation files...")
        
        # Create migration guide
        migration_guide = """# CSS Migration Guide

## Files Created
- `src/styles/main.css` - Main entry point (import this in your components)
- `src/styles/base/` - Reset, variables, typography
- `src/styles/layout/` - Grid system and panels
- `src/styles/components/` - Reusable UI components
- `src/styles/views/` - View-specific styles
- `src/styles/themes/` - Color themes

## How to Use

1. Replace the import in your main component:
   ```jsx
   // OLD
   import './MTGOLayout.css'
   
   // NEW
   import '../styles/main.css'
   ```

2. Use CSS custom properties in your components:
   ```css
   /* Instead of hardcoded colors */
   background-color: #2a2a2a;
   
   /* Use variables */
   background-color: var(--color-bg-secondary);
   ```

3. Use utility classes for common patterns:
   ```jsx
   // Instead of custom CSS
   <div className="flex items-center justify-between">
   ```

## Validation
Run the validation script to ensure no styles are broken:
```bash
python validate_css_migration.py
```
"""
        
        with open(self.base_styles_dir / "MIGRATION_GUIDE.md", 'w') as f:
            f.write(migration_guide)
        
        print("    📋 Migration guide created")

def main():
    """Main execution function"""
    css_file = "src/components/MTGOLayout.css"
    analysis_file = "src/components/css_analysis_results.json"
    
    if not Path(css_file).exists():
        print(f"❌ CSS file not found: {css_file}")
        return
    
    if not Path(analysis_file).exists():
        print("⚠️ Analysis file not found. Running analysis first...")
        # Could run the analyzer here, but for now just warn
        print("Please run analyze_css_structure.py first")
        return
    
    print("🔧 MTG Deck Builder - CSS Component Extraction")
    print("=" * 50)
    
    extractor = CSSExtractor(css_file, analysis_file)
    extractor.extract_all_components()
    
    print("\n🎉 CSS extraction complete!")
    print("Next steps:")
    print("1. Update your component imports to use 'src/styles/main.css'")
    print("2. Run validation to ensure no regressions")
    print("3. Start using utility classes and CSS custom properties")

if __name__ == "__main__":
    main()
