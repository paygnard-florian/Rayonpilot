# Feuille de route

Référence : PRD §14 (phases A à G). État au 26/10/2026.

| Phase | Contenu | État |
|---|---|---|
| A — Préparation | scénario, GitHub, jeu de test, rayon cible, coûts | Fait : rayon lessive, dépôt, coûts IA suivis. Reste : 29 photos. |
| B — Vision | comparer fournisseurs, erreurs et coût par photo | En cours : Claude intégré (artifact et API). Comparaison à faire. |
| C — Correction / données | correction, catalogue, import, dimensions | Fait au niveau prototype. |
| D — Planogramme | mobilier, placement, contraintes, rendu 2D, cas impossibles | Fait au niveau prototype (8 objectifs, 3 dispositions, rendu photo). |
| E — Démonstration | parcours complet, tests, mesures | Fait en simulation (39/39). Reste : mesure avec la vraie IA. |
| F — MVP commercial | comptes, magasins, historique, rapports, quotas, facturation | À faire. |
| G — Pilote | tests utilisateurs, support, sécurité, lancement progressif | À faire. |

## Prochaines étapes proposées (dans l'ordre)

1. Mesurer la vraie détection sur la photo lessive, puis constituer les 30 photos du PRD.
2. Extraire le moteur (`optimize`, `checks`, calculs d'indices) dans un module TypeScript testé unitairement (`packages/engine`), réutilisé par le prototype.
3. Ajouter le poids au catalogue et l'utiliser dans les critères physiques.
4. Comparer 2 fournisseurs de vision sur les 30 photos (Claude + un modèle ouvert ou une API concurrente).
5. Décider du passage au MVP (critères §15.2) ; si oui : Next.js + Supabase (région UE), authentification, organisations, magasins, quotas côté serveur.
6. Application mobile Expo réutilisant le moteur.
