import numpy as np

def aplicar_zoom(img, factor=2):
    img = img[:, :, :3]
    if img.dtype != np.uint8:
        img = (img * 255).astype(np.uint8)
        
    factor = max(1, int(round(factor)))
    zoom = np.repeat(np.repeat(img, factor, axis=0), factor, axis=1)
    return zoom
