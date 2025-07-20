#include <iostream>
#include <limits>

using namespace std;

const int INF = numeric_limits<int>::max(); // Infinito

// Nodo de lista de adyacencia
class Arista {
public:
    int destino;
    int peso;
    Arista* siguiente;
    Arista(int destino, int peso) {
        this->destino = destino;
        this->peso = peso;
        this->siguiente = nullptr;
    }
};

// Nodo del grafo
class Nodo {
public:
    int id;
    Arista* adyacentes;

    Nodo(int id) {
        this->id = id;
        this->adyacentes = nullptr;
    }

    void agregarArista(int destino, int peso) {
        Arista* nueva = new Arista(destino, peso);
        nueva->siguiente = adyacentes;
        adyacentes = nueva;
    }
};

// Clase Grafo
class Grafo {
private:
    int numNodos;
    Nodo** nodos;

public:
    Grafo(int n) {
        numNodos = n;
        nodos = new Nodo*[n];
        for (int i = 0; i < n; i++) {
            nodos[i] = new Nodo(i);
        }
    }

    void agregarArista(int origen, int destino, int peso) {
        nodos[origen]->agregarArista(destino, peso);
    }

    int encontrarMinDistancia(int dist[], bool visitado[]) {
        int min = INF;
        int indice = -1;

        for (int i = 0; i < numNodos; i++) {
            if (!visitado[i] && dist[i] < min) {
                min = dist[i];
                indice = i;
            }
        }
        return indice;
    }

    void dijkstra(int inicio) {
        int* dist = new int[numNodos];
        bool* visitado = new bool[numNodos];

        // Inicializar
        for (int i = 0; i < numNodos; i++) {
            dist[i] = INF;
            visitado[i] = false;
        }
        dist[inicio] = 0;

        for (int i = 0; i < numNodos - 1; i++) {
            int u = encontrarMinDistancia(dist, visitado);
            if (u == -1) break;

            visitado[u] = true;

            Arista* temp = nodos[u]->adyacentes;
            while (temp != nullptr) {
                int v = temp->destino;
                int peso = temp->peso;

                if (!visitado[v] && dist[u] != INF && dist[u] + peso < dist[v]) {
                    dist[v] = dist[u] + peso;
                }

                temp = temp->siguiente;
            }
        }

        // Mostrar resultado
        cout << "Distancias mínimas desde el nodo " << inicio << ":\n";
        for (int i = 0; i < numNodos; i++) {
            if (dist[i] == INF)
                cout << "Nodo " << i << ": INF" << endl;
            else
                cout << "Nodo " << i << ": " << dist[i] << endl;
        }

        delete[] dist;
        delete[] visitado;
    }

    ~Grafo() {
        for (int i = 0; i < numNodos; i++) {
            Arista* temp = nodos[i]->adyacentes;
            while (temp != nullptr) {
                Arista* borrar = temp;
                temp = temp->siguiente;
                delete borrar;
            }
            delete nodos[i];
        }
        delete[] nodos;
    }
};

int main() {
    Grafo g(5); 

    g.agregarArista(0, 1, 2);  // 0 → 1 (peso 2)
    g.agregarArista(1, 0, 2);  // 1 → 0 (peso 2)

    g.agregarArista(0, 2, 4);  // 0 → 2 (peso 4)
    g.agregarArista(2, 0, 4);  // 2 → 0 (peso 4)

    g.agregarArista(1, 2, 1);  // 1 → 2 (peso 1)
    g.agregarArista(2, 1, 1);  // 2 → 1 (peso 1)

    g.agregarArista(1, 3, 7);  // 1 → 3 (peso 7)
    g.agregarArista(3, 1, 7);  // 3 → 1 (peso 7)

    g.agregarArista(2, 4, 3);  // 2 → 4 (peso 3)
    g.agregarArista(4, 2, 3);  // 4 → 2 (peso 3)

    g.agregarArista(3, 4, 1);  // 3 → 4 (peso 1)
    g.agregarArista(4, 3, 1);

    g.dijkstra(0); // Desde el nodo 0

    system("pause");
    return 0;
}
