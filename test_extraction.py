import numpy as np
import cv2
from dct import *
import json

# Load config
with open('config.json', 'r') as f:
    config = json.load(f)

# Load original small image that was embedded
small_img = cv2.imread('img_32/img2.png')
print(f"Original small image shape: {small_img.shape}")
print(f"Original small image range: [{small_img.min()}, {small_img.max()}]")

# Apply DCT
small_dct = dct_3d(small_img)
print(f"Small DCT range: [{small_dct.min():.2f}, {small_dct.max():.2f}]")

# Check what happens when we embed
sample_small_val = small_dct[0, 0, 0]
embedded_val = config['alpha'] * sample_small_val
print(f"\nSample small DCT value: {sample_small_val:.2f}")
print(f"After embedding (alpha * y): {embedded_val:.2f}")
print(f"After extraction (z / alpha): {embedded_val / config['alpha']:.2f}")

# Now test the full round trip
reconstructed_dct = small_dct / config['alpha'] * config['alpha']
print(f"\nReconstructed DCT range: [{reconstructed_dct.min():.2f}, {reconstructed_dct.max():.2f}]")

reconstructed_img = idct_3d(reconstructed_dct)
print(f"Reconstructed image range: [{reconstructed_img.min():.2f}, {reconstructed_img.max():.2f}]")
