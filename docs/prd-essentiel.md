# PRD v2.0 — l'essentiel

Résumé de travail du PRD consolidé v2.0 du 23 octobre 2026. Le document complet (PDF) fait foi : le placer dans `docs/references/` (voir le README de ce dossier).

## Cadre

- SaaS d'aide au merchandising pour enseignes, magasins et réseaux ; à terme, industriels.
- Développement solo, 15 à 25 h par semaine, budget < 5 000 €, MVP visé en environ 6 mois. Le délai n'est pas une garantie.
- Marché initial : rayon alimentaire de produits emballés.
- Objectif prioritaire : **photo → détection → correction → dimensions vérifiées → planogramme 2D**.

## Principes directeurs (§1.1)

Qualité avant vitesse ; contraintes physiques strictes ; l'utilisateur corrige l'IA ; incertitudes visibles, données manquantes jamais inventées ; prévisions et résultats observés distincts ; données commerciales isolées ; budget, temps et coûts IA suivis dès le prototype.

## Fonctions (§4)

- **Reconnaissance** : emballages et étiquettes, confiance affichée, correction, produits inconnus, association manuelle. Codes-barres et OCR avancé plus tard.
- **Prise de vue** : import au prototype, capture guidée mobile à terme, détection du flou et de la couverture.
- **Correction** : ajouter, supprimer, modifier référence, facings, position, dimensions ; corrections sans nouvelle unité.
- **Dimensions** : provenance catalogue / mesurée / estimée / inconnue ; toute dimension incertaine qui menace la faisabilité est validée avant optimisation.
- **Mobilier** : largeur, hauteur, profondeur, étagères, séparateurs, zones interdites.
- **Catalogue** : CSV, XLSX, XLS ; correspondance des colonnes suggérée et réutilisable ; le dernier import prévaut pour les champs présents ; traçabilité.
- **Optimisation** : objectif principal + secondaires (CA, marge, rotation, stock, promotion, performance au mètre, équilibre). Contraintes physiques prioritaires ; si aucune solution, lister les contraintes bloquantes.
- **Planogramme** : 2D simple au prototype ; éditeur complet au produit cible, sans contournement silencieux des contraintes.
- **Rapports** : tableau de bord, exports PDF/Excel, indicateurs affichés seulement si les données existent.
- **Plan d'action** : responsable, échéance, statut (à faire, en cours, terminé, bloqué), preuves photo, comparaison à 30 jours.

## Comptes et tarifs (§5–6)

- Rôles Owner, Admin, Manager, Operator ; droits par organisation et magasin ; journal d'audit.
- Offres hypothétiques : Starter 49 € (5 unités), Pro 149 € (20), Enterprise 298 €/magasin (50).
- 1 unité = 1,33 m linéaire, plafond(longueur ÷ 1,33). Quotas mensuels par magasin, alerte à 80 %, blocage à 100 %, pas de dépassement payant au lancement.
- Débit : analyse réussie seulement ; échec technique non facturé ; tentatives idempotentes.

## IA et qualité (§8)

- Confiance élevée / moyenne / faible ; seuils définis par tâche.
- Analyse standard en 5 min maximum, progression visible.
- Moteur de contraintes séparé du fournisseur de vision, déterministe, fournisseurs remplaçables.
- Statuts en cours / terminée / échouée ; distinguer analyse impossible et erreur technique.

## Architecture cible (§10)

Web Next.js + TypeScript ; mobile React Native + Expo ; backend API sécurisée, PostgreSQL, authentification, stockage privé (Supabase ou équivalent, à vérifier) ; vision IA par API choisie après comparaison ; traitement asynchrone idempotent avec suivi des coûts ; Stripe pour le web ; hébergement dans l'UE ; environnements dev/test/prod.

## Exigences non fonctionnelles et sécurité (§11–12)

Disponibilité 99,5 % ; sauvegardes et restauration testées ; isolation stricte des organisations ; chiffrement ; pas d'entraînement de modèles sur données clients sans base légale ; durées de conservation par catégorie ; export et suppression par l'Owner ; documents juridiques (mentions, confidentialité, CGV, DPA).

## Plan (§14–15)

Phases : A préparation → B vision → C correction/données → D planogramme → E démonstration → F MVP commercial → G pilote.
Première tranche : vertical slice, reconnaissance visuelle, dimensions IA validées, planogramme 2D, jeu de 30 photos, GitHub privé ; critère de passage : démonstration réussie sur plusieurs photos.

## Décisions ouvertes (§16) et état

| Sujet | Options du PRD | État au 26/10/2026 |
|---|---|---|
| Interface initiale | web responsive / mobile / les deux | Web responsive + PWA installable (voir ADR 0001). |
| Méthode de développement | code assisté, low-code, agent IA, mix | Agent de développement IA (Claude Code) sur dépôt GitHub. |
| Fournisseur de vision | comparer 2–3 fournisseurs | Claude intégré ; comparaison à faire sur 30 photos (ADR 0003). |
| Dimensions du rayon | manuel / photo + confirmation / hybride | Hybride : saisie manuelle du mobilier, produits par fiche, mesure ou estimation confirmée. |
| Catalogue du premier test | CSV / saisie / sans catalogue | CSV de 33 références + association automatique après analyse. |
| Premier scénario | 1 photo / plusieurs / rayon complet | 1 photo d'un rayon complet de 6 étagères (lessive). |
