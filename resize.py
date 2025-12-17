from PIL import Image
import os

def resize_image(img, target_size):
    """
    Crop image to square (center crop), then resize to target size.
    """
    # Get original dimensions
    width, height = img.size
    
    # Determine the size of the square crop
    crop_size = min(width, height)
    
    # Calculate crop coordinates (center crop)
    left = (width - crop_size) // 2
    top = (height - crop_size) // 2
    right = left + crop_size
    bottom = top + crop_size
    
    # Crop to square
    img_cropped = img.crop((left, top, right, bottom))
    
    # Resize to target size with high-quality resampling
    img_resized = img_cropped.resize((target_size, target_size), Image.Resampling.LANCZOS)
    
    return img_resized

# Directories
img_dir = "img"
output_256_dir = "img_256"
output_32_dir = "img_8"

# Create output directories if they don't exist
os.makedirs(output_256_dir, exist_ok=True)
os.makedirs(output_32_dir, exist_ok=True)
# Get all PNG files
png_files = [f for f in os.listdir(img_dir) if f.lower().endswith('.png')]

print(f"Found {len(png_files)} PNG files to resize:\n")

for idx, png_file in enumerate(png_files, start=1):
    img_path = os.path.join(img_dir, png_file)
    new_name = f"img{idx}.png"
    
    try:
        # Open image
        img = Image.open(img_path)
        
        # Ensure RGB mode
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Rename original image
        new_img_path = os.path.join(img_dir, new_name)
        img.save(new_img_path, 'PNG')
        
        # Resize to 256x256
        # img_256 = resize_image(img, 256)
        # img_256.save(os.path.join(output_256_dir, new_name), 'PNG')
        
        # Resize to 32x32
        img_32 = resize_image(img, 8)
        img_32.save(os.path.join(output_32_dir, new_name), 'PNG')
        
        print(f"✓ {png_file} -> {new_name}: cropped & resized to 256x256 & 32x32")
        
    except Exception as e:
        print(f"✗ Error processing {png_file}: {e}")

print(f"\nResize complete!")
print(f"Original images renamed in: {img_dir}/")
print(f"256x256 images saved to: {output_256_dir}/")
print(f"32x32 images saved to: {output_32_dir}/")