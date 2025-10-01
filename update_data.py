# update_data.py
# Autor: Gemini
# Fecha: 30-09-2025
# Descripción: Script para extraer datos de la API simulada y guardarlos en data.json.

import json
import os

# --- Constantes y Configuración ---
JSON_FILE_PATH = os.path.join(os.path.dirname(__file__), 'data.json')

# --- Lógica de Obtención de Datos ---

def _fetch_data_from_api():
    """
    Método de ejemplo que simula una llamada a una API REST externa.
    """
    print("Intentando obtener datos desde la API externa simulada...")
    # Datos de ejemplo que la API devolvería.
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
        {
            "id_consulta": "C004", "paciente": {"nombre": "Ricardo Vargas", "id_paciente": "P115", "edad": 52, "genero": "Masculino"},
            "fecha": "2025-09-28", "hora": "04:00 PM", "dentista": "Dra. Elena Torres", "motivo_consulta": "Implante dental.",
            "diagnostico": {"descripcion": "Ausencia de pieza 24.", "codigo_cie": "K08.1"}, "tratamiento": {"procedimiento": "Colocación de implante de titanio.", "costo_usd": 1200, "estado": "Pendiente"},
            "notas_adicionales": "Requiere evaluación de tomografía."
        },
        # Simulando una nueva consulta añadida en esta ejecución
        {
            "id_consulta": "C005", "paciente": {"nombre": "Elena Jiménez", "id_paciente": "P120", "edad": 28, "genero": "Femenino"},
            "fecha": "2025-09-30", "hora": "09:00 AM", "dentista": "Dr. Carlos Sánchez", "motivo_consulta": "Ortodoncia.",
            "diagnostico": {"descripcion": "Maloclusión.", "codigo_cie": "K07.4"}, "tratamiento": {"procedimiento": "Colocación de brackets.", "costo_usd": 2500, "estado": "Pendiente"},
            "notas_adicionales": "Plan de tratamiento a 24 meses."
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

def main():
    """
    Orquesta el flujo de datos.
    """
    try:
        fresh_data = _fetch_data_from_api()
        _save_data_to_json(fresh_data)
    except Exception as e:
        print(f"ERROR: Falló la obtención o guardado de datos ({e}).")

# --- Punto de Entrada Principal ---
if __name__ == '__main__':
    main()
