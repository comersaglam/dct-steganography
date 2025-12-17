"""
jpgToPng.py - JPEG to PNG Converter

This module converts JPEG images to PNG format for preprocessing before steganography operations.
PNG format is lossless and more suitable for DCT-based steganography as it preserves exact pixel values.

Directory Structure:
    - Input: jpg/ (contains JPEG/JPG files)
    - Output: img/ (saves converted PNG files)

Usage:
    python jpgToPng.py

Features:
    - Batch conversion of all JPG/JPEG files in the jpg directory
    - Automatic RGBA to RGB conversion for compatibility
    - Error handling for corrupted or unsupported files
"""

from PIL import Image
import os

# Directory containing the images
jpg_dir = "jpg"
img_dir = "img"

# Get all jpg files in the directory
jpg_files = [f for f in os.listdir(jpg_dir) if f.lower().endswith(('.jpg', '.jpeg'))]

print(f"Found {len(jpg_files)} JPG files to convert:")

# Convert each jpg to png
for jpg_file in jpg_files:
    jpg_path = os.path.join(jpg_dir, jpg_file)
    png_file = os.path.splitext(jpg_file)[0] + '.png'
    png_path = os.path.join(img_dir, png_file)
    
    try:
        # Open the JPG image
        img = Image.open(jpg_path)
        
        # Convert RGBA to RGB if necessary (PNG supports RGBA, but good practice)
        if img.mode == 'RGBA':
            img = img.convert('RGB')
        
        # Save as PNG
        img.save(png_path, 'PNG')
        print(f"✓ Converted: {jpg_file} -> {png_file}")
    except Exception as e:
        print(f"✗ Error converting {jpg_file}: {e}")

print(f"\nConversion complete!")
