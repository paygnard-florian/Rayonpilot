"""Reconstruit prototype/pwa/index.html à partir de prototype/rayonpilot.html."""
import os, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]
D=str(ROOT/'prototype'/'pwa')
html=open(D+'/index.html',encoding='utf-8').read()
head=html[:html.index('<body>')+len('<body>\n')]
tail=html[html.index("\n<script>if('serviceWorker'"):]
body=open(ROOT/'prototype'/'rayonpilot.html',encoding='utf-8').read()
open(D+'/index.html','w',encoding='utf-8').write(head+body+tail)
sw=open(D+'/sw.js',encoding='utf-8').read()
import re
sw=re.sub(r"const CACHE='rayonpilot-v\d+'","const CACHE='rayonpilot-v2'",sw)
# ne jamais mettre en cache les appels IA
sw=sw.replace("self.addEventListener('fetch',e=>{const r=e.request;if(r.method!=='GET')return;","self.addEventListener('fetch',e=>{const r=e.request;if(r.method!=='GET'||r.url.includes('/api/')||r.url.includes('anthropic.com'))return;")
open(D+'/sw.js','w',encoding='utf-8').write(sw)
os.makedirs(D+'/netlify/functions',exist_ok=True)
open(D+'/netlify/functions/analyse.mjs','w',encoding='utf-8').write("""// Serveur relais RayonPilot : garde la clé API côté serveur.
// Variables d'environnement Netlify : ANTHROPIC_API_KEY (obligatoire), RAYONPILOT_CODE (code d'accès, conseillé).
const MODELES = ['claude-sonnet-5-5', 'claude-opus-5-5', 'claude-haiku-5-5'];

export default async (req) => {
  if (req.method !== 'POST') return new Response('Méthode non autorisée', { status: 405 });
  const code = process.env.RAYONPILOT_CODE;
  if (code && req.headers.get('x-access-code') !== code) {
    return Response.json({ error: { type: 'authentication_error', message: 'Code d’accès incorrect.' } }, { status: 401 });
  }
  let body;
  try { body = await req.json(); } catch { return Response.json({ error: { type: 'invalid_request_error', message: 'JSON invalide.' } }, { status: 400 }); }
  const model = MODELES.includes(body.model) ? body.model : MODELES[0];
  const max_tokens = Math.min(Number(body.max_tokens) || 12000, 16000);
  const r = await fetch('https://api.anthropic.com/v1/messages', {
    method: 'POST',
    headers: { 'content-type': 'application/json', 'x-api-key': process.env.ANTHROPIC_API_KEY, 'anthropic-version': '2023-06-01' },
    body: JSON.stringify({ model, max_tokens, messages: body.messages })
  });
  return new Response(await r.text(), { status: r.status, headers: { 'content-type': 'application/json' } });
};

export const config = { path: '/api/analyse' };
""")
open(D+'/netlify.toml','w',encoding='utf-8').write("""[build]
  publish = "."

[functions]
  directory = "netlify/functions"
""")
open(D+'/LISEZ-MOI.txt','w',encoding='utf-8').write("""RayonPilot — version installable sur téléphone (application web)

1. Mettre l'application en ligne (gratuit)
   - Sur un ordinateur, ouvrez https://app.netlify.com/drop et créez un compte gratuit si besoin.
   - Glissez le dossier « rayonpilot-pwa » (décompressé) dans la page.
   - Netlify donne une adresse du type https://nom-au-hasard.netlify.app

2. Installer sur Android
   - Ouvrez l'adresse dans Chrome, menu ⋮, « Installer l'application » (ou « Ajouter à l'écran d'accueil »).
   - Sur iPhone : Safari, bouton Partager, « Sur l'écran d'accueil ».

3. Activer l'analyse IA (deux possibilités)

   A. Pour vous seul : clé API sur le téléphone (le plus simple)
      - Créez un compte sur https://platform.claude.com, ajoutez du crédit, créez une clé API (elle commence par sk-ant-).
      - Dans l'application : étape Photo, « Connecter l'IA », « Clé API sur cet appareil », collez la clé, Enregistrer.
      - La clé reste sur le téléphone. Ne partagez pas l'application ainsi configurée.

   B. Pour une équipe : serveur relais (la clé reste sur le serveur)
      - Le dossier contient une fonction Netlify (netlify/functions/analyse.mjs).
      - Le glisser-déposer peut ne pas publier les fonctions : déployez plutôt avec Netlify CLI
        (« npx netlify-cli deploy --prod » dans le dossier) ou depuis un dépôt GitHub relié à Netlify.
      - Dans Netlify, Site configuration > Environment variables, ajoutez :
          ANTHROPIC_API_KEY = votre clé
          RAYONPILOT_CODE   = un code d'accès que vous donnez à l'équipe
      - Dans l'application : « Connecter l'IA », « Serveur relais », adresse /api/analyse, code d'accès.

   Coût indicatif : quelques centimes par photo avec Sonnet 5.5 (le coût réel s'affiche après chaque analyse,
   et le journal des analyses en garde la trace).

Limites
   - Les projets sont enregistrés sur le téléphone uniquement.
   - Mise à jour : republiez le dossier au même endroit.
""")
print('pwa ok')
