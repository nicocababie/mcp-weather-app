#!/bin/bash

# Script para ejecutar la aplicación de clima MCP con entorno virtual
# Maneja automáticamente la instalación inicial y la ejecución

# Navegar al directorio del proyecto
cd "$(dirname "$0")"

# Colores para output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}🌤️ Iniciando aplicación de clima MCP...${NC}"

# Verificar si existe el entorno virtual
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}📦 Creando entorno virtual...${NC}"
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo -e "${RED}❌ Error creando entorno virtual${NC}"
        exit 1
    fi
    echo -e "${GREEN}✅ Entorno virtual creado${NC}"
fi

# Activar entorno virtual
echo -e "${YELLOW}🔧 Activando entorno virtual...${NC}"
source venv/bin/activate

# Verificar si requests está instalado
if ! python3 -c "import requests" 2>/dev/null; then
    echo -e "${YELLOW}📥 Instalando dependencias (requests)...${NC}"
    pip install requests
    if [ $? -ne 0 ]; then
        echo -e "${RED}❌ Error instalando dependencias${NC}"
        exit 1
    fi
    echo -e "${GREEN}✅ Dependencias instaladas${NC}"
else
    echo -e "${GREEN}✅ Dependencias ya instaladas${NC}"
fi

# Ejecutar la aplicación
echo -e "${GREEN}🚀 Ejecutando aplicación...${NC}"
python3 src/weather_app.py
