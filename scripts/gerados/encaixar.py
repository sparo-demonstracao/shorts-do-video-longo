"""Encaixa um trecho de um clipe gerado por cima de um video base (o som da base fica).
  python encaixar.py <base> <clipe> <saida> <de> <ate> <em> <dur> [imagem_final fundir_s]
de/ate: trecho do clipe (s); em: onde entra na base (s); dur: quanto dura na base (o clipe e acelerado pra caber).
imagem_final: imagem real pra onde o fim do clipe se funde nos ultimos fundir_s segundos."""
import subprocess
import sys

base, clipe, saida = sys.argv[1:4]
de, ate, em, dur = map(float, sys.argv[4:8])
img = sys.argv[8] if len(sys.argv) > 8 else None
fundir = float(sys.argv[9]) if len(sys.argv) > 9 else 0.3

fator = dur / (ate - de)
cmd = ["ffmpeg", "-y", "-v", "error", "-i", base, "-i", clipe]
fc = f"[1:v]trim={de}:{ate},setpts=(PTS-STARTPTS)*{fator:.6f},fps=30,scale=1080:1920:flags=lanczos,setsar=1[c];"
ult = "c"
if img:
    cmd += ["-loop", "1", "-t", f"{dur:.3f}", "-r", "30", "-i", img]
    fc += (f"[2:v]scale=1080:1920,format=yuva420p,fade=t=in:st={dur - fundir:.3f}:d={fundir:.3f}:alpha=1[s];"
           f"[c][s]overlay=0:0:shortest=1[c2];")
    ult = "c2"
fc += (f"[{ult}]setpts=PTS+{em}/TB[m];"
       f"[0:v][m]overlay=0:0:enable='between(t,{em},{em + dur:.3f})':eof_action=pass[v]")
cmd += ["-filter_complex", fc, "-map", "[v]", "-map", "0:a", "-c:v", "libx264", "-crf", "16", "-preset", "medium",
        "-pix_fmt", "yuv420p", "-c:a", "copy", saida]
r = subprocess.run(cmd, capture_output=True, text=True)
if r.returncode:
    sys.exit(r.stderr[-1500:])
print("feito", saida)
