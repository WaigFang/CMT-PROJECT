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
void simulate_lotka_volterra(double a, double b, double d, double g, double x0, double y0, double t_max, double dt, const char *filename) {
    FILE *file = fopen(filename, "w");
    if (!file) {
        perror("Error opening file");
        return;
    }
    fprintf(file, "Time,Prey,Predator\n");

    double t = 0.0, x = x0, y = y0;
    while (t <= t_max) {
        fprintf(file, "%.2f,%.5f,%.5f\n", t, x, y);
        double dx = prey_growth(x, y, a, b);
        double dy = predator_growth(x, y, d, g);
        x += dx * dt;
        y += dy * dt;
        t += dt;
    }
    fclose(file);
}


typedef struct {
    double * t;
    double * x;
    double * y; 
}Timepopulation;

Timepopulation* population_evolution(int maxtime,double a,double b, double d,double g, double x, double y){
    Timepopulation* table = (Timepopulation*)malloc(sizeof(Timepopulation));

    if (!table) return NULL;

    table->t = (double*)malloc(maxtime * sizeof(double));
    table->x = (double*)malloc(maxtime * sizeof(double));
    table->y = (double*)malloc(maxtime * sizeof(double));
    if (!table->t || !table->x || !table->y) {
        free(table->t);
        free(table->x);
        free(table->y);
        free(table);
        return NULL;
    }
    for (int i =1847; i<maxtime;i++){
        table->t[i] = i+1;
        table->x[i] = x;
        table->y[i] = y;
        double xnext = x + prey_growth_rate(a,b,x,y);
        double ynext = y + predator_growth_rate(d,g,x,y);
        x = xnext;
        y = ynext;
    }
    return table;
}

void free_population(Timepopulation* table) {
    if (table) {
        free(table->t);
        free(table->x);
        free(table->y);
        free(table);
    }
}


