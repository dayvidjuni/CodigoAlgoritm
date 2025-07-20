#include <iostream>
using namespace std;

const int SIZE = 10;
const int MAX_ACTIONS = 10;

class Action {
public:
    string type;
    int x1, y1;
    int x2, y2;
    char prevChar;
    char newChar;

    Action() {}

    Action(string t, int x, int y, char pc, char nc)
        : type(t), x1(x), y1(y), prevChar(pc), newChar(nc), x2(-1), y2(-1) {}

    // Overload for move
    Action(string t, int x1_, int y1_, int x2_, int y2_, char pc)
        : type(t), x1(x1_), y1(y1_), x2(x2_), y2(y2_), prevChar(pc) {}
};

class Stack {
private:
    Action actions[MAX_ACTIONS];
    int top;

public:
    Stack() {
        top = -1;
    }

    bool isEmpty() {
        return top == -1;
    }

    bool isFull() {
        return top == MAX_ACTIONS - 1;
    }

    void push(Action a) {
        if (isFull()) {
            // Shift left to make space
            for (int i = 1; i <= top; i++) {
                actions[i - 1] = actions[i];
            }
            actions[top] = a;
        } else {
            actions[++top] = a;
        }
    }

    Action pop() {
        if (!isEmpty()) {
            return actions[top--];
        } else {
            return Action();
        }
    }

    void clear() {
        top = -1;
    }
};

class Canvas {
private:
    char grid[SIZE][SIZE];
    Stack undoStack;
    Stack redoStack;

public:
    Canvas() {
        for (int i = 0; i < SIZE; i++)
            for (int j = 0; j < SIZE; j++)
                grid[i][j] = '.';
    }

    void draw(int x, int y, char c) {
        if (isValid(x, y)) {
            char prev = grid[y][x];
            grid[y][x] = c;
            undoStack.push(Action("draw", x, y, prev, c));
            redoStack.clear();
            cout << "Drew '" << c << "' at (" << x << "," << y << ")\n";
        }
    }

    void move(int x1, int y1, int x2, int y2) {
        if (isValid(x1, y1) && isValid(x2, y2)) {
            char ch = grid[y1][x1];
            if (ch != '.') {
                grid[y2][x2] = ch;
                grid[y1][x1] = '.';
                undoStack.push(Action("move", x1, y1, x2, y2, ch));
                redoStack.clear();
                cout << "Moved '" << ch << "' from (" << x1 << "," << y1 << ") to (" << x2 << "," << y2 << ")\n";
            } else {
                cout << "No character to move at source.\n";
            }
        }
    }

    void erase(int x, int y) {
        if (isValid(x, y)) {
            char prev = grid[y][x];
            if (prev != '.') {
                grid[y][x] = '.';
                undoStack.push(Action("erase", x, y, prev, '.'));
                redoStack.clear();
                cout << "Erased character at (" << x << "," << y << ")\n";
            } else {
                cout << "Nothing to erase.\n";
            }
        }
    }

    void undo() {
        if (undoStack.isEmpty()) {
            cout << "Nothing to undo.\n";
            return;
        }

        Action a = undoStack.pop();
        if (a.type == "draw" || a.type == "erase") {
            grid[a.y1][a.x1] = a.prevChar;
        } else if (a.type == "move") {
            grid[a.y1][a.x1] = a.prevChar;
            grid[a.y2][a.x2] = '.';
        }
        redoStack.push(a);
        cout << "Undid action: " << a.type << endl;
    }

    void redo() {
        if (redoStack.isEmpty()) {
            cout << "Nothing to redo.\n";
            return;
        }

        Action a = redoStack.pop();
        if (a.type == "draw" || a.type == "erase") {
            grid[a.y1][a.x1] = a.newChar;
        } else if (a.type == "move") {
            grid[a.y2][a.x2] = a.prevChar;
            grid[a.y1][a.x1] = '.';
        }
        undoStack.push(a);
        cout << "Redid action: " << a.type << endl;
    }

    void display() {
        cout << "\nCanvas:\n";
        for (int i = 0; i < SIZE; i++) {
            for (int j = 0; j < SIZE; j++) {
                cout << grid[i][j] << " ";
            }
            cout << endl;
        }
    }

    bool isValid(int x, int y) {
        return x >= 0 && x < SIZE && y >= 0 && y < SIZE;
    }
};

int main() {
    Canvas paintApp;
    int choice;
    int x, y, x2, y2;
    char ch;

    do {
        cout << "\n=== Paint Menu ===\n";
        cout << "[1] Draw\n";
        cout << "[2] Move\n";
        cout << "[3] Erase\n";
        cout << "[4] Undo\n";
        cout << "[5] Redo\n";
        cout << "[6] Show Canvas\n";
        cout << "[0] Exit\n";
        cout << "Choice: ";
        cin >> choice;

        switch (choice) {
            case 1:
                cout << "Enter x y and character: ";
                cin >> x >> y >> ch;
                paintApp.draw(x, y, ch);
                break;
            case 2:
                cout << "Enter x1 y1 (from) and x2 y2 (to): ";
                cin >> x >> y >> x2 >> y2;
                paintApp.move(x, y, x2, y2);
                break;
            case 3:
                cout << "Enter x y to erase: ";
                cin >> x >> y;
                paintApp.erase(x, y);
                break;
            case 4:
                paintApp.undo();
                break;
            case 5:
                paintApp.redo();
                break;
            case 6:
                paintApp.display();
                break;
            case 0:
                cout << "Exiting.\n";
                break;
            default:
                cout << "Invalid option.\n";
        }

    } while (choice != 0);

    return 0;
}
