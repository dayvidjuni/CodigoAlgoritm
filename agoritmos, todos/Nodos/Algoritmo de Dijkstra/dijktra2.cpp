#include <iostream>
#include <vector>
#include <queue>
#include <utility>
#include <climits>
#include <random>
#include <chrono>
#include <algorithm>

using namespace std;

// Generar grafo conectado con conexiones aleatorias
vector<vector<pair<int, int>>> generarGrafo(int n, int conexionesPorNodo) {
    vector<vector<pair<int, int>>> grafo(n);
    random_device rd;
    mt19937 gen(rd());
    uniform_int_distribution<> distNodo(0, n - 1);
    uniform_int_distribution<> distPeso(1,20);

    // Paso 1: conectar todos los nodos en cadena para garantizar conectividad
    for (int u = 0; u < n - 1; ++u) {
        int peso = distPeso(gen);
        grafo[u].emplace_back(u + 1, peso);
        grafo[u + 1].emplace_back(u, peso);
    }

    // Paso 2: añadir conexiones aleatorias adicionales sin duplicar
    for (int u = 0; u < n; ++u) {
        int maxConexiones = min(conexionesPorNodo, n - 1);  // evitar bucle infinito
        while ((int)grafo[u].size() < maxConexiones) {
            int v = distNodo(gen);
            if (v == u) continue;

            // Verifica si ya existe la conexión u-v
            bool existe = false;
            for (auto& par : grafo[u]) {
                if (par.first == v) {
                    existe = true;
                    break;
                }
            }

            if (!existe) {
                int peso = distPeso(gen);
                grafo[u].emplace_back(v, peso);
                grafo[v].emplace_back(u, peso);
            }
        }
    }

    return grafo;
}

// Algoritmo de Dijkstra
vector<int> dijkstra(int n, const vector<vector<pair<int, int>>>& grafo, int inicio) {
    vector<int> dist(n, INT_MAX);
    priority_queue<pair<int, int>, vector<pair<int, int>>, greater<pair<int, int>>> pq;

    dist[inicio] = 0;
    pq.emplace(0, inicio);

    while (!pq.empty()) {
        pair<int, int> top = pq.top(); pq.pop();
        int d = top.first;
        int u = top.second;

        if (d > dist[u]) continue;

        for (const auto& edge : grafo[u]) {
            int v = edge.first;
            int w = edge.second;
            if (dist[u] + w < dist[v]) {
                dist[v] = dist[u] + w;
                pq.emplace(dist[v], v);
            }
        }
    }

    return dist;
}

// Función para medir tiempo de ejecución
void ejecutarCaso(int n, int conexionesPorNodo) {
    cout << "\n=== Grafo con " << n << " nodos ===" << endl;

    auto grafo = generarGrafo(n, conexionesPorNodo);

    auto start = chrono::steady_clock::now();
    vector<int> distancias = dijkstra(n, grafo, 0);
    auto end = chrono::steady_clock::now();

    chrono::duration<double, std::milli> duracion = end - start;
    cout << "Tiempo de ejecucion: " << duracion.count() << " ms" << endl;

    // Mostrar distancias si n es pequeño
    if (n <= 10) {
        cout << "Distancias desde nodo 0:" << endl;
        for (int i = 0; i < n; ++i) {
            cout << "Nodo " << i << ": " << distancias[i] << endl;
        }
    }
}


int main() {
    ejecutarCaso(10, 2);     // Grafo pequeño
    //ejecutarCaso(100, 5);    // Grafo mediano
    //ejecutarCaso(1000, 10);  // Grafo grande

    cin.get(); // Reemplaza system("pause") para mayor portabilidad
    return 0;
}