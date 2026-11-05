import numpy as np

def aplicar_negativo(img):
    img = img[:, :, :3]
    if img.dtype != np.uint8:
        img = (img * 255).astype(np.uint8)
    inv = 255 - img
    return inv
