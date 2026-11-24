# -*- coding: utf-8 -*-
"""Grava um site real em formato de celular, quadro a quadro: desce a página
de pouquinho em pouquinho e fotografa cada posição em 1080x1920. Como o site reage à posição da rolagem, a cena pode
depois tocar esses quadros em qualquer velocidade, pra frente ou pra trás.
Uso: python gravar_site_vertical.py <endereço-do-site> <pasta-de-saida> [passo_em_px]"""
import json, os, sys
from playwright.sync_api import sync_playwright

url = sys.argv[1]; sai = sys.argv[2]; passo = int(sys.argv[3]) if len(sys.argv) > 3 else 12
os.makedirs(sai, exist_ok=True)
with sync_playwright() as pw:
    try:
        nav = pw.chromium.launch(channel='msedge', headless=True)
    except Exception:
        nav = pw.chromium.launch(headless=True)
    ctx = nav.new_context(viewport={'width': 540, 'height': 960}, device_scale_factor=2, is_mobile=True, has_touch=True)
    pag = ctx.new_page()
    pag.goto(url, wait_until='networkidle', timeout=90000)
    pag.wait_for_timeout(5000)
    alt = pag.evaluate('document.documentElement.scrollHeight'); fim = alt - 960
    ys = list(range(0, fim + 1, passo))
    for k, y in enumerate(ys):
        pag.evaluate('(y) => window.scrollTo(0, y)', y)
        pag.wait_for_timeout(110)                      # deixa a animação assentar naquela posição
        pag.screenshot(path=os.path.join(sai, f'{k + 1:04d}.jpg'), type='jpeg', quality=88)
        if k % 100 == 0:
            print(f'  {k}/{len(ys)} (y={y})', flush=True)
    nav.close()
json.dump({'quadros': len(ys), 'passo': passo, 'altura_da_pagina': alt, 'ys': ys}, open(os.path.join(sai, 'rolagem.json'), 'w'))
print(f'{len(ys)} quadros em {sai} (página de {alt} px, passo de {passo} px)')
