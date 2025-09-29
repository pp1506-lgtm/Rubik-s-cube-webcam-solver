import numpy as np
import cv2
import kociemba

# order expected by kociemba: U, R, F, D, L, B (each 9 stickers)
ORDER = ['U','R','F','D','L','B']

def color_dist(a, b):
    # robust distance: convert to Lab and compute Euclidean
    a_lab = cv2.cvtColor(np.uint8([[a]]), cv2.COLOR_BGR2LAB)[0,0].astype(int)
    b_lab = cv2.cvtColor(np.uint8([[b]]), cv2.COLOR_BGR2LAB)[0,0].astype(int)
    return np.linalg.norm(a_lab - b_lab)

def build_cube_string(scanned, centers):
    # scanned: face -> list of 9 BGR arrays; centers: face -> center BGR
    # For each sticker, find nearest center color and append its face letter.
    cube_chars = []
    for face in ORDER:
        stickers = scanned[face]  # 9 samples
        for s in stickers:
            # find closest center (min distance)
            best = None
            bestd = float('inf')
            for face2, c in centers.items():
                d = color_dist(s, c)
                if d < bestd:
                    bestd = d; best = face2
            cube_chars.append(best)
    return ''.join(cube_chars)

def try_solve_cube(scanned, centers):
    cube_string = build_cube_string(scanned, centers)
    try:
        solution = kociemba.solve(cube_string)
    except Exception as e:
        solution = f"error: {e}; cube_string={cube_string}"
    return solution
