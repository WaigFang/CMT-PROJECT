#include <math.h>
#include <stdio.h>

void prey_density_over_time(double alpha,double beta,int x,int y){
    double dx_dt = 0;
    dx_dt = (alpha * x) - (beta * x *y);
}


void predator_density_over_time(double delta, double gamma, int x, int y){
double dy_dt = 0; 
dy_dt = (delta*x*y) - (gamma*y);
}

