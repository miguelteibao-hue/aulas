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
            dados.append('{n:"%s",t:"%s"}' % (nn, esc(f'{titulo} · {dur}')))
        bot_video = (f'<button class="bt cheio" data-parte="{nn}">▶ Ver o vídeo · {dur}</button>' if tem_video else '')
        linhas.append(
            f'<li class="parte" id="parte-{nn}"><span class="num">{int(nn) if nn != "01" else "1–3"}</span>'
            f'<span class="txt">{esc(titulo)}<small>{esc(quais)}</small></span>'
            f'<span class="acoes">{bot_video}'
            f'<a class="bt" href="apresentacao.html#d{d}">Abrir a apresentação</a></span></li>')
    leitor = '' if not dados else """
<div class="leitor" id="leitor" hidden><video id="video" controls playsinline preload="metadata"></video></div>
<div class="agora" id="agora" hidden><b id="titulo"></b><span><button class="bt" id="ant">◀ Anterior</button> <button class="bt" id="seg">Seguinte ▶</button></span></div>"""
    script = '' if not dados else """
<script>
const P = [%s];
const v = document.getElementById('video');
let atual = -1;
function abrir(i, tocar) {
  if (i < 0 || i >= P.length) return;
  atual = i;
  document.getElementById('leitor').hidden = false;
  document.getElementById('agora').hidden = false;
  v.src = 'videos/parte_' + P[i].n + '.mp4';
  document.getElementById('titulo').textContent = P[i].t;
  document.getElementById('ant').disabled = i === 0;
  document.getElementById('seg').disabled = i === P.length - 1;
  document.querySelectorAll('.parte').forEach(el => el.classList.toggle('sel', el.id === 'parte-' + P[i].n));
  try { history.replaceState(null, '', '#parte-' + P[i].n); } catch (e) {}
  if (tocar) { v.play().catch(() => {}); window.scrollTo({ top: 0, behavior: 'smooth' }); }
}
document.querySelectorAll('[data-parte]').forEach(b => b.addEventListener('click', () => abrir(P.findIndex(p => p.n === b.dataset.parte), true)));
document.getElementById('ant').onclick = () => abrir(atual - 1, true);
document.getElementById('seg').onclick = () => abrir(atual + 1, true);
v.addEventListener('ended', () => { if (atual < P.length - 1) abrir(atual + 1, false); });
const m = /^#parte-(\\d\\d)$/.exec(location.hash);
if (m) { const i = P.findIndex(p => p.n === m[1]); if (i >= 0) abrir(i, false); else document.getElementById('parte-' + m[1])?.scrollIntoView(); }
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
<h1>Isometrias</h1>
<p class="sub">Matemática · 8.º ano · escolhe a parte que queres ver</p>
{leitor}
<ul class="partes">
{chr(10).join(linhas)}
</ul>
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
    apresentacao_iso('--copiar' in args)
    with open(os.path.join(ISO, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(pagina_iso())
    with open(os.path.join(AQUI, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(pagina_raiz())
    print('Páginas de entrada refeitas.')


if __name__ == '__main__':
    main(sys.argv[1:])
