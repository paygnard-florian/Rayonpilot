# 0005 — Unités, quota et débit dans le prototype

Date : 26/10/2026 · Statut : accepté (simulation)

**Décision.** Unités = plafond(longueur ÷ 1,33 m). Quota de démonstration Pro (20 unités par mois) tenu localement : alerte à 80 %, blocage si le solde est insuffisant, débit après succès uniquement, une fois par analyse ; corrections gratuites ; échec technique noté « échouée » à 0 unité.

**Conséquences.** Comportement conforme au PRD §6.2–6.3, mais sans sécurité : au MVP, la réservation et le débit idempotent doivent se faire côté serveur.
