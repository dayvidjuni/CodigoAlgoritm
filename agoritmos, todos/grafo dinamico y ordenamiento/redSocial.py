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
        
        # Configurar ventana
        self.root = tk.Tk()
        self.root.title("Red Social Interactiva - Vista Navegable")
        self.root.geometry("1024x1024")
        
        # Crear canvas con scrollbars
        self.canvas_frame = tk.Frame(self.root)
        self.canvas_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.canvas = tk.Canvas(self.canvas_frame, width=1000, height=1000, bg="white", 
                               scrollregion=(-2000, -2000, 2000, 2000))
        
        # Scrollbars
        self.h_scrollbar = tk.Scrollbar(self.canvas_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.v_scrollbar = tk.Scrollbar(self.canvas_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.canvas.configure(xscrollcommand=self.h_scrollbar.set, yscrollcommand=self.v_scrollbar.set)
        
        # Empaquetar canvas y scrollbars
        self.h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Configurar eventos del mouse para pan
        self.canvas.bind("<Button-1>", self.start_pan)
        self.canvas.bind("<B1-Motion>", self.do_pan)
        self.canvas.bind("<ButtonRelease-1>", self.end_pan)
        self.canvas.bind("<MouseWheel>", self.zoom)  # Windows
        self.canvas.bind("<Button-4>", self.zoom)    # Linux
        self.canvas.bind("<Button-5>", self.zoom)    # Linux
        
        # Cambiar cursor cuando se hace pan
        self.canvas.bind("<Motion>", self.on_motion)
        
        # Crear controles
        self.crear_controles()
        
        # Inicializar datos
        self.inicializar_grafo()
        self.detectar_componentes_por_peso()
        self.generar_posiciones()
        self.dibujar_grafo()
        
        # Centrar la vista inicialmente
        self.centrar_vista()
    
    def crear_controles(self):
        control_frame = tk.Frame(self.root)
        control_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=5)
        
        # Primera fila de controles
        fila1 = tk.Frame(control_frame)
        fila1.pack(fill=tk.X, pady=2)
        
        # Campo de entrada para usuario
        tk.Label(fila1, text="Usuario:").pack(side=tk.LEFT)
        self.entrada_usuario = tk.Entry(fila1, width=15)
        self.entrada_usuario.pack(side=tk.LEFT, padx=5)
        
        # Botón de búsqueda
        boton_buscar = tk.Button(fila1, text="Buscar Interacción", 
                                command=self.buscar_interaccion)
        boton_buscar.pack(side=tk.LEFT, padx=5)
        
        # Botón para centrar vista
        boton_centrar = tk.Button(fila1, text="Centrar Vista", 
                                 command=self.centrar_vista)
        boton_centrar.pack(side=tk.LEFT, padx=5)
        
        # Botón para resetear posiciones
        boton_reset = tk.Button(fila1, text="Resetear Posiciones", 
                               command=self.resetear_posiciones)
        boton_reset.pack(side=tk.LEFT, padx=5)
        
        # Segunda fila de controles
        fila2 = tk.Frame(control_frame)
        fila2.pack(fill=tk.X, pady=2)
        
        # Slider para umbral
        tk.Label(fila2, text="Umbral de Peso:").pack(side=tk.LEFT, padx=(0, 5))
        self.slider = tk.Scale(fila2, from_=1, to=10, orient=tk.HORIZONTAL, 
                              command=self.actualizar_umbral)
        self.slider.set(5)
        self.slider.pack(side=tk.LEFT, padx=5)
        
        # Controles de zoom
        tk.Label(fila2, text="Zoom:").pack(side=tk.LEFT, padx=(20, 5))
        boton_zoom_in = tk.Button(fila2, text="🔍+", command=self.zoom_in, width=3)
        boton_zoom_in.pack(side=tk.LEFT, padx=2)
        boton_zoom_out = tk.Button(fila2, text="🔍-", command=self.zoom_out, width=3)
        boton_zoom_out.pack(side=tk.LEFT, padx=2)
        boton_zoom_reset = tk.Button(fila2, text="1:1", command=self.reset_zoom, width=3)
        boton_zoom_reset.pack(side=tk.LEFT, padx=2)
        
        # Etiqueta de instrucciones
        fila3 = tk.Frame(control_frame)
        fila3.pack(fill=tk.X, pady=2)
        instrucciones = tk.Label(fila3, text="💡 Arrastra para mover la vista | Rueda del mouse para zoom | Usa las barras de desplazamiento", 
                                fg="blue", font=("Arial", 9))
        instrucciones.pack()
    
    def start_pan(self, event):
        """Inicia el pan de la vista"""
        self.panning = True
        self.last_x = event.x
        self.last_y = event.y
        self.canvas.config(cursor="fleur")  # Cursor de mano cerrada
    
    def do_pan(self, event):
        """Realiza el pan de la vista"""
        if self.panning:
            # Calcular el desplazamiento
            dx = event.x - self.last_x
            dy = event.y - self.last_y
            
            # Mover la vista del canvas
            self.canvas.scan_dragto(event.x, event.y, gain=1)
            
            # Actualizar posición del mouse
            self.last_x = event.x
            self.last_y = event.y
    
    def end_pan(self, event):
        """Termina el pan de la vista"""
        self.panning = False
        self.canvas.config(cursor="")
    
    def on_motion(self, event):
        """Cambia el cursor cuando no se está haciendo pan"""
        if not self.panning:
            self.canvas.config(cursor="hand1")
    
    def zoom(self, event):
        """Maneja el zoom con la rueda del mouse"""
        # Determinar dirección del zoom
        if event.num == 4 or event.delta > 0:
            factor = 1.1
        elif event.num == 5 or event.delta < 0:
            factor = 0.9
        else:
            return
        
        # Aplicar zoom
        self.zoom_factor *= factor
        self.canvas.scale("all", event.x, event.y, factor, factor)
        
        # Actualizar scroll region
        bbox = self.canvas.bbox("all")
        if bbox:
            self.canvas.configure(scrollregion=bbox)
    
    def zoom_in(self):
        """Zoom in desde el centro"""
        center_x = self.canvas.winfo_width() / 2
        center_y = self.canvas.winfo_height() / 2
        factor = 1.2
        self.zoom_factor *= factor
        self.canvas.scale("all", center_x, center_y, factor, factor)
        bbox = self.canvas.bbox("all")
        if bbox:
            self.canvas.configure(scrollregion=bbox)
    
    def zoom_out(self):
        """Zoom out desde el centro"""
        center_x = self.canvas.winfo_width() / 2
        center_y = self.canvas.winfo_height() / 2
        factor = 0.8
        self.zoom_factor *= factor
        self.canvas.scale("all", center_x, center_y, factor, factor)
        bbox = self.canvas.bbox("all")
        if bbox:
            self.canvas.configure(scrollregion=bbox)
    
    def reset_zoom(self):
        """Resetea el zoom a 1:1"""
        if self.zoom_factor != 1.0:
            center_x = self.canvas.winfo_width() / 2
            center_y = self.canvas.winfo_height() / 2
            factor = 1.0 / self.zoom_factor
            self.zoom_factor = 1.0
            self.canvas.scale("all", center_x, center_y, factor, factor)
            bbox = self.canvas.bbox("all")
            if bbox:
                self.canvas.configure(scrollregion=bbox)
    
    def centrar_vista(self):
        """Centra la vista en el grafo"""
        # Obtener el bounding box de todos los elementos
        bbox = self.canvas.bbox("all")
        if bbox:
            # Calcular el centro del contenido
            content_center_x = (bbox[0] + bbox[2]) / 2
            content_center_y = (bbox[1] + bbox[3]) / 2
            
            # Calcular el centro del canvas visible
            canvas_center_x = self.canvas.winfo_width() / 2
            canvas_center_y = self.canvas.winfo_height() / 2
            
            # Calcular el desplazamiento necesario
            dx = canvas_center_x - content_center_x
            dy = canvas_center_y - content_center_y
            
            # Mover todo el contenido
            self.canvas.move("all", dx, dy)
            
            # Actualizar scroll region
            new_bbox = self.canvas.bbox("all")
            if new_bbox:
                self.canvas.configure(scrollregion=new_bbox)
    
    def inicializar_grafo(self):
        # Crear usuarios
        for i in range(1, 31):
            self.usuarios.append(f"User{i}")
        
        n = len(self.usuarios)
        self.matriz_adyacencia = [[0 for _ in range(n)] for _ in range(n)]
        self.matriz_pesos = [[0 for _ in range(n)] for _ in range(n)]
        
        # Generar conexiones aleatorias
        for i in range(n):
            conexiones = 2 + self.random.randint(0, 3)
            for j in range(conexiones):
                destino = self.random.randint(0, n-1)
                if i != destino:
                    self.matriz_adyacencia[i][destino] = 1
                    self.matriz_adyacencia[destino][i] = 1
                    peso = 1 + self.random.randint(0, 9)
                    self.matriz_pesos[i][destino] = peso
                    self.matriz_pesos[destino][i] = peso
        
        self.detectar_componentes_por_peso()
    
    def detectar_componentes_por_peso(self):
        n = len(self.usuarios)
        self.componente = [-1] * n
        self.colores = []
        componente_id = 0
        
        for i in range(n):
            if self.componente[i] == -1:
                self.dfs_por_peso(i, componente_id)
                # Generar color aleatorio
                color = f"#{self.random.randint(0, 255):02x}{self.random.randint(0, 255):02x}{self.random.randint(0, 255):02x}"
                self.colores.append(color)
                componente_id += 1
    
    def dfs_por_peso(self, nodo: int, id: int):
        self.componente[nodo] = id
        for i in range(len(self.usuarios)):
            if (self.matriz_adyacencia[nodo][i] == 1 and 
                self.matriz_pesos[nodo][i] >= self.umbral_peso and 
                self.componente[i] == -1):
                self.dfs_por_peso(i, id)
    
    def generar_posiciones(self):
        self.posiciones = []
        centro_x = 0  # Centrado en el origen
        centro_y = 0
        radio = 400
        
        for i in range(len(self.usuarios)):
            angulo = 2 * math.pi * i / len(self.usuarios)
            x = int(centro_x + radio * math.cos(angulo))
            y = int(centro_y + radio * math.sin(angulo))
            self.posiciones.append(Point(x, y))
    
    def resetear_posiciones(self):
        """Resetea las posiciones de los nodos a la disposición circular original"""
        self.generar_posiciones()
        self.dibujar_grafo()
        self.centrar_vista()
    
    def dibujar_grafo(self):
        self.canvas.delete("all")
        
        # Dibujar aristas
        for i in range(len(self.usuarios)):
            for j in range(i + 1, len(self.usuarios)):
                if self.matriz_adyacencia[i][j] == 1:
                    p1 = self.posiciones[i]
                    p2 = self.posiciones[j]
                    
                    # Color de la arista basado en el peso
                    peso = self.matriz_pesos[i][j]
                    if peso >= self.umbral_peso:
                        color_arista = "darkblue"
                        ancho = 2
                    else:
                        color_arista = "lightgray"
                        ancho = 1
                    
                    self.canvas.create_line(p1.x, p1.y, p2.x, p2.y, 
                                          fill=color_arista, width=ancho, tags="graph")
                    
                    # Mostrar peso en el medio de la arista
                    mid_x = (p1.x + p2.x) // 2
                    mid_y = (p1.y + p2.y) // 2
                    self.canvas.create_text(mid_x, mid_y, text=str(peso), 
                                          fill="black", font=("Arial", 8), tags="graph")
        
        # Dibujar nodos
        for i in range(len(self.usuarios)):
            p = self.posiciones[i]
            color = self.colores[self.componente[i] % len(self.colores)] if self.colores else "lightblue"
            
            # Dibujar nodo principal
            self.canvas.create_oval(p.x - 15, p.y - 15, p.x + 15, p.y + 15, 
                                  fill=color, outline="black", width=2, tags="graph")
            
            # Etiqueta del usuario
            self.canvas.create_text(p.x, p.y - 25, text=self.usuarios[i], 
                                  fill="black", font=("Arial", 9, "bold"), tags="graph")
        
        # Actualizar scroll region
        bbox = self.canvas.bbox("all")
        if bbox:
            # Expandir un poco el área de scroll
            margin = 100
            self.canvas.configure(scrollregion=(bbox[0]-margin, bbox[1]-margin, 
                                              bbox[2]+margin, bbox[3]+margin))
    
    def buscar_interaccion(self):
        nombre = self.entrada_usuario.get().strip()
        if not nombre:
            return
        
        try:
            index = self.usuarios.index(nombre)
        except ValueError:
            messagebox.showinfo("Error", f"Usuario no encontrado: {nombre}")
            return
        
        max_peso = -1
        usuario_relacionado = ""
        detalles = []
        
        for j in range(len(self.usuarios)):
            if self.matriz_adyacencia[index][j] == 1:
                peso = self.matriz_pesos[index][j]
                detalles.append(f"Con {self.usuarios[j]} (peso: {peso})")
                if peso > max_peso:
                    max_peso = peso
                    usuario_relacionado = self.usuarios[j]
        
        if usuario_relacionado:
            mensaje = "\n".join(detalles)
            mensaje += f"\n\nMayor interacción: {usuario_relacionado} (peso: {max_peso})"
            messagebox.showinfo(f"Interacciones de {nombre}", mensaje)
            
            # Resaltar visualmente el nodo buscado y su mayor conexión
            self.resaltar_conexion(index, self.usuarios.index(usuario_relacionado))
        else:
            messagebox.showinfo("Sin conexiones", f"{nombre} no tiene conexiones.")
    
    def resaltar_conexion(self, nodo1: int, nodo2: int):
        """Resalta visualmente una conexión específica"""
        # Redibujar el grafo
        self.dibujar_grafo()
        
        # Resaltar la conexión específica
        p1 = self.posiciones[nodo1]
        p2 = self.posiciones[nodo2]
        
        # Línea resaltada
        self.canvas.create_line(p1.x, p1.y, p2.x, p2.y, 
                              fill="red", width=4, tags="highlight")
        
        # Nodos resaltados
        self.canvas.create_oval(p1.x - 18, p1.y - 18, p1.x + 18, p1.y + 18, 
                              fill="", outline="red", width=3, tags="highlight")
        self.canvas.create_oval(p2.x - 18, p2.y - 18, p2.x + 18, p2.y + 18, 
                              fill="", outline="red", width=3, tags="highlight")
        
        # Centrar la vista en la conexión resaltada
        center_x = (p1.x + p2.x) / 2
        center_y = (p1.y + p2.y) / 2
        canvas_center_x = self.canvas.winfo_width() / 2
        canvas_center_y = self.canvas.winfo_height() / 2
        
        dx = canvas_center_x - center_x
        dy = canvas_center_y - center_y
        self.canvas.move("all", dx, dy)
        
        # Eliminar resaltado después de 3 segundos
        self.root.after(3000, lambda: self.canvas.delete("highlight"))
    
    def actualizar_umbral(self, valor):
        self.umbral_peso = int(valor)
        self.detectar_componentes_por_peso()
        self.dibujar_grafo()
    
    def mostrar_mayor_interaccion(self, nombre_usuario: str):
        """Método equivalente al original de Java"""
        try:
            index = self.usuarios.index(nombre_usuario)
        except ValueError:
            messagebox.showinfo("Error", f"Usuario no encontrado: {nombre_usuario}")
            return
        
        max_peso = -1
        usuario_relacionado = ""
        detalles = []
        
        for j in range(len(self.usuarios)):
            if self.matriz_adyacencia[index][j] == 1:
                peso = self.matriz_pesos[index][j]
                detalles.append(f"Con {self.usuarios[j]} (peso: {peso})")
                if peso > max_peso:
                    max_peso = peso
                    usuario_relacionado = self.usuarios[j]
        
        if usuario_relacionado:
            mensaje = "\n".join(detalles)
            mensaje += f"\n\nMayor interacción: {usuario_relacionado} (peso: {max_peso})"
            messagebox.showinfo(f"Interacciones de {nombre_usuario}", mensaje)
        else:
            messagebox.showinfo("Sin conexiones", f"{nombre_usuario} no tiene conexiones.")
    
    def ejecutar(self):
        self.root.mainloop()

def main():
    app = RedSocialGrafica()
    app.ejecutar()

if __name__ == "__main__":
    main()