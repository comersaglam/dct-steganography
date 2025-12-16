# -*- coding: utf-8 -*-

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