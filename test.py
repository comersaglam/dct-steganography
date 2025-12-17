"""
test.py - DCT Steganography Testing and Visualization Suite

This script performs a complete round-trip test of the steganography pipeline:
1. Embedding a small image into a big image
2. Extracting the hidden image back
3. Comparing original and extracted images
4. Generating comprehensive visualizations

Output:
    Creates a test_N directory with:
        - complete_pipeline.png: 3x3 visualization grid showing all steps
        - Individual images at each pipeline stage
        - config.txt: Test parameters used
        - Error statistics

Configuration:
    Adjust parameters at the top of main section:
        - small_img_size: Size of hidden image (8, 16, 32, etc.)
        - big_img_size: Size of cover image (typically 8x small_img_size)
        - alpha: Embedding strength (0.001-0.5)
        - method: 'center' or 'high_freq'

Usage:
    python test.py
    
Visualization Grid (3x3):
    Row 1: Original big image | Original small image | Small DCT
    Row 2: Big DCT | Embedded DCT | Reconstructed big image  
    Row 3: Re-DCT | Extracted DCT | Extracted small image (with error)

Performance Notes:
    - Small alpha (<0.01) may cause high errors due to quantization
    - Larger images accumulate more error
    - High-frequency embedding is more robust but more visible
"""

import numpy as np
import cv2
from dct import *
from embed import *
from receiver import *

def print_image(img):
    """
    Print a subset of image values to console for debugging.
    
    Args:
        img (np.ndarray): Image array with shape (H, W, C)
    
    Prints:
        Green channel values in a formatted grid
    """
    height, width, channels = img.shape
    channel_names = ['B', 'G', 'R'] if channels == 3 else [f'Ch{i}' for i in range(channels)]
    
    for c in range(1, channels):
        if c > 1:
            break
        print(f"\n{channel_names[c]} Channel:")
        print("-" * (width * 8))
        for h in range(height):
            row = " ".join([f"{img[h, w, c]:6.1f}" for w in range(width)])
            print(row)
    print()
    

# Define image sizes
small_img_size = 16
alpha = 0.001
method = 'center'  # 'center' or 'high_freq'
big_img_size = 8*small_img_size

# Use the sizes in paths
test_img_path = f"img_{big_img_size}/img2.png"
test_img = cv2.imread(test_img_path)

test_img_2x2_path = f"img_{small_img_size}/img1.png"
test_img_2x2 = cv2.imread(test_img_2x2_path)

dct_test = dct_3d(test_img)
dct_s = dct_3d(test_img_2x2)

embedded_img = embed_3d(dct_test, dct_s, {
    'alpha': alpha,
    'p': 3,
    'q': 5,
    'encrypt': False,
    'method': method
})

reconstructed_test = idct_3d(embedded_img)

# extraction test - use small_img_size
img_embed = dct_3d(reconstructed_test)
extracted_dct = extract_3d(img_embed, small_img_size, small_img_size, {
    'alpha': alpha,
    'p': 3,
    'q': 5,
    'encrypt': False,
    'method': method
})

print("\n\n\n\nxxxxxxxxxxxxxx\n\n\n\n")
reconstructed_small = idct_3d(extracted_dct)

error = np.abs(test_img_2x2.astype(np.float32) - reconstructed_small.astype(np.float32))
print("Reconstruction error statistics:")
print(f"Min error: {error.min():.2f}")
print(f"Max error: {error.max():.2f}")
print(f"Mean error: {error.mean():.2f}")


testnum= 0
output_dir = "test"
while os.path.exists(f"{output_dir}_{testnum}"):
    testnum += 1
output_dir = f"{output_dir}_{testnum}"
os.makedirs(output_dir)

# plot every image in a single figure
import matplotlib.pyplot as plt

fig, axes = plt.subplots(3, 3, figsize=(15, 15))

# Row 1: Original images - use sizes in titles
axes[0, 0].imshow(cv2.cvtColor(test_img, cv2.COLOR_BGR2RGB))
axes[0, 0].set_title(f'Original Big Image ({big_img_size}x{big_img_size})')
axes[0, 0].axis('off')

axes[0, 1].imshow(cv2.cvtColor(test_img_2x2, cv2.COLOR_BGR2RGB))
axes[0, 1].set_title(f'Original Small Image ({small_img_size}x{small_img_size})')
axes[0, 1].axis('off')

axes[0, 2].imshow(np.clip((dct_s - dct_s.min()) / (dct_s.max() - dct_s.min()) * 255, 0, 255).astype(np.uint8))
axes[0, 2].set_title('Small DCT')
axes[0, 2].axis('off')

# Row 2: Embedding process
axes[1, 0].imshow(np.clip((dct_test - dct_test.min()) / (dct_test.max() - dct_test.min()) * 255, 0, 255).astype(np.uint8))
axes[1, 0].set_title('Big DCT')
axes[1, 0].axis('off')

axes[1, 1].imshow(np.clip((embedded_img - embedded_img.min()) / (embedded_img.max() - embedded_img.min()) * 255, 0, 255).astype(np.uint8))
axes[1, 1].set_title('Embedded DCT')
axes[1, 1].axis('off')

axes[1, 2].imshow(cv2.cvtColor(np.clip(reconstructed_test, 0, 255).astype(np.uint8), cv2.COLOR_BGR2RGB))
axes[1, 2].set_title('Reconstructed Big Image')
axes[1, 2].axis('off')

# Row 3: Extraction process
axes[2, 0].imshow(np.clip((img_embed - img_embed.min()) / (img_embed.max() - img_embed.min()) * 255, 0, 255).astype(np.uint8))
axes[2, 0].set_title('Re-DCT of Reconstructed')
axes[2, 0].axis('off')

axes[2, 1].imshow(np.clip((extracted_dct - extracted_dct.min()) / (extracted_dct.max() - extracted_dct.min()) * 255, 0, 255).astype(np.uint8))
axes[2, 1].set_title('Extracted DCT')
axes[2, 1].axis('off')

axes[2, 2].imshow(cv2.cvtColor(np.clip(reconstructed_small, 0, 255).astype(np.uint8), cv2.COLOR_BGR2RGB))
axes[2, 2].set_title(f'Extracted Small Image\n(Error: {error.mean():.2f})')
axes[2, 2].axis('off')

plt.tight_layout()
plt.savefig(os.path.join(output_dir, "complete_pipeline.png"), dpi=150, bbox_inches='tight')
plt.show()



#print every image in the process
cv2.imwrite(os.path.join(output_dir, "test_img.png"), test_img)
cv2.imwrite(os.path.join(output_dir, "dct_test.png"), np.clip((dct_test - dct_test.min()) / (dct_test.max() - dct_test.min()) * 255, 0, 255).astype(np.uint8))
cv2.imwrite(os.path.join(output_dir, "embedded_img.png"), np.clip((embedded_img - embedded_img.min()) / (embedded_img.max() - embedded_img.min()) * 255, 0, 255).astype(np.uint8))
cv2.imwrite(os.path.join(output_dir, "reconstructed_test.png"), np.clip(reconstructed_test, 0, 255).astype(np.uint8))
cv2.imwrite(os.path.join(output_dir, "img_embed.png"), np.clip((img_embed - img_embed.min()) / (img_embed.max() - img_embed.min()) * 255, 0, 255).astype(np.uint8))
cv2.imwrite(os.path.join(output_dir, "extracted_dct.png"), np.clip((extracted_dct - extracted_dct.min()) / (extracted_dct.max() - extracted_dct.min()) * 255, 0, 255).astype(np.uint8))
cv2.imwrite(os.path.join(output_dir, "reconstructed_small.png"), np.clip(reconstructed_small, 0, 255).astype(np.uint8))
print(f"All intermediate images saved in '{output_dir}' directory.")
print(f"Test configuration: Big={big_img_size}x{big_img_size}, Small={small_img_size}x{small_img_size}")

#write config file as txt
with open(os.path.join(output_dir, "config.txt"), 'w') as f:
    f.write(f"small_img_size: {small_img_size}\n")
    f.write(f"alpha: {alpha}\n")
    f.write(f"method: {method}\n")