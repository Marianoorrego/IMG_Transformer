// Estado global en cliente
let herramientaActual = 'negativo';
let anguloRotacion = 90;
let dimensionesActuales = { ancho: 0, alto: 0 };

document.addEventListener('DOMContentLoaded', () => {
    initTabs();
    initSliders();
    initUpload();
    initRotacionButtons();
    cargarMuestras();
    initFromQueryParams();
    
    // Boton restablecer
    document.getElementById('btn-restablecer').addEventListener('click', () => {
        mostrarCargando(true);
        fetch('/api/restablecer', { method: 'POST' })
            .then(res => res.json())
            .then(data => {
                mostrarCargando(false);
                if (data.success) {
                    actualizarResultado(data);
                }
            })
            .catch(() => mostrarCargando(false));
    });

    // Boton descargar
    document.getElementById('btn-descargar').addEventListener('click', () => {
        window.location.href = '/api/descargar';
    });

    // Boton cambiar imagen
    document.getElementById('btn-cambiar-img').addEventListener('click', () => {
        document.getElementById('file-input-main').click();
    });

    // Selector suma tipo
    document.getElementById('suma-tipo').addEventListener('change', (e) => {
        const grupoAlfa = document.getElementById('grupo-alfa');
        grupoAlfa.style.display = (e.target.value === 'ponderada') ? 'flex' : 'none';
    });

    // Input segunda imagen
    document.getElementById('input-segunda-img').addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            subirArchivo(e.target.files[0], true);
        }
    });
});

// Control de Pestañas de Herramientas
function initTabs() {
    const tabs = document.querySelectorAll('.tool-tab');
    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            tabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
            
            herramientaActual = tab.getAttribute('data-tool');
            
            // Ocultar todos los paneles y mostrar el seleccionado
            document.querySelectorAll('.tool-panel').forEach(p => p.classList.remove('active'));
            const panel = document.getElementById('panel-' + herramientaActual);
            if (panel) {
                panel.classList.add('active');
            }
        });
    });
}

// Inicializar Sliders e indicadores numericos
function initSliders() {
    // Brillo
    const sBrillo = document.getElementById('brillo-slider');
    const vBrillo = document.getElementById('brillo-val');
    sBrillo.addEventListener('input', () => {
        const val = sBrillo.value;
        vBrillo.textContent = (val > 0 ? '+' : '') + val;
    });

    // Brillo canal
    const sBrilloCanal = document.getElementById('brillo-canal-slider');
    const vBrilloCanal = document.getElementById('brillo-canal-val');
    sBrilloCanal.addEventListener('input', () => {
        const val = sBrilloCanal.value;
        vBrilloCanal.textContent = (val > 0 ? '+' : '') + val;
    });

    // Umbral
    const sUmbral = document.getElementById('umbral-slider');
    const vUmbral = document.getElementById('umbral-val');
    sUmbral.addEventListener('input', () => {
        vUmbral.textContent = sUmbral.value;
    });

    // Alfa suma
    const sAlfa = document.getElementById('suma-alfa');
    const vAlfa = document.getElementById('suma-alfa-val');
    sAlfa.addEventListener('input', () => {
        vAlfa.textContent = parseFloat(sAlfa.value).toFixed(2);
    });

    // Zoom
    const sZoom = document.getElementById('zoom-slider');
    const vZoom = document.getElementById('zoom-val');
    sZoom.addEventListener('input', () => {
        vZoom.textContent = sZoom.value + 'x';
    });

    // Reduccion
    const sRed = document.getElementById('reduccion-slider');
    const vRed = document.getElementById('reduccion-val');
    sRed.addEventListener('input', () => {
        vRed.textContent = sRed.value + 'x (paso ' + sRed.value + ')';
    });
}

// Botones de rotacion
function initRotacionButtons() {
    const btns = document.querySelectorAll('.btn-rot');
    btns.forEach(btn => {
        btn.addEventListener('click', () => {
            btns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            anguloRotacion = parseInt(btn.getAttribute('data-ang'));
        });
    });
}

// Cargar y listar muestras de la carpeta
function cargarMuestras() {
    fetch('/api/muestras')
        .then(res => res.json())
        .then(data => {
            const contenedor = document.getElementById('muestras-lista');
            contenedor.innerHTML = '';
            if (data.muestras && data.muestras.length > 0) {
                data.muestras.forEach(nombre => {
                    const btn = document.createElement('button');
                    btn.className = 'btn-muestra';
                    btn.textContent = nombre;
                    btn.onclick = () => cargarMuestra(nombre, false);
                    contenedor.appendChild(btn);
                });
            }
        });
}

function cargarMuestra(nombre, esSegunda = false) {
    mostrarCargando(true);
    fetch('/api/cargar-muestra', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ nombre: nombre, es_segunda: esSegunda })
    })
    .then(res => res.json())
    .then(data => {
        mostrarCargando(false);
        if (data.success) {
            if (esSegunda) {
                document.getElementById('label-segunda-img').textContent = nombre;
            } else {
                establecerImagenBase(data);
            }
        } else {
            alert('Error al cargar muestra: ' + (data.error || 'Desconocido'));
        }
    })
    .catch(err => {
        mostrarCargando(false);
        console.error(err);
    });
}

// Manejo de carga de archivos
function initUpload() {
    const dropzone = document.getElementById('dropzone-container');
    const fileInput = document.getElementById('file-input-main');

    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            subirArchivo(e.target.files[0], false);
        }
    });

    ['dragenter', 'dragover'].forEach(eventName => {
        dropzone.addEventListener(eventName, (e) => {
            e.preventDefault();
            dropzone.classList.add('dragover');
        });
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropzone.addEventListener(eventName, (e) => {
            e.preventDefault();
            dropzone.classList.remove('dragover');
        });
    });

    dropzone.addEventListener('drop', (e) => {
        if (e.dataTransfer.files.length > 0) {
            subirArchivo(e.dataTransfer.files[0], false);
        }
    });
}

function subirArchivo(file, esSegunda = false) {
    const formData = new FormData();
    formData.append('archivo', file);
    formData.append('es_segunda', esSegunda);

    mostrarCargando(true);

    fetch('/api/subir', {
        method: 'POST',
        body: formData
    })
    .then(res => res.json())
    .then(data => {
        mostrarCargando(false);
        if (data.success) {
            if (esSegunda) {
                document.getElementById('label-segunda-img').textContent = file.name;
            } else {
                establecerImagenBase(data);
            }
        } else {
            alert('Error: ' + (data.error || 'No se pudo subir la imagen'));
        }
    })
    .catch(err => {
        mostrarCargando(false);
        console.error(err);
    });
}

function establecerImagenBase(data) {
    document.getElementById('dropzone-container').style.display = 'none';
    document.getElementById('workspace-container').style.display = 'grid';
    document.getElementById('btn-descargar').disabled = false;

    // Actualizar visor original
    const imgOrig = document.getElementById('img-orig-view');
    imgOrig.src = data.base64;

    document.getElementById('orig-dim').textContent = `${data.ancho} × ${data.alto} px`;
    document.getElementById('orig-dtype').textContent = data.dtype || 'uint8';

    dimensionesActuales.ancho = data.ancho;
    dimensionesActuales.alto = data.alto;

    // Actualizar visor resultado inicialmente igual
    actualizarResultado(data);

    // Ajustar valores de recorte por defecto
    document.getElementById('rec-x1').value = 0;
    document.getElementById('rec-y1').value = 0;
    document.getElementById('rec-x2').value = data.ancho;
    document.getElementById('rec-y2').value = data.alto;
}

function actualizarResultado(data) {
    const imgRes = document.getElementById('img-res-view');
    imgRes.src = data.base64;

    document.getElementById('res-dim').textContent = `${data.ancho} × ${data.alto} px`;
    document.getElementById('res-dtype').textContent = data.dtype || 'uint8';
}

function mostrarCargando(estado) {
    const loader = document.getElementById('loader');
    if (loader) {
        loader.style.display = estado ? 'flex' : 'none';
    }
}

// Ejecución de Transformaciones
function ejecutarTransformacion(operacion, params = {}) {
    mostrarCargando(true);

    fetch('/api/transformar', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ operacion: operacion, params: params })
    })
    .then(res => res.json())
    .then(data => {
        mostrarCargando(false);
        if (data.success) {
            actualizarResultado(data);
        } else {
            alert('Error: ' + (data.error || 'No se pudo aplicar la transformacion'));
        }
    })
    .catch(err => {
        mostrarCargando(false);
        console.error(err);
    });
}

function ejecutarBrillo() {
    const val = document.getElementById('brillo-slider').value;
    ejecutarTransformacion('brillo', { valor: val });
}

function ejecutarBrilloCanal() {
    const canal = document.getElementById('brillo-canal-sel').value;
    const val = document.getElementById('brillo-canal-slider').value;
    ejecutarTransformacion('brillo_canal', { canal: canal, valor: val });
}

function ejecutarGrises() {
    const metodo = document.getElementById('grises-metodo').value;
    ejecutarTransformacion(metodo, {});
}

function ejecutarUmbral() {
    const val = document.getElementById('umbral-slider').value;
    ejecutarTransformacion('umbralizacion', { umbral: val });
}

function ejecutarCanales() {
    const modo = document.getElementById('canales-modo').value;
    ejecutarTransformacion('canales_rgb_cmy', { modo: modo });
}

function ejecutarSuma() {
    const tipo = document.getElementById('suma-tipo').value;
    const alfa = document.getElementById('suma-alfa').value;
    ejecutarTransformacion('suma_imagenes', { tipo: tipo, alfa: alfa });
}

function ejecutarRecorte() {
    const x1 = document.getElementById('rec-x1').value;
    const y1 = document.getElementById('rec-y1').value;
    const x2 = document.getElementById('rec-x2').value;
    const y2 = document.getElementById('rec-y2').value;
    ejecutarTransformacion('recorte', { x1: x1, y1: y1, x2: x2, y2: y2 });
}

function autoValoresRecorte() {
    const w = dimensionesActuales.ancho;
    const h = dimensionesActuales.alto;
    document.getElementById('rec-x1').value = Math.floor(w * 0.25);
    document.getElementById('rec-y1').value = Math.floor(h * 0.25);
    document.getElementById('rec-x2').value = Math.floor(w * 0.75);
    document.getElementById('rec-y2').value = Math.floor(h * 0.75);
}

function ejecutarZoom() {
    const factor = document.getElementById('zoom-slider').value;
    ejecutarTransformacion('zoom', { factor: factor });
}

function ejecutarReduccion() {
    const factor = document.getElementById('reduccion-slider').value;
    ejecutarTransformacion('reduccion', { factor: factor });
}

function ejecutarRotacion() {
    ejecutarTransformacion('rotacion', { angulo: anguloRotacion });
}

function initFromQueryParams() {
    const params = new URLSearchParams(window.location.search);
    const imgName = params.get('img');
    const tool = params.get('tool');
    
    if (imgName) {
        cargarMuestra(imgName, false);
    }
    
    if (tool) {
        setTimeout(() => {
            const tab = document.querySelector(`.tool-tab[data-tool="${tool}"]`);
            if (tab) tab.click();
            
            setTimeout(() => {
                if (tool === 'brillo') {
                    const val = params.get('val') || 50;
                    document.getElementById('brillo-slider').value = val;
                    document.getElementById('brillo-val').textContent = (val > 0 ? '+' : '') + val;
                    ejecutarBrillo();
                } else if (tool === 'canales') {
                    const modo = params.get('modo') || 'mosaico_rgb';
                    document.getElementById('canales-modo').value = modo;
                    ejecutarCanales();
                } else if (tool === 'suma') {
                    const tipo = params.get('tipo') || 'promedio';
                    const alfa = params.get('alfa') || '0.5';
                    document.getElementById('suma-tipo').value = tipo;
                    document.getElementById('suma-alfa').value = alfa;
                    ejecutarSuma();
                } else if (tool === 'histograma') {
                    ejecutarTransformacion('histograma');
                } else if (tool === 'recorte') {
                    autoValoresRecorte();
                    ejecutarRecorte();
                } else if (tool === 'zoom') {
                    document.getElementById('zoom-slider').value = params.get('factor') || 3;
                    ejecutarZoom();
                } else if (tool === 'reduccion') {
                    document.getElementById('reduccion-slider').value = params.get('factor') || 4;
                    ejecutarReduccion();
                } else if (tool === 'rotacion') {
                    anguloRotacion = parseInt(params.get('ang') || 90);
                    ejecutarRotacion();
                }
            }, 300);
        }, 300);
    }
}
