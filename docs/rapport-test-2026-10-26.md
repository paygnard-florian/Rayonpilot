# Rapport de test — 26 octobre 2026

Test de bout en bout du prototype sur le rayon lessive (`data/test-lessive/`), rejouable avec `python tests/e2e/test_parcours.py`.

## Conditions

- Projet vide, mobilier 3 × 1 m, 6 étagères, saisi dans l'interface.
- Catalogue de 33 références importé depuis `catalogue.csv` (dimensions : 9 issues de fiches bol.com, 24 mesurées sur la photo ; prix et ventes **inventés**).
- Réponse de l'IA **simulée** au format réel, avec erreurs volontaires : 6 produits non reconnus, un nombre de facings faux, une confusion de référence, un produit coupé au bord.
- La vraie détection par Claude n'a pas encore été mesurée sur ce jeu.

## Résultat : 39/39 contrôles réussis

| | Contrôle | Détail |
|---|---|---|
| ✅ | Projet vide créé | {'ex': False, 'cat': 0, 'det': 0, 'tab': 'fixture'} |
| ✅ | Mobilier saisi et validé | 300 cm, 18.0 m développés, 3 unités |
| ✅ | Mobilier non validé = blocage |  |
| ✅ | Calcul des unités : 3,00 m → 3 unités (plafond de 3 ÷ 1,33) |  |
| ✅ | Correspondance des colonnes détectée | non associées : ean |
| ✅ | Import du catalogue | 33 réf., 6 MDD, CA total 22831 € |
| ✅ | Ré-import : correspondance réutilisée, aucun doublon |  |
| ✅ | Valeurs invalides signalées à l’import | 1 erreur(s) |
| ✅ | Photo importée et redimensionnée | 441 Ko, contrôle de flou : nette |
| ✅ | Échec technique : aucune unité débitée, analyse marquée échouée | {'used': 0, 'h': ['échouée'], 'd': 0} |
| ✅ | Analyse réussie : 3 unités débitées une seule fois | 61 blocs, 6 non associés, 6 confiance faible |
| ✅ | Photo et catalogue envoyés à l’IA | invite de 3926 caractères |
| ✅ | Visuels produits découpés dans la photo | 31 références illustrées |
| ✅ | Optimisation bloquée tant que les détections ne sont pas vérifiées | 6 détection(s) ne sont associées à aucune référence du catalogue. / 6 détection(s) à confiance faible doivent être vérifiées. |
| ✅ | Corrections appliquées sans nouveau débit | 8 corrections sur 61 blocs (13 %), 60 blocs retenus |
| ✅ | Dimension estimée : blocage puis confirmation | Dimensions estimées à confirmer : Lessive poudre Prix X-tra 4,6 kg (Xtra). |
| ✅ | Saisie d’une mesure → provenance « Mesurée » |  |
| ✅ | Plan ca / horizontal / gradient | remplissage 88 %, facings 82→85, 24 déplacés, 0 violation(s), 1 ms |
| ✅ | Plan marge / horizontal / gradient | remplissage 88 %, facings 82→85, 22 déplacés, 0 violation(s), 1 ms |
| ✅ | Plan rotation / horizontal / gradient | remplissage 93 %, facings 82→93, 21 déplacés, 0 violation(s), 1 ms |
| ✅ | Plan rentabilite / horizontal / gradient | remplissage 89 %, facings 82→86, 24 déplacés, 0 violation(s), 1 ms |
| ✅ | Plan couverture / horizontal / gradient | remplissage 78 %, facings 82→74, 25 déplacés, 0 violation(s), 1 ms |
| ✅ | Plan is / horizontal / gradient | remplissage 96 %, facings 82→93, 22 déplacés, 0 violation(s), 1 ms |
| ✅ | Plan promo / horizontal / gradient | remplissage 88 %, facings 82→85, 24 déplacés, 0 violation(s), 1 ms |
| ✅ | Plan equilibre / horizontal / gradient | remplissage 96 %, facings 82→93, 22 déplacés, 0 violation(s), 1 ms |
| ✅ | Plan equilibre / horizontal / tiers | remplissage 96 %, facings 82→93, 22 déplacés, 0 violation(s), 1 ms |
| ✅ | Plan equilibre / horizontal / hot | remplissage 96 %, facings 82→93, 22 déplacés, 0 violation(s), 0 ms |
| ✅ | Plan equilibre / horizontal / perf / droite→gauche | remplissage 96 %, facings 82→93, 22 déplacés, 0 violation(s), 0 ms |
| ✅ | Plan equilibre / vert_cat / gradient | remplissage 92 %, facings 82→99, 26 déplacés, 0 violation(s), 2 ms |
| ✅ | Plan equilibre / vert_brand / gradient | impossible signalé : Disposition verticale impossible : les 13 blocs demandent au moins 413 cm pour 300 cm disponibles. Passez en d |
| ✅ | Contrainte impossible signalée (baril 30 cm imposé sur une étagère de 30 cm) | Lessive poudre Prix X-tra 4,6 kg est imposé sur l’étagère 2, mais il n’y tient pas (hauteur 30,0 cm, dégagement 30 cm). |
| ✅ | Règle produits volumineux | facings minimum cumulés : 47 avec la règle, 78 sans |
| ✅ | Génération par l’interface | remplissage 94 % |
| ✅ | Indice de sensibilité CA recalculé à la main (Apta Couleurs) | 1.819 ; 27 actions au plan d’action |
| ✅ | Exports CSV et PNG | planogramme-test-complet-lessive.csv (33 lignes), planogramme-test-complet-lessive.png [blob 1604196 o image/png] |
| ✅ | Quota : alerte à 80 % et analyse bloquée si le solde est insuffisant |  |
| ✅ | Projet conservé après rechargement | {'name': 'Test complet lessive', 'n': 60, 'cat': 33, 'plan': True, 'photo': True} |
| ✅ | Affichage mobile 390 px sans défilement horizontal |  |
| ✅ | Aucune erreur JavaScript |  |

Durées d'automatisation (secondes, indicatives) : mobilier 1.7, catalogue 1.8, analyse 1.5, corrections 2.1, dimensions 1.3, planogrammes 1.5, rapport 3.2.

## Défauts trouvés et corrigés pendant le test

- Erreur JavaScript quand un champ était modifié puis quitté (rendu pendant `blur`) → rendus différés (`deferIfChange`).
- Colonne « Source des dimensions » du CSV ignorée → reprise dans `dimNote`.

## Limites observées

- Critères physiques basés sur le volume : une boîte de poudre dense finit sur l'étagère du haut.
- En disposition horizontale, une catégorie peut être éclatée sur plusieurs étagères ; la disposition verticale par catégorie l'évite (92 % de remplissage).
- Disposition verticale par marque impossible sur 3 m avec 13 marques : signalée correctement.
- Visuels des capsules empilées par deux écrasés dans le rendu photo.

## À mesurer ensuite (PRD §15.1)

Sur 30 photos réelles : taux de blocs détectés, taux de correction, erreurs de référence, temps d'analyse, coût par photo, par fournisseur de vision.
