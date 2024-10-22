import os
import requests
from urllib.parse import quote
import tkinter as tk
from tkinter import ttk, messagebox
import base64
import threading  # Para manejar los hilos
import time  # Para la reconexión periódica

# Códigos de idiomas
IDIOMAS = {
    'Inglés': 'en',
    'Español': 'es',
    'Francés': 'fr',
    'Alemán': 'de',
    'Italiano': 'it',
    'Portugués': 'pt',
    'Chino (simplificado)': 'zh-CN',
    'Chino (tradicional)': 'zh-TW',
    'Japonés': 'ja',
    'Ruso': 'ru',
    'Árabe': 'ar',
    'Hindi': 'hi',
    'Coreano': 'ko',
    'Turco': 'tr',
    'Neerlandés': 'nl',
    'Sueco': 'sv',
    'Danés': 'da',
    'Noruego': 'no',
    'Finlandés': 'fi',
    'Checo': 'cs',
    'Húngaro': 'hu',
    'Polaco': 'pl',
    'Rumano': 'ro',
    'Búlgaro': 'bg',
    'Griego': 'el',
    'Hebreo': 'iw',
    'Tailandés': 'th',
    'Vietnamita': 'vi',
    'Malayo': 'ms',
    'Filipino': 'tl',
    'Indonesio': 'id',
    'Serbio': 'sr',
    'Croata': 'hr',
    'Esloveno': 'sl',
    'Estonio': 'et',
    'Lituano': 'lt',
    'Letón': 'lv',
    'Tamil': 'ta',
    'Telugu': 'te',
    'Maratí': 'mr',
    'Bengalí': 'bn',
    'Urdu': 'ur'
}

def verificar_conexion_anki():
    """Función para verificar si AnkiConnect está disponible."""
    payload = {
        "action": "version",
        "version": 6
    }
    try:
        response = requests.post("http://localhost:8765", json=payload)
        result = response.json()
        if result.get("error") is None:
            return True
        return False
    except Exception as e:
        return False

def obtener_mazos():
    """Función para obtener los mazos disponibles en Anki usando AnkiConnect."""
    payload = {
        "action": "deckNames",
        "version": 6
    }
    try:
        response = requests.post("http://localhost:8765", json=payload)
        result = response.json()
        if result.get("error") is not None:
            print(f"Error al obtener mazos de Anki: {result['error']}")
            return []
        return result["result"]
    except Exception as e:
        print(f"Error en la conexión con Anki: {e}")
        return []

#todo: agregar una función que busque una imagen de la palabra en ingreso
def descargar_audio(palabra, idioma='en'):
    url = f"https://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&tl={idioma}&q={quote(palabra)}"
    nombre_archivo = f"{palabra}.mp3"

    try:
        respuesta = requests.get(url)

        if respuesta.status_code == 200:
            with open(nombre_archivo, 'wb') as archivo:
                archivo.write(respuesta.content)
            print(f"Audio descargado como {nombre_archivo}")
            return nombre_archivo
        else:
            print(f"Error al descargar el audio. Código: {respuesta.status_code}")
            return None

    except Exception as e:
        print(f"Error: {e}")
        return None

def agregar_a_anki(palabra, translate, archivo_audio, mazo='Vocabulario'):
    
    if not os.path.exists(archivo_audio):
        print(f"Error: El archivo de audio {archivo_audio} no existe.")
        return
    
    if not palabra:
        print("Error: La palabra está vacía.")
        return

    try:
        with open(archivo_audio, 'rb') as f:
            audio_data = f.read()

        audio_base64 = base64.b64encode(audio_data).decode('utf-8')

        payload_audio = {
            "action": "storeMediaFile",
            "version": 6,
            "params": {
                "filename": archivo_audio,  
                "data": audio_base64
            }
        }

        response_audio = requests.post("http://localhost:8765", json=payload_audio)
        result_audio = response_audio.json()

        if result_audio.get("error") is not None:
            print(f"Error al subir el audio a Anki: {result_audio['error']}")
            return
        else:
            print(f"Audio {archivo_audio} subido exitosamente.")

    except Exception as e:
        print(f"Error al subir el archivo de audio: {e}")
        return

    try:
        # Crear el cuerpo de la solicitud para agregar la tarjeta
        payload = {
            "action": "addNote",
            "version": 6,
            "params": {
                "note": {
                    "deckName": mazo,  # Nombre del mazo al que se quiere agregar la tarjeta
                    "modelName": "Básico",  # Cambiar esto si el idioma de anki esta en ingles o español
                    "fields": {
                        "Anverso": f"{palabra} [sound:{archivo_audio}]",
                        "Reverso": translate #Todo: usar una api de traduccion de idiomas o chatgpt para que forme oraciones usando la palabra o traduzca la palabra 
                    },
                    "tags": [mazo],
                    "options": {
                        "allowDuplicate": False
                    }
                }
            }
        }

        # Realizar la solicitud a AnkiConnect para agregar la nota
        response = requests.post("http://localhost:8765", json=payload)
        result = response.json()

        print(f"Respuesta de AnkiConnect: {result}")

        if result.get("error") is not None:
            print(f"Error al agregar a Anki: {result['error']}")
        else:
            print("Tarjeta agregada a Anki exitosamente")
    
    except Exception as e:
        print(f"Error en la conexión con Anki: {e}")

def verificar_y_actualizar_estado_conexion():
    """Función para verificar periódicamente la conexión a Anki y actualizar la interfaz."""
    if verificar_conexion_anki():
        etiqueta_estado_anki.config(text="Conectado a Anki", fg="green")
        boton_descargar.config(state='normal')

        # Si AnkiConnect está disponible, actualizamos los mazos
        mazos_disponibles = obtener_mazos()
        combo_mazos['values'] = mazos_disponibles
        combo_mazos.set(mazos_disponibles[0] if mazos_disponibles else '')
    else:
        etiqueta_estado_anki.config(text="No conectado a Anki. Abre Anki y AnkiConnect.", fg="red")
        boton_descargar.config(state='disabled')

    # Vuelve a intentar cada 5 segundos.
    root.after(5000, verificar_y_actualizar_estado_conexion)

def realizar_proceso():
    """Función que realiza todo el proceso de descarga y adición a Anki en segundo plano."""
    palabra = entrada_palabra.get()
    translate = entrada_translate.get()
    idioma_seleccionado = combo_idiomas.get()
    mazo_seleccionado = combo_mazos.get()

    if not palabra or not translate or not idioma_seleccionado or not mazo_seleccionado:
        messagebox.showwarning("Advertencia", "Por favor, completa todos los campos.")
        return

    idioma_codigo = IDIOMAS[idioma_seleccionado]
    archivo_audio = descargar_audio(palabra, idioma_codigo)

    if archivo_audio:
        # Agregar palabra y audio a Anki
        agregar_a_anki(palabra, translate, archivo_audio, mazo=mazo_seleccionado)

        # Mostrar mensaje de éxito
        etiqueta_estado.config(text="Proceso completado.", fg='green')
        messagebox.showinfo("Éxito", f"El audio se ha guardado como {archivo_audio} y se ha agregado a Anki.")
    else:
        etiqueta_estado.config(text="Error al descargar el audio.", fg='red')

    # Detener la barra de progreso y ocultarla
    barra_progreso.stop()
    barra_progreso.grid_remove()
    # Habilitar el botón de nuevo
    boton_descargar.config(state='normal')

def on_download():
    """Función que se ejecuta cuando se presiona el botón de descarga."""
    # Deshabilitar el botón y mostrar estado
    boton_descargar.config(state='disabled')
    etiqueta_estado.config(text="Descargando y agregando a Anki...", fg='blue')

    # Mostrar la barra de progreso y comenzarla
    barra_progreso.grid()  # La mostramos cuando se presiona el botón
    barra_progreso.start(10)  # Comienza la animación de la barra

    root.update_idletasks()  # Actualiza la interfaz gráfica

    # Iniciar el proceso en un nuevo hilo
    threading.Thread(target=realizar_proceso).start()

# Crear la interfaz gráfica
root = tk.Tk()
root.title("Descargador de Audio para Anki")
root.configure(bg='#f0f0f0')  # Color de fondo de la ventana

# Etiqueta para mostrar el estado de conexión a Anki
etiqueta_estado_anki = tk.Label(root, text="Verificando conexión a Anki...", bg='#f0f0f0', font=('Arial', 12))
etiqueta_estado_anki.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

# Etiqueta y entrada para la palabra
etiqueta_palabra = tk.Label(root, text="Ingresa la palabra o frase:", bg='#f0f0f0', font=('Arial', 12))
etiqueta_palabra.grid(row=1, column=0, padx=10, pady=10)

entrada_palabra = tk.Entry(root, font=('Arial', 12))
entrada_palabra.grid(row=2, column=0, padx=10, pady=10)

etiqueta_translate = tk.Label(root, text="Ingresa la traducción:", bg='#f0f0f0', font=('Arial', 12))
etiqueta_translate.grid(row=1, column=1, padx=10, pady=10)

entrada_translate = tk.Entry(root, font=('Arial', 12))
entrada_translate.grid(row=2, column=1, padx=10, pady=10)

# Obtener los mazos y mostrarlos en el ComboBox
mazos_disponibles = obtener_mazos()
etiqueta_mazos = tk.Label(root, text="Selecciona tu mazo:", bg='#f0f0f0', font=('Arial', 12))
etiqueta_mazos.grid(row=3, column=0, padx=10, pady=10)

combo_mazos = ttk.Combobox(root, values=mazos_disponibles, font=('Arial', 12))
combo_mazos.set(mazos_disponibles[0] if mazos_disponibles else '')
combo_mazos.grid(row=4, column=0, padx=10, pady=10)

# Etiqueta y dropdown para seleccionar el idioma
etiqueta_idioma = tk.Label(root, text="Selecciona el idioma:", bg='#f0f0f0', font=('Arial', 12))
etiqueta_idioma.grid(row=3, column=1, padx=10, pady=10)

combo_idiomas = ttk.Combobox(root, values=list(IDIOMAS.keys()), font=('Arial', 12))
combo_idiomas.set('Inglés')  # Valor por defecto
combo_idiomas.grid(row=4, column=1, padx=10, pady=10)

# Botón para descargar el audio
boton_descargar = tk.Button(root, text="Descargar Audio y Agregar a Anki", command=on_download, bg='#4CAF50', fg='white', font=('Arial', 12))
boton_descargar.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

# Barra de progreso (inicialmente oculta)
barra_progreso = ttk.Progressbar(root, mode='indeterminate', length=300)
barra_progreso.grid(row=6, column=0, columnspan=2, padx=10, pady=10)
barra_progreso.grid_remove()  # La ocultamos al principio

# Label para mostrar el estado
etiqueta_estado = tk.Label(root, text="", bg='#f0f0f0', font=('Arial', 12))
etiqueta_estado.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

# Iniciar la verificación periódica de la conexión con Anki
verificar_y_actualizar_estado_conexion()

root.mainloop()