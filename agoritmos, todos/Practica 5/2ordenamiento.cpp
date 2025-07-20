#include <iostream>
#include <vector>
#include <string>
#include <utility>
#include <chrono>
#include <iomanip>
#include <cstdlib>
#include <ctime>

using namespace std;

// Constante de tamaño
const int SIZE = 1000;

// -------------------- ALGORITMOS DE ORDENAMIENTO --------------------

pair<int, int> bubble_sort(vector<int>& arr) {
    int comparisons = 0, swaps = 0;
    int n = arr.size();
    for (int i = 0; i < n - 1; ++i) {
        bool swapped = false;
        for (int j = 0; j < n - i - 1; ++j) {
            comparisons++;
            if (arr[j] > arr[j + 1]) {
                swap(arr[j], arr[j + 1]);
                swaps++;
                swapped = true;
            }
        }
        if (!swapped) break;
    }
    return {comparisons, swaps};
}

pair<int, int> insertion_sort(vector<int>& arr) {
    int comparisons = 0, swaps = 0;
    for (int i = 1; i < arr.size(); ++i) {
        int key = arr[i];
        int j = i - 1;
        while (j >= 0) {
            comparisons++;
            if (arr[j] > key) {
                arr[j + 1] = arr[j];
                swaps++;
                j--;
            } else {
                break;
            }
        }
        arr[j + 1] = key;
        if (j + 1 != i) swaps++;
    }
    return {comparisons, swaps};
}

pair<int, int> merge_sort(vector<int>& arr) {
    int comparisons = 0, swaps = 0;

    function<void(vector<int>&)> merge_sort_helper = [&](vector<int>& vec) {
        if (vec.size() <= 1) return;

        int mid = vec.size() / 2;
        vector<int> L(vec.begin(), vec.begin() + mid);
        vector<int> R(vec.begin() + mid, vec.end());

        merge_sort_helper(L);
        merge_sort_helper(R);

        int i = 0, j = 0, k = 0;
        while (i < L.size() && j < R.size()) {
            comparisons++;
            if (L[i] < R[j]) {
                vec[k++] = L[i++];
                swaps++;
            } else {
                vec[k++] = R[j++];
                swaps++;
            }
        }

        while (i < L.size()) {
            vec[k++] = L[i++];
            swaps++;
        }
        while (j < R.size()) {
            vec[k++] = R[j++];
            swaps++;
        }
    };

    merge_sort_helper(arr);
    return {comparisons, swaps};
}

pair<int, int> quick_sort(vector<int>& arr) {
    int comparisons = 0, swaps = 0;

    function<vector<int>(vector<int>)> quick_sort_helper = [&](vector<int> vec) -> vector<int> {
        if (vec.size() <= 1) return vec;
        int pivot = vec[vec.size() / 2];
        vector<int> left, middle, right;

        for (int x : vec) {
            comparisons++;
            if (x < pivot) {
                left.push_back(x);
                swaps++;
            } else if (x > pivot) {
                right.push_back(x);
                swaps++;
            } else {
                middle.push_back(x);
            }
        }

        vector<int> sorted_left = quick_sort_helper(left);
        vector<int> sorted_right = quick_sort_helper(right);

        vector<int> result;
        result.insert(result.end(), sorted_left.begin(), sorted_left.end());
        result.insert(result.end(), middle.begin(), middle.end());
        result.insert(result.end(), sorted_right.begin(), sorted_right.end());

        return result;
    };

    vector<int> sorted = quick_sort_helper(arr);
    arr = sorted;  // sobrescribimos arr para mantener la interfaz
    return {comparisons, swaps};
}

// -------------------- GENERADORES DE ARREGLOS --------------------

vector<int> generate_random_list() {
    vector<int> vec(SIZE);
    for (int i = 0; i < SIZE; ++i) {
        vec[i] = rand() % 10000;
    }
    return vec;
}

vector<int> generate_sorted_list() {
    vector<int> vec(SIZE);
    for (int i = 0; i < SIZE; ++i) {
        vec[i] = i;
    }
    return vec;
}

vector<int> generate_reverse_list() {
    vector<int> vec(SIZE);
    for (int i = 0; i < SIZE; ++i) {
        vec[i] = SIZE - i - 1;
    }
    return vec;
}

// -------------------- MEDIDOR DE TIEMPO --------------------

void measure_time(
    pair<int, int> (*sort_func)(vector<int>&),
    vector<int> (*arr_generator)(),
    const string& sort_name,
    const string& array_type
) {
    vector<int> arr = arr_generator();
    vector<int> arr_copy = arr;

    auto start = chrono::high_resolution_clock::now();
    pair<int, int> result = sort_func(arr_copy);
    auto end = chrono::high_resolution_clock::now();

    double elapsed_ms = chrono::duration<double, milli>(end - start).count();

    cout << right << setw(14) << sort_name
         << " " << setw(9) << array_type << ": "
         << fixed << setprecision(2) << setw(10) << elapsed_ms << " ms | "
         << "Comparaciones: " << setw(8) << result.first
         << " | Intercambios: " << setw(7) << result.second << endl;
}

// -------------------- PROGRAMA PRINCIPAL --------------------

int main() {
    srand(time(0));

    cout << "\n" << string(90, '=') << endl;
    cout << "COMPARACIÓN DE ALGORITMOS DE ORDENAMIENTO (C++) - TIEMPO, COMPARACIONES E INTERCAMBIOS\n";
    cout << string(90, '=') << endl;

    vector<pair<string, vector<int>(*)()>> test_cases = {
        {"aleatoria", generate_random_list},
        {"ordenada", generate_sorted_list},
        {"inversa", generate_reverse_list}
    };

    vector<pair<string, pair<int, int>(*)(vector<int>&)>> algorithms = {
        {"Bubble Sort", bubble_sort},
        {"Insertion Sort", insertion_sort},
        {"Merge Sort", merge_sort},
        {"Quick Sort", quick_sort}
    };

    for (size_t i = 0; i < test_cases.size(); ++i) {
        string array_type = test_cases[i].first;
        auto generator = test_cases[i].second;

        cout << "\n=== ARREGLO " << array_type << " ===" << endl;

        for (size_t j = 0; j < algorithms.size(); ++j) {
            string name = algorithms[j].first;
            auto algorithm = algorithms[j].second;

            measure_time(algorithm, generator, name, array_type);
        }
    }

    return 0;
}