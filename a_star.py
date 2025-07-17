import math
import heapq
from utils import obtener_nodo_mas_cercano
from puntos import UNIVERSIDAD, COLEGIOS, MERCADOS, PARQUES, HOSPITALES

class Nodo:
    def __init__(self, id, lat, lon):
        self.id = id
        self.lat = lat
        self.lon = lon
        self.vecinos = []  # Lista de tuplas: (nodo_id, peso)

    def agregar_vecino(self, vecino_id, peso):
        self.vecinos.append((vecino_id, peso))


def heuristica(nodo_a, nodo_b):
    """Distancia euclidiana entre dos nodos"""
    return math.sqrt((nodo_a.lat - nodo_b.lat)**2 + (nodo_a.lon - nodo_b.lon)**2)


def a_star(grafo, origen_id, destino_id):
    if origen_id not in grafo or destino_id not in grafo:
        return []

    abiertos = []  # (f_score, nodo_id)
    heapq.heappush(abiertos, (0, origen_id))

    came_from = {}
    g_score = {nodo_id: float('inf') for nodo_id in grafo}
    g_score[origen_id] = 0

    f_score = {nodo_id: float('inf') for nodo_id in grafo}
    f_score[origen_id] = heuristica(grafo[origen_id], grafo[destino_id])

    while abiertos:
        _, actual = heapq.heappop(abiertos)

        if actual == destino_id:
            return reconstruir_camino(came_from, actual, grafo)

        for vecino_id, peso in grafo[actual].vecinos:
            tentativo_g = g_score[actual] + peso
            if tentativo_g < g_score[vecino_id]:
                came_from[vecino_id] = actual
                g_score[vecino_id] = tentativo_g
                f_score[vecino_id] = tentativo_g + heuristica(grafo[vecino_id], grafo[destino_id])
                heapq.heappush(abiertos, (f_score[vecino_id], vecino_id))

    return []  # No se encontró ruta


def reconstruir_camino(came_from, nodo_actual, grafo):
    ruta_ids = [nodo_actual]
    while nodo_actual in came_from:
        nodo_actual = came_from[nodo_actual]
        ruta_ids.append(nodo_actual)
    ruta_ids.reverse()
    return [(grafo[nid].lat, grafo[nid].lon) for nid in ruta_ids]
print("[OK] a_star.py cargado correctamente.")
