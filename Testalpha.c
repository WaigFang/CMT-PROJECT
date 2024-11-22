#include <stdio.h>
#include <stdlib.h>
#include <math.h> // Pour utiliser log()

#define MAX_LINES 100 // Nombre maximum de lignes à lire

int main() {
    // Déclarer les tableaux pour stocker les données
    int annees[MAX_LINES];
    int lievres[MAX_LINES];
    int lynx[MAX_LINES];  // Bien que nous ne l'utilisions pas dans ce calcul
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

    // Calcul de alpha pour les lièvres
    double L0 = lievres[0]; // Population initiale des lièvres (première ligne)
    double alpha[MAX_LINES - 1];

    // Afficher les valeurs de log(L(t)) et log(L0) avant le calcul de alpha
    for (int i = 1; i < count; i++) {
        int t = annees[i] - annees[0]; // Temps écoulé depuis la première année
        double logL_t = log(lievres[i]); // Calcul du logarithme de L(t)
        double logL_0 = log(L0); // Logarithme de L0 (population initiale des lièvres)

        printf("Log(L(%d)) = %.6f, Log(L0) = %.6f\n", annees[i], logL_t, logL_0);

        // Calcul de alpha
        alpha[i - 1] = (logL_t - logL_0) / t;
    }

    // Afficher uniquement les valeurs de alpha
    for (int i = 1; i < count; i++) {
        printf("%.6f\n", alpha[i - 1]); // Affiche alpha pour chaque année
    }

    return 0;
}