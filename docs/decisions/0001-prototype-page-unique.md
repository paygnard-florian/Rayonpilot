# 0001 — Prototype en une page HTML, puis PWA

Date : 26/10/2026 · Statut : accepté

**Contexte.** PRD §16.1 : choisir l'interface initiale. Il faut valider le parcours vite, sans serveur ni coût.

**Décision.** Prototype en une seule page HTML autonome (`prototype/rayonpilot.html`), publiée comme artifact Claude et déclinée en PWA installable (`prototype/pwa/`). Données dans le stockage local du navigateur.

**Conséquences.** Démontrable immédiatement sur ordinateur et téléphone, hors ligne en PWA. Pas de comptes, pas de synchronisation, pas d'isolation multi-organisation : à reprendre au MVP (Next.js + Supabase, Expo).
