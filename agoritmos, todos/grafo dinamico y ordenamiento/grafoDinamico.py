import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import heapq
import random
from collections import defaultdict
import math

class Nodo:
    def __init__(self, nombre, x, y):
        self.nombre = nombre
        self.x = x
        self.y = y

class Arista:
    def __init__(self, desde, hasta, peso):
        self.desde = desde
        self.hasta = hasta
        self.peso = peso

class GrafoDinamico:
    def __init__(self, root):
        self.root = root
        self.root.title("Grafo Transporte - Entrada Manual")
        self.root.geometry("800x600")
        
        self.nodos = {}
        self.aristas = []
        self.ruta_corta = []
        
        self.setup_ui()
        
    def setup_ui(self):
        # Frame superior para entrada de datos
        top_frame = ttk.Frame(self.root)
        top_frame.pack(fill='x', padx=10, pady=10)
        
        # Label y área de texto para aristas
        ttk.Label(top_frame, text="Ingrese aristas (formato: Nodo1 Nodo2 Peso):").pack(anchor='w')
        
        entrada_frame = ttk.Frame(top_frame)
        entrada_frame.pack(fill='x', pady=5)
        
        self.entrada_text = scrolledtext.ScrolledText(entrada_frame, height=4, width=60)
        self.entrada_text.pack(side='left', fill='both', expand=True)
        self.entrada_text.insert('1.0', "A B 4\nA C 2\nB D 10\nC D 3\nC E 8\nD E 6")
        
        self.crear_grafo_button = ttk.Button(entrada_frame, text="Crear Grafo", command=self.cargar_grafo_desde_texto)
        self.crear_grafo_button.pack(side='right', padx=(10, 0))
        
        # Frame para controles de búsqueda
        control_frame = ttk.Frame(self.root)
        control_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(control_frame, text="Inicio:").pack(side='left')
        self.inicio_field = ttk.Entry(control_frame, width=10)
        self.inicio_field.pack(side='left', padx=5)
        
        ttk.Label(control_frame, text="Fin:").pack(side='left')
        self.fin_field = ttk.Entry(control_frame, width=10)
        self.fin_field.pack(side='left', padx=5)
        
        self.buscar_ruta_button = ttk.Button(control_frame, text="Buscar Ruta", command=self.buscar_ruta)
        self.buscar_ruta_button.pack(side='left', padx=10)
        
        # Área de resultado
        resultado_frame = ttk.Frame(self.root)
        resultado_frame.pack(fill='x', padx=10, pady=5)
        
        self.resultado_text = scrolledtext.ScrolledText(resultado_frame, height=3, width=60)
        self.resultado_text.pack(fill='x')
        
        # Canvas para dibujar el grafo
        self.canvas = tk.Canvas(self.root, bg='white', height=300)
        self.canvas.pack(fill='both', expand=True, padx=10, pady=10)
        
    def cargar_grafo_desde_texto(self):
        self.nodos.clear()
        self.aristas.clear()
        self.ruta_corta.clear()
        
        lineas = self.entrada_text.get('1.0', tk.END).strip().split('\n')
        
        for linea in lineas:
            parts = linea.strip().split()
            if len(parts) == 3:
                try:
                    n1, n2, peso = parts[0].upper(), parts[1].upper(), int(parts[2])
                    
                    # Crear nodos si no existen
                    if n1 not in self.nodos:
                        self.nodos[n1] = Nodo(n1, random.randint(100, 500), random.randint(100, 250))
                    if n2 not in self.nodos:
                        self.nodos[n2] = Nodo(n2, random.randint(100, 500), random.randint(100, 250))
                    
                    # Crear aristas bidireccionales
                    self.aristas.append(Arista(self.nodos[n1], self.nodos[n2], peso))
                    self.aristas.append(Arista(self.nodos[n2], self.nodos[n1], peso))
                    
                except ValueError:
                    continue
        
        self.dibujar_grafo()
    
    def dijkstra(self, inicio):
        distancias = {nodo: float('inf') for nodo in self.nodos.values()}
        padres = {}
        distancias[inicio] = 0
        padres[inicio] = None
        
        cola = [(0, inicio)]
        
        while cola:
            dist_actual, nodo_actual = heapq.heappop(cola)
            
            if dist_actual > distancias[nodo_actual]:
                continue
            
            for arista in self.aristas:
                if arista.desde == nodo_actual:
                    nueva_dist = dist_actual + arista.peso
                    if nueva_dist < distancias[arista.hasta]:
                        distancias[arista.hasta] = nueva_dist
                        padres[arista.hasta] = nodo_actual
                        heapq.heappush(cola, (nueva_dist, arista.hasta))
        
        return distancias, padres
    
    def reconstruir_ruta(self, destino, padres):
        ruta = []
        nodo_actual = destino
        
        while nodo_actual is not None:
            ruta.append(nodo_actual)
            nodo_actual = padres.get(nodo_actual)
        
        ruta.reverse()
        return ruta
    
    def buscar_ruta(self):
        inicio_texto = self.inicio_field.get().upper()
        fin_texto = self.fin_field.get().upper()
        
        if inicio_texto not in self.nodos or fin_texto not in self.nodos:
            messagebox.showerror("Error", "Nodos inválidos")
            return
        
        nodo_inicio = self.nodos[inicio_texto]
        nodo_fin = self.nodos[fin_texto]
        
        distancias, padres = self.dijkstra(nodo_inicio)
        
        if distancias[nodo_fin] == float('inf'):
            self.resultado_text.delete('1.0', tk.END)
            self.resultado_text.insert('1.0', "No hay camino")
            self.ruta_corta = []
        else:
            distancia_total = distancias[nodo_fin]
            self.ruta_corta = self.reconstruir_ruta(nodo_fin, padres)
            
            resultado = "Ruta más corta: "
            for nodo in self.ruta_corta:
                resultado += nodo.nombre + " "
            resultado += f"\nDistancia: {distancia_total}"
            
            self.resultado_text.delete('1.0', tk.END)
            self.resultado_text.insert('1.0', resultado)
        
        self.dibujar_grafo()
    
    def dibujar_grafo(self):
        self.canvas.delete("all")
        
        # Dibujar aristas
        aristas_dibujadas = set()
        for arista in self.aristas:
            # Evitar dibujar la misma arista dos veces
            arista_key = tuple(sorted([arista.desde.nombre, arista.hasta.nombre]))
            if arista_key not in aristas_dibujadas:
                aristas_dibujadas.add(arista_key)
                
                self.canvas.create_line(arista.desde.x, arista.desde.y, 
                                      arista.hasta.x, arista.hasta.y,
                                      fill='gray', width=1)
                
                # Dibujar peso en el punto medio
                xm = (arista.desde.x + arista.hasta.x) // 2
                ym = (arista.desde.y + arista.hasta.y) // 2
                self.canvas.create_text(xm, ym, text=str(arista.peso), fill='black')
        
        # Dibujar ruta más corta
        if len(self.ruta_corta) > 1:
            for i in range(len(self.ruta_corta) - 1):
                n1 = self.ruta_corta[i]
                n2 = self.ruta_corta[i + 1]
                self.canvas.create_line(n1.x, n1.y, n2.x, n2.y,
                                      fill='red', width=3)
        
        # Dibujar nodos
        for nodo in self.nodos.values():
            # Círculo del nodo
            self.canvas.create_oval(nodo.x - 15, nodo.y - 15, 
                                  nodo.x + 15, nodo.y + 15,
                                  fill='#66ccff', outline='black', width=2)
            
            # Nombre del nodo
            self.canvas.create_text(nodo.x, nodo.y, text=nodo.nombre, 
                                  fill='black', font=('Arial', 10, 'bold'))

def main():
    root = tk.Tk()
    app = GrafoDinamico(root)
    root.mainloop()

if __name__ == "__main__":
    main()