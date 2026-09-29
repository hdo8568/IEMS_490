"""Assemble pass 13 (clean look on the 30 faces): download, contact sheet, index JSON. Then build the PDF with build_catalogue_pdf.py."""
import json, os, urllib.request
from concurrent.futures import ThreadPoolExecutor
from PIL import Image
P = '/tmp/claude-0/-home-user-IEMS-490/76d8a8da-60ab-5cff-aaff-4a9af2d4536b/scratchpad/p13'
here = os.path.dirname(os.path.abspath(__file__))
plan = {p['index']: p['label'] for p in json.load(open(f'{P}/plan.json'))}
jobs = sorted([j for j in json.load(open(f'{P}/jobs.json')) if j.get('status') == 'completed' and j.get('result_url')], key=lambda j: j['index'])
print('completed', len(jobs), 'missing', sorted(set(plan) - {j['index'] for j in jobs}))
os.makedirs(f'{P}/img', exist_ok=True)
def f(j):
    fn = f"{P}/img/{j['index']:02d}.png"
    if not os.path.exists(fn): open(fn, 'wb').write(urllib.request.urlopen(j['result_url']).read())
list(ThreadPoolExecutor(8).map(f, jobs))
ims = [Image.open(f"{P}/img/{j['index']:02d}.png").convert('RGB').resize((300, 375)) for j in jobs]
rows = (len(ims) + 5) // 6; c = Image.new('RGB', (1800, 375 * rows), 'white')
for k, im in enumerate(ims): c.paste(im, (300 * (k % 6), 375 * (k // 6)))
c.save(f'{here}/essos_30faces_clean_contact_2026-09-29.jpg', quality=86)
json.dump([dict(id=j['job_id'], createdAt=0, model='gpt_image_2_5', ar='4:5', prompt=f"{j['index']}. {plan[j['index']]}", url=j['result_url'], ref=1) for j in jobs],
          open(f'{here}/essos_30faces_clean_2026-09-29.json', 'w'), indent=1)
print('ok')
