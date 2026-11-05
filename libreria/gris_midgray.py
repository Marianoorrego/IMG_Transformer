import numpy as np

def aplicar_gris_midgray(img):
    img = img[:, :, :3]
    if img.dtype != np.uint8:
        img = (img * 255).astype(np.uint8)
    img_float = img.astype(np.float32)
    maximo = np.max(img_float, axis=2)
    minimo = np.min(img_float, axis=2)
    gris = (maximo + minimo) / 2
    gris = np.clip(gris, 0, 255).astype(np.uint8)
    return np.stack([gris, gris, gris], axis=2)
