import cv2
import numpy as np
import base64

def decode_base64_image(data_url):
    # data_url is like "data:image/png;base64,..."
    header, encoded = data_url.split(",", 1)
    data = base64.b64decode(encoded)
    arr = np.frombuffer(data, np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    return img

def extract_facelet_colors(img):
    """
    img: BGR numpy image (cv2)
    returns: list of 9 average BGR colors in row-major order
    Simple approach: compute 3x3 grid around image center and sample small squares.
    """
    h, w = img.shape[:2]
    cx, cy = w // 2, h // 2
    cell = min(w, h) // 6   # approximate cell spacing
    offsets = [-cell, 0, cell]  # relative x/y for 3x3
    colors = []
    sample_radius = max(3, cell // 6)

    for ry in offsets:
        for rx in offsets:
            x = int(cx + rx)
            y = int(cy + ry)
            x1, x2 = max(0, x - sample_radius), min(w, x + sample_radius)
            y1, y2 = max(0, y - sample_radius), min(h, y + sample_radius)
            patch = img[y1:y2, x1:x2]
            if patch.size == 0:
                avg = np.array([0,0,0], dtype=np.uint8)
            else:
                avg = patch.mean(axis=(0,1)).astype(np.uint8)
            colors.append(avg)  # BGR
    return colors
