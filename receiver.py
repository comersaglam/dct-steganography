import numpy as np
import cv2
from embed import *
import json
import os
from dct import *


def extract_3d(embedded_dct, cover_dct, small_h, small_w, config):
    """Extract small DCT from embedded DCT based on configuration.

    `cover_dct` is the DCT of the ORIGINAL cover image. It is required because
    embedding stored z = x + alpha*f(y); recovering y means undoing the `+ x`.
    This makes the scheme non-blind: the receiver needs the original cover.
    """
    big_h, big_w, big_d = embedded_dct.shape

    extracted_dct = np.zeros((small_h, small_w, big_d))

    for ch in range(big_d):
        extracted_dct[:, :, ch] = extract_2d(
            embedded_dct[:, :, ch], cover_dct[:, :, ch], small_h, small_w, config
        )

    return extracted_dct


def extract_2d(embedded_dct_channel, cover_dct_channel, small_h, small_w, config):
    big_h, big_w = embedded_dct_channel.shape
    extracted_dct = np.zeros((small_h, small_w))

    stride_h = big_h // small_h
    stride_w = big_w // small_w

    for sx in range(small_h):
        for sy in range(small_w):
            #position in big image
            bx, by = target_position(sx, sy, stride_h, stride_w, config['method'])
            val = embedded_dct_channel[bx, by]
            extracted_val = decrypt(
                val,
                cover_dct_channel[bx, by],
                config['alpha'],
                config['p'],
                config['q'],
                config['encrypt']
            )
            extracted_dct[sx, sy] = extracted_val
    return extracted_dct


def main():
    embedded_img_path = 'img_embed/embedded_result_11.png' # and 12
    cover_img_path = 'img_256/img1.png'  # the ORIGINAL cover used by sender.py

    # Create output directory if it doesn't exist
    os.makedirs('img_extracted', exist_ok=True)

    # Read embedded image and original big image
    embedded_img = cv2.imread(embedded_img_path)
    print(f"Embedded image loaded from '{embedded_img_path}'")

    cover_img = cv2.imread(cover_img_path)
    print(f"Cover image loaded from '{cover_img_path}'")

    # Load configuration
    with open('config.json', 'r') as f:
        config = json.load(f)
    print("Configuration loaded.")

    # Apply DCT to both embedded and original images
    embedded_dct = dct_3d_fast(embedded_img)
    cover_dct = dct_3d_fast(cover_img)
    print("DCT applied to embedded and cover images.")

    # Extract the small image DCT
    # Ratio between cover and hidden image (8x by default)
    big_h, big_w, _ = embedded_img.shape
    ratio = config.get('ratio', 8)
    small_h = big_h // ratio
    small_w = big_w // ratio

    extracted_dct = extract_3d(embedded_dct, cover_dct, small_h, small_w, config)
    print(f"Extraction process completed. Extracted size: {small_h}x{small_w}")
    print(f"Extracted DCT range: [{extracted_dct.min():.2f}, {extracted_dct.max():.2f}]")
    
    # Apply inverse DCT to get the image back
    extracted_img = idct_3d_fast(extracted_dct)
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
