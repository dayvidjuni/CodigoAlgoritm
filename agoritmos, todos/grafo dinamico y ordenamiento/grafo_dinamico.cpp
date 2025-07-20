#include <iostream>
#include <vector>
#include <map>
#include <queue>
#include <string>
#include <sstream>
#include <algorithm>
#include <climits>
#include <random>
#include <FL/Fl.H>
#include <FL/Fl_Window.H>
#include <FL/Fl_Button.H>
#include <FL/Fl_Input.H>
#include <FL/Fl_Text_Editor.H>
#include <FL/Fl_Text_Buffer.H>
#include <FL/Fl_Box.H>
#include <FL/fl_draw.H>
#include <FL/Fl_Widget.H>

using namespace std;

struct Nodo {
    string nombre;
    int x, y;
    
    Nodo(const string& n, int x_pos, int y_pos) : nombre(n), x(x_pos), y(y_pos) {}
};

struct Arista {
    Nodo* desde;
    Nodo* hasta;
    int peso;
    
    Arista(Nodo* d, Nodo* h, int p) : desde(d), hasta(h), peso(p) {}
};

struct NodoDistancia {
    Nodo* nodo;
    int distancia;
    
    NodoDistancia(Nodo* n, int d) : nodo(n), distancia(d) {}
    
    bool operator>(const NodoDistancia& other) const {
        return distancia > other.distancia;
    }
};

class GrafoDinamico : public Fl_Widget {
private:
    map<string, unique_ptr<Nodo>> nodos;
    vector<unique_ptr<Arista>> aristas;
    vector<Nodo*> rutaCorta;
    
    Fl_Text_Buffer* entradaBuffer;
    Fl_Text_Editor* entradaTextArea;
    Fl_Input* inicioField;
    Fl_Input* finField;
    Fl_Button* crearGrafoButton;
    Fl_Button* buscarRutaButton;
    Fl_Text_Buffer* resultadoBuffer;
    Fl_Text_Editor* resultadoArea;
    
    random_device rd;
    mt19937 gen;
    
public:
    GrafoDinamico(int x, int y, int w, int h) : Fl_Widget(x, y, w, h), gen(rd()) {
        setupUI();
    }
    
    void setupUI() {
        // Configurar área de entrada
        entradaBuffer = new Fl_Text_Buffer();
        entradaBuffer->text("A B 4\nA C 2\nB D 10\nC D 3\nC E 8\nD E 6");
        
        // Configurar área de resultado
        resultadoBuffer = new Fl_Text_Buffer();
    }
    
    void cargarGrafoDesdeTexto() {
        nodos.clear();
        aristas.clear();
        rutaCorta.clear();
        
        string texto = entradaBuffer->text();
        istringstream iss(texto);
        string linea;
        
        uniform_int_distribution<> randX(100, 600);
        uniform_int_distribution<> randY(100, 400);
        
        while (getline(iss, linea)) {
            if (linea.empty()) continue;
            
            istringstream lineStream(linea);
            string n1, n2;
            int peso;
            
            if (lineStream >> n1 >> n2 >> peso) {
                transform(n1.begin(), n1.end(), n1.begin(), ::toupper);
                transform(n2.begin(), n2.end(), n2.begin(), ::toupper);
                
                if (nodos.find(n1) == nodos.end()) {
                    nodos[n1] = make_unique<Nodo>(n1, randX(gen), randY(gen));
                }
                if (nodos.find(n2) == nodos.end()) {
                    nodos[n2] = make_unique<Nodo>(n2, randX(gen), randY(gen));
                }
                
                aristas.push_back(make_unique<Arista>(nodos[n1].get(), nodos[n2].get(), peso));
                aristas.push_back(make_unique<Arista>(nodos[n2].get(), nodos[n1].get(), peso));
            }
        }
    }
    
    map<Nodo*, int> dijkstra(Nodo* inicio, map<Nodo*, Nodo*>& padres) {
        map<Nodo*, int> distancias;
        priority_queue<NodoDistancia, vector<NodoDistancia>, greater<NodoDistancia>> cola;
        
        distancias[inicio] = 0;
        padres[inicio] = nullptr;
        cola.push(NodoDistancia(inicio, 0));
        
        while (!cola.empty()) {
            NodoDistancia actual = cola.top();
            cola.pop();
            
            Nodo* vActual = actual.nodo;
            int distActual = actual.distancia;
            
            if (distancias.count(vActual) && distancias[vActual] < distActual)
                continue;
            
            for (const auto& a : aristas) {
                if (a->desde == vActual) {
                    int nuevaDist = distActual + a->peso;
                    if (!distancias.count(a->hasta) || nuevaDist < distancias[a->hasta]) {
                        distancias[a->hasta] = nuevaDist;
                        padres[a->hasta] = vActual;
                        cola.push(NodoDistancia(a->hasta, nuevaDist));
                    }
                }
            }
        }
        
        return distancias;
    }
    
    vector<Nodo*> reconstruirRuta(Nodo* destino, const map<Nodo*, Nodo*>& padres) {
        vector<Nodo*> ruta;
        for (Nodo* v = destino; v != nullptr; v = padres.count(v) ? padres.at(v) : nullptr) {
            ruta.push_back(v);
        }
        reverse(ruta.begin(), ruta.end());
        return ruta;
    }
    
    void buscarRuta() {
        string inicioTexto = inicioField->value();
        string finTexto = finField->value();
        
        transform(inicioTexto.begin(), inicioTexto.end(), inicioTexto.begin(), ::toupper);
        transform(finTexto.begin(), finTexto.end(), finTexto.begin(), ::toupper);
        
        if (nodos.find(inicioTexto) == nodos.end() || nodos.find(finTexto) == nodos.end()) {
            resultadoBuffer->text("Nodos inválidos");
            return;
        }
        
        Nodo* startNode = nodos[inicioTexto].get();
        Nodo* endNode = nodos[finTexto].get();
        
        map<Nodo*, Nodo*> padres;
        auto distancias = dijkstra(startNode, padres);
        
        if (distancias.find(endNode) == distancias.end()) {
            resultadoBuffer->text("No hay camino");
            rutaCorta.clear();
        } else {
            int distanciaTotal = distancias[endNode];
            rutaCorta = reconstruirRuta(endNode, padres);
            
            string resultado = "Ruta más corta: ";
            for (const auto& n : rutaCorta) {
                resultado += n->nombre + " ";
            }
            resultado += "\nDistancia: " + to_string(distanciaTotal);
            resultadoBuffer->text(resultado.c_str());
        }
        
        redraw();
    }
    
    void draw() override {
        fl_rectf(x(), y(), w(), h(), FL_WHITE);
        
        // Dibujar aristas
        fl_color(FL_GRAY);
        fl_line_style(FL_SOLID, 1);
        
        for (const auto& a : aristas) {
            fl_line(a->desde->x, a->desde->y, a->hasta->x, a->hasta->y);
            
            int xm = (a->desde->x + a->hasta->x) / 2;
            int ym = (a->desde->y + a->hasta->y) / 2;
            
            fl_color(FL_BLACK);
            fl_draw(to_string(a->peso).c_str(), xm, ym);
            fl_color(FL_GRAY);
        }
        
        // Dibujar ruta más corta
        if (rutaCorta.size() > 1) {
            fl_color(FL_RED);
            fl_line_style(FL_SOLID, 3);
            
            for (size_t i = 0; i < rutaCorta.size() - 1; i++) {
                Nodo* n1 = rutaCorta[i];
                Nodo* n2 = rutaCorta[i + 1];
                fl_line(n1->x, n1->y, n2->x, n2->y);
            }
        }
        
        // Dibujar nodos
        for (const auto& pair : nodos) {
            Nodo* n = pair.second.get();
            
            fl_color(fl_rgb_color(102, 204, 255));
            fl_pie(n->x - 15, n->y - 15, 30, 30, 0, 360);
            
            fl_color(FL_BLACK);
            fl_circle(n->x - 15, n->y - 15, 30);
            fl_draw(n->nombre.c_str(), n->x - 5, n->y + 5);
        }
        
        fl_line_style(FL_SOLID, 1);
    }
    
    void setEntradaBuffer(Fl_Text_Buffer* buffer) { entradaBuffer = buffer; }
    void setResultadoBuffer(Fl_Text_Buffer* buffer) { resultadoBuffer = buffer; }
    void setInicioField(Fl_Input* field) { inicioField = field; }
    void setFinField(Fl_Input* field) { finField = field; }
};

// Funciones callback
void crear_grafo_callback(Fl_Widget* widget, void* data) {
    GrafoDinamico* grafo = static_cast<GrafoDinamico*>(data);
    grafo->cargarGrafoDesdeTexto();
    grafo->redraw();
}

void buscar_ruta_callback(Fl_Widget* widget, void* data) {
    GrafoDinamico* grafo = static_cast<GrafoDinamico*>(data);
    grafo->buscarRuta();
}

int main() {
    Fl_Window window(800, 600, "Grafo Transporte - Entrada Manual");
    
    // Área de entrada
    Fl_Text_Buffer* entradaBuffer = new Fl_Text_Buffer();
    entradaBuffer->text("A B 4\nA C 2\nB D 10\nC D 3\nC E 8\nD E 6");
    
    Fl_Text_Editor* entradaArea = new Fl_Text_Editor(10, 30, 500, 100);
    entradaArea->buffer(entradaBuffer);
    
    Fl_Button* crearButton = new Fl_Button(520, 30, 100, 30, "Crear Grafo");
    
    // Campos de entrada
    Fl_Input* inicioField = new Fl_Input(70, 140, 50, 25, "Inicio:");
    Fl_Input* finField = new Fl_Input(180, 140, 50, 25, "Fin:");
    Fl_Button* buscarButton = new Fl_Button(240, 140, 100, 25, "Buscar Ruta");
    
    // Área de resultado
    Fl_Text_Buffer* resultadoBuffer = new Fl_Text_Buffer();
    Fl_Text_Editor* resultadoArea = new Fl_Text_Editor(10, 170, 500, 60);
    resultadoArea->buffer(resultadoBuffer);
    
    // Área de dibujo
    GrafoDinamico* grafoPanel = new GrafoDinamico(10, 240, 780, 350);
    grafoPanel->setEntradaBuffer(entradaBuffer);
    grafoPanel->setResultadoBuffer(resultadoBuffer);
    grafoPanel->setInicioField(inicioField);
    grafoPanel->setFinField(finField);
    
    // Configurar callbacks
    crearButton->callback(crear_grafo_callback, grafoPanel);
    buscarButton->callback(buscar_ruta_callback, grafoPanel);
    
    window.end();
    window.show();
    
    return Fl::run();
}