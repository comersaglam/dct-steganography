# -*- coding: utf-8 -*-
"""Demo run used for the README figure: hide img_128/img2 inside img_1024/img1."""

import os
import time

import cv2
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from dct import dct_3d, idct_3d, dct_3d_fast, idct_3d_fast
from embed import embed_3d, target_position
from receiver import extract_3d

HERE = os.path.dirname(os.path.abspath(__file__))

# --- configuration --------------------------------------------------------
BIG_SIZE = 1024
SMALL_SIZE = 128          # BIG_SIZE // 8

COVER = f"img_{BIG_SIZE}/img1.png"
HIDDEN = f"img_{SMALL_SIZE}/img2.png"

ALPHA = 0.25              # balance between cover quality and secret quality
METHOD = "high_freq"      # 'center' or 'high_freq'

# Matrix DCT is ~1000x faster and provably identical (see test_matrix_dct.py).
USE_FAST_DCT = True

CONFIG = {
    "alpha": ALPHA,
    "p": 3,
    "q": 5,
    "encrypt": False,
    "method": METHOD,
}

forward = dct_3d_fast if USE_FAST_DCT else dct_3d
inverse = idct_3d_fast if USE_FAST_DCT else idct_3d


def norm_for_display(arr):
    """Scale an arbitrary float array into a viewable 0-255 image."""
    lo, hi = arr.min(), arr.max()
    if hi - lo < 1e-12:
        return np.zeros_like(arr, dtype=np.uint8)
    return np.clip((arr - lo) / (hi - lo) * 255, 0, 255).astype(np.uint8)


def dct_for_display(arr):
    """DCT coefficients span a huge range, so show them on a log scale."""
    return norm_for_display(np.log1p(np.abs(arr)))


def bgr(img):
    return cv2.cvtColor(np.clip(img, 0, 255).astype(np.uint8), cv2.COLOR_BGR2RGB)


def main():
    cover = cv2.imread(os.path.join(HERE, COVER))
    hidden = cv2.imread(os.path.join(HERE, HIDDEN))
    if cover is None or hidden is None:
        raise SystemExit(f"Missing {COVER} or {HIDDEN}")

    print(f"cover  {COVER}  {cover.shape}")
    print(f"hidden {HIDDEN}  {hidden.shape}")
    print(f"alpha={ALPHA}  method={METHOD}  fast_dct={USE_FAST_DCT}\n")

    t0 = time.time()

    # --- embed ------------------------------------------------------------
    cover_dct = forward(cover)
    hidden_dct = forward(hidden)
    embedded_dct = embed_3d(cover_dct, hidden_dct, CONFIG)
    stego_float = inverse(embedded_dct)

    # This is what actually gets transmitted: 8-bit pixels, not floats.
    stego = np.clip(np.rint(stego_float), 0, 255).astype(np.uint8)

    # --- extract ----------------------------------------------------------
    # Non-blind: the receiver re-derives the cover DCT to undo the "+ x" term.
    stego_dct = forward(stego.astype(float))
    extracted_dct = extract_3d(stego_dct, cover_dct, SMALL_SIZE, SMALL_SIZE, CONFIG)
    recovered = inverse(extracted_dct)
    print(f"done in {time.time() - t0:.2f}s\n")

    # --- metrics ----------------------------------------------------------
    cover_err = np.abs(stego.astype(float) - cover.astype(float))
    hidden_err = np.abs(np.clip(recovered, 0, 255) - hidden.astype(float))
    mse = (cover_err ** 2).mean()
    psnr = 10 * np.log10(255.0 ** 2 / mse) if mse > 0 else float("inf")

    print("Cover distortion:")
    print(f"  mean {cover_err.mean():.2f}   max {cover_err.max():.2f}   PSNR {psnr:.2f} dB")
    print("Recovered hidden image:")
    print(f"  mean {hidden_err.mean():.2f}   max {hidden_err.max():.2f}")

    # Regression check. The old code computed z/alpha instead of (z-x)/alpha,
    # i.e. it never subtracted the cover coefficient. Since we already have the
    # correct result, adding x/alpha back reproduces the buggy output.
    stride = BIG_SIZE // SMALL_SIZE
    cover_at_targets = np.zeros_like(extracted_dct)
    for sx in range(SMALL_SIZE):
        for sy in range(SMALL_SIZE):
            bx, by = target_position(sx, sy, stride, stride, METHOD)
            cover_at_targets[sx, sy, :] = cover_dct[bx, by, :]

    buggy = inverse(extracted_dct + cover_at_targets / ALPHA)
    buggy_err = np.abs(np.clip(buggy, 0, 255) - hidden.astype(float)).mean()
    print("\nEffect of the decrypt() fix:")
    print(f"  old 'z/alpha'       -> mean error {buggy_err:.2f}")
    print(f"  fixed '(z-x)/alpha' -> mean error {hidden_err.mean():.2f}")

    # --- 3x3 figure -------------------------------------------------------
    fig, axes = plt.subplots(3, 3, figsize=(15, 15))

    panels = [
        (bgr(cover), f"1. Cover ({BIG_SIZE}x{BIG_SIZE})"),
        (bgr(hidden), f"2. Hidden image ({SMALL_SIZE}x{SMALL_SIZE})"),
        (dct_for_display(hidden_dct), "3. DCT of hidden image"),
        (dct_for_display(cover_dct), "4. DCT of cover"),
        (dct_for_display(embedded_dct), f"5. Embedded DCT (alpha={ALPHA}, {METHOD})"),
        (bgr(stego), f"6. Stego image\n(PSNR {psnr:.1f} dB, mean err {cover_err.mean():.2f})"),
        (dct_for_display(stego_dct), "7. Re-DCT of stego"),
        (dct_for_display(extracted_dct), "8. Extracted DCT"),
        (bgr(recovered), f"9. Recovered hidden image\n(mean err {hidden_err.mean():.2f})"),
    ]

    for ax, (img, title) in zip(axes.flat, panels):
        ax.imshow(img)
        ax.set_title(title, fontsize=11)
        ax.axis("off")

    plt.tight_layout()

    docs_dir = os.path.join(HERE, "docs")
    os.makedirs(docs_dir, exist_ok=True)
    fig_path = os.path.join(docs_dir, "pipeline.png")
    plt.savefig(fig_path, dpi=110, bbox_inches="tight")
    plt.close(fig)

    print(f"\nFigure saved to {fig_path}")


if __name__ == "__main__":
    main()
