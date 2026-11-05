import os
import io
import base64
import numpy as np
from PIL import Image
from flask import Flask, render_template, request, jsonify, send_file

# En Vercel el disco es de solo lectura; matplotlib necesita una carpeta escribible para su cache
os.environ.setdefault('MPLCONFIGDIR', '/tmp/matplotlib')

import libreria

CARPETA_ACTUAL = os.path.dirname(os.path.abspath(__file__))
DIR_TEMPLATES = os.path.join(CARPETA_ACTUAL, 'templates')
# Los estilos y scripts van en public/static: en Vercel se sirven directo desde el CDN
# y en local Flask los sirve desde la misma carpeta bajo la ruta /static
DIR_STATIC = os.path.join(CARPETA_ACTUAL, 'public', 'static')

app = Flask(__name__, template_folder=DIR_TEMPLATES, static_folder=DIR_STATIC, static_url_path='/static')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

def obtener_ruta_muestra(nombre):
    posibles_carpetas = [
        os.path.join(CARPETA_ACTUAL, 'imagenes_de_muestra'),
        os.path.join(CARPETA_ACTUAL, 'imágenes de muestra'),
        CARPETA_ACTUAL
    ]
    for carpeta in posibles_carpetas:
        ruta = os.path.join(carpeta, nombre)
        if os.path.exists(ruta):
            return ruta
    return None

# Variables de estado en memoria para la sesion actual
ESTADO = {
    'img_original': None,
    'img_actual': None,
    'nombre_archivo': 'imagen.png',
    'img_segunda': None,
    'nombre_segunda': 'segunda.png'
}

def array_a_base64(arr):
    if arr is None:
        return None
    if arr.dtype != np.uint8:
        arr = np.clip(arr, 0, 255).astype(np.uint8)
    if arr.ndim == 2:
        pil_img = Image.fromarray(arr, mode='L')
    else:
        pil_img = Image.fromarray(arr[:, :, :3], mode='RGB')
    
    buffer = io.BytesIO()
    pil_img.save(buffer, format='PNG')
    buffer.seek(0)
    b64_str = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return f"data:image/png;base64,{b64_str}"

def cargar_imagen_desde_bytes(archivo_bytes):
    pil_img = Image.open(io.BytesIO(archivo_bytes)).convert('RGB')
    return np.array(pil_img, dtype=np.uint8)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/muestras', methods=['GET'])
def listar_muestras():
    archivos_ejemplo = ['mariposa.jpg', 'ghost.png', 'mario_imagen.png', 'pixel_art.png', 'diferentesobjetos.jpeg']
    disponibles = []
    for nombre in archivos_ejemplo:
        if obtener_ruta_muestra(nombre):
            disponibles.append(nombre)
    return jsonify({'muestras': disponibles})

@app.route('/api/cargar-muestra', methods=['POST'])
def cargar_muestra():
    data = request.get_json() or {}
    nombre = data.get('nombre', 'mariposa.jpg')
    es_segunda = data.get('es_segunda', False)
    
    ruta = obtener_ruta_muestra(nombre)
    if not ruta:
        return jsonify({'error': 'Archivo no encontrado'}), 404
        
    pil_img = Image.open(ruta).convert('RGB')
    arr = np.array(pil_img, dtype=np.uint8)
    
    if es_segunda:
        ESTADO['img_segunda'] = arr
        ESTADO['nombre_segunda'] = nombre
        return jsonify({
            'success': True,
            'nombre': nombre,
            'base64': array_a_base64(arr),
            'alto': arr.shape[0],
            'ancho': arr.shape[1]
        })
    else:
        ESTADO['img_original'] = arr
        ESTADO['img_actual'] = arr
        ESTADO['nombre_archivo'] = nombre
        return jsonify({
            'success': True,
            'nombre': nombre,
            'base64': array_a_base64(arr),
            'alto': arr.shape[0],
            'ancho': arr.shape[1],
            'canales': arr.shape[2] if arr.ndim > 2 else 1,
            'dtype': str(arr.dtype)
        })

@app.route('/api/subir', methods=['POST'])
def subir_imagen():
    if 'archivo' not in request.files:
        return jsonify({'error': 'No se encontro archivo en la peticion'}), 400
        
    archivo = request.files['archivo']
    if archivo.filename == '':
        return jsonify({'error': 'Archivo sin nombre'}), 400
        
    es_segunda = request.form.get('es_segunda', 'false').lower() == 'true'
    
    bytes_img = archivo.read()
    arr = cargar_imagen_desde_bytes(bytes_img)
    
    if es_segunda:
        ESTADO['img_segunda'] = arr
        ESTADO['nombre_segunda'] = archivo.filename
        return jsonify({
            'success': True,
            'nombre': archivo.filename,
            'base64': array_a_base64(arr),
            'alto': arr.shape[0],
            'ancho': arr.shape[1]
        })
    else:
        ESTADO['img_original'] = arr
        ESTADO['img_actual'] = arr
        ESTADO['nombre_archivo'] = archivo.filename
        return jsonify({
            'success': True,
            'nombre': archivo.filename,
            'base64': array_a_base64(arr),
            'alto': arr.shape[0],
            'ancho': arr.shape[1],
            'canales': arr.shape[2] if arr.ndim > 2 else 1,
            'dtype': str(arr.dtype)
        })

@app.route('/api/transformar', methods=['POST'])
def transformar():
    if ESTADO['img_original'] is None:
        return jsonify({'error': 'No hay imagen cargada'}), 400
        
    data = request.get_json() or {}
    op = data.get('operacion')
    params = data.get('params', {})
    
    img = np.copy(ESTADO['img_original'])
    resultado = None
    
    try:
        if op == 'negativo':
            resultado = libreria.aplicar_negativo(img)
            
        elif op == 'brillo':
            val = int(params.get('valor', 50))
            resultado = libreria.aplicar_brillo(img, val)
            
        elif op == 'brillo_canal':
            canal = params.get('canal', 'R')
            val = int(params.get('valor', 50))
            resultado = libreria.aplicar_brillo_canal(img, canal, val)
            
        elif op == 'gris_promedio':
            resultado = libreria.aplicar_gris_promedio(img)
            
        elif op == 'gris_midgray':
            resultado = libreria.aplicar_gris_midgray(img)
            
        elif op == 'gris_luminosidad':
            resultado = libreria.aplicar_gris_luminosidad(img)
            
        elif op == 'umbralizacion':
            umbral = int(params.get('umbral', 128))
            resultado = libreria.aplicar_umbralizacion(img, umbral)
            
        elif op == 'canales_rgb_cmy':
            modo = params.get('modo', 'mosaico_rgb')
            if modo == 'mosaico_rgb':
                resultado = libreria.mosaico_canales(img, 'rgb')
            elif modo == 'mosaico_cmy':
                resultado = libreria.mosaico_canales(img, 'cmy')
            else:
                resultado = libreria.extraer_canal(img, modo)
                
        elif op == 'suma_imagenes':
            if ESTADO['img_segunda'] is None:
                # Cargar ghost.png por defecto si no ha seleccionado la segunda
                ruta_defecto = obtener_ruta_muestra('ghost.png')
                if ruta_defecto and os.path.exists(ruta_defecto):
                    ESTADO['img_segunda'] = np.array(Image.open(ruta_defecto).convert('RGB'))
                else:
                    ESTADO['img_segunda'] = np.copy(img)
                    
            tipo = params.get('tipo', 'promedio')
            alfa = float(params.get('alfa', 0.5))
            resultado = libreria.fusionar_o_sumar(img, ESTADO['img_segunda'], tipo=tipo, alfa=alfa)
            
        elif op == 'histograma':
            resultado = libreria.generar_histograma(img)
            
        elif op == 'recorte':
            x1 = int(params.get('x1', 0))
            y1 = int(params.get('y1', 0))
            x2 = int(params.get('x2', img.shape[1]))
            y2 = int(params.get('y2', img.shape[0]))
            resultado = libreria.aplicar_recorte(img, x1, y1, x2, y2)
            
        elif op == 'zoom':
            factor = float(params.get('factor', 2))
            resultado = libreria.aplicar_zoom(img, factor)
            
        elif op == 'reduccion':
            factor = float(params.get('factor', 2))
            resultado = libreria.aplicar_reduccion(img, factor)
            
        elif op == 'rotacion':
            angulo = int(params.get('angulo', 90))
            resultado = libreria.aplicar_rotacion(img, angulo)
            
        else:
            return jsonify({'error': f'Operacion desconocida: {op}'}), 400
            
        ESTADO['img_actual'] = resultado
        
        return jsonify({
            'success': True,
            'base64': array_a_base64(resultado),
            'alto': resultado.shape[0],
            'ancho': resultado.shape[1],
            'canales': resultado.shape[2] if resultado.ndim > 2 else 1,
            'dtype': str(resultado.dtype)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/descargar', methods=['GET'])
def descargar():
    if ESTADO['img_actual'] is None:
        return jsonify({'error': 'No hay imagen para descargar'}), 400
        
    arr = ESTADO['img_actual']
    if arr.ndim == 2:
        pil_img = Image.fromarray(arr, mode='L')
    else:
        pil_img = Image.fromarray(arr[:, :, :3], mode='RGB')
        
    buffer = io.BytesIO()
    pil_img.save(buffer, format='PNG')
    buffer.seek(0)
    
    nombre_descarga = "resultado_" + os.path.splitext(ESTADO['nombre_archivo'])[0] + ".png"
    return send_file(
        buffer,
        mimetype='image/png',
        as_attachment=True,
        download_name=nombre_descarga
    )

@app.route('/api/restablecer', methods=['POST'])
def restablecer():
    if ESTADO['img_original'] is not None:
        ESTADO['img_actual'] = np.copy(ESTADO['img_original'])
        arr = ESTADO['img_actual']
        return jsonify({
            'success': True,
            'base64': array_a_base64(arr),
            'alto': arr.shape[0],
            'ancho': arr.shape[1],
            'canales': arr.shape[2] if arr.ndim > 2 else 1,
            'dtype': str(arr.dtype)
        })
    return jsonify({'error': 'No hay imagen original'}), 400

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
