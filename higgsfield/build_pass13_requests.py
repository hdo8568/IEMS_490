"""Pass 13: the 30 faces from pass 12 re-edited to the clean guide-post look (E3/E5): plain wall, soft side key, no band, no vignette.
Usage: python3 build_pass13_requests.py <out_dir>
"""
import json, itertools, sys, os
here = os.path.dirname(os.path.abspath(__file__))
P = sys.argv[1]; os.makedirs(P, exist_ok=True)
sc = json.load(open(f'{here}/pass11_spec_scenes.json'))
T = sc['people_no_tint'].replace(
    'The reference has darkened, vignetted corners and a dim surround: remove that entirely.',
    'The reference has a band of light at eye level with shade at the top and bottom: remove that entirely.')
COL = ['warm brown, a soft tan like an old plaster wall', 'pearl white, a warm off-white', 'stone grey, a warm mid grey',
       'dusty rose, a muted greyed pink-beige', 'charcoal, a warm near-black', 'light cool grey, a pale silver-grey',
       'peach, a pale muted apricot, not orange', 'slate navy, a dark grey-blue', 'forest green, a deep muted grey-green']
col = itertools.cycle(COL)
faces = json.load(open(f'{here}/essos_30faces_2026-09-29.json'))
R, plan = [], []
for k, f in enumerate(faces, 1):
    c = next(col)
    R.append({'index': k, 'params': {'model': 'gpt_image_2_5', 'aspect_ratio': '4:5', 'prompt': T.replace('{COLOUR}', c),
                                     'medias': [{'role': 'image_references', 'value': f['id']}]}})
    plan.append({'index': k, 'label': f['prompt'].split('. ', 1)[1].split(' · ')[0] + ' · clean · ' + c.split(',')[0]})
assert not any('{' in r['params']['prompt'] for r in R)
for b in range(0, 30, 12):
    json.dump(R[b:b + 12], open(f'{P}/batch_{b // 12}.json', 'w'))
json.dump(plan, open(f'{P}/plan.json', 'w'), indent=1)
print(len(R), 'requests')
