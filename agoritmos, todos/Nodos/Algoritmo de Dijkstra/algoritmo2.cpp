#include <iostream>
#include <limits>
#include <queue> 

using namespace std;

const int INF = numeric_limits<int>::max();

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

    void dijkstra(int inicio) {
        int* dist = new int[numNodos];
        bool* visitado = new bool[numNodos];

        for (int i = 0; i < numNodos; i++) {
            dist[i] = INF;
            visitado[i] = false;
        }
        dist[inicio] = 0;

        /*la cola  */
        priority_queue<pair<int, int>, vector<pair<int, int>>, greater<pair<int, int>>> pq;
        pq.push({0, inicio});

        while (!pq.empty()) {
            int u = pq.top().second;
            pq.pop();

            if (visitado[u]) continue;
            visitado[u] = true;

            Arista* temp = nodos[u]->adyacentes;
            while (temp != nullptr) {
                int v = temp->destino;
                int peso = temp->peso;

                if (!visitado[v] && dist[u] + peso < dist[v]) {
                    dist[v] = dist[u] + peso;
                    pq.push({dist[v], v});
                }

                temp = temp->siguiente;
            }
        }

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

    g.agregarArista(0, 1, 2);
    g.agregarArista(1, 0, 2);
    g.agregarArista(0, 2, 4);
    g.agregarArista(2, 0, 4);
    g.agregarArista(1, 2, 1);
    g.agregarArista(2, 1, 1);
    g.agregarArista(1, 3, 7);
    g.agregarArista(3, 1, 7);
    g.agregarArista(2, 4, 3);
    g.agregarArista(4, 2, 3);
    g.agregarArista(3, 4, 1);
    g.agregarArista(4, 3, 1);

    g.dijkstra(0);

    system("pause");
    return 0;
}