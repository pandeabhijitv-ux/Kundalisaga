"""
Generate Android app icons from Ganesh image
Creates all required mipmap sizes for Android
"""

from PIL import Image
import os

# Source image
source_image = r"C:\AstroKnowledge\assets\ganesh.jpg"
output_base = r"C:\AstroKnowledge\mobile\android\app\src\main\res"

# Android icon sizes
icon_sizes = {
    "mipmap-mdpi": 48,
    "mipmap-hdpi": 72,
    "mipmap-xhdpi": 96,
    "mipmap-xxhdpi": 144,
    "mipmap-xxxhdpi": 192
}

def create_round_icon(img, size):
    """Create a square icon with rounded corners"""
    # Create a circular mask
    from PIL import ImageDraw
    
    # Resize image
    img = img.resize((size, size), Image.Resampling.LANCZOS)
    
    # Create mask for rounded corners
    mask = Image.new('L', (size, size), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size, size), fill=255)
    
    # Apply mask
    output = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    output.paste(img, (0, 0))
    output.putalpha(mask)
    
    return output

def main():
    print("🕉️  Generating Android icons from Shree Ganesh image...\n")
    
    # Load source image
    img = Image.open(source_image)
    print(f"✅ Loaded image: {img.size}, mode: {img.mode}\n")
    
    # Convert to RGB if needed
    if img.mode != 'RGB':
        img = img.convert('RGB')
    
    # Generate icons for each size
    for folder, size in icon_sizes.items():
        folder_path = os.path.join(output_base, folder)
        
        # Create folder if doesn't exist
        os.makedirs(folder_path, exist_ok=True)
        
        # Generate square icon
        square_icon = img.resize((size, size), Image.Resampling.LANCZOS)
        square_path = os.path.join(folder_path, "ic_launcher.png")
        square_icon.save(square_path, "PNG")
        print(f"✅ {folder}/ic_launcher.png ({size}x{size})")
        
        # Generate round icon
        round_icon = create_round_icon(img.copy(), size)
        round_path = os.path.join(folder_path, "ic_launcher_round.png")
        round_icon.save(round_path, "PNG")
        print(f"✅ {folder}/ic_launcher_round.png ({size}x{size})")
    
    print(f"\n🎉 All icons generated successfully!")
    print("App icon will now show Shree Ganesh Ji! 🙏")

if __name__ == "__main__":
    main()
