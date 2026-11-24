/* Peças comuns das cenas. Carregue depois do kit.js.
 *  - Motion.ir novo: roda a cena e só carrega o quadro das gravações que estão em cena (as outras "dormem");
 *  - Palco.cartao: põe um cartão no lugar com entrada, respiração e saída;
 *  - Palco.camera: ele, mudando de tamanho entre estados;
 *  - Palco.legendas: legenda palavra por palavra, tirada da fala.
 * Tudo é função do tempo: nada de transition, animation ou setTimeout. */
(function () {
  const M = Motion, E = M.ease, mix = M.mix;
  const P = (window.Palco = {});
  const norm = (x) => x.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase().replace(/[^a-z0-9%]/g, '');

  // as fontes entram antes do primeiro quadro (texto escondido não puxa a fonte sozinho)
  P.fontes = Promise.all(['500', '600', '700', '800'].map((p) => document.fonts.load(`${p} 40px Montserrat`))).catch(() => {});
  const pronto0 = M.pronto;
  M.pronto = async () => { await P.fontes; return pronto0(); };

  M.ir = async (t) => {
    if (M._gsap) M._gsap.seek(t, false);
    for (const fn of M._cenas) fn(t);
    const esperas = [];
    const poe = (img, src) => { if (img.getAttribute('src') !== src) { img.setAttribute('src', src); esperas.push(img.decode().catch(() => {})); } };
    for (const s of M._seq) {
      if (s.img.dataset.dormindo === '1') continue;
      const n = Math.min(s.total, Math.max(1, Math.floor((t - s.inicio) * M.fps + 1e-6) + 1));
      poe(s.img, `quadros/${s.nome}/${String(n).padStart(5, '0')}.${s.img.dataset.ext || 'jpg'}`);
    }
    // quadro dirigido pela cena: <img data-dir="pasta" data-digitos="4">, e a cena escreve img.dataset.quadro a cada instante
    for (const img of document.querySelectorAll('img[data-dir]')) {
      if (img.dataset.dormindo === '1' || !img.dataset.quadro) continue;
      poe(img, `${img.dataset.dir}/${String(img.dataset.quadro).padStart(+(img.dataset.digitos || 5), '0')}.${img.dataset.ext || 'jpg'}`);
    }
    await Promise.all(esperas);
    return true;
  };

  P.entre = (a, b, p) => ({ x: mix(a.x, b.x, p), y: mix(a.y, b.y, p), w: mix(a.w, b.w, p), h: mix(a.h, b.h, p), r: mix(a.r || 0, b.r || 0, p) });
  P.caixa = (el, q, o = {}) => {
    const s = el.style;
    s.left = q.x + 'px'; s.top = q.y + 'px'; s.width = q.w + 'px'; s.height = q.h + 'px';
    if (q.r !== undefined) s.borderRadius = q.r + 'px';
    s.opacity = o.op === undefined ? 1 : o.op;
    s.transform = o.tf || '';
    s.filter = o.blur > 0.05 ? `blur(${o.blur.toFixed(2)}px)` : '';
  };

  /** Cartão em cena de t0 a t1. entrada: direita | esquerda | baixo | cima | zoom | fundo. saida: idem.
   *  Devolve a presença (0 a 1). `empurra` = zoom lento enquanto fica; `fase` varia a respiração de cada cartão. */
  P.cartao = (el, q, t, o) => {
    const dIn = o.dIn || 0.5, dOut = o.dOut || 0.32;
    const vivo = t >= o.t0 - 0.001 && (o.t1 === undefined || t < o.t1);
    const img = el.querySelector('img[data-seq]'); if (img) img.dataset.dormindo = vivo ? '0' : '1';
    if (!vivo) { el.style.visibility = 'hidden'; return 0; }
    el.style.visibility = 'visible';
    // entrada/saida 'nada' = troca seca, pra um cartão continuar exatamente onde o anterior estava
    const e = o.entrada === 'nada' ? 1 : M.faixa(t, o.t0, o.t0 + dIn, E.fora5);
    const s = o.t1 === undefined || o.saida === 'nada' ? 0 : M.faixa(t, o.t1 - dOut, o.t1, E.dentro);
    const f = o.fase || 0, fim = o.t1 === undefined ? o.t0 + 10 : o.t1;
    let tx = 0, ty = M.onda(t, 5.3, f + 1) * 4, rx = 2.0, ry = M.onda(t, 7.1, f) * 1.5;
    let sc = 1 + (o.empurra || 0) * M.faixa(t, o.t0, fim);
    const en = o.entrada || 'direita', sa = o.saida || 'esquerda';
    if (en === 'direita') { tx += (1 - e) * 210; ry -= (1 - e) * 28; sc *= mix(0.9, 1, e); }
    if (en === 'esquerda') { tx -= (1 - e) * 210; ry += (1 - e) * 28; sc *= mix(0.9, 1, e); }
    if (en === 'baixo') { ty += (1 - e) * 180; rx += (1 - e) * 22; sc *= mix(0.92, 1, e); }
    if (en === 'cima') { ty -= (1 - e) * 180; rx -= (1 - e) * 18; sc *= mix(0.92, 1, e); }
    if (en === 'zoom') { sc *= mix(1.18, 1, e); }
    if (en === 'fundo') { sc *= mix(0.76, 1, e); ty += (1 - e) * 46; }
    if (sa === 'esquerda') { tx -= s * 200; ry += s * 24; sc *= mix(1, 0.9, s); }
    if (sa === 'direita') { tx += s * 200; ry -= s * 24; sc *= mix(1, 0.9, s); }
    if (sa === 'cima') { ty -= s * 180; rx -= s * 14; sc *= mix(1, 0.9, s); }
    if (sa === 'baixo') { ty += s * 160; rx += s * 14; sc *= mix(1, 0.92, s); }
    if (sa === 'fundo') { sc *= mix(1, 0.78, s); ty -= s * 30; }
    const op = Math.min(o.entrada === 'nada' ? 1 : M.faixa(t, o.t0, o.t0 + dIn * 0.5), 1 - s) * (o.op === undefined ? 1 : o.op);
    P.caixa(el, q, { op, blur: (1 - e) * 16 + s * 10 + (o.blur || 0),
      tf: `perspective(1900px) translate3d(${tx.toFixed(2)}px, ${ty.toFixed(2)}px, 0) rotateX(${rx.toFixed(2)}deg) rotateY(${ry.toFixed(2)}deg) scale(${sc.toFixed(4)})` });
    return Math.min(e, 1 - s);
  };

  /** Ele: `estados` é uma lista [{t, q, foco}] de quadros-chave; entre um e outro a caixa desliza (dur antes de t). */
  P.camera = (el, t, chaves, dur = 0.5) => {
    let q = chaves[0].q, foco = chaves[0].foco || 56;
    for (let k = 1; k < chaves.length; k++) {
      const c = chaves[k], p = M.faixa(t, c.t - dur, c.t, E.dentroFora);
      if (p <= 0) break;
      q = P.entre(q, c.q, p); foco = mix(foco, c.foco || 56, p);
    }
    P.caixa(el, q, { tf: `translateY(${(M.onda(t, 6.1, 2) * 2.5).toFixed(2)}px)` });
    el.querySelector('img').style.objectPosition = `${foco.toFixed(2)}% 50%`;
    return q;
  };

  /** Legenda. palavras = [{p, i, f}] no tempo do Short. opções: destaques (laranja), mudos [[t0, t1]] (trechos em que
   *  outro texto da cena já diz a fala), max (palavras por grupo), chars, quebras [t, ...] (instantes de troca de cena, onde
   *  um grupo não pode atravessar). Devolve desenha(t, yCentro). */
  P.legendas = (palavras, o = {}) => {
    const destaques = new Set((o.destaques || []).map(norm)), mudos = o.mudos || [];
    const limpa = (p) => p.replace(/[.,;:!…]+$/, '');
    const ws = palavras.filter((w) => !mudos.some(([a, b]) => w.i >= a - 0.01 && w.i < b));
    const grupos = []; let g = [];
    for (const w of ws) {
      const ant = g[g.length - 1];
      const texto = g.map((x) => limpa(x.p)).concat(limpa(w.p)).join(' ');
      const troca = (o.quebras || []).some((q) => ant && ant.i < q - 0.001 && w.i >= q - 0.001);   // troca de cena: grupo novo
      if (ant && (troca || g.length >= (o.max || 3) || texto.length > (o.chars || 16) || w.i - ant.f > 0.42 || /[.?!]$/.test(ant.p)
                  || (/,$/.test(ant.p) && g.length >= 2))) { grupos.push(g); g = []; }
      g.push(w);
    }
    if (g.length) grupos.push(g);
    const raiz = document.getElementById('legendas');
    const gs = grupos.map((gr, k) => {
      const el = document.createElement('div'); el.className = 'leg';
      const miolo = document.createElement('i'); el.appendChild(miolo);
      const spans = gr.map((w) => { const s = document.createElement('span'); s.textContent = limpa(w.p);
        if (destaques.has(norm(w.p))) s.className = 'd'; miolo.appendChild(s); return s; });
      raiz.appendChild(el);
      const prox = grupos[k + 1];
      const ult = gr[gr.length - 1], corte = (o.quebras || []).filter((q) => q > ult.i + 0.001).sort((x, y) => x - y)[0];   // não atravessa a troca de cena
      return { el, miolo, spans, g: gr, i: gr[0].i, f: Math.min(ult.f + 0.5, prox ? prox[0].i : 1e9, corte === undefined ? 1e9 : Math.max(corte, ult.f + 0.08)), esc: 0 };
    });
    return (t, y, alfa = 1) => {
      for (const G of gs) {
        const on = t >= G.i - 0.05 && t < G.f && alfa > 0.01;
        G.el.style.display = on ? 'block' : 'none';
        if (!on) continue;
        if (!G.esc) G.esc = Math.min(1, 1000 / Math.max(1, G.miolo.offsetWidth));     // grupo largo demais encolhe pra caber
        G.el.style.top = (y - 37) + 'px'; G.el.style.transform = `scale(${G.esc})`;
        const some = (1 - M.faixa(t, G.f - 0.06, G.f)) * alfa;
        G.spans.forEach((s, k) => {
          const w = G.g[k], p = M.faixa(t, w.i - 0.05, w.i + 0.15, E.volta), a = M.faixa(t, w.i - 0.05, w.i + 0.04);
          s.style.opacity = a * some;
          s.style.transform = `translateY(${((1 - p) * 26).toFixed(2)}px) scale(${mix(0.8, 1, p).toFixed(4)})`;
          s.style.filter = a < 1 ? `blur(${((1 - a) * 8).toFixed(2)}px)` : '';
        });
      }
    };
  };

  /** Número grande que conta, com rótulo ao lado (faixa entre a tela e ele). */
  P.fato = (el, t, t0, t1) => {
    const e = M.faixa(t, t0, t0 + 0.5, E.fora5), s = M.faixa(t, t1 - 0.3, t1, E.dentro);
    el.style.opacity = Math.min(M.faixa(t, t0, t0 + 0.2), 1 - s);
    el.style.transform = `translateY(${((1 - e) * 46 - s * 24).toFixed(2)}px)`;
    el.style.filter = (1 - e) + s > 0.02 ? `blur(${((1 - e) * 14 + s * 8).toFixed(2)}px)` : '';
    return Math.min(e, 1 - s);
  };
})();
