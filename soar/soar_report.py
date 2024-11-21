import requests
import uuid
from datetime import datetime

def generate_uuid_from_date(date):
    """Generate a UUID using the given date as a seed."""
    seed = date.strftime("%Y%m%d%H%M%S")
    return uuid.uuid5(uuid.NAMESPACE_DNS, seed)

def send_soar_report(url, soar_id, soar_key, soar_name, start_date, end_date, token):
    # Format the dates
    start_date_str = start_date.strftime("%Y-%m-%d %H:%M:%S")
    end_date_str = end_date.strftime("%Y-%m-%d %H:%M:%S")
    
    # Generate UUID based on the start date
    uuid_generated = generate_uuid_from_date(start_date)
    
    # Data structure to be sent
    data = {
        "id_ejecucion": str(uuid_generated),
        "fk_flujo": soar_id,
        "fk_metrica": "",
        "Adjetivo1": "Informes",
        "Adjetivo2": soar_key,
        "Adjetivo3": "",
        "Adjetivo4": "",
        "AcumuladoMetrica": "1",
        "FechaInicioEjecucion": start_date_str,
        "FechaFinEjecucion": end_date_str,
        "fk_pais": "ES",
        "NotaInterna": soar_name,
        "Timestamp": end_date_str
    }
    
    # Headers
    headers = {
        "Content-Type": "application/json",
        "TokenAuth": token
    }
    
    # Send the POST request
    response = requests.post(f"{url}", json=data, headers=headers)
    
    # Handle the response
    if response.status_code == 201:
        print("Report sent successfully.")
    else:
        raise Exception(f"Error sending report: {response.status_code} - {response.text}")
