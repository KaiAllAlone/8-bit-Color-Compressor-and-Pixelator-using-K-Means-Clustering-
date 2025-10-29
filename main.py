import sklearn
from sklearn.cluster import KMeans
import numpy as np
import cv2 as cv
import tempfile
from PIL import Image, ImageOps

# -------------------------------
# Helper Functions
# -------------------------------

def convert_to_supported_format(file):
    """Converts HEIC or unsupported formats to JPEG."""
    img = Image.open(file)
    temp_jpeg = tempfile.NamedTemporaryFile(delete=False, suffix=".jpeg")
    rgb_img = img.convert("RGB")
    rgb_img.save(temp_jpeg.name, "JPEG")
    return temp_jpeg.name

def fix_orientation(path):
    """Fix EXIF orientation from phone cameras."""
    try:
        img = Image.open(path)
        img = ImageOps.exif_transpose(img)
        img.save(path)
    except Exception:
        pass  # Skip if no EXIF data

def resize_if_large(path, max_dim=2000):
    """Resizes image if it's too large (to prevent memory issues)."""
    img = cv.imread(path)
    if img is None:
        return
    h, w = img.shape[:2]
    if max(h, w) > max_dim:
        scale = max_dim / max(h, w)
        img = cv.resize(img, (int(w * scale), int(h * scale)))
        cv.imwrite(path, img)

# -------------------------------
# Core Compression Logic
# -------------------------------

def bit_compressor(k, image):
    h, w, c = image.shape
    flat_img = image.reshape((-1, 3))  # RGB pixels
    vals = np.float32(flat_img)

    kmeans = KMeans(n_clusters=k, random_state=0, n_init=10)
    labels = kmeans.fit_predict(vals)
    centers = np.uint8(kmeans.cluster_centers_)

    compressed_flat = centers[labels]
    compressed_img = compressed_flat.reshape((h, w, 3))
    return compressed_img

def pixelate(res, scale=3):
    res = cv.resize(res, (res.shape[1] // scale, res.shape[0] // scale), interpolation=cv.INTER_LINEAR)
    res = cv.resize(res, (res.shape[1] * scale, res.shape[0] * scale), interpolation=cv.INTER_NEAREST)
    return res

def whole(image, k):
    return bit_compressor(k, image)

def main(input_path, output_path, k, scale):
    fix_orientation(input_path)
    resize_if_large(input_path)

    orig = cv.imread(input_path)
    if orig is None:
        raise ValueError("Could not read input image — possibly unsupported format.")

    res = whole(orig, k)
    res = pixelate(res, scale)
    cv.imwrite(output_path, res)
    print(f"Final image stored at {output_path}")
