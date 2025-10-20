# 🌤️ MCP Weather Server & Client

**Servidor y Cliente MCP (Model Context Protocol) para información meteorológica en tiempo real**

Este proyecto implementa un sistema completo basado en el protocolo MCP oficial para consultar información meteorológica en tiempo real utilizando la API pública de wttr.in, con una interfaz gráfica desarrollada en Python Tkinter.

## 📋 Descripción del Proyecto

El sistema está compuesto por tres componentes principales que siguen la arquitectura del **Model Context Protocol (MCP)**:

- **🌐 MCP Server**: Servidor que expone herramientas para consultar clima via wttr.in
- **🔗 MCP Client**: Cliente Python que se comunica con el servidor via stdio/JSON-RPC  
- **🖥️ MCP Host**: Aplicación Tkinter (Windows) que gestiona el cliente y muestra la información

## 🏗️ Arquitectura del Sistema

```
┌─────────────────┐    stdio/JSON-RPC    ┌─────────────────┐    HTTP API    ┌─────────────────┐
│   MCP Host      │◄────────────────────►│   MCP Server    │◄──────────────►│   wttr.in API   │
│  (Tkinter App)  │                      │  (mcp_server.py)│                │  (Weather Data) │
└─────────────────┘                      └─────────────────┘                └─────────────────┘
         ▲                                        ▲
         │                                        │
         │                                        │
┌─────────────────┐                      ┌─────────────────┐
│   MCP Client    │                      │ Weather Service │
│ (mcp_client.py) │                      │(weather_service)│
└─────────────────┘                      └─────────────────┘
```

## 📁 Estructura de Archivos

```
tarea-mcp/
├── src/
│   ├── weather_service.py     # Servicio para consultar wttr.in
│   ├── mcp_server.py          # Servidor MCP con protocolo stdio/JSON-RPC
│   ├── mcp_client.py          # Cliente MCP para comunicación con servidor
│   └── weather_app.py         # Aplicación Tkinter (MCP Host)
├── requirements.txt           # Dependencias del proyecto
├── README.md                  # Este archivo
└── GUIA_INSTALACION.md       # Guía paso a paso de configuración
```

## 🚀 Opciones de Ejecución

### 🐳 DevContainer (Recomendado)

**Para desarrollo y testing:**
1. **Abrir en VS Code** con la extensión "Dev Containers"
2. **Reabrir en contenedor** (Ctrl+Shift+P → "Dev Containers: Reopen in Container")
3. **Ejecutar aplicación** usando las tareas predefinidas

**Ventajas del DevContainer:**
- ✅ Entorno aislado y reproducible
- ✅ Todas las dependencias preinstaladas
- ✅ Soporte completo para GUI (Tkinter)
- ✅ Configuraciones de debug listas

### 💻 Instalación Local

1. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Ejecutar la aplicación:**
   ```bash
   python src/weather_app.py
   ```

## 🚀 Características Principales

### ✅ Protocolo MCP Oficial
- Implementación completa del protocolo MCP con transporte stdio
- Comunicación JSON-RPC entre cliente y servidor
- Manejo de mensajes: `initialize`, `tools/list`, `tools/call`

### 🌤️ Información Meteorológica Completa
- **Temperatura actual** (°C)
- **Condiciones meteorológicas** (ej: "Partly cloudy")
- **Humedad** (%)
- **Velocidad del viento** (km/h)
- **Dirección del viento**
- **Presión atmosférica**
- **Visibilidad**
- **Índice UV**
- **Sensación térmica**

### 🖥️ Interfaz Gráfica Moderna
- Aplicación Tkinter con diseño profesional
- Campo de entrada para ciudad
- Visualización clara de datos meteorológicos
- Manejo de errores con mensajes informativos
- Reconexión automática al servidor
- Interfaz responsive y fácil de usar

### 🔧 Características Técnicas
- **Sin API Key requerida**: Utiliza wttr.in (servicio gratuito)
- **Comunicación asíncrona**: Hilos separados para consultas
- **Manejo robusto de errores**: Validación y mensajes informativos
- **Logging completo**: Registro de eventos para debugging
- **Arquitectura modular**: Componentes independientes y reutilizables

## 🛠️ Tecnologías Utilizadas

- **Python 3.8+**: Lenguaje de programación base
- **Tkinter**: Interfaz gráfica (incluida en Python estándar)
- **requests**: Consultas HTTP a wttr.in
- **JSON-RPC**: Protocolo de comunicación MCP
- **subprocess**: Comunicación stdio entre procesos
- **threading**: Manejo de hilos para operaciones asíncronas

## 📊 Flujo de Comunicación MCP

1. **Usuario** ingresa ciudad en la aplicación Tkinter (MCP Host)
2. **MCP Host** llama a `mcp_client.get_weather(city)`
3. **MCP Client** envía mensaje JSON-RPC al servidor via stdin
4. **MCP Server** consulta wttr.in API
5. **MCP Server** responde con datos en formato JSON-RPC via stdout
6. **MCP Client** parsea respuesta y retorna datos estructurados
7. **MCP Host** muestra información meteorológica en la interfaz

## 🎯 Casos de Uso

- **Consultas meteorológicas en tiempo real** para cualquier ciudad del mundo
- **Aplicaciones educativas** para aprender el protocolo MCP
- **Desarrollo de sistemas distribuidos** con comunicación stdio
- **Prototipos de aplicaciones meteorológicas** con arquitectura modular

## 📈 Información Meteorológica Disponible

El sistema obtiene datos de **wttr.in** en formato JSON, incluyendo:

| Campo | Descripción | Unidad |
|-------|-------------|--------|
| `temperature` | Temperatura actual | °C |
| `condition` | Descripción del clima | Texto |
| `humidity` | Humedad relativa | % |
| `wind_speed` | Velocidad del viento | km/h |
| `wind_direction` | Dirección del viento | Puntos cardinales |
| `pressure` | Presión atmosférica | mb |
| `feels_like` | Sensación térmica | °C |
| `visibility` | Visibilidad | km |
| `uv_index` | Índice UV | Número |
| `timestamp` | Última actualización | Fecha/Hora |

## 🔍 Ejemplos de Uso

### Consulta Básica
```python
from src.mcp_client import get_weather_for_city

# Obtener clima de Madrid
weather = get_weather_for_city("Madrid")
print(weather)
```

### Uso del Servicio Directo
```python
from src.weather_service import WeatherService

service = WeatherService()
weather = service.get_weather("London")
summary = service.get_weather_summary("London")
print(summary)
```

## 🚨 Requisitos del Sistema

- **Python 3.8 o superior**
- **Conexión a Internet** (para consultar wttr.in)
- **Sistema operativo**: Windows, macOS, o Linux
- **Memoria**: Mínimo 100MB RAM
- **Espacio en disco**: 10MB

## 📚 Documentación Adicional

- **[GUIA_INSTALACION.md](GUIA_INSTALACION.md)**: Guía paso a paso para configurar el proyecto
- **Código fuente**: Comentarios detallados en español
- **Logs**: Información de debugging en stderr

## 🤝 Contribuciones

Este proyecto está diseñado como una implementación educativa del protocolo MCP. Las contribuciones son bienvenidas para:

- Mejoras en la interfaz de usuario
- Optimizaciones de rendimiento
- Nuevas funcionalidades meteorológicas
- Mejoras en la documentación

## 📄 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

---

**🌤️ Desarrollado con Python y el protocolo MCP para consultas meteorológicas en tiempo real**
