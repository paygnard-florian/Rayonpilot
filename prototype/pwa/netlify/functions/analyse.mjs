// Serveur relais RayonPilot : garde la clé API côté serveur.
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
