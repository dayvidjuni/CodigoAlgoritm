#include <iostream>
using namespace std;

class Graph {
private:
    string* names;
    int** adjacencyMatrix;
    int capacity;
    int nodeCount;

public:
    Graph() {
        capacity = 5;
        nodeCount = 0;
        names = new string[capacity];
        adjacencyMatrix = new int*[capacity];
        for (int i = 0; i < capacity; i++) {
            adjacencyMatrix[i] = new int[capacity];
            for (int j = 0; j < capacity; j++)
                adjacencyMatrix[i][j] = 0;
        }
    }
    int getIndex(string name) {
        for (int i = 0; i < nodeCount; i++) {
            if (names[i] == name)
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

        for (int i = 0; i < nodeCount; i++) {
            if (adjacencyMatrix[current][i] > 0 && !visited[i]) {
                dfsExists(i, target, visited, found);
            }
        }
    }

    void dfsPaths(int current, int target, bool* visited, string* path, int level) {
        visited[current] = true;
        path[level] = names[current];
        level++;

        if (current == target) {
            for (int i = 0; i < level; i++) {
                cout << path[i];
                if (i < level - 1) cout << " -> ";
            }
            cout << endl;
        } else {
            for (int i = 0; i < nodeCount; i++) {
                if (adjacencyMatrix[current][i] > 0 && !visited[i]) {
                    dfsPaths(i, target, visited, path, level);
                }
            }
        }

        visited[current] = false;
    }

    void resize() {
        int newCapacity = capacity * 2;

        // Resize names array
        string* newNames = new string[newCapacity];
        for (int i = 0; i < nodeCount; i++)
            newNames[i] = names[i];
        delete[] names;
        names = newNames;

        // Resize matrix
        int** newMatrix = new int*[newCapacity];
        for (int i = 0; i < newCapacity; i++) {
            newMatrix[i] = new int[newCapacity];
            for (int j = 0; j < newCapacity; j++)
                newMatrix[i][j] = 0;
        }

        for (int i = 0; i < nodeCount; i++)
            for (int j = 0; j < nodeCount; j++)
                newMatrix[i][j] = adjacencyMatrix[i][j];

        for (int i = 0; i < capacity; i++)
            delete[] adjacencyMatrix[i];
        delete[] adjacencyMatrix;

        adjacencyMatrix = newMatrix;
        capacity = newCapacity;
    }

    ~Graph() {
        for (int i = 0; i < capacity; i++)
            delete[] adjacencyMatrix[i];
        delete[] adjacencyMatrix;
        delete[] names;
    }

    void addNode(string name) {
        if (getIndex(name) != -1) {
            cout << "Node already exists.\n";
            return;
        }

        if (nodeCount >= capacity)
            resize();

        names[nodeCount++] = name;
    }

    void addConnection(string origin, string destination, int weight) {
        int i = getIndex(origin);
        int j = getIndex(destination);
        if (i == -1 || j == -1) {
            cout << "One or both points do not exist.\n";
            return;
        }

        adjacencyMatrix[i][j] = weight;
        adjacencyMatrix[j][i] = weight; // undirected graph
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
        cout << "  [" << i << "] " << names[i] << "\n";
    }

    cout << "\nAdjacency Matrix (weights):\n    ";

    for (int i = 0; i < nodeCount; i++)
        cout << names[i].substr(0, 3) << "\t";
    cout << "\n";

    cout << "   ";
    for (int i = 0; i < nodeCount; i++)
        cout << "----\t";
    cout << "\n";

    for (int i = 0; i < nodeCount; i++) {
        cout << names[i].substr(0, 3) << " | ";
        for (int j = 0; j < nodeCount; j++) {
            if (adjacencyMatrix[i][j] > 0)
                cout << adjacencyMatrix[i][j] << "\t";
            else
                cout << ".\t"; 
        }
        cout << "\n";
    }

    cout << "\nConnections:\n";
    for (int i = 0; i < nodeCount; i++) {
        cout << names[i] << " -> ";
        bool hasConnections = false;
        for (int j = 0; j < nodeCount; j++) {
            if (adjacencyMatrix[i][j] > 0) {
                cout << names[j] << "(" << adjacencyMatrix[i][j] << ") ";
                hasConnections = true;
            }
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
