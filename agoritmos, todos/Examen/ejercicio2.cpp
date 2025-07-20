#include <iostream>
using namespace std;

struct AdjNode {
    int index;
    int weight;
    AdjNode* next;
    AdjNode(int idx, int w) : index(idx), weight(w), next(nullptr) {}
};

struct Node {
    string name;
    AdjNode* adjList;
    Node(string n) : name(n), adjList(nullptr) {}
};

class Graph {
private:
    Node** nodes;
    int capacity;
    int nodeCount;

public:
    Graph() {
        capacity = 5;
        nodeCount = 0;
        nodes = new Node*[capacity];
    }

    int getIndex(string name) {
        for (int i = 0; i < nodeCount; i++) {
            if (nodes[i]->name == name)
                return i;
        }
        return -1;
    }

    void dfsExists(int current, int target, bool* visited, bool& found) {
        if (current == target) {
            found = true;
            return;
        }

        visited[current] = true;
        AdjNode* adj = nodes[current]->adjList;
        while (adj) {
            if (!visited[adj->index])
            
                dfsExists(adj->index, target, visited, found);
            adj = adj->next;
        }
    }

    void dfsPaths(int current, int target, bool* visited, string* path, int level) {
        visited[current] = true;
        path[level] = nodes[current]->name;
        level++;

        if (current == target) {
            for (int i = 0; i < level; i++) {
                cout << path[i];
                if (i < level - 1) cout << " -> ";
            }
            cout << endl;
        } else {
            AdjNode* adj = nodes[current]->adjList;
            while (adj) {
                if (!visited[adj->index])
                    dfsPaths(adj->index, target, visited, path, level);
                adj = adj->next;
            }
        }

        visited[current] = false;
    }

    void resize() {
        int newCapacity = capacity * 2;
        Node** newNodes = new Node*[newCapacity];
        for (int i = 0; i < nodeCount; i++)
            newNodes[i] = nodes[i];
        delete[] nodes;
        nodes = newNodes;
        capacity = newCapacity;
    }

    ~Graph() {
        for (int i = 0; i < nodeCount; i++) {
            AdjNode* adj = nodes[i]->adjList;
            while (adj) {
                AdjNode* temp = adj;
                adj = adj->next;
                delete temp;
            }
            delete nodes[i];
        }
        delete[] nodes;
    }

    void addNode(string name) {
        if (getIndex(name) != -1) {
            cout << "Node already exists.\n";
            return;
        }

        if (nodeCount >= capacity)
            resize();

        nodes[nodeCount++] = new Node(name);
    }

    void addConnection(string origin, string destination, int weight) {
        int i = getIndex(origin);
        int j = getIndex(destination);
        if (i == -1 || j == -1) {
            cout << "One or both points do not exist.\n";
            return;
        }

        AdjNode* adj1 = new AdjNode(j, weight);
        adj1->next = nodes[i]->adjList;
        nodes[i]->adjList = adj1;

        AdjNode* adj2 = new AdjNode(i, weight);
        adj2->next = nodes[j]->adjList;
        nodes[j]->adjList = adj2;
    }

    void checkPathExists(string start, string end) {
        int i = getIndex(start);
        int j = getIndex(end);
        if (i == -1 || j == -1) {
            cout << "Point not found.\n";
            return;
        }

        bool* visited = new bool[nodeCount];
        for (int k = 0; k < nodeCount; k++) visited[k] = false;

        bool found = false;
        dfsExists(i, j, visited, found);
        delete[] visited;

        if (found)
            cout << "There is a path between " << start << " and " << end << ".\n";
        else
            cout << "There is no path between " << start << " and " << end << ".\n";
    }

    void showAllPaths(string start, string end) {
        int i = getIndex(start);
        int j = getIndex(end);
        if (i == -1 || j == -1) {
            cout << "Point not found.\n";
            return;
        }

        bool* visited = new bool[nodeCount];
        string* path = new string[nodeCount];

        for (int k = 0; k < nodeCount; k++) visited[k] = false;

        cout << "All possible paths from " << start << " to " << end << ":\n";
        dfsPaths(i, j, visited, path, 0);

        delete[] visited;
        delete[] path;
    }

    void showAllConnections() {
        cout << "\n====== CURRENT GRAPH ======\n";

        cout << "Nodes:\n";
        for (int i = 0; i < nodeCount; i++) {
            cout << "  [" << i << "] " << nodes[i]->name << "\n";
        }

        cout << "\nAdjacency List (weights):\n";
        for (int i = 0; i < nodeCount; i++) {
            cout << nodes[i]->name.substr(0, 3) << " | ";
            bool hasConnections = false;
            AdjNode* adj = nodes[i]->adjList;
            while (adj) {
                cout << nodes[adj->index]->name.substr(0, 3) << "(" << adj->weight << ") ";
                adj = adj->next;
                hasConnections = true;
            }
            if (!hasConnections)
                cout << ".";
            cout << "\n";
        }

        cout << "\nConnections:\n";
        for (int i = 0; i < nodeCount; i++) {
            cout << nodes[i]->name << " -> ";
            bool hasConnections = false;
            AdjNode* adj = nodes[i]->adjList;
            while (adj) {
                cout << nodes[adj->index]->name << "(" << adj->weight << ") ";
                adj = adj->next;
                hasConnections = true;
            }
            if (!hasConnections) cout << "No connections";
            cout << "\n";
        }

        cout << "===========================\n";
    }
};

int main() {
    Graph city;
    int option;
    string a, b;
    int weight;

    do {
        cout << "\n----- MENU -----\n";
        cout << "1. Add point (node)\n";
        cout << "2. Add connection with weight\n";
        cout << "3. Check if a path exists\n";
        cout << "4. Show all possible paths\n";
        cout << "5. Exit\n";
        cout << "Choose an option: ";
        cin >> option;

        switch (option) {
            case 1:
                cout << "Enter point name: ";
                cin >> a;
                city.addNode(a);
                city.showAllConnections();
                break;
            case 2:
                cout << "Enter origin point: ";
                cin >> a;
                cout << "Enter destination point: ";
                cin >> b;
                cout << "Enter weight: ";
                cin >> weight;
                city.addConnection(a, b, weight);
                city.showAllConnections();
                break;
            case 3:
                cout << "Enter starting point: ";
                cin >> a;
                cout << "Enter destination point: ";
                cin >> b;
                city.checkPathExists(a, b);
                break;
            case 4:
                cout << "Enter starting point: ";
                cin >> a;
                cout << "Enter destination point: ";
                cin >> b;
                city.showAllPaths(a, b);
                break;
            case 5:
                cout << "Exiting...\n";
                break;
            default:
                cout << "Invalid option.\n";
        }

    } while (option != 5);

    return 0;
}
