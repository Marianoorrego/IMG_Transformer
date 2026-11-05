import numpy as np

def aplicar_umbralizacion(img, umbral=128):
    img = img[:, :, :3]
    if img.dtype != np.uint8:
        img = (img * 255).astype(np.uint8)
    img_float = img.astype(np.float32)
    gris = (img_float[:, :, 0] + img_float[:, :, 1] + img_float[:, :, 2]) / 3
    binaria = (gris >= umbral).astype(np.uint8) * 255
    return np.stack([binaria, binaria, binaria], axis=2)
