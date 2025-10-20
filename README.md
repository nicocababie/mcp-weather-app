# 🌤️ Aplicación de Clima MCP

**Aplicación de consulta meteorológica en tiempo real usando el protocolo MCP**

## 🚀 Inicio Rápido

### Ejecución rápida
```bash
# Ejecutar la aplicación
./run_app.sh
```

### Ejecución Manual
```bash
# Crear entorno virtual (solo la primera vez)
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install requests

# Ejecutar la aplicación
python3 src/weather_app.py
```

## 🏗️ Arquitectura

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Weather App   │◄──►│   MCP Client    │◄──►│   MCP Server    │◄──►│  Weather Service│
│   (Tkinter UI)  │    │                 │    │                 │    │   (wttr.in API) │
└─────────────────┘    └─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 📁 Estructura del Proyecto

```
mcp-weather-app/
├── src/
│   ├── weather_app.py      # Interfaz gráfica principal
│   ├── mcp_client.py       # Cliente MCP
│   ├── mcp_server.py        # Servidor MCP
│   └── weather_service.py   # Servicio meteorológico
├── run_app.sh              # Script de inicio automático
├── venv/                   # Entorno virtual (creado automáticamente)
└── README.md               # Este archivo
```

## 🎯 Características

- ✅ **Interfaz gráfica** con Tkinter
- ✅ **Protocolo MCP** oficial implementado
- ✅ **Datos en tiempo real** desde wttr.in
- ✅ **Manejo de errores** robusto
- ✅ **Reconexión automática**
- ✅ **Instalación automática** de dependencias

## 🔧 Requisitos

- Python 3.7+
- Conexión a internet
- macOS/Linux/Windows

## 📊 Información Meteorológica

La aplicación proporciona:
- 🌡️ Temperatura actual y sensación térmica
- ☁️ Condiciones climáticas
- 💧 Humedad relativa
- 💨 Velocidad y dirección del viento
- 🌬️ Presión atmosférica
- 👁️ Visibilidad
- ☀️ Índice UV
- 🕐 Timestamp de actualización

## 📖 Uso de la Aplicación

1. **Ejecutar** la aplicación con `./run_app.sh`
2. **Esperar** a que aparezca "✅ Conectado al servidor MCP"
3. **Ingresar** el nombre de una ciudad
4. **Hacer clic** en "🌤️ Obtener Clima"
5. **Ver** la información meteorológica en tiempo real

## 🔄 Comandos Útiles

```bash
# Ejecutar aplicación (recomendado)
./run_app.sh

# Limpiar y reinstalar desde cero
rm -rf venv
./run_app.sh

# Probar componentes individuales (después de ./run_app.sh)
source venv/bin/activate
python3 src/weather_service.py    # Probar servicio meteorológico
python3 src/mcp_client.py         # Probar cliente MCP
python3 src/mcp_server.py         # Probar servidor MCP
```