"""
Servidor MCP (Model Context Protocol) para información meteorológica
Implementa el protocolo MCP oficial con transporte stdio/JSON-RPC
"""

import json
import sys
import logging
from typing import Dict, Any, List, Optional
from weather_service import WeatherService

# Configurar logging a stderr para no interferir con stdio
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    stream=sys.stderr
)
logger = logging.getLogger(__name__)


class MCPServer:
    """Servidor MCP que implementa el protocolo oficial"""
    
    def __init__(self):
        self.weather_service = WeatherService()
        self.initialized = False
        self.server_info = {
            "name": "weather-mcp-server",
            "version": "1.0.0"
        }
    
    def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Maneja una solicitud JSON-RPC del cliente MCP
        
        Args:
            request (Dict[str, Any]): Solicitud JSON-RPC
            
        Returns:
            Dict[str, Any]: Respuesta JSON-RPC
        """
        try:
            method = request.get("method")
            params = request.get("params", {})
            request_id = request.get("id")
            
            logger.info(f"Procesando solicitud: {method}")
            
            if method == "initialize":
                return self._handle_initialize(params, request_id)
            elif method == "tools/list":
                return self._handle_tools_list(request_id)
            elif method == "tools/call":
                return self._handle_tools_call(params, request_id)
            else:
                return self._create_error_response(
                    -32601, "Method not found", request_id
                )
                
        except Exception as e:
            logger.error(f"Error procesando solicitud: {e}")
            return self._create_error_response(
                -32603, f"Internal error: {str(e)}", request.get("id")
            )
    
    def _handle_initialize(self, params: Dict[str, Any], request_id: Any) -> Dict[str, Any]:
        """Maneja la solicitud de inicialización del protocolo MCP"""
        self.initialized = True
        
        response = {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {}
                },
                "serverInfo": self.server_info
            }
        }
        
        logger.info("Servidor MCP inicializado correctamente")
        return response
    
    def _handle_tools_list(self, request_id: Any) -> Dict[str, Any]:
        """Maneja la solicitud de listar herramientas disponibles"""
        if not self.initialized:
            return self._create_error_response(
                -32002, "Server not initialized", request_id
            )
        
        tools = [
            {
                "name": "get_weather",
                "description": "Obtiene información meteorológica para una ciudad específica",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "city": {
                            "type": "string",
                            "description": "Nombre de la ciudad para consultar el clima"
                        }
                    },
                    "required": ["city"]
                }
            }
        ]
        
        response = {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "tools": tools
            }
        }
        
        logger.info("Lista de herramientas enviada")
        return response
    
    def _handle_tools_call(self, params: Dict[str, Any], request_id: Any) -> Dict[str, Any]:
        """Maneja la llamada a una herramienta específica"""
        if not self.initialized:
            return self._create_error_response(
                -32002, "Server not initialized", request_id
            )
        
        tool_name = params.get("name")
        arguments = params.get("arguments", {})
        
        if tool_name == "get_weather":
            city = arguments.get("city")
            if not city:
                return self._create_error_response(
                    -32602, "Missing required parameter: city", request_id
                )
            
            try:
                weather_data = self.weather_service.get_weather(city)
                
                response = {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "content": [
                            {
                                "type": "text",
                                "text": json.dumps(weather_data, ensure_ascii=False, indent=2)
                            }
                        ]
                    }
                }
                
                logger.info(f"Información meteorológica enviada para: {city}")
                return response
                
            except Exception as e:
                logger.error(f"Error obteniendo clima para {city}: {e}")
                return self._create_error_response(
                    -32603, f"Error obteniendo información meteorológica: {str(e)}", request_id
                )
        else:
            return self._create_error_response(
                -32601, f"Unknown tool: {tool_name}", request_id
            )
    
    def _create_error_response(self, code: int, message: str, request_id: Any) -> Dict[str, Any]:
        """Crea una respuesta de error JSON-RPC"""
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {
                "code": code,
                "message": message
            }
        }
    
    def run(self):
        """Ejecuta el servidor MCP en modo stdio"""
        logger.info("Iniciando servidor MCP...")
        
        try:
            while True:
                # Leer línea desde stdin
                line = sys.stdin.readline()
                if not line:
                    break
                
                line = line.strip()
                if not line:
                    continue
                
                try:
                    # Parsear JSON-RPC
                    request = json.loads(line)
                    
                    # Procesar solicitud
                    response = self.handle_request(request)
                    
                    # Enviar respuesta por stdout
                    print(json.dumps(response, ensure_ascii=False))
                    sys.stdout.flush()
                    
                except json.JSONDecodeError as e:
                    logger.error(f"Error parseando JSON: {e}")
                    error_response = self._create_error_response(
                        -32700, "Parse error", None
                    )
                    print(json.dumps(error_response))
                    sys.stdout.flush()
                    
        except KeyboardInterrupt:
            logger.info("Servidor MCP detenido por el usuario")
        except Exception as e:
            logger.error(f"Error en servidor MCP: {e}")
        finally:
            logger.info("Servidor MCP finalizado")


def main():
    """Función principal del servidor MCP"""
    server = MCPServer()
    server.run()


if __name__ == "__main__":
    main()
