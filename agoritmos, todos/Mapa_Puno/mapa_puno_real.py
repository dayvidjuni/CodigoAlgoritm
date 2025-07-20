import requests
import networkx as nx
import folium
import tkinter as tk
from tkinter import messagebox, ttk
from geopy.geocoders import Nominatim
import webbrowser
import os
import math

# Configurar geolocalizador
geolocalizador = Nominatim(user_agent="puno_ruta_app")

# Lugares predefinidos en Puno
LUGARES_PUNO = [
    "Escuela Profesional de Ingeniería de Sistemas",
    "Biblioteca Central Universidad Nacional del Altiplano",
    "Mercado Bellavista",
    "Estadio Enrique Torres Belón",
    "Puerto Puno",
    "Clínica Las Kalas",
    "Catedral de Puno",
    "Casa del Corregidor",
    "Parque Pino",
    "Museo Naval de Puno",
    "Mirador Kuntur Wasi",
    "Cerro Huajsapata",
    "Terminal Terrestre Puno",
    "Hospital Regional Manuel Núñez Butrón"
]

# Función para obtener datos OSM de Puno
def obtener_calles_puno():
    try:
        consulta = """
        [out:json];
        area[name="Puno"]->.a;
        (
          way(area.a)[highway];
        );
        out body;
        >;
        out skel qt;
        """
        url = "http://overpass-api.de/api/interpreter"
        r = requests.post(url, data={'data': consulta}, timeout=30)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error de conexión", f"No se pudo conectar al servidor OSM: {e}")
        return None

# Función para construir el grafo de calles
def crear_grafo_osm(datos_osm):
    if datos_osm is None or 'elements' not in datos_osm:
        return None, None
        
    G = nx.Graph()
    nodos = {}

    for elem in datos_osm['elements']:
        if elem['type'] == 'node':
            nodos[elem['id']] = (elem['lat'], elem['lon'])

    for elem in datos_osm['elements']:
        if elem['type'] == 'way' and 'nodes' in elem:
            nodes_way = elem['nodes']
            for i in range(len(nodes_way) - 1):
                n1 = nodes_way[i]
                n2 = nodes_way[i + 1]
                if n1 in nodos and n2 in nodos:
                    lat1, lon1 = nodos[n1]
                    lat2, lon2 = nodos[n2]
                    dist = haversine_distance(lat1, lon1, lat2, lon2)
                    G.add_edge(n1, n2, weight=dist, highway=elem.get('tags', {}).get('highway', 'unknown'))

    return G, nodos

# Función para calcular distancia haversine
def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371  # Radio de la Tierra en km
    dLat = math.radians(lat2 - lat1)
    dLon = math.radians(lon2 - lon1)
    a = (math.sin(dLat/2) * math.sin(dLat/2) +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dLon/2) * math.sin(dLon/2))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c

# Función para obtener el nodo más cercano
def obtener_nodo_desde_direccion(direccion, nodos_dict):
    if not direccion or not nodos_dict:
        return None
        
    try:
        ubicacion = geolocalizador.geocode(direccion + ", Puno, Perú", timeout=10)
        if not ubicacion:
            return None
        lat, lon = ubicacion.latitude, ubicacion.longitude
        nodo_cercano = min(nodos_dict, 
                          key=lambda n: haversine_distance(nodos_dict[n][0], nodos_dict[n][1], lat, lon))
        return nodo_cercano
    except Exception as e:
        print(f"Error geocodificando {direccion}: {e}")
        return None

# Función para mostrar el mapa en el navegador
def mostrar_mapa_en_navegador(archivo_html):
    try:
        ruta_absoluta = 'file://' + os.path.abspath(archivo_html)
        webbrowser.open(ruta_absoluta, new=2)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo abrir el navegador: {e}")

# Función para calcular la distancia total
def calcular_distancia_total(grafo, ruta):
    distancia = 0.0
    for i in range(len(ruta)-1):
        distancia += grafo.edges[ruta[i], ruta[i+1]]['weight']
    return distancia

# Función para actualizar los campos de entrada
def seleccionar_lugar(event, campo_entrada):
    widget = event.widget
    seleccion = widget.get()
    campo_entrada.delete(0, tk.END)
    campo_entrada.insert(0, seleccion)

# Función principal al hacer clic en el botón
def calcular_ruta():
    origen = entrada_origen.get().strip()
    destino = entrada_destino.get().strip()

    if not origen or not destino:
        messagebox.showwarning("Campos vacíos", "Por favor ingresa tanto el origen como el destino.")
        return

    progress_bar.start(10)
    ventana.update_idletasks()

    try:
        nodo_o = obtener_nodo_desde_direccion(origen, nodos)
        nodo_d = obtener_nodo_desde_direccion(destino, nodos)

        if nodo_o is None or nodo_d is None:
            messagebox.showerror("Error", "No se encontraron uno o ambos lugares. Verifica los nombres.")
            return

        ruta = nx.shortest_path(grafo, nodo_o, nodo_d, weight='weight')
        puntos = [nodos[n] for n in ruta]
        distancia_total = calcular_distancia_total(grafo, ruta)

        # Calcular centro del mapa
        latitudes = [p[0] for p in puntos]
        longitudes = [p[1] for p in puntos]
        centro = (sum(latitudes) / len(latitudes), sum(longitudes) / len(longitudes))

        # Crear mapa interactivo
        mapa = folium.Map(
            location=centro, 
            zoom_start=16, 
            control_scale=True, 
            zoom_control=True,
            tiles='https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
            attr='OpenStreetMap'
        )

        # Añadir marcadores
        folium.Marker(
            nodos[nodo_o], 
            tooltip=f"Inicio: {origen}",
            popup=f"<b>Punto de inicio</b><br>{origen}",
            icon=folium.Icon(color='green', icon='play', prefix='fa')
        ).add_to(mapa)

        folium.Marker(
            nodos[nodo_d], 
            tooltip=f"Destino: {destino}",
            popup=f"<b>Punto de destino</b><br>{destino}<br>Distancia total: {distancia_total:.2f} km",
            icon=folium.Icon(color='red', icon='flag-checkered', prefix='fa')
        ).add_to(mapa)

        # Añadir línea de ruta
        folium.PolyLine(
            puntos, 
            color='#0066ff', 
            weight=6, 
            opacity=0.8,
            tooltip=f"Ruta más corta: {distancia_total:.2f} km"
        ).add_to(mapa)

        # Guardar el mapa
        archivo_html = "ruta_interactiva_puno.html"
        mapa.save(archivo_html)

        # Mostrar mensaje y abrir navegador
        messagebox.showinfo("Ruta generada", 
                          f"Ruta calculada exitosamente!\n\n"
                          f"Origen: {origen}\n"
                          f"Destino: {destino}\n"
                          f"Distancia: {distancia_total:.2f} km\n\n"
                          f"El mapa se abrirá en tu navegador.")
        mostrar_mapa_en_navegador(archivo_html)

    except nx.NetworkXNoPath:
        messagebox.showerror("Error", "No existe una ruta entre los puntos seleccionados.")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error inesperado: {e}")
    finally:
        progress_bar.stop()

# -------- Cargar datos OSM --------
print("Descargando las calles de Puno...")
datos_osm = obtener_calles_puno()
if datos_osm is None:
    exit()

grafo, nodos = crear_grafo_osm(datos_osm)
if grafo is None or nodos is None:
    messagebox.showerror("Error", "No se pudo crear el grafo de calles.")
    exit()

print(f"Grafo creado con {len(grafo.nodes)} nodos y {len(grafo.edges)} aristas.")

# -------- Interfaz gráfica mejorada --------
ventana = tk.Tk()
ventana.title("Ruta más corta en Puno")
ventana.geometry("500x400")
ventana.resizable(False, False)

# Estilo
style = ttk.Style()
style.configure('TLabel', font=('Arial', 10))
style.configure('TButton', font=('Arial', 10, 'bold'))
style.configure('TEntry', font=('Arial', 10))
style.configure('TCombobox', font=('Arial', 10))

# Marco principal
main_frame = ttk.Frame(ventana, padding="15")
main_frame.pack(fill=tk.BOTH, expand=True)

# Título
ttk.Label(main_frame, text="Calculadora de Rutas en Puno", font=('Arial', 14, 'bold')).grid(row=0, column=0, columnspan=2, pady=10)

# Sección de origen
ttk.Label(main_frame, text="Origen:").grid(row=1, column=0, sticky=tk.W, pady=5)
entrada_origen = ttk.Entry(main_frame, width=40)
entrada_origen.grid(row=2, column=0, pady=5, padx=5, sticky=tk.EW)

combo_origen = ttk.Combobox(main_frame, values=LUGARES_PUNO, state="readonly")
combo_origen.grid(row=3, column=0, pady=5, padx=5, sticky=tk.EW)
combo_origen.bind("<<ComboboxSelected>>", lambda e: seleccionar_lugar(e, entrada_origen))
combo_origen.set("-- Selecciona un lugar --")

# Sección de destino
ttk.Label(main_frame, text="Destino:").grid(row=1, column=1, sticky=tk.W, pady=5)
entrada_destino = ttk.Entry(main_frame, width=40)
entrada_destino.grid(row=2, column=1, pady=5, padx=5, sticky=tk.EW)

combo_destino = ttk.Combobox(main_frame, values=LUGARES_PUNO, state="readonly")
combo_destino.grid(row=3, column=1, pady=5, padx=5, sticky=tk.EW)
combo_destino.bind("<<ComboboxSelected>>", lambda e: seleccionar_lugar(e, entrada_destino))
combo_destino.set("-- Selecciona un lugar --")

# Ejemplos pre-cargados
entrada_origen.insert(0, "Mercado Bellavista")
entrada_destino.insert(0, "Catedral de Puno")

# Barra de progreso
progress_bar = ttk.Progressbar(main_frame, mode='indeterminate', length=200)
progress_bar.grid(row=4, column=0, columnspan=2, pady=15)

# Botón de cálculo
calcular_btn = ttk.Button(main_frame, text="Calcular Ruta", command=calcular_ruta, style='TButton')
calcular_btn.grid(row=5, column=0, columnspan=2, pady=10)

# Nota informativa
ttk.Label(main_frame, 
         text="Nota: También puedes escribir direcciones manualmente o seleccionar de la lista",
         font=('Arial', 8), 
         foreground="gray").grid(row=6, column=0, columnspan=2, pady=5)

ventana.mainloop()