# IMG Transformer - Computación Gráfica (Nota 2)

Aplicación web desarrollada con Flask para la visualización y aplicación de transformaciones de imágenes en tiempo real.
*Computación gráfica taller procesamiento digital imágenes*

## 1. Estructura Modular del Proyecto

El proyecto está organizado de forma modular, cumpliendo el requisito de tener un archivo independiente por cada transformación dentro del paquete `libreria/`:

```text
IMG_Transformer/
├── app.py                      # Servidor backend en Flask
├── requirements.txt            # Dependencias del proyecto
├── vercel.json                 # Configuración de despliegue en Vercel
├── api/
│   └── index.py                # Punto de entrada para Serverless Vercel
├── imagenes_de_muestra/        # Imágenes de prueba del curso (mariposa, ghost, mario, etc.)
├── libreria/                   # Librería propia modular
│   ├── __init__.py             # Exportación centralizada de funciones
│   ├── negativo.py             # Inversión de color (255 - img)
│   ├── brillo.py               # Ajuste general de brillo con np.clip
│   ├── brillo_canal.py         # Brillo por canal independiente (R, G, B)
│   ├── gris_promedio.py        # Escala de grises por promedio (R+G+B)/3
│   ├── gris_midgray.py         # Escala de grises tonalidad media (Max+Min)/2
│   ├── gris_luminosidad.py     # Escala de grises ponderada por luminosidad
│   ├── umbralizacion.py        # Binarización con umbral ajustable
│   ├── canales_rgb_cmy.py      # Separación y mosaicos de capas RGB y CMY
│   ├── suma_imagenes.py        # Fusión promedio y ponderada con alfa
│   ├── histograma.py           # Histograma comparativo de 4 paneles (R, G, B, Gris)
│   ├── recorte.py              # Recorte mediante slicing matricial
│   ├── zoom.py                 # Ampliación por duplicación de píxeles
│   ├── reduccion.py            # Reducción por submuestreo de paso
│   └── rotacion.py             # Rotación 90°, 180° y 270° (cv2.rotate)
├── static/
│   ├── css/
│   │   └── style.css           # Estilos de interfaz tipo iLoveIMG
│   └── js/
│       └── main.js             # Lógica interactiva cliente y AJAX
└── templates/
    └── index.html              # Plantilla HTML principal
```

## 2. Requisitos e Instalación

Para ejecutar localmente:

1. Instalar dependencias:
```bash
pip install -r requirements.txt
```

2. Iniciar el servidor:
```bash
python app.py
```

3. Abrir en el navegador:
```text
http://127.0.0.1:5000
```

## 3. Funcionalidades de la Interfaz

- **Carga de imágenes:** Soporte para archivos `.jpg`, `.png` y `.jpeg` mediante selector o arrastrando el archivo (drag & drop), además de acceso rápido a las imágenes de prueba del taller (`mariposa.jpg`, `ghost.png`, etc.).
- **Visualización comparativa:** Panel dual que muestra simultáneamente la imagen original y el resultado procesado, junto a sus dimensiones y tipo de dato (`uint8`).
- **Controles interactivos:** Sliders libres para intensidad de brillo, umbral, factor de zoom, factor de reducción y alfa de ponderación.
- **Suma de dos imágenes:** Permite subir una segunda imagen o utilizar la imagen predeterminada para realizar fusión promedio o ponderada.
- **Descarga:** Botón directo para descargar en la computadora el resultado transformado en formato PNG.
