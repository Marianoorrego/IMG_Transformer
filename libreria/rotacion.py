import cv2
import numpy as np

def aplicar_rotacion(img, angulo=90):
    img = img[:, :, :3]
    if img.dtype != np.uint8:
        img = (img * 255).astype(np.uint8)
        
    angulo = int(angulo)
    if angulo == 90:
        return cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
    elif angulo == 180:
        return cv2.rotate(img, cv2.ROTATE_180)
    elif angulo == 270:
        return cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
    else:
        return img
