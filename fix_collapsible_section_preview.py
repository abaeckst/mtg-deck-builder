#!/usr/bin/env python3

import os
import sys

def fix_collapsible_section_preview():
    """Fix CollapsibleSection to properly support previewText prop"""
    
    collapsible_file = "src/components/CollapsibleSection.tsx"
    if not os.path.exists(collapsible_file):
        print(f"❌ {collapsible_file} not found")
        return False
    
    with open(collapsible_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix 1: Add previewText to interface
    old_interface = '''interface CollapsibleSectionProps {
  title: string;
  isExpanded: boolean;
  hasActiveFilters: boolean;
  onToggle: () => void;
  children: React.ReactNode;
  className?: string;
}'''
    
    new_interface = '''interface CollapsibleSectionProps {
  title: string;
  previewText?: string;
  isExpanded: boolean;
  hasActiveFilters: boolean;
  onToggle: () => void;
  children: React.ReactNode;
  className?: string;
}'''
    
    if old_interface in content:
        content = content.replace(old_interface, new_interface)
        print("✅ Added previewText to CollapsibleSectionProps interface")
    else:
        print("❌ Could not find interface to update")
        return False
    
    # Fix 2: Add previewText to component signature
    old_signature = '''const CollapsibleSection: React.FC<CollapsibleSectionProps> = ({
  title,
  isExpanded,
  hasActiveFilters,
  onToggle,
  children,
  className = ''
}) => {'''
    
    new_signature = '''const CollapsibleSection: React.FC<CollapsibleSectionProps> = ({
  title,
  previewText = '',
  isExpanded,
  hasActiveFilters,
  onToggle,
  children,
  className = ''
}) => {'''
    
    if old_signature in content:
        content = content.replace(old_signature, new_signature)
        print("✅ Added previewText to component signature")
    else:
        print("❌ Could not find component signature to update")
        return False
    
    with open(collapsible_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ CollapsibleSection preview text support fixed!")
    return True

if __name__ == "__main__":
    success = fix_collapsible_section_preview()
    sys.exit(0 if success else 1)