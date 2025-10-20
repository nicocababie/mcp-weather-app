"""
Servicio para consultar información meteorológica desde wttr.in
Proporciona funciones para obtener datos del clima en tiempo real
"""

import requests
import json
from typing import Dict, Optional, Any


class WeatherService:
    """Servicio para obtener información meteorológica desde wttr.in"""
    
    def __init__(self):
        self.base_url = "https://wttr.in"
        self.timeout = 10  # segundos
    
    def get_weather(self, city: str) -> Dict[str, Any]:
        """
        Obtiene información meteorológica para una ciudad específica
        
        Args:
            city (str): Nombre de la ciudad
            
        Returns:
            Dict[str, Any]: Diccionario con información meteorológica o error
            
        Raises:
            Exception: Si hay error en la consulta
        """
        try:
            # Consultar wttr.in en formato JSON
            url = f"{self.base_url}/{city}?format=j1"
            response = requests.get(url, timeout=self.timeout)
            
            if response.status_code == 200:
                data = response.json()
                return self._parse_weather_data(data, city)
            else:
                return {
                    "error": f"Error HTTP {response.status_code}",
                    "message": "No se pudo obtener información meteorológica"
                }
                
        except requests.exceptions.Timeout:
            return {
                "error": "Timeout",
                "message": "La consulta tardó demasiado tiempo"
            }
        except requests.exceptions.ConnectionError:
            return {
                "error": "Connection Error",
                "message": "No se pudo conectar al servicio meteorológico"
            }
        except json.JSONDecodeError:
            return {
                "error": "JSON Error",
                "message": "Respuesta inválida del servicio meteorológico"
            }
        except Exception as e:
            return {
                "error": "Unknown Error",
                "message": f"Error inesperado: {str(e)}"
            }
    
    def _parse_weather_data(self, data: Dict[str, Any], city: str) -> Dict[str, Any]:
        """
        Parsea los datos JSON de wttr.in y extrae información relevante
        
        Args:
            data (Dict[str, Any]): Datos JSON de wttr.in
            city (str): Nombre de la ciudad
            
        Returns:
            Dict[str, Any]: Datos meteorológicos parseados
        """
        try:
            # Extraer datos de la condición actual
            current = data.get("current_condition", [{}])[0]
            
            # Extraer datos de la ubicación
            nearest_area = data.get("nearest_area", [{}])[0]
            area_name = nearest_area.get("areaName", [{}])[0].get("value", city)
            
            # Construir respuesta estructurada
            weather_info = {
                "city": area_name,
                "temperature": current.get("temp_C", "N/A"),
                "condition": current.get("weatherDesc", [{}])[0].get("value", "N/A"),
                "humidity": current.get("humidity", "N/A"),
                "wind_speed": current.get("windspeedKmph", "N/A"),
                "wind_direction": current.get("winddir16Point", "N/A"),
                "pressure": current.get("pressure", "N/A"),
                "feels_like": current.get("FeelsLikeC", "N/A"),
                "visibility": current.get("visibility", "N/A"),
                "uv_index": current.get("uvIndex", "N/A"),
                "timestamp": current.get("localObsDateTime", "N/A")
            }
            
            return weather_info
            
        except (KeyError, IndexError, TypeError) as e:
            return {
                "error": "Parse Error",
                "message": f"Error al procesar datos meteorológicos: {str(e)}"
            }
    
    def get_weather_summary(self, city: str) -> str:
        """
        Obtiene un resumen textual del clima para una ciudad
        
        Args:
            city (str): Nombre de la ciudad
            
        Returns:
            str: Resumen textual del clima
        """
        weather_data = self.get_weather(city)
        
        if "error" in weather_data:
            return f"Error: {weather_data['message']}"
        
        return (
            f"🌤️  Clima en {weather_data['city']}\n"
            f"🌡️  Temperatura: {weather_data['temperature']}°C\n"
            f"☁️  Condiciones: {weather_data['condition']}\n"
            f"💧 Humedad: {weather_data['humidity']}%\n"
            f"💨 Viento: {weather_data['wind_speed']} km/h {weather_data['wind_direction']}\n"
            f"🌡️  Sensación térmica: {weather_data['feels_like']}°C"
        )


# Función de conveniencia para uso directo
def get_weather_for_city(city: str) -> Dict[str, Any]:
    """
    Función de conveniencia para obtener clima de una ciudad
    
    Args:
        city (str): Nombre de la ciudad
        
    Returns:
        Dict[str, Any]: Información meteorológica
    """
    service = WeatherService()
    return service.get_weather(city)


if __name__ == "__main__":
    # Prueba del servicio
    service = WeatherService()
    
    # Probar con Madrid
    print("Probando servicio meteorológico...")
    result = service.get_weather("Madrid")
    
    if "error" in result:
        print(f"Error: {result['message']}")
    else:
        print(service.get_weather_summary("Madrid"))
