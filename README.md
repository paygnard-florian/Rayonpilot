# RayonPilot

Aide au merchandising des rayons en libre-service : à partir d'une photo du rayon et des chiffres du magasin, RayonPilot relève les produits, vérifie les dimensions et propose un planogramme 2D qui respecte les contraintes physiques, avec un plan d'action.

Statut : **prototype démontrable** (phase E du PRD v2.0). Dépôt privé.

## Contenu

| Dossier | Rôle |
|---|---|
| `prototype/rayonpilot.html` | Le prototype, en une seule page (source de vérité). |
| `prototype/pwa/` | Version installable sur téléphone (application web), avec serveur relais IA optionnel. |
| `data/test-lessive/` | Jeu de test : photo d'un rayon lessive, catalogue de 33 références (chiffres inventés, poids nets lus sur les emballages), réponse IA simulée. |
| `tests/e2e/` | Test de bout en bout rejouable (40 contrôles). |
| `scripts/` | Reconstruction de la PWA. |
| `docs/` | PRD condensé, règles de merchandising, décisions, rapport de test, feuille de route, backlog. |

## Essayer le prototype

- Ouvrir `prototype/rayonpilot.html` dans un navigateur. L'analyse IA automatique ne fonctionne que dans Claude (artifact) ou avec une clé API dans la version installable ; sinon, relever les produits avec « Dessiner une détection ».
- Version téléphone : voir `prototype/pwa/LISEZ-MOI.txt`.

## Lancer les tests

```bash
pip install -r tests/requirements.txt
playwright install chromium
python tests/e2e/test_parcours.py
```

Les tests tournent aussi à chaque push (GitHub Actions, `.github/workflows/tests.yml`).

## Développer avec Claude Code

1. Installer Claude Code (inclus dans les formules Pro et Max) et ouvrir le dossier du dépôt : `claude`.
2. Claude Code lit automatiquement `CLAUDE.md` (contexte, règles produit, architecture, tests).
3. Optionnel : la boîte à outils ECC (agents de planification, revue, sécurité). D'après son README, dans Claude Code :
   ```
   /plugin marketplace add https://github.com/affaan-m/ECC
   /plugin install ecc@ecc
   ```
   L'installer uniquement depuis la source officielle.
4. Point de départ conseillé : les tickets « Prochaines étapes » de `docs/backlog.md`.

## Créer le dépôt GitHub

```bash
git remote add origin git@github.com:<votre-compte>/rayonpilot.git
git push -u origin main
```

Créer le dépôt en **privé** et activer l'authentification à deux facteurs sur le compte (PRD §14).
