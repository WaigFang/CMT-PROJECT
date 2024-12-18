#include <math.h>
#include <stdio.h>
#include <stdlib.h>

double prey_growth_rate(double a,double b,double x,double y){ //dx/dt 
    return a*x - b*x*y;
}

double predator_growth_rate(double d, double g, double x, double y){ // dy/dt
    return d*x*y - g*y;
}

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
        fprintf(file1, "%.2f,%.5f,%.5f\n", t, x, y); // Important it's not same to compute dx and dy and then x and y or dx then x and dy then y 
        double dx = prey_growth_rate(a, b, x, y);
        x = x + dx * dt;
        double dy = predator_growth_rate(d, g, x, y); 
        y = y + dy * dt;
        fprintf(file2, "%.2f,%.5f,%.5f\n", t, dx, dy);
        t += dt;
    }
    fclose(file1);
    fclose(file2);
}





