"""
Aplicación Tkinter (MCP Host) para consultar información meteorológica
Utiliza el protocolo MCP para comunicarse con el servidor meteorológico
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import json
from typing import Dict, Any, Optional
from mcp_client import WeatherMCPClient


class WeatherApp:
    """Aplicación principal con interfaz Tkinter para consultas meteorológicas"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.mcp_client = WeatherMCPClient()
        self.connected = False
        self.setup_ui()
        self.connect_to_server()
    
    def setup_ui(self):
        """Configura la interfaz de usuario"""
        self.root.title(" Clima en Tiempo Real - MCP Client")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        # Configurar estilo
        style = ttk.Style()
        style.theme_use('clam')
        
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Título
        title_label = ttk.Label(
            main_frame, 
            text=" Consulta de Clima en Tiempo Real",
            font=('Arial', 16, 'bold')
        )
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Estado de conexión
        self.status_label = ttk.Label(
            main_frame,
            text=" Conectando al servidor MCP...",
            font=('Arial', 10)
        )
        self.status_label.grid(row=1, column=0, columnspan=3, pady=(0, 10))
        
        # Frame de entrada
        input_frame = ttk.LabelFrame(main_frame, text="Consulta de Ciudad", padding="10")
        input_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        input_frame.columnconfigure(1, weight=1)
        
        # Campo de entrada para ciudad
        ttk.Label(input_frame, text="Ciudad:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.city_entry = ttk.Entry(input_frame, font=('Arial', 12))
        self.city_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        self.city_entry.bind('<Return>', lambda e: self.get_weather())
        
        # Botón de consulta
        self.query_button = ttk.Button(
            input_frame,
            text=" Obtener Clima",
            command=self.get_weather,
            state='disabled'
        )
        self.query_button.grid(row=0, column=2)
        
        # Frame de resultados
        results_frame = ttk.LabelFrame(main_frame, text="Información Meteorológica", padding="10")
        results_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(3, weight=1)
        
        # Área de texto para mostrar resultados
        self.results_text = scrolledtext.ScrolledText(
            results_frame,
            height=15,
            font=('Consolas', 10),
            wrap=tk.WORD,
            state='disabled'
        )
        self.results_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Frame de botones
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, columnspan=3, pady=(10, 0))
        
        # Botón de limpiar
        ttk.Button(
            button_frame,
            text="Limpiar",
            command=self.clear_results
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        # Botón de reconectar
        self.reconnect_button = ttk.Button(
            button_frame,
            text="Reconectar",
            command=self.reconnect_server
        )
        self.reconnect_button.pack(side=tk.LEFT)
        
        # Barra de progreso
        self.progress = ttk.Progressbar(
            main_frame,
            mode='indeterminate',
            length=200
        )
        self.progress.grid(row=5, column=0, columnspan=3, pady=(10, 0), sticky=(tk.W, tk.E))
        self.progress.grid_remove()  # Ocultar inicialmente
    
    def connect_to_server(self):
        """Conecta al servidor MCP en un hilo separado"""
        def connect():
            try:
                if self.mcp_client.connect():
                    self.connected = True
                    self.root.after(0, self.on_connection_success)
                else:
                    self.root.after(0, self.on_connection_failure)
            except Exception as e:
                self.root.after(0, lambda: self.on_connection_failure(str(e)))
        
        threading.Thread(target=connect, daemon=True).start()
    
    def on_connection_success(self):
        """Maneja la conexión exitosa"""
        self.status_label.config(text=" Conectado al servidor MCP")
        self.query_button.config(state='normal')
        self.reconnect_button.config(state='disabled')
    
    def on_connection_failure(self, error_msg: str = None):
        """Maneja el fallo de conexión"""
        error_text = f" Error de conexión: {error_msg}" if error_msg else " No se pudo conectar al servidor MCP"
        self.status_label.config(text=error_text)
        self.query_button.config(state='disabled')
        self.reconnect_button.config(state='normal')
        
        if error_msg:
            messagebox.showerror("Error de Conexión", f"No se pudo conectar al servidor MCP:\n{error_msg}")
    
    def get_weather(self):
        """Obtiene información meteorológica para la ciudad ingresada"""
        city = self.city_entry.get().strip()
        if not city:
            messagebox.showwarning("Advertencia", "Por favor, ingrese el nombre de una ciudad.")
            return
        
        if not self.connected:
            messagebox.showerror("Error", "No hay conexión con el servidor MCP.")
            return
        
        # Deshabilitar botón y mostrar progreso
        self.query_button.config(state='disabled')
        self.progress.grid()
        self.progress.start()
        
        # Ejecutar consulta en hilo separado
        def fetch_weather():
            try:
                weather_data = self.mcp_client.get_weather(city)
                self.root.after(0, lambda: self.display_weather(weather_data, city))
            except Exception as e:
                self.root.after(0, lambda: self.display_error(str(e), city))
        
        threading.Thread(target=fetch_weather, daemon=True).start()
    
    def display_weather(self, weather_data: Dict[str, Any], city: str):
        """Muestra la información meteorológica"""
        self.progress.stop()
        self.progress.grid_remove()
        self.query_button.config(state='normal')
        
        if "error" in weather_data:
            self.display_error(weather_data.get("message", "Error desconocido"), city)
            return
        
        # Formatear información meteorológica
        weather_text = f"""
 INFORMACIÓN METEOROLÓGICA - {weather_data.get('city', city).upper()}
{'=' * 60}

Temperatura: {weather_data.get('temperature', 'N/A')}°C
Sensación térmica: {weather_data.get('feels_like', 'N/A')}°C
Condiciones: {weather_data.get('condition', 'N/A')}
Humedad: {weather_data.get('humidity', 'N/A')}%
Viento: {weather_data.get('wind_speed', 'N/A')} km/h {weather_data.get('wind_direction', '')}
Presión: {weather_data.get('pressure', 'N/A')} mb
Visibilidad: {weather_data.get('visibility', 'N/A')} km
Índice UV: {weather_data.get('uv_index', 'N/A')}
Última actualización: {weather_data.get('timestamp', 'N/A')}

{'=' * 60}
Datos obtenidos desde wttr.in via MCP Server
        """.strip()
        
        # Mostrar en el área de texto
        self.results_text.config(state='normal')
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(1.0, weather_text)
        self.results_text.config(state='disabled')
        
        # Scroll al inicio
        self.results_text.see(1.0)
    
    def display_error(self, error_msg: str, city: str):
        """Muestra un mensaje de error"""
        self.progress.stop()
        self.progress.grid_remove()
        self.query_button.config(state='normal')
        
        error_text = f"""
 ERROR AL OBTENER INFORMACIÓN METEOROLÓGICA
{'=' * 50}

Ciudad consultada: {city}
Error: {error_msg}

{'=' * 50}
Sugerencias:
• Verifique que el nombre de la ciudad sea correcto
• Asegúrese de que hay conexión a internet
• Intente con el nombre en inglés (ej: Madrid, London, New York)
• Verifique que el servidor MCP esté funcionando
        """.strip()
        
        self.results_text.config(state='normal')
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(1.0, error_text)
        self.results_text.config(state='disabled')
        
        self.results_text.see(1.0)
    
    def clear_results(self):
        """Limpia el área de resultados"""
        self.results_text.config(state='normal')
        self.results_text.delete(1.0, tk.END)
        self.results_text.config(state='disabled')
    
    def reconnect_server(self):
        """Reconecta al servidor MCP"""
        self.status_label.config(text="🔄 Reconectando...")
        self.query_button.config(state='disabled')
        self.reconnect_button.config(state='disabled')
        
        # Desconectar primero
        if self.connected:
            self.mcp_client.disconnect()
            self.connected = False
        
        # Reconectar
        self.connect_to_server()
    
    def run(self):
        """Ejecuta la aplicación"""
        try:
            self.root.mainloop()
        finally:
            # Limpiar recursos al cerrar
            if self.connected:
                self.mcp_client.disconnect()


def main():
    """Función principal"""
    print(" Iniciando aplicación de clima MCP...")
    
    try:
        app = WeatherApp()
        app.run()
    except Exception as e:
        print(f" Error iniciando aplicación: {e}")
        messagebox.showerror("Error", f"Error iniciando aplicación: {e}")


if __name__ == "__main__":
    main()
