#!/usr/bin/env python3
"""Site das aulas do Prof. Miguel Teibão (GitHub Pages, conta miguelteibao-hue, repositório «aulas").

Chapéu de PROFESSOR (AE D. Maria II), NÃO Da Vinci: nada de marca, domínio ou logótipo da Da Vinci aqui.
Endereço: https://miguelteibao-hue.github.io/aulas/

Por agora só o 8.º ano, Isometrias (/8/isometrias/):
  - apresentacao.html = cópia de «apresentacao/publicar/iexplicacao_8/index.html» (a mesma do /8 do projetor);
  - videos/parte_NN.mp4 = os filmes com voz de «apresentacao/locucao/filmes/» (um por guião NN);
  - index.html = página de entrada GERADA aqui: uma linha por parte, com «Ver o vídeo» (só se o ficheiro existir)
    e «Abrir a apresentação» nesse tema. index.html#parte-NN abre logo essa parte.

    ~/Davinci/CODE/.venv/bin/python3 construir.py                 (refaz as páginas de entrada)
    ~/Davinci/CODE/.venv/bin/python3 construir.py --copiar        (copia antes a apresentação do 8.º; a cópia do site leva os botões «Todos os temas» e «▶ Vídeo deste tema»)
    ~/Davinci/CODE/.venv/bin/python3 construir.py --video 04 <ficheiro.mp4>   (põe o vídeo da parte 04)
    ~/Davinci/CODE/.venv/bin/python3 construir.py --video-vertical 04 <ficheiro.mp4>   (versão vertical: no telemóvel
        a página pergunta «Vertical / Horizontal» antes de tocar; no computador toca sempre o horizontal)
Depois: git add -A && git commit && git push (o GitHub Pages publica em ~1 min).
Vídeos: só depois do OK do Miguel a cada um; máx. 100 MB por ficheiro (limite do GitHub).
"""
import html
import os
import shutil
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
ISO = os.path.join(AQUI, '8', 'isometrias')
APRES_8 = os.path.expanduser('~/Documents/AULAS/3º Ciclo/8º Ano/Isometrias 2026-27/apresentacao/publicar/iexplicacao_8/index.html')

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


def pagina_iso():
    linhas, dados = [], []
    for nn, titulo, quais, d in PARTES_ISO:
        mp4 = os.path.join(ISO, 'videos', f'parte_{nn}.mp4')
        tem_video = os.path.exists(mp4)
        dur = duracao(mp4) if tem_video else ''
        if tem_video:
            tem_v = os.path.exists(os.path.join(ISO, 'videos', f'parte_{nn}_v.mp4'))
            dados.append('{n:"%s",t:"%s",v:%s}' % (nn, esc(f'{titulo} · {dur}'), 'true' if tem_v else 'false'))
        bot_video = (f'<button class="bt cheio" data-parte="{nn}">▶ Ver o vídeo · {dur}</button>' if tem_video else '')
        linhas.append(
            f'<li class="parte" id="parte-{nn}"><span class="num">{int(nn) if nn != "01" else "1–3"}</span>'
            f'<span class="txt">{esc(titulo)}<small>{esc(quais)}</small></span>'
            f'<span class="acoes">{bot_video}'
            f'<a class="bt" href="apresentacao.html#d{d}">Abrir a apresentação</a></span></li>')
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
<title>Isometrias · 8.º ano</title>
<style>{CSS}</style>
</head>
<body>
<main>
<div class="cabeca"><h1>Isometrias</h1>
<p class="sub">Matemática · 8.º ano · escolhe a parte que queres ver</p></div>
<div class="grelha{'' if dados else ' sem-video'}">
{leitor}
<ul class="partes">
{chr(10).join(linhas)}
</ul>
</div>
<footer>Prof. Miguel Teibão · 2026/27</footer>
</main>
{script}
</body>
</html>
"""


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


def botoes_apresentacao(vid):
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
@media print { .sv-bar { display:none; } }
</style>
<div class="sv-bar"><a class="sv-bt sv-claro" href="index.html">☰ <span class="sv-longo">Todos os temas</span><span class="sv-curto">Temas</span></a><a class="sv-bt" id="sv-video" hidden></a></div>
<script>
(function () {
  const VID = %s;
  const b = document.getElementById('sv-video');
  function parte(id) {
    if (/^(em|ra)-/.test(id)) return '13';
    const m = /^t(\\d+)-/.exec(id || ''); if (!m) return null;
    const t = +m[1]; return t <= 3 ? '01' : String(t).padStart(2, '0');
  }
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
""" % json.dumps(vid, ensure_ascii=False) + FIM


def apresentacao_iso(copiar):
    dest = os.path.join(ISO, 'apresentacao.html')
    s = open(APRES_8 if copiar else dest, encoding='utf-8').read()
    if INI in s:
        s = s[:s.index(INI)] + s[s.index(FIM) + len(FIM):]
    assert s.count('</body>') == 1
    s = s.replace('</body>', botoes_apresentacao(videos_iso()) + '\n</body>')
    open(dest, 'w', encoding='utf-8').write(s)


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
    apresentacao_iso('--copiar' in args)
    with open(os.path.join(ISO, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(pagina_iso())
    with open(os.path.join(AQUI, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(pagina_raiz())
    print('Páginas de entrada refeitas.')


if __name__ == '__main__':
    main(sys.argv[1:])
