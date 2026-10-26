# RayonPilot — instructions pour Claude Code

RayonPilot aide à optimiser le merchandising d'un rayon en libre-service : photo du rayon → détection des produits → correction → dimensions vérifiées → planogramme 2D sous contraintes → plan d'action.
Langue du produit, de l'interface, des commits et de la documentation : **français**.

## Où en est le projet

- Phase actuelle : fin de la phase E du PRD (démonstration de bout en bout). Le prototype fonctionne ; le MVP (phase F) n'est pas commencé.
- `prototype/rayonpilot.html` est **la source de vérité** du prototype : une seule page HTML autonome (CSS + JS sans framework), publiée telle quelle comme artifact Claude.
- `prototype/pwa/` est la version installable (PWA). Son `index.html` est **généré** : ne pas le modifier à la main, lancer `python scripts/build_pwa.py`.
- Lire `docs/prd-essentiel.md` avant toute décision produit, et `docs/feuille-de-route.md` pour la suite.

## Règles produit non négociables (PRD §18)

1. Les contraintes physiques (largeur, hauteur, profondeur des étagères) priment toujours sur l'objectif commercial. Aucun plan ne doit les dépasser, ni les contourner en silence.
2. Les dimensions ne sont jamais inventées : chaque dimension garde sa provenance (catalogue, fiche produit, mesurée, estimée, inconnue). Une dimension estimée non confirmée ou manquante **bloque** l'optimisation.
3. Si aucun plan valide n'existe, lister les contraintes bloquantes au lieu de produire un plan.
4. Prévisions et résultats observés restent séparés. Un indicateur ne s'affiche que si ses données existent.
5. Échec technique = aucune unité débitée. Les corrections d'une même analyse ne consomment pas d'unité. Débit idempotent.
6. Unité de consommation : 1 unité = 1,33 m linéaire, unités = plafond(longueur ÷ 1,33).
7. Les données commerciales d'une organisation ne sont jamais visibles d'une autre.
8. Le moteur d'optimisation est déterministe et indépendant du fournisseur de vision (PRD §8.4).

## Architecture actuelle du prototype

Dans `prototype/rayonpilot.html`, sections repérées par des commentaires `/* ---------- … ---------- */` :

- **état** : objet global `S` (mobilier, catalogue, détections, réglages, plan), sauvegardé dans `localStorage` (`rayonpilot_v1`). La clé API éventuelle est stockée à part (`rayonpilot_api`) et ne doit jamais entrer dans `S` ni dans les exports.
- **contrôles bloquants** : `checks()` renvoie `{bad, warn}` ; tout point `bad` désactive la génération.
- **moteur d'optimisation** : `optimize()` → objectifs, zones (disposition horizontale ou verticale), placement par étagère, remplissage vers la cible, ordre de présentation, indicateurs. Fonction pure vis-à-vis du DOM.
- **visuels / rendu** : `planoSVG()` (blocs ou photos), `exportPNG()`.
- **analyse IA** : `runAI()` passe par `claude.use('sample')` dans un artifact Claude, ou par l'API Claude (clé locale ou serveur relais `prototype/pwa/netlify/functions/analyse.mjs`). Prompt : `buildPrompt(W,H)`, cadres demandés **en pixels** puis normalisés (`fitDims()` fixe la taille d'image envoyée).
- **étapes d'interface** : `renderFixture`, `renderPhoto`, `renderCatalog` (étape « Chiffres »), `renderDims`, `renderPlan`, `renderReport`. Les rendus déclenchés pendant un `change`/`blur` sont différés (`deferIfChange`) : conserver ce mécanisme.

Contraintes de l'artifact Claude (si la page doit rester publiable comme artifact) : un seul fichier, scripts externes uniquement depuis cdnjs/jsdelivr/unpkg, polices Google Fonts, pas de `fetch` vers d'autres sites, pas d'`alert/confirm/prompt`, thème clair/sombre par jetons CSS.

## Tests

- `python tests/e2e/test_parcours.py` : 39 contrôles sur le parcours complet (mobilier, import, photo, échec IA sans débit, analyse, corrections, dimensions, 13 combinaisons de plans avec vérification des contraintes, indices recalculés, exports, quota, persistance, mobile 390 px, absence d'erreur JS). **Doit rester à 39/39** avant tout commit.
- Prérequis : `pip install -r tests/requirements.txt && playwright install chromium`.
- Tout nouveau comportement du moteur ou de l'interface s'accompagne d'un contrôle dans ce test, ou d'un test unitaire une fois le moteur extrait (voir feuille de route).

## Manière de travailler

- Petites modifications vérifiables, un sujet par commit, message en français à l'impératif (« Ajouter le poids au catalogue »).
- Avant de modifier le moteur : relire `docs/regles-merchandising.md` (règles du cours et leur traduction dans le code).
- Après toute modification de `prototype/rayonpilot.html` : relancer le test, puis `python scripts/build_pwa.py`.
- Décision technique structurante : ajouter un fichier dans `docs/decisions/` (format ADR court).
- Ne jamais committer de clé API, de données commerciales réelles de client, ni de photo non autorisée.
- Rester sous le budget du PRD (< 5 000 €) : signaler tout service payant avant de l'introduire.
