#include <math.h>
#include <stdio.h>
#include <stdlib.h>


struct Timepopulation{
    int * t;
    double * x;
    double * y; 
};

double prey_growth_rate(double alpha,double beta,int x,int y){ //dx/dt // alpha,beta > 0
    return (alpha * x) - (beta * x *y);
}


double predator_growth_rate(double delta, double gamma, int x, int y){ // dy/dt //delta,gamma > 0
    return (delta*x*y) - (gamma*y);
}

Timepopulation* population_evolution(int maxtime,double alpha,double beta, double delta,double gamma, int x, int y){
    Timepopulation* table = (Timepopulation*)malloc(sizeof(Timepopulation));
    int t = 0;
    t += 1;
    x += prey_growth_rate(alpha,beta,x,y);
    y += predator_growth_rate(delta,gamma,x,y);




}