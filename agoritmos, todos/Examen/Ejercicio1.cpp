#include <iostream>
#include <iomanip>
using namespace std;

class Patient {
public:
    string name;
    string dni;
    int emergencyLevel;
    int estimatedTime;

    Patient(string n, string d, int e, int t) {
        name = n;
        dni = d;
        emergencyLevel = e;
        estimatedTime = t;
    }
};

class Node {
public:
    Patient* patient;
    Node* next;

    Node(Patient* p) {
        patient = p;
        next = nullptr;
    }
};

class PriorityQueue {
private:
    Node* head;
    int totalServed;
    int totalTime;

public:
    PriorityQueue() {
        head = nullptr;
        totalServed = 0;
        totalTime = 0;
    }

    void insertPatient(string name, string dni, int level, int time) {
        Patient* newPatient = new Patient(name, dni, level, time);
        Node* newNode = new Node(newPatient);

        if (!head || level < head->patient->emergencyLevel) {
            newNode->next = head;
            head = newNode;
            return;
        }

        Node* current = head;
        while (current->next && current->next->patient->emergencyLevel <= level) {
            current = current->next;
        }

        newNode->next = current->next;
        current->next = newNode;
    }

    void servePatient() {
        if (!head) {
            cout << "\nNo patients to serve.\n";
            return;
        }

        Node* served = head;
        head = head->next;

        cout << "\nServing: " << served->patient->name << " (DNI: " << served->patient->dni << ")\n";
        cout << "Emergency level: " << served->patient->emergencyLevel << "\n";
        cout << "Estimated time: " << served->patient->estimatedTime << " minutes\n";

        totalServed++;
        totalTime += served->patient->estimatedTime;

        delete served->patient;
        delete served;
    }

    void showPendingPatients() {
        if (!head) {
            cout << "\nPending patients: None\n";
            return;
        }

        cout << "\nPENDING PATIENTS (From highest to lowest priority):\n";

        Node* current = head;
        while (current) {
            cout << "+-------------------------------------------------------------+\n";
            cout << "| Name: " << setw(12) << left << current->patient->name
                 << "| DNI: " << setw(6) << left << current->patient->dni
                 << "| Emergency: " << setw(2) << left << current->patient->emergencyLevel
                 << "| Time: " << setw(3) << left << current->patient->estimatedTime << " min |\n";
            cout << "+-------------------------------------------------------------+\n";
            if (current->next) {
                cout << "                       ↓\n";
            }
            current = current->next;
        }
    }

    void showStatistics() {
        cout << "\nTotal patients served: " << totalServed << endl;
        cout << "Total attention time: " << totalTime << " minutes\n";
    }

    void displaySystemState() {
        showPendingPatients();
        showStatistics();
    }
};

int main() {
    PriorityQueue system;
    int option;

    do {
        cout << "\n=== HOSPITAL EMERGENCY SYSTEM ===\n";
        system.displaySystemState();

        cout << "\n1. Register new patient\n";
        cout << "2. Serve next patient\n";
        cout << "3. Exit\n";
        cout << "Choose an option: ";
        cin >> option;
        cin.ignore();

        if (option == 1) {
            string name, dni;
            int level, time;
            cout << "Patient name: ";
            getline(cin, name);
            cout << "DNI: ";
            getline(cin, dni);
            cout << "Emergency level (1 = most critical to 5): ";
            cin >> level;
            cout << "Estimated attention time (minutes): ";
            cin >> time;
            cin.ignore();
            system.insertPatient(name, dni, level, time);
        } else if (option == 2) {
            system.servePatient();
        }

    } while (option != 3);

    return 0;
}