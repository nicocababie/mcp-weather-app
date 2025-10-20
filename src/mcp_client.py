"""
Cliente MCP (Model Context Protocol) para comunicación con el servidor
Implementa el protocolo MCP oficial con transporte stdio/JSON-RPC
"""

import json
import subprocess
import sys
import os
import logging
from typing import Dict, Any, Optional, List
from pathlib import Path

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MCPClient:
    """Cliente MCP que se comunica con el servidor via subprocess stdio"""
    
    def __init__(self, server_script_path: str):
        """
        Inicializa el cliente MCP
        
        Args:
            server_script_path (str): Ruta al script del servidor MCP
        """
        self.server_script_path = server_script_path
        self.process = None
        self.initialized = False
        self.request_id = 0
    
    def _get_next_request_id(self) -> int:
        """Obtiene el siguiente ID de solicitud"""
        self.request_id += 1
        return self.request_id
    
    def _send_request(self, method: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Envía una solicitud JSON-RPC al servidor
        
        Args:
            method (str): Método JSON-RPC
            params (Dict[str, Any]): Parámetros de la solicitud
            
        Returns:
            Dict[str, Any]: Respuesta del servidor
        """
        if not self.process:
            raise RuntimeError("Cliente no conectado al servidor")
        
        request = {
            "jsonrpc": "2.0",
            "id": self._get_next_request_id(),
            "method": method
        }
        
        if params:
            request["params"] = params
        
        # Enviar solicitud
        request_json = json.dumps(request) + "\n"
        self.process.stdin.write(request_json)
        self.process.stdin.flush()
        
        # Leer respuesta
        response_line = self.process.stdout.readline()
        if not response_line:
            raise RuntimeError("No se recibió respuesta del servidor")
        
        response = json.loads(response_line)
        
        # Verificar si hay error en la respuesta
        if "error" in response:
            error = response["error"]
            raise RuntimeError(f"Error del servidor: {error.get('message', 'Error desconocido')}")
        
        return response
    
    def connect(self) -> bool:
        """
        Conecta al servidor MCP
        
        Returns:
            bool: True si la conexión fue exitosa
        """
        try:
            # Verificar que el script del servidor existe
            if not os.path.exists(self.server_script_path):
                raise FileNotFoundError(f"Script del servidor no encontrado: {self.server_script_path}")
            
            # Iniciar proceso del servidor
            self.process = subprocess.Popen(
                [sys.executable, self.server_script_path],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=0
            )
            
            logger.info("Proceso del servidor MCP iniciado")
            return True
            
        except Exception as e:
            logger.error(f"Error conectando al servidor: {e}")
            return False
    
    def initialize(self) -> bool:
        """
        Inicializa la conexión con el servidor MCP
        
        Returns:
            bool: True si la inicialización fue exitosa
        """
        try:
            response = self._send_request("initialize", {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {
                    "name": "weather-mcp-client",
                    "version": "1.0.0"
                }
            })
            
            if "result" in response:
                self.initialized = True
                logger.info("Cliente MCP inicializado correctamente")
                return True
            else:
                logger.error("Error en la inicialización del cliente")
                return False
                
        except Exception as e:
            logger.error(f"Error inicializando cliente: {e}")
            return False
    
    def get_available_tools(self) -> List[Dict[str, Any]]:
        """
        Obtiene la lista de herramientas disponibles del servidor
        
        Returns:
            List[Dict[str, Any]]: Lista de herramientas disponibles
        """
        if not self.initialized:
            raise RuntimeError("Cliente no inicializado")
        
        try:
            response = self._send_request("tools/list")
            return response.get("result", {}).get("tools", [])
            
        except Exception as e:
            logger.error(f"Error obteniendo herramientas: {e}")
            return []
    
    def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Llama a una herramienta específica del servidor
        
        Args:
            tool_name (str): Nombre de la herramienta
            arguments (Dict[str, Any]): Argumentos para la herramienta
            
        Returns:
            Dict[str, Any]: Resultado de la herramienta
        """
        if not self.initialized:
            raise RuntimeError("Cliente no inicializado")
        
        try:
            response = self._send_request("tools/call", {
                "name": tool_name,
                "arguments": arguments
            })
            
            return response.get("result", {})
            
        except Exception as e:
            logger.error(f"Error llamando herramienta {tool_name}: {e}")
            raise
    
    def get_weather(self, city: str) -> Dict[str, Any]:
        """
        Obtiene información meteorológica para una ciudad
        
        Args:
            city (str): Nombre de la ciudad
            
        Returns:
            Dict[str, Any]: Información meteorológica
        """
        try:
            result = self.call_tool("get_weather", {"city": city})
            
            # Parsear el contenido de texto JSON
            content = result.get("content", [])
            if content and content[0].get("type") == "text":
                weather_data = json.loads(content[0]["text"])
                return weather_data
            else:
                return {"error": "No se recibieron datos meteorológicos válidos"}
                
        except Exception as e:
            logger.error(f"Error obteniendo clima para {city}: {e}")
            return {"error": f"Error obteniendo clima: {str(e)}"}
    
    def disconnect(self):
        """Desconecta del servidor MCP"""
        if self.process:
            try:
                self.process.stdin.close()
                self.process.stdout.close()
                self.process.stderr.close()
                self.process.terminate()
                self.process.wait(timeout=5)
                logger.info("Desconectado del servidor MCP")
            except Exception as e:
                logger.error(f"Error desconectando: {e}")
            finally:
                self.process = None
                self.initialized = False


class WeatherMCPClient:
    """Cliente de conveniencia para consultas meteorológicas"""
    
    def __init__(self):
        # Obtener la ruta del script del servidor
        current_dir = Path(__file__).parent
        server_script = current_dir / "mcp_server.py"
        self.client = MCPClient(str(server_script))
        self.connected = False
    
    def connect(self) -> bool:
        """
        Conecta al servidor meteorológico
        
        Returns:
            bool: True si la conexión fue exitosa
        """
        if self.client.connect() and self.client.initialize():
            self.connected = True
            logger.info("Conectado al servidor meteorológico MCP")
            return True
        return False
    
    def get_weather(self, city: str) -> Dict[str, Any]:
        """
        Obtiene información meteorológica para una ciudad
        
        Args:
            city (str): Nombre de la ciudad
            
        Returns:
            Dict[str, Any]: Información meteorológica
        """
        if not self.connected:
            if not self.connect():
                return {"error": "No se pudo conectar al servidor"}
        
        return self.client.get_weather(city)
    
    def disconnect(self):
        """Desconecta del servidor"""
        if self.connected:
            self.client.disconnect()
            self.connected = False


# Función de conveniencia para uso directo
def get_weather_for_city(city: str) -> Dict[str, Any]:
    """
    Función de conveniencia para obtener clima de una ciudad
    
    Args:
        city (str): Nombre de la ciudad
        
    Returns:
        Dict[str, Any]: Información meteorológica
    """
    client = WeatherMCPClient()
    try:
        return client.get_weather(city)
    finally:
        client.disconnect()


if __name__ == "__main__":
    # Prueba del cliente
    print("Probando cliente MCP...")
    
    client = WeatherMCPClient()
    if client.connect():
        print("✅ Conectado al servidor MCP")
        
        # Probar herramientas disponibles
        tools = client.client.get_available_tools()
        print(f"🔧 Herramientas disponibles: {len(tools)}")
        for tool in tools:
            print(f"  - {tool['name']}: {tool['description']}")
        
        # Probar consulta meteorológica
        print("\n🌤️ Probando consulta meteorológica...")
        weather = client.get_weather("Madrid")
        
        if "error" in weather:
            print(f"❌ Error: {weather['error']}")
        else:
            print("✅ Datos meteorológicos obtenidos:")
            for key, value in weather.items():
                print(f"  {key}: {value}")
        
        client.disconnect()
    else:
        print("❌ No se pudo conectar al servidor MCP")
