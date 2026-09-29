"""Build the pass-11 Higgsfield request batches from the workflow's final prompt system (spec.json).

Usage: python3 build_pass11_requests.py <spec.json> <out_dir>
Writes out_dir/batch_<n>.json (<=12 requests each) and out_dir/plan.json (index -> label/set/source).
"""
import json, sys, os, itertools

spec = json.load(open(sys.argv[1]))
out = sys.argv[2]; os.makedirs(out, exist_ok=True)

# Existing people: ORIGINAL catalogue sources (the look the user wants back) + the 6 new people from pass 10.
EXISTING = [
    ('198ec6c8-c859-49ed-a468-492e17eeba20', 'platinum-haired woman'),
    ('11835ad7-967c-40a0-b302-222715a1d6d3', 'woman, dark hair up'),
    ('0e3e7990-ace6-4577-886c-d9c4709014df', 'man, white linen shirt, plate'),
    ('5fb55d82-b246-4902-a3db-08e9fa70a40d', 'Black woman, low bun'),
    ('3244ad1b-3b44-4650-8e77-116e63ac7abb', 'dark-haired man'),
    ('a6e8a12d-9f91-489a-a979-c93317ad2220', 'woman, long straight dark hair'),
    ('99e7fa98-b95e-4012-91cf-778fc5157cfe', 'curly-haired man'),
    ('2f85644c-63a3-42ed-9167-b991d86a6255', 'East Asian man, hand at face'),
    ('fe54646f-606b-4f04-8cf8-f07fe9758832', 'new: Middle Eastern woman, wavy hair'),
    ('e8226e50-3567-491a-835b-b0d22ce0fff5', 'new: South Asian man, eyes closed'),
    ('eaf5563e-801f-45d0-948d-abe36c809ce0', 'new: East Asian woman, bob'),
    ('1b300b8b-c193-4adb-84cd-69bf6ea152ba', 'new: freckled woman, auburn hair'),
    ('9a2964f8-ef00-4ab4-a4a8-c206cf20b2b0', 'new: Latino man, curly hair'),
    ('c32f59d8-4dcc-4659-bb29-1d505f904df7', 'new: Black woman, short natural hair'),
]
# Existing scenes: pass-7 versions (lighter, incl. the hotel suite the user liked) + pass-10 scenes.
SCENES = [
    ('687d39f6-b9d5-46aa-80ff-14b5d1861daa', 'hotel suite, Bosphorus view'),
    ('1992f313-cce8-4a97-9b7e-935baa13d019', 'chauffeur SUV, hotel entrance'),
    ('20d1f04a-0cf2-4af8-a062-8f5a6ce140c7', 'airport arrivals, lone suitcase'),
    ('686b180c-d279-4838-966c-61d8da0fa3e1', 'balcony tea, Bosphorus sunrise'),
    ('f23fa419-c251-4c7f-8a9b-9365be07fb20', 'hotel bedside still life'),
    ('64097e1a-e4aa-4340-bce8-d5ea93ac0bba', 'Galata street cafe'),
    ('a9ee3544-6cec-4b9b-876f-365d9418d420', 'clinic consultation room'),
    ('7344c898-6761-4efe-8883-eac91f18f495', 'car back seat, tinted window'),
    ('e8ab4727-4d7b-4c9b-baaf-444c13eca0aa', 'airplane window seat'),
    ('46357548-eb61-4d86-95b6-bc8759404b18', 'hotel bathroom vanity'),
    ('d34e771d-8ce1-4b7f-8fcc-0cb50f6d3a85', 'Bosphorus ferry deck'),
    ('3f7e862b-8943-4159-86cb-41dcd928173e', 'hotel entryway at night'),
]
COLOURS = ['pearl white #EBE4D1', 'warm tan brown #6B5A48', 'dusty rose #D6AEB0', 'stone grey #9F9697',
           'peach #F1AFA5', 'light cool grey #A7A9AE', 'charcoal #28282E', 'slate navy #2B3040', 'forest green #1F2A22']
col = itertools.cycle(COLOURS)

def ref(v): return [{'role': 'image_references', 'value': v}]
def fill(t, **kw):
    for k, v in kw.items(): t = t.replace('{' + k + '}', v)
    return t

R, plan, n = [], [], 0
def add(prompt, label, set_, medias=None, ar='4:5'):
    global n
    n += 1
    p = {'model': 'gpt_image_2_5', 'aspect_ratio': ar, 'prompt': prompt}
    if medias: p['medias'] = medias
    R.append({'index': n, 'params': p}); plan.append({'index': n, 'label': label, 'set': set_})

# A. people, no tint (14)
for sid, who in EXISTING:
    c = next(col); add(fill(spec['people_no_tint'], COLOUR=c), f'{who} · no tint · {c}', 'people', ref(sid))
# B. people, 10-15% tint (4)
for sid, who in [EXISTING[0], EXISTING[4], EXISTING[9], EXISTING[13]]:
    c = next(col); add(fill(spec['people_low_tint'], COLOUR=c), f'{who} · 12% tint · {c}', 'people', ref(sid))
# C. people, purple undertone (6)
for sid, who in [EXISTING[3], EXISTING[5], EXISTING[7], EXISTING[8], EXISTING[10], EXISTING[11]]:
    c = next(col); add(fill(spec['people_purple'], COLOUR=c), f'{who} · purple · {c}', 'people', ref(sid))
# D. new people, text-to-image (8)
for person in spec['new_people'][:8]:
    c = next(col); add(fill(spec['new_person_t2i'], PERSON=person, COLOUR=c), f'NEW {person[:60]} · {c}', 'people')
# E. scene edits: each existing scene x 2 methods (24)
M = spec['scene_methods']
for i, (sid, what) in enumerate(SCENES):
    for j in (0, 1):
        m = M[(2 * i + j) % len(M)]
        add(m['edit_template'], f'{what} · method: {m["name"]}', 'scenes', ref(sid))
# F. scene purple (6)
for sid, what in SCENES[:6]:
    t = spec['scene_purple']
    add(fill(t, SCENE=what), f'{what} · purple', 'scenes', ref(sid))
# G. new scenes t2i (8), methods round-robin
for i, s in enumerate(spec['new_scenes'][:8]):
    m = M[i % len(M)]
    add(fill(m['t2i_template'], SCENE=s), f'NEW {s[:60]} · method: {m["name"]}', 'scenes')
# H. dim text-backdrop set (8 + 4 purple) -> separate PDF
for s in spec['dim_scenes'][:8]:
    add(fill(spec['dim_backdrop_t2i'], SCENE=s), f'DIM {s[:60]}', 'dim')
for s in spec['dim_scenes'][8:10] + spec['dim_scenes'][:2]:
    add(fill(spec['dim_backdrop_purple'], SCENE=s), f'DIM purple {s[:60]}', 'dim')

for b in range(0, len(R), 12):
    json.dump(R[b:b + 12], open(f'{out}/batch_{b // 12}.json', 'w'))
json.dump(plan, open(f'{out}/plan.json', 'w'), indent=1)
print(len(R), 'requests in', (len(R) + 11) // 12, 'batches;', {s: sum(1 for p in plan if p['set'] == s) for s in ('people', 'scenes', 'dim')})
