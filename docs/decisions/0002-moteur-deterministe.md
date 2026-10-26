# 0002 — Moteur d'optimisation déterministe et séparé de la vision

Date : 26/10/2026 · Statut : accepté

**Contexte.** PRD §8.4 et §18 : les contraintes physiques priment et le fournisseur de vision doit rester remplaçable.

**Décision.** `optimize()` ne dépend que des données (mobilier, catalogue, détections validées, réglages). Algorithme glouton en deux temps : placement des minimums (visibilité, nouveautés, couverture) avec réservation de la largeur cible, puis remplissage vers la cible de chaque référence jusqu'à la saturation. Ordre de présentation appliqué ensuite (blocs, gradient prix, 3 tiers, points chauds, MDD).

**Conséquences.** Résultats reproductibles et vérifiables (le test contrôle 13 combinaisons). Pas d'optimum garanti : une résolution exacte (programmation linéaire en nombres entiers) pourra être évaluée au MVP.
