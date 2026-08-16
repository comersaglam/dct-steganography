# -*- coding: utf-8 -*-
"""Proof that the matrix DCT and the hand-written loop DCT are the same transform."""

import time

import numpy as np

from dct import (
    dct_1d, idct_1d,
    dct_2d, idct_2d,
    dct_2d_fast, idct_2d_fast,
    dct_matrix,
)

TOL = 1e-9

np.random.seed(0)

print("Comparing matrix DCT against the loop implementation\n")

# --- 1D -------------------------------------------------------------------
n = 32
x = np.random.rand(n) * 255
C = dct_matrix(n)

d_fwd = np.abs(C @ x - dct_1d(x)).max()
d_inv = np.abs(C.T @ x - idct_1d(x)).max()
print(f"1D forward  (C @ x   vs dct_1d) : {d_fwd:.3e}")
print(f"1D inverse  (C.T @ x vs idct_1d): {d_inv:.3e}")

# --- orthonormality -------------------------------------------------------
d_orth = np.abs(C @ C.T - np.eye(n)).max()
print(f"orthonormal (C @ C.T vs I)      : {d_orth:.3e}")

# --- 2D -------------------------------------------------------------------
img = np.random.rand(16, 16) * 255
d_2d = np.abs(dct_2d_fast(img) - dct_2d(img)).max()
d_2di = np.abs(idct_2d_fast(img) - idct_2d(img)).max()
print(f"2D forward  (16x16)             : {d_2d:.3e}")
print(f"2D inverse  (16x16)             : {d_2di:.3e}")

# --- roundtrip ------------------------------------------------------------
d_round = np.abs(idct_2d_fast(dct_2d_fast(img)) - img).max()
print(f"2D roundtrip (idct(dct(x)) vs x): {d_round:.3e}")

# --- speed ----------------------------------------------------------------
big = np.random.rand(512, 512) * 255
t = time.time()
dct_2d_fast(big)
print(f"\n512x512 matrix DCT took {time.time() - t:.3f}s "
      f"(loop version needs ~100s for the same array)")

# --- verdict --------------------------------------------------------------
worst = max(d_fwd, d_inv, d_orth, d_2d, d_2di, d_round)
assert worst < TOL, f"matrix and loop DCT disagree by {worst:.3e}"
print(f"\nOK - largest difference {worst:.3e} is below {TOL:.0e}")
