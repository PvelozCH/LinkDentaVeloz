# app.py
# Autor: Gemini
# Fecha: 30-09-2025
# Descripción: Backend con Flask y pywebview para la aplicación de escritorio.
# Esta versión solo lee datos del JSON local.

from flask import Flask, jsonify, send_from_directory
import json
import os
import webview

# --- Constantes y Configuración ---
JSON_FILE_PATH = os.path.join(os.path.dirname(__file__), 'data.json')

# --- Inicialización de la Aplicación Flask ---
app = Flask(__name__, static_folder='static', static_url_path='')

# --- Rutas de la API ---
@app.route('/api/consultas')
def obtener_consultas():
    """
    Endpoint que lee el archivo data.json local y lo sirve.
    """
    try:
        with open(JSON_FILE_PATH, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return jsonify(data)
    except FileNotFoundError:
        print(f"ERROR CRÍTICO: El archivo {JSON_FILE_PATH} no fue encontrado.")
        return jsonify({"error": "El archivo de datos no fue encontrado. Ejecute el script de actualización."}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- Rutas para servir el Frontend ---
@app.route('/')
def servir_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/historial.html')
def servir_historial():
    return send_from_directory(app.static_folder, 'historial.html')

# --- Punto de Entrada Principal ---
if __name__ == '__main__':
    # Iniciar la aplicación de escritorio con pywebview.
    webview.create_window('LinkDentaVeloz', app)
    webview.start()