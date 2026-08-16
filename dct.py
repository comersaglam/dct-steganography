# -*- coding: utf-8 -*-

from functools import lru_cache
from math import cos, pi, sqrt
import numpy as np


def dct_3d(image):
    """3D DCT by applying 2D DCT on each slice along the third dimension"""
    depth = image.shape[2]
    dct_slices = []
    
    for d in range(depth):
        print(f"Processing slice {d+1}/{depth}...")
        dct_slice = dct_2d(image[:, :, d])
        dct_slices.append(dct_slice)
    
    return np.stack(dct_slices, axis=2)


def dct_2d(image):
    """2D DCT without coefficient truncation"""
    height = image.shape[0]
    width = image.shape[1]
    imageRow = np.zeros_like(image).astype(float)
    imageCol = np.zeros_like(image).astype(float)

    print(f"Applying 2D DCT...")
    for h in range(height):
        if h % 50 == 0:
            print(f" Processing row {h+1}/{height}...")
        imageRow[h, :] = dct_1d(image[h, :])
    
    for w in range(width):
        if w % 50 == 0:
            print(f" Processing column {w+1}/{width}...")
        imageCol[:, w] = dct_1d(imageRow[:, w])

    return imageCol


def dct_1d(image):
    """1D DCT without coefficient truncation"""
    n = len(image)
    newImage = np.zeros_like(image).astype(float)
  
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


# ---------------------------------------------------------------------------
# Matrix (numpy) versions of the exact same transform.
#
# The loops above compute, for every output index k:
#     X[k] = sqrt(2/n) * ck * sum_i x[i] * cos(2*pi*k/(2n)*i + k*pi/(2n))
#
# That sum is a matrix-vector product, so building the coefficient matrix C
# once and multiplying is the same maths written differently -- no library
# transform (scipy/fftpack) is used, the cosine formula is still ours.
#
#     C[k, i] = sqrt(2/n) * ck * cos(2*pi*k/(2n)*i + k*pi/(2n))
#     1D DCT:   X = C @ x           1D IDCT:  x = C.T @ X
#     2D DCT:   X = C @ img @ C.T   2D IDCT:  img = C.T @ X @ C
#
# C is orthonormal (C @ C.T == I), which is why the inverse is the transpose.
# Verified against the loop versions to ~1e-12; see test_matrix_dct.py.
# ---------------------------------------------------------------------------


@lru_cache(maxsize=None)
def dct_matrix(n):
    """n x n DCT matrix built from the same formula used in dct_1d."""
    k = np.arange(n)[:, None]  # row index -> frequency
    i = np.arange(n)[None, :]  # column index -> sample
    C = np.sqrt(2.0 / n) * np.cos(2 * np.pi * k / (2.0 * n) * i + (k * np.pi) / (2.0 * n))
    C[0, :] *= np.sqrt(0.5)  # the ck term, which is sqrt(0.5) only for k == 0
    return C


def dct_2d_fast(image):
    """2D DCT via matrix multiplication. Same result as dct_2d, much faster."""
    image = np.asarray(image, dtype=float)
    C_rows = dct_matrix(image.shape[0])
    C_cols = dct_matrix(image.shape[1])
    return C_rows @ image @ C_cols.T


def idct_2d_fast(image):
    """2D Inverse DCT via matrix multiplication. Same result as idct_2d."""
    image = np.asarray(image, dtype=float)
    C_rows = dct_matrix(image.shape[0])
    C_cols = dct_matrix(image.shape[1])
    return C_rows.T @ image @ C_cols


def dct_3d_fast(image):
    """3D DCT (per channel) via matrix multiplication. Same result as dct_3d."""
    image = np.asarray(image, dtype=float)
    return np.stack([dct_2d_fast(image[:, :, d]) for d in range(image.shape[2])], axis=2)


def idct_3d_fast(image):
    """3D Inverse DCT (per channel) via matrix multiplication."""
    image = np.asarray(image, dtype=float)
    return np.stack([idct_2d_fast(image[:, :, d]) for d in range(image.shape[2])], axis=2)