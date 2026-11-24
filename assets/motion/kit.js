/* Kit de motion da skill shorts-do-video-longo.
 *
 * Uma regra só: TUDO na página é função do tempo. Nada de setTimeout, transition ou animation de CSS,
 * nada que dependa do relógio de verdade. O renderizador chama Motion.ir(t) pra cada quadro e fotografa.
 * Assim o quadro 73 sai igual toda vez, e o motion casa com a fala no milésimo.
 *
 * O kit é caixa de ferramentas, não molde: ele não decide o visual de nada. O desenho, o estilo e o
 * movimento de cada motion são escritos pra aquele momento do vídeo.
 *
 * Uso mínimo:
 *   Motion.config({dur: 6.4});
 *   Motion.quadro(t => { caixa.style.opacity = Motion.faixa(t, 0.2, 0.7, Motion.ease.fora); });
 *
 * Com GSAP (opcional, carregado do cdnjs): monte uma timeline pausada e chame Motion.gsap(tl).
 */
(function () {
  const M = (window.Motion = { fps: 30, dur: 5, _cenas: [], _sfx: [], _seq: [], _gsap: null });

  M.config = (o) => Object.assign(M, o);
  M.quadro = (fn) => M._cenas.push(fn);
  M.gsap = (tl) => { M._gsap = tl; tl.pause(); M.dur = M.dur || tl.duration(); };

  // ---------- curvas ----------
  const c = (x) => Math.min(1, Math.max(0, x));
  M.ease = {
    linear: (x) => x,
    fora: (x) => 1 - Math.pow(1 - x, 3),                 // chega desacelerando (entrada padrão)
    fora5: (x) => 1 - Math.pow(1 - x, 5),                // chega e assenta bem suave
    dentro: (x) => x * x * x,                            // sai acelerando (saída padrão)
    dentroFora: (x) => (x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2),
    volta: (x) => { const k = 1.70158; return 1 + (k + 1) * Math.pow(x - 1, 3) + k * Math.pow(x - 1, 2); }, // passa um pouco e volta
    mola: (x) => 1 - Math.exp(-6.5 * x) * Math.cos(11 * x),  // balança e para
  };
  /** progresso de 0 a 1 entre os tempos a e b, com curva */
  M.faixa = (t, a, b, ease) => (ease || M.ease.linear)(c((t - a) / Math.max(1e-6, b - a)));
  /** mistura dois valores */
  M.mix = (v0, v1, p) => v0 + (v1 - v0) * p;
  /** sobe de 0 a 1 em [a, a+dIn] e volta a 0 em [b-dOut, b]: presença de um elemento na tela */
  M.janela = (t, a, b, dIn = 0.45, dOut = 0.3) =>
    Math.min(M.faixa(t, a, a + dIn, M.ease.fora), 1 - M.faixa(t, b - dOut, b, M.ease.dentro));

  // ---------- ajudantes de elemento (use os que servirem; escreva os seus) ----------
  /** entrada com subida, desfoque e opacidade; saída opcional em `ate` */
  M.entra = (el, t, t0, o = {}) => {
    const { dur = 0.55, dy = 36, dx = 0, blur = 14, escala = 1, ate = null, ease = M.ease.fora5 } = o;
    let p = M.faixa(t, t0, t0 + dur, ease);
    if (ate !== null) p = Math.min(p, 1 - M.faixa(t, ate - 0.3, ate, M.ease.dentro));
    el.style.opacity = p;
    el.style.transform = `translate(${dx * (1 - p)}px, ${dy * (1 - p)}px) scale(${M.mix(escala, 1, p)})`;
    el.style.filter = blur ? `blur(${blur * (1 - p)}px)` : '';
    return p;
  };
  /** parte o texto de um elemento em spans (por 'letra' ou 'palavra') e devolve a lista */
  M.parte = (el, modo = 'palavra') => {
    const txt = el.textContent; el.textContent = '';
    const pedacos = modo === 'letra' ? [...txt] : txt.split(/(\s+)/);
    return pedacos.map((p) => {
      if (/^\s+$/.test(p)) { el.appendChild(document.createTextNode(p)); return null; }
      const s = document.createElement('span'); s.textContent = p; s.style.display = 'inline-block';
      s.style.willChange = 'transform, opacity, filter'; el.appendChild(s); return s;
    }).filter(Boolean);
  };
  /** aplica fn(el, tLocal, i) em cada item com atraso crescente */
  M.escalona = (els, t, t0, passo, fn) => [...els].forEach((el, i) => fn(el, t - (t0 + i * passo), i));
  /** número que conta de `de` até `ate` */
  M.conta = (el, t, t0, dur, de, ate, o = {}) => {
    const { casas = 0, antes = '', depois = '', ease = M.ease.fora5 } = o;
    const v = M.mix(de, ate, M.faixa(t, t0, t0 + dur, ease));
    el.textContent = antes + v.toLocaleString('pt-BR', { minimumFractionDigits: casas, maximumFractionDigits: casas }) + depois;
  };
  /** desenha um traço de SVG (path, line, polyline) de 0 a 100% */
  M.traca = (path, t, t0, dur, ease = M.ease.dentroFora) => {
    const L = path.__L || (path.__L = path.getTotalLength());
    const p = M.faixa(t, t0, t0 + dur, ease);
    path.style.strokeDasharray = L; path.style.strokeDashoffset = L * (1 - p);
    return p;
  };
  /** ponto {x, y} a uma fração p do caminho: pra bolinha que viaja numa linha */
  M.noCaminho = (path, p) => { const L = path.__L || (path.__L = path.getTotalLength()); return path.getPointAtLength(L * c(p)); };
  /** texto que se digita */
  M.digita = (el, t, t0, porSegundo = 28) => {
    const cheio = el.__txt || (el.__txt = el.textContent);
    el.textContent = cheio.slice(0, Math.max(0, Math.floor((t - t0) * porSegundo)));
  };
  /** ruído suave e repetível (respiração, flutuar): devolve de -1 a 1 */
  M.onda = (t, periodo = 4, fase = 0) => Math.sin((2 * Math.PI * t) / periodo + fase);

  // ---------- gravações reais dentro do motion ----------
  /** <img data-seq="tela"> mostra o quadro certo da sequência quadros/tela/00001.jpg ... a cada instante.
   *  data-inicio="1.5" desloca: a sequência começa a tocar 1.5 s depois do início do motion. */
  M._prepSeq = () => {
    M._seq = [...document.querySelectorAll('img[data-seq]')].map((img) => ({
      img, nome: img.dataset.seq, inicio: parseFloat(img.dataset.inicio || '0'),
      total: (window.MOTION_DADOS && window.MOTION_DADOS.quadros && window.MOTION_DADOS.quadros[img.dataset.seq]) || 1,
    }));
  };

  // ---------- som ----------
  /** marca um efeito sonoro no tempo t. tipos sintetizados (sem crédito): 'vuush', 'pop', 'tique', 'plim', 'subida', 'baque'.
   *  `tipo` também pode ser o caminho de um som gravado ('../../material/audio/vuush.mp3'); aí `extra` aceita
   *  {corte: segundos de silêncio a pular no começo do arquivo, dur: tamanho máximo}.
   *  O renderizador monta a pista e a montagem mistura com a fala. */
  M.sfx = (t, tipo, volume = 1, extra = {}) => M._sfx.push({ t, tipo, volume, ...extra });

  // ---------- o que o renderizador chama ----------
  M.ir = async (t) => {
    const esperas = [];
    for (const s of M._seq) {
      const n = Math.min(s.total, Math.max(1, Math.floor((t - s.inicio) * M.fps + 1e-6) + 1));
      const src = `quadros/${s.nome}/${String(n).padStart(5, '0')}.jpg`;
      if (s.img.getAttribute('src') !== src) { s.img.setAttribute('src', src); esperas.push(s.img.decode().catch(() => {})); }
    }
    if (M._gsap) M._gsap.seek(t, false);
    for (const fn of M._cenas) fn(t);
    await Promise.all(esperas);
    return true;
  };
  M.pronto = async () => {
    M._prepSeq();
    if (document.fonts && document.fonts.ready) await document.fonts.ready;
    await M.ir(0);
    return { dur: M.dur, fps: M.fps, sfx: M._sfx };
  };
})();
