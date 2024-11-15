#include <math.h>
#include <stdio.h>

double prey_density_over_time(double alpha,double beta,int x,int y){
    return (alpha * x) - (beta * x *y);
}


double predator_density_over_time(double delta, double gamma, int x, int y){
    return (delta*x*y) - (gamma*y);
}

hs