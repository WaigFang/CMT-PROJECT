#include <math.h>
#include <stdio.h>

double prey_growth_rate(double alpha,double beta,int x,int y){ //dx/dt // alpha,beta > 0
    return (alpha * x) - (beta * x *y);
}


double predator_growth_rate(double delta, double gamma, int x, int y){ // dy/dt //delta,gamma > 0
    return (delta*x*y) - (gamma*y);
}
<<<<<<< HEAD
=======

hs
>>>>>>> bc2642641544ba1d82522915c41f1e23de75ced1
