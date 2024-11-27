#include <stdio.h>
#include <stdlib.h>
#include <math.h> // Pour utiliser log()

#define MAX_LINES 100 // Nombre maximum de lignes à lire

int main() {
    // Déclarer les tableaux pour stocker les données
    int annees[MAX_LINES];
    int lievres[MAX_LINES];
    int lynx[MAX_LINES];  // Données pour les lynx
    int count = 0; // Compteur pour le nombre de lignes lues

    // Ouvrir le fichier en lecture
    FILE* file = fopen("Data/Leigh1968_harelynx.csv", "r");
    if (file == NULL) {
        printf("Erreur : impossible d'ouvrir le fichier.\n");
        return 1;
    }

    // Lire les données à partir du fichier
    while (fscanf(file, "%d,%d,%d", &annees[count], &lievres[count], &lynx[count]) == 3) {
        // Afficher les données lues pour vérifier
        printf("Année: %d, Lièvres: %d, Lynx: %d\n", annees[count], lievres[count], lynx[count]);
        count++;
        if (count >= MAX_LINES) {
            printf("Erreur : trop de lignes dans le fichier.\n");
            break;
        }
    }

    // Fermer le fichier
    fclose(file);

    // Initialisation des variables
    double L0 = lievres[0]; // Population initiale des lièvres (première ligne)
    double F0 = lynx[0]; // Population initiale des lynx (1847)

    // Déclaration des tableaux pour les paramètres
    double alpha[MAX_LINES - 1];
    double gamma[MAX_LINES - 1];
    double beta[MAX_LINES - 1];
    double delta[MAX_LINES - 1]; // Nouveau tableau pour delta

    // Calcul de alpha, gamma, beta et delta pour chaque année
    for (int i = 1; i < count; i++) {
        int t = annees[i] - annees[0]; // Temps écoulé depuis la première année

        // Calcul de alpha pour les lièvres
        double logL_t = log(lievres[i]); // Logarithme de L(t) pour les lièvres
        double logL_0 = log(L0); // Logarithme de L0 pour les lièvres
        alpha[i - 1] = (logL_t - logL_0) / t;

        // Calcul de gamma pour les lynx
        double logF_t = log(lynx[i]); // Logarithme de F(t) pour les lynx
        double logF_0 = log(F0); // Logarithme de F0 pour les lynx
        gamma[i - 1] = (logF_0 - logF_t) / t;

        // Calcul de la variation de la population des lièvres (ΔL)
        int delta_L = lievres[i] - lievres[i - 1];

        // Calcul de beta pour les lynx (prédation)
        if (lievres[i] != 0 && lynx[i] != 0) {
            beta[i - 1] = (alpha[i - 1] * lievres[i] - delta_L) / (lievres[i] * lynx[i]);
        }

        // Calcul de la variation de la population des lynx (ΔF)
        double dF_dt = lynx[i] - lynx[i - 1];

        // Calcul de delta (taux de reproduction des lynx)
        if (lievres[i] != 0 && lynx[i] != 0) {
            delta[i - 1] = (dF_dt + gamma[i - 1] * lynx[i]) / (lievres[i] * lynx[i]);
        }

        // Affichage des résultats pour vérifier
        printf("Année: %d\n", annees[i]);
        printf("Log(L(%d)) = %.6f, Log(L0) = %.6f, Alpha = %.6f\n", annees[i], logL_t, logL_0, alpha[i - 1]);
        printf("Log(F(%d)) = %.6f, Log(F0) = %.6f, Gamma = %.6f\n", annees[i], logF_t, logF_0, gamma[i - 1]);
        printf("Beta = %.6f\n", beta[i - 1]);  // Affichage du Beta
        printf("Delta = %.6f\n", delta[i - 1]);  // Affichage du Delta
    }

    // Afficher uniquement les valeurs de alpha, gamma, beta et delta
    printf("\nAlpha values for hares:\n");
    for (int i = 1; i < count; i++) {
        printf("%.6f\n", alpha[i - 1]); // Affiche alpha pour chaque année
    }

    printf("\nGamma values for lynx:\n");
    for (int i = 1; i < count; i++) {
        printf("%.6f\n", gamma[i - 1]); // Affiche gamma pour chaque année
    }

    printf("\nBeta values for predation:\n");
    for (int i = 1; i < count; i++) {
        printf("%.6f\n", beta[i - 1]); // Affiche beta pour chaque année
    }

    printf("\nDelta values for lynx reproduction:\n");
    for (int i = 1; i < count; i++) {
        printf("%.6f\n", delta[i - 1]); // Affiche delta pour chaque année
    }

    return 0;
}