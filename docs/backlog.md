# Backlog

À recopier en issues GitHub (un titre = une issue). Étiquettes proposées : `moteur`, `vision`, `interface`, `données`, `mvp`, `test`.

## Prochaines étapes

- [ ] **[vision] Mesurer la vraie détection sur la photo lessive** — lancer l'analyse dans Claude, comparer aux 60 blocs de référence (`reponse-ia-simulee.json`), noter blocs trouvés, erreurs de référence, temps, coût.
- [ ] **[données] Constituer le jeu de 30 photos autorisées** — rayons variés, une fiche par photo (mobilier, date, magasin anonymisé).
- [ ] **[moteur] Extraire le moteur en module TypeScript** — `packages/engine` avec `checks`, `optimize`, indices ; tests unitaires (contraintes, seuils, MDD, cas impossibles) ; le prototype l'importe ou l'intègre au build.
- [x] **[moteur] Ajouter le poids** — colonne `poids_kg` au catalogue, critères physiques sur le poids (repli sur le volume).
- [ ] **[test] Ajouter un test de non-régression du planogramme** — comparer le plan généré sur le jeu lessive à un instantané validé.

## Moteur

- [ ] Empêcher l'éclatement d'une catégorie sur des étagères non voisines en disposition horizontale.
- [ ] Zones interdites et séparateurs dans le mobilier (PRD §4.5).
- [ ] Produits en rappel / casquette et facing feuilleté (cours 1.9, 2.2).
- [ ] Évaluer une résolution exacte (PLNE) pour comparer à l'algorithme glouton.

## Vision

- [ ] Mode « serveur compatible Ollama / OpenAI » pour un modèle ouvert.
- [ ] Analyse en plusieurs photos d'un même rayon (assemblage).
- [ ] Découpage des visuels empilés (une seule unité par vignette).

## Interface

- [ ] Éditeur de planogramme : déplacer un produit, modifier les facings, avec contrôle des contraintes en direct (PRD §4.8).
- [ ] Preuves d'exécution : photo après implantation dans le plan d'action (PRD §4.10).
- [ ] Export PDF du rapport.

## MVP

- [ ] Comptes, organisations, magasins et rôles (PRD §5).
- [ ] Quotas et débit idempotent côté serveur (PRD §6.3).
- [ ] Hébergement UE, sauvegardes, journal d'audit (PRD §10–12).
