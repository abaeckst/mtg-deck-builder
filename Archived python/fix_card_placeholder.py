#!/usr/bin/env python3
"""
Quick fix for CardPlaceholder component in MagicCard.tsx
"""

def fix_card_placeholder():
    """Fix CardPlaceholder component to support scaleFactor"""
    file_path = "src/components/MagicCard.tsx"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find and fix the CardPlaceholder component
        old_placeholder = '''export const CardPlaceholder: React.FC<{
  size?: 'small' | 'normal' | 'large';
  className?: string;
  style?: React.CSSProperties;
}> = ({ size = 'normal', className = '', style }) => {
  const sizeStyles = getSizeStyles(size, scaleFactor);'''

        new_placeholder = '''export const CardPlaceholder: React.FC<{
  size?: 'small' | 'normal' | 'large';
  scaleFactor?: number;
  className?: string;
  style?: React.CSSProperties;
}> = ({ size = 'normal', scaleFactor = 1, className = '', style }) => {
  const sizeStyles = getSizeStyles(size, scaleFactor);'''

        # Apply the fix
        content = content.replace(old_placeholder, new_placeholder)
        
        # Write updated content
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        print(f"✅ Successfully fixed CardPlaceholder in {file_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error fixing CardPlaceholder: {e}")
        return False

if __name__ == "__main__":
    print("🔧 Fixing CardPlaceholder component...")
    if fix_card_placeholder():
        print("✅ Fix applied successfully!")
        print("Now run 'npm start' to test the application.")
    else:
        print("❌ Fix failed - please check the error above.")
