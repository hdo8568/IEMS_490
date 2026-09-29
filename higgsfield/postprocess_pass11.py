"""Deterministic post steps from the pass-11 review.
 - scenes: asymmetric corner darkening anchored to the light side, target far-corner/centre luminance ratio ~0.55
 - dim: pull the amber cast 25% toward neutral
Usage: python3 postprocess_pass11.py <p11_dir>
"""
import sys, os, json, numpy as np
from PIL import Image, ImageEnhance
P = sys.argv[1]; os.makedirs(f'{P}/post', exist_ok=True)

def lum(a): return 0.299*a[...,0]+0.587*a[...,1]+0.114*a[...,2]
def vignette(img, target=0.55):
    a = np.asarray(img.convert('RGB'), dtype=np.float32); h, w = a.shape[:2]
    L = lum(a); light_left = L[:, :w//2].mean() > L[:, w//2:].mean()
    ax = 0.30*w if light_left else 0.70*w; ay = 0.38*h            # anchor near the lit side, upper-middle
    yy, xx = np.mgrid[0:h, 0:w]
    d = np.sqrt(((xx-ax)/w)**2 + ((yy-ay)/h)**2); d = d/d.max()
    k = 1-target
    m = 1 - k*np.clip(d, 0, 1)**1.6
    out = np.clip(a*m[...,None], 0, 255).astype(np.uint8)
    Lo = lum(out.astype(np.float32)); c = Lo[int(.4*h):int(.6*h), int(.4*w):int(.6*w)].mean()
    corners = [Lo[:h//10,:w//10].mean(), Lo[:h//10,-w//10:].mean(), Lo[-h//10:,:w//10].mean(), Lo[-h//10:,-w//10:].mean()]
    return Image.fromarray(out), round(min(corners)/c, 2), round(max(corners)/c, 2)

SCENES = [59, 58, 63, 57, 55, 47, 50, 61, 33, 40]
rep = {}
for i in SCENES:
    im = Image.open(f'{P}/img/{i:02d}.png'); o, lo, hi = vignette(im)
    o.save(f'{P}/post/{i:02d}_dosed.png'); rep[i] = (lo, hi)
DIM = [65,66,68,69,70,72,73,74,77,78]
for i in DIM:
    im = Image.open(f'{P}/img/{i:02d}.png').convert('RGB')
    ImageEnhance.Color(im).enhance(0.75).save(f'{P}/post/{i:02d}_neutral.png')
print('corner/centre ratio (min,max) after dosing:', rep)
def sheet(files, cols, out):
    ims = [Image.open(f).convert('RGB').resize((300,375)) for f in files]
    rows = (len(ims)+cols-1)//cols; c = Image.new('RGB', (300*cols, 375*rows), 'white')
    for k, im in enumerate(ims): c.paste(im, (300*(k%cols), 375*(k//cols)))
    c.save(out, quality=86)
pairs = [f for i in SCENES[:5] for f in (f'{P}/img/{i:02d}.png', f'{P}/post/{i:02d}_dosed.png')]
sheet(pairs, 10, '/home/user/IEMS_490/higgsfield/essos_pass11_scenes_dosed_before_after_2026-09-29.jpg')
sheet([f'{P}/post/{i:02d}_dosed.png' for i in SCENES], 5, '/home/user/IEMS_490/higgsfield/essos_pass11_scenes_dosed_contact_2026-09-29.jpg')
sheet([f for i in DIM[:5] for f in (f'{P}/img/{i:02d}.png', f'{P}/post/{i:02d}_neutral.png')], 10, '/home/user/IEMS_490/higgsfield/essos_pass11_dim_neutral_before_after_2026-09-29.jpg')
