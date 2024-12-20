#include <stdio.h>
#include <stdlib.h>
#include <math.h> 
#define MAX_LINES 100 

int main() {
    // stock data
    int years[MAX_LINES];
    int hares[MAX_LINES];
    int lynx[MAX_LINES];
    int count = 0; // counts number of lines 

    char filename[] = "Data/Leigh1968_harelynx.csv";

    // opens file in read mode 
    FILE *file = fopen(filename, "r");
    if (file == NULL) {
        printf("Error: unable to open file %s.\n", filename);
        return 1; // ends code if error 
    }

    // Affichage des données brutes
    char buffer[256];
    printf("Years and hare and lynx populations :\n");
    while (fgets(buffer, sizeof(buffer), file)) {
        if (sscanf(buffer, "%d,%d,%d", &years[count], &hares[count], &lynx[count]) == 3) {
            count++;
        }
    }

    // variables initialisation
    double L0 = hares[0]; 
    double F0 = lynx[0];   
    double alpha[MAX_LINES - 1];
    double gamma[MAX_LINES - 1];
    double beta[MAX_LINES - 1];
    double delta[MAX_LINES - 1];

    double sum_alpha = 0.0, sum_beta = 0.0, sum_gamma = 0.0, sum_delta = 0.0;

    // Computation of parameters for each year 
    printf("\nCalculated parameters by year:\n");
    for (int i = 1; i < count; i++) {
        int t = years[i] - years[0]; // Temps écoulé

        // alpha for hares
        double logL_t = log(hares[i]);
        double logL_0 = log(L0);
        alpha[i - 1] = (logL_t - logL_0) / t;

        // gamma for lynx
        double logF_t = log(lynx[i]);
        double logF_0 = log(F0);
        gamma[i - 1] = (logF_0 - logF_t) / t;

        // beta
        int delta_L = hares[i] - hares[i - 1];
        if (hares[i] != 0 && lynx[i] != 0) {
            beta[i - 1] = (alpha[i - 1] * hares[i] - delta_L) / (hares[i] * lynx[i]);
        }

        // delta 
        double dF_dt = lynx[i] - lynx[i - 1];
        if (hares[i] != 0 && lynx[i] != 0) {
            delta[i - 1] = (dF_dt + gamma[i - 1] * lynx[i]) / (hares[i] * lynx[i]);
        }

        
        sum_alpha += alpha[i - 1];
        sum_beta += beta[i - 1];
        sum_gamma += gamma[i - 1];
        sum_delta += delta[i - 1];

        // print parameters for each year
        printf("Year: %d, Alpha: %.6f, Beta: %.6f, Gamma: %.6f, Delta: %.6f\n",
               years[i], alpha[i - 1], beta[i - 1], gamma[i - 1], delta[i - 1]);
    }

    // mean calculation
    double mean_alpha = sum_alpha / (count - 1);
    double mean_beta = sum_beta / (count - 1);
    double mean_gamma = sum_gamma / (count - 1);
    double mean_delta = sum_delta / (count - 1);

    // print mean
    printf("\nMeans of parameters :\n");
    printf("Mean of Alpha = %.6f\n", mean_alpha);
    printf("Mean of Beta = %.6f\n", mean_beta);
    printf("Mean of Gamma = %.6f\n", mean_gamma);
    printf("Mean of Delta = %.6f\n", mean_delta);

    // save in a .csv file 
    char output_filename[] = "Outputs/mean_estimated_parameters.csv";

    // open in write mode the file
    FILE *output_file = fopen(output_filename, "w");
    if (output_file == NULL) {
        printf("Error: unable to open file %s.\n", output_filename);
        return 1; // Terminer en cas d'erreur
    }

    
    fprintf(output_file, "Alpha,Beta,Delta,Gamma\n");

    fprintf(output_file, "%.6f, %.6f, %.6f, %.6f\n", mean_alpha, mean_beta, mean_delta, mean_gamma);

    fclose(output_file);

    fclose(file);
    return 0;
}
