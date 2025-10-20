# 🌤️ Aplicación de Clima MCP

**Aplicación de consulta meteorológica en tiempo real usando el protocolo MCP**

## 🚀 Inicio Rápido

```bash
./run_app.sh
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
│   ├── weather_app.py       # Interfaz gráfica principal
│   ├── mcp_client.py        # Cliente MCP
│   ├── mcp_server.py        # Servidor MCP
│   └── weather_service.py   # Servicio meteorológico
├── run_app.sh               # Script de inicio automático
├── venv/                    # Entorno virtual (creado automáticamente)
└── README.md                # Documentación
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