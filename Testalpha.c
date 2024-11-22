#include <stdio.h>
#include <stdlib.h>
#include <math.h> // Pour utiliser log()

#define MAX_LINES 100 // Nombre maximum de lignes à lire

int main() {
    //Déclarer les tableaux pour stocker les données
    int annees[MAX_LINES];
    int lievres[MAX_LINES];
    int lynx[MAX_LINES];  // Bien que nous ne l'utilisions pas dans ce calcul
    int count = 0; // Compteur pour le nombre de lignes lues

    // Ouvrir le fichier en lecture
    FILE* file = fopen("Leigh1968_harelynx.csv", "r");
    if (file == NULL) {
        printf("Erreur : impossible d'ouvrir le fichier.\n");
        return 1;
    }

    // Lire le fichier ligne par ligne (ignorer la première ligne si c'est un en-tête)
    char buffer[100];
    fgets(buffer, sizeof(buffer), file); // Lire et ignorer la première ligne

    // Lire les données à partir du fichier
    while (fscanf(file, "%d,%d,%d", &annees[count], &lievres[count], &lynx[count]) == 3) {
        count++;
        if (count >= MAX_LINES) {
            printf("Erreur : trop de lignes dans le fichier.\n");
            break;
        }
    }

    // Fermer le fichier
    fclose(file);

    // Calcul de alpha pour les lièvres
    double L0 = lievres[0]; // Population initiale des lièvres
    double alpha[MAX_LINES - 1];

    for (int i = 1; i < count; i++) {
        int t = annees[i] - annees[0]; // Temps écoulé depuis la première année
        alpha[i - 1] = (log(lievres[i]) - log(L0)) / t; // Formule de alpha
    }

    // Afficher uniquement les valeurs de alpha
    for (int i = 1; i < count; i++) {
        printf("%.6f\n", alpha[i - 1]); // Affiche alpha pour chaque année
    }

    return 0;
}