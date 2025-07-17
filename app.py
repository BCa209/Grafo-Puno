import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from dibujar_grafo import dibujar_grafo
from tkintermapview import TkinterMapView   
from utils import cargar_grafo, obtener_nodo_mas_cercano
from dijkstra import construir_grafo, dijkstra
from a_star import a_star
from puntos import UNIVERSIDAD, COLEGIOS, MERCADOS, PARQUES, HOSPITALES

# === Cargar grafo ===
G = cargar_grafo()
grafo = construir_grafo()

# === Variables globales ===
origen_id = None
destino_id = None
ruta_actual = None
marcadores_temporales = []
marcadores_grafo = []
mostrar_marcadores = False
mostrar_puntos_interes = False
marcadores_puntos_interes = []
origen_nombre = ""
destino_nombre = ""

# === App tkinter ===
root = tk.Tk()
root.geometry("1200x800")
root.title("Mapa con Dijkstra y puntos de interés")
ruta_info_var = tk.StringVar()

root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=3)
root.columnconfigure(0, weight=3)
root.columnconfigure(1, weight=2)

# === Frames ===
frame_superior = tk.Frame(root, bg="lightblue")
frame_superior.grid(row=0, column=0, columnspan=2, sticky="nsew")

frame_derecha = tk.Frame(root, bg="lightgray")
frame_derecha.grid(row=1, column=1, sticky="nsew")

map_widget = TkinterMapView(root, corner_radius=0)
map_widget.grid(row=1, column=0, sticky="nsew")
map_widget.set_position(-15.84876, -70.02135)
map_widget.set_zoom(16)

# === Funciones ===
def mostrar_marcadores_grafo():
    global marcadores_grafo
    for node_id in G.nodes:
        lat = G.nodes[node_id]["lat"]
        lon = G.nodes[node_id]["lon"]
        marcador = map_widget.set_marker(lat, lon,)
        marcadores_grafo.append(marcador)

def ocultar_marcadores_grafo():
    global marcadores_grafo
    for marcador in marcadores_grafo:
        marcador.delete()
    marcadores_grafo = []

def alternar_marcadores():
    global mostrar_marcadores
    if mostrar_marcadores:
        ocultar_marcadores_grafo()
        btn_toggle_marcadores.config(text="Mostrar Nodos")
    else:
        mostrar_marcadores_grafo()
        btn_toggle_marcadores.config(text="Ocultar Nodos")
    mostrar_marcadores = not mostrar_marcadores

def mostrar_puntos():
    global marcadores_puntos_interes
    for clave, info in TODOS_PUNTOS.items():
        lat, lon = info["centro"]
        marcador = map_widget.set_marker(lat, lon, text=info.get("etiqueta", clave), marker_color_circle="blue", marker_color_outside="white")
        marcadores_puntos_interes.append(marcador)

def ocultar_puntos():
    global marcadores_puntos_interes
    for marcador in marcadores_puntos_interes:
        marcador.delete()
    marcadores_puntos_interes = []

def click_en_mapa(event):
    global origen_id, destino_id, marcadores_temporales

    lat, lon = map_widget.convert_canvas_coords_to_decimal_coords(event.x, event.y)
    nodo_cercano = obtener_nodo_mas_cercano(G, lat, lon)

    if not origen_id:
        origen_id = nodo_cercano
        coord = (G.nodes[origen_id]["lat"], G.nodes[origen_id]["lon"])
        marcador = map_widget.set_marker(*coord, text="🟢 Origen")
        marcadores_temporales.append(marcador)
    elif not destino_id:
        destino_id = nodo_cercano
        coord = (G.nodes[destino_id]["lat"], G.nodes[destino_id]["lon"])
        marcador = map_widget.set_marker(*coord, text="🔴 Destino")
        marcadores_temporales.append(marcador)

def calcular_ruta():
    global origen_id, destino_id, ruta_actual
    if origen_id and destino_id:
        ruta = dijkstra(grafo, origen_id, destino_id)
        if ruta:
            if ruta_actual:
                ruta_actual.delete()
            ruta_actual = map_widget.set_path(ruta)

            # Mostrar info de ruta
            origen_etiqueta = origen_var.get() if origen_var.get() in TODOS_PUNTOS else str(origen_id)
            destino_etiqueta = destino_var.get() if destino_var.get() in TODOS_PUNTOS else str(destino_id)
            if origen_etiqueta in TODOS_PUNTOS:
                origen_etiqueta = TODOS_PUNTOS[origen_etiqueta]["etiqueta"]
            if destino_etiqueta in TODOS_PUNTOS:
                destino_etiqueta = TODOS_PUNTOS[destino_etiqueta]["etiqueta"]
            ruta_info_var.set(f"Ruta desde '{origen_etiqueta}' hasta '{destino_etiqueta}' usando Dijkstra")
        else:
            ruta_info_var.set("No se pudo calcular la ruta.")
    else:
        ruta_info_var.set("Selecciona origen y destino.")

def calcular_ruta_astar():
    global origen_id, destino_id, ruta_actual
    if origen_id and destino_id:
        ruta = a_star(grafo, origen_id, destino_id)
        if ruta:
            if ruta_actual:
                ruta_actual.delete()
            ruta_actual = map_widget.set_path(ruta)

            # Mostrar info de ruta
            origen_etiqueta = origen_var.get() if origen_var.get() in TODOS_PUNTOS else str(origen_id)
            destino_etiqueta = destino_var.get() if destino_var.get() in TODOS_PUNTOS else str(destino_id)
            if origen_etiqueta in TODOS_PUNTOS:
                origen_etiqueta = TODOS_PUNTOS[origen_etiqueta]["etiqueta"]
            if destino_etiqueta in TODOS_PUNTOS:
                destino_etiqueta = TODOS_PUNTOS[destino_etiqueta]["etiqueta"]
            ruta_info_var.set(f"Ruta desde '{origen_etiqueta}' hasta '{destino_etiqueta}' usando A*")
        else:
            ruta_info_var.set("No se pudo calcular la ruta.")
    else:
        ruta_info_var.set("Selecciona origen y destino.")

def reiniciar():
    global origen_id, destino_id, ruta_actual, marcadores_temporales
    origen_id = None
    destino_id = None
    for m in marcadores_temporales:
        m.delete()
    marcadores_temporales = []
    if ruta_actual:
        ruta_actual.delete()
        ruta_actual = None
    ruta_info_var.set("")

def mostrar_grafo_en_ventana():
    dibujar_grafo("utils/grafo.png")
    ventana = tk.Toplevel(root)
    ventana.title("Imagen del Grafo")
    ventana.geometry("800x800")

    img = Image.open("grafo.png")
    img = img.resize((780, 780), Image.Resampling.LANCZOS)
    img_tk = ImageTk.PhotoImage(img)

    label = tk.Label(ventana, image=img_tk)
    label.image = img_tk
    label.pack(padx=10, pady=10)

def set_origen_desde_dropdown(event):
    global origen_id
    key = origen_var.get()
    punto = TODOS_PUNTOS.get(key)
    if punto:
        origen_nombre =key
        lat, lon = punto["centro"]
        origen_id = obtener_nodo_mas_cercano(G, lat, lon)
        marcador = map_widget.set_marker(lat, lon, text="🟢 Origen")
        marcadores_temporales.append(marcador)

def set_destino_desde_dropdown(event):
    global destino_id
    key = destino_var.get()
    punto = TODOS_PUNTOS.get(key)
    if punto:
        destino_nombre = key
        lat, lon = punto["centro"]
        destino_id = obtener_nodo_mas_cercano(G, lat, lon)
        marcador = map_widget.set_marker(lat, lon, text="🔴 Destino")
        marcadores_temporales.append(marcador)

# === Reunir todos los puntos en un solo dict para los dropdowns ===
TODOS_PUNTOS = {**UNIVERSIDAD, **COLEGIOS, **MERCADOS, **PARQUES, **HOSPITALES}

# === Elementos UI superiores ===
btn_toggle_marcadores = tk.Button(frame_superior, text="Mostrar Nodos", command=alternar_marcadores)
btn_toggle_marcadores.pack(side="left", padx=10, pady=10)

def alternar_puntos_interes():
    global mostrar_puntos_interes
    if mostrar_puntos_interes:
        ocultar_puntos()
        btn_toggle_puntos.config(text="Mostrar Puntos")
    else:
        mostrar_puntos()
        btn_toggle_puntos.config(text="Ocultar Puntos")
    mostrar_puntos_interes = not mostrar_puntos_interes

btn_toggle_puntos = tk.Button(frame_superior, text="Mostrar Puntos", command=alternar_puntos_interes)
btn_toggle_puntos.pack(side="left", padx=10)

btn_ver_grafo = tk.Button(frame_superior, text="Mostrar Grafo", command=mostrar_grafo_en_ventana)
btn_ver_grafo.pack(side="left", padx=10, pady=10)

ruta_info_label = tk.Label(frame_superior, textvariable=ruta_info_var, bg="lightblue", font=("Arial", 11))
ruta_info_label.pack(side="left", padx=10)

# Dropdowns de puntos de interés
origen_var = tk.StringVar()
destino_var = tk.StringVar()

origen_menu = ttk.Combobox(frame_superior, textvariable=origen_var, values=list(TODOS_PUNTOS.keys()))
origen_menu.set("Origen desde punto...")
origen_menu.bind("<<ComboboxSelected>>", set_origen_desde_dropdown)
origen_menu.pack(side="left", padx=10)

destino_menu = ttk.Combobox(frame_superior, textvariable=destino_var, values=list(TODOS_PUNTOS.keys()))
destino_menu.set("Destino desde punto...")
destino_menu.bind("<<ComboboxSelected>>", set_destino_desde_dropdown)
destino_menu.pack(side="left", padx=10)

# === Botones laterales ===
btn_dijkstra = tk.Button(frame_derecha, text="Ruta Dijkstra", font=("Arial", 12), command=calcular_ruta)
btn_dijkstra.pack(pady=20)

btn_astar = tk.Button(frame_derecha, text="Ruta A*", font=("Arial", 12), command=calcular_ruta_astar)
btn_astar.pack(pady=10)

btn_reset = tk.Button(frame_derecha, text="Reiniciar", font=("Arial", 12), command=reiniciar)
btn_reset.pack(pady=10)


# === Inicializaciones ===
map_widget.canvas.bind("<Button-3>", click_en_mapa)
#mostrar_marcadores_grafo()
#mostrar_puntos()

# === Ejecutar ===
root.mainloop()