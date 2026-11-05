import numpy as np
from PIL import Image

def fusionar_o_sumar(img1, img2, tipo='promedio', alfa=0.5):
    img1 = img1[:, :, :3]
    img2 = img2[:, :, :3]
    if img1.dtype != np.uint8:
        img1 = (img1 * 255).astype(np.uint8)
    if img2.dtype != np.uint8:
        img2 = (img2 * 255).astype(np.uint8)
        
    alto, ancho = img1.shape[:2]
    img2_pil = Image.fromarray(img2).resize((ancho, alto))
    img2_redim = np.array(img2_pil)
    
    if tipo == 'ponderada':
        A = img1.astype(np.float32)
        B = img2_redim.astype(np.float32)
        fusion = alfa * A + (1.0 - alfa) * B
        return np.clip(fusion, 0, 255).astype(np.uint8)
    else:
        A = img1.astype(np.int16)
        B = img2_redim.astype(np.int16)
        fusion = (A + B) / 2
        return np.clip(fusion, 0, 255).astype(np.uint8)
