import numpy as np

def aplicar_gris_promedio(img):
    img = img[:, :, :3]
    if img.dtype != np.uint8:
        img = (img * 255).astype(np.uint8)
    img_float = img.astype(np.float32)
    gris = (img_float[:, :, 0] + img_float[:, :, 1] + img_float[:, :, 2]) / 3
    gris = np.clip(gris, 0, 255).astype(np.uint8)
    return np.stack([gris, gris, gris], axis=2)
