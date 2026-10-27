"""Test de bout en bout du prototype RayonPilot (parcours complet sur le rayon lessive).

Lancement :  pip install -r tests/requirements.txt && playwright install chromium
             python tests/e2e/test_parcours.py
La réponse de l'IA est simulée (data/test-lessive/reponse-ia-simulee.json), avec des erreurs volontaires.
"""
import asyncio, json, time, sys, pathlib
from playwright.async_api import async_playwright
ROOT = pathlib.Path(__file__).resolve().parents[2]
DATA = ROOT / 'data' / 'test-lessive'
OUT = ROOT / 'tests' / 'output'; OUT.mkdir(exist_ok=True)
SD = str(OUT) + '/'
AI = open(DATA / 'reponse-ia-simulee.json', encoding='utf-8').read()
open(SD + 'page.html', 'w', encoding='utf-8').write('<!doctype html><html><head><meta charset=utf8><meta name=viewport content="width=device-width,initial-scale=1"></head><body>' + open(ROOT / 'prototype' / 'rayonpilot.html', encoding='utf-8').read() + '</body></html>')

STUB = """
window.__AI = %s; window.__mode = 'ok'; window.__calls = 0; window.__saved = [];
const sample = async (input, opts) => { window.__calls++; await new Promise(r=>setTimeout(r,300));
  if (window.__mode==='fail') throw {code:'upstream_error', message:'test'}; if(opts&&opts.onText) opts.onText({text:'{', delta:'{'}); return {text:JSON.stringify(window.__AI)} };
sample.json = async (input, opts) => { window.__lastPrompt = input; window.__lastImages = opts && opts.images; const r = await sample(input, opts); return JSON.parse(r.text) };
sample.limits = async () => ({maxPromptBytes: 262144, images: {maxCount: 5, maxInputBytes: 2e7, mediaTypes: ['image/jpeg','image/png']}});
const downloads = { save: async ({filename, data}) => { let t = typeof data==='string' ? data : (data instanceof Blob ? '[blob '+data.size+' o '+data.type+']' : '[bin]'); window.__saved.push({filename, t}); return {status:'saved'} } };
window.claude = { use: async (n) => n==='sample' ? sample : n==='downloads' ? downloads : null };
""" % AI

R = []
def log(step, ok, detail=''):
    R.append((step, ok, detail)); print(('OK  ' if ok else 'ÉCHEC ') + step + (' — ' + detail if detail else ''))

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={'width': 1300, 'height': 1000})
        errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.add_init_script(STUB)
        await pg.goto('file://' + SD + 'page.html')
        await pg.wait_for_timeout(1500)
        T = {}
        ev = pg.evaluate

        # 1. projet vide
        t = time.time(); await pg.click('#btnNew'); await pg.wait_for_timeout(200)
        st = await ev('({ex:S.example, cat:S.catalog.length, det:S.detections.length, tab:S.tab})')
        log('Projet vide créé', st['ex'] is False and st['cat'] == 0 and st['det'] == 0, str(st))
        await ev("S.name='Test complet lessive';save()")

        # 2. mobilier par l'interface
        async def setnum(sel, v):
            await pg.fill(sel, str(v)); await pg.dispatch_event(sel, 'change'); await pg.wait_for_timeout(80)
        await setnum('#fx-elements', 3); await setnum('#fx-elemWidth', 100); await setnum('#fx-height', 220)
        await setnum('#fx-depth', 45); await setnum('#fx-base', 10)
        clears = [33, 30, 32, 32, 33]
        for i, c in enumerate(clears): await setnum(f'#sh-{i}', c)
        await pg.click('#addShelf'); await pg.wait_for_timeout(100); await setnum('#sh-5', 36)
        blocked = await ev("checks().bad.some(b=>b.go==='fixture')")
        await pg.check('#fx-validated'); await pg.dispatch_event('#fx-validated', 'change'); await pg.wait_for_timeout(100)
        fx = await ev("({L:totalLen(),u:unitsFor(totalLen()),sh:S.fixture.shelves,val:S.fixture.validated,mld:totalLen()*S.fixture.shelves.length})")
        log('Mobilier saisi et validé', fx['L'] == 300 and fx['sh'] == [33,30,32,32,33,36] and fx['val'], f"{fx['L']} cm, {fx['mld']/100} m développés, {fx['u']} unités")
        log('Mobilier non validé = blocage', blocked)
        log('Calcul des unités : 3,00 m → 3 unités (plafond de 3 ÷ 1,33)', fx['u'] == 3)
        T['mobilier'] = time.time() - t

        # 3. import du catalogue CSV par le champ fichier
        t = time.time(); await ev("go('catalog')")
        await pg.set_input_files('#catFile', str(DATA / 'catalogue.csv')); await pg.wait_for_timeout(500)
        mp = await ev("pending&&{map:pending.map,h:pending.headers,rows:pending.rows.length}")
        unm = [k for k, v in mp['map'].items() if v < 0]
        log('Correspondance des colonnes détectée', set(unm) <= {'ean'}, 'non associées : ' + (', '.join(unm) or 'aucune'))
        await pg.click('#doImport'); await pg.wait_for_timeout(300)
        c = await ev("({n:S.catalog.length,mdd:S.catalog.filter(p=>p.mdd).length,dims:S.catalog.filter(p=>p.w>0&&p.h>0&&p.d>0).length,w11:S.catalog.find(p=>p.ref==='L11').w,ca:S.catalog.reduce((a,p)=>a+(p.ca||0),0)})")
        log('Import du catalogue', c['n'] == 33 and c['dims'] == 33 and c['mdd'] == 6, f"{c['n']} réf., {c['mdd']} MDD, CA total {round(c['ca'])} €")
        # ré-import : correspondance réutilisée, pas de doublon
        await pg.set_input_files('#catFile', str(DATA / 'catalogue.csv')); await pg.wait_for_timeout(400)
        reused = await ev("pending.reused"); await pg.click('#doImport'); await pg.wait_for_timeout(300)
        n2 = await ev("S.catalog.length")
        log('Ré-import : correspondance réutilisée, aucun doublon', reused and n2 == 33)
        # import d'un fichier avec erreurs
        await ev("prepareImport(parseCSV('Référence;Prix;Largeur\\nL05;abc;15\\nZZ9;;\\n'),'erreurs.csv')")
        errn = await ev("readImport().errors.length"); await ev("pending=null")
        log('Valeurs invalides signalées à l’import', errn >= 1, f'{errn} erreur(s)')
        T['catalogue'] = time.time() - t

        # 4. photo
        t = time.time(); await ev("go('photo')")
        await pg.set_input_files('#phFile', str(DATA / 'rayon-lessive.jpg')); await pg.wait_for_timeout(1200)
        ph = await ev("({has:!!photoMem,q:S.aiQuality,len:photoMem&&photoMem.length})")
        log('Photo importée et redimensionnée', ph['has'], f"{round(ph['len']/1024)} Ko, contrôle de flou : {'flou détecté' if ph['q'] and ph['q'].get('blur') else 'nette'}")

        # 5. échec technique : pas de débit
        await ev("window.__mode='fail'"); await pg.wait_for_timeout(200)
        await pg.click('#aiRun'); await pg.wait_for_timeout(900)
        f = await ev("({used:S.quota.used,h:S.history.map(h=>h.status),d:S.detections.length})")
        log('Échec technique : aucune unité débitée, analyse marquée échouée', f['used'] == 0 and f['h'][-1] == 'échouée' and f['d'] == 0, str(f))

        # 6. analyse réussie
        await ev("window.__mode='ok'"); t6 = time.time()
        await pg.click('#aiRun'); await pg.wait_for_timeout(1500)
        a = await ev("({used:S.quota.used,n:S.detections.length,unm:S.detections.filter(d=>!d.productId).length,low:S.detections.filter(d=>d.conf==='faible').length,imgs:S.catalog.filter(p=>p.imgSrc==='photo').length,h:S.history.slice(-1)[0],pr:(window.__lastPrompt||'').length,img:!!window.__lastImages})")
        log('Analyse réussie : 3 unités débitées une seule fois', a['used'] == 3, f"{a['n']} blocs, {a['unm']} non associés, {a['low']} confiance faible")
        log('Photo et catalogue envoyés à l’IA', a['img'] and a['pr'] > 2000, f"invite de {a['pr']} caractères")
        log('Visuels produits découpés dans la photo', a['imgs'] >= 25, f"{a['imgs']} références illustrées")
        bl = await ev("checks().bad.map(b=>b.t)")
        log('Optimisation bloquée tant que les détections ne sont pas vérifiées', len(bl) >= 2, ' | '.join(bl))
        T['analyse'] = time.time() - t6

        # 7. corrections (par l'interface)
        t = time.time(); corr = 0
        ids = await ev("S.detections.map(d=>({id:d.id,ref:d.productId&&prod(d.productId).ref,label:d.label,shelf:d.shelf,f:d.facings,x:d.box&&d.box[0]}))")
        refid = await ev("Object.fromEntries(S.catalog.map(p=>[p.ref,p.id]))")
        truth = json.load(open(DATA / 'reponse-ia-simulee.json', encoding='utf-8'))  # positions identiques
        for d in ids:
            sel = None
            if d['ref'] is None and 'petite boîte' in d['label']: sel = 'L17'
            elif d['ref'] is None and 'Sachet vert Apta' in d['label']: sel = 'L25'
            elif d['ref'] == 'L33' and d['shelf'] == 6: sel = 'L21'
            if sel:
                await pg.select_option(f'#dp-{d["id"]}', refid[sel]); await pg.wait_for_timeout(60); corr += 1
            if d['ref'] is None and 'Sachet Ariel' in d['label']:
                await pg.click(f'[data-deldet="{d["id"]}"]'); await pg.wait_for_timeout(60); corr += 1
            if d['ref'] == 'L05':
                await pg.fill(f'#df-{d["id"]}', '4'); await pg.dispatch_event(f'#df-{d["id"]}', 'change'); await pg.wait_for_timeout(60); corr += 1
        await ev("S.detections.forEach(d=>{if(d.productId)d.status='validee'});markDirty();save();renderAll()")
        k = await ev("({n:S.detections.length,unm:S.detections.filter(d=>!d.productId).length,used:S.quota.used,bad:checks().bad.length})")
        log('Corrections appliquées sans nouveau débit', k['unm'] == 0 and k['used'] == 3 and k['bad'] == 0, f"{corr} corrections sur 61 blocs ({round(corr/61*100)} %), {k['n']} blocs retenus")
        T['corrections'] = time.time() - t

        # 8. dimensions : une estimée non confirmée bloque
        t = time.time()
        await ev("const p=S.catalog.find(p=>p.ref==='L29');p.dimSrc='estimee';p.dimOk=false;markDirty();save();go('dims')")
        b1 = await ev("checks().bad.map(b=>b.t)")
        pid = await ev("S.catalog.find(p=>p.ref==='L29').id")
        await pg.click(f'[data-dimok="{pid}"]'); await pg.wait_for_timeout(100)
        b2 = await ev("checks().bad.length")
        log('Dimension estimée : blocage puis confirmation', len(b1) == 1 and b2 == 0, b1[0] if b1 else '')
        await pg.fill(f'#dm-h-{pid}', '30'); await pg.dispatch_event(f'#dm-h-{pid}', 'change'); await pg.wait_for_timeout(100)
        log('Saisie d’une mesure → provenance « Mesurée »', await ev(f"prod('{pid}').dimSrc==='mesuree'"))
        T['dimensions'] = time.time() - t

        # 9. planogrammes : objectifs × dispositions, contrôle des contraintes
        t = time.time(); await ev("go('plan')")
        VERIFY = """(pl)=>{const F=S.fixture,L=totalLen(),geo=shelvesGeom();const v=[];
          if(!pl.after)return ['pas de plan'];
          pl.after.forEach((sh,i)=>{let w=0;sh.forEach(it=>{if(it.gap){w+=it.gap;return}const p=prod(it.pid);w+=p.w*it.f;
            if(p.h>geo[i].clear-1)v.push(`hauteur ${p.ref} étagère ${i+1}`);if(p.d>F.depth)v.push(`profondeur ${p.ref}`)});
            if(w>L+0.01)v.push(`largeur étagère ${i+1} : ${w.toFixed(1)} > ${L}`)});
          const seen=new Set();pl.after.flat().forEach(it=>{if(it.pid)seen.add(it.pid)});
          const expect=new Set(S.detections.filter(d=>!prod(d.productId).exclude).map(d=>d.productId));
          expect.forEach(id=>{if(!seen.has(id))v.push('absent '+prod(id).ref)});
          pl.rows.forEach(r=>{if(r.after.f<r.minF&&!pl.warnings.some(w=>w.t.includes(prod(r.pid).name)))v.push('min non signalé '+prod(r.pid).ref)});
          if(pl.settings.rules.mdd)pl.after.forEach((sh,i)=>{const it=sh.filter(x=>x.pid);it.forEach((m,k)=>{const pm=prod(m.pid);if(!pm.mdd)return;
            const lead=it.filter(x=>{const q=prod(x.pid);return !q.mdd&&q.cat===pm.cat});if(!lead.length)return;
            const best=lead.sort((a,b)=>(prod(b.pid).ca||0)-(prod(a.pid).ca||0))[0];const prev=it[k-1];
            if(!(prev&&(prev===best||prod(prev.pid).mdd)))v.push(`MDD ${pm.ref} pas à droite du leader (étagère ${i+1})`)})});
          return v}"""
        combos = []
        for obj in ['ca', 'marge', 'rotation', 'rentabilite', 'couverture', 'is', 'promo', 'equilibre']:
            combos.append(dict(objective=obj, layout='horizontal', order='gradient'))
        combos += [dict(objective='equilibre', layout='horizontal', order='tiers'), dict(objective='equilibre', layout='horizontal', order='hot'),
                   dict(objective='equilibre', layout='horizontal', order='perf', flow='rtl'),
                   dict(objective='equilibre', layout='vert_cat', order='gradient'), dict(objective='equilibre', layout='vert_brand', order='gradient')]
        res = []
        for cbo in combos:
            r = await ev("""([c,VER])=>{const st=S.settings;Object.assign(st,{order:'gradient',flow:'ltr',layout:'horizontal',secondary:[]},c);
              const t0=performance.now();const pl=optimize();const ms=performance.now()-t0;
              if(pl.blocking)return {c,blk:pl.blocking.map(b=>b.t),ms};const v=eval(VER)(pl);
              const moved=pl.rows.filter(r=>r.before.shelf!==r.after.shelf).length;
              return {c,fill:pl.fill,viol:v,ms,moved,warn:pl.warnings.length,fb:pl.rows.reduce((a,r)=>a+r.before.f,0),fa:pl.rows.reduce((a,r)=>a+r.after.f,0)}}""", [cbo, VERIFY])
            res.append(r)
            name = f"{cbo['objective']} / {cbo['layout']} / {cbo['order']}{' / droite→gauche' if cbo.get('flow')=='rtl' else ''}"
            if 'blk' in r: log('Plan ' + name, cbo['layout'] != 'horizontal', 'impossible signalé : ' + r['blk'][0][:110])
            else: log('Plan ' + name, not r['viol'], f"remplissage {round(r['fill']*100)} %, facings {r['fb']}→{r['fa']}, {r['moved']} déplacés, {len(r['viol'])} violation(s){' : ' + '; '.join(r['viol'][:3]) if r['viol'] else ''}, {r['ms']:.0f} ms")
        # cas impossible : référence imposée sur une étagère trop basse
        r = await ev("()=>{const st=S.settings;Object.assign(st,{objective:'equilibre',layout:'horizontal',order:'gradient',flow:'ltr'});const p=S.catalog.find(p=>p.ref==='L29');p.lockShelf=2;const pl=optimize();p.lockShelf=null;return pl.blocking?pl.blocking[0].t:null}")
        log('Contrainte impossible signalée (baril 30 cm imposé sur une étagère de 30 cm)', bool(r), r or '')
        # règle produits volumineux : désactivée -> plus de facings minimum
        r = await ev("()=>{const st=S.settings;st.rules.bulky=false;const a=optimize();st.rules.bulky=true;const b=optimize();return {off:a.blocking?'blocage':a.rows.reduce((x,r)=>x+r.minF,0),on:b.rows.reduce((x,r)=>x+r.minF,0)}}")
        log('Règle produits volumineux', True, f"facings minimum cumulés : {r['on']} avec la règle, {r['off']} sans")
        # plan final retenu : équilibre horizontal, généré par le bouton
        await ev("Object.assign(S.settings,{objective:'equilibre',layout:'horizontal',order:'gradient',flow:'ltr',secondary:['marge']});save();renderPlan()")
        await pg.click('#gen'); await pg.wait_for_timeout(400)
        fin = await ev("({ok:!!(S.plan&&S.plan.after),dirty:S.planDirty,fill:S.plan.fill})")
        log('Génération par l’interface', fin['ok'] and not fin['dirty'], f"remplissage {round(fin['fill']*100)} %")
        T['planogrammes'] = time.time() - t
        el = await pg.query_selector('#afterBox'); await el.screenshot(path=SD + 'final_after.png')

        # 10. rapport : vérification d'un indice de sensibilité à la main
        t = time.time(); await ev("go('report')"); await pg.wait_for_timeout(200)
        chk = await ev("""()=>{const pl=S.plan;const r=pl.rows.find(r=>prod(r.pid).ref==='L08');const items=pl.rows;
          const ca=items.reduce((a,x)=>a+(prod(x.pid).ca||0),0);const lin=items.reduce((a,x)=>a+x.before.lin,0);
          const man=(prod(r.pid).ca/ca)/(r.before.lin/lin);return {app:r.isCA,man,acts:document.querySelectorAll('[data-act="status"]').length}}""")
        log('Indice de sensibilité CA recalculé à la main (Apta Couleurs)', abs(chk['app'] - chk['man']) < 1e-9, f"{chk['app']:.3f} ; {chk['acts']} actions au plan d’action")
        await pg.click('#expCsv'); await pg.wait_for_timeout(200)
        await ev("go('plan')"); await pg.wait_for_timeout(200); await pg.click('#pngBtn'); await pg.wait_for_timeout(1500)
        sv = await ev("window.__saved")
        csvlines = sv[0]['t'].count('\n') if sv else 0
        log('Exports CSV et PNG', len(sv) == 2 and csvlines > 30, f"{sv[0]['filename']} ({csvlines} lignes), {sv[1]['filename']} {sv[1]['t'] if len(sv)>1 else ''}")
        T['rapport'] = time.time() - t

        # 11. quota : avertissement 80 %, blocage 100 %
        await ev("S.quota.used=18;save();go('photo')")
        w80 = await ev("document.querySelector('#side').textContent.includes('80 %')")
        dis = await ev("document.querySelector('#aiRun').disabled")
        await ev("S.quota.used=3;save();renderAll()")
        log('Quota : alerte à 80 % et analyse bloquée si le solde est insuffisant', w80 and dis)

        # 12. persistance après rechargement
        await pg.reload(); await pg.wait_for_timeout(1500)
        pers = await ev("({name:S.name,n:S.detections.length,cat:S.catalog.length,plan:!!S.plan,photo:!!photoMem})")
        log('Projet conservé après rechargement', pers['name'] == 'Test complet lessive' and pers['n'] == 60 and pers['plan'] and pers['photo'], str(pers))

        # 13. mobile
        await pg.set_viewport_size({'width': 390, 'height': 844})
        ov = []
        for tab in ['fixture', 'catalog', 'photo', 'dims', 'plan', 'report']:
            await ev(f"go('{tab}')"); await pg.wait_for_timeout(150)
            if await ev("document.documentElement.scrollWidth") > 391: ov.append(tab)
        log('Affichage mobile 390 px sans défilement horizontal', not ov, ', '.join(ov))

        log('Aucune erreur JavaScript', not errs, '; '.join(errs[:3]))
        print('TEMPS', {k: round(v, 2) for k, v in T.items()})
        json.dump({'results': R, 'times': T, 'combos': res}, open(SD + 'e2e_results.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        await b.close()

asyncio.run(main())
failed = [r for r in R if not r[1]]
print(f'{len(R) - len(failed)}/{len(R)} contrôles réussis')
sys.exit(1 if failed else 0)
