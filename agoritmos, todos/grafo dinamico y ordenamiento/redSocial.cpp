#include <QtWidgets/QApplication>
#include <QtWidgets/QMainWindow>
#include <QtWidgets/QWidget>
#include <QtWidgets/QVBoxLayout>
#include <QtWidgets/QHBoxLayout>
#include <QtWidgets/QLabel>
#include <QtWidgets/QLineEdit>
#include <QtWidgets/QPushButton>
#include <QtWidgets/QSlider>
#include <QtWidgets/QMessageBox>
#include <QtGui/QPainter>
#include <QtGui/QPen>
#include <QtGui/QBrush>
#include <QtCore/QTimer>
#include "RedSocialGrafica.moc"
#include <vector>
#include <string>
#include <random>
#include <algorithm>
#include <cmath>
#include <sstream>

struct Point {
    int x, y;
    Point(int x = 0, int y = 0) : x(x), y(y) {}
};

class RedSocialGrafica : public QWidget {
    Q_OBJECT

private:
    std::vector<std::string> usuarios;
    std::vector<Point> posiciones;
    std::vector<std::vector<int>> matrizAdyacencia;
    std::vector<std::vector<int>> matrizPesos;
    std::vector<int> componente;
    std::mt19937 random;
    std::vector<QColor> colores;
    int umbralPeso;

public:
    RedSocialGrafica(QWidget* parent = nullptr) : QWidget(parent), random(std::random_device{}()), umbralPeso(5) {
        setFixedSize(1000, 1000);
        colores.resize(100);
        inicializarGrafo();
        detectarComponentesPorPeso();
        generarPosiciones();
    }

private:
    void inicializarGrafo() {
        for (int i = 1; i <= 30; i++) {
            usuarios.push_back("User" + std::to_string(i));
        }

        int n = usuarios.size();
        matrizAdyacencia.assign(n, std::vector<int>(n, 0));
        matrizPesos.assign(n, std::vector<int>(n, 0));

        for (int i = 0; i < n; i++) {
            int conexiones = 2 + (random() % 4);
            for (int j = 0; j < conexiones; j++) {
                int destino = random() % n;
                if (i != destino) {
                    matrizAdyacencia[i][destino] = 1;
                    matrizAdyacencia[destino][i] = 1;
                    int peso = 1 + (random() % 10);
                    matrizPesos[i][destino] = peso;
                    matrizPesos[destino][i] = peso;
                }
            }
        }
        detectarComponentesPorPeso();
    }

    void detectarComponentesPorPeso() {
        int n = usuarios.size();
        componente.assign(n, -1);
        std::fill(colores.begin(), colores.end(), QColor());
        int componenteId = 0;

        for (int i = 0; i < n; i++) {
            if (componente[i] == -1) {
                dfsPorPeso(i, componenteId);
                colores[componenteId] = QColor(random() % 256, random() % 256, random() % 256);
                componenteId++;
            }
        }
    }

    void dfsPorPeso(int nodo, int id) {
        componente[nodo] = id;
        for (int i = 0; i < usuarios.size(); i++) {
            if (matrizAdyacencia[nodo][i] == 1 && matrizPesos[nodo][i] >= umbralPeso && componente[i] == -1) {
                dfsPorPeso(i, id);
            }
        }
    }

    void generarPosiciones() {
        posiciones.clear();
        int centroX = 500;
        int centroY = 500;
        int radio = 400;
        for (int i = 0; i < usuarios.size(); i++) {
            double angulo = 2 * M_PI * i / usuarios.size();
            int x = (int)(centroX + radio * std::cos(angulo));
            int y = (int)(centroY + radio * std::sin(angulo));
            posiciones.push_back(Point(x, y));
        }
    }

protected:
    void paintEvent(QPaintEvent* event) override {
        QPainter painter(this);
        painter.setRenderHint(QPainter::Antialiasing);

        // Dibujar aristas
        for (int i = 0; i < usuarios.size(); i++) {
            for (int j = i + 1; j < usuarios.size(); j++) {
                if (matrizAdyacencia[i][j] == 1) {
                    Point p1 = posiciones[i];
                    Point p2 = posiciones[j];
                    painter.setPen(QPen(Qt::gray, 1));
                    painter.drawLine(p1.x, p1.y, p2.x, p2.y);
                    
                    int peso = matrizPesos[i][j];
                    int midX = (p1.x + p2.x) / 2;
                    int midY = (p1.y + p2.y) / 2;
                    painter.drawText(midX, midY, QString::number(peso));
                }
            }
        }

        // Dibujar nodos
        for (int i = 0; i < usuarios.size(); i++) {
            Point p = posiciones[i];
            painter.setBrush(QBrush(colores[componente[i] % colores.size()]));
            painter.setPen(QPen(Qt::black, 1));
            painter.drawEllipse(p.x - 15, p.y - 15, 30, 30);
            painter.drawText(p.x - 15, p.y - 20, QString::fromStdString(usuarios[i]));
        }
    }

public slots:
    void mostrarMayorInteraccion(const QString& nombreUsuario) {
        std::string nombre = nombreUsuario.toStdString();
        auto it = std::find(usuarios.begin(), usuarios.end(), nombre);
        if (it == usuarios.end()) {
            QMessageBox::information(this, "Error", "Usuario no encontrado: " + nombreUsuario);
            return;
        }

        int index = std::distance(usuarios.begin(), it);
        int maxPeso = -1;
        std::string usuarioRelacionado = "";
        std::ostringstream detalles;

        for (int j = 0; j < usuarios.size(); j++) {
            if (matrizAdyacencia[index][j] == 1) {
                int peso = matrizPesos[index][j];
                detalles << "Con " << usuarios[j] << " (peso: " << peso << ")\n";
                if (peso > maxPeso) {
                    maxPeso = peso;
                    usuarioRelacionado = usuarios[j];
                }
            }
        }

        if (!usuarioRelacionado.empty()) {
            detalles << "\nMayor interacción: " << usuarioRelacionado << " (peso: " << maxPeso << ")";
            QMessageBox::information(this, QString("Interacciones de %1").arg(nombreUsuario), 
                                   QString::fromStdString(detalles.str()));
        } else {
            QMessageBox::information(this, "Sin conexiones", nombreUsuario + " no tiene conexiones.");
        }
    }

    void actualizarUmbral(int nuevoUmbral) {
        umbralPeso = nuevoUmbral;
        detectarComponentesPorPeso();
        update();
    }
};

class VentanaPrincipal : public QMainWindow {
    Q_OBJECT

private:
    RedSocialGrafica* panel;
    QLineEdit* entradaUsuario;
    QPushButton* botonBuscar;
    QSlider* slider;

public:
    VentanaPrincipal(QWidget* parent = nullptr) : QMainWindow(parent) {
        setWindowTitle("Red Social Interactiva - Clústeres por Peso");
        setFixedSize(1024, 1024);

        QWidget* centralWidget = new QWidget(this);
        setCentralWidget(centralWidget);

        QVBoxLayout* mainLayout = new QVBoxLayout(centralWidget);
        
        panel = new RedSocialGrafica(this);
        mainLayout->addWidget(panel);

        QHBoxLayout* controlLayout = new QHBoxLayout();
        
        controlLayout->addWidget(new QLabel("Usuario:"));
        entradaUsuario = new QLineEdit(this);
        entradaUsuario->setMaximumWidth(100);
        controlLayout->addWidget(entradaUsuario);

        botonBuscar = new QPushButton("Buscar Interacción", this);
        controlLayout->addWidget(botonBuscar);

        controlLayout->addWidget(new QLabel("Umbral de Peso:"));
        slider = new QSlider(Qt::Horizontal, this);
        slider->setRange(1, 10);
        slider->setValue(5);
        slider->setTickPosition(QSlider::TicksBelow);
        slider->setTickInterval(1);
        controlLayout->addWidget(slider);

        mainLayout->addLayout(controlLayout);

        connect(botonBuscar, &QPushButton::clicked, this, &VentanaPrincipal::buscarInteraccion);
        connect(slider, &QSlider::valueChanged, panel, &RedSocialGrafica::actualizarUmbral);
    }

private slots:
    void buscarInteraccion() {
        QString nombre = entradaUsuario->text().trimmed();
        if (!nombre.isEmpty()) {
            panel->mostrarMayorInteraccion(nombre);
        }
    }
};

int main(int argc, char *argv[]) {
    QApplication app(argc, argv);
    
    VentanaPrincipal ventana;
    ventana.show();
    
    return app.exec();
}
