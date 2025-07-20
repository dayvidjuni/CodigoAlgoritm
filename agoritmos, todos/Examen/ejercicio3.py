import tkinter as tk
from tkinter import colorchooser
from collections import deque

# Main configuration for window
root = tk.Tk()
root.title("Mini Paint with Undo/Redo")
root.geometry("800x600")

# Stack with a limit of 10 for undo history and secondary stack for redo
MAX_ACTIONS = 10
history = deque(maxlen=MAX_ACTIONS)
redo_history = []

# Canvas
canvas = tk.Canvas(root, bg="white", width=800, height=550)
canvas.pack()

# Global variables
current_color = "black"
thickness = 3
current_line = []

def print_stacks():
    print("\n--- STACK STATES ---")
    print("Undo History:")
    for action in list(history):
        print(f"  {action['action']} - ID: {action.get('id', '')}")
    print("Redo History:")
    for action in redo_history:
        print(f"  {action['action']} - ID: {action.get('id', '')}")
    print("---------------------\n")

# Functions
def choose_color():
    global current_color
    current_color = colorchooser.askcolor()[1]

def start_drawing(event):
    global current_line
    current_line = [(event.x, event.y)]

def draw(event):
    global current_line
    if current_line:
        x1, y1 = current_line[-1]
        x2, y2 = event.x, event.y
        line_id = canvas.create_line(x1, y1, x2, y2, fill=current_color, width=thickness, capstyle=tk.ROUND, smooth=True)
        action = {'action': 'draw', 'id': line_id, 'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2, 'color': current_color, 'thickness': thickness}
        history.append(action)
        current_line.append((x2, y2))
        redo_history.clear()
        print_stacks()

def undo():
    if history:
        action = history.pop()
        if action['action'] == 'draw' or action['action'] == 'move':
            canvas.delete(action['id'])
        redo_history.append(action)
        print_stacks()

def redo():
    if redo_history:
        action = redo_history.pop()
        if action['action'] == 'draw' or action['action'] == 'move':
            line_id = canvas.create_line(
                action['x1'], action['y1'], action['x2'], action['y2'],
                fill=action['color'], width=action['thickness'], capstyle=tk.ROUND, smooth=True
            )
            action['id'] = line_id
        history.append(action)
        print_stacks()

def clear_all():
    items = canvas.find_all()
    for item_id in items:
        canvas.delete(item_id)
        history.append({'action': 'delete', 'id': item_id})
        if len(history) > MAX_ACTIONS:
            history.popleft()
    redo_history.clear()
    print_stacks()

def move_line():
    # Simulated move: create a new line shifted down
    if history:
        last = history[-1]
        if last['action'] == 'draw':
            x1 = last['x1']
            y1 = last['y1'] + 20
            x2 = last['x2']
            y2 = last['y2'] + 20
            line_id = canvas.create_line(x1, y1, x2, y2, fill=last['color'], width=last['thickness'], capstyle=tk.ROUND, smooth=True)
            new_action = {'action': 'move', 'id': line_id, 'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2, 'color': last['color'], 'thickness': last['thickness']}
            history.append(new_action)
            if len(history) > MAX_ACTIONS:
                history.popleft()
            redo_history.clear()
            print_stacks()

# Buttons
button_frame = tk.Frame(root)
button_frame.pack()

btn_color = tk.Button(button_frame, text="Color", command=choose_color)
btn_color.pack(side=tk.LEFT, padx=5)

btn_undo = tk.Button(button_frame, text="Undo", command=undo)
btn_undo.pack(side=tk.LEFT, padx=5)

btn_redo = tk.Button(button_frame, text="Redo", command=redo)
btn_redo.pack(side=tk.LEFT, padx=5)

btn_move = tk.Button(button_frame, text="Move", command=move_line)
btn_move.pack(side=tk.LEFT, padx=5)

btn_clear = tk.Button(button_frame, text="Clear All", command=clear_all)
btn_clear.pack(side=tk.LEFT, padx=5)

# Events
canvas.bind("<Button-1>", start_drawing)
canvas.bind("<B1-Motion>", draw)

# Run
root.mainloop()
