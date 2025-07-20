import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import random
import time
import threading
import winsound  # Para los sonidos (Windows)
from datetime import datetime

class SortingVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Visualizador Avanzado de Algoritmos de Ordenamiento")
        self.root.geometry("1100x750")
        self.root.configure(bg='#2c3e50')
        
        # Variables
        self.array = []
        self.array_size = 50
        self.speed = 50
        self.is_sorting = False
        self.current_algorithm = "Bubble Sort"
        self.comparisons = 0
        self.swaps = 0
        self.start_time = 0
        self.sound_enabled = True
        
        # Colores
        self.colors = {
            'default': '#3498db',
            'comparing': '#e74c3c',
            'swapping': '#f39c12',
            'sorted': '#27ae60',
            'pivot': '#9b59b6',
            'heap_node': '#8e44ad',
            'shell_gap': '#16a085'
        }
        
        self.setup_ui()
        self.generate_array()
        
    def setup_ui(self):
        # Frame principal
        main_frame = tk.Frame(self.root, bg='#2c3e50')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Frame de controles
        control_frame = tk.Frame(main_frame, bg='#34495e', relief=tk.RAISED, bd=2)
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Primera fila de controles
        row1 = tk.Frame(control_frame, bg='#34495e')
        row1.pack(fill=tk.X, padx=10, pady=5)
        
        # Algoritmo
        tk.Label(row1, text="Algoritmo:", bg='#34495e', fg='white', font=('Arial', 10, 'bold')).pack(side=tk.LEFT)
        self.algorithm_var = tk.StringVar(value=self.current_algorithm)
        algorithm_combo = ttk.Combobox(row1, textvariable=self.algorithm_var, 
                                     values=["Bubble Sort", "Insertion Sort", "Selection Sort", 
                                           "Quick Sort", "Merge Sort", "Heap Sort", "Shell Sort"], 
                                     state="readonly", width=15)
        algorithm_combo.pack(side=tk.LEFT, padx=(5, 20))
        algorithm_combo.bind('<<ComboboxSelected>>', self.on_algorithm_change)
        
        # Tamaño del array
        tk.Label(row1, text="Tamaño:", bg='#34495e', fg='white', font=('Arial', 10, 'bold')).pack(side=tk.LEFT)
        self.size_var = tk.IntVar(value=self.array_size)
        size_scale = tk.Scale(row1, from_=5, to=150, orient=tk.HORIZONTAL, variable=self.size_var,
                            bg='#34495e', fg='white', highlightthickness=0, length=150,
                            command=self.on_size_change)
        size_scale.pack(side=tk.LEFT, padx=(5, 20))
        
        # Velocidad
        tk.Label(row1, text="Velocidad:", bg='#34495e', fg='white', font=('Arial', 10, 'bold')).pack(side=tk.LEFT)
        self.speed_var = tk.IntVar(value=self.speed)
        speed_scale = tk.Scale(row1, from_=1, to=100, orient=tk.HORIZONTAL, variable=self.speed_var,
                             bg='#34495e', fg='white', highlightthickness=0, length=150,
                             command=self.on_speed_change)
        speed_scale.pack(side=tk.LEFT, padx=(5, 20))
        
        # Checkbox para sonido
        self.sound_var = tk.BooleanVar(value=True)
        sound_check = tk.Checkbutton(row1, text="Sonido", variable=self.sound_var, 
                                   bg='#34495e', fg='white', selectcolor='#2c3e50',
                                   command=self.toggle_sound)
        sound_check.pack(side=tk.LEFT, padx=(20, 0))
        
        # Segunda fila de controles
        row2 = tk.Frame(control_frame, bg='#34495e')
        row2.pack(fill=tk.X, padx=10, pady=5)
        
        # Botones
        self.start_button = tk.Button(row2, text="▶ Iniciar", command=self.start_sorting,
                                    bg='#27ae60', fg='white', font=('Arial', 10, 'bold'),
                                    relief=tk.FLAT, padx=20)
        self.start_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.stop_button = tk.Button(row2, text="⏸ Pausar", command=self.stop_sorting,
                                   bg='#e74c3c', fg='white', font=('Arial', 10, 'bold'),
                                   relief=tk.FLAT, padx=20, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.reset_button = tk.Button(row2, text="🔄 Reset", command=self.reset_array,
                                    bg='#95a5a6', fg='white', font=('Arial', 10, 'bold'),
                                    relief=tk.FLAT, padx=20)
        self.reset_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.generate_button = tk.Button(row2, text="🎲 Aleatorio", command=self.generate_array,
                                       bg='#3498db', fg='white', font=('Arial', 10, 'bold'),
                                       relief=tk.FLAT, padx=20)
        self.generate_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.manual_button = tk.Button(row2, text="✏️ Manual", command=self.manual_input,
                                     bg='#f39c12', fg='white', font=('Arial', 10, 'bold'),
                                     relief=tk.FLAT, padx=20)
        self.manual_button.pack(side=tk.LEFT, padx=(0, 20))
        
        # Estadísticas
        stats_frame = tk.Frame(row2, bg='#34495e')
        stats_frame.pack(side=tk.RIGHT)
        
        self.time_label = tk.Label(stats_frame, text="Tiempo: 0.00s", 
                                 bg='#34495e', fg='#ecf0f1', font=('Arial', 10))
        self.time_label.pack(anchor='e')
        
        self.stats_label = tk.Label(stats_frame, text="Comparaciones: 0 | Intercambios: 0",
                                  bg='#34495e', fg='#ecf0f1', font=('Arial', 10))
        self.stats_label.pack(anchor='e')
        
        # Tercera fila - Leyenda de colores
        legend_frame = tk.Frame(control_frame, bg='#34495e')
        legend_frame.pack(fill=tk.X, padx=10, pady=5)
        
        legend_items = [
            ("Comparando", self.colors['comparing']),
            ("Intercambiando", self.colors['swapping']),
            ("Ordenado", self.colors['sorted']),
            ("Pivote", self.colors['pivot']),
            ("Nodo Heap", self.colors['heap_node']),
            ("Brecha Shell", self.colors['shell_gap'])
        ]
        
        for i, (text, color) in enumerate(legend_items):
            item_frame = tk.Frame(legend_frame, bg='#34495e')
            item_frame.pack(side=tk.LEFT, padx=(0 if i == 0 else 15, 0))
            
            color_box = tk.Label(item_frame, text="  ", bg=color, relief=tk.RAISED, bd=1)
            color_box.pack(side=tk.LEFT)
            
            tk.Label(item_frame, text=text, bg='#34495e', fg='white', font=('Arial', 9)).pack(side=tk.LEFT, padx=(5, 0))
        
        # Canvas para la visualización
        self.canvas = tk.Canvas(main_frame, bg='#ecf0f1', relief=tk.SUNKEN, bd=2)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
    def toggle_sound(self):
        self.sound_enabled = self.sound_var.get()
        
    def play_sound(self, freq=500, duration=50):
        if self.sound_enabled:
            winsound.Beep(freq, duration)
        
    def generate_array(self):
        if self.is_sorting:
            return
        self.array = [random.randint(10, 400) for _ in range(self.array_size)]
        self.comparisons = 0
        self.swaps = 0
        self.update_stats()
        self.draw_array()
        
    def manual_input(self):
        if self.is_sorting:
            return
            
        input_str = simpledialog.askstring("Entrada Manual", 
                                         "Ingrese números separados por comas:",
                                         parent=self.root)
        if input_str:
            try:
                numbers = [int(num.strip()) for num in input_str.split(',')]
                if 5 <= len(numbers) <= 150:
                    self.array = numbers
                    self.array_size = len(numbers)
                    self.size_var.set(self.array_size)
                    self.comparisons = 0
                    self.swaps = 0
                    self.update_stats()
                    self.draw_array()
                else:
                    messagebox.showerror("Error", "El tamaño del array debe estar entre 5 y 150")
            except ValueError:
                messagebox.showerror("Error", "Ingrese solo números separados por comas")
        
    def draw_array(self, comparing=[], swapping=[], sorted_indices=[], pivot_index=-1, 
                  heap_nodes=[], shell_gaps=[]):
        self.canvas.delete("all")
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        if canvas_width <= 1 or canvas_height <= 1:
            self.root.after(100, lambda: self.draw_array(comparing, swapping, sorted_indices, pivot_index, heap_nodes, shell_gaps))
            return
            
        bar_width = canvas_width / len(self.array)
        max_value = max(self.array) if self.array else 1
        
        for i, value in enumerate(self.array):
            x1 = i * bar_width
            y1 = canvas_height - (value / max_value) * (canvas_height - 20)
            x2 = (i + 1) * bar_width - 2
            y2 = canvas_height
            
            # Determinar color
            color = self.colors['default']
            if i == pivot_index:
                color = self.colors['pivot']
            elif i in swapping:
                color = self.colors['swapping']
            elif i in comparing:
                color = self.colors['comparing']
            elif i in sorted_indices:
                color = self.colors['sorted']
            elif i in heap_nodes:
                color = self.colors['heap_node']
            elif i in shell_gaps:
                color = self.colors['shell_gap']
            
            self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline='#2c3e50', width=1)
            
            # Mostrar valor si hay espacio
            if bar_width > 25 and len(self.array) <= 50:
                text_x = x1 + bar_width / 2
                text_y = y1 - 10
                self.canvas.create_text(text_x, text_y, text=str(value), font=('Arial', 8), fill='#2c3e50')
    
    def update_stats(self):
        elapsed_time = time.time() - self.start_time if self.is_sorting else 0
        self.time_label.config(text=f"Tiempo: {elapsed_time:.2f}s")
        self.stats_label.config(text=f"Comparaciones: {self.comparisons} | Intercambios: {self.swaps}")
    
    def on_algorithm_change(self, event):
        self.current_algorithm = self.algorithm_var.get()
    
    def on_size_change(self, value):
        if not self.is_sorting:
            self.array_size = int(value)
            self.generate_array()
    
    def on_speed_change(self, value):
        self.speed = int(value)
    
    def start_sorting(self):
        if self.is_sorting:
            return
        
        self.is_sorting = True
        self.start_time = time.time()
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.generate_button.config(state=tk.DISABLED)
        self.manual_button.config(state=tk.DISABLED)
        
        # Actualizar tiempo en tiempo real
        self.update_time()
        
        # Ejecutar algoritmo en hilo separado
        thread = threading.Thread(target=self.run_algorithm)
        thread.daemon = True
        thread.start()
    
    def update_time(self):
        if self.is_sorting:
            elapsed_time = time.time() - self.start_time
            self.time_label.config(text=f"Tiempo: {elapsed_time:.2f}s")
            self.root.after(100, self.update_time)
    
    def stop_sorting(self):
        self.is_sorting = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.generate_button.config(state=tk.NORMAL)
        self.manual_button.config(state=tk.NORMAL)
    
    def reset_array(self):
        self.stop_sorting()
        self.comparisons = 0
        self.swaps = 0
        self.update_stats()
        self.draw_array()
    
    def run_algorithm(self):
        try:
            if self.current_algorithm == "Bubble Sort":
                self.bubble_sort()
            elif self.current_algorithm == "Insertion Sort":
                self.insertion_sort()
            elif self.current_algorithm == "Selection Sort":
                self.selection_sort()
            elif self.current_algorithm == "Quick Sort":
                self.quick_sort(0, len(self.array) - 1)
            elif self.current_algorithm == "Merge Sort":
                self.merge_sort(0, len(self.array) - 1)
            elif self.current_algorithm == "Heap Sort":
                self.heap_sort()
            elif self.current_algorithm == "Shell Sort":
                self.shell_sort()
        except Exception as e:
            print(f"Error en algoritmo: {e}")
        finally:
            self.root.after(0, self.sorting_finished)
    
    def sorting_finished(self):
        self.is_sorting = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.generate_button.config(state=tk.NORMAL)
        self.manual_button.config(state=tk.NORMAL)
        
        # Mostrar array completamente ordenado
        sorted_indices = list(range(len(self.array)))
        self.root.after(0, lambda: self.draw_array(sorted_indices=sorted_indices))
        self.play_sound(1000, 200)  # Sonido de finalización
    
    def delay(self):
        time.sleep((101 - self.speed) / 1000)
    
    # Algoritmos de ordenamiento existentes (bubble, insertion, selection, quick, merge)
    # ... (los mismos que en tu versión original)
    
    # Nuevos algoritmos añadidos:
    
    def heap_sort(self):
        n = len(self.array)
        sorted_indices = []
        
        # Construir max heap
        for i in range(n // 2 - 1, -1, -1):
            if not self.is_sorting:
                return
            self.heapify(n, i, sorted_indices)
        
        # Extraer elementos uno por uno
        for i in range(n - 1, 0, -1):
            if not self.is_sorting:
                return
                
            # Mover la raíz actual al final
            self.swaps += 1
            self.array[0], self.array[i] = self.array[i], self.array[0]
            self.root.after(0, self.update_stats)
            self.root.after(0, lambda: self.draw_array(
                swapping=[0, i], 
                heap_nodes=list(range(i)),
                sorted_indices=sorted_indices
            ))
            self.play_sound(800, 50)
            self.delay()
            
            sorted_indices.append(i)
            
            # Llamar heapify en el heap reducido
            self.heapify(i, 0, sorted_indices)
        
        if self.is_sorting:
            sorted_indices.append(0)
            self.root.after(0, lambda: self.draw_array(sorted_indices=sorted_indices))
    
    def heapify(self, n, i, sorted_indices):
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2
        
        # Comparar con el hijo izquierdo
        if left < n:
            self.comparisons += 1
            self.root.after(0, self.update_stats)
            self.root.after(0, lambda: self.draw_array(
                comparing=[largest, left],
                heap_nodes=list(range(n)),
                sorted_indices=sorted_indices
            ))
            self.play_sound(600, 20)
            self.delay()
            
            if self.array[left] > self.array[largest]:
                largest = left
        
        # Comparar con el hijo derecho
        if right < n:
            self.comparisons += 1
            self.root.after(0, self.update_stats)
            self.root.after(0, lambda: self.draw_array(
                comparing=[largest, right],
                heap_nodes=list(range(n)),
                sorted_indices=sorted_indices
            ))
            self.play_sound(600, 20)
            self.delay()
            
            if self.array[right] > self.array[largest]:
                largest = right
        
        # Si el más grande no es la raíz
        if largest != i:
            self.swaps += 1
            self.array[i], self.array[largest] = self.array[largest], self.array[i]
            self.root.after(0, self.update_stats)
            self.root.after(0, lambda: self.draw_array(
                swapping=[i, largest],
                heap_nodes=list(range(n)),
                sorted_indices=sorted_indices
            ))
            self.play_sound(400, 50)
            self.delay()
            
            # Heapify el subárbol afectado
            self.heapify(n, largest, sorted_indices)
    
    def shell_sort(self):
        n = len(self.array)
        gap = n // 2
        sorted_indices = []
        
        while gap > 0:
            if not self.is_sorting:
                return
                
            # Hacer un insertion sort para esta brecha
            for i in range(gap, n):
                if not self.is_sorting:
                    return
                    
                temp = self.array[i]
                j = i
                
                # Resaltar los elementos en la brecha actual
                gap_indices = list(range(i % gap, n, gap))
                self.root.after(0, lambda: self.draw_array(
                    comparing=[i],
                    shell_gaps=gap_indices,
                    sorted_indices=sorted_indices
                ))
                self.play_sound(700, 20)
                self.delay()
                
                while j >= gap and self.array[j - gap] > temp:
                    if not self.is_sorting:
                        return
                        
                    self.comparisons += 1
                    self.root.after(0, self.update_stats)
                    self.root.after(0, lambda: self.draw_array(
                        comparing=[j, j - gap],
                        shell_gaps=gap_indices,
                        sorted_indices=sorted_indices
                    ))
                    self.play_sound(600, 20)
                    self.delay()
                    
                    self.swaps += 1
                    self.array[j] = self.array[j - gap]
                    self.root.after(0, self.update_stats)
                    self.root.after(0, lambda: self.draw_array(
                        swapping=[j, j - gap],
                        shell_gaps=gap_indices,
                        sorted_indices=sorted_indices
                    ))
                    self.play_sound(500, 30)
                    self.delay()
                    
                    j -= gap
                
                self.array[j] = temp
                if j != i:
                    self.swaps += 1
                    self.root.after(0, self.update_stats)
                    self.root.after(0, lambda: self.draw_array(
                        swapping=[j, i],
                        shell_gaps=gap_indices,
                        sorted_indices=sorted_indices
                    ))
                    self.play_sound(500, 30)
                    self.delay()
            
            gap //= 2
        
        if self.is_sorting:
            sorted_indices = list(range(n))
            self.root.after(0, lambda: self.draw_array(sorted_indices=sorted_indices))

if __name__ == "__main__":
    root = tk.Tk()
    app = SortingVisualizer(root)
    root.mainloop()