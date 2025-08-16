import sklearn
from sklearn.cluster import KMeans
import pandas as pd
import numpy as np
import cv2 as cv
import sys
import os
path = r'Programs\Python\pine-watt-2Hzmz15wGik-unsplash.jpg'
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

def dithering_rgb(img):
    img = img.astype(np.float32) / 255
    height, width, channels = img.shape
    out = np.copy(img)
    for y in range(height):
        for x in range(width):
            for c in range(channels):
                old_pixel = out[y, x, c]
                new_pixel = 1.0 if old_pixel > 0.5 else 0.0
                out[y, x, c] = new_pixel
                error = old_pixel - new_pixel
                for dx, dy, factor in [(1, 0, 0.5), (0, 1, 0.25), (1, 1, 0.25)]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < width and 0 <= ny < height:
                        out[ny, nx, c] += error * factor
                        
    return (np.clip(out, 0, 1) * 255).astype(np.uint8)

def whole(image,k=32):
    comp_img=bit_compressor(k,image)
    return comp_img
def pixelate(res,scale):
    res = cv.resize(res, (res.shape[1]//scale,res.shape[0]//scale), interpolation=cv.INTER_LINEAR)
    # Upscale back to original size (pixelated)
    res= cv.resize(res, (res.shape[1]*scale,res.shape[0]*scale), interpolation=cv.INTER_NEAREST)
    return res
  
  
if __name__ == "__main__":
    
    print(f"Attempting to read image from:{os.path.abspath(path)}")
    orig = cv.imread(path)
    if orig is None:
        print(f"Error: Could not read image at {path}")
        sys.exit(1)
    print(f"Successfully read image with shape: {orig.shape}")
    # Save and show original
    cv.imwrite('Original.png',orig)
    cv.imshow('Original',orig)
    print("Processing image...")
    # Using separate channel compression for better quality
    # res=whole(path)
    res=orig
    # res=dithering_rgb(res)
    res=whole(res,32)
    res= cv.bilateralFilter(res,d=9,sigmaColor=100,sigmaSpace=75)
    res=pixelate(res,3)
    if res is None:
        print("Error: Could not read compressed result")
        sys.exit(1)  
    cv.imwrite('Compressed.png',res)
    print(f"Compressed image shape:{res.shape}")
    # Post-processing
    # res = cv.dilate(res,(3,3))
    # res = cv.erode(res,(3,3))
    # Save and show result
    cv.imshow('Result',res)
    print("Press any key to close the windows...")
    cv.waitKey(0)
    cv.destroyAllWindows()