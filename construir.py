#!/usr/bin/env python3
"""Site das aulas do Prof. Miguel Teibão (GitHub Pages, conta miguelteibao-hue, repositório «aulas").

Chapéu de PROFESSOR (AE D. Maria II), NÃO Da Vinci: nada de marca, domínio ou logótipo da Da Vinci aqui.
⚠ EXCEÇÃO (decisão do Miguel, 24/11/2026): /10/estatistica/ leva o logótipo Da Vinci — é a ficha das explicações
Da Vinci. SÓ essas páginas; o resto do site continua sem marca. O endereço /10/estatistica/ é o do QR da ficha e não muda
nunca (quando os recursos passarem para o painel, redireciona).
Endereço: https://miguelteibao-hue.github.io/aulas/

8.º ano, Isometrias (/8/isometrias/):
  - apresentacao.html = cópia de «apresentacao/publicar/iexplicacao_8/index.html» (a mesma do /8 do projetor);
  - videos/parte_NN.mp4 = os filmes com voz de «apresentacao/locucao/filmes/» (um por guião NN);
  - index.html = página de entrada GERADA aqui: uma linha por parte, com «Ver o vídeo» (só se o ficheiro existir)
    e «Abrir a apresentação» nesse tema. index.html#parte-NN abre logo essa parte.

    ~/Davinci/CODE/.venv/bin/python3 construir.py                 (refaz as páginas de entrada)
    ~/Davinci/CODE/.venv/bin/python3 construir.py --copiar        (copia antes a apresentação do 8.º; a cópia do site leva os botões «Todos os temas» e «▶ Vídeo deste tema»)
    ~/Davinci/CODE/.venv/bin/python3 construir.py --video 04 <ficheiro.mp4>   (põe o vídeo da parte 04)
    ~/Davinci/CODE/.venv/bin/python3 construir.py --video-vertical 04 <ficheiro.mp4>   (versão vertical: no telemóvel
        a página pergunta «Vertical / Horizontal» antes de tocar; no computador toca sempre o horizontal)
10.º ano, Estatística (/10/estatistica/, Explicações Da Vinci):
  - apresentacao.html + img/ = cópia de «SECUNDÁRIO/10º Ano/6 Estatística/apresentacao/publicar/site/» (gerada pelo
    construir.py dessa pasta);
  - index.html = uma linha por parte (01–04 capítulos, 05 exercícios finais, 06 teste final), com «▶ Vídeo — em breve»
    enquanto não houver vídeo e a âncora #teste (resolução do teste: é para lá que o QR leva quem quer as soluções).
    A apresentação aceita #parte-N e #teste (convertidos em #dN ao arrancar).

    ~/Davinci/CODE/.venv/bin/python3 construir.py --copiar-10     (copia antes a apresentação do 10.º, as imagens e o logótipo)
    ~/Davinci/CODE/.venv/bin/python3 construir.py --video-10 03 <ficheiro.mp4>   (vídeo da parte 03 do 10.º)

Depois: git add -A && git commit && git push (o GitHub Pages publica em ~1 min).
Espaço: o GitHub Pages aceita até 1 GB por site; o .git tinha 478 MB a 24/11/2026 (vídeos do 8.º).
Vídeos: só depois do OK do Miguel a cada um; máx. 100 MB por ficheiro (limite do GitHub).
"""
import html
import os
import shutil
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
ISO = os.path.join(AQUI, '8', 'isometrias')
APRES_8 = os.path.expanduser('~/Documents/AULAS/3º Ciclo/8º Ano/Isometrias 2026-27/apresentacao/publicar/iexplicacao_8/index.html')
EST = os.path.join(AQUI, '10', 'estatistica')
DIR_10 = os.path.expanduser('~/Documents/AULAS/SECUNDÁRIO/10º Ano/6 Estatística')
APRES_10 = os.path.join(DIR_10, 'apresentacao', 'publicar', 'site')   # index.html + img/
LOGO_10 = os.path.join(DIR_10, 'logo_davinci.jpg')

# NN do guião → (título, diapositivo onde começa na apresentação, 1 = capa)
PARTES_ISO = [
    ('01', 'Isometrias, rotação e reflexão', 'Temas 1 a 3', 2),
    ('04', 'Vetores', 'Tema 4', 8),
    ('05', 'Adição de vetores', 'Tema 5', 14),
    ('06', 'Translação associada a um vetor', 'Tema 6', 29),
    ('07', 'Composição de translações', 'Tema 7', 41),
    ('08', 'Reflexão deslizante', 'Tema 8', 49),
    ('09', 'Simetrias', 'Tema 9', 57),
    ('10', 'Frisos', 'Tema 10', 68),
    ('11', 'Revisão: que isometria foi?', 'Tema 11', 74),
    ('12', 'Resumo: o que conserva cada isometria', 'Tema 12', 77),
    ('13', 'Exercícios finais', 'Escolha múltipla e resposta aberta', 79),
]

# 10.º Estatística: NN → (título, o que tem, link na apresentação, número no círculo, âncora extra)
PARTES_EST = [
    ('01', 'Introdução à Estatística', 'Capítulo 1 · temas 1 a 4', 'apresentacao.html#parte-1', '1', ''),
    ('02', 'Dados univariados', 'Capítulo 2 · temas 5 a 9', 'apresentacao.html#parte-2', '2', ''),
    ('03', 'Medidas estatísticas', 'Capítulo 3 · temas 10 a 14', 'apresentacao.html#parte-3', '3', ''),
    ('04', 'Dados bivariados', 'Capítulo 4 · temas 15 e 16', 'apresentacao.html#parte-4', '4', ''),
    ('05', 'Exercícios finais', 'Escolha múltipla (1 a 24) e questões tipo exame (71 a 79)', 'apresentacao.html#parte-5', '5', ''),
    ('06', 'Teste final: resolução', 'Grupo I e Grupo II, passo a passo', 'apresentacao.html#teste', '6', 'teste'),
]

CSS = """
:root { --fundo:#f6f7fb; --cartao:#fff; --texto:#1d2433; --suave:#5b6478; --linha:#dfe3ec; --acento:#2457c5; --acento2:#e8eefb; }
@media (prefers-color-scheme: dark) { :root { --fundo:#12151c; --cartao:#1b2029; --texto:#e8ebf2; --suave:#9aa3b5; --linha:#2c3340; --acento:#7ea4f5; --acento2:#1f2a40; } }
* { box-sizing:border-box; }
[hidden] { display:none !important; }
body { margin:0; background:var(--fundo); color:var(--texto); font:17px/1.45 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif; }
main { max-width:760px; margin:0 auto; padding:20px 16px 48px; }
h1 { font-size:1.6rem; margin:.2rem 0 .1rem; }
.sub { color:var(--suave); margin:0 0 1.2rem; }
.leitor { background:#000; border-radius:12px; overflow:hidden; margin:0 0 .6rem; }
.leitor video { display:block; width:100%; aspect-ratio:16/9; background:#000; }
.agora { display:flex; gap:8px; align-items:center; justify-content:space-between; flex-wrap:wrap; margin:0 0 1.4rem; }
.agora b { font-size:1.05rem; }
.partes { list-style:none; margin:0; padding:0; display:grid; gap:10px; }
.parte { background:var(--cartao); border:1px solid var(--linha); border-radius:12px; padding:12px 14px; display:flex; gap:12px; align-items:center; }
.parte.sel { border-color:var(--acento); box-shadow:0 0 0 2px var(--acento2); }
.num { flex:none; width:2.2rem; height:2.2rem; border-radius:50%; background:var(--acento2); color:var(--acento); display:grid; place-items:center; font-weight:700; }
.txt { flex:1; min-width:0; }
.txt small { color:var(--suave); display:block; }
.acoes { display:flex; gap:8px; flex-wrap:wrap; justify-content:flex-end; }
.bt { border:1px solid var(--acento); color:var(--acento); background:transparent; border-radius:999px; padding:7px 13px; font:inherit; font-size:.92rem; text-decoration:none; cursor:pointer; white-space:nowrap; }
.bt.cheio { background:var(--acento); color:#fff; }
.bt[disabled] { opacity:.4; cursor:default; }
footer { color:var(--suave); font-size:.9rem; margin-top:2rem; }
@media (max-width:560px) { .parte { flex-wrap:wrap; } .acoes { width:100%; justify-content:flex-start; padding-left:3.2rem; } }
/* Pergunta «vertical ou horizontal» e leitor vertical em ecrã inteiro */
.escolha { position:fixed; inset:0; z-index:50; background:rgba(10,14,22,.55); display:grid; place-items:center; padding:16px; }
.esc-caixa { background:var(--cartao); color:var(--texto); border-radius:16px; padding:20px 18px 16px; width:min(360px,100%); display:grid; gap:10px; text-align:center; box-shadow:0 10px 40px rgba(0,0,0,.3); }
.esc-caixa b { font-size:1.15rem; }
.esc-caixa small { color:var(--suave); }
.esc-ops { display:grid; grid-template-columns:1fr 1fr; gap:12px; margin:6px 0 4px; }
.esc-op { display:grid; justify-items:center; gap:8px; padding:16px 8px 12px; border:2px solid var(--acento); border-radius:14px; background:var(--acento2); color:var(--acento); font:inherit; font-weight:700; cursor:pointer; }
.esc-op svg { height:64px; width:64px; fill:none; stroke:currentColor; stroke-width:3.5; stroke-linecap:round; }
.telav { position:fixed; inset:0; z-index:40; background:#000; display:flex; flex-direction:column; }
.telav video { flex:1; min-height:0; width:100%; object-fit:contain; background:#000; }
.telav-barra { display:flex; align-items:center; gap:8px; padding:8px 10px calc(8px + env(safe-area-inset-bottom)); background:#000; color:#fff; }
.telav-barra b { flex:1; font-size:.9rem; min-width:0; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }
.telav-barra .bt { padding:6px 12px; }
body.com-telav { overflow:hidden; }
/* Vertical (telemóvel): o vídeo fica preso no topo enquanto se percorre a lista */
.palco:not([hidden]) { position:sticky; top:0; z-index:5; background:var(--fundo); padding-top:8px; }
.palco .agora { margin:0 0 .8rem; }
/* Horizontal (telemóvel deitado e computador): vídeo à esquerda, capítulos à direita */
@media (orientation:landscape) and (min-width:700px) {
  main { max-width:1500px; }
  .grelha { display:grid; grid-template-columns:minmax(0,1fr) minmax(300px,380px); gap:20px; align-items:start; }
  .palco:not([hidden]) { position:sticky; top:12px; padding-top:0; }
  .leitor video { max-height:calc(100vh - 150px); }
  .partes { max-height:calc(100vh - 40px); overflow-y:auto; padding:2px 4px 2px 2px; position:sticky; top:12px; }
  .parte { flex-wrap:wrap; }
  .acoes { width:100%; justify-content:flex-start; padding-left:3.2rem; }
  .grelha.sem-video { display:block; }
}
/* Telemóvel deitado (pouca altura): tudo mais compacto para o vídeo caber */
@media (orientation:landscape) and (max-height:520px) {
  body { font-size:15px; }
  main { padding:8px 12px 16px; }
  h1 { font-size:1.15rem; display:inline; margin-right:.5rem; }
  .sub { display:inline; font-size:.85rem; }
  .cabeca { margin-bottom:6px; }
  .leitor { border-radius:8px; margin-bottom:.3rem; }
  .leitor video { max-height:calc(100vh - 70px); }
  .palco .agora { margin:0; }
  .agora b { font-size:.9rem; }
  .bt { padding:5px 10px; font-size:.85rem; }
  .grelha { grid-template-columns:minmax(0,1fr) 260px; gap:12px; }
  .partes { max-height:calc(100vh - 16px); top:8px; gap:6px; }
  .acoes { padding-left:0; }
  .parte { padding:8px 10px; gap:8px; }
  .num { width:1.8rem; height:1.8rem; font-size:.85rem; }
  .acoes { padding-left:2.6rem; }
  footer { display:none; }
}
"""


def esc(s):
    return html.escape(s, quote=True)


def duracao(caminho):
    """Duração do vídeo, lida no ficheiro (ffprobe), no formato «6 min 12 s»."""
    import subprocess
    r = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', caminho],
                       capture_output=True, text=True, check=True)
    s = round(float(r.stdout.strip()))
    return f'{s // 60} min {s % 60:02d} s' if s >= 60 else f'{s} s'


# PT/EN (só nas páginas com c['en']): o inglês aparece por baixo, em itálico; a escolha fica guardada na mesma chave
# da apresentação do 10.º («estat-en»), por isso a apresentação abre já com o inglês ligado.
BANDEIRA_UK = ('<svg class="bandeira" viewBox="0 0 60 30" aria-hidden="true"><clipPath id="bdc"><path d="M0,0v30h60V0z"/></clipPath>'
               '<clipPath id="bdt"><path d="M30,15h30v15zv15H0zH0V0zV0h30z"/></clipPath><g clip-path="url(#bdc)"><path d="M0,0v30h60V0z" fill="#012169"/>'
               '<path d="M0,0L60,30M60,0L0,30" stroke="#fff" stroke-width="6"/><path d="M0,0L60,30M60,0L0,30" clip-path="url(#bdt)" stroke="#C8102E" stroke-width="4"/>'
               '<path d="M30,0v30M0,15h60" stroke="#fff" stroke-width="10"/><path d="M30,0v30M0,15h60" stroke="#C8102E" stroke-width="6"/></g></svg>')
# bandeirinha (pedido do Miguel, 25/11): «English» liga o inglês; ligado mostra «PT + EN»
BOTAO_EN = '<button type="button" class="bt bt-en" id="bt-en" aria-pressed="false">' + BANDEIRA_UK + '<span id="bt-en-t">English</span></button>'
SCRIPT_EN = """<style>.en{display:none}body.lingua-en .en{display:block;font-style:italic;color:#5b6b7f;font-size:.86em;margin-top:2px}
.bt-en{margin-top:10px;display:inline-flex;align-items:center;gap:8px}.bandeira{width:30px;height:15px;border-radius:2px;box-shadow:0 0 0 1px rgba(0,0,0,.15)}body.lingua-en .bt-en{background:#0A687E;color:#fff;border-color:#0A687E}</style>
<script>(function(){var b=document.getElementById('bt-en');function por(on){document.body.classList.toggle('lingua-en',on);
b.setAttribute('aria-pressed',on?'true':'false');document.getElementById('bt-en-t').textContent=on?'PT + EN':'English';try{localStorage.setItem('estat-en',on?'1':'0')}catch(e){}}
var on=false;try{on=localStorage.getItem('estat-en')==='1'}catch(e){}por(on);b.addEventListener('click',function(){por(!document.body.classList.contains('lingua-en'))});})();</script>"""


def pagina_temas(c):
    """Página de entrada de um tema: uma linha por parte, com o vídeo (se existir) e o link para a apresentação.
    c = {dir, partes: [(nn, título, o que tem, link, número, âncora)], title, h1, sub, rodape, logo?, css?, em_breve?}"""
    linhas, dados = [], []
    for nn, titulo, quais, href, num, ancora in c['partes']:
        mp4 = os.path.join(c['dir'], 'videos', f'parte_{nn}.mp4')
        tem_video = os.path.exists(mp4)
        dur = duracao(mp4) if tem_video else ''
        if tem_video:
            tem_v = os.path.exists(os.path.join(c['dir'], 'videos', f'parte_{nn}_v.mp4'))
            dados.append('{n:"%s",t:"%s",v:%s}' % (nn, esc(f'{titulo} · {dur}'), 'true' if tem_v else 'false'))
        bot_video = (f'<button class="bt cheio" data-parte="{nn}">▶ Ver o vídeo · {dur}</button>' if tem_video else
                     ('<button class="bt" disabled>▶ Vídeo — em breve</button>' if c.get('em_breve') else ''))
        linhas.append(
            f'<li class="parte" id="parte-{nn}">' + (f'<span class="ancora" id="{ancora}"></span>' if ancora else '') +
            f'<span class="num">{esc(num)}</span>'
            f'<span class="txt">{esc(titulo)}<small>{esc(quais)}</small>'
            + (f'<span class="en">{esc(c["en"][nn][0])} · {esc(c["en"][nn][1])}</span>' if c.get('en') and nn in c['en'] else '') + '</span>'
            f'<span class="acoes">{bot_video}'
            f'<a class="bt" href="{href}">Abrir a apresentação</a></span></li>')
    leitor = '' if not dados else """
<section class="palco" id="palco" hidden>
<div class="leitor"><video id="video" controls playsinline preload="metadata"></video></div>
<div class="agora"><b id="titulo"></b><span><button class="bt" id="ant">◀ Anterior</button> <button class="bt" id="seg">Seguinte ▶</button></span></div>
</section>
<div class="escolha" id="escolha" hidden role="dialog" aria-modal="true" aria-labelledby="esc-tit">
 <div class="esc-caixa">
  <b id="esc-tit">Como queres ver o vídeo?</b>
  <small id="esc-parte"></small>
  <div class="esc-ops">
   <button type="button" class="esc-op" data-modo="v"><svg viewBox="0 0 40 64" aria-hidden="true"><rect x="3" y="2" width="34" height="60" rx="6"/><line x1="15" y1="55" x2="25" y2="55"/></svg>Vertical</button>
   <button type="button" class="esc-op" data-modo="h"><svg viewBox="0 0 64 40" aria-hidden="true"><rect x="2" y="3" width="60" height="34" rx="6"/><line x1="55" y1="15" x2="55" y2="25"/></svg>Horizontal</button>
  </div>
  <button type="button" class="bt" id="esc-nao">Cancelar</button>
 </div>
</div>
<div class="telav" id="telav" hidden>
 <video id="videov" controls playsinline preload="metadata"></video>
 <div class="telav-barra"><button type="button" class="bt cheio" id="antv">◀</button><b id="titulov"></b><button type="button" class="bt cheio" id="segv">▶</button><button type="button" class="bt cheio" id="fecharv" aria-label="Fechar">✕</button></div>
</div>"""
    script = '' if not dados else """
<script>
const P = [%s];
const v = document.getElementById('video');
let atual = -1;
function abrir(i, tocar) {
  if (i < 0 || i >= P.length) return;
  atual = i;
  document.getElementById('palco').hidden = false;
  v.src = 'videos/parte_' + P[i].n + '.mp4';
  document.getElementById('titulo').textContent = P[i].t;
  document.getElementById('ant').disabled = i === 0;
  document.getElementById('seg').disabled = i === P.length - 1;
  document.querySelectorAll('.parte').forEach(el => el.classList.toggle('sel', el.id === 'parte-' + P[i].n));
  try { history.replaceState(null, '', '#parte-' + P[i].n); } catch (e) {}
  if (tocar) { v.play().catch(() => {}); if (!matchMedia('(orientation:landscape) and (min-width:700px)').matches) window.scrollTo({ top: 0, behavior: 'smooth' }); }
}
/* Vídeo vertical: no telemóvel, se a parte tiver versão vertical, pergunta antes de tocar; no computador é sempre horizontal */
const vv = document.getElementById('videov'), telav = document.getElementById('telav'), esc = document.getElementById('escolha');
let atualV = -1, pedido = -1;
function telemovel() { return matchMedia('(pointer:coarse)').matches && Math.min(screen.width, screen.height) < 600; }
function vizV(i, d) { for (let k = i + d; k >= 0 && k < P.length; k += d) if (P[k].v) return k; return -1; }
function abrirV(i, tocar) {
  atualV = i; telav.hidden = false; document.body.classList.add('com-telav');
  v.pause(); vv.src = 'videos/parte_' + P[i].n + '_v.mp4';
  document.getElementById('titulov').textContent = P[i].t;
  document.getElementById('antv').disabled = vizV(i, -1) < 0;
  document.getElementById('segv').disabled = vizV(i, 1) < 0;
  document.querySelectorAll('.parte').forEach(el => el.classList.toggle('sel', el.id === 'parte-' + P[i].n));
  try { history.replaceState(null, '', '#parte-' + P[i].n); } catch (e) {}
  if (tocar) vv.play().catch(() => {});
}
function fecharV() { vv.pause(); telav.hidden = true; document.body.classList.remove('com-telav'); if (atualV >= 0) abrir(atualV, false); }
document.getElementById('antv').onclick = () => { const k = vizV(atualV, -1); if (k >= 0) abrirV(k, true); };
document.getElementById('segv').onclick = () => { const k = vizV(atualV, 1); if (k >= 0) abrirV(k, true); };
document.getElementById('fecharv').onclick = fecharV;
vv.addEventListener('ended', () => { const k = vizV(atualV, 1); if (k >= 0) abrirV(k, false); });
function pedir(i) {
  if (i < 0) return;
  if (P[i].v && telemovel()) { pedido = i; document.getElementById('esc-parte').textContent = P[i].t; esc.hidden = false; }
  else abrir(i, true);
}
esc.querySelectorAll('.esc-op').forEach(b => b.addEventListener('click', () => { esc.hidden = true; if (b.dataset.modo === 'v') abrirV(pedido, true); else abrir(pedido, true); }));
document.getElementById('esc-nao').onclick = () => { esc.hidden = true; };
esc.addEventListener('click', e => { if (e.target === esc) esc.hidden = true; });
document.querySelectorAll('[data-parte]').forEach(b => b.addEventListener('click', () => pedir(P.findIndex(p => p.n === b.dataset.parte))));
document.getElementById('ant').onclick = () => abrir(atual - 1, true);
document.getElementById('seg').onclick = () => abrir(atual + 1, true);
v.addEventListener('ended', () => { if (atual < P.length - 1) abrir(atual + 1, false); });
const m = /^#parte-(\\d\\d)$/.exec(location.hash);
let ini = 0;
if (m) { const i = P.findIndex(p => p.n === m[1]); if (i >= 0) ini = i; else document.getElementById('parte-' + m[1])?.scrollIntoView(); }
abrir(ini, false);   // abre já um vídeo (sem tocar), para a área do vídeo não ficar vazia
</script>""" % ','.join(dados)
    return f"""<!doctype html>
<html lang="pt-PT">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>{esc(c['title'])}</title>
<style>{CSS}{c.get('css', '')}</style>
</head>
<body>
<main>
<div class="cabeca">{c.get('logo', '')}<h1>{esc(c['h1'])}</h1>
<p class="sub">{esc(c['sub'])}{('<span class="en">' + esc(c['sub_en']) + '</span>') if c.get('sub_en') else ''}</p>{BOTAO_EN if c.get('en') else ''}</div>
<div class="grelha{'' if dados else ' sem-video'}">
{leitor}
<ul class="partes">
{chr(10).join(linhas)}
</ul>
</div>
<footer>{esc(c['rodape'])}</footer>
</main>
{script}{SCRIPT_EN if c.get('en') else ''}
</body>
</html>
"""


def pagina_iso():
    return pagina_temas({
        'dir': ISO, 'title': 'Isometrias · 8.º ano', 'h1': 'Isometrias', 'sub': 'Matemática · 8.º ano · escolhe a parte que queres ver',
        'rodape': 'Prof. Miguel Teibão · 2026/27',
        'partes': [(nn, t, q, f'apresentacao.html#d{d}', str(int(nn)) if nn != '01' else '1–3', '') for nn, t, q, d in PARTES_ISO]})


CSS_EST = """
.logo { display:inline-block; background:#fff; border-radius:10px; padding:6px 10px; margin:0 0 10px; }
.logo img { display:block; height:52px; width:auto; }
.ancora { position:absolute; margin-top:-24px; }   /* fora do fluxo: não empurra o número */
.parte:has(> .ancora:target) { border-color:var(--acento); box-shadow:0 0 0 2px var(--acento2); }
"""


def pagina_est():
    return pagina_temas({
        'dir': EST, 'title': 'Estatística · 10.º ano', 'h1': 'Estatística', 'sub': 'Matemática A · 10.º ano · escolhe a parte que queres ver',
        'rodape': 'Ginásios da Educação Da Vinci · Explicações · 2026/27', 'em_breve': True, 'css': CSS_EST,
        'logo': '<span class="logo"><img src="logo_davinci.jpg" alt="Ginásios da Educação Da Vinci"></span>',
        'partes': PARTES_EST, 'sub_en': 'Mathematics A · Year 10 · choose the part you want to see',
        'en': {'01': ('Introduction to Statistics', 'Chapter 1'), '02': ('Univariate data', 'Chapter 2'),
               '03': ('Statistical measures', 'Chapter 3'), '04': ('Bivariate data', 'Chapter 4'),
               '05': ('Final exercises', 'multiple choice and exam-style questions'),
               '06': ('Final test: solutions', 'step by step')}})


def pagina_raiz():
    return f"""<!doctype html>
<html lang="pt-PT">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>Aulas de Matemática</title>
<style>{CSS}</style>
</head>
<body>
<main>
<h1>Aulas de Matemática</h1>
<p class="sub">Prof. Miguel Teibão · 2026/27</p>
<ul class="partes">
<li class="parte"><span class="num">8.º</span><span class="txt">Isometrias<small>Vídeos e apresentação, por partes</small></span>
<span class="acoes"><a class="bt cheio" href="8/isometrias/">Abrir</a></span></li>
<li class="parte"><span class="num">10.º</span><span class="txt">Estatística<small>Apresentação por partes e resolução do teste</small></span>
<span class="acoes"><a class="bt cheio" href="10/estatistica/">Abrir</a></span></li>
</ul>
</main>
</body>
</html>
"""


def videos_iso():
    """Partes com vídeo publicado: {NN: duração}."""
    out = {}
    for nn, *_ in PARTES_ISO:
        mp4 = os.path.join(ISO, 'videos', f'parte_{nn}.mp4')
        if os.path.exists(mp4):
            out[nn] = duracao(mp4)
    return out


INI, FIM = '<!--SITE-VIDEOS-->', '<!--/SITE-VIDEOS-->'


PARTE_ISO_JS = """  function parte(id) {
    if (/^(em|ra)-/.test(id)) return '13';
    const m = /^t(\\d+)-/.exec(id || ''); if (!m) return null;
    const t = +m[1]; return t <= 3 ? '01' : String(t).padStart(2, '0');
  }"""
# 10.º: a parte de cada diapositivo é o seu «tema» (1 a 6) → '01' … '06'
PARTE_EST_JS = """  function parte(id) {
    const d = ((window.Apresentacao && window.Apresentacao._E.dias) || []).find(x => x.id === id);
    return d && /^[1-6]$/.test(d.tema) ? '0' + d.tema : null;
  }"""


def botoes_apresentacao(vid, parte_js=PARTE_ISO_JS, longo='Todos os temas', curto='Temas'):
    """Botões por cima da apresentação (SÓ na cópia do site; a do projetor e as gravações ficam como estão):
    à esquerda «Todos os temas» (página de entrada); à direita «▶ Vídeo deste tema · duração», só nos temas com vídeo."""
    import json
    return INI + """
<style>
.sv-bar { position:fixed; top:10px; left:10px; right:10px; display:flex; justify-content:space-between; gap:8px; z-index:2147483000; pointer-events:none; }
.sv-bt { pointer-events:auto; font:600 15px/1.2 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif; text-decoration:none; color:#fff; background:#194178; border-radius:999px; padding:8px 14px; box-shadow:0 2px 8px rgba(0,0,0,.18); white-space:nowrap; }
.sv-bt.sv-claro { color:#194178; background:rgba(255,255,255,.92); border:1px solid #194178; }
.sv-bt[hidden] { display:none !important; }
.sv-curto { display:none; }
@media (max-width:560px) { .sv-bt { font-size:13px; padding:7px 11px; } .sv-longo { display:none; } .sv-curto { display:inline; } }
body.vert #palco { --topo-vert: 130px; } /* apresentação na vertical (telemóvel em pé): o cabeçalho desce para a .sv-bar não o tapar */
/* Tela deitada (telemóvel deitado e computador): a apresentação desce para a barra ter faixa própria e não tapar o cabeçalho */
body:not(.vert) #app { top:52px; }
@media (orientation:landscape) and (max-height:500px) {
  body:not(.vert) #app { top:36px; }
  body:not(.vert) .sv-bar { top:4px; }
  body:not(.vert) .sv-bt { font-size:12px; padding:5px 10px; }
}
@media print { .sv-bar { display:none; } }
</style>
<div class="sv-bar"><a class="sv-bt sv-claro" href="index.html">☰ <span class="sv-longo">@@LONGO@@</span><span class="sv-curto">@@CURTO@@</span></a><a class="sv-bt" id="sv-video" hidden></a></div>
<script>
(function () {
  const VID = @@VID@@;
  const b = document.getElementById('sv-video');
@@PARTE@@
  let ultimo;
  function ver() {
    const E = window.Apresentacao && window.Apresentacao._E; if (!E || !E.dias) return;
    const p = parte(E.dias[E.i] && E.dias[E.i].id);
    if (p === ultimo) return; ultimo = p;
    if (p && VID[p]) { b.href = 'index.html#parte-' + p; b.innerHTML = '▶ <span class="sv-longo">Vídeo deste tema</span><span class="sv-curto">Vídeo</span> · ' + VID[p]; b.hidden = false; }
    else b.hidden = true;
  }
  document.querySelectorAll('.sv-bt').forEach(a => ['pointerdown', 'mousedown', 'click', 'keydown'].forEach(ev =>
    a.addEventListener(ev, e => e.stopPropagation())));
  setInterval(ver, 300); ver();
})();
</script>
""".replace('@@VID@@', json.dumps(vid, ensure_ascii=False)).replace('@@PARTE@@', parte_js).replace('@@LONGO@@', longo).replace('@@CURTO@@', curto) + FIM


def injetar(s, barra):
    """Põe (ou troca) a barra do site antes do </body>. Idempotente: antes, cada corrida juntava uma linha em branco."""
    if INI in s:
        resto = s[s.index(FIM) + len(FIM):]
        s = s[:s.index(INI)] + (resto[1:] if resto.startswith('\n') else resto)
    assert s.count('</body>') == 1
    return s.replace('</body>', barra + '\n</body>')


def apresentacao_iso(copiar):
    dest = os.path.join(ISO, 'apresentacao.html')
    s = open(APRES_8 if copiar else dest, encoding='utf-8').read()
    open(dest, 'w', encoding='utf-8').write(injetar(s, botoes_apresentacao(videos_iso())))


def videos_est():
    out = {}
    for nn, *_ in PARTES_EST:
        mp4 = os.path.join(EST, 'videos', f'parte_{nn}.mp4')
        if os.path.exists(mp4):
            out[nn] = duracao(mp4)
    return out


def apresentacao_est(copiar):
    dest = os.path.join(EST, 'apresentacao.html')
    if copiar:
        # Sincroniza (copia só o que mudou, apaga o que já não existe na origem). Apagar e voltar a copiar tudo
        # fazia o iCloud (a pasta Documentos está sincronizada) criar cópias «nome 3.webp» — 143 a 24/11/2026.
        img_o, img_d = os.path.join(APRES_10, 'img'), os.path.join(EST, 'img')
        os.makedirs(img_d, exist_ok=True)
        origem = set(os.listdir(img_o))
        for f in os.listdir(img_d):
            if f not in origem:
                os.remove(os.path.join(img_d, f))
        for f in origem:
            o, d = os.path.join(img_o, f), os.path.join(img_d, f)
            if not os.path.exists(d) or open(o, 'rb').read() != open(d, 'rb').read():
                shutil.copyfile(o, d)
        if not os.path.exists(os.path.join(EST, 'logo_davinci.jpg')):
            shutil.copyfile(LOGO_10, os.path.join(EST, 'logo_davinci.jpg'))
    if not os.path.exists(dest) and not copiar:
        return False
    s = open(os.path.join(APRES_10, 'index.html') if copiar else dest, encoding='utf-8').read()
    open(dest, 'w', encoding='utf-8').write(injetar(s, botoes_apresentacao(videos_est(), PARTE_EST_JS, 'Todas as partes', 'Partes')))
    return True


def main(args):
    if '--copiar' in args:
        print('Apresentação copiada da do projetor.')
    if '--video' in args:
        i = args.index('--video')
        nn, origem = args[i + 1], args[i + 2]
        assert nn in [p[0] for p in PARTES_ISO], f'parte desconhecida: {nn}'
        mb = os.path.getsize(origem) / 1e6
        assert mb < 95, f'{mb:.0f} MB: o GitHub recusa ficheiros com mais de 100 MB'
        shutil.copyfile(origem, os.path.join(ISO, 'videos', f'parte_{nn}.mp4'))
        print(f'Vídeo da parte {nn} posto ({mb:.1f} MB).')
    if '--video-vertical' in args:
        i = args.index('--video-vertical')
        nn, origem = args[i + 1], args[i + 2]
        assert nn in [p[0] for p in PARTES_ISO], f'parte desconhecida: {nn}'
        assert os.path.exists(os.path.join(ISO, 'videos', f'parte_{nn}.mp4')), 'publicar primeiro o vídeo horizontal desta parte'
        mb = os.path.getsize(origem) / 1e6
        assert mb < 95, f'{mb:.0f} MB: o GitHub recusa ficheiros com mais de 100 MB'
        shutil.copyfile(origem, os.path.join(ISO, 'videos', f'parte_{nn}_v.mp4'))
        print(f'Vídeo VERTICAL da parte {nn} posto ({mb:.1f} MB).')
    if '--video-10' in args:
        i = args.index('--video-10')
        nn, origem = args[i + 1], args[i + 2]
        assert nn in [p[0] for p in PARTES_EST], f'parte desconhecida: {nn}'
        mb = os.path.getsize(origem) / 1e6
        assert mb < 95, f'{mb:.0f} MB: o GitHub recusa ficheiros com mais de 100 MB'
        os.makedirs(os.path.join(EST, 'videos'), exist_ok=True)
        shutil.copyfile(origem, os.path.join(EST, 'videos', f'parte_{nn}.mp4'))
        print(f'Vídeo da parte {nn} do 10.º posto ({mb:.1f} MB).')
    apresentacao_iso('--copiar' in args)
    with open(os.path.join(ISO, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(pagina_iso())
    if apresentacao_est('--copiar-10' in args):
        with open(os.path.join(EST, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(pagina_est())
    with open(os.path.join(AQUI, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(pagina_raiz())
    print('Páginas de entrada refeitas.')


if __name__ == '__main__':
    main(sys.argv[1:])
