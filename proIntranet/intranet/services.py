"""
Imports organizados por categorías:
1. Librerías estándar de Python
2. Django (core + contrib)
3. Librerías de terceros
4. Configuración del proyecto
5. Módulos internos de la app
"""


# 1. Librerías estándar
import requests
from django.core.cache import cache

# 2. Configuración global del proyecto
from config import conn as conn_settings


class SIIService:
    def __init__(self):
        self.url_auth = "https://sii.paraguay.gov.py/security"
        self.url_base = (
            "https://sii.paraguay.gov.py/frontend-identificaciones/api/persona"
        )
        self.cache_key = "sii_jwt_token"

    def get_token(self, force_refresh=False):
        """Obtiene el token de la caché o pide uno nuevo si no existe."""
        token = cache.get(self.cache_key)

        if not token or force_refresh:
            print("Solicitando nuevo token al SII...")
            headers = {"Accept": "application/json", "Content-Type": "application/json"}
            payload = {
                "username": conn_settings.SII_CREDENTIALS["USERNAME"],
                "password": conn_settings.SII_CREDENTIALS["PASSWORD"],
            }

            response = requests.post(self.url_auth, json=payload, headers=headers)
            if response.status_code == 200:
                # Extraemos el token (ajusta la llave 'token' según la respuesta real)
                token = response.json().get("token")
                # Guardamos en caché por 1 hora (3600 seg) o lo que dure el JWT
                cache.set(self.cache_key, token, timeout=3600)
            else:
                return None
        return token

    def consultar_cedula(self, cedula):
        token = self.get_token()

        if not token:
            return {"error": "No se pudo obtener el token de acceso"}

        url = f"{self.url_base}/obtenerPersonaPorCedula/{cedula}"
        headers = {"Accept": "application/json", "Authorization": f"Bearer {token}"}

        response = requests.get(url, headers=headers)

        # SI EL TOKEN EXPIRÓ (401 Unauthorized)
        if response.status_code == 401:
            print("Token expirado, reintentando con uno nuevo...")
            token = self.get_token(force_refresh=True)  # Forzar refresco
            headers["Authorization"] = f"Bearer {token}"
            response = requests.get(url, headers=headers)  # Reintentar

        if response.status_code == 200:
            return response.json()

        return {
            "status_code": response.status_code,
            "error": f"Error en la API: {response.status_code}",
            "detalle": response.text,
        }


# --- Ejemplo de uso en una vista o script ---
# service = SIIService()
# resultado = service.consultar_cedula("80020808")
