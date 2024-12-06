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

    double sum_alpha = 0.0, sum_beta = 0.0, sum_gamma = 0.0, sum_delta = 0.0;

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

        // Ajouter les valeurs pour les moyennes
        sum_alpha += alpha[i - 1];
        sum_beta += beta[i - 1];
        sum_gamma += gamma[i - 1];
        sum_delta += delta[i - 1];
    }

    // Calcul des moyennes
    double a = sum_alpha / (count - 1); // Moyenne de alpha
    double b = sum_beta / (count - 1);  // Moyenne de beta
    double g = sum_gamma / (count - 1); // Moyenne de gamma
    double d = sum_delta / (count - 1); // Moyenne de delta

    // Affichage des résultats pour vérifier
    printf("\nMoyennes des paramètres :\n");
    printf("Moyenne de alpha (a) = %.6f\n", a);
    printf("Moyenne de beta (b) = %.6f\n", b);
    printf("Moyenne de gamma (g) = %.6f\n", g);
    printf("Moyenne de delta (d) = %.6f\n", d);

    return 0;
}
