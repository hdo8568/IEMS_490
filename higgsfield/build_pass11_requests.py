"""Build the pass-11 Higgsfield request batches from the workflow prompt systems.

Usage: python3 build_pass11_requests.py <spec_scenes.json> <spec_people.json> <out_dir>
  spec_scenes.json : final system from workflow 1 (scene_methods, scene_purple, new_scenes, dim_*, new_people)
  spec_people.json : final system from workflow 2 (people_band, people_band_hopeful, people_purple, new_person_t2i)
Writes out_dir/batch_<n>.json (<=12 requests each) and out_dir/plan.json (index -> label/set/source).
"""
import json, sys, os

sc = json.load(open(sys.argv[1])); pp = json.load(open(sys.argv[2]))
out = sys.argv[3]; os.makedirs(out, exist_ok=True)

# Existing people: ORIGINAL catalogue sources + the 6 new people from pass 10. (id, who, garment tone)
EXISTING = [
    ('198ec6c8-c859-49ed-a468-492e17eeba20', 'platinum-haired woman', 'light'),
    ('11835ad7-967c-40a0-b302-222715a1d6d3', 'woman, dark hair up', 'light'),
    ('0e3e7990-ace6-4577-886c-d9c4709014df', 'man, white linen shirt, plate', 'light'),
    ('5fb55d82-b246-4902-a3db-08e9fa70a40d', 'Black woman, low bun', 'light'),
    ('3244ad1b-3b44-4650-8e77-116e63ac7abb', 'dark-haired man', 'light'),
    ('a6e8a12d-9f91-489a-a979-c93317ad2220', 'woman, long straight dark hair', 'dark'),
    ('99e7fa98-b95e-4012-91cf-778fc5157cfe', 'curly-haired man', 'dark'),
    ('2f85644c-63a3-42ed-9167-b991d86a6255', 'East Asian man, hand at face', 'mid'),
    ('fe54646f-606b-4f04-8cf8-f07fe9758832', 'new: Middle Eastern woman, wavy hair', 'light'),
    ('e8226e50-3567-491a-835b-b0d22ce0fff5', 'new: South Asian man, eyes closed', 'dark'),
    ('eaf5563e-801f-45d0-948d-abe36c809ce0', 'new: East Asian woman, bob', 'light'),
    ('1b300b8b-c193-4adb-84cd-69bf6ea152ba', 'new: freckled woman, auburn hair', 'mid'),
    ('9a2964f8-ef00-4ab4-a4a8-c206cf20b2b0', 'new: Latino man, curly hair', 'light'),
    ('c32f59d8-4dcc-4659-bb29-1d505f904df7', 'new: Black woman, short natural hair', 'mid'),
]
# Existing scenes. pass-7 versions have no vignette (DOSE_ADD); pass-10 versions have the heavy one (DOSE_REDUCE).
SCENES7 = [
    ('687d39f6-b9d5-46aa-80ff-14b5d1861daa', 'hotel suite, Bosphorus view'),
    ('1992f313-cce8-4a97-9b7e-935baa13d019', 'chauffeur SUV, hotel entrance'),
    ('20d1f04a-0cf2-4af8-a062-8f5a6ce140c7', 'airport arrivals, lone suitcase'),
    ('686b180c-d279-4838-966c-61d8da0fa3e1', 'balcony tea, Bosphorus sunrise'),
    ('f23fa419-c251-4c7f-8a9b-9365be07fb20', 'hotel bedside still life'),
    ('64097e1a-e4aa-4340-bce8-d5ea93ac0bba', 'Galata street cafe'),
]
SCENES10 = [
    ('a9ee3544-6cec-4b9b-876f-365d9418d420', 'clinic consultation room'),
    ('7344c898-6761-4efe-8883-eac91f18f495', 'car back seat, tinted window'),
    ('e8ab4727-4d7b-4c9b-baaf-444c13eca0aa', 'airplane window seat'),
    ('46357548-eb61-4d86-95b6-bc8759404b18', 'hotel bathroom vanity'),
    ('d34e771d-8ce1-4b7f-8fcc-0cb50f6d3a85', 'Bosphorus ferry deck'),
    ('3f7e862b-8943-4159-86cb-41dcd928173e', 'hotel entryway at night'),
]
HOTEL_REF = '687d39f6-b9d5-46aa-80ff-14b5d1861daa'
DOSE_REDUCE = 'Overall the darkening is about a fifth lighter than in the reference: the corners lifted so their texture reads, the lit area a touch brighter, the same shape of falloff.'
DOSE_ADD = 'Add this falloff on top of the reference, which has none, but stop at about four fifths of the depth of the organic Essos posts: the corners deep but with texture still readable.'

# Colour names with descriptors (never hex), keyed by which garment tones they suit.
COLOURS = {
    'pearl white, a warm off-white': ('dark', 'mid'),
    'warm brown, a soft tan like an old plaster wall': ('light', 'mid'),
    'dusty rose, a muted greyed pink-beige': ('light', 'dark', 'mid'),
    'stone grey, a warm mid grey': ('light', 'dark'),
    'peach, a pale muted apricot, not orange': ('dark', 'mid'),
    'light cool grey, a pale silver-grey': ('dark', 'mid'),
    'charcoal, a warm near-black': ('light', 'mid'),
    'slate navy, a dark grey-blue': ('light', 'mid'),
    'forest green, a deep muted grey-green': ('light', 'mid'),
}
_ci = 0
def colour_for(tone):
    global _ci
    keys = list(COLOURS)
    for _ in range(len(keys)):
        c = keys[_ci % len(keys)]; _ci += 1
        if tone in COLOURS[c]: return c
    return keys[0]

def ref(*ids): return [{'role': 'image_references', 'value': v} for v in ids]
def fill(t, **kw):
    for k, v in kw.items(): t = t.replace('{' + k + '}', v)
    assert '{' not in t or '}' not in t, 'unfilled placeholder: ' + t[:120]
    return t

R, plan, n = [], [], 0
def add(prompt, label, set_, medias=None):
    global n
    n += 1
    p = {'model': 'gpt_image_2_5', 'aspect_ratio': '4:5', 'prompt': prompt}
    if medias: p['medias'] = medias
    R.append({'index': n, 'params': p}); plan.append({'index': n, 'label': label, 'set': set_})

# ---- PEOPLE (32) ----
for sid, who, tone in EXISTING:                                   # 14 band light, standard
    c = colour_for(tone); add(fill(pp['people_band'], COLOUR=c), f'{who} · band light · {c.split(",")[0]}', 'people', ref(sid))
for sid, who, tone in [EXISTING[i] for i in (0, 4, 9, 13)]:        # 4 band light, lighter + more hopeful
    c = colour_for(tone); add(fill(pp['people_band_hopeful'], COLOUR=c), f'{who} · band light, lighter/hopeful · {c.split(",")[0]}', 'people', ref(sid))
for sid, who, tone in [EXISTING[i] for i in (3, 5, 7, 8, 10, 11)]:  # 6 purple undertone
    c = colour_for(tone); add(fill(pp['people_purple'], COLOUR=c), f'{who} · band light + purple · {c.split(",")[0]}', 'people', ref(sid))
NEW_TONE = ['light', 'dark', 'light', 'mid', 'dark', 'light', 'dark', 'mid']
for person, tone in zip(sc['new_people'][:8], NEW_TONE):          # 8 new people, text-to-image
    c = colour_for(tone); add(fill(pp['new_person_t2i'], PERSON=person, COLOUR=c), f'NEW {person[:70]} · {c.split(",")[0]}', 'people')

# ---- SCENES (32) ----
M = sc['scene_methods']
mi = 0
def method():
    global mi
    m = M[mi % len(M)]; mi += 1; return m
for sid, what in SCENES7:                                         # 6 x 2 methods = 12 (add ~80% vignette)
    for _ in range(2):
        m = method()
        med = ref(sid, HOTEL_REF) if (m['name'].lower().startswith('hotel') and sid != HOTEL_REF) else ref(sid)
        add(fill(m['edit_template'], DOSE=DOSE_ADD, SCENE=what), f'{what} · {m["name"]}', 'scenes', med)
for sid, what in SCENES10:                                        # 6 x 1 method = 6 (reduce vignette by ~20%)
    m = method()
    med = ref(sid, HOTEL_REF) if m['name'].lower().startswith('hotel') else ref(sid)
    add(fill(m['edit_template'], DOSE=DOSE_REDUCE, SCENE=what), f'{what} · {m["name"]}', 'scenes', med)
for sid, what in SCENES7[:3] + SCENES10[:3]:                      # 6 purple undertone
    dose = DOSE_ADD if (sid, what) in SCENES7 else DOSE_REDUCE
    add(fill(sc['scene_purple'], DOSE=dose, SCENE=what), f'{what} · purple', 'scenes', ref(sid))
for i, s in enumerate(sc['new_scenes'][:8]):                      # 8 new scenes, text-to-image, methods round-robin
    m = M[i % len(M)]
    add(fill(m['t2i_template'], SCENE=s), f'NEW {s[:70]} · {m["name"]}', 'scenes')

# ---- DIM TEXT-BACKDROP SET (16) -> separate PDF ----
BLUR = ('{SCENE}, seen completely out of focus, as if the camera were focused a metre in front of the scene at f/1.4: every edge dissolved into soft overlapping shapes and gradients, no detail anywhere, the picture reading as a dark abstract wash of the scene\'s own colours. The whole picture about three stops underexposed: most of the frame deep shadow, one broad soft pool of faint light near an edge (a window, a band of sky, a distant lamp) that never gets lighter than a dark grey, roughly a third of the way to white. {CAST} The middle of the frame an even, empty darkness with no shape or highlight in it. The bottom of the frame darker than the top. Real photograph, fine grain living in the shadows, no uniform grain layer. No vignette ring, no spotlight circle; the darkness is simply the room or the evening. No people, no text, no logos, no legible signage, no brand badges, no licence plate text, no readable labels, no borders or film-frame edges, no halo, rim-light outline or cut-out edge around any object.')
CAST_N = 'A faint warm brown cast, the sepia of a dim room at dusk, no blue, no colour grade.'
CAST_P = 'Colour is a film split-tone: the deep shadows, which are most of the frame, carry a muted dusty plum-mauve undertone, the blacks leaning warm maroon-mauve, red and blue both a touch above green, never blue, so low in saturation that they still read as near-black; the faint light stays warm-neutral, a muted peach-ivory, never purple; no purple light, no magenta cast, no coloured filter.'
DS = sc['dim_scenes']
for s in DS[:8]:                                                  # 8 dim, neutral
    add(fill(sc['dim_backdrop_t2i'], SCENE=s), f'DIM {s[:70]}', 'dim')
for s in [DS[0], DS[1], DS[8], DS[9]]:                            # 4 dim, purple
    add(fill(sc['dim_backdrop_purple'], SCENE=s), f'DIM purple {s[:70]}', 'dim')
for s in [DS[0], DS[4]]:                                          # 2 blur, neutral
    add(fill(BLUR, SCENE=s, CAST=CAST_N), f'BLUR {s[:70]}', 'dim')
for s in [DS[1], DS[8]]:                                          # 2 blur, purple
    add(fill(BLUR, SCENE=s, CAST=CAST_P), f'BLUR purple {s[:70]}', 'dim')

for b in range(0, len(R), 12):
    json.dump(R[b:b + 12], open(f'{out}/batch_{b // 12}.json', 'w'))
json.dump(plan, open(f'{out}/plan.json', 'w'), indent=1)
print(len(R), 'requests in', (len(R) + 11) // 12, 'batches;', {s: sum(1 for p in plan if p['set'] == s) for s in ('people', 'scenes', 'dim')})
