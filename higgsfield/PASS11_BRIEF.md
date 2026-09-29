# Pass 11 brief: what the research found, and the plan

Interim handoff while generation is pending. Sources: `pass11_research.json` (three research agents, 2026-09-29), the workflow's final prompt system, `ESSOS_IMAGE_LOG.md`.

## 1. Essos, from the site (essos.com; facts, not inference)
- Positioning: "Book Safe Medical Procedures Worldwide." Mission: "make world-class healthcare accessible to everyone, everywhere." Principles on /about: **Verified, Not Listed / No Middlemen / Always On Your Side.**
- Trust mechanics: Medical Board of 30+ US board-certified surgeons led by CMO Dr. Erez Dayan (MGH/Harvard); 21 named members with headshots; institution logos (Harvard, Johns Hopkins, Cleveland Clinic, U of Toronto, NYU Langone) rendered in neutral black. "Crystal clear" pricing, "no hidden charges." Editorial-standards page discloses AI-assisted content: the brand is comfortable with AI imagery **as long as it never poses as a real patient.**
- Journey: Intake (2-minute questionnaire) → Explore options → Match with a certified clinic → Book procedure and trip. Concierge "from booking through recovery." The lived moments to depict: phone on the nightstand, car at arrivals, hotel bed, tea, the window, the quiet morning after. **Never the operating room.**
- Voice: calm, second person, declarative, occasionally wry. Serif headline (PSTimes), sans body (ABC Repro). No exclamation marks, no "transform your look", no urgency, no glamour. The recurring word is "safe."
- Site colours: cream page `#F5F1E5`, near-black `#171715`, accent pearl white `#EBE4D1`, greys `#D8D4CA` `#BCB6A7` `#8D897D`, small gold `#DCC27B`. **No purple, rose or peach on the site**; those live only in the social palette.
- Site photography: three images only, all one person on a mottled warm grey-taupe or caramel seamless, soft low-contrast light, film grain, no props.

## 2. What the references measure (luminance 0–255, on the post area)
- **Tier A organic scenes** (ground truth for still lifes): mean L 37–58, darkest 5% at 4–7% grey. One warm light from a side; falloff to the far corner **1.9–2.4 stops**, and it is **asymmetric, anchored to the light**, not a centred lens circle. A2/A3 (water, smoke) are a soft centre glow, not a corner vignette. Shadows carry a faint cool-magenta black.
- **Tier E people** (ground truth for people): E1 mean L 132, no corner darkening; E3 (our platinum woman) wall ~0.7 stops brighter where the light enters, otherwise flat; the originals are a **near-black warm backdrop with one soft key, 2.2–2.8 stops subject-to-backdrop, no vignette needed because the backdrop is simply unlit.**
- **Tier F dim backdrops**: mean L ~43, 83% of pixels under L20, corners only ~0.5 stops below centre, chroma 2–4 (near neutral). The darkness is global, not a vignette.
- **E4 purple undertone**: the split-tone lives in the deepest tones only; highlights stay warm-neutral. On a rhinoplasty account, mauve on the face reads as bruising, so it must stay off the skin.
- Tier D (prompts.soul) is all AI, not real; useful only for the warm-light-on-cool-wall idea.

## 3. Why the pass-10 still lifes read as AI (diagnosis)
1. Prop-list staging: every named object appears, centred and unobstructed.
2. Everything in focus at once, with uniform micro-detail on towels, linen, leaves and rug.
3. Perfect surfaces: no water rings, fingerprints, creases, dust, cables, outlets.
4. Art-directed placement at pleasing thirds.
5. One spotlight-like source with everything else falling to black; real rooms have fill from walls and ceilings.
6. A radial vignette overlay centred on the frame, darkening the window side as much as the wall side.
7. Sun discs and orange-to-navy sunsets; the real Bosphorus in C1 is hazy and pale.
8. Render bokeh: a hard focus plane with uniformly creamy blur.
9. One amber cast over whites, clouds, stone and leather.
10. "Film grain" and "35mm" rendered as a grain layer and, twice, a sprocket border.
What the pass-7 hotel suite did right: it mirrors the real C1 hotel photo; mid-key; slightly blown window; grey-brown shadows; a rumpled duvet, a curtain mid-motion, a lamp cut by the frame; no vignette, no grain, no cast.

## 4. The six anti-AI methods now in the scene prompts
| Method | Mechanism |
|---|---|
| Hotel's own photo | Tonality of a hotel listing photo: hazy window blown to white, low contrast, open shadows; the pass-7 suite passed as a second reference image for tonality only |
| Open daylight | Overcast window light bouncing off pale walls; whites white; no sun disc; no warm grade |
| Lived-in Portra | One or two things a guest left (pushed-back sheet, water ring, cable), handheld, slight motion softness |
| Wide off-axis, deep focus | 28mm, a step back, camera a degree off level, subject off-centre and cut by the frame, whole depth in focus |
| Phone candid | Small-sensor snapshot: deep depth of field, mild HDR flatness, noise in shadows, nothing arranged |
| Plain photo (control) | A short prompt; lets the model fall back on its ordinary photographic prior |
Every scene edit also carries a dose sentence: pass-10 sources "about a fifth lighter than the reference"; pass-7 sources "add the falloff, stop at four fifths of the organic posts' depth." All replace sunsets and lit lamps with hazy daylight, and add "a bright, clear morning" for hopefulness.

## 5. The 80-image plan (7 batches)
- **People (32):** 14 existing people (8 originals + 6 pass-10 new) with the G1 band light; 4 lighter/more hopeful variants; 6 purple-undertone variants; 8 new people (early-sixties Northern European woman, mid-forties Black man, late-twenties Filipino woman, late-fifties Latino man, early-forties mixed-heritage woman, late-twenties Scandinavian man, late-fifties Chinese woman, late-forties Korean man). Colours named with descriptors, never hex, and never matched to the garment tone.
- **Scenes (32):** 6 pass-7 scenes × 2 methods, 6 pass-10 scenes × 1 method, 6 purple variants, 8 new journey scenes (suite, sitting room, recovery day, mid-flight, sedan at the kerb, side street after rain, last morning, bathroom counter, questionnaire moment, departure gate).
- **Dim text backdrops (16, separate PDF):** 8 neutral, 4 purple, 4 fully out-of-focus "blur" variants (2 neutral, 2 purple). Scenes: LA palms at dusk, sheer curtain and radiator, hotel corridor, tea glass at dusk, nightstand lamp, creased linen, plaster wall with a strip of light, towel stack, Bosphorus from a car, courtyard pool at night.

## 6. Open risks
- The band light for people is new (G1) and unproven on this model; the first batch is a test before the rest.
- Vignette percentages cannot be set exactly by prompt; if the model overshoots, a fixed corner mask in PIL is the fallback.
- Purple must stay off skin; every purple people image gets checked for anything that reads as bruising.
