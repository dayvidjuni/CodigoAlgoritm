#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
using namespace std;

// Clase Nodo para Lista Doblemente Enlazada
class Nodo {
public:
    int id;
    string nombre, correo, carrera;
    int anio;
    Nodo* siguiente;
    Nodo* anterior;
    Nodo(int _id, string _nombre, string _correo, string _carrera, int _anio)
        : id(_id), nombre(_nombre), correo(_correo),
          carrera(_carrera), anio(_anio),
          siguiente(nullptr), anterior(nullptr) {}
};

// Clase ListaDoble
class ListaDoble {
private:
    Nodo* cabeza;
    int idActual;
public:
    ListaDoble() {
        cabeza = nullptr;
        idActual = 1;
        cargarDesdeArchivo();
    }

    void agregar(string nombre, string correo, string carrera, int anio) {
        Nodo* nuevo = new Nodo(idActual++, nombre, correo, carrera, anio);

        if (!cabeza) {
            cabeza = nuevo;
        } else {
            Nodo* actual = cabeza;
            while (actual->siguiente) actual = actual->siguiente;
            actual->siguiente = nuevo;
            nuevo->anterior = actual;
        }
        guardarEnArchivo();
    }

    void mostrar() {
        Nodo* actual = cabeza;
        cout << "\nID\tNombre\t\tCorreo\t\t\tCarrera\t\tAnio\n";
        cout << "--------------------------------------------------------------\n";
        while (actual) {
            cout << actual->id << "\t"
                 << actual->nombre << "\t"
                 << (actual->nombre.length() < 8 ? "\t" : "")
                 << actual->correo << "\t"
                 << (actual->correo.length() < 16 ? "\t" : "")
                 << actual->carrera << "\t"
                 << (actual->carrera.length() < 8 ? "\t" : "")
                 << actual->anio << endl;
            actual = actual->siguiente;
        }
        cout << endl;
    }

    void buscarPorNombre(string nombreBuscar) {
        Nodo* actual = cabeza;
        bool encontrado = false;
        while (actual) {
            if (actual->nombre == nombreBuscar) {
                cout << "\nRegistro encontrado:\n";
                cout << "ID: " << actual->id << ", Nombre: " << actual->nombre
                     << ", Correo: " << actual->correo << " Carrera: " << actual->carrera
                     << ", Anio: " << actual->anio << endl;
                encontrado = true;
                break;
            }
            actual = actual->siguiente;
        }
        if (!encontrado)
            cout << "No se encontro el nombre: " << nombreBuscar << endl;
    }

    void eliminar(int idEliminar) {
        Nodo* actual = cabeza;
        while (actual) {
            if (actual->id == idEliminar) {
                if (actual->anterior) actual->anterior->siguiente = actual->siguiente;
                else cabeza = actual->siguiente;

                if (actual->siguiente) actual->siguiente->anterior = actual->anterior;

                delete actual;
                guardarEnArchivo();
                cout << "Registro eliminado correctamente.\n";
                return;
            }
            actual = actual->siguiente;
        }
        cout << "ID no encontrado.\n";
    }

    void modificar(int idModificar) {
        Nodo* actual = cabeza;
        while (actual) {
            if (actual->id == idModificar) {
                cout << "Registro encontrado. Ingrese los nuevos datos:\n";

                cout << "Nuevo nombre (anterior: " << actual->nombre << "): ";
                getline(cin, actual->nombre);

                cout << "Nuevo correo (anterior: " << actual->correo << "): ";
                getline(cin, actual->correo);

                cout << "Nueva carrera (anterior: " << actual->carrera << "): ";
                getline(cin, actual->carrera);

                cout << "Nuevo anio de ingreso (anterior: " << actual->anio << "): ";
                cin >> actual->anio;
                cin.ignore();

                guardarEnArchivo();
                cout << "Registro modificado correctamente.\n";
                return;
            }
            actual = actual->siguiente;
        }
        cout << "ID no encontrado.\n";
    }

    void guardarEnArchivo() {
        ofstream archivo("registros.txt");
        Nodo* actual = cabeza;
        while (actual) {
            archivo << actual->id << ";" << actual->nombre << ";" << actual->correo
                    << ";" << actual->carrera << ";" << actual->anio << endl;
            actual = actual->siguiente;
        }
        archivo.close();
    }

    void cargarDesdeArchivo() {
        ifstream archivo("registros.txt");
        string linea;
        while (getline(archivo, linea)) {
            stringstream ss(linea);
            string campo;
            int id, anio;
            string nombre, correo, carrera;

            getline(ss, campo, ';'); id = stoi(campo);
            getline(ss, nombre, ';');
            getline(ss, correo, ';');
            getline(ss, carrera, ';');
            getline(ss, campo, ';'); anio = stoi(campo);

            Nodo* nuevo = new Nodo(id, nombre, correo, carrera, anio);
            if (!cabeza) {
                cabeza = nuevo;
            } else {
                Nodo* actual = cabeza;
                while (actual->siguiente) actual = actual->siguiente;
                actual->siguiente = nuevo;
                nuevo->anterior = actual;
            }
            if (id >= idActual) idActual = id + 1;
        }
        archivo.close();
    }

    void recargarDesdeArchivo() {
        Nodo* actual = cabeza;
        while (actual) {
            Nodo* temp = actual;
            actual = actual->siguiente;
            delete temp;
        }
        cabeza = nullptr;
        idActual = 1;
        cargarDesdeArchivo();
        cout << "Registros recargados desde archivo correctamente.\n";
    }
};

// Funcion principal con menu interactivo
int main() {
    ListaDoble lista;
    int opcion;

    while (true) {
        cout << "\n--- SISTEMA DE REGISTRO ACADEMICO ---\n";
        cout << "1. Agregar nuevo estudiante\n";
        cout << "2. Mostrar registros\n";
        cout << "3. Buscar por nombre\n";
        cout << "4. Eliminar por ID\n";
        cout << "5. Modificar por ID\n";
        cout << "6. Cargar registros desde archivo (manual)\n";
        cout << "7. Salir\n";
        cout << "Seleccione una opcion: ";
        cin >> opcion;
        cin.ignore();

        if (opcion == 1) {
            string nombre, correo, carrera;
            int anio;
            cout << "Nombre completo: ";
            getline(cin, nombre);
            cout << "Correo: ";
            getline(cin, correo);
            cout << "Carrera profesional: ";
            getline(cin, carrera);
            cout << "Anio de ingreso: ";
            cin >> anio; cin.ignore();
            lista.agregar(nombre, correo, carrera, anio);
        }
        else if (opcion == 2) {
            lista.mostrar();
        }
        else if (opcion == 3) {
            string nombreBuscar;
            cout << "Nombre a buscar: ";
            getline(cin, nombreBuscar);
            lista.buscarPorNombre(nombreBuscar);
        }
        else if (opcion == 4) {
            int id;
            cout << "ID a eliminar: ";
            cin >> id; cin.ignore();
            lista.eliminar(id);
        }
        else if (opcion == 5) {
            int id;
            cout << "ID a modificar: ";
            cin >> id; cin.ignore();
            lista.modificar(id);
        }
        else if (opcion == 6) {
            lista.recargarDesdeArchivo();
        }
        else if (opcion == 7) {
            cout << "Gracias por usar el sistema.\n";
            break;
        }
        else {
            cout << "Opcion no valida. Intente nuevamente.\n";
        }
    }

    return 0;
}
