"""Assemble pass-11 outputs: download every result, contact sheets per set, two PDFs (main + dim), JSON index.

Usage: python3 assemble_pass11.py <p11_dir> <date>
  p11_dir holds plan.json, test_result.json and jobs.json (from the generate workflow).
"""
import json, sys, os, io, urllib.request
from concurrent.futures import ThreadPoolExecutor
from PIL import Image

P, date = sys.argv[1], sys.argv[2]
here = os.path.dirname(os.path.abspath(__file__))
plan = {p['index']: p for p in json.load(open(f'{P}/plan.json'))}
jobs = json.load(open(f'{P}/test_result.json')) + json.load(open(f'{P}/jobs.json'))
jobs = {j['index']: j for j in jobs if j.get('status') == 'completed' and j.get('result_url')}
missing = sorted(set(plan) - set(jobs))
print('completed', len(jobs), 'missing', missing)

os.makedirs(f'{P}/img', exist_ok=True)
def fetch(i):
    fn = f'{P}/img/{i:02d}.png'
    if not os.path.exists(fn):
        open(fn, 'wb').write(urllib.request.urlopen(jobs[i]['result_url']).read())
    return i
list(ThreadPoolExecutor(8).map(fetch, sorted(jobs)))

def sheet(indices, cols, out):
    ims = [Image.open(f'{P}/img/{i:02d}.png').convert('RGB').resize((300, 375)) for i in indices]
    rows = (len(ims) + cols - 1) // cols
    c = Image.new('RGB', (300 * cols, 375 * rows), 'white')
    for k, im in enumerate(ims): c.paste(im, (300 * (k % cols), 375 * (k // cols)))
    c.save(out, quality=86); return out

sets = {s: [i for i in sorted(jobs) if plan[i]['set'] == s] for s in ('people', 'scenes', 'dim')}
for s, idx in sets.items():
    sheet(idx, 8 if s != 'dim' else 4, f'{here}/essos_pass11_{s}_contact_{date}.jpg')

def index_json(indices, fn):
    json.dump([dict(id=jobs[i]['job_id'], createdAt=0, model='gpt_image_2_5', ar='4:5',
                    prompt=f"{i}. {plan[i]['label']}", url=jobs[i]['result_url'], ref=1) for i in indices],
              open(fn, 'w'), indent=1)
index_json(sets['people'] + sets['scenes'], f'{here}/essos_pass11_main_{date}.json')
index_json(sets['dim'], f'{here}/essos_pass11_dim_{date}.json')
print('sheets + json written; build PDFs with build_catalogue_pdf.py')
