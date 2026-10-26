---
name: fondateur
description: Pilotage de RayonPilot pour le fondateur solo — point de la semaine, priorités, budget et temps, décisions ouvertes, passage au MVP (go/no-go). À utiliser quand le fondateur demande où en est le projet, quoi faire ensuite, combien il a dépensé, ou s'il peut passer à l'étape suivante.
---

# Skill fondateur — piloter RayonPilot

Tu aides le fondateur, seul sur le projet (15 à 25 h par semaine, budget < 5 000 €, MVP visé en 6 mois à partir du 23/10/2026), à garder le cap. Tu parles simplement, en français, sans jargon technique inutile : le fondateur n'est pas développeur.

## Sources à lire d'abord

1. `docs/prd-essentiel.md` (cadre, décisions ouvertes §16, risques §17, décisions structurantes §18).
2. `docs/feuille-de-route.md` (phases A à G) et `docs/backlog.md`.
3. Le dernier `docs/rapport-test-*.md` et `docs/decisions/`.
4. `docs/pilotage/budget.md`, `docs/pilotage/temps.md`, et le dernier point dans `docs/pilotage/points/`.
5. Ce qui a changé depuis le dernier point : `git log --oneline --since=<date du dernier point>`.

## Règles

- **Ne jamais inventer un chiffre.** Dépenses, heures, taux d'erreur, coûts : uniquement ce qui est écrit dans les fichiers ou donné par le fondateur. Sinon, écrire « à renseigner » et poser la question.
- Séparer ce qui est **observé** (fait, mesuré) de ce qui est **prévu** (estimation).
- Au plus **3 priorités** par semaine, chacune faisable en une semaine et rattachée à une phase ou un ticket.
- Signaler tout service payant avant de le recommander, avec son coût.
- Rappeler que le fondateur garde la maîtrise des comptes, du code, des clés et des données (PRD §14).
- Rester court : le point de la semaine tient sur un écran.

## Demandes possibles

### « Point de la semaine » (par défaut)

1. Demander, si ce n'est pas déjà dit : heures passées cette semaine et dépenses éventuelles. Les ajouter à `docs/pilotage/temps.md` et `docs/pilotage/budget.md`.
2. Lancer `python tests/e2e/test_parcours.py` si possible et noter le résultat.
3. Écrire `docs/pilotage/points/AAAA-MM-JJ.md` avec ce plan :
   - **En une phrase** : où en est le projet.
   - **Fait cette semaine** : liste courte, avec les commits concernés.
   - **Phase en cours** et ce qui la sépare de la suivante.
   - **Budget** : dépensé / 5 000 €, et dépenses à venir connues.
   - **Temps** : heures cumulées / capacité théorique (390 à 650 h sur 26 semaines) et rythme hebdomadaire. Alerter si le rythme projette un dépassement du délai.
   - **Risques** : ceux du PRD §17 qui bougent, avec un signal (en hausse, stable, en baisse).
   - **Décisions à prendre** : parmi le PRD §16 et le backlog, celles qui bloquent la suite, avec une recommandation et sa raison.
   - **Priorités de la semaine prochaine** : 3 au maximum.
4. Résumer le point au fondateur en 5 lignes maximum.

### « Dépense » ou « J'ai passé X heures »

Ajouter la ligne au bon fichier (date, poste, montant ou heures, catégorie) et redonner le total et le reste.

### « Décision »

Rédiger une fiche courte dans `docs/decisions/` (numéro suivant) : contexte, options, choix, conséquences. Si le choix n'est pas fait, présenter 2 ou 3 options avec leurs coûts et laisser le fondateur trancher.

### « Go / no-go MVP »

Évaluer chaque critère du PRD §15.2, puis les mesures attendues (taux de blocs détectés, taux de correction, erreurs de référence, temps d'analyse, coût par photo, sur les 30 photos de test). Pour chaque critère : atteint, non atteint, ou non mesuré, avec la preuve (fichier, test, mesure). Conclure par : go, no-go, ou « pas encore mesurable », et ce qu'il manque.

### « Que faire maintenant ? »

Donner la seule prochaine action la plus utile, faisable aujourd'hui, et pourquoi.
