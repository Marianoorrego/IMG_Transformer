import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
from PIL import Image

def generar_histograma(img):
    img = img[:, :, :3]
    if img.dtype != np.uint8:
        img = (img * 255).astype(np.uint8)
        
    r = img[:, :, 0].ravel()
    g = img[:, :, 1].ravel()
    b = img[:, :, 2].ravel()
    gris = ((img[:, :, 0].astype(np.float32) + img[:, :, 1] + img[:, :, 2]) / 3).astype(np.uint8).ravel()

    fig, axes = plt.subplots(2, 2, figsize=(8, 6))
    
    axes[0, 0].hist(r, bins=256, color='red', alpha=0.7, range=(0, 256))
    axes[0, 0].set_title("Canal Rojo")
    axes[0, 0].set_xlim([0, 256])
    
    axes[0, 1].hist(g, bins=256, color='green', alpha=0.7, range=(0, 256))
    axes[0, 1].set_title("Canal Verde")
    axes[0, 1].set_xlim([0, 256])
    
    axes[1, 0].hist(b, bins=256, color='blue', alpha=0.7, range=(0, 256))
    axes[1, 0].set_title("Canal Azul")
    axes[1, 0].set_xlim([0, 256])
    
    axes[1, 1].hist(gris, bins=256, color='gray', alpha=0.7, range=(0, 256))
    axes[1, 1].set_title("Escala de Grises")
    axes[1, 1].set_xlim([0, 256])
    
    plt.tight_layout()
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=100)
    plt.close(fig)
    buf.seek(0)
    
    img_hist = Image.open(buf)
    return np.array(img_hist)[:, :, :3]
