import sklearn
from sklearn.cluster import KMeans
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

def whole(image,k):
    comp_img=bit_compressor(k,image)
    return comp_img
def pixelate(res,scale=3):
    res = cv.resize(res, (res.shape[1]//scale,res.shape[0]//scale), interpolation=cv.INTER_LINEAR)
    # Upscale back to original size (pixelated)
    res= cv.resize(res, (res.shape[1]*scale,res.shape[0]*scale), interpolation=cv.INTER_NEAREST)
    return res
  

def main(input_path,output_path, k, scale):    
    orig = cv.imread(input_path)
    res=orig
    res=whole(res,k)
    # res= cv.bilateralFilter(res,d=9,sigmaColor=100,sigmaSpace=75)
    res=pixelate(res,scale) 
    cv.imwrite(output_path,res)
    print(f"Final image stored at {output_path}")