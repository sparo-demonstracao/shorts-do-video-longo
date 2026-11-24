// Cole no javascript_tool do navegador do app, com uma aba aberta em youtube.com, trocando o ID do vídeo.
// Devolve título, duração, descrição e capítulos do vídeo publicado. Não baixa nada.
// A legenda automática do YouTube NÃO vem por aqui (o YouTube devolve vazio): a fala sai das gravações brutas.
const ID = 'TROQUE_PELO_ID';
const r = await fetch('https://www.youtube.com/watch?v=' + ID);
const t = await r.text();
const g = (re) => (t.match(re) || [])[1];
({
  titulo: g(/<title>(.*?) - YouTube<\/title>/),
  duracao_s: Number(g(/"lengthSeconds":"(\d+)"/)),
  publicado: g(/"publishDate":"(.*?)"/),
  views: Number(g(/"viewCount":"(\d+)"/)),
  descricao: (g(/"shortDescription":"(.*?)","isCrawlable/) || '').replace(/\\n/g, '\n').slice(0, 3000),
  capitulos: [...t.matchAll(/"chapterRenderer":\{"title":\{"simpleText":"(.*?)"\},"timeRangeStartMillis":(\d+)/g)]
    .map((x) => ({ inicio_s: Math.round(x[2] / 1000), titulo: x[1] })),
});
