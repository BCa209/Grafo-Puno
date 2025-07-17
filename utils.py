import json
import networkx as nx
import os

# Ruta relativa a la carpeta del proyecto
NODOS_PATH = os.path.join("utils", "nodos.json")
ARISTAS_PATH = os.path.join("utils", "aristas.json")

def cargar_grafo():
    """Carga el grafo desde los archivos JSON de nodos y aristas."""
    with open(NODOS_PATH, "r", encoding="utf-8") as f:
        nodos = json.load(f)
    with open(ARISTAS_PATH, "r", encoding="utf-8") as f:
        aristas = json.load(f)

    G = nx.DiGraph()
    for nodo in nodos:
        G.add_node(nodo["id"], lat=nodo["lat"], lon=nodo["lon"])
    for arista in aristas:
        G.add_edge(arista["from"], arista["to"], length=arista["length"])
    return G

def obtener_posicion_nodo(G, node_id):
    """Devuelve (lat, lon) de un nodo dado su ID."""
    return (G.nodes[node_id]["lat"], G.nodes[node_id]["lon"])

def obtener_nodo_mas_cercano(G, lat, lon):
    """Encuentra el nodo más cercano a una coordenada (lat, lon)."""
    min_dist = float("inf")
    nodo_cercano = None
    for node_id, data in G.nodes(data=True):
        d = (data["lat"] - lat)**2 + (data["lon"] - lon)**2
        if d < min_dist:
            min_dist = d
            nodo_cercano = node_id
    return nodo_cercano
