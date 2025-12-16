import numpy as np
import cv2
from embed import *
import json
import os
from dct import *


def process_rgb_image(img, func):
    """Apply a function to each RGB channel separately"""
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