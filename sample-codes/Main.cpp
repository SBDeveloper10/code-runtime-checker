#include <iostream>
#include <chrono>
#include <iomanip>

using namespace std;

int main() {
    // Record the start time
    auto start_time = chrono::high_resolution_clock::now();

    // Code to measure execution time
    

    // Record the end time
    auto end_time = chrono::high_resolution_clock::now();

    // Calculate the time taken (in milliseconds)
    auto duration = chrono::duration_cast<chrono::milliseconds>(end_time - start_time).count();
    
    // Convert to seconds (float) and print with 2 decimal places
    float execution_time = static_cast<float>(duration) / 1000.0f;

    cout << "executionTime=" << fixed << setprecision(2) << execution_time << endl;

    return 0;
}