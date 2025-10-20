# 🚀 Guía de Instalación - MCP Weather Server & Client

**Guía paso a paso para configurar y ejecutar el sistema MCP de información meteorológica**

Esta guía te permitirá configurar y ejecutar el servidor MCP y la aplicación cliente sin necesidad de conocimientos técnicos avanzados.

## 🐳 Opción 1: DevContainer (Recomendado)

**Para desarrollo y testing, la opción más fácil es usar el DevContainer:**

### ✅ Ventajas del DevContainer
- **Entorno aislado**: No interfiere con tu sistema local
- **Preconfigurado**: Todas las dependencias ya instaladas
- **Reproducible**: Mismo entorno en cualquier máquina
- **GUI funcionando**: Tkinter configurado automáticamente
- **Debug listo**: Configuraciones de debug predefinidas

### 🚀 Pasos para DevContainer

1. **Instalar VS Code** y la extensión "Dev Containers"
2. **Abrir el proyecto** en VS Code
3. **Reabrir en contenedor**: Ctrl+Shift+P → "Dev Containers: Reopen in Container"
4. **Esperar** a que se construya el contenedor (primera vez puede tardar 2-3 minutos)
5. **Ejecutar aplicación**: Ctrl+Shift+P → "Tasks: Run Task" → "🌤️ Ejecutar Weather App"

**¡Listo!** La aplicación se ejecutará automáticamente.

---

## 💻 Opción 2: Instalación Local

**Si prefieres instalar en tu sistema local:**

## 📋 Requisitos Previos

### ✅ Verificación de Python

**Paso 1: Verificar instalación de Python**

Abre una terminal (Command Prompt en Windows, Terminal en macOS/Linux) y ejecuta:

```bash
python --version
```

**Resultado esperado:**
```
Python 3.8.x o superior
```

Si no tienes Python instalado o tienes una versión anterior:
- **Windows**: Descarga desde [python.org](https://www.python.org/downloads/)
- **macOS**: `brew install python3` (si tienes Homebrew) o descarga desde python.org
- **Linux**: `sudo apt install python3` (Ubuntu/Debian) o `sudo yum install python3` (CentOS/RHEL)

### ✅ Verificación de pip

```bash
pip --version
```

**Resultado esperado:**
```
pip 21.x.x o superior
```

Si pip no está instalado:
```bash
python -m ensurepip --upgrade
```

## 🏗️ Configuración del Proyecto

### **Paso 2: Crear entorno virtual (Recomendado)**

**¿Por qué usar un entorno virtual?**
- Aísla las dependencias del proyecto
- Evita conflictos con otros proyectos Python
- Facilita la gestión de versiones

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En Windows:
venv\Scripts\activate

# En macOS/Linux:
source venv/bin/activate
```

**Indicador de éxito:** Verás `(venv)` al inicio de tu línea de comandos.

### **Paso 3: Instalar dependencias**

```bash
# Instalar todas las dependencias necesarias
pip install -r requirements.txt
```

**Resultado esperado:**
```
Collecting requests>=2.31.0
  Downloading requests-2.31.0-py2.py3-none-any.whl (62 kB)
Installing collected packages: requests
Successfully installed requests-2.31.0
```

### **Paso 4: Verificar estructura de archivos**

Tu proyecto debe tener esta estructura:

```
tarea-mcp/
├── src/
│   ├── weather_service.py
│   ├── mcp_server.py
│   ├── mcp_client.py
│   └── weather_app.py
├── requirements.txt
├── README.md
└── GUIA_INSTALACION.md
```

## 🚀 Ejecución del Sistema

### **Paso 5: Ejecutar la aplicación principal**

**Opción A: Ejecución directa (Recomendada)**

```bash
# Desde el directorio raíz del proyecto
python src/weather_app.py
```

**Opción B: Ejecución con módulo**

```bash
# Desde el directorio raíz del proyecto
python -m src.weather_app
```

### **Paso 6: Verificar funcionamiento**

**Indicadores de éxito:**

1. **Ventana de la aplicación se abre** con el título "🌤️ Clima en Tiempo Real - MCP Client"
2. **Estado de conexión** muestra "✅ Conectado al servidor MCP"
3. **Botón "Obtener Clima"** está habilitado
4. **Campo de entrada** está listo para escribir

## 🧪 Pruebas del Sistema

### **Paso 7: Probar consulta meteorológica**

1. **Escribe una ciudad** en el campo de entrada (ej: "Madrid", "London", "New York")
2. **Presiona Enter** o haz clic en "🌤️ Obtener Clima"
3. **Verifica la información** mostrada:
   - Temperatura actual
   - Condiciones meteorológicas
   - Humedad
   - Velocidad del viento
   - Otros datos meteorológicos

### **Paso 8: Probar diferentes ciudades**

Prueba con estas ciudades para verificar el funcionamiento:

- **Madrid** (España)
- **London** (Reino Unido)
- **New York** (Estados Unidos)
- **Tokyo** (Japón)
- **Sydney** (Australia)

## 🔧 Solución de Problemas Comunes

### ❌ **Error: "No se pudo conectar al servidor MCP"**

**Causa:** El servidor MCP no se puede iniciar.

**Solución:**
1. Verifica que estás en el directorio correcto
2. Asegúrate de que el entorno virtual esté activado
3. Verifica que todos los archivos estén presentes

```bash
# Verificar archivos
ls src/  # En macOS/Linux
dir src\  # En Windows
```

### ❌ **Error: "ModuleNotFoundError: No module named 'requests'"**

**Causa:** Las dependencias no están instaladas.

**Solución:**
```bash
# Asegúrate de estar en el entorno virtual
# En Windows:
venv\Scripts\activate

# En macOS/Linux:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### ❌ **Error: "No se pudo obtener información meteorológica"**

**Causa:** Problemas de conectividad o ciudad no encontrada.

**Solución:**
1. Verifica tu conexión a internet
2. Intenta con el nombre de la ciudad en inglés
3. Usa nombres de ciudades principales (Madrid, London, Paris, etc.)

### ❌ **Error: "Tkinter no está disponible"**

**Causa:** Tkinter no está instalado en el sistema.

**Solución:**

**En Windows:** Tkinter viene incluido con Python por defecto.

**En macOS:**
```bash
# Si usas Homebrew
brew install python-tk

# O reinstala Python desde python.org
```

**En Linux (Ubuntu/Debian):**
```bash
sudo apt-get install python3-tk
```

**En Linux (CentOS/RHEL):**
```bash
sudo yum install tkinter
```

## 📊 Verificación Avanzada

### **Paso 9: Probar componentes individuales**

**Probar el servicio meteorológico:**

```bash
python src/weather_service.py
```

**Resultado esperado:**
```
Probando servicio meteorológico...
🌤️  Clima en Madrid
🌡️  Temperatura: 15°C
☁️  Condiciones: Partly cloudy
💧 Humedad: 65%
💨 Viento: 12 km/h SW
🌡️  Sensación térmica: 13°C
```

**Probar el cliente MCP:**

```bash
python src/mcp_client.py
```

**Resultado esperado:**
```
Probando cliente MCP...
✅ Conectado al servidor MCP
🔧 Herramientas disponibles: 1
  - get_weather: Obtiene información meteorológica para una ciudad específica

🌤️ Probando consulta meteorológica...
✅ Datos meteorológicos obtenidos:
  city: Madrid
  temperature: 15
  condition: Partly cloudy
  ...
```

## 🎯 Uso de la Aplicación

### **Interfaz Principal**

1. **Campo de entrada**: Escribe el nombre de la ciudad
2. **Botón "Obtener Clima"**: Ejecuta la consulta
3. **Área de resultados**: Muestra información meteorológica detallada
4. **Botón "Limpiar"**: Borra los resultados
5. **Botón "Reconectar"**: Reinicia la conexión al servidor

### **Características de la Interfaz**

- **Diseño responsive**: Se adapta al tamaño de la ventana
- **Manejo de errores**: Mensajes informativos en caso de problemas
- **Reconexión automática**: Se conecta automáticamente al servidor
- **Información detallada**: Muestra todos los datos meteorológicos disponibles

## 📈 Monitoreo del Sistema

### **Logs del Sistema**

El sistema genera logs que puedes ver en la terminal:

```
2024-01-15 10:30:15 - INFO - Iniciando servidor MCP...
2024-01-15 10:30:16 - INFO - Servidor MCP inicializado correctamente
2024-01-15 10:30:20 - INFO - Procesando solicitud: get_weather
2024-01-15 10:30:21 - INFO - Información meteorológica enviada para: Madrid
```

### **Indicadores de Estado**

- **🔄 Conectando al servidor MCP...**: Iniciando conexión
- **✅ Conectado al servidor MCP**: Conexión exitosa
- **❌ Error de conexión**: Problema de conectividad

## 🚀 Próximos Pasos

Una vez que el sistema esté funcionando correctamente, puedes:

1. **Explorar el código**: Revisar los archivos fuente para entender la implementación
2. **Personalizar la interfaz**: Modificar colores, fuentes, o layout
3. **Agregar funcionalidades**: Pronósticos extendidos, historial, etc.
4. **Integrar con otros servicios**: APIs meteorológicas adicionales

## 📞 Soporte

Si encuentras problemas no cubiertos en esta guía:

1. **Verifica los logs** en la terminal para mensajes de error específicos
2. **Revisa la documentación** en README.md
3. **Asegúrate** de seguir todos los pasos en orden
4. **Verifica** que tu conexión a internet funcione correctamente

---

**🎉 ¡Felicidades! Has configurado exitosamente el sistema MCP de información meteorológica.**

**🌤️ Ahora puedes consultar el clima de cualquier ciudad del mundo en tiempo real.**
