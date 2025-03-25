#include <stdio.h>
#include <time.h>

int main() {
    // Start time measurement
    clock_t start_time = clock();

    // Code to measure execution time
    

    // End time measurement
    clock_t end_time = clock();

    // Calculate time taken (in milliseconds)
    double time_taken = ((double)(end_time - start_time)) / CLOCKS_PER_SEC * 1000;

    printf("executionTime=%.2f", time_taken);

    return 0;
}
