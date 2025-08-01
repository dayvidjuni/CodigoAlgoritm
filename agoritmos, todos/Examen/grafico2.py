import tkinter as tk
from tkinter import messagebox, simpledialog
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class AdjNode:
    def __init__(self, index, weight):
        self.index = index
        self.weight = weight
        self.next = None

class Node:
    def __init__(self, name):
        self.name = name
        self.adjList = None

class Graph:
    def __init__(self):
        self.nodes = []
        self.positions = {}

    def get_index(self, name):
        for i, node in enumerate(self.nodes):
            if node.name == name:
                return i
        return -1

    def add_node(self, name):
        if self.get_index(name) != -1:
            messagebox.showinfo("Error", "Node already exists.")
            return
        self.nodes.append(Node(name))

    def add_connection(self, origin, destination, weight):
        i = self.get_index(origin)
        j = self.get_index(destination)
        if i == -1 or j == -1:
            messagebox.showinfo("Error", "One or both points do not exist.")
            return

        adj1 = AdjNode(j, weight)
        adj1.next = self.nodes[i].adjList
        self.nodes[i].adjList = adj1

        adj2 = AdjNode(i, weight)
        adj2.next = self.nodes[j].adjList
        self.nodes[j].adjList = adj2

    def check_path_exists_visual(self, start, end, draw_callback, root, delay=1000):
        i = self.get_index(start)
        j = self.get_index(end)
        if i == -1 or j == -1:
            messagebox.showinfo("Error", "Point not found.")
            return

        visited = [False] * len(self.nodes)
        path_edges = []
        stack = [(i, [])]

        def step():
            if not stack:
                messagebox.showinfo("Path Not Found", f"No path between {start} and {end}.")
                return

            current, path = stack.pop()
            if visited[current]:
                root.after(delay, step)
                return

            visited[current] = True
            draw_callback(current, path)
            if current == j:
                messagebox.showinfo("Path Exists", f"There is a path between {start} and {end}.")
                return

            adj = self.nodes[current].adjList
            neighbors = []
            while adj:
                if not visited[adj.index]:
                    neighbors.append((adj.index, path + [(current, adj.index)]))
                adj = adj.next

            stack.extend(reversed(neighbors))
            root.after(delay, step)

        step()

    def get_edges(self):
        edges = set()
        for i, node in enumerate(self.nodes):
            adj = node.adjList
            while adj:
                if (adj.index, i) not in edges:
                    edges.add((i, adj.index, adj.weight))
                adj = adj.next
        return edges

    def get_adjacency_dict(self):
        adj_dict = {}
        for i, node in enumerate(self.nodes):
            connections = []
            adj = node.adjList
            while adj:
                connections.append((self.nodes[adj.index].name, adj.weight))
                adj = adj.next
            adj_dict[node.name] = connections
        return adj_dict

def draw_graph(graph_obj, canvas_frame, highlight_node=None, path_edges=None):
    G = nx.Graph()
    node_names = [node.name for node in graph_obj.nodes]
    G.add_nodes_from(node_names)
    for i, j, w in graph_obj.get_edges():
        G.add_edge(graph_obj.nodes[i].name, graph_obj.nodes[j].name, weight=w)

    fig, ax = plt.subplots(figsize=(6, 4))

    pos = nx.spring_layout(G, seed=42)

    edge_colors = []
    for u, v in G.edges():
        i = graph_obj.get_index(u)
        j = graph_obj.get_index(v)
        if path_edges and ((i, j) in path_edges or (j, i) in path_edges):
            edge_colors.append('red')
        else:
            edge_colors.append('black')

    node_colors = []
    for name in node_names:
        if highlight_node is not None and graph_obj.nodes[highlight_node].name == name:
            node_colors.append('orange')
        else:
            node_colors.append('lightblue')

    nx.draw(G, pos, with_labels=True, ax=ax, node_color=node_colors, edge_color=edge_colors, node_size=1000)
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax)

    for widget in canvas_frame.winfo_children():
        widget.destroy()

    canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()
    canvas.get_tk_widget().update()

def draw_adjacency_lists(graph_obj, text_widget):
    adj_dict = graph_obj.get_adjacency_dict()
    text_widget.delete('1.0', tk.END)
    for node, connections in adj_dict.items():
        line = f"{node}: " + ", ".join([f"{dest}({weight})" for dest, weight in connections]) + "\n"
        text_widget.insert(tk.END, line)

def main():
    g = Graph()

    root = tk.Tk()
    root.title("Graph Visualizer")

    control_frame = tk.Frame(root)
    control_frame.pack(side=tk.TOP, fill=tk.X)

    canvas_frame = tk.Frame(root)
    canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    adjacency_frame = tk.Frame(root)
    adjacency_frame.pack(side=tk.RIGHT, fill=tk.Y)

    text = tk.Text(adjacency_frame, width=30)
    text.pack(fill=tk.BOTH, expand=True)

    def refresh():
        draw_graph(g, canvas_frame)
        draw_adjacency_lists(g, text)

    def add_node():
        name = simpledialog.askstring("Add Node", "Enter node name:")
        if name:
            g.add_node(name)
            refresh()

    def add_connection():
        a = simpledialog.askstring("Add Connection", "Enter origin:")
        b = simpledialog.askstring("Add Connection", "Enter destination:")
        w = simpledialog.askinteger("Add Connection", "Enter weight:")
        if a and b and w is not None:
            g.add_connection(a, b, w)
            refresh()

    def check_path_visual():
        a = simpledialog.askstring("Check Path", "Enter origin:")
        b = simpledialog.askstring("Check Path", "Enter destination:")
        if a and b:
            def draw_callback(current, path_edges):
                draw_graph(g, canvas_frame, highlight_node=current, path_edges=path_edges)
                root.update()
            g.check_path_exists_visual(a, b, draw_callback, root, delay=1000)

    tk.Button(control_frame, text="Add Node", command=add_node).pack(side=tk.LEFT)
    tk.Button(control_frame, text="Add Connection", command=add_connection).pack(side=tk.LEFT)
    tk.Button(control_frame, text="Check Path Step-by-Step", command=check_path_visual).pack(side=tk.LEFT)

    refresh()
    root.mainloop()

if __name__ == "__main__":
    main()
