# Essos image generation: running log + handoff spec

Purpose: a continuous record of every revision pass, the feedback behind it, what went wrong and why. It exists so a new chat can pick this up without re-learning. **Read section 1 first; it's the current spec. Sections 2–4 are history.**

Model used throughout: Higgsfield `gpt_image_2_5`, image edits via `medias[].role = image_references`.
Reference screenshots: `higgsfield/moodboard/` (tiers A–D below).

---

## 1. CURRENT SPEC (as of pass 11, 2026-09-29)

**Full prompt systems live in `pass11_spec_people.json` (people) and `pass11_spec_scenes.json` (scenes, dim, new people). Research in `pass11_research.json`; brief in `PASS11_BRIEF.md`; builder `build_pass11_requests.py`.** What follows is the summary.

### Reference hierarchy (what wins when references disagree)
| Tier | Files (`moodboard/`) | Governs | Do NOT use for |
|---|---|---|---|
| **G: people light** | `G1` (real) | The people shading: a soft HORIZONTAL band of light across eyes/nose/cheek at eye level; top and bottom of frame ease darker; sides and corners untouched; subtle | Scenes |
| **E: people look** | `E1`–`E6` site + guide posts, `originals_8people_contact.jpg` | The original Essos portrait: plain wall, soft warm key, Portra colour, faithful skin, hopeful | Scene mood |
| **A: scene mood** | `A1`–`A9` organic posts | Corner/edge darkening on still lifes, now at ~80% of A strength, anchored to the light not centred; measured 1.9–2.4 stops to the far corner in A | People |
| **F: dim backdrops** | `F1` carousel | The separate text-backdrop set: globally ~3 stops under, near-neutral/warm-neutral, one residual light area, soft; corners only ~0.5 stop under centre | Anything else |
| E4 | eye close-up (real) | Purple/mauve split-tone: deepest tones only, never on skin | — |
| B, C, D | realism refs, designed posts, external | Skin realism (B); colours in use (C); D is all AI, idea-only | — |

### Colours (one per person; named with a descriptor, never hex; never matched to the garment tone)
pearl white (warm off-white) · warm brown (soft tan like old plaster) · dusty rose (muted greyed pink-beige) · stone grey (warm mid grey) · peach (pale muted apricot, not orange) · light cool grey (pale silver-grey) · charcoal (warm near-black) · slate navy (dark grey-blue) · forest green (deep muted grey-green). Site itself uses only cream/near-black/pearl white/greys; rose/peach/purple are social-only.

### People prompt (edit; `people_band` in pass11_spec_people.json)
Identity clause → plain wall in {COLOUR} → **band-light definition** (soft warm light from the direction the face is turned, entering low and wide from beyond the frame, one gentle horizontal band at eye level; whole face lit, fullest across eyes, nose bridge/tip, cheekbones; eases into soft shade only above the hairline and below the jaw; wall keeps its hue, brightest at eye level; sides not darkened; no stripes, no visible source, no bright spot on the nose) → Portra colour block (skin never lightened, deep brown stays deep) → skin/hair-as-reference block → 85mm, grain in shadows only → no halo/borders/text. Variants: `people_band_hopeful` (blind raised, top/bottom only a shade darker), `people_purple` (mauve only in near-black hair, shadow side of clothing, shaded wall; explicit no purple on face), `new_person_t2i` (same light; realism block; no jewellery; no redness/dressings).

### Scene prompts (`scene_methods` ×6 in pass11_spec_scenes.json)
All: keep composition; replace sun discs/sunsets/lit lamps with hazy daylight from one window (the one content change allowed); "a bright, clear morning"; lift corners vs the heavy pass-10 refs; single darkness sentence "deep but readable, heaviest in the far corners away from the light, never black, not a ring"; `{DOSE}` = pass-10 sources "about a fifth lighter than the reference" / pass-7 sources "add the falloff, stop at four fifths of the organic posts' depth"; no signage/plates/labels/people. Methods: Hotel's own photo (pass-7 suite as a tonal second reference) · Open daylight · Lived-in Portra · Wide off-axis deep focus · Phone candid · Plain photo (control). `scene_purple` = same with plum-mauve blacks.

### Dim text-backdrop set (`dim_backdrop_t2i`, `_purple`, plus the blur variant in the builder)
Daylight/dusk photo seen through a dark neutral filter, ~3 stops under; brightest region a dark grey a third of the way to white, kept near an edge; faint warm sepia cast (or plum-mauve blacks for purple); middle of frame an even empty darkness; bottom darker than top; ordinary focus (blur variant: fully out of focus at f/1.4). Separate PDF, never in the main set.

### Hard rules learned
1. "no halo, rim-light outline or cut-out edge" in every prompt.
2. "no borders or film-frame edges" whenever a film look is named (pass 7/8 border bug).
3. "no room, furniture or window visible" for plain-wall edits (pass 7 kitchen bug).
4. Scenes: "no text, logos, legible signage, brand badges, licence plate text, readable labels"; no people.
5. Choose sources by PERSON, not by image (pool = 8 originals + 6 pass-10 + 8 pass-11 new = 22 distinct people).
6. Percentages are ignored by the model; state doses as comparisons ("a fifth lighter than the reference") and keep PIL as the exact fallback.
7. Never paste the people realism block (pores, hair) into scene prompts: it renders fabric and stone as hyper-detailed (pass-10 AI look).
8. Name a place, not a prop list; leave something cut by the frame; sun out of frame; lamps off; whites white.
9. Corner darkening belongs to scenes; people get the horizontal band (G1). The A-tier vignette on people was tried (pass 8/10) and rejected.
10. AI people are never labelled as named patients; purple never on skin (bruising read on a rhinoplasty account).
11. Test 3 before spending on a full batch when a template changes.

### Selects shipped
`essos_selects_2026-09-29.pdf` (pass 9) · pass 11: `essos_pass11_main_2026-09-29.pdf` (64: people + scenes), `essos_pass11_dim_backdrops_2026-09-29.pdf` (16). Review-based selects to follow.

---

## 2. PASS LOG

| # | What was asked | What I did | Result / problems | Mistake & why |
|---|---|---|---|---|
| 0 | "Build the PDF from catalogue_2026-09-29.json" | PDF of the 27 images in the JSON | OK | — |
| 0b | **Feedback:** "isn't everything, I need it all" | Paged whole history (600+), asked scope; user said last 3h, then 30h | 35-image / 129-image catalogues | JSON only covered 2h and I didn't say so up front. **Fix:** state source coverage in the first answer. |
| 1 | "Generate all the people with Essos beige background" | Asked colour; user pasted palette, said "pick a colour, proof of concept". 3-image test on Pearl White | Worked; halos present from source images | Asked "which set" twice; answer came back as the palette, not a set. I proceeded on 3 and reported. OK. |
| 2 | **Feedback:** remove halo on every person; dark green + beige; mood board screenshots (D1–D5) plus Essos designed posts (C1–C5); "one colour per person, vary, all people ×2 colours, + 3 new scenes (airport, chauffeur SUV, Turkey)" | 24 people × 2 colours (6-colour rotation) + 3 new scenes = 51 | Halos gone, mood decent. Peach/dusty rose read loud | Read "legs" as "all of" (correct, confirmed by user). Forest green was sampled from MA3, not the palette; I disclosed this. |
| 3 | "S-curve 4 random location/still life, then 3 people" | Interpreted as tone curve; 7 edits | Subtle; LA skyline sky shifted pinker | "S curve" guessed; I stated the assumption. The model can't do a pure tone curve and re-renders colour. **Better:** do tone curves locally with PIL, not via generation. |
| 4 | "Make the set: one colour per person, vary, only 15, few locations, very realistic" | 11 people + 4 Istanbul locations | Generated; user interrupted before review | — |
| 5 | Screenshots only (C-tier + B1 macro skin), no text | Asked what to do | — | Correct to ask. |
| 6 | "Part two prompts" | Asked what it meant | Unresolved | — |
| 7 | (experiment, **not feedback**): redo people realistic per B1/B2, 15 people, vary colours, 6 people-free scenes | 15 people × 8 colours + 6 scenes | Film-strip border on 2; plate man put in a kitchen; faces repeated | Border: "35mm film" wording invited a literal frame. Kitchen: "real room wall" wording invited a room. Repeats: sampled images, not people. |
| 8 | **Feedback:** tier-A organic posts = ground truth mood; keep colours but apply this mood, esp. dark shaded edges on hotels/cars/still lifes | Re-edited all 21 pass-7 images with the mood block + fixes for border/kitchen | Mood matches A-tier; fixes landed | Repeats remain (inherited). |
| 9 | "Confirm okay to send" → yes, curate | 8 distinct people × 8 colours + 6 scenes → selects PDF | Shipped | Flagged: hand image is weakest; AI people ≠ patients. |

Pass 7 people prompt (realism block, reuse it):
> …Background: a plain matte painted wall in {COLOUR}… Light: soft window daylight from one side with a touch of warm low sun… Make it look like a real unretouched candid photograph shot on 35mm film by a documentary photographer, not a studio render: visible pores, fine facial hair, slight skin unevenness and natural shine, flyaway hairs, real fabric texture, slight softness and natural lens falloff, organic film grain, muted true-to-life colour. No halo… No airbrushing, no plastic skin, no CGI look.

Full per-image prompts and job IDs live in the JSON files next to each set:
`essos_palette_regen_*.json` (pass 2), `scurve_*.json` (3), `essos_set15_*.json` (4), `essos_realistic_v3_*.json` (7), `essos_mood_v4_*.json` (8), `essos_selects_*.json` (9).

---

## 3. MY RECURRING FAILURE MODES (so the next chat avoids them)
1. **Guessing dictation instead of asking** when a term changes the output ("S curve", "legs", "part two"). Rule: one line "reading X as Y" is fine for cheap guesses; ask when a wrong guess costs a batch.
2. **Unverified claims.** I said "nothing was saved" when a file had been written. Rule: check `git status` before stating repo state.
3. **Reviewing a sample and implying the whole.** Always state how many I actually looked at.
4. **Prompt words taken literally** by the model ("film" → frame, "room wall" → room). Rule: add negatives for any literal reading.
5. **Sampling by file, not by identity**, which caused repeats.

---

## 4. REVISION LOG FOR FUTURE PASSES (append here)
Format: `pass N | date | ask (quoted) | change to spec | why | result | kept/reverted`
pass 10 | 2026-09-29 | "just do it 20 images" | Merged realism block (pass 7) + mood block (pass 8) into one prompt; added text-to-image portraits for new people (only 8 distinct people exist in source pool); scene prompts drop skin wording, add "no brand badges / legible passport text" | Deliver 20 on the current spec without repeating faces | 8 existing people on new colours + 6 new people + 6 scenes; mood consistent across all 20. Issues: #13 (new curly-haired man) looks close to #7 (existing curly man); "arms folded" lost to the head-and-shoulders crop; #20 hotel entryway is the darkest, maybe too dark | kept. Next: vary new-person hair/age more against existing pool; review #20 brightness
pass 11 | 2026-09-29 | Feedback: scenes "18–23% less severe, more hopeful, fix the AI look"; people "back to the original, remove the corner tint, more hopeful, keep the new people"; purple undertone on people + scenes; separate dim/blur text-backdrop set like F1; then G1: people shading = horizontal band, not corners | Two design workflows (Essos site crawl + reference measurement + pass diagnosis → 3 designers, 2 judges, synthesis, 3 adversarial critics, fix; then a second run for the G1 band light) → 80 images: 32 people (14 band, 4 lighter, 6 purple, 8 new t2i), 32 scenes (18 method edits, 6 purple, 8 new t2i), 16 dim (8 neutral, 4 purple, 4 blur). 3-image band test passed before the rest. | 80/80 completed. My read of the sheets: band light holds, no corner darkening, identities intact; scenes now mid-key daylight and read as photos; dim set matches F1. Open questions for the critic pass: scene vignette may now be lighter than the asked 20% reduction; method pairs on the same source came out near-identical (edits preserve composition, so methods differ only in tonality); a few pass-10 tells may remain in the t2i scenes. | kept. Mistakes this pass: (a) I applied the A-tier vignette to people in passes 8/10 on the user's "apply this mood to everything" and had to be told people are a different job; the reference hierarchy above now separates them. (b) The first people templates were written for "no tint" before G1 arrived; cost one extra workflow, no wasted generations. Spec changes for pass 12 come from the review synthesis (appended when it lands).
