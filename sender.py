"""
sender.py - Image Steganography Embedding Script

This script embeds a small image into a larger image using DCT-based steganography.

Process:
    1. Load big and small images from configured directories
    2. Apply 3D DCT to both images
    3. Embed small DCT into big DCT using configured method and parameters
    4. Apply inverse DCT to get spatial domain result
    5. Save embedded image to img_embed directory

Configuration:
    Edit config.json to adjust:
        - alpha: Embedding strength (0.01-0.5)
def main():
    """
    Main embedding workflow.
    
    Steps:
        1. Load images from disk
        2. Load configuration from config.json
        3. Transform images to frequency domain (DCT)
        4. Embed small DCT into big DCT
        5. Transform back to spatial domain (IDCT)
        6. Save result with auto-incremented filename
    """ethod: 'center' or 'high_freq'
        - encrypt: Enable/disable encryption
        - p, q: Encryption parameters

Input:
    - Big image: img_256/img1.png (or configured size)
    - Small image: img_32/img2.png (or configured size)
    
Output:
    - Embedded image: img_embed/embedded_result_N.png (N auto-increments)

Usage:
    python sender.py
    
Example:
    $ python sender.py
    Images loaded.
    Configuration loaded.
    DCT applied to both images.
    Embedding process completed.
    Embedding complete! Result saved as 'img_embed/embedded_result_0.png'
"""

import numpy as np
import cv2
from embed import *
import json
import os
from dct import *


def process_rgb_image(img, func):
    """
    Apply a function to each RGB channel separately.
    
    Args:
        img (np.ndarray): Input RGB image
        func (callable): Function to apply to each channel
    
    Returns:
        list: Processed channels
    """
    channels = cv2.split(img)
    processed_channels = [func(channel) for channel in channels]
    return processed_channels


def main():

    big_img_path = 'img_256/img1.png'
    small_img_path = 'img_32/img2.png'
    num = 0
    while os.path.exists(f'img_embed/embedded_result_{num}.png'):
        num += 1
    output_path = f'img_embed/embedded_result_{num}.png'

    # Read images
    big_img = cv2.imread(big_img_path)
    small_img = cv2.imread(small_img_path)
    print("Images loaded.")
    
    # Load configuration
    with open('config.json', 'r') as f:
        config = json.load(f)
    print("Configuration loaded.")

    big_dct = dct_3d(big_img)
    small_dct = dct_3d(small_img)
    print("DCT applied to both images.")
    
    comb = embed_3d(big_dct, small_dct, config)
    print("Embedding process completed.")
    
    
    # Save result
    comb_img = idct_3d(comb)
    cv2.imwrite(output_path, comb_img)
    print(f"Embedding complete! Result saved as '{output_path}'")

if __name__ == "__main__":
    main()