import tkinter as tk
from tkinter import ttk
import random
import time
import threading

class SortingVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Visualizador de Algoritmos de Ordenamiento")
        self.root.geometry("1000x700")
        self.root.configure(bg='#2c3e50')
        
        # Variables
        self.array = []
        self.array_size = 50
        self.speed = 50
        self.is_sorting = False
        self.current_algorithm = "Bubble Sort"
        self.comparisons = 0
        self.swaps = 0
        
        # Colores
        self.colors = {
            'default': '#3498db',
            'comparing': '#e74c3c',
            'swapping': '#f39c12',
            'sorted': '#27ae60',
            'pivot': '#9b59b6'
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
                                           "Quick Sort", "Merge Sort"], state="readonly", width=15)
        algorithm_combo.pack(side=tk.LEFT, padx=(5, 20))
        algorithm_combo.bind('<<ComboboxSelected>>', self.on_algorithm_change)
        
        # Tamaño del array
        tk.Label(row1, text="Tamaño:", bg='#34495e', fg='white', font=('Arial', 10, 'bold')).pack(side=tk.LEFT)
        self.size_var = tk.IntVar(value=self.array_size)
        size_scale = tk.Scale(row1, from_=10, to=100, orient=tk.HORIZONTAL, variable=self.size_var,
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
        
        self.generate_button = tk.Button(row2, text="🎲 Nuevo Array", command=self.generate_array,
                                       bg='#3498db', fg='white', font=('Arial', 10, 'bold'),
                                       relief=tk.FLAT, padx=20)
        self.generate_button.pack(side=tk.LEFT, padx=(0, 20))
        
        # Estadísticas
        stats_frame = tk.Frame(row2, bg='#34495e')
        stats_frame.pack(side=tk.RIGHT)
        
        self.stats_label = tk.Label(stats_frame, text="Comparaciones: 0 | Intercambios: 0",
                                  bg='#34495e', fg='#ecf0f1', font=('Arial', 10))
        self.stats_label.pack()
        
        # Leyenda de colores
        legend_frame = tk.Frame(control_frame, bg='#34495e')
        legend_frame.pack(fill=tk.X, padx=10, pady=5)
        
        legend_items = [
            ("Comparando", self.colors['comparing']),
            ("Intercambiando", self.colors['swapping']),
            ("Ordenado", self.colors['sorted']),
            ("Pivote", self.colors['pivot'])
        ]
        
        for i, (text, color) in enumerate(legend_items):
            item_frame = tk.Frame(legend_frame, bg='#34495e')
            item_frame.pack(side=tk.LEFT, padx=(0 if i == 0 else 20, 0))
            
            color_box = tk.Label(item_frame, text="  ", bg=color, relief=tk.RAISED, bd=1)
            color_box.pack(side=tk.LEFT)
            
            tk.Label(item_frame, text=text, bg='#34495e', fg='white', font=('Arial', 9)).pack(side=tk.LEFT, padx=(5, 0))
        
        # Canvas para la visualización
        self.canvas = tk.Canvas(main_frame, bg='#ecf0f1', relief=tk.SUNKEN, bd=2)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
    def generate_array(self):
        if self.is_sorting:
            return
        self.array = [random.randint(10, 400) for _ in range(self.array_size)]
        self.comparisons = 0
        self.swaps = 0
        self.update_stats()
        self.draw_array()
        
    def draw_array(self, comparing=[], swapping=[], sorted_indices=[], pivot_index=-1):
        self.canvas.delete("all")
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        if canvas_width <= 1 or canvas_height <= 1:
            self.root.after(100, lambda: self.draw_array(comparing, swapping, sorted_indices, pivot_index))
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
            
            self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline='#2c3e50', width=1)
            
            # Mostrar valor si hay espacio
            if bar_width > 20 and len(self.array) <= 30:
                text_x = x1 + bar_width / 2
                text_y = y1 - 10
                self.canvas.create_text(text_x, text_y, text=str(value), font=('Arial', 8), fill='#2c3e50')
    
    def update_stats(self):
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
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.generate_button.config(state=tk.DISABLED)
        
        # Ejecutar algoritmo en hilo separado
        thread = threading.Thread(target=self.run_algorithm)
        thread.daemon = True
        thread.start()
    
    def stop_sorting(self):
        self.is_sorting = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.generate_button.config(state=tk.NORMAL)
    
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
        except Exception as e:
            print(f"Error en algoritmo: {e}")
        finally:
            self.root.after(0, self.sorting_finished)
    
    def sorting_finished(self):
        self.is_sorting = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.generate_button.config(state=tk.NORMAL)
        
        # Mostrar array completamente ordenado
        sorted_indices = list(range(len(self.array)))
        self.root.after(0, lambda: self.draw_array(sorted_indices=sorted_indices))
    
    def delay(self):
        time.sleep((101 - self.speed) / 1000)
    
    def bubble_sort(self):
        n = len(self.array)
        sorted_indices = []
        
        for i in range(n):
            if not self.is_sorting:
                break
                
            for j in range(0, n - i - 1):
                if not self.is_sorting:
                    break
                
                self.comparisons += 1
                self.root.after(0, self.update_stats)
                self.root.after(0, lambda: self.draw_array(comparing=[j, j + 1], sorted_indices=sorted_indices))
                self.delay()
                
                if self.array[j] > self.array[j + 1]:
                    self.swaps += 1
                    self.array[j], self.array[j + 1] = self.array[j + 1], self.array[j]
                    self.root.after(0, self.update_stats)
                    self.root.after(0, lambda: self.draw_array(swapping=[j, j + 1], sorted_indices=sorted_indices))
                    self.delay()
            
            sorted_indices.append(n - i - 1)
    
    def insertion_sort(self):
        sorted_indices = [0]
        
        for i in range(1, len(self.array)):
            if not self.is_sorting:
                break
                
            key = self.array[i]
            j = i - 1
            
            self.root.after(0, lambda: self.draw_array(comparing=[i], sorted_indices=sorted_indices))
            self.delay()
            
            while j >= 0 and self.array[j] > key:
                if not self.is_sorting:
                    break
                
                self.comparisons += 1
                self.root.after(0, self.update_stats)
                self.root.after(0, lambda: self.draw_array(comparing=[j, j + 1], sorted_indices=sorted_indices))
                self.delay()
                
                self.swaps += 1
                self.array[j + 1] = self.array[j]
                self.root.after(0, self.update_stats)
                self.root.after(0, lambda: self.draw_array(swapping=[j, j + 1], sorted_indices=sorted_indices))
                self.delay()
                j -= 1
            
            self.array[j + 1] = key
            sorted_indices.append(i)
    
    def selection_sort(self):
        sorted_indices = []
        
        for i in range(len(self.array)):
            if not self.is_sorting:
                break
                
            min_idx = i
            
            for j in range(i + 1, len(self.array)):
                if not self.is_sorting:
                    break
                
                self.comparisons += 1
                self.root.after(0, self.update_stats)
                self.root.after(0, lambda: self.draw_array(comparing=[min_idx, j], sorted_indices=sorted_indices))
                self.delay()
                
                if self.array[j] < self.array[min_idx]:
                    min_idx = j
            
            if min_idx != i:
                self.swaps += 1
                self.array[i], self.array[min_idx] = self.array[min_idx], self.array[i]
                self.root.after(0, self.update_stats)
                self.root.after(0, lambda: self.draw_array(swapping=[i, min_idx], sorted_indices=sorted_indices))
                self.delay()
            
            sorted_indices.append(i)
    
    def quick_sort(self, low, high):
        if low < high and self.is_sorting:
            pi = self.partition(low, high)
            self.quick_sort(low, pi - 1)
            self.quick_sort(pi + 1, high)
    
    def partition(self, low, high):
        pivot = self.array[high]
        i = low - 1
        
        self.root.after(0, lambda: self.draw_array(pivot_index=high))
        self.delay()
        
        for j in range(low, high):
            if not self.is_sorting:
                break
                
            self.comparisons += 1
            self.root.after(0, self.update_stats)
            self.root.after(0, lambda: self.draw_array(comparing=[j, high], pivot_index=high))
            self.delay()
            
            if self.array[j] < pivot:
                i += 1
                if i != j:
                    self.swaps += 1
                    self.array[i], self.array[j] = self.array[j], self.array[i]
                    self.root.after(0, self.update_stats)
                    self.root.after(0, lambda: self.draw_array(swapping=[i, j], pivot_index=high))
                    self.delay()
        
        self.swaps += 1
        self.array[i + 1], self.array[high] = self.array[high], self.array[i + 1]
        self.root.after(0, self.update_stats)
        self.root.after(0, lambda: self.draw_array(swapping=[i + 1, high]))
        self.delay()
        
        return i + 1
    
    def merge_sort(self, left, right):
        if left < right and self.is_sorting:
            mid = (left + right) // 2
            self.merge_sort(left, mid)
            self.merge_sort(mid + 1, right)
            self.merge(left, mid, right)
    
    def merge(self, left, mid, right):
        left_arr = self.array[left:mid + 1]
        right_arr = self.array[mid + 1:right + 1]
        
        i = j = 0
        k = left
        
        while i < len(left_arr) and j < len(right_arr):
            if not self.is_sorting:
                break
                
            self.comparisons += 1
            self.root.after(0, self.update_stats)
            self.root.after(0, lambda: self.draw_array(comparing=[left + i, mid + 1 + j]))
            self.delay()
            
            if left_arr[i] <= right_arr[j]:
                self.array[k] = left_arr[i]
                i += 1
            else:
                self.array[k] = right_arr[j]
                j += 1
            
            self.swaps += 1
            self.root.after(0, self.update_stats)
            self.root.after(0, lambda: self.draw_array(swapping=[k]))
            self.delay()
            k += 1
        
        while i < len(left_arr):
            if not self.is_sorting:
                break
            self.array[k] = left_arr[i]
            self.root.after(0, lambda: self.draw_array(swapping=[k]))
            self.delay()
            i += 1
            k += 1
        
        while j < len(right_arr):
            if not self.is_sorting:
                break
            self.array[k] = right_arr[j]
            self.root.after(0, lambda: self.draw_array(swapping=[k]))
            self.delay()
            j += 1
            k += 1

if __name__ == "__main__":
    root = tk.Tk()
    app = SortingVisualizer(root)
    root.mainloop()