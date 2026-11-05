import numpy as np

def aplicar_gris_luminosidad(img):
    img = img[:, :, :3]
    if img.dtype != np.uint8:
        img = (img * 255).astype(np.uint8)
    img_float = img.astype(np.float32)
    gris = 0.299 * img_float[:, :, 0] + 0.587 * img_float[:, :, 1] + 0.114 * img_float[:, :, 2]
    gris = np.clip(gris, 0, 255).astype(np.uint8)
    return np.stack([gris, gris, gris], axis=2)
