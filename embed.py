import numpy as np

def encrypt(x, y, alpha, p, q, encrypt_flag):
    #* x + alpha f(y) = z where fy = y^p mod q
    #* Without encryption we still keep the cover coefficient x, otherwise the
    #* cover value is thrown away and the stego image is visibly damaged.
    if not encrypt_flag:
        return x + alpha * y
    fy = pow(y, p, q)
    z = x + alpha * fy
    return z

def decrypt(z, x, alpha, p, q, encrypt_flag):
    #* f(y) = (z - x) / alpha  => y = (f(y))^(p^-1 mod q-1) mod q
    #* `x` is the original cover coefficient. It MUST be subtracted: embedding
    #* stored z = x + alpha*f(y), so dividing z by alpha alone leaks x/alpha
    #* into the result and swamps the hidden value (worse as alpha shrinks).
    if not encrypt_flag:
        return (z - x) / alpha
    fy = (z - x) / alpha
    # Compute modular inverse of p mod (q-1)
    p_inv = pow(p, -1, q - 1)
    y = pow(int(fy), p_inv, q)
    return y

def target_position(sx, sy, stride_h, stride_w, method):
    """Where coefficient (sx, sy) of the small image lands in the big DCT.

    Shared by embedding and extraction so the two can never drift apart.
    """
    if method == 'center':
        return sx * stride_h + stride_h // 2, sy * stride_w + stride_w // 2
    if method == 'high_freq':
        return (sx + 1) * stride_h - 1, (sy + 1) * stride_w - 1
    raise ValueError(f"unknown embedding method: {method!r} (use 'center' or 'high_freq')")


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
            bx, by = target_position(sx, sy, stride_h, stride_w, config['method'])
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