#include <iostream>
#include <vector>
#include <algorithm>
#include <chrono>
#include <cstdlib>
#include <iomanip>

using namespace std;
using namespace std::chrono;

const int SIZE = 1000;

pair<int, int> bubble_sort(vector<int> arr) {
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

pair<int, int> insertion_sort(vector<int> arr) {
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

void merge_sort_helper(vector<int>& arr, int& comparisons, int& swaps) {
    if (arr.size() > 1) {
        int mid = arr.size() / 2;
        vector<int> L(arr.begin(), arr.begin() + mid);
        vector<int> R(arr.begin() + mid, arr.end());

        merge_sort_helper(L, comparisons, swaps);
        merge_sort_helper(R, comparisons, swaps);

        int i = 0, j = 0, k = 0;
        while (i < L.size() && j < R.size()) {
            comparisons++;
            if (L[i] < R[j]) {
                arr[k++] = L[i++];
                swaps++;
            } else {
                arr[k++] = R[j++];
                swaps++;
            }
        }

        while (i < L.size()) {
            arr[k++] = L[i++];
            swaps++;
        }

        while (j < R.size()) {
            arr[k++] = R[j++];
            swaps++;
        }
    }
}

pair<int, int> merge_sort(vector<int> arr) {
    int comparisons = 0, swaps = 0;
    merge_sort_helper(arr, comparisons, swaps);
    return {comparisons, swaps};
}

vector<int> quick_sort_helper(vector<int> arr, int& comparisons, int& swaps) {
    if (arr.size() <= 1) return arr;

    int pivot = arr[arr.size() / 2];
    vector<int> left, middle, right;

    for (int x : arr) {
        comparisons++;
        if (x < pivot) left.push_back(x);
        else if (x == pivot) middle.push_back(x);
        else right.push_back(x);
    }

    swaps += left.size() + right.size();
    vector<int> sorted_left = quick_sort_helper(left, comparisons, swaps);
    vector<int> sorted_right = quick_sort_helper(right, comparisons, swaps);

    vector<int> result;
    result.insert(result.end(), sorted_left.begin(), sorted_left.end());
    result.insert(result.end(), middle.begin(), middle.end());
    result.insert(result.end(), sorted_right.begin(), sorted_right.end());

    return result;
}

pair<int, int> quick_sort(vector<int> arr) {
    int comparisons = 0, swaps = 0;
    quick_sort_helper(arr, comparisons, swaps);
    return {comparisons, swaps};
}

vector<int> generate_random_list() {
    vector<int> v(SIZE);
    for (int& x : v) x = rand() % 10000;
    return v;
}

vector<int> generate_sorted_list() {
    vector<int> v(SIZE);
    for (int i = 0; i < SIZE; ++i) v[i] = i;
    return v;
}

vector<int> generate_reverse_list() {
    vector<int> v(SIZE);
    for (int i = 0; i < SIZE; ++i) v[i] = SIZE - 1 - i;
    return v;
}

void measure_time(pair<int, int> (*sort_func)(vector<int>), vector<int> (*arr_generator)(), string sort_name, string array_type) {
    vector<int> arr = arr_generator();
    auto start = high_resolution_clock::now();
    pair<int, int> result = sort_func(arr);
    auto end = high_resolution_clock::now();
    auto duration = duration_cast<milliseconds>(end - start).count();
    
    cout.width(14); cout << right << sort_name;
    cout.width(9); cout << right << array_type << ": ";
    cout.width(10); cout << right << duration << " ms | ";
    cout << "Comparaciones: ";
    cout.width(8); cout << result.first << " | Intercambios: ";
    cout.width(7); cout << result.second << endl;
}

int main() {
    srand(time(nullptr));

    cout << "\n" << string(90, '=') << endl;
    cout << "COMPARACIÓN DE ALGORITMOS DE ORDENAMIENTO\n";
    cout << string(90, '=') << endl;

    vector<pair<string, vector<int>(*)()>> test_cases = {
        {"aleatoria", generate_random_list},
        {"ordenada", generate_sorted_list},
        {"inversa", generate_reverse_list}
    };

    vector<pair<string, pair<int, int> (*)(vector<int>)>> algorithms = {
        {"Bubble Sort", bubble_sort},
        {"Insertion Sort", insertion_sort},
        {"Merge Sort", merge_sort},
        {"Quick Sort", quick_sort}
    };

    for (const auto& test_case : test_cases) {
        string array_type = test_case.first;
        auto generator = test_case.second;
    
        cout << "\n=== ARREGLO " << array_type << " ===" << endl;
    
        for (const auto& algorithm : algorithms) {
            string name = algorithm.first;
            auto func = algorithm.second;
    
            measure_time(func, generator, name, array_type);
        }
    }
    

    system("pause");
    return 0;
}
