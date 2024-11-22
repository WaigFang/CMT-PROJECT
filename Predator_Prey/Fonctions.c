#include <math.h>
#include <stdio.h>
#include <stdlib.h>

double prey_growth_rate(double alpha,double beta,double x,double y){ //dx/dt // alpha,beta > 0
    return (alpha * x) - (beta * x *y);
}

double predator_growth_rate(double delta, double gamma, double x, double y){ // dy/dt //delta,gamma > 0
    return (delta*x*y) - (gamma*y);
}


typedef struct {
    double * t;
    double * x;
    double * y; 
}Timepopulation;

Timepopulation* population_evolution(int maxtime,double alpha,double beta, double delta,double gamma, double x, double y){
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
        double xnext = x + prey_growth_rate(alpha,beta,x,y);
        double ynext = y + predator_growth_rate(delta,gamma,x,y);
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
