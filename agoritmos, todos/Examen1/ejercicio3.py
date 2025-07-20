import tkinter as tk
from tkinter import colorchooser
from collections import deque

# Configuración principal
root = tk.Tk()
root.title("Mini Paint con Deshacer/Rehacer")
root.geometry("800x600")

# Pila con límite de 10 para historial y pila secundaria para rehacer
MAX_ACCIONES = 10
historial = deque(maxlen=MAX_ACCIONES)
redo_historial = []

# Lienzo
canvas = tk.Canvas(root, bg="white", width=800, height=550)
canvas.pack()

# Variables globales
color_actual = "black"
grosor = 3
linea_actual = []

def imprimir_pilas():
    print("\n--- ESTADO DE LAS PILAS ---")
    print("Historial (UNDO):")
    for acc in list(historial):
        print(f"  {acc['accion']} - ID: {acc.get('id', '')}")
    print("Rehacer (REDO):")
    for acc in redo_historial:
        print(f"  {acc['accion']} - ID: {acc.get('id', '')}")
    print("----------------------------\n")

# Funciones
def seleccionar_color():
    global color_actual
    color_actual = colorchooser.askcolor()[1]

def inicio_dibujo(event):
    global linea_actual
    linea_actual = [(event.x, event.y)]

def dibujar(event):
    global linea_actual
    if linea_actual:
        x1, y1 = linea_actual[-1]
        x2, y2 = event.x, event.y
        linea_id = canvas.create_line(x1, y1, x2, y2, fill=color_actual, width=grosor, capstyle=tk.ROUND, smooth=True)
        accion = {'accion': 'dibujar', 'id': linea_id, 'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2, 'color': color_actual, 'grosor': grosor}
        historial.append(accion)
        linea_actual.append((x2, y2))
        redo_historial.clear()
        imprimir_pilas()

def deshacer():
    if historial:
        accion = historial.pop()
        if accion['accion'] == 'dibujar' or accion['accion'] == 'mover':
            canvas.delete(accion['id'])
        redo_historial.append(accion)
        imprimir_pilas()

def rehacer():
    if redo_historial:
        accion = redo_historial.pop()
        if accion['accion'] == 'dibujar' or accion['accion'] == 'mover':
            linea_id = canvas.create_line(
                accion['x1'], accion['y1'], accion['x2'], accion['y2'],
                fill=accion['color'], width=accion['grosor'], capstyle=tk.ROUND, smooth=True
            )
            accion['id'] = linea_id
        historial.append(accion)
        imprimir_pilas()

def eliminar_todo():
    items = canvas.find_all()
    for item_id in items:
        canvas.delete(item_id)
        historial.append({'accion': 'eliminar', 'id': item_id})
        if len(historial) > MAX_ACCIONES:
            historial.popleft()
    redo_historial.clear()
    imprimir_pilas()

def mover_linea():
    # Simulación: crear una nueva línea movida hacia abajo
    if historial:
        ultima = historial[-1]
        if ultima['accion'] == 'dibujar':
            x1 = ultima['x1']
            y1 = ultima['y1'] + 20
            x2 = ultima['x2']
            y2 = ultima['y2'] + 20
            linea_id = canvas.create_line(x1, y1, x2, y2, fill=ultima['color'], width=ultima['grosor'], capstyle=tk.ROUND, smooth=True)
            nueva_accion = {'accion': 'mover', 'id': linea_id, 'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2, 'color': ultima['color'], 'grosor': ultima['grosor']}
            historial.append(nueva_accion)
            if len(historial) > MAX_ACCIONES:
                historial.popleft()
            redo_historial.clear()
            imprimir_pilas()

# Botones
frame_botones = tk.Frame(root)
frame_botones.pack()

btn_color = tk.Button(frame_botones, text="Color", command=seleccionar_color)
btn_color.pack(side=tk.LEFT, padx=5)

btn_deshacer = tk.Button(frame_botones, text="Deshacer", command=deshacer)
btn_deshacer.pack(side=tk.LEFT, padx=5)

btn_rehacer = tk.Button(frame_botones, text="Rehacer", command=rehacer)
btn_rehacer.pack(side=tk.LEFT, padx=5)

btn_mover = tk.Button(frame_botones, text="Mover", command=mover_linea)
btn_mover.pack(side=tk.LEFT, padx=5)

btn_eliminar = tk.Button(frame_botones, text="Eliminar Todo", command=eliminar_todo)
btn_eliminar.pack(side=tk.LEFT, padx=5)

# Eventos
canvas.bind("<Button-1>", inicio_dibujo)
canvas.bind("<B1-Motion>", dibujar)

# Ejecutar
root.mainloop()
