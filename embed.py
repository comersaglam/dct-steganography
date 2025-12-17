"""
embed.py - DCT Steganography Embedding Functions

This module implements the core embedding logic for hiding a small image within a larger image
using Discrete Cosine Transform (DCT) coefficients.

Key Concepts:
    - Embedding occurs in the frequency domain (DCT coefficients)
    - Small DCT coefficients are distributed across big image DCT using stride-based positioning
    - Optional modular exponentiation encryption for security
    - Alpha parameter controls embedding strength

Embedding Formula:
    Without encryption: z = alpha * y
    With encryption: z = x + alpha * (y^p mod q)
    
    Where:
        x = big image DCT coefficient
        y = small image DCT coefficient  
        z = embedded (combined) coefficient
        alpha = embedding strength parameter
        p, q = encryption parameters
"""

import numpy as np

def encrypt(x, y, alpha, p, q, encrypt_flag):
    """
    Embed a small image DCT coefficient into a big image DCT coefficient.
    
    Args:
        x (float): Big image DCT coefficient
        y (float): Small image DCT coefficient to embed
        alpha (float): Embedding strength (typical range: 0.01-0.5)
        p (int): Encryption exponent
        q (int): Encryption modulus
        encrypt_flag (bool): Whether to use modular exponentiation encryption
    
    Returns:
        float: Combined/embedded DCT coefficient
    
    Formula:
        - Without encryption: z = alpha * y
        - With encryption: z = x + alpha * (y^p mod q)
    """
    #* x + alpha f(y) = z where fy = y^p mod q
    if not encrypt_flag:
        return alpha * y
    fy = pow(y, p, q)
    z = x + alpha * fy
    return z

def decrypt(z, alpha, p, q, encrypt_flag):
    """
    Extract the hidden small image DCT coefficient from an embedded coefficient.
    
    Args:
        z (float): Embedded DCT coefficient
        alpha (float): Embedding strength used during embedding
        p (int): Encryption exponent
        q (int): Encryption modulus
        encrypt_flag (bool): Whether encryption was used during embedding
def embed_3d(big_dct, small_dct, config):
    """
    Embed a 3D small image DCT into a 3D big image DCT (processes all color channels).
    
    Args:
        big_dct (np.ndarray): Big image DCT coefficients, shape (H, W, C)
        small_dct (np.ndarray): Small image DCT coefficients, shape (h, w, C)
        config (dict): Configuration containing:
            - alpha: embedding strength
            - p, q: encryption parameters
            - encrypt: encryption flag
def embed_2d(big_dct_channel, small_dct_channel, config):
    """
    Embed small DCT into big DCT for a single channel using stride-based positioning.
    
    Args:
        big_dct_channel (np.ndarray): Big image DCT for one channel, shape (H, W)
        small_dct_channel (np.ndarray): Small image DCT for one channel, shape (h, w)
        config (dict): Configuration dictionary
    
    Returns:
        np.ndarray: Combined DCT with embedded coefficients, shape (H, W)
    
    Embedding Strategy:
        - Divides big DCT into a grid based on small DCT dimensions
        - Stride = big_dimension / small_dimension
        - Places each small coefficient at a specific position within its corresponding block:
            * 'center': middle of each block (stride_h // 2, stride_w // 2)
            * 'high_freq': high-frequency corner (stride_h - 1, stride_w - 1)
    
    Example:
        Small: 32x32, Big: 256x256
        Stride: 8x8
        Each small coefficient embeds into one of 1024 blocks (32x32 grid of 8x8 blocks)
    """ Applies embed_2d independently to each color channel (B, G, R).
    """
        float: Extracted small image DCT coefficient
    
    Formula:
        - Without encryption: y = z / alpha
        - With encryption: y = ((z - x) / alpha)^(p^-1 mod (q-1)) mod q
    """
    #* f(y) = (z - x) / alpha  => y = (f(y))^(p^-1 mod q-1) mod q
    if not encrypt_flag:
        return z / alpha
    fy = (z) / alpha
    # Compute modular inverse of p mod (q-1)
    p_inv = pow(p, -1, q - 1)
    y = pow(int(fy), p_inv, q)
    return y

def embed_3d(big_dct, small_dct, config):
    """Embed small DCT into big DCT based on configuration"""
    big_h, big_w, big_d = big_dct.shape
    small_h, small_w, small_d = small_dct.shape
    
    comb_dct = big_dct.copy()
    for ch in range(big_d):
        comb_dct[:, :, ch] = embed_2d(big_dct[:, :, ch], small_dct[:, :, ch], config)
    
    return comb_dct

def embed_2d(big_dct_channel, small_dct_channel, config):
    """
    Embed small DCT into big DCT by distributing coefficients evenly.
    Small: 128x128 → 16x16 blocks
    Big: 1024x1024 → 128x128 blocks
    Stride: 128/16 = 8 (place small coefficients every 8 blocks)
    """
    big_h, big_w = big_dct_channel.shape
    small_h, small_w = small_dct_channel.shape
    comb_dct = big_dct_channel.copy()

    stride_h = big_h // small_h
    stride_w = big_w // small_w

    for sx in range(small_h):
        for sy in range(small_w):
            #position in big image
            if config['method'] == 'center':
                bx = sx * stride_h + stride_h // 2
                by = sy * stride_w + stride_w // 2
            elif config['method'] == 'high_freq':
                bx = (sx + 1) * stride_h - 1
                by = (sy + 1) * stride_w - 1
            val = encrypt(
                big_dct_channel[bx, by],
                small_dct_channel[sx, sy],
                config['alpha'],
                config['p'],
                config['q'],
                config['encrypt']
            )
            comb_dct[bx, by] = val
    
    return comb_dct