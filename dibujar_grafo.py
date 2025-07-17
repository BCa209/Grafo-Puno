import json
import networkx as nx
import matplotlib.pyplot as plt
import os

def dibujar_grafo(output_path="utils/grafo.png"):
    # Si ya existe, no volver a generarlo
    if os.path.exists(output_path):
        print(f"[OK] Imagen ya existente: {output_path}")
        return

    print("[8] Generando imagen del grafo...")
    with open("utils/nodos.json", "r", encoding="utf-8") as f:
        nodos = json.load(f)

    with open("utils/aristas.json", "r", encoding="utf-8") as f:
        aristas = json.load(f)

    G = nx.DiGraph()
    pos = {}

    for nodo in nodos:
        G.add_node(nodo["id"])
        pos[nodo["id"]] = (nodo["lon"], nodo["lat"])  # (x, y)

    for arista in aristas:
        G.add_edge(arista["from"], arista["to"])

    plt.figure(figsize=(10, 10))
    nx.draw(G, pos, node_size=20, node_color="red", arrows=True, with_labels=False)
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    print(f"[OK] Imagen del grafo guardada en {output_path}")
