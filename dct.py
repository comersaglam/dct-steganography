"""
dct.py - Discrete Cosine Transform (DCT) Implementation

This module provides pure Python implementations of 1D, 2D, and 3D DCT and their inverses.
DCT is used to transform images from spatial domain to frequency domain for steganography.

Mathematical Background:
    DCT transforms spatial pixel values into frequency coefficients, where:
    - Low frequencies (top-left) represent smooth variations
    - High frequencies (bottom-right) represent sharp edges/details
    
    The DCT is orthogonal and reversible (IDCT reconstructs original image).

Formula (1D DCT):
    X[k] = sqrt(2/N) * c[k] * Σ(x[n] * cos((2n+1)kπ / 2N))
    where c[k] = 1/sqrt(2) for k=0, else 1

Performance:
    This is a reference implementation. For large images, consider using:
    - dct_cpp.cpp (C++ optimized version with pybind11)
    - scipy.fftpack.dct (native NumPy/SciPy)

Usage:
    from dct import dct_3d, idct_3d
    dct_coeffs = dct_3d(image)  # Forward transform
    reconstructed = idct_3d(dct_coeffs)  # Inverse transform
"""

# -*- coding: utf-8 -*-

from math import cos, pi, sqrt
import numpy as np


def dct_3d(image):
    """
    3D DCT by applying 2D DCT on each slice along the third dimension.
    
    Args:
        image (np.ndarray): Input image, shape (H, W, C) where C is number of channels
    
    Returns:
        np.ndarray: DCT coefficients, shape (H, W, C)
    
    Process:
        For RGB images (C=3), applies 2D DCT independently to each color channel.
        This preserves color information while transforming spatial frequencies.
    """
    depth = image.shape[2]
    dct_slices = []
    
    for d in range(depth):
        print(f"Processing slice {d+1}/{depth}...")
        dct_slice = dct_2d(image[:, :, d])
        dct_slices.append(dct_slice)
    
    return np.stack(dct_slices, axis=2)


def dct_2d(image):
    """
    2D DCT without coefficient truncation.
    
    Args:
        image (np.ndarray): 2D input array, shape (H, W)
    
    Returns:
        np.ndarray: 2D DCT coefficients, shape (H, W)
    
    Algorithm:
        1. Apply 1D DCT to each row (transforms horizontal frequencies)
        2. Apply 1D DCT to each column of result (transforms vertical frequencies)
        
    Result:
        - Top-left: DC component (average intensity)
        - Edges: Low frequencies (smooth gradients)
        - Corners: High frequencies (edges, noise)
    """
    height = image.shape[0]
    width = image.shape[1]
def dct_1d(image):
    """
    1D DCT without coefficient truncation.
    
    Args:
        image (np.ndarray): 1D input array, shape (N,)
    
    Returns:
        np.ndarray: 1D DCT coefficients, shape (N,)
    
    Formula:
        X[k] = sqrt(2/N) * c[k] * Σ(x[n] * cos((2πk / 2N) * n + kπ / 2N))
        where c[k] = sqrt(0.5) for k=0, else 1
    
    Properties:
        - Energy compaction: Most energy concentrates in low-frequency coefficients
        - Orthogonal: DCT basis functions are orthogonal
        - Real-valued: No complex numbers (unlike DFT)
    """t)

    print(f"Applying 2D DCT...")
    for h in range(height):
        if h % 50 == 0:
            print(f" Processing row {h+1}/{height}...")
        imageRow[h, :] = dct_1d(image[h, :])
    
    for w in range(width):
        if w % 50 == 0:
            print(f" Processing column {w+1}/{width}...")
        imageCol[:, w] = dct_1d(imageRow[:, w])

def idct_3d(image):
    """
    3D Inverse DCT by applying 2D Inverse DCT on each slice.
    
    Args:
        image (np.ndarray): DCT coefficients, shape (H, W, C)
    
    Returns:
        np.ndarray: Reconstructed spatial domain image, shape (H, W, C)
    
    Note:
        Applies IDCT independently to each color channel.
def idct_2d(image):
    """
    2D Inverse DCT - reconstructs spatial domain from frequency domain.
    
    Args:
        image (np.ndarray): 2D DCT coefficients, shape (H, W)
    
    Returns:
        np.ndarray: Reconstructed 2D spatial image, shape (H, W)
    
    Algorithm:
        1. Apply 1D IDCT to each row
        2. Apply 1D IDCT to each column of result
        
    Properties:
        - Exact inverse of dct_2d (within numerical precision)
        - Reconstruction error typically < 1e-10
    """

def dct_1d(image):
    """1D DCT without coefficient truncation"""
def idct_1d(image):
    """
    1D Inverse DCT - reconstructs spatial signal from frequency coefficients.
    
    Args:
        image (np.ndarray): 1D DCT coefficients, shape (N,)
    
    Returns:
        np.ndarray: Reconstructed 1D spatial signal, shape (N,)
    
    Formula:
        x[n] = sqrt(2/N) * Σ(c[k] * X[k] * cos((2πk / 2N) * n + kπ / 2N))
        where c[k] = sqrt(0.5) for k=0, else 1
    
    Relationship:
        idct_1d(dct_1d(x)) ≈ x (exact within floating-point precision)
    """like(image).astype(float)
  
    for k in range(n):
        sum = 0
        for i in range(n):
            sum += image[i] * cos(2 * pi * k / (2.0 * n) * i + (k * pi) / (2.0 * n))
        ck = sqrt(0.5) if k == 0 else 1
        newImage[k] = sqrt(2.0 / n) * ck * sum

    return newImage

def idct_3d(image):
    """3D Inverse DCT by applying 2D Inverse DCT on each slice along the third dimension"""
    depth = image.shape[2]
    idct_slices = []
    
    for d in range(depth):
        print(f"Processing slice {d+1}/{depth}...")
        idct_slice = idct_2d(image[:, :, d])
        idct_slices.append(idct_slice)
    
    return np.stack(idct_slices, axis=2)

def idct_2d(image):
    """2D Inverse DCT"""
    height = image.shape[0]
    width = image.shape[1]
    imageRow = np.zeros_like(image).astype(float)
    imageCol = np.zeros_like(image).astype(float)
    
    print(f"Applying 2D Inverse DCT...")
    for h in range(height):
        if h % 50 == 0:
            print(f" Processing row {h+1}/{height}...")
        imageRow[h, :] = idct_1d(image[h, :])
    
    for w in range(width):
        if w % 50 == 0:
            print(f" Processing column {w+1}/{width}...")
        imageCol[:, w] = idct_1d(imageRow[:, w])

    return imageCol


def idct_1d(image):
    """1D Inverse DCT"""
    n = len(image)
    newImage = np.zeros_like(image).astype(float)

    for i in range(n):
        sum = 0
        for k in range(n):
            ck = sqrt(0.5) if k == 0 else 1
            sum += ck * image[k] * cos(2 * pi * k / (2.0 * n) * i + (k * pi) / (2.0 * n))
        newImage[i] = sqrt(2.0 / n) * sum

    return newImage