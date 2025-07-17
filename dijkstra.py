import json
import heapq

# Clase Nodo básica
class Nodo:
    def __init__(self, id, lat, lon):
        self.id = id
        self.lat = lat
        self.lon = lon
        self.vecinos = []  # lista de tuplas: (id_vecino, peso)

    def agregar_vecino(self, vecino_id, peso):
        self.vecinos.append((vecino_id, peso))


def construir_grafo(nodos_path="utils/nodos.json", aristas_path="utils/aristas.json"):
    """Construye el grafo como diccionario de Nodo desde archivos JSON."""
    with open(nodos_path, "r", encoding="utf-8") as f:
        nodos_json = json.load(f)
    with open(aristas_path, "r", encoding="utf-8") as f:
        aristas_json = json.load(f)

    grafo = {}
    for nodo in nodos_json:
        grafo[nodo["id"]] = Nodo(nodo["id"], nodo["lat"], nodo["lon"])

    for arista in aristas_json:
        origen = arista["from"]
        destino = arista["to"]
        peso = arista["length"]
        if origen in grafo:
            grafo[origen].agregar_vecino(destino, peso)

    return grafo

def dijkstra(grafo, origen_id, destino_id):
    """Algoritmo de Dijkstra desde cero: retorna lista de coordenadas (lat, lon)."""
    distancias = {nodo_id: float("inf") for nodo_id in grafo}
    anteriores = {nodo_id: None for nodo_id in grafo}
    distancias[origen_id] = 0

    visitados = set()
    heap = [(0, origen_id)]

    while heap:
        distancia_actual, actual_id = heapq.heappop(heap)

        if actual_id in visitados:
            continue
        visitados.add(actual_id)

        if actual_id == destino_id:
            break

        nodo_actual = grafo[actual_id]
        for vecino_id, peso in nodo_actual.vecinos:
            nueva_distancia = distancia_actual + peso
            if nueva_distancia < distancias[vecino_id]:
                distancias[vecino_id] = nueva_distancia
                anteriores[vecino_id] = actual_id
                heapq.heappush(heap, (nueva_distancia, vecino_id))

    # Reconstruir camino desde destino hacia origen
    camino_ids = []
    actual = destino_id
    while actual is not None:
        camino_ids.insert(0, actual)
        actual = anteriores[actual]

    if not camino_ids or camino_ids[0] != origen_id:
        return []  # No se encontró camino válido

    return [(grafo[nodo_id].lat, grafo[nodo_id].lon) for nodo_id in camino_ids]
print("[OK] dijkstra.py cargado correctamente.")