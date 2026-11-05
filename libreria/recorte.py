import numpy as np

def aplicar_recorte(img, x1, y1, x2, y2):
    img = img[:, :, :3]
    if img.dtype != np.uint8:
        img = (img * 255).astype(np.uint8)
        
    alto, ancho = img.shape[:2]
    x1 = max(0, min(int(x1), ancho - 1))
    x2 = max(x1 + 1, min(int(x2), ancho))
    y1 = max(0, min(int(y1), alto - 1))
    y2 = max(y1 + 1, min(int(y2), alto))
    
    recorte = img[y1:y2, x1:x2]
    return recorte
