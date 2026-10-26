# 0003 — Vision IA : Claude, coordonnées en pixels, fournisseur interchangeable

Date : 26/10/2026 · Statut : accepté pour le prototype ; comparaison des fournisseurs à faire

**Contexte.** PRD §16.3 : comparer 2 ou 3 fournisseurs sur les mêmes images.

**Décision.** Dans un artifact Claude, l'analyse passe par le compte Claude de l'utilisateur. Dans la PWA, par l'API Claude (clé locale pour un usage personnel, ou serveur relais `netlify/functions/analyse.mjs` pour une équipe). L'image envoyée est redimensionnée à une taille connue (`fitDims`) et les cadres sont demandés en pixels, conformément à la documentation de Claude sur les coordonnées. Les réponses sont normalisées dans un format unique (`detections` avec `bbox`), pour pouvoir brancher un autre fournisseur (modèle ouvert via Ollama, détection embarquée).

**Conséquences.** Coût et durée enregistrés à chaque analyse. Reste à mesurer sur 30 photos : taux de détection, taux de correction, erreurs de référence, temps et coût, par fournisseur.
