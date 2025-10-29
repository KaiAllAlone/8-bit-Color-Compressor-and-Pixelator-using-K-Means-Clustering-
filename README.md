# Color Compressor using K-Means Clustering

This project implements an **color compression tool** in Python using **K-Means clustering** for color quantization, plus optional post-processing like **pixelation** and **bilateral smoothing**. It reduces the number of colors in an image while preserving key visual structure.

---

## 📌 Features

* **K-Means-based color quantization** → Clusters pixel colors and replaces each pixel with its cluster centroid.
* **Pixelation option** → Downscale + upscale to create a pixel-art effect.
* **Bilateral filtering** → Edge-preserving smoothing to reduce quantization noise.
* Saves and displays both original and compressed images.
---

## 📂 File Structure

* `image_compressor.py` → Main script containing compression logic.

---

## ⚙️ Installation

Clone the repository and install required dependencies:

```bash
git clone https://github.com/your-username/image-compressor.git
cd image-compressor
pip install -r requirements.txt
```

### Requirements

```
numpy
pandas
opencv-python
scikit-learn
```

---

## ▶️ Usage

Run the script directly:

```bash
python image_compressor.py
```

NOTE:-The script reads the image from the hardcoded `path` variable inside the file. Update `path` with your input image location.

### Example:

```python
path = r"Programs\\Python\\pine-watt-2Hzmz15wGik-unsplash.jpg"
```

If you are running in a headless environment (no GUI), comment out the `cv.imshow(...)` lines and rely on the saved files (`Original.png`, `Compressed.png`).

**OR**

Run the Web Application
@

<a href="https://eight-bit-color-compressor-and-pixelator.onrender.com"> Image Pixelator </a>

---

## 🔧 Configuration Highlights

* **Number of colors (`k`)**: set in `whole(image, k=32)`.
* **Pixelation scale**: set in `pixelate(res, scale)`; larger `scale` ⇒ chunkier pixels.
* **Bilateral filter**: `cv.bilateralFilter(res, d=9, sigmaColor=100, sigmaSpace=75)` controls smoothing strength.

---

## 📖 How It Works

1. **Read Input Image**
   Loads the image using OpenCV from the provided `path`.

2. **Color Quantization with K-Means**

   * Reshape the image to a list of RGB pixels.
   * Run `KMeans(n_clusters=k, random_state=0, n_init=10)` from scikit-learn.
   * Replace each pixel with its cluster centroid to form the compressed image.

3. **Pixelation (Optional)**

   * Downscale the image and then upscale it using nearest-neighbor to produce a blocky, retro look.

4. **Post-Processing**

   * Apply **bilateral filtering** to smooth color banding while preserving edges.
   * Save outputs as `Original.png` and `Compressed.png`.

5. **Display**

   * Show both images in OpenCV windows (if a GUI is available).

---

## 🧩 Example Workflow

* Load original image → K-Means compression (`k=8`) → Bilateral filter → Pixelate → Save/Display results.

---

## ✅ Future Improvements

* **Add dithering** (e.g., Floyd–Steinberg, ordered dithering) with proper tuning to reduce banding.
* Command-line arguments for path, `k`, pixelation scale, and filter strengths.
* Batch processing of multiple images and output directories.
* Alternative color spaces (Lab/HSV) for perceptually better quantization.
* Export options (e.g., JPEG/WebP quality settings).
* Performance: vectorization, streaming for large images, or GPU acceleration.
* Make a deplyable Website using this( WIP)

---

## 📝 License

This project is open-source and available under the **MIT License**.

P.S :- Tried implementing dithering but it wasn't producing the wanted retro-style effects so later removed it. 
