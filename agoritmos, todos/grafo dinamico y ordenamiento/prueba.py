import tkinter as tk
from tkinter import ttk, messagebox
import random
import math
from typing import List, Tuple, Optional
import numpy as np

class Point:
    def __init__(self, x: int = 0, y: int = 0):
        self.x = x
        self.y = y

class RedSocialGrafica:
    def __init__(self):
        self.usuarios: List[str] = []
        self.posiciones: List[Point] = []
        self.matriz_adyacencia: List[List[int]] = []
        self.matriz_pesos: List[List[int]] = []
        self.componente: List[int] = []
        self.colores: List[str] = []
        self.umbral_peso: int = 5
        self.random = random.Random()
        
        # Variables para pan/scroll de la vista
        self.offset_x: int = 0
        self.offset_y: int = 0
        self.last_x: int = 0
        self.last_y: int = 0
        self.panning: bool = False
        self.zoom_factor: float = 1.0
        
        # Variables para animaciones y efectos
        self.highlighted_nodes: List[int] = []
        self.highlighted_edges: List[Tuple[int, int]] = []
        self.animation_frame: int = 0
        self.show_stats: bool = True
        self.show_grid: bool = False
        self.dark_mode: bool = False
        
        # Configurar ventana principal
        self.root = tk.Tk()
        self.root.title("🌐 Red Social Interactiva - Vista Profesional")
        self.root.geometry("1200x900")
        self.root.configure(bg='#f0f0f0')
        
        # Configurar estilo
        self.setup_styles()
        
        # Crear interfaz
        self.create_main_interface()
        
        # Inicializar datos
        self.inicializar_grafo()
        self.detectar_componentes_por_peso()
        self.generar_posiciones()
        self.dibujar_grafo()
        
        # Centrar la vista inicialmente
        self.centrar_vista()
        
        # Iniciar animaciones
        self.start_animations()
    
    def setup_styles(self):
        """Configura los estilos de la interfaz"""
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Colores del tema
        self.colors = {
            'primary': '#2E86AB',
            'secondary': '#A23B72',
            'accent': '#F18F01',
            'success': '#C73E1D',
            'background': '#F5F5F5',
            'surface': '#FFFFFF',
            'text': '#2C3E50',
            'text_light': '#7F8C8D'
        }
        
        # Configurar estilos personalizados
        self.style.configure('Title.TLabel', font=('Arial', 16, 'bold'), foreground=self.colors['primary'])
        self.style.configure('Subtitle.TLabel', font=('Arial', 10), foreground=self.colors['text_light'])
        self.style.configure('Custom.TButton', font=('Arial', 9, 'bold'))
        self.style.configure('Stats.TLabel', font=('Courier', 9), foreground=self.colors['text'])
    
    def create_main_interface(self):
        """Crea la interfaz principal mejorada"""
        # Frame principal con padding
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header con título y estadísticas
        self.create_header(main_frame)
        
        # Frame central con canvas y panel lateral
        center_frame = ttk.Frame(main_frame)
        center_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        # Panel lateral izquierdo
        self.create_side_panel(center_frame)
        
        # Canvas principal
        self.create_canvas_area(center_frame)
        
        # Panel de controles inferior
        self.create_control_panel(main_frame)
        
        # Barra de estado
        self.create_status_bar(main_frame)
    
    def create_header(self, parent):
        """Crea el header con título y estadísticas"""
        header_frame = ttk.Frame(parent)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Título principal
        title_label = ttk.Label(header_frame, text="🌐 Red Social Interactiva", style='Title.TLabel')
        title_label.pack(side=tk.LEFT)
        
        # Frame de estadísticas
        stats_frame = ttk.Frame(header_frame)
        stats_frame.pack(side=tk.RIGHT)
        
        self.stats_label = ttk.Label(stats_frame, text="", style='Stats.TLabel')
        self.stats_label.pack()
        
        # Botón de modo oscuro
        self.dark_mode_btn = ttk.Button(stats_frame, text="🌙", width=3, 
                                       command=self.toggle_dark_mode)
        self.dark_mode_btn.pack(side=tk.RIGHT, padx=(10, 0))
    
    def create_side_panel(self, parent):
        """Crea el panel lateral con controles avanzados"""
        side_frame = ttk.LabelFrame(parent, text="🎛️ Controles", padding="10")
        side_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        # Sección de búsqueda
        search_frame = ttk.LabelFrame(side_frame, text="🔍 Búsqueda", padding="5")
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(search_frame, text="Usuario:").pack(anchor=tk.W)
        self.entrada_usuario = ttk.Entry(search_frame, width=15)
        self.entrada_usuario.pack(fill=tk.X, pady=(2, 5))
        
        ttk.Button(search_frame, text="🔍 Buscar", style='Custom.TButton',
                  command=self.buscar_interaccion).pack(fill=tk.X, pady=1)
        
        ttk.Button(search_frame, text="🎯 Buscar Aleatorio", style='Custom.TButton',
                  command=self.buscar_aleatorio).pack(fill=tk.X, pady=1)
        
        # Sección de visualización
        viz_frame = ttk.LabelFrame(side_frame, text="👁️ Visualización", padding="5")
        viz_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Umbral de peso
        ttk.Label(viz_frame, text="Umbral de Peso:").pack(anchor=tk.W)
        self.slider = ttk.Scale(viz_frame, from_=1, to=10, orient=tk.HORIZONTAL, 
                               command=self.actualizar_umbral)
        self.slider.set(5)
        self.slider.pack(fill=tk.X, pady=(2, 5))
        
        self.umbral_label = ttk.Label(viz_frame, text="Valor: 5")
        self.umbral_label.pack(anchor=tk.W)
        
        # Opciones de visualización
        self.show_weights_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(viz_frame, text="Mostrar Pesos", 
                       variable=self.show_weights_var,
                       command=self.dibujar_grafo).pack(anchor=tk.W, pady=2)
        
        self.show_labels_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(viz_frame, text="Mostrar Etiquetas", 
                       variable=self.show_labels_var,
                       command=self.dibujar_grafo).pack(anchor=tk.W, pady=2)
        
        self.show_grid_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(viz_frame, text="Mostrar Cuadrícula", 
                       variable=self.show_grid_var,
                       command=self.toggle_grid).pack(anchor=tk.W, pady=2)
        
        # Sección de navegación
        nav_frame = ttk.LabelFrame(side_frame, text="🧭 Navegación", padding="5")
        nav_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Controles de zoom
        zoom_frame = ttk.Frame(nav_frame)
        zoom_frame.pack(fill=tk.X, pady=2)
        
        ttk.Button(zoom_frame, text="🔍+", width=4, command=self.zoom_in).pack(side=tk.LEFT, padx=1)
        ttk.Button(zoom_frame, text="🔍-", width=4, command=self.zoom_out).pack(side=tk.LEFT, padx=1)
        ttk.Button(zoom_frame, text="1:1", width=4, command=self.reset_zoom).pack(side=tk.LEFT, padx=1)
        
        ttk.Button(nav_frame, text="🎯 Centrar Vista", style='Custom.TButton',
                  command=self.centrar_vista).pack(fill=tk.X, pady=2)
        
        ttk.Button(nav_frame, text="🔄 Resetear Posiciones", style='Custom.TButton',
                  command=self.resetear_posiciones).pack(fill=tk.X, pady=2)
        
        # Sección de análisis
        analysis_frame = ttk.LabelFrame(side_frame, text="📊 Análisis", padding="5")
        analysis_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(analysis_frame, text="📈 Estadísticas", style='Custom.TButton',
                  command=self.mostrar_estadisticas).pack(fill=tk.X, pady=2)
        
        ttk.Button(analysis_frame, text="🎨 Nuevo Layout", style='Custom.TButton',
                  command=self.generar_layout_aleatorio).pack(fill=tk.X, pady=2)
        
        ttk.Button(analysis_frame, text="🔗 Regenerar Red", style='Custom.TButton',
                  command=self.regenerar_red).pack(fill=tk.X, pady=2)
    
    def create_canvas_area(self, parent):
        """Crea el área del canvas con scrollbars mejorados"""
        canvas_frame = ttk.LabelFrame(parent, text="🖼️ Visualización de Red", padding="5")
        canvas_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Canvas con scrollbars
        self.canvas = tk.Canvas(canvas_frame, bg="white", 
                               scrollregion=(-2000, -2000, 2000, 2000),
                               highlightthickness=1, highlightbackground="#ddd")
        
        # Scrollbars con estilo
        self.h_scrollbar = ttk.Scrollbar(canvas_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.v_scrollbar = ttk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.canvas.configure(xscrollcommand=self.h_scrollbar.set, yscrollcommand=self.v_scrollbar.set)
        
        # Empaquetar
        self.h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Eventos del mouse
        self.setup_mouse_events()
    
    def create_control_panel(self, parent):
        """Crea el panel de controles inferior"""
        control_frame = ttk.LabelFrame(parent, text="⚡ Acciones Rápidas", padding="10")
        control_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Botones de acción rápida
        buttons_frame = ttk.Frame(control_frame)
        buttons_frame.pack(fill=tk.X)
        
        quick_buttons = [
            ("🎲 Usuario Aleatorio", self.buscar_aleatorio),
            ("🌟 Nodo Central", self.encontrar_nodo_central),
            ("🔗 Mayor Conexión", self.encontrar_mayor_conexion),
            ("🎨 Colores Aleatorios", self.regenerar_colores),
            ("📷 Captura", self.capturar_pantalla),
        ]
        
        for i, (text, command) in enumerate(quick_buttons):
            btn = ttk.Button(buttons_frame, text=text, command=command, style='Custom.TButton')
            btn.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
    
    def create_status_bar(self, parent):
        """Crea la barra de estado"""
        status_frame = ttk.Frame(parent)
        status_frame.pack(fill=tk.X, pady=(5, 0))
        
        self.status_label = ttk.Label(status_frame, text="✅ Red social cargada correctamente", 
                                     style='Subtitle.TLabel')
        self.status_label.pack(side=tk.LEFT)
        
        # Información de zoom
        self.zoom_label = ttk.Label(status_frame, text="Zoom: 100%", style='Subtitle.TLabel')
        self.zoom_label.pack(side=tk.RIGHT)
    
    def setup_mouse_events(self):
        """Configura los eventos del mouse mejorados"""
        self.canvas.bind("<Button-1>", self.start_pan)
        self.canvas.bind("<B1-Motion>", self.do_pan)
        self.canvas.bind("<ButtonRelease-1>", self.end_pan)
        self.canvas.bind("<MouseWheel>", self.zoom)
        self.canvas.bind("<Button-4>", self.zoom)
        self.canvas.bind("<Button-5>", self.zoom)
        self.canvas.bind("<Motion>", self.on_motion)
        self.canvas.bind("<Double-Button-1>", self.on_double_click)
        self.canvas.bind("<Button-3>", self.show_context_menu)  # Clic derecho
    
    def start_pan(self, event):
        """Inicia el pan con efectos visuales"""
        self.panning = True
        self.last_x = event.x
        self.last_y = event.y
        self.canvas.config(cursor="fleur")
        self.update_status("🖱️ Arrastrando vista...")
    
    def do_pan(self, event):
        """Realiza el pan suave"""
        if self.panning:
            self.canvas.scan_dragto(event.x, event.y, gain=1)
            self.last_x = event.x
            self.last_y = event.y
    
    def end_pan(self, event):
        """Termina el pan"""
        self.panning = False
        self.canvas.config(cursor="")
        self.update_status("✅ Vista actualizada")
    
    def on_motion(self, event):
        """Maneja el movimiento del mouse con feedback"""
        if not self.panning:
            self.canvas.config(cursor="hand1")
    
    def on_double_click(self, event):
        """Maneja doble clic para centrar"""
        self.centrar_vista()
        self.update_status("🎯 Vista centrada")
    
    def show_context_menu(self, event):
        """Muestra menú contextual"""
        context_menu = tk.Menu(self.root, tearoff=0)
        context_menu.add_command(label="🎯 Centrar Vista", command=self.centrar_vista)
        context_menu.add_command(label="🔄 Resetear", command=self.resetear_posiciones)
        context_menu.add_separator()
        context_menu.add_command(label="📊 Estadísticas", command=self.mostrar_estadisticas)
        context_menu.add_command(label="🎨 Nuevo Layout", command=self.generar_layout_aleatorio)
        
        try:
            context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            context_menu.grab_release()
    
    def zoom(self, event):
        """Zoom mejorado con feedback"""
        if event.num == 4 or event.delta > 0:
            factor = 1.1
        elif event.num == 5 or event.delta < 0:
            factor = 0.9
        else:
            return
        
        self.zoom_factor *= factor
        self.canvas.scale("all", event.x, event.y, factor, factor)
        
        bbox = self.canvas.bbox("all")
        if bbox:
            self.canvas.configure(scrollregion=bbox)
        
        # Actualizar etiqueta de zoom
        zoom_percent = int(self.zoom_factor * 100)
        self.zoom_label.config(text=f"Zoom: {zoom_percent}%")
        self.update_status(f"🔍 Zoom: {zoom_percent}%")
    
    def zoom_in(self):
        """Zoom in mejorado"""
        center_x = self.canvas.winfo_width() / 2
        center_y = self.canvas.winfo_height() / 2
        factor = 1.2
        self.zoom_factor *= factor
        self.canvas.scale("all", center_x, center_y, factor, factor)
        self.update_zoom_display()
    
    def zoom_out(self):
        """Zoom out mejorado"""
        center_x = self.canvas.winfo_width() / 2
        center_y = self.canvas.winfo_height() / 2
        factor = 0.8
        self.zoom_factor *= factor
        self.canvas.scale("all", center_x, center_y, factor, factor)
        self.update_zoom_display()
    
    def reset_zoom(self):
        """Reset zoom mejorado"""
        if self.zoom_factor != 1.0:
            center_x = self.canvas.winfo_width() / 2
            center_y = self.canvas.winfo_height() / 2
            factor = 1.0 / self.zoom_factor
            self.zoom_factor = 1.0
            self.canvas.scale("all", center_x, center_y, factor, factor)
            self.update_zoom_display()
    
    def update_zoom_display(self):
        """Actualiza la visualización del zoom"""
        bbox = self.canvas.bbox("all")
        if bbox:
            self.canvas.configure(scrollregion=bbox)
        zoom_percent = int(self.zoom_factor * 100)
        self.zoom_label.config(text=f"Zoom: {zoom_percent}%")
    
    def centrar_vista(self):
        """Centra la vista con animación suave"""
        bbox = self.canvas.bbox("all")
        if bbox:
            content_center_x = (bbox[0] + bbox[2]) / 2
            content_center_y = (bbox[1] + bbox[3]) / 2
            
            canvas_center_x = self.canvas.winfo_width() / 2
            canvas_center_y = self.canvas.winfo_height() / 2
            
            dx = canvas_center_x - content_center_x
            dy = canvas_center_y - content_center_y
            
            self.canvas.move("all", dx, dy)
            
            new_bbox = self.canvas.bbox("all")
            if new_bbox:
                self.canvas.configure(scrollregion=new_bbox)
        
        self.update_status("🎯 Vista centrada correctamente")
    
    def inicializar_grafo(self):
        """Inicializa el grafo con datos mejorados"""
        for i in range(1, 31):
            self.usuarios.append(f"User{i}")
        
        n = len(self.usuarios)
        self.matriz_adyacencia = [[0 for _ in range(n)] for _ in range(n)]
        self.matriz_pesos = [[0 for _ in range(n)] for _ in range(n)]
        
        # Generar conexiones más realistas
        for i in range(n):
            conexiones = 2 + self.random.randint(0, 4)
            for j in range(conexiones):
                destino = self.random.randint(0, n-1)
                if i != destino:
                    self.matriz_adyacencia[i][destino] = 1
                    self.matriz_adyacencia[destino][i] = 1
                    peso = 1 + self.random.randint(0, 9)
                    self.matriz_pesos[i][destino] = peso
                    self.matriz_pesos[destino][i] = peso
        
        self.detectar_componentes_por_peso()
        self.update_stats()
    
    def detectar_componentes_por_peso(self):
        """Detecta componentes con colores mejorados"""
        n = len(self.usuarios)
        self.componente = [-1] * n
        self.colores = []
        componente_id = 0
        
        # Paleta de colores más atractiva
        color_palette = [
            "#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#FFEAA7",
            "#DDA0DD", "#98D8C8", "#F7DC6F", "#BB8FCE", "#85C1E9",
            "#F8C471", "#82E0AA", "#F1948A", "#85C1E9", "#D7BDE2"
        ]
        
        for i in range(n):
            if self.componente[i] == -1:
                self.dfs_por_peso(i, componente_id)
                if componente_id < len(color_palette):
                    self.colores.append(color_palette[componente_id])
                else:
                    # Generar color aleatorio si se agotan los predefinidos
                    color = f"#{self.random.randint(0, 255):02x}{self.random.randint(0, 255):02x}{self.random.randint(0, 255):02x}"
                    self.colores.append(color)
                componente_id += 1
    
    def dfs_por_peso(self, nodo: int, id: int):
        """DFS mejorado"""
        self.componente[nodo] = id
        for i in range(len(self.usuarios)):
            if (self.matriz_adyacencia[nodo][i] == 1 and 
                self.matriz_pesos[nodo][i] >= self.umbral_peso and 
                self.componente[i] == -1):
                self.dfs_por_peso(i, id)
    
    def generar_posiciones(self):
        """Genera posiciones con diferentes layouts"""
        self.posiciones = []
        centro_x = 0
        centro_y = 0
        radio = 400
        
        for i in range(len(self.usuarios)):
            angulo = 2 * math.pi * i / len(self.usuarios)
            x = int(centro_x + radio * math.cos(angulo))
            y = int(centro_y + radio * math.sin(angulo))
            self.posiciones.append(Point(x, y))
    
    def generar_layout_aleatorio(self):
        """Genera un layout aleatorio más interesante"""
        layouts = ['circular', 'grid', 'random', 'spiral', 'clusters']
        layout = self.random.choice(layouts)
        
        self.posiciones = []
        n = len(self.usuarios)
        
        if layout == 'circular':
            self.generar_posiciones()  # Layout circular original
        
        elif layout == 'grid':
            # Layout en cuadrícula
            cols = int(math.ceil(math.sqrt(n)))
            for i in range(n):
                x = (i % cols) * 100 - (cols * 50)
                y = (i // cols) * 100 - (cols * 50)
                self.posiciones.append(Point(x, y))
        
        elif layout == 'random':
            # Layout completamente aleatorio
            for i in range(n):
                x = self.random.randint(-400, 400)
                y = self.random.randint(-400, 400)
                self.posiciones.append(Point(x, y))
        
        elif layout == 'spiral':
            # Layout en espiral
            for i in range(n):
                angle = i * 0.5
                radius = i * 15
                x = int(radius * math.cos(angle))
                y = int(radius * math.sin(angle))
                self.posiciones.append(Point(x, y))
        
        elif layout == 'clusters':
            # Layout por clusters/componentes
            component_centers = {}
            for comp_id in set(self.componente):
                angle = comp_id * 2 * math.pi / len(set(self.componente))
                center_x = int(200 * math.cos(angle))
                center_y = int(200 * math.sin(angle))
                component_centers[comp_id] = (center_x, center_y)
            
            component_counts = {}
            for i, comp_id in enumerate(self.componente):
                if comp_id not in component_counts:
                    component_counts[comp_id] = 0
                
                center_x, center_y = component_centers[comp_id]
                angle = component_counts[comp_id] * 0.8
                radius = 50 + component_counts[comp_id] * 10
                
                x = int(center_x + radius * math.cos(angle))
                y = int(center_y + radius * math.sin(angle))
                self.posiciones.append(Point(x, y))
                
                component_counts[comp_id] += 1
        
        self.dibujar_grafo()
        self.centrar_vista()
        self.update_status(f"🎨 Layout '{layout}' aplicado")
    
    def dibujar_grafo(self):
        """Dibuja el grafo con efectos visuales mejorados"""
        self.canvas.delete("all")
        
        # Dibujar cuadrícula si está habilitada
        if self.show_grid_var.get():
            self.dibujar_cuadricula()
        
        # Dibujar aristas con efectos
        for i in range(len(self.usuarios)):
            for j in range(i + 1, len(self.usuarios)):
                if self.matriz_adyacencia[i][j] == 1:
                    self.dibujar_arista(i, j)
        
        # Dibujar nodos con efectos
        for i in range(len(self.usuarios)):
            self.dibujar_nodo(i)
        
        # Actualizar scroll region
        bbox = self.canvas.bbox("all")
        if bbox:
            margin = 100
            self.canvas.configure(scrollregion=(bbox[0]-margin, bbox[1]-margin, 
                                              bbox[2]+margin, bbox[3]+margin))
    
    def dibujar_cuadricula(self):
        """Dibuja una cuadrícula de fondo"""
        for x in range(-1000, 1001, 50):
            self.canvas.create_line(x, -1000, x, 1000, fill="#f0f0f0", width=1, tags="grid")
        for y in range(-1000, 1001, 50):
            self.canvas.create_line(-1000, y, 1000, y, fill="#f0f0f0", width=1, tags="grid")
    
    def dibujar_arista(self, i: int, j: int):
        """Dibuja una arista con efectos visuales"""
        p1 = self.posiciones[i]
        p2 = self.posiciones[j]
        peso = self.matriz_pesos[i][j]
        
        # Determinar estilo de la arista
        if peso >= self.umbral_peso:
            color_arista = "#2E86AB"
            ancho = 3
            dash = None
        else:
            color_arista = "#BDC3C7"
            ancho = 1
            dash = (2, 2)
        
        # Resaltar si está en la lista de aristas destacadas
        if (i, j) in self.highlighted_edges or (j, i) in self.highlighted_edges:
            color_arista = "#E74C3C"
            ancho = 4
        
        # Dibujar la línea
        line_id = self.canvas.create_line(p1.x, p1.y, p2.x, p2.y, 
                                         fill=color_arista, width=ancho, 
                                         dash=dash, tags="graph")
        
        # Mostrar peso si está habilitado
        if self.show_weights_var.get():
            mid_x = (p1.x + p2.x) // 2
            mid_y = (p1.y + p2.y) // 2
            
            # Fondo para el texto del peso
            self.canvas.create_oval(mid_x-8, mid_y-8, mid_x+8, mid_y+8, 
                                   fill="white", outline="#ddd", width=1, tags="graph")
            
            self.canvas.create_text(mid_x, mid_y, text=str(peso), 
                                   fill="#2C3E50", font=("Arial", 8, "bold"), tags="graph")
    
    def dibujar_nodo(self, i: int):
        """Dibuja un nodo con efectos visuales mejorados"""
        p = self.posiciones[i]
        color = self.colores[self.componente[i] % len(self.colores)] if self.colores else "#3498DB"
        
        # Tamaño del nodo basado en conexiones
        conexiones = sum(self.matriz_adyacencia[i])
        radio = 15 + min(conexiones * 2, 10)
        
        # Resaltar si está en la lista de nodos destacados
        if i in self.highlighted_nodes:
            # Efecto de brillo
            self.canvas.create_oval(p.x - radio - 5, p.y - radio - 5, 
                                   p.x + radio + 5, p.y + radio + 5, 
                                   fill="#FFD700", outline="#FFA500", width=3, tags="graph")
        
        # Sombra del nodo
        self.canvas.create_oval(p.x - radio + 2, p.y - radio + 2, 
                               p.x + radio + 2, p.y + radio + 2, 
                               fill="#34495E", outline="", tags="graph")
        
        # Nodo principal con gradiente simulado
        self.canvas.create_oval(p.x - radio, p.y - radio, 
                               p.x + radio, p.y + radio, 
                               fill=color, outline="#2C3E50", width=2, tags="graph")
        
        # Highlight interno
        self.canvas.create_oval(p.x - radio + 3, p.y - radio + 3, 
                               p.x - radio + 8, p.y - radio + 8, 
                               fill="white", outline="", tags="graph")
        
        # Etiqueta del usuario si está habilitada
        if self.show_labels_var.get():
            self.canvas.create_text(p.x, p.y - radio - 15, text=self.usuarios[i], 
                                   fill="#2C3E50", font=("Arial", 9, "bold"), tags="graph")
        
        # Mostrar número de conexiones
        self.canvas.create_text(p.x, p.y, text=str(conexiones), 
                               fill="white", font=("Arial", 8, "bold"), tags="graph")
    
    def toggle_grid(self):
        """Alterna la visualización de la cuadrícula"""
        self.dibujar_grafo()
        status = "activada" if self.show_grid_var.get() else "desactivada"
        self.update_status(f"📐 Cuadrícula {status}")
    
    def toggle_dark_mode(self):
        """Alterna entre modo claro y oscuro"""
        self.dark_mode = not self.dark_mode
        
        if self.dark_mode:
            bg_color = "#2C3E50"
            canvas_color = "#34495E"
            text_color = "#ECF0F1"
            self.dark_mode_btn.config(text="☀️")
        else:
            bg_color = "#f0f0f0"
            canvas_color = "white"
            text_color = "#2C3E50"
            self.dark_mode_btn.config(text="🌙")
        
        self.root.configure(bg=bg_color)
        self.canvas.configure(bg=canvas_color)
        self.dibujar_grafo()
        self.update_status(f"🎨 Modo {'oscuro' if self.dark_mode else 'claro'} activado")
    
    def buscar_interaccion(self):
        """Busca interacciones con efectos visuales mejorados"""
        nombre = self.entrada_usuario.get().strip()
        if not nombre:
            self.update_status("⚠️ Ingresa un nombre de usuario")
            return
        
        try:
            index = self.usuarios.index(nombre)
        except ValueError:
            messagebox.showinfo("❌ Error", f"Usuario no encontrado: {nombre}")
            self.update_status(f"❌ Usuario '{nombre}' no encontrado")
            return
        
        max_peso = -1
        usuario_relacionado = ""
        detalles = []
        
        for j in range(len(self.usuarios)):
            if self.matriz_adyacencia[index][j] == 1:
                peso = self.matriz_pesos[index][j]
                detalles.append(f"🔗 Con {self.usuarios[j]} (peso: {peso})")
                if peso > max_peso:
                    max_peso = peso
                    usuario_relacionado = self.usuarios[j]
        
        if usuario_relacionado:
            mensaje = "\n".join(detalles)
            mensaje += f"\n\n⭐ Mayor interacción: {usuario_relacionado} (peso: {max_peso})"
            messagebox.showinfo(f"📊 Interacciones de {nombre}", mensaje)
            
            # Resaltar visualmente
            self.resaltar_conexion(index, self.usuarios.index(usuario_relacionado))
            self.update_status(f"✅ Mostrando interacciones de {nombre}")
        else:
            messagebox.showinfo("ℹ️ Sin conexiones", f"{nombre} no tiene conexiones.")
            self.update_status(f"ℹ️ {nombre} no tiene conexiones")
    
    def buscar_aleatorio(self):
        """Busca un usuario aleatorio"""
        usuario_aleatorio = self.random.choice(self.usuarios)
        self.entrada_usuario.delete(0, tk.END)
        self.entrada_usuario.insert(0, usuario_aleatorio)
        self.buscar_interaccion()
    
    def encontrar_nodo_central(self):
        """Encuentra el nodo con más conexiones"""
        max_conexiones = -1
        nodo_central = -1
        
        for i in range(len(self.usuarios)):
            conexiones = sum(self.matriz_adyacencia[i])
            if conexiones > max_conexiones:
                max_conexiones = conexiones
                nodo_central = i
        
        if nodo_central != -1:
            self.highlighted_nodes = [nodo_central]
            self.dibujar_grafo()
            self.centrar_en_nodo(nodo_central)
            
            usuario = self.usuarios[nodo_central]
            messagebox.showinfo("🌟 Nodo Central", 
                               f"El nodo más conectado es:\n{usuario}\nCon {max_conexiones} conexiones")
            self.update_status(f"🌟 Nodo central: {usuario} ({max_conexiones} conexiones)")
    
    def encontrar_mayor_conexion(self):
        """Encuentra la conexión con mayor peso"""
        max_peso = -1
        mejor_conexion = None
        
        for i in range(len(self.usuarios)):
            for j in range(i + 1, len(self.usuarios)):
                if self.matriz_adyacencia[i][j] == 1:
                    peso = self.matriz_pesos[i][j]
                    if peso > max_peso:
                        max_peso = peso
                        mejor_conexion = (i, j)
        
        if mejor_conexion:
            i, j = mejor_conexion
            self.resaltar_conexion(i, j)
            
            usuario1 = self.usuarios[i]
            usuario2 = self.usuarios[j]
            messagebox.showinfo("🔗 Mayor Conexión", 
                               f"La conexión más fuerte es:\n{usuario1} ↔ {usuario2}\nPeso: {max_peso}")
            self.update_status(f"🔗 Mayor conexión: {usuario1} ↔ {usuario2} (peso: {max_peso})")
    
    def regenerar_colores(self):
        """Regenera los colores de los componentes"""
        self.detectar_componentes_por_peso()
        self.dibujar_grafo()
        self.update_status("🎨 Colores regenerados")
    
    def capturar_pantalla(self):
        """Simula captura de pantalla"""
        messagebox.showinfo("📷 Captura", "Funcionalidad de captura no implementada\nen esta versión de demostración")
        self.update_status("📷 Captura solicitada")
    
    def centrar_en_nodo(self, nodo_index: int):
        """Centra la vista en un nodo específico"""
        p = self.posiciones[nodo_index]
        canvas_center_x = self.canvas.winfo_width() / 2
        canvas_center_y = self.canvas.winfo_height() / 2
        
        dx = canvas_center_x - p.x
        dy = canvas_center_y - p.y
        
        self.canvas.move("all", dx, dy)
        
        bbox = self.canvas.bbox("all")
        if bbox:
            self.canvas.configure(scrollregion=bbox)
    
    def resaltar_conexion(self, nodo1: int, nodo2: int):
        """Resalta una conexión específica con animación"""
        # Limpiar resaltados anteriores
        self.highlighted_nodes = [nodo1, nodo2]
        self.highlighted_edges = [(nodo1, nodo2)]
        
        # Redibujar con resaltado
        self.dibujar_grafo()
        
        # Centrar en la conexión
        p1 = self.posiciones[nodo1]
        p2 = self.posiciones[nodo2]
        center_x = (p1.x + p2.x) / 2
        center_y = (p1.y + p2.y) / 2
        
        canvas_center_x = self.canvas.winfo_width() / 2
        canvas_center_y = self.canvas.winfo_height() / 2
        
        dx = canvas_center_x - center_x
        dy = canvas_center_y - center_y
        self.canvas.move("all", dx, dy)
        
        # Limpiar resaltado después de 5 segundos
        self.root.after(5000, self.limpiar_resaltados)
    
    def limpiar_resaltados(self):
        """Limpia los resaltados visuales"""
        self.highlighted_nodes = []
        self.highlighted_edges = []
        self.dibujar_grafo()
        self.update_status("✨ Resaltados limpiados")
    
    def resetear_posiciones(self):
        """Resetea las posiciones con confirmación"""
        self.generar_posiciones()
        self.limpiar_resaltados()
        self.dibujar_grafo()
        self.centrar_vista()
        self.update_status("🔄 Posiciones reseteadas al layout circular")
    
    def regenerar_red(self):
        """Regenera completamente la red"""
        respuesta = messagebox.askyesno("🔄 Regenerar Red", 
                                       "¿Estás seguro de que quieres generar una nueva red?\nSe perderán todas las conexiones actuales.")
        if respuesta:
            self.inicializar_grafo()
            self.detectar_componentes_por_peso()
            self.generar_posiciones()
            self.dibujar_grafo()
            self.centrar_vista()
            self.update_status("🆕 Nueva red generada correctamente")
    
    def actualizar_umbral(self, valor):
        """Actualiza el umbral con feedback visual"""
        self.umbral_peso = int(float(valor))
        self.umbral_label.config(text=f"Valor: {self.umbral_peso}")
        self.detectar_componentes_por_peso()
        self.dibujar_grafo()
        self.update_stats()
        self.update_status(f"⚖️ Umbral actualizado a {self.umbral_peso}")
    
    def mostrar_estadisticas(self):
        """Muestra estadísticas detalladas de la red"""
        n = len(self.usuarios)
        total_conexiones = sum(sum(row) for row in self.matriz_adyacencia) // 2
        componentes = len(set(self.componente))
        
        # Calcular estadísticas adicionales
        pesos = []
        for i in range(n):
            for j in range(i + 1, n):
                if self.matriz_adyacencia[i][j] == 1:
                    pesos.append(self.matriz_pesos[i][j])
        
        peso_promedio = sum(pesos) / len(pesos) if pesos else 0
        peso_max = max(pesos) if pesos else 0
        peso_min = min(pesos) if pesos else 0
        
        # Nodo más conectado
        max_conexiones = max(sum(self.matriz_adyacencia[i]) for i in range(n))
        nodos_centrales = [self.usuarios[i] for i in range(n) if sum(self.matriz_adyacencia[i]) == max_conexiones]
        
        estadisticas = f"""📊 ESTADÍSTICAS DE LA RED SOCIAL
        
👥 Usuarios: {n}
🔗 Conexiones totales: {total_conexiones}
🎨 Componentes: {componentes}
⚖️ Umbral actual: {self.umbral_peso}

📈 ANÁLISIS DE PESOS:
• Peso promedio: {peso_promedio:.2f}
• Peso máximo: {peso_max}
• Peso mínimo: {peso_min}

🌟 NODOS CENTRALES:
• Máximo conexiones: {max_conexiones}
• Usuarios: {', '.join(nodos_centrales[:3])}{'...' if len(nodos_centrales) > 3 else ''}

🔍 ZOOM ACTUAL: {int(self.zoom_factor * 100)}%"""
        
        messagebox.showinfo("📊 Estadísticas de Red", estadisticas)
        self.update_status("📊 Estadísticas mostradas")
    
    def update_stats(self):
        """Actualiza las estadísticas en tiempo real"""
        n = len(self.usuarios)
        conexiones = sum(sum(row) for row in self.matriz_adyacencia) // 2
        componentes = len(set(self.componente))
        
        stats_text = f"👥 {n} usuarios | 🔗 {conexiones} conexiones | 🎨 {componentes} componentes | ⚖️ Umbral: {self.umbral_peso}"
        self.stats_label.config(text=stats_text)
    
    def update_status(self, mensaje: str):
        """Actualiza la barra de estado"""
        self.status_label.config(text=mensaje)
        # Auto-limpiar después de 3 segundos
        self.root.after(3000, lambda: self.status_label.config(text="✅ Listo"))
    
    def start_animations(self):
        """Inicia las animaciones de la interfaz"""
        self.animate_title()
    
    def animate_title(self):
        """Anima el título con efectos sutiles"""
        self.animation_frame += 1
        # Aquí podrías agregar efectos de animación más complejos
        self.root.after(100, self.animate_title)
    
    def ejecutar(self):
        """Ejecuta la aplicación"""
        self.root.mainloop()

def main():
    """Función principal"""
    try:
        app = RedSocialGrafica()
        app.ejecutar()
    except Exception as e:
        print(f"Error al iniciar la aplicación: {e}")
        messagebox.showerror("Error", f"Error al iniciar la aplicación:\n{e}")

if __name__ == "__main__":
    main()