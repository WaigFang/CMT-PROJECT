#include <math.h>
#include <stdio.h>
#include <stdlib.h>

double prey_growth_rate(double a,double b,double x,double y){ //dx/dt 
    return a*x - b*x*y;
}

double predator_growth_rate(double d, double g, double x, double y){ // dy/dt
    return d*x*y - g*y;
}

// Prey growth with carrying capacity (logistic growth)
double prey_growth_rate_2(double a, double b, double x, double y, double K) { // dx/dt
    return a * x * (1 - x / K) - b * x * y;
}

// Predator growth with a functional response (Holling's type II)
double predator_growth_rate_2(double d, double g, double x, double y, double h) { // dy/dt
    return d * (x * y) / (h + x) - g * y;
}
//not using this for the moment


// Lotka-Volterra simulation
void simulate_lotka_volterra(double a, double b, double d, double g, double x0, double y0, double t_max, double dt, const char *filename1, const char *filename2) {
    FILE *file1 = fopen(filename1, "w");
    if (!file1) {
        perror("Error opening first file");
        return;
    }
    fprintf(file1, "Time,Prey,Predator\n");

    FILE *file2 = fopen(filename2, "w");
    if (!file2) {
        perror("Error opening second file");
        fclose(file1);
        return;
    }
    fprintf(file2, "Time,dx,dy\n");






    double t = 0.0, x = x0, y = y0;
    while (t <= t_max) {
        // Add stochasticity (random noise) to prey and predator growth
        // double noise_x = ((rand() % 200) - 100) / 1000.0;  // Small random noise for prey
        // double noise_y = ((rand() % 200) - 100) / 1000.0;  // Small random noise for predators

        fprintf(file1, "%.2f,%.5f,%.5f\n", t, x, y); // Important it's not same to compute dx and dy and then x and y or dx then x and dy then y 
        double dx = prey_growth_rate(a, b, x, y); // + noise_x
        x = x + dx * dt;
        double dy = predator_growth_rate(d, g, x, y); // + noise_y
        y = y + dy * dt;
        fprintf(file2, "%.2f,%.5f,%.5f\n", t, dx, dy);
        t += dt;
    }
    fclose(file1);
    fclose(file2);
}




// // sensitivity test 
// void sensitivity_test(
//     double d, double g, double x, double y, double t_max, double dt,
//     double a_min, double a_max, double a_step,
//     double b_min, double b_max, double b_step,
//     const char *filename) {

//     FILE *file = fopen(filename, "w");
//     if (!file) {
//         perror("Error opening file");
//         return;
//     }
//     fprintf(file, "a,b,FinalPrey,FinalPredators\n");

//     for (double a = a_min; a <= a_max; a += a_step) {
//         for (double b = b_min; b <= b_max; b += b_step) {
//             double final_prey, final_predators;
//             simulate_lotka_volterra(a, b, d, g, x, y, t_max, dt); // +file + &final_prey, &final_predators should not work wait for changes 
//             fprintf(file, "%.2f,%.2f,%.5f,%.5f\n", a, b, final_prey, final_predators);
//         }
//     }

//     fclose(file);
// }




