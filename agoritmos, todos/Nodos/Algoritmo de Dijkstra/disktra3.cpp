#include <iostream>
#include <vector>
#include <queue>
#include <utility>
#include <climits>
#include <random>
#include <chrono>
#include <algorithm>

using namespace std;

// Clase Nodo
class Nodo {
public:
    int id;
    vector<pair<int, int>> adyacentes; // (vecino, peso)

    Nodo(int id) : id(id) {}
    
    void agregarArista(int destino, int peso) {
        adyacentes.emplace_back(destino, peso);
    }

    bool existeConexion(int destino) {
        for (size_t i = 0; i < adyacentes.size(); ++i) {
            if (adyacentes[i].first == destino) return true;
        }
        return false;
    }
};

// Clase Grafo
class Grafo {
private:
    vector<Nodo> nodos;
    mt19937 gen;
    uniform_int_distribution<> distPeso;

public:
    Grafo(int n) : distPeso(1, 20), gen(random_device{}()) {
        for (int i = 0; i < n; ++i) {
            nodos.emplace_back(i);
        }
    }

    void generarConexiones(int conexionesPorNodo) {
        int n = nodos.size();
        uniform_int_distribution<> distNodo(0, n - 1);

        // Paso 1: conectar todos los nodos en cadena para garantizar conectividad
        for (int u = 0; u < n - 1; ++u) {
            int peso = distPeso(gen);
            nodos[u].agregarArista(u + 1, peso);
            nodos[u + 1].agregarArista(u, peso);
        }

        // Paso 2: añadir conexiones aleatorias adicionales
        for (int u = 0; u < n; ++u) {
            int maxConexiones = min(conexionesPorNodo, n - 1);
            while ((int)nodos[u].adyacentes.size() < maxConexiones) {
                int v = distNodo(gen);
                if (v == u || nodos[u].existeConexion(v)) continue;

                int peso = distPeso(gen);
                nodos[u].agregarArista(v, peso);
                nodos[v].agregarArista(u, peso);
            }
        }
    }

    const vector<Nodo>& obtenerNodos() const {
        return nodos;
    }

    vector<int> dijkstra(int inicio) const {
        int n = nodos.size();
        vector<int> dist(n, INT_MAX);
        priority_queue<pair<int, int>, vector<pair<int, int>>, greater<pair<int, int>>> pq;

        dist[inicio] = 0;
        pq.emplace(0, inicio);

        while (!pq.empty()) {
            pair<int, int> top = pq.top(); pq.pop();
            int d = top.first;
            int u = top.second;

            if (d > dist[u]) continue;

            for (size_t i = 0; i < nodos[u].adyacentes.size(); ++i) {
                int v = nodos[u].adyacentes[i].first;
                int peso = nodos[u].adyacentes[i].second;

                if (dist[u] + peso < dist[v]) {
                    dist[v] = dist[u] + peso;
                    pq.emplace(dist[v], v);
                }
            }
        }

        return dist;
    }
};

// Función para ejecutar un caso de prueba
void ejecutarCaso(int n, int conexionesPorNodo) {
    cout << "\n=== Grafo con " << n << " nodos ===" << endl;

    Grafo grafo(n);
    grafo.generarConexiones(conexionesPorNodo);

    auto start = chrono::steady_clock::now();
    vector<int> distancias = grafo.dijkstra(0);
    auto end = chrono::steady_clock::now();

    chrono::duration<double, milli> duracion = end - start;
    cout << "Tiempo de ejecucion: " << duracion.count() << " ms" << endl;

    if (n <= 10) {
        cout << "Distancias desde nodo 0:" << endl;
        for (int i = 0; i < n; ++i) {
            cout << "Nodo " << i << ": " << distancias[i] << endl;
        }
    }
}

int main() {
    ejecutarCaso(10, 2);     // Grafo pequeño
    // ejecutarCaso(100, 5); // Grafo mediano
    // ejecutarCaso(1000, 10); // Grafo grande

    cin.get(); // Espera entrada para terminar
    return 0;
}
