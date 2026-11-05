import numpy as np

def aplicar_reduccion(img, factor=2):
    img = img[:, :, :3]
    if img.dtype != np.uint8:
        img = (img * 255).astype(np.uint8)
        
    factor = max(1, int(round(factor)))
    reducida = img[::factor, ::factor]
    return reducida
