import numpy as np

def extraer_canal(img, tipo='rojo'):
    img = img[:, :, :3]
    if img.dtype != np.uint8:
        img = (img * 255).astype(np.uint8)
    
    salida = np.copy(img)
    tipo = tipo.lower()
    
    if tipo in ['rojo', 'r']:
        salida[:, :, 1] = 0
        salida[:, :, 2] = 0
    elif tipo in ['verde', 'g']:
        salida[:, :, 0] = 0
        salida[:, :, 2] = 0
    elif tipo in ['azul', 'b']:
        salida[:, :, 0] = 0
        salida[:, :, 1] = 0
    elif tipo in ['cian', 'c']:
        salida[:, :, 0] = 0
    elif tipo in ['magenta', 'm']:
        salida[:, :, 1] = 0
    elif tipo in ['amarillo', 'y']:
        salida[:, :, 2] = 0
        
    return salida

def mosaico_canales(img, modo='rgb'):
    img = img[:, :, :3]
    if img.dtype != np.uint8:
        img = (img * 255).astype(np.uint8)
    
    if modo == 'cmy':
        c1 = extraer_canal(img, 'cian')
        c2 = extraer_canal(img, 'magenta')
        c3 = extraer_canal(img, 'amarillo')
    else:
        c1 = extraer_canal(img, 'rojo')
        c2 = extraer_canal(img, 'verde')
        c3 = extraer_canal(img, 'azul')
        
    fila_sup = np.hstack([img, c1])
    fila_inf = np.hstack([c2, c3])
    mosaico = np.vstack([fila_sup, fila_inf])
    return mosaico
