#!/usr/bin/env python3
"""
Update package.json to add homepage field for GitHub Pages deployment
"""

import json
import os

def update_package_json():
    """Update package.json with GitHub Pages homepage"""
    
    package_file = "package.json"
    
    if not os.path.exists(package_file):
        print(f"❌ Error: {package_file} not found")
        return False
    
    try:
        # Read current package.json
        with open(package_file, 'r', encoding='utf-8') as f:
            package_data = json.load(f)
        
        print(f"📖 Current package.json loaded")
        
        # Add homepage field for GitHub Pages
        package_data["homepage"] = "https://abaeckst.github.io/mtg-deck-builder"
        
        # Write updated package.json
        with open(package_file, 'w', encoding='utf-8') as f:
            json.dump(package_data, f, indent=2, ensure_ascii=False)
        
        print("✅ Successfully updated package.json with GitHub Pages homepage")
        print("🌐 Homepage set to: https://abaeckst.github.io/mtg-deck-builder")
        return True
        
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON in {package_file}: {e}")
        return False
    except Exception as e:
        print(f"❌ Error updating {package_file}: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Updating package.json for GitHub Pages deployment...")
    update_package_json()