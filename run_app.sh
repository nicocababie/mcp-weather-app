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

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  Iniciando aplicación de clima MCP...${NC}"
echo -e "${GREEN}========================================${NC}"

# Detectar automáticamente la estructura del entorno virtual
echo -e "${YELLOW}----------------------------------------${NC}"
echo -e "${YELLOW}  Detectando estructura del entorno...${NC}"
echo -e "${YELLOW}----------------------------------------${NC}"

if [ -f "venv/bin/activate" ]; then
    ACTIVATE_PATH="venv/bin/activate"
    echo -e "${GREEN} >> Entorno virtual detectado${NC}"
elif [ -f "venv/Scripts/activate" ]; then
    ACTIVATE_PATH="venv/Scripts/activate"
    echo -e "${GREEN} >> Entorno virtual detectado${NC}"
else
    # Si no existe el entorno virtual, usar el path por defecto según el sistema actual
    if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
        ACTIVATE_PATH="venv/Scripts/activate"
        echo -e "${GREEN} >> Configurado para entorno virtual${NC}"
    else
        ACTIVATE_PATH="venv/bin/activate"
        echo -e "${GREEN} >> Configurado para entorno virtual${NC}"
    fi
fi

# Verificar si existe el entorno virtual
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}----------------------------------------${NC}"
    echo -e "${YELLOW}  Creando entorno virtual...${NC}"
    echo -e "${YELLOW}----------------------------------------${NC}"
    echo -e "${YELLOW} >> Creando entorno virtual...${NC}"
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo -e "${RED} Error creando entorno virtual${NC}"
        exit 1
    fi
    echo -e "${GREEN} >> Entorno virtual creado${NC}"
fi

# Activar entorno virtual
echo -e "${YELLOW}----------------------------------------${NC}"
echo -e "${YELLOW}  Activando entorno virtual...${NC}"
echo -e "${YELLOW}----------------------------------------${NC}"
source "$ACTIVATE_PATH"
echo -e "${GREEN} >> Entorno virtual activado${NC}"

# Verificar si requests está instalado
echo -e "${YELLOW}----------------------------------------${NC}"
echo -e "${YELLOW}  Verificando dependencias...${NC}"
echo -e "${YELLOW}----------------------------------------${NC}"

if ! python3 -c "import requests" 2>/dev/null; then
    echo -e "${YELLOW} >> Instalando dependencias (requests)...${NC}"
    pip install requests
    if [ $? -ne 0 ]; then
        echo -e "${RED} Error instalando dependencias${NC}"
        exit 1
    fi
    echo -e "${GREEN} >> Dependencias instaladas${NC}"
else
    echo -e "${GREEN} >> Dependencias ya instaladas${NC}"
fi

echo -e "${GREEN} >> Verificación de dependencias completada${NC}"

# Verificar Tkinter
echo -e "${YELLOW}----------------------------------------${NC}"
echo -e "${YELLOW}  Verificando Tkinter...${NC}"
echo -e "${YELLOW}----------------------------------------${NC}"

if ! python3 -c "import tkinter" 2>/dev/null; then
    echo -e "${YELLOW} >> Tkinter no encontrado, intentando instalar...${NC}"
    
    # Detectar sistema operativo y intentar instalar Tkinter
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux - intentar instalar con el gestor de paquetes disponible
        if command -v apt-get &> /dev/null; then
            echo -e "${YELLOW} >> Instalando python3-tk (Ubuntu/Debian)...${NC}"
            sudo apt-get update && sudo apt-get install -y python3-tk
        elif command -v yum &> /dev/null; then
            echo -e "${YELLOW} >> Instalando tkinter (CentOS/RHEL)...${NC}"
            sudo yum install -y tkinter
        elif command -v dnf &> /dev/null; then
            echo -e "${YELLOW} >> Instalando python3-tkinter (Fedora)...${NC}"
            sudo dnf install -y python3-tkinter
        else
            echo -e "${RED} >> Error: No se pudo detectar el gestor de paquetes${NC}"
            echo -e "${RED} >> Instale manualmente: python3-tk o tkinter${NC}"
            exit 1
        fi
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        if command -v brew &> /dev/null; then
            echo -e "${YELLOW} >> Instalando python-tk (macOS con Homebrew)...${NC}"
            brew install python-tk
        else
            echo -e "${RED} >> Error: Tkinter no disponible en macOS${NC}"
            echo -e "${RED} >> Solución: Instale Python desde https://python.org${NC}"
            echo -e "${RED} >> O instale Homebrew: /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\"${NC}"
            exit 1
        fi
    elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
        # Windows
        echo -e "${RED} >> Error: Tkinter no disponible en Windows${NC}"
        echo -e "${RED} >> Solución: Reinstale Python desde https://python.org${NC}"
        echo -e "${RED} >> Asegúrese de marcar 'tcl/tk and IDLE' durante la instalación${NC}"
        exit 1
    fi
    
    # Verificar si la instalación fue exitosa
    if ! python3 -c "import tkinter" 2>/dev/null; then
        echo -e "${RED} >> Error: Tkinter aún no disponible después de la instalación${NC}"
        echo -e "${RED} >> Por favor, instale Tkinter manualmente según su sistema operativo${NC}"
        exit 1
    fi
    echo -e "${GREEN} >> Tkinter instalado correctamente${NC}"
else
    echo -e "${GREEN} >> Tkinter ya disponible${NC}"
fi

echo -e "${GREEN} >> Verificación de Tkinter completada${NC}"

# Ejecutar la aplicación
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  Ejecutando aplicación...${NC}"
echo -e "${GREEN}========================================${NC}"
python3 src/weather_app.py
