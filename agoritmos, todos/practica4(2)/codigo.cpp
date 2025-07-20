#include <windows.h> 
#include <fstream> 
#include <sstream> 
#include <string> 
#include <vector> 
using namespace std; 

// Estructura para registro 
struct Estudiante { 
    string nombre; 
    string correo; 
    string carrera; 
    int anio; 
}; 

vector<Estudiante> lista; 

// Controles 
HWND hNombre, hCorreo, hCarrera, hAnio, hLista; 

// Función para agregar registro 
void AgregarEstudiante(HWND hwnd) { 
    char nombre[100], correo[100], carrera[100], anioStr[10]; 
    GetWindowText(hNombre, nombre, 100); 
    GetWindowText(hCorreo, correo, 100); 
    GetWindowText(hCarrera, carrera, 100); 
    GetWindowText(hAnio, anioStr, 10); 
    
    int anio = atoi(anioStr); 
    Estudiante e = {nombre, correo, carrera, anio}; 
    lista.push_back(e); 
    
    SendMessage(hLista, LB_ADDSTRING, 0, (LPARAM)(string(nombre) + " - " + correo).c_str()); 
    
    SetWindowText(hNombre, ""); 
    SetWindowText(hCorreo, ""); 
    SetWindowText(hCarrera, ""); 
    SetWindowText(hAnio, ""); 
} 

// Guardar en archivo 
void GuardarArchivo() { 
    ofstream file("registros.txt"); 
    for (auto& e : lista) { 
        file << e.nombre << ";" << e.correo << ";" << e.carrera << ";" << e.anio << "\n"; 
    } 
    file.close(); 
} 

// Cargar desde archivo 
void CargarArchivo(HWND hwnd) { 
    lista.clear(); 
    SendMessage(hLista, LB_RESETCONTENT, 0, 0); 
    
    ifstream file("registros.txt"); 
    string linea; 
    while (getline(file, linea)) { 
        stringstream ss(linea); 
        string nombre, correo, carrera, anioStr; 
        
        getline(ss, nombre, ';'); 
        getline(ss, correo, ';'); 
        getline(ss, carrera, ';'); 
        getline(ss, anioStr, ';'); 
        
        int anio = stoi(anioStr); 
        Estudiante e = {nombre, correo, carrera, anio}; 
        lista.push_back(e); 
        
        SendMessage(hLista, LB_ADDSTRING, 0, (LPARAM)(nombre + " - " + correo).c_str()); 
    } 
    file.close(); 
} 

// Procesamiento de mensajes 
LRESULT CALLBACK WindowProcedure(HWND hwnd, UINT msg, WPARAM wp, LPARAM lp) { 
    switch (msg) { 
        case WM_COMMAND: 
            switch (wp) { 
                case 1: AgregarEstudiante(hwnd); break; 
                case 2: GuardarArchivo(); break; 
                case 3: CargarArchivo(hwnd); break; 
            } 
            break; 
        case WM_DESTROY: 
            PostQuitMessage(0); 
            break; 
        default: 
            return DefWindowProc(hwnd, msg, wp, lp); 
    } 
    return 0; 
} 

// Crear controles 
void CrearControles(HWND hwnd) { 
    CreateWindow("STATIC", "Nombre:", WS_VISIBLE | WS_CHILD, 20, 20, 80, 20, hwnd, NULL, NULL, NULL); 
    hNombre = CreateWindow("EDIT", "", WS_VISIBLE | WS_CHILD | WS_BORDER, 100, 20, 200, 20, hwnd, NULL, NULL, NULL); 
    
    CreateWindow("STATIC", "Correo:", WS_VISIBLE | WS_CHILD, 20, 50, 80, 20, hwnd, NULL, NULL, NULL); 
    hCorreo = CreateWindow("EDIT", "", WS_VISIBLE | WS_CHILD | WS_BORDER, 100, 50, 200, 20, hwnd, NULL, NULL, NULL); 
    
    CreateWindow("STATIC", "Carrera:", WS_VISIBLE | WS_CHILD, 20, 80, 80, 20, hwnd, NULL, NULL, NULL); 
    hCarrera = CreateWindow("EDIT", "", WS_VISIBLE | WS_CHILD | WS_BORDER, 100, 80, 200, 20, hwnd, NULL, NULL, NULL); 
    
    CreateWindow("STATIC", "Anio:", WS_VISIBLE | WS_CHILD, 20, 110, 80, 20, hwnd, NULL, NULL, NULL); 
    hAnio = CreateWindow("EDIT", "", WS_VISIBLE | WS_CHILD | WS_BORDER, 100, 110, 100, 20, hwnd, NULL, NULL, NULL); 
    
    CreateWindow("BUTTON", "Agregar", WS_VISIBLE | WS_CHILD, 320, 20, 100, 30, hwnd, (HMENU)1, NULL, NULL); 
    CreateWindow("BUTTON", "Guardar", WS_VISIBLE | WS_CHILD, 320, 60, 100, 30, hwnd, (HMENU)2, NULL, NULL); 
    CreateWindow("BUTTON", "Cargar", WS_VISIBLE | WS_CHILD, 320, 100, 100, 30, hwnd, (HMENU)3, NULL, NULL); 
    
    hLista = CreateWindow("LISTBOX", NULL, WS_VISIBLE | WS_CHILD | WS_BORDER | LBS_NOTIFY, 
                        20, 150, 400, 200, hwnd, NULL, NULL, NULL); 
} 

// Función principal WinAPI 
int WINAPI WinMain(HINSTANCE hInst, HINSTANCE hPrev, LPSTR args, int nCmdShow) { 
    WNDCLASS wc = {0}; 
    wc.hbrBackground = (HBRUSH)COLOR_WINDOW; 
    wc.hCursor = LoadCursor(NULL, IDC_ARROW); 
    wc.hInstance = hInst; 
    wc.lpszClassName = "RegistroWin"; 
    wc.lpfnWndProc = WindowProcedure; 
    
    if (!RegisterClass(&wc)) return -1; 
    
    HWND hwnd = CreateWindow("RegistroWin", "Sistema de Registro Académico", 
                            WS_OVERLAPPEDWINDOW | WS_VISIBLE, 
                            100, 100, 470, 420, NULL, NULL, NULL, NULL); 
    CrearControles(hwnd); 
    
    MSG msg = {0}; 
    while (GetMessage(&msg, NULL, 0, 0)) { 
        TranslateMessage(&msg); 
        DispatchMessage(&msg); 
    } 
    return 0; 
}