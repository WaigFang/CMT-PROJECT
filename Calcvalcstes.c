#include <stdio.h>
#include <stdlib.h>
#include <math.h> // Pour utiliser log()

#define MAX_LINES 100 // Nombre maximum de lignes à lire

int main() {
    // Déclarer les tableaux pour stocker les données
    int annees[MAX_LINES];
    int lievres[MAX_LINES];
    int lynx[MAX_LINES];
    int count = 0; // Compteur pour le nombre de lignes lues

    // Définir le chemin du fichier
    char filename[] = "Data/Leigh1968_harelynx.csv";

    // Ouvrir le fichier en lecture
    FILE *file = fopen(filename, "r");
    if (file == NULL) {
        printf("Erreur : impossible d'ouvrir le fichier %s.\n", filename);
        return 1; // Terminer le programme en cas d'erreur
    }

    // Lire les données à partir du fichier
//    printf("\nLecture des données...\n"); // Indiquer qu'on commence la lecture des données
//    while (fscanf(file, "%d,%d,%d", &annees[count], &lievres[count], &lynx[count]) == 3) {
//        printf("Lue : Année = %d, Lièvres = %d, Lynx = %d\n", annees[count], lievres[count], lynx[count]);
//        count++;
//        if (count >= MAX_LINES) {
//            printf("Erreur : trop de lignes dans le fichier.\n");
//            break;
//        }
//    }  Avec fscanf ca ne marche pas et doinc nous devons trouver une autre méthodes

// Affichage des données brutes
    char buffer[256];
    printf("Années avec populations de lièvres et lynx :\n");
while (fgets(buffer, sizeof(buffer), file)) {
    if (sscanf(buffer, "%d,%d,%d", &annees[count], &lievres[count], &lynx[count]) == 3) {
        printf("Année = %d, Lièvres = %d, Lynx = %d\n", annees[count], lievres[count], lynx[count]);
        count++;
    }
}


    // Initialisation des variables
    double L0 = lievres[0]; // Population initiale des lièvres
    double F0 = lynx[0];    // Population initiale des lynx
    double alpha[MAX_LINES - 1];
    double gamma[MAX_LINES - 1];
    double beta[MAX_LINES - 1];
    double delta[MAX_LINES - 1];

    double sum_alpha = 0.0, sum_beta = 0.0, sum_gamma = 0.0, sum_delta = 0.0;

    // Calcul des paramètres pour chaque année
    printf("\nParamètres calculés par année :\n");
    for (int i = 1; i < count; i++) {
        int t = annees[i] - annees[0]; // Temps écoulé

        // Calcul de alpha pour les lièvres
        double logL_t = log(lievres[i]);
        double logL_0 = log(L0);
        alpha[i - 1] = (logL_t - logL_0) / t;

        // Calcul de gamma pour les lynx
        double logF_t = log(lynx[i]);
        double logF_0 = log(F0);
        gamma[i - 1] = (logF_0 - logF_t) / t;

        // Calcul de beta (prédation)
        int delta_L = lievres[i] - lievres[i - 1];
        if (lievres[i] != 0 && lynx[i] != 0) {
            beta[i - 1] = (alpha[i - 1] * lievres[i] - delta_L) / (lievres[i] * lynx[i]);
        }

        // Calcul de delta (reproduction des lynx)
        double dF_dt = lynx[i] - lynx[i - 1];
        if (lievres[i] != 0 && lynx[i] != 0) {
            delta[i - 1] = (dF_dt + gamma[i - 1] * lynx[i]) / (lievres[i] * lynx[i]);
        }

        // Ajouter les valeurs aux sommes
        sum_alpha += alpha[i - 1];
        sum_beta += beta[i - 1];
        sum_gamma += gamma[i - 1];
        sum_delta += delta[i - 1];

        // Afficher les paramètres pour cette année
        printf("Année: %d, Alpha: %.6f, Beta: %.6f, Gamma: %.6f, Delta: %.6f\n",
               annees[i], alpha[i - 1], beta[i - 1], gamma[i - 1], delta[i - 1]);
    }

    // Calcul des moyennes
    double mean_alpha = sum_alpha / (count - 1);
    double mean_beta = sum_beta / (count - 1);
    double mean_gamma = sum_gamma / (count - 1);
    double mean_delta = sum_delta / (count - 1);

    // Affichage des moyennes
    printf("\nMoyennes des paramètres :\n");
    printf("Moyenne de Alpha = %.6f\n", mean_alpha);
    printf("Moyenne de Beta = %.6f\n", mean_beta);
    printf("Moyenne de Gamma = %.6f\n", mean_gamma);
    printf("Moyenne de Delta = %.6f\n", mean_delta);

        // Fermer le fichier
    fclose(file);
    return 0;
    }
