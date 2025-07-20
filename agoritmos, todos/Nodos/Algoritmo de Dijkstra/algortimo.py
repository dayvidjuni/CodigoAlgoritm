import heapq

def dijkstra(start, graph):
    n = len(graph)
    dist = [float('inf')] * n
    dist[start] = 0
    prev = [None] * n  # Para reconstruir el camino

    pq = [(0, start)]  # (distancia, nodo)

    while pq:
        current_dist, u = heapq.heappop(pq)

        if current_dist > dist[u]:
            continue

        for v, weight in graph[u]:
            if dist[u] + weight < dist[v]:
                dist[v] = dist[u] + weight
                prev[v] = u  # Guardamos el nodo anterior
                heapq.heappush(pq, (dist[v], v))

    # Función para reconstruir el camino desde el nodo inicial
    def reconstruir_camino(destino):
        camino = []
        while destino is not None:
            camino.append(destino)
            destino = prev[destino]
        return list(reversed(camino))

    # Imprimir distancias y caminos
    for i in range(n):
        if dist[i] == float('inf'):
            print(f"Distancia desde {start} a {i}: INF (no alcanzable)")
        else:
            camino = reconstruir_camino(i)
            print(f"Distancia desde {start} a {i}: {dist[i]} | Camino: {' -> '.join(map(str, camino))}")

# Ejemplo de grafo no dirigido
n = 6
graph = [[] for _ in range(n)]

graph[0].append((1, 2))
graph[0].append((2, 3))

graph[1].append((3, 5))
graph[1].append((4, 2))
graph[1].append((0, 2))

graph[2].append((0, 3))
graph[2].append((4, 5))

graph[3].append((1, 5))
graph[3].append((4, 1))
graph[3].append((5, 2))

graph[4].append((1, 2))
graph[4].append((2, 5))
graph[4].append((3, 1))
graph[4].append((5, 4))

graph[5].append((3, 2))
graph[5].append((4, 4))

dijkstra(0, graph)
