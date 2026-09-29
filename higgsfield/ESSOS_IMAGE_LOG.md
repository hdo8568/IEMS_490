# Essos image generation: running log + handoff spec

Purpose: a continuous record of every revision pass, the feedback behind it, what went wrong and why. It exists so a new chat can pick this up without re-learning. **Read section 1 first; it's the current spec. Sections 2–4 are history.**

Model used throughout: Higgsfield `gpt_image_2_5`, image edits via `medias[].role = image_references`.
Reference screenshots: `higgsfield/moodboard/` (tiers A–D below).

---

## 1. CURRENT SPEC (as of pass 9, 2026-09-29)

### Reference hierarchy (what wins when references disagree)
| Tier | Files | Use for | Do NOT use for |
|---|---|---|---|
| **A: ground truth** | `A1`–`A9` organic Essos IG posts | Mood, light, darkness, shaded edges, crop style | — |
| **B: realism** | `B1` uposh macro skin, `B2` Headway candid | How real skin and people should look | Colour, mood |
| C: Essos designed posts | `C1`–`C5` (MY-3, MA3/4/5, Maya LA) | Background colours in use (grey, navy, green), hotel realism (C1) | Overall mood (brighter than A) |
| D: external mood board | `D1`–`D5` prompts.soul etc. | Warm-light-on-cool-wall contrast (D1/D2) | Colour or styling to copy directly |

### Colours (one per person, vary across set)
- Brand palette: charcoal `#28282E`, pearl white `#EBE4D1`, dusty rose `#D6AEB0`, peach `#F1AFA5`, stone grey `#9F9697`
- From Essos posts: forest green `#1F2A22` (MA3), slate navy `#2B3040` (MA5), light cool grey `#A7A9AE` (MA4)
- Rule from user: **mood from tier A overrides colour brightness** — every colour is rendered "deeper and quieter".
- Logo-only colour, never a background: warm white `#F2DCD5`.

### Working prompt, people (edit of a reference image)
> Edit of the reference photo. Keep the subject exactly the same: same person or people, face, hair, clothing, hands, props, pose, framing and crop. Keep the background a plain wall in {COLOUR}, but deeper and quieter, with no room, furniture or window visible. Apply the Essos brand mood: low-key, quiet and intimate; one soft directional light that falls off gently into deep shadow; darkened, softly vignetted edges and corners; muted, slightly desaturated earthy tones; warm light on the subject against dim surroundings; soft focus falloff; fine organic film grain; calm, contemplative, quietly hopeful. Real unretouched photograph, true skin and material texture, no CGI look, no halo around the subject. No text, no logos, no borders or film-frame edges.

(Pass 9 applied this on top of pass-8 images, which already carried the realism wording: visible pores, fine facial hair, flyaway hairs, 35mm documentary. **For a from-scratch run, merge both**: see pass 8 prompt in §2.)

### Working prompt, scenes (no people)
> Edit of the reference photo. Keep the same scene, objects, composition and framing, with no people. + the same Essos mood block.
Original scene briefs are in pass 8 (§2).

### Hard rules learned
1. Always say "no halo / rim-light outline / cut-out edge" (pass 1–2 bug).
2. Always say "no borders or film-frame edges" when invoking film looks (pass 8 bug).
3. Always say "no room, furniture or window visible" for plain-wall edits (pass 8 bug).
4. Say "no legible signage, no brand badges, no licence plate text" for scenes.
5. Choose sources **by person, not by image**. The source pool is many variants of ~8 people; random sampling repeats faces (pass 7–9 bug).
6. Test 3 before spending on a full batch when the prompt changes materially.
7. AI people must never be labelled as a named patient / "Patient Stories" (compliance).

### Selects shipped
`essos_selects_2026-09-29.pdf`: 8 distinct people × 8 colours + 6 scenes (from pass 9).

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
