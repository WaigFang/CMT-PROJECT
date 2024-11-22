#include <math.h>
#include <stdio.h>
#include <stdlib.h>

double prey_growth_rate(double alpha,double beta,int x,int y){ //dx/dt // alpha,beta > 0
    return (alpha * x) - (beta * x *y);
}

double predator_growth_rate(double delta, double gamma, int x, int y){ // dy/dt //delta,gamma > 0
    return (delta*x*y) - (gamma*y);
}


typedef struct {
    int * t;
    double * x;
    double * y; 
}Timepopulation;

Timepopulation* population_evolution(int maxtime,double alpha,double beta, double delta,double gamma, int x, int y){
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


}

void free_population(Timepopulation* table) {
    if (table) {
        free(table->t);
        free(table->x);
        free(table->y);
        free(table);
    }
}
