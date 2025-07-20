import random
import heapq
import time

def generar_grafo(n, conexiones_por_nodo):
    grafo = {i: [] for i in range(n)}

    # Paso 1: cadena para asegurar conectividad
    for u in range(n - 1):
        peso = random.randint(1, 20)
        grafo[u].append((u + 1, peso))
        grafo[u + 1].append((u, peso))

    # Paso 2: agregar conexiones aleatorias sin duplicados
    for u in range(n):
        while len(grafo[u]) < conexiones_por_nodo:
            v = random.randint(0, n - 1)
            if v == u or any(vecino == v for vecino, _ in grafo[u]):
                continue
            peso = random.randint(1, 20)
            grafo[u].append((v, peso))
            grafo[v].append((u, peso))

    return grafo

def dijkstra(grafo, inicio):
    dist = {nodo: float('inf') for nodo in grafo}
    dist[inicio] = 0
    heap = [(0, inicio)]

    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            continue
        for v, peso in grafo[u]:
            if dist[u] + peso < dist[v]:
                dist[v] = dist[u] + peso
                heapq.heappush(heap, (dist[v], v))

    return dist

def main():
    n = 1000  # número de nodos
    conexiones_por_nodo = 10

    grafo = generar_grafo(n, conexiones_por_nodo)

    inicio = 0
    start_time = time.perf_counter()
    distancias = dijkstra(grafo, inicio)
    end_time = time.perf_counter()

    duracion_ms = (end_time - start_time) * 1000
    print(f"Tiempo de ejecución: {duracion_ms:.3f} ms")
    print(f"Distancias desde nodo {inicio}:")
    for nodo in sorted(distancias):
        if distancias[nodo] == float('inf'):
            print(f"Nodo {nodo}: INALCANZABLE")
        else:
            print(f"Nodo {nodo}: {distancias[nodo]}")

if __name__ == "__main__":
    main()
