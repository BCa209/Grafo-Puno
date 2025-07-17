import json
import networkx as nx
import matplotlib.pyplot as plt

# Cargar nodos y aristas
with open("utils/nodos.json", "r") as f:
    nodes = json.load(f)
with open("utils/aristas.json", "r") as f:
    edges = json.load(f)

# Crear grafo dirigido
G = nx.DiGraph()
for node in nodes:
    G.add_node(node["id"], pos=(node["lon"], node["lat"]))  # (x=lon, y=lat)

for edge in edges:
    G.add_edge(edge["from"], edge["to"], length=edge["length"])

# Obtener posiciones
pos = nx.get_node_attributes(G, "pos")

# Dibujar grafo
plt.figure(figsize=(10, 10))
nx.draw(G, pos, node_size=20, node_color="red", edge_color="gray", arrows=True, width=1)
plt.title("Grafo de intersecciones (OpenStreetMap)")
plt.axis("off")
plt.tight_layout()

# Guardar como imagen
plt.savefig("grafo_mapa.png", dpi=300)
plt.show()
