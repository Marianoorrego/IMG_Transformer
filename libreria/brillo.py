import numpy as np

def aplicar_brillo(img, valor=50):
    img = img[:, :, :3]
    if img.dtype != np.uint8:
        img = (img * 255).astype(np.uint8)
    img_int = img.astype(np.int16)
    resultado = np.clip(img_int + valor, 0, 255).astype(np.uint8)
    return resultado
