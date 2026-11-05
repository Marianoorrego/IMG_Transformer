import numpy as np

def aplicar_brillo_canal(img, canal='R', valor=50):
    img = img[:, :, :3]
    if img.dtype != np.uint8:
        img = (img * 255).astype(np.uint8)
    
    res = np.copy(img).astype(np.int16)
    idx = 0
    if canal in ['G', 'verde', 'Verde', 1]:
        idx = 1
    elif canal in ['B', 'azul', 'Azul', 2]:
        idx = 2
        
    res[:, :, idx] = np.clip(res[:, :, idx] + valor, 0, 255)
    return res.astype(np.uint8)
