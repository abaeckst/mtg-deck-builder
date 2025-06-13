#!/usr/bin/env python3
"""
CSS Architecture Analysis Script
Analyzes the monolithic MTGOLayout.css file to identify patterns for automated extraction
"""

import re
import json
from collections import defaultdict, Counter
from pathlib import Path

class CSSAnalyzer:
    def __init__(self, css_file_path):
        self.css_file_path = Path(css_file_path)
        self.css_content = self.css_file_path.read_text(encoding='utf-8')
        self.analysis_results = {}
        
    def analyze(self):
        """Run complete CSS analysis"""
        print("🔍 Analyzing CSS structure...")
        
        # Core analysis functions
        self.analyze_selectors()
        self.analyze_properties()
        self.analyze_media_queries()
        self.analyze_component_boundaries()
        self.analyze_repeated_patterns()
        self.analyze_hardcoded_values()
        
        # Generate extraction plan
        self.generate_extraction_plan()
        
        # Save results
        self.save_analysis()
        
        return self.analysis_results
    
    def analyze_selectors(self):
        """Analyze CSS selectors to identify component boundaries"""
        print("  📊 Analyzing selectors...")
        
        # Extract all selectors
        selector_pattern = r'([^{]+){'
        selectors = re.findall(selector_pattern, self.css_content, re.MULTILINE)
        
        # Clean and categorize selectors
        component_selectors = defaultdict(list)
        
        for selector in selectors:
            clean_selector = selector.strip()
            if not clean_selector or clean_selector.startswith('/*'):
                continue
                
            # Categorize by component patterns
            if '.mtgo-layout' in clean_selector:
                component_selectors['layout'].append(clean_selector)
            elif '.mtgo-filter' in clean_selector or '.filter-' in clean_selector:
                component_selectors['filter-panel'].append(clean_selector)
            elif '.mtgo-collection' in clean_selector or '.collection-' in clean_selector:
                component_selectors['collection'].append(clean_selector)
            elif '.mtgo-deck' in clean_selector or '.deck-' in clean_selector:
                component_selectors['deck'].append(clean_selector)
            elif '.mtgo-sideboard' in clean_selector or '.sideboard-' in clean_selector:
                component_selectors['sideboard'].append(clean_selector)
            elif '.pile-' in clean_selector or 'pile-view' in clean_selector:
                component_selectors['pile-view'].append(clean_selector)
            elif '.list-view' in clean_selector or '.list-' in clean_selector:
                component_selectors['list-view'].append(clean_selector)
            elif '.drag' in clean_selector or '.drop' in clean_selector:
                component_selectors['drag-drop'].append(clean_selector)
            elif any(btn in clean_selector for btn in ['-btn', 'button', '-toggle']):
                component_selectors['buttons'].append(clean_selector)
            elif any(form in clean_selector for form in ['input', 'select', 'slider', 'range']):
                component_selectors['forms'].append(clean_selector)
            elif '.adaptive-header' in clean_selector or '.header-' in clean_selector:
                component_selectors['headers'].append(clean_selector)
            elif '@media' in clean_selector:
                component_selectors['responsive'].append(clean_selector)
            else:
                component_selectors['base'].append(clean_selector)
        
        self.analysis_results['selectors'] = dict(component_selectors)
        print(f"    ✅ Found {len(selectors)} selectors across {len(component_selectors)} components")
    
    def analyze_properties(self):
        """Analyze CSS properties to identify repeated patterns"""
        print("  🎨 Analyzing properties...")
        
        # Extract property-value pairs
        property_pattern = r'([a-z-]+):\s*([^;]+);'
        properties = re.findall(property_pattern, self.css_content, re.IGNORECASE)
        
        # Count property usage
        property_counts = Counter(prop for prop, _ in properties)
        value_counts = Counter(f"{prop}: {val}" for prop, val in properties)
        
        # Identify frequently used properties
        common_properties = {prop: count for prop, count in property_counts.items() if count > 5}
        common_values = {prop_val: count for prop_val, count in value_counts.items() if count > 3}
        
        self.analysis_results['properties'] = {
            'common_properties': common_properties,
            'common_values': common_values,
            'total_properties': len(properties)
        }
        
        print(f"    ✅ Found {len(common_properties)} frequently used properties")
    
    def analyze_media_queries(self):
        """Analyze media queries for consolidation opportunities"""
        print("  📱 Analyzing media queries...")
        
        # Extract media queries
        media_pattern = r'@media\s*\([^)]+\)\s*{[^}]+}'
        media_queries = re.findall(media_pattern, self.css_content, re.DOTALL)
        
        # Extract breakpoints
        breakpoint_pattern = r'@media[^{]*\((?:max-width|min-width):\s*(\d+)px\)'
        breakpoints = re.findall(breakpoint_pattern, self.css_content)
        breakpoint_counts = Counter(breakpoints)
        
        self.analysis_results['media_queries'] = {
            'total_queries': len(media_queries),
            'breakpoints': dict(breakpoint_counts),
            'consolidation_opportunities': len(set(breakpoints))
        }
        
        print(f"    ✅ Found {len(media_queries)} media queries with {len(set(breakpoints))} unique breakpoints")
    
    def analyze_component_boundaries(self):
        """Identify clear component boundaries for file splitting"""
        print("  🧩 Analyzing component boundaries...")
        
        # Find section comments that indicate component boundaries
        section_pattern = r'/\*\s*=+\s*([^*]+)\s*=+\s*\*/'
        sections = re.findall(section_pattern, self.css_content, re.IGNORECASE)
        
        # Calculate approximate line distribution
        lines = self.css_content.split('\n')
        total_lines = len(lines)
        
        component_boundaries = {}
        for section in sections:
            section_clean = section.strip()
            # Estimate lines per section (rough calculation)
            component_boundaries[section_clean] = {
                'estimated_lines': total_lines // max(len(sections), 1)
            }
        
        self.analysis_results['component_boundaries'] = {
            'sections': component_boundaries,
            'total_lines': total_lines,
            'splitting_strategy': 'section_based' if sections else 'selector_based'
        }
        
        print(f"    ✅ Found {len(sections)} component sections in {total_lines} lines")
    
    def analyze_repeated_patterns(self):
        """Identify repeated CSS patterns that can become utility classes"""
        print("  🔄 Analyzing repeated patterns...")
        
        # Common utility patterns to look for
        utility_patterns = {
            'display_flex': r'display:\s*flex[^;]*;',
            'center_alignment': r'(justify-content:\s*center|align-items:\s*center)[^;]*;',
            'padding_values': r'padding:\s*(\d+px)[^;]*;',
            'margin_values': r'margin:\s*(\d+px)[^;]*;',
            'border_radius': r'border-radius:\s*(\d+px)[^;]*;',
            'background_color': r'background-color:\s*(#[0-9a-fA-F]{6}|#[0-9a-fA-F]{3})[^;]*;',
            'color_values': r'color:\s*(#[0-9a-fA-F]{6}|#[0-9a-fA-F]{3})[^;]*;',
            'font_size': r'font-size:\s*(\d+px)[^;]*;',
            'transitions': r'transition:\s*[^;]+;',
            'box_shadow': r'box-shadow:\s*[^;]+;'
        }
        
        repeated_patterns = {}
        for pattern_name, pattern_regex in utility_patterns.items():
            matches = re.findall(pattern_regex, self.css_content, re.IGNORECASE)
            if matches:
                repeated_patterns[pattern_name] = {
                    'count': len(matches),
                    'values': list(set(matches)) if isinstance(matches[0], str) else ['complex_values']
                }
        
        self.analysis_results['repeated_patterns'] = repeated_patterns
        print(f"    ✅ Found {len(repeated_patterns)} repeated pattern types")
    
    def analyze_hardcoded_values(self):
        """Identify hardcoded values that should become CSS custom properties"""
        print("  🎯 Analyzing hardcoded values...")
        
        # Extract color values
        color_pattern = r'(#[0-9a-fA-F]{6}|#[0-9a-fA-F]{3})'
        colors = re.findall(color_pattern, self.css_content)
        color_counts = Counter(colors)
        
        # Extract pixel values
        pixel_pattern = r'(\d+)px'
        pixels = re.findall(pixel_pattern, self.css_content)
        pixel_counts = Counter(pixels)
        
        # Extract percentage values
        percent_pattern = r'(\d+)%'
        percentages = re.findall(percent_pattern, self.css_content)
        percent_counts = Counter(percentages)
        
        # Identify values that appear frequently (good candidates for variables)
        frequent_colors = {color: count for color, count in color_counts.items() if count > 3}
        frequent_pixels = {px: count for px, count in pixel_counts.items() if count > 5}
        frequent_percentages = {pct: count for pct, count in percent_counts.items() if count > 2}
        
        self.analysis_results['hardcoded_values'] = {
            'colors': frequent_colors,
            'pixels': frequent_pixels,
            'percentages': frequent_percentages,
            'total_colors': len(set(colors)),
            'total_pixels': len(set(pixels))
        }
        
        print(f"    ✅ Found {len(frequent_colors)} repeated colors, {len(frequent_pixels)} repeated pixel values")
    
    def generate_extraction_plan(self):
        """Generate a detailed plan for CSS extraction"""
        print("  📋 Generating extraction plan...")
        
        # Determine file structure based on analysis
        file_structure = {
            'base/': ['reset.css', 'variables.css', 'typography.css'],
            'layout/': ['grid.css', 'panels.css', 'responsive.css'],
            'components/': [],
            'views/': [],
            'themes/': ['mtgo-dark.css']
        }
        
        # Add component files based on selector analysis
        if 'selectors' in self.analysis_results:
            for component, selectors in self.analysis_results['selectors'].items():
                if component in ['pile-view', 'list-view']:
                    file_structure['views/'].append(f'{component}.css')
                elif component in ['layout', 'responsive']:
                    continue  # Already handled
                else:
                    file_structure['components/'].append(f'{component}.css')
        
        # Generate utility classes from repeated patterns
        utility_classes = {}
        if 'repeated_patterns' in self.analysis_results:
            for pattern_name, pattern_data in self.analysis_results['repeated_patterns'].items():
                if pattern_data['count'] > 5:  # Only create utilities for frequently used patterns
                    utility_classes[pattern_name] = pattern_data['values']
        
        # Generate custom properties from hardcoded values
        custom_properties = {}
        if 'hardcoded_values' in self.analysis_results:
            hv = self.analysis_results['hardcoded_values']
            
            # Color variables
            for i, (color, count) in enumerate(hv.get('colors', {}).items()):
                if count > 5:
                    custom_properties[f'color-{i+1}'] = color
            
            # Spacing variables
            for px, count in hv.get('pixels', {}).items():
                if count > 8 and int(px) % 4 == 0:  # Common spacing values
                    custom_properties[f'space-{px}'] = f'{px}px'
        
        extraction_plan = {
            'file_structure': file_structure,
            'utility_classes': utility_classes,
            'custom_properties': custom_properties,
            'migration_priority': [
                'base/variables.css',  # Set up custom properties first
                'layout/grid.css',     # Core layout
                'components/',         # Component styles
                'views/',              # View-specific styles
                'layout/responsive.css' # Responsive last
            ]
        }
        
        self.analysis_results['extraction_plan'] = extraction_plan
        print(f"    ✅ Generated extraction plan with {len(custom_properties)} custom properties")
    
    def save_analysis(self):
        """Save analysis results to JSON file"""
        output_file = self.css_file_path.parent / 'css_analysis_results.json'
        
        with open(output_file, 'w') as f:
            json.dump(self.analysis_results, f, indent=2)
        
        print(f"📄 Analysis saved to: {output_file}")
        
        # Generate human-readable summary
        self.generate_summary()
    
    def generate_summary(self):
        """Generate human-readable summary"""
        print("\n" + "="*60)
        print("📊 CSS ANALYSIS SUMMARY")
        print("="*60)
        
        if 'component_boundaries' in self.analysis_results:
            cb = self.analysis_results['component_boundaries']
            print(f"📏 Total Lines: {cb['total_lines']}")
            print(f"🧩 Components: {len(cb['sections'])} identified sections")
        
        if 'selectors' in self.analysis_results:
            total_selectors = sum(len(selectors) for selectors in self.analysis_results['selectors'].values())
            print(f"🎯 Total Selectors: {total_selectors}")
            print("   Component Distribution:")
            for component, selectors in self.analysis_results['selectors'].items():
                print(f"     • {component}: {len(selectors)} selectors")
        
        if 'hardcoded_values' in self.analysis_results:
            hv = self.analysis_results['hardcoded_values']
            print(f"🎨 Colors: {len(hv['colors'])} repeated colors")
            print(f"📐 Spacing: {len(hv['pixels'])} repeated pixel values")
        
        if 'extraction_plan' in self.analysis_results:
            ep = self.analysis_results['extraction_plan']
            total_files = sum(len(files) for files in ep['file_structure'].values())
            print(f"📁 Extraction Plan: {total_files} files across {len(ep['file_structure'])} directories")
            print(f"🔧 Utility Classes: {len(ep['utility_classes'])} patterns identified")
            print(f"⚙️ Custom Properties: {len(ep['custom_properties'])} variables to create")
        
        print("\n🚀 NEXT STEPS:")
        print("1. Run the CSS extraction script")
        print("2. Set up the new file structure")
        print("3. Create custom properties and utilities")
        print("4. Validate with regression testing")
        print("="*60)

def main():
    """Main execution function"""
    css_file = "src/components/MTGOLayout.css"
    
    if not Path(css_file).exists():
        print(f"❌ CSS file not found: {css_file}")
        return
    
    print("🎯 MTG Deck Builder - CSS Architecture Analysis")
    print("=" * 50)
    
    analyzer = CSSAnalyzer(css_file)
    results = analyzer.analyze()
    
    print("\n✅ Analysis complete! Check css_analysis_results.json for detailed results.")

if __name__ == "__main__":
    main()
