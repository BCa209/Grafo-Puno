import osmnx as ox
import json
import os

# Crear carpeta si no existe
os.makedirs("utils", exist_ok=True)

# Nombre exacto del lugar (provincias son unidades administrativas)
place_name = "Puno, Puno, Perú"

# Descargar grafo de red vial (solo para autos)
G = ox.graph_from_place(place_name, network_type='drive')

# Nodos
nodes = [{"id": nid, "lat": data["y"], "lon": data["x"]} for nid, data in G.nodes(data=True)]
with open("utils/nodos.json", "w", encoding="utf-8") as f:
    json.dump(nodes, f, indent=2, ensure_ascii=False)

# Aristas
edges = [{
    "from": u,
    "to": v,
    "length": data.get("length", 1.0),
    "name": data.get("name", ""),
    "highway": data.get("highway", "")
} for u, v, data in G.edges(data=True)]
with open("utils/aristas.json", "w", encoding="utf-8") as f:
    json.dump(edges, f, indent=2, ensure_ascii=False)

print("[OK] Calles de la provincia de Puno extraídas exitosamente.")
