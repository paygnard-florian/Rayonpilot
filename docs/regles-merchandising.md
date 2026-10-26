# Règles de merchandising et leur traduction dans le moteur

Source : *Cours de techniques merchandising* (carnet de marchandisage, voir `docs/references/`). Les numéros renvoient aux sections du cours.

## Objectifs (`OBJ` dans `optimize()`)

| Objectif | Calcul de la priorité d'une référence | Cours |
|---|---|---|
| Chiffre d'affaires | part de CA | 4.6 |
| Marge brute | part de marge | 4.6, 4.9 |
| Rotation | part des unités vendues | 4.8 |
| Rentabilité du linéaire | marge × coefficient de rotation (ventes ÷ stock moyen) | 4.9 |
| Couverture de stock | facings = ventes/jour × jours cibles ÷ capacité d'un facing (profondeur ÷ profondeur produit) | 1.8, capacité de stockage |
| Indices de sensibilité | place actuelle × indice moyen (CA, marge, quantités) | 4.6 |
| Mise en avant | priorité aux promotions et nouveautés, puis CA | 2.9 |
| Équilibre | moyenne des parts CA, marge, quantités | — |

Objectifs secondaires : poids de 35 % ajouté à l'objectif principal (PRD §4.7).

## Règles physiques et de gestion

| Règle | Implémentation | Cours |
|---|---|---|
| Contraintes physiques (largeur, hauteur, profondeur) | strictes : hauteur produit ≤ dégagement − 1 cm, profondeur ≤ profondeur d'étagère, somme des largeurs ≤ longueur | — (PRD §18) |
| Seuil de visibilité | minimum de facings = plafond(seuil ÷ largeur) ; 33 cm en grande surface, 20 cm en proximité | 1.11 |
| Produits volumineux | façade (L × H) ≥ seuil (300 cm² par défaut) → 1 facing autorisé ; réglable par référence | 1.11 (adaptation) |
| Seuil de saturation | maximum de facings = plancher(saturation ÷ largeur), 100 cm par défaut | 1.12 |
| Valeur des niveaux | sol < 50 cm : 0,55 ; < 90 : 0,75 ; < 120 : 0,9 ; 120–165 (yeux) : 1 ; au-delà : 0,7 | 1.6 |
| Compensation des niveaux | cible multipliée par 1 ÷ valeur du niveau | 1.6 |
| Critères physiques | pénalité pour les produits volumineux placés haut (volume relatif²) | 2.1 |
| Couverture minimale | minimum de facings pour tenir N jours | 1.8 |

## Organisation et présentation

| Règle | Implémentation | Cours |
|---|---|---|
| Horizontalité / verticalité | disposition horizontale, verticale par catégorie ou par marque (colonnes sur toute la hauteur, une référence peut occuper plusieurs étagères) | 2.4, 2.6 |
| Product blocking / color blocking | regroupement par catégorie ou par marque dans l'étagère | 2.12, 2.13 |
| Gradient prix horizontal | du moins cher au plus cher dans le sens de circulation | 2.5 |
| Gradient prix vertical | premiers prix en bas | 2.5 |
| Règle des 3 tiers | meilleures références au centre | 2.7 |
| Points chauds aux extrémités | références d'appel aux deux bouts | zone chaude (glossaire) |
| MDD à droite du leader | contre-type MDD juste après la marque leader de la catégorie | 2.8 |
| Nouveautés | au moins 2 facings, de préférence au niveau des yeux | 2.9 |
| Sens de circulation | inversion de l'ordre si circulation de droite à gauche | 1.5 |

## Limites connues (rapport de test du 26/10/2026)

- Les critères physiques reposent sur le volume, pas sur le poids : une petite boîte dense (poudre) peut finir en haut. → ajouter un champ poids.
- En disposition horizontale, une catégorie peut être répartie sur plusieurs étagères non voisines.
- Pas encore de rappel (casquette), de facing feuilleté, ni de zones interdites dans le mobilier.
