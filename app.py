
# app.py
# Autor: Gemini
# Fecha: 26-09-2025
# Descripción: Backend con Flask que simula la obtención de datos de una API externa.

from flask import Flask, jsonify, send_from_directory
import json
import os

# --- Constantes y Configuración ---
JSON_FILE_PATH = os.path.join(os.path.dirname(__file__), 'data.json')

# --- Lógica de Obtención de Datos ---

def _fetch_data_from_api():
    """
    Método de ejemplo que simula una llamada a una API REST externa.
    En un caso real, aquí se usaría una librería como 'requests'.
    Ej: response = requests.get('https://api.dental.com/consultas')
    """
    print("Intentando obtener datos desde la API externa simulada...")
    # Simulación: Si la API falla, podría lanzar una excepción.
    # import random
    # if random.random() < 0.5:
    #     raise ConnectionError("No se pudo conectar a la API externa.")

    # Datos de ejemplo que la API devolvería. Se añade un nuevo paciente.
    api_data = [
        {
            "id_consulta": "C001", "paciente": {"nombre": "Ana García", "id_paciente": "P078", "edad": 34, "genero": "Femenino"},
            "fecha": "2025-09-26", "hora": "10:00 AM", "dentista": "Dr. Carlos Sánchez", "motivo_consulta": "Revisión y limpieza dental.",
            "diagnostico": {"descripcion": "Placa y sarro.", "codigo_cie": "K03.6"}, "tratamiento": {"procedimiento": "Profilaxis.", "costo_usd": 80, "estado": "Completado"},
            "notas_adicionales": "Mejorar técnica de cepillado."
        },
        {
            "id_consulta": "C002", "paciente": {"nombre": "Luis Martínez", "id_paciente": "P102", "edad": 45, "genero": "Masculino"},
            "fecha": "2025-09-26", "hora": "11:30 AM", "dentista": "Dra. Elena Torres", "motivo_consulta": "Dolor en molar.",
            "diagnostico": {"descripcion": "Caries profunda.", "codigo_cie": "K02.1"}, "tratamiento": {"procedimiento": "Endodoncia.", "costo_usd": 750, "estado": "En progreso"},
            "notas_adicionales": "Cita en 2 semanas."
        },
        # Este es un nuevo dato que simula una actualización desde la API.
        {
            "id_consulta": "C004", "paciente": {"nombre": "Ricardo Vargas", "id_paciente": "P115", "edad": 52, "genero": "Masculino"},
            "fecha": "2025-09-28", "hora": "04:00 PM", "dentista": "Dra. Elena Torres", "motivo_consulta": "Implante dental.",
            "diagnostico": {"descripcion": "Ausencia de pieza 24.", "codigo_cie": "K08.1"}, "tratamiento": {"procedimiento": "Colocación de implante de titanio.", "costo_usd": 1200, "estado": "Pendiente"},
            "notas_adicionales": "Requiere evaluación de tomografía."
        }
    ]
    print("Datos obtenidos de la API exitosamente.")
    return api_data

def _save_data_to_json(data):
    """
    Toma los datos (una lista de diccionarios) y los guarda en el archivo JSON.
    """
    try:
        with open(JSON_FILE_PATH, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
        print(f"Datos guardados correctamente en {JSON_FILE_PATH}")
    except IOError as e:
        print(f"Error al escribir en el archivo JSON: {e}")

def initialize_data():
    """
    Orquesta el flujo de datos al iniciar la aplicación.
    """
    try:
        # 1. Intentar obtener datos de la API
        fresh_data = _fetch_data_from_api()
        # 2. Si hay éxito, guardarlos en el JSON
        _save_data_to_json(fresh_data)
    except Exception as e:
        # 3. Si la API falla, informar y usar el archivo local si existe.
        print(f"ADVERTENCIA: Falló la obtención de datos de la API ({e}).")
        print("La aplicación usará los datos locales del archivo data.json si existe.")

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
        # 4. Error si el archivo no existe (y la API falló previamente)
        print(f"ERROR CRÍTICO: El archivo {JSON_FILE_PATH} no fue encontrado.")
        return jsonify({"error": "El archivo de datos no fue encontrado. Contacte al administrador."}), 404
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
    # 1. Ejecutar el flujo de datos antes de iniciar el servidor.
    initialize_data()
    # 2. Iniciar el servidor de desarrollo de Flask.
    app.run(debug=True, port=5000)
