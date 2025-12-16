# dct-steganography
An attempt to embed images inside of bigger images as an encryption mechanism. Implementation of DCT and IDCT by hand an a simple embedding mechanism that can be improved in the future.


# DCT-Based Steganography

A Python implementation of steganography using Discrete Cosine Transform (DCT) to hide images within other images.

## Features

- 3D DCT implementation (optimized with C++ extension)
- Multiple embedding methods (center, high_freq, scattered, zigzag, frequency_weighted)
- Configurable alpha parameter for embedding strength
- Optional encryption using modular exponentiation
- Sender/Receiver pipeline for embedding and extraction

## Installation

1. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/dct-steganography.git
cd dct-steganography
```

2. Create virtual environment:
```bash
python -m venv .env
source .env/bin/activate  # On Windows: .env\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Build C++ extension (optional, for faster DCT):
```bash
python setup.py build_ext --inplace
```

## Usage

### Quick Test

```python
python test.py
```

This will:
- Load a 128x128 big image and 16x16 small image
- Embed the small image into the big image using DCT
- Extract and verify the embedded image
- Save results to `test_X/` directory

### Embed an Image

```python
python sender.py
```

### Extract an Image

```python
python receiver.py
```

## Configuration

Edit `config.json` to adjust parameters:

```json
{
    "alpha": 0.1,
    "p": 3,
    "q": 5,
    "encrypt": false,
    "method": "center"
}
```

- **alpha**: Embedding strength (0.01-0.5)
- **method**: Embedding strategy (`center`, `high_freq`, `scattered`, `zigzag`, `frequency_weighted`)
- **encrypt**: Enable modular exponentiation encryption

## Project Structure

```
steganography/
├── dct.py              # Pure Python DCT implementation
├── dct_cpp.cpp         # C++ optimized DCT (optional)
├── embed.py            # Embedding functions
├── receiver.py         # Extraction functions
├── sender.py           # Main embedding script
├── test.py             # Testing and visualization
├── resize.py           # Image preprocessing
└── config.json         # Configuration file
```

## Results

| Alpha | Method | Mean Error | Visual Quality |
|-------|--------|------------|----------------|
| 0.1   | center | 2.5        | Excellent      |
| 0.01  | scattered | 15.3    | Good           |

## License

MIT
