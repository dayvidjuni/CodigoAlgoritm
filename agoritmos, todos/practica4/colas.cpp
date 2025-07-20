#include <iostream>
#include <fstream>
#include <sstream>
using namespace std;

class Nodo {
public:
    int id;
    string nombre, correo, carrera;
    int anio;
    Nodo* siguiente;

    Nodo(int _id, string _nombre, string _correo, string _carrera, int _anio)
        : id(_id), nombre(_nombre), correo(_correo),
          carrera(_carrera), anio(_anio), siguiente(nullptr) {}
};

class ColaEstudiantes {
private:
    Nodo* frente;
    Nodo* final;
    int idActual;

public:
    ColaEstudiantes() {
        frente = final = nullptr;
        idActual = 1;
        cargarDesdeArchivo();
    }

    void agregar(string nombre, string correo, string carrera, int anio) {
        Nodo* nuevo = new Nodo(idActual++, nombre, correo, carrera, anio);
        if (!frente) {
            frente = final = nuevo;
        } else {
            final->siguiente = nuevo;
            final = nuevo;
        }
        guardarEnArchivo();
    }

    void mostrar() {
        Nodo* actual = frente;
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
        Nodo* actual = frente;
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

    void eliminar() {
        if (!frente) {
            cout << "Cola vacia\n";
            return;
        }
        Nodo* temp = frente;
        frente = frente->siguiente;
        delete temp;

        if (!frente) final = nullptr;

        guardarEnArchivo();
        cout << "Primer registro eliminado correctamente.\n";
    }

    void guardarEnArchivo() {
        ofstream archivo("registros.txt");
        Nodo* actual = frente;
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
            if (!frente) {
                frente = final = nuevo;
            } else {
                final->siguiente = nuevo;
                final = nuevo;
            }
            if (id >= idActual) idActual = id + 1;
        }
        archivo.close();
    }

    void recargarDesdeArchivo() {
        Nodo* actual = frente;
        while (actual) {
            Nodo* temp = actual;
            actual = actual->siguiente;
            delete temp;
        }
        frente = final = nullptr;
        idActual = 1;
        cargarDesdeArchivo();
        cout << "Registros recargados desde archivo correctamente.\n";
    }
};

int main() {
    ColaEstudiantes cola;
    int opcion;
    while (true) {
        cout << "\n--- SISTEMA DE REGISTRO ACADEMICO ---\n";
        cout << "1. Agregar nuevo estudiante\n";
        cout << "2. Mostrar registros\n";
        cout << "3. Buscar por nombre\n";
        cout << "4. Eliminar primer registro\n";
        cout << "5. Salir\n";
        cout << "6. Cargar registros desde archivo (manual)\n";
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
            cout << "Aioo de ingreso: ";
            cin >> anio; cin.ignore();
            cola.agregar(nombre, correo, carrera, anio);
        }
        else if (opcion == 2) {
            cola.mostrar();
        }
        else if (opcion == 3) {
            string nombreBuscar;
            cout << "Nombre a buscar: ";
            getline(cin, nombreBuscar);
            cola.buscarPorNombre(nombreBuscar);
        }
        else if (opcion == 4) {
            cola.eliminar();
        }
        else if (opcion == 5) {
            cout << "buen uso\n";
            break;
        }
        else if (opcion == 6) {
            cola.recargarDesdeArchivo();
        }
        else {
            cout << "Opcion no valida\n";
        }
    }
    return 0;
}
