"""Monta os videos de comparacao dos testes.
  python comparar.py lado <esq> <dir> <saida> "<rotulo esq>" "<rotulo dir>" [esq|dir]   (audio de qual lado)
  python comparar.py seq <saida> <arq1> "<rotulo1>" <arq2> "<rotulo2>" ...
Os rotulos sao so da comparacao; nao fazem parte do Short."""
import os
import subprocess
import sys

from PIL import Image, ImageDraw, ImageFont

FONTE = "C:/Windows/Fonts/segoeuib.ttf"
TMP = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tmp")
os.makedirs(TMP, exist_ok=True)


def rotulo(texto, larg, alt, nome, cor=(255, 255, 255)):
    im = Image.new("RGBA", (larg, alt), (12, 12, 14, 255))
    d = ImageDraw.Draw(im)
    tam = int(alt * 0.5)
    f = ImageFont.truetype(FONTE, tam)
    while d.textlength(texto, font=f) > larg - 40 and tam > 14:
        tam -= 2
        f = ImageFont.truetype(FONTE, tam)
    w = d.textlength(texto, font=f)
    d.text(((larg - w) / 2, (alt - tam) / 2 - tam * 0.12), texto, font=f, fill=cor)
    p = os.path.join(TMP, nome)
    im.save(p)
    return p


def tem_audio(arq):
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "a", "-show_entries", "stream=index", "-of", "csv=p=0", arq],
                       capture_output=True, text=True)
    return bool(r.stdout.strip())


def roda(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        sys.exit(r.stderr[-2000:])


def lado(esq, dire, saida, re, rd, audio="esq"):
    L, A, F = 720, 1280, 80
    pe = rotulo(re, L, F, "rot-e.png", (200, 200, 205))
    pd = rotulo(rd, L, F, "rot-d.png", (255, 170, 60))
    fc = (f"[0:v]fps=30,scale={L}:{A}:force_original_aspect_ratio=decrease,pad={L}:{A}:(ow-iw)/2:(oh-ih)/2,setsar=1[a];"
          f"[1:v]fps=30,scale={L}:{A}:force_original_aspect_ratio=decrease,pad={L}:{A}:(ow-iw)/2:(oh-ih)/2,setsar=1[b];"
          f"[2:v][a]vstack[ca];[3:v][b]vstack[cb];[ca][cb]hstack=shortest=1[v]")
    ia = 0 if audio == "esq" else 1
    roda(["ffmpeg", "-y", "-v", "error", "-i", esq, "-i", dire, "-loop", "1", "-i", pe, "-loop", "1", "-i", pd,
          "-filter_complex", fc, "-map", "[v]", "-map", f"{ia}:a", "-c:v", "libx264", "-crf", "18", "-preset", "medium",
          "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", saida])
    print("feito", saida)


def seq(saida, pares):
    L, A, F = 1080, 1920, 96
    partes = []
    for i, (arq, txt) in enumerate(pares):
        pr = rotulo(f"{i + 1}/{len(pares)}  {txt}", L, F, f"rot-s{i}.png", (255, 170, 60) if i else (200, 200, 205))
        sai = os.path.join(TMP, f"seq-{i}.mp4")
        cmd = ["ffmpeg", "-y", "-v", "error", "-i", arq, "-loop", "1", "-i", pr]
        if not tem_audio(arq):
            cmd += ["-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo"]
            ma = "2:a"
        else:
            ma = "0:a"
        fc = (f"[0:v]fps=30,scale={L}:{A}:force_original_aspect_ratio=decrease,pad={L}:{A}:(ow-iw)/2:(oh-ih)/2,setsar=1[a];"
              f"[a][1:v]overlay=0:0:shortest=1[v]")
        cmd += ["-filter_complex", fc, "-map", "[v]", "-map", ma, "-c:v", "libx264", "-crf", "18", "-preset", "medium",
                "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2", "-shortest", sai]
        roda(cmd)
        partes.append(sai)
    lista = os.path.join(TMP, "seq-lista.txt")
    open(lista, "w").write("".join(f"file '{p.replace(os.sep, '/')}'\n" for p in partes))
    roda(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lista, "-c:v", "libx264", "-crf", "18",
          "-preset", "medium", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", saida])
    print("feito", saida)


if __name__ == "__main__":
    if sys.argv[1] == "lado":
        lado(*sys.argv[2:8])
    else:
        a = sys.argv[3:]
        seq(sys.argv[2], list(zip(a[0::2], a[1::2])))
