"""
receiver.py - Image Steganography Extraction Script

This script extracts a hidden small image from an embedded image created by sender.py.

Process:
    1. Load embedded image from img_embed directory
    2. Apply 3D DCT to embedded image
    3. Extract small DCT coefficients from specific positions
    4. Decrypt extracted coefficients
    5. Apply inverse DCT to get spatial domain small image
    6. Save extracted image

Configuration:
    Must use the SAME config.json as sender.py:
        - alpha: Must match embedding alpha
        - method: Must match embedding method
        - encrypt: Must match embedding encryption setting
        - p, q: Must match encryption parameters

def extract_2d(embedded_dct_channel, small_h, small_w, config):
    """
    Extract small DCT from a single channel using stride-based positioning.
    
    Args:
        embedded_dct_channel (np.ndarray): Embedded DCT for one channel, shape (H, W)
        small_h (int): Target small image height
        small_w (int): Target small image width
        config (dict): Configuration dictionary
    
    Returns:
        np.ndarray: Extracted small DCT, shape (small_h, small_w)
    
    Extraction Strategy:
        - Must use SAME stride and positioning logic as embed_2d
        - Reads coefficients from predetermined positions
        - Applies decrypt function to recover original small coefficients
        
    Critical:
        config['method'] must match the method used during embedding!
    """
    #* size is 32*32: img_embed/embedded_result_11.png (or specified)
    
Output:
    - Extracted image: img_extracted/extracted_N.png (N auto-increments)

Usage:
    python receiver.py
    
Example:
    $ python receiver.py
    Embedded image loaded from 'img_embed/embedded_result_11.png'
    Configuration loaded.
    DCT applied to embedded image.
    Extraction process completed. Extracted size: 32x32
    Extraction complete! Result saved as 'img_extracted/extracted_0.png'
"""

import numpy as np
import cv2
from embed import *
import json
import os
from dct import *


def extract_3d(embedded_dct, small_h, small_w, config):
    """
    Extract small 3D DCT from embedded DCT (processes all color channels).
    
    Args:
        embedded_dct (np.ndarray): Embedded image DCT, shape (H, W, C)
        small_h (int): Target small image height
        small_w (int): Target small image width
        config (dict): Configuration with extraction parameters
    
    Returns:
        np.ndarray: Extracted small DCT, shape (small_h, small_w, C)
    
    Note:
        Applies extract_2d independently to each color channel.
    """
    big_h, big_w, big_d = embedded_dct.shape
    
    extracted_dct = np.zeros((small_h, small_w, big_d))
    
    for ch in range(big_d):
        extracted_dct[:, :, ch] = extract_2d(embedded_dct[:, :, ch],  small_h, small_w, config)
    
    return extracted_dct


def extract_2d(embedded_dct_channel, small_h, small_w, config):
    #* size is 32*32
    big_h, big_w = embedded_dct_channel.shape
    extracted_dct = np.zeros((small_h, small_w))

    stride_h = big_h // small_h
    stride_w = big_w // small_w

    for sx in range(small_h):
def main():
    """
    Main extraction workflow.
    
    Steps:
        1. Load embedded image from disk
        2. Load configuration (must match embedding config!)
        3. Transform embedded image to frequency domain (DCT)
        4. Extract small DCT from specific positions
        5. Decrypt extracted coefficients
        6. Transform back to spatial domain (IDCT)
        7. Save result with auto-incremented filename
    """ sy in range(small_w):
            #position in big image
            if config['method'] == 'center':
                bx = sx * stride_h + stride_h // 2
                by = sy * stride_w + stride_w // 2
            elif config['method'] == 'high_freq':
                bx = (sx + 1) * stride_h - 1
                by = (sy + 1) * stride_w - 1
            val = embedded_dct_channel[bx, by]
            extracted_val = decrypt(
                val,
                config['alpha'],
                config['p'],
                config['q'],
                config['encrypt']
            )
            extracted_dct[sx, sy] = extracted_val
    return extracted_dct


def main():
    embedded_img_path = 'img_embed/embedded_result_11.png' # and 12
    output_path = 'img_extracted/extracted.png'
    
    # Create output directory if it doesn't exist
    os.makedirs('img_extracted', exist_ok=True)

    # Read embedded image and original big image
    embedded_img = cv2.imread(embedded_img_path)
    print(f"Embedded image loaded from '{embedded_img_path}'")
    
    # Load configuration
    with open('config.json', 'r') as f:
        config = json.load(f)
    print("Configuration loaded.")

    # Apply DCT to both embedded and original images
    embedded_dct = dct_3d(embedded_img)
    print("DCT applied to embedded image.")
    
    # Extract the small image DCT
    # Get dimensions from embedded image - assuming 256x256 big, 32x32 small
    big_h, big_w, _ = embedded_img.shape
    small_h = 32  # You can make this configurable
    small_w = 32
    
    extracted_dct = extract_3d(embedded_dct, small_h, small_w, config)
    print(f"Extraction process completed. Extracted size: {small_h}x{small_w}")
    print(f"Extracted DCT range: [{extracted_dct.min():.2f}, {extracted_dct.max():.2f}]")
    
    # Apply inverse DCT to get the image back
    extracted_img = idct_3d(extracted_dct)
    print(f"Extracted image range: [{extracted_img.min():.2f}, {extracted_img.max():.2f}]")
    
    # Save result
    num = 0
    while os.path.exists(f'img_extracted/extracted_{num}.png'):
        num += 1
    output_path = f'img_extracted/extracted_{num}.png'
    cv2.imwrite(output_path, extracted_img)
    print(f"Extraction complete! Result saved as '{output_path}'")


if __name__ == "__main__":
    main()
