#include <iostream>
#include <vector>
#include <cmath>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#define PI 3.14159265358979323846

namespace py = pybind11;

// Function to calculate 1D DCT
std::vector<double> dct_1d(const std::vector<double>& image) {
    size_t n = image.size();
    std::vector<double> newImage(n, 0.0);

    for (size_t k = 0; k < n; ++k) {
        double sum = 0;
        for (size_t i = 0; i < n; ++i) {
            sum += image[i] * cos(2 * PI * k / (2.0 * n) * i + (k * PI) / (2.0 * n));
        }
        double ck = (k == 0) ? sqrt(0.5) : 1.0;
        newImage[k] = sqrt(2.0 / n) * ck * sum;
    }

    return newImage;
}

// Function to apply 2D DCT (row-wise and then column-wise)
std::vector<std::vector<double>> dct_2d(const std::vector<std::vector<double>>& image) {
    size_t height = image.size();
    size_t width = image[0].size();
    std::vector<std::vector<double>> imageRow(height, std::vector<double>(width, 0.0));
    std::vector<std::vector<double>> imageCol(height, std::vector<double>(width, 0.0));

    // Apply 1D DCT on rows
    for (size_t h = 0; h < height; ++h) {
        imageRow[h] = dct_1d(image[h]);
    }

    // Apply 1D DCT on columns
    for (size_t w = 0; w < width; ++w) {
        std::vector<double> col(height, 0.0);
        for (size_t h = 0; h < height; ++h) {
            col[h] = imageRow[h][w];
        }
        std::vector<double> dct_col = dct_1d(col);
        for (size_t h = 0; h < height; ++h) {
            imageCol[h][w] = dct_col[h];
        }
    }

    return imageCol;
}

// Function to apply 3D DCT by applying 2D DCT on each slice
std::vector<std::vector<std::vector<double>>> dct_3d(const std::vector<std::vector<std::vector<double>>>& image) {
    size_t depth = image[0][0].size();
    size_t height = image.size();
    size_t width = image[0].size();
    
    std::vector<std::vector<std::vector<double>>> dct_slices(depth, std::vector<std::vector<double>>(height, std::vector<double>(width, 0.0)));
    
    for (size_t d = 0; d < depth; ++d) {
        std::vector<std::vector<double>> slice(height, std::vector<double>(width, 0.0));
        for (size_t h = 0; h < height; ++h) {
            for (size_t w = 0; w < width; ++w) {
                slice[h][w] = image[h][w][d];
            }
        }
        dct_slices[d] = dct_2d(slice);
    }

    return dct_slices;
}

// Function to calculate 1D Inverse DCT
std::vector<double> idct_1d(const std::vector<double>& image) {
    size_t n = image.size();
    std::vector<double> newImage(n, 0.0);

    for (size_t i = 0; i < n; ++i) {
        double sum = 0;
        for (size_t k = 0; k < n; ++k) {
            double ck = (k == 0) ? sqrt(0.5) : 1.0;
            sum += ck * image[k] * cos(2 * PI * k / (2.0 * n) * i + (k * PI) / (2.0 * n));
        }
        newImage[i] = sqrt(2.0 / n) * sum;
    }

    return newImage;
}

// Function to apply 2D Inverse DCT (row-wise and then column-wise)
std::vector<std::vector<double>> idct_2d(const std::vector<std::vector<double>>& image) {
    size_t height = image.size();
    size_t width = image[0].size();
    std::vector<std::vector<double>> imageRow(height, std::vector<double>(width, 0.0));
    std::vector<std::vector<double>> imageCol(height, std::vector<double>(width, 0.0));

    // Apply 1D IDCT on rows
    for (size_t h = 0; h < height; ++h) {
        imageRow[h] = idct_1d(image[h]);
    }

    // Apply 1D IDCT on columns
    for (size_t w = 0; w < width; ++w) {
        std::vector<double> col(height, 0.0);
        for (size_t h = 0; h < height; ++h) {
            col[h] = imageRow[h][w];
        }
        std::vector<double> idct_col = idct_1d(col);
        for (size_t h = 0; h < height; ++h) {
            imageCol[h][w] = idct_col[h];
        }
    }

    return imageCol;
}

// Function to apply 3D Inverse DCT by applying 2D Inverse DCT on each slice
std::vector<std::vector<std::vector<double>>> idct_3d(const std::vector<std::vector<std::vector<double>>>& image) {
    size_t depth = image[0][0].size();
    size_t height = image.size();
    size_t width = image[0].size();

    std::vector<std::vector<std::vector<double>>> idct_slices(depth, std::vector<std::vector<double>>(height, std::vector<double>(width, 0.0)));

    for (size_t d = 0; d < depth; ++d) {
        std::vector<std::vector<double>> slice(height, std::vector<double>(width, 0.0));
        for (size_t h = 0; h < height; ++h) {
            for (size_t w = 0; w < width; ++w) {
                slice[h][w] = image[h][w][d];
            }
        }
        idct_slices[d] = idct_2d(slice);
    }

    return idct_slices;
}

// Pybind11 Module
PYBIND11_MODULE(dct_cpp, m) {
    m.doc() = "C++ DCT implementation for steganography";
    
    m.def("dct_1d", &dct_1d, "Compute 1D Discrete Cosine Transform",
          py::arg("image"));
    m.def("dct_2d", &dct_2d, "Compute 2D Discrete Cosine Transform",
          py::arg("image"));
    m.def("dct_3d", &dct_3d, "Compute 3D Discrete Cosine Transform",
          py::arg("image"));
    m.def("idct_1d", &idct_1d, "Compute 1D Inverse Discrete Cosine Transform",
          py::arg("image"));
    m.def("idct_2d", &idct_2d, "Compute 2D Inverse Discrete Cosine Transform",
          py::arg("image"));
    m.def("idct_3d", &idct_3d, "Compute 3D Inverse Discrete Cosine Transform",
          py::arg("image"));
}