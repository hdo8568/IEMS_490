# Essos image system: handoff for the next session

Read this first. It is the state of the Essos organic-image work as of 2026-09-29, written so a session that has the full Essos codebase/design system can pick up without this chat. Everything referenced is in `higgsfield/` on branch `claude/pdf-catalogue-build-ml264c`.

## 0. What exists, in one paragraph
30 distinct AI people (the "face register" below), each available in two finished treatments: **band light** (`essos_30faces_2026-09-29.pdf`, the user's preferred method) and **clean guide-post look** (`essos_30faces_clean_2026-09-29.pdf`). Both PDFs share page order, so page N is the same person. Plus: 32 scenes and 16 dim text-backdrops from pass 11 (`essos_pass11_*.pdf`), a critic review with selects, and a full history log. All images are Higgsfield `gpt_image_2_5`; every image has a Higgsfield job ID that can be passed as `medias: [{role: "image_references", value: <id>}]` to re-edit that exact face or scene.

## 1. How to use the 30 faces (the important part)
- **To put a face on a new background, light or crop:** edit from the job ID in the register with the relevant template. Do NOT regenerate a person from a text description; identity will drift. The band-light IDs are the best sources (dark wall, most faithful skin).
- **Templates** (full text, ready to send): `pass11_spec_people.json` → `people_band` (band light) ; `pass11_spec_scenes.json` → `people_no_tint` (clean look; swap the "vignetted corners" sentence for "band of light ... remove that entirely" when the source is a band-light image, see `build_pass13_requests.py`). Replace `{COLOUR}` with a colour NAME plus descriptor, never hex.
- **Colours:** band light works on dark walls only (charcoal, slate navy, forest green, deep warm brown). The clean look works on all nine: those four plus pearl white, warm brown, stone grey, dusty rose, peach, light cool grey. Never match a wall to the garment tone.
- **Never** label an AI person as a named patient or place them in a "Patient Stories" layout; the Essos editorial-standards page discloses AI-assisted content, which is the cover for using them in general brand posts only.
- Purple/mauve grading on faces reads as bruising on a rhinoplasty account: retired.

## 2. Face register
| # | Person | Origin | Original source ID (if edited from the catalogue) | Band-light ID (pass 12) | Clean ID (pass 13) |
|---|---|---|---|---|---|
| 1 | platinum-haired woman | original catalogue (pass 0) | `198ec6c8-c859-49ed-a468-492e17eeba20` | `7e90e772-40e8-4625-81ea-c2fbe4e779fe` | `76faa8c0-4eaa-4d5c-98ad-b2e90796fa40` |
| 2 | woman, dark hair up | original catalogue (pass 0) | `11835ad7-967c-40a0-b302-222715a1d6d3` | `d16adfda-d9c9-4103-b843-6103edd3c0c3` | `6e91c185-f419-4ce4-8808-3995d09ea92e` |
| 3 | man, white linen shirt | original catalogue (pass 0) | `0e3e7990-ace6-4577-886c-d9c4709014df` | `4adfd697-ace8-4617-80ab-ecd77179d7cd` | `653b2070-8090-4f84-8b2e-7bf6c761af15` |
| 4 | Black woman, low bun | original catalogue (pass 0) | `5fb55d82-b246-4902-a3db-08e9fa70a40d` | `b9a15c78-cc04-4455-a702-7f25b6fe526a` | `19c3ae09-c787-4f4a-ae77-d291ea221e49` |
| 5 | dark-haired man | original catalogue (pass 0) | `3244ad1b-3b44-4650-8e77-116e63ac7abb` | `5ee4cb1d-718c-45bc-ab75-7ade73a7dcef` | `22ee77d9-4bb1-4ac5-905f-6f6b522561a1` |
| 6 | woman, long straight dark hair | original catalogue (pass 0) | `a6e8a12d-9f91-489a-a979-c93317ad2220` | `266b042b-0d5b-41ac-85d2-1d88b005458e` | `069f9ba9-402a-46ef-80ef-d64e142cabc3` |
| 7 | curly-haired man | original catalogue (pass 0) | `99e7fa98-b95e-4012-91cf-778fc5157cfe` | `298bb458-3d6e-4120-bf45-4a7c1f17dded` | `48075965-ba76-4227-9ef9-854aaab7dacc` |
| 8 | East Asian man, hand at face | original catalogue (pass 0) | `2f85644c-63a3-42ed-9167-b991d86a6255` | `9438c06a-dd23-4992-bbd9-2929b7cf3f29` | `35e22a20-0841-477b-8e97-deb8ee4713dd` |
| 9 | Middle Eastern woman, wavy hair | pass 10 t2i | `fe54646f-606b-4f04-8cf8-f07fe9758832` | `80fc564d-507f-4d34-bde2-12cefc687010` | `b7f58a9e-4b32-4c4e-b11b-7d570fd1d899` |
| 10 | South Asian man, eyes closed | pass 10 t2i | `e8226e50-3567-491a-835b-b0d22ce0fff5` | `ccd5fd86-5a42-4961-a77a-9b2a8b1e426d` | `8cd3450e-934b-47e1-a515-30103cae8de3` |
| 11 | East Asian woman, bob | pass 10 t2i | `eaf5563e-801f-45d0-948d-abe36c809ce0` | `f889a16c-6777-424f-b7ea-5b44eba4e230` | `4f52d5ea-2f29-4d02-9bb1-78aef22a824f` |
| 12 | freckled woman, auburn hair | pass 10 t2i | `1b300b8b-c193-4adb-84cd-69bf6ea152ba` | `6ba6d586-0c56-4f57-bd79-0c38dfb5e024` | `0bdedd40-6d81-468c-8ae5-eeeceb1dc9f1` |
| 13 | Latino man, curly hair | pass 10 t2i | `9a2964f8-ef00-4ab4-a4a8-c206cf20b2b0` | `d49f2cf0-5b84-4be6-8fda-581a86e42610` | `1ee5d779-d45c-4d1a-ba0e-025e512c678c` |
| 14 | Black woman, short natural hair | pass 10 t2i | `c32f59d8-4dcc-4659-bb29-1d505f904df7` | `b25c6578-25e4-4281-9403-9e54c821d8ab` | `1ef87e6e-076f-4d72-80d7-6c875979d1d4` |
| 15 | NEW a woman in her early sixties, Northern European, silver-grey | pass 12 t2i | `—` | `6f780df1-46e9-4a2a-a836-217fdba589b6` | `539a57a6-de2e-48a4-afc3-37293d1b6593` |
| 16 | NEW a Black man in his mid-forties, deep brown skin, hair croppe | pass 12 t2i | `—` | `b126b695-ea4b-4bd2-aff4-759d2fd83a00` | `3e41ce92-8225-4952-97b2-019d39c61326` |
| 17 | NEW a Filipino woman in her late twenties, tan skin, long black  | pass 12 t2i | `—` | `f08a5bf1-e9bf-4232-bc11-21ef4a739aba` | `5cf2f3cf-b8fd-4d1c-9742-a45ba8fb36f4` |
| 18 | NEW a Latino man around fifty-eight, tan skin, hair cut close an | pass 12 t2i | `—` | `bbc6649c-09c9-4794-8068-4fabafc0a7da` | `2bb4a5e3-a096-41bf-9bbe-2d58099d2319` |
| 19 | NEW a woman in her early forties of mixed Black and white herita | pass 12 t2i | `—` | `9edbcbd9-439a-4660-a8f9-dd85074c8550` | `8911be43-7f79-46c4-b6f4-23ec47b3b284` |
| 20 | NEW a Chinese woman in her late fifties, warm light-tan skin, sh | pass 12 t2i | `—` | `fa8aeea9-6b4a-49cf-b05c-2492389bd159` | `6c296620-6b34-4dd7-91e3-68b58be65490` |
| 21 | NEW a Turkish woman in her mid-thirties, olive skin, dark hair p | pass 12 t2i | `—` | `8502ec99-d1be-4f5d-842e-898261ad296f` | `fe77345e-c8f9-4f4e-8d94-f89d54b7b984` |
| 22 | NEW a Black woman in her early twenties, deep brown skin, long b | pass 12 t2i | `—` | `9df674eb-9330-43f8-beb1-b12fba58d058` | `8d767380-d70f-4c2e-a384-44951b73400d` |
| 23 | NEW a white man in his early fifties, salt-and-pepper hair swept | pass 12 t2i | `—` | `316fda95-c790-44ae-adaa-18e0a980b930` | `02f8b89c-5f36-43eb-b80b-b70be89a7ebb` |
| 24 | NEW a South Asian woman in her late forties, warm brown skin, sh | pass 12 t2i | `—` | `8d47b9b4-ba54-45d5-a906-ab5b7735b2ce` | `578361a5-ddfe-4eee-98a6-daec1063bde6` |
| 25 | NEW a Latina woman in her late twenties, tan skin, dark hair in  | pass 12 t2i | `—` | `92c80ed0-e872-49c8-930a-04b00df7a728` | `bc640596-411f-4767-b935-e6c434ba71b1` |
| 26 | NEW an East Asian man in his early sixties, short grey hair, a c | pass 12 t2i | `—` | `9c7c5520-ad93-4155-9a19-b704df77c634` | `e4213460-69a2-4ba4-83de-eead976c692c` |
| 27 | NEW a mixed-heritage man in his mid-thirties, light brown skin,  | pass 12 t2i | `—` | `7ad5dbd5-68eb-495f-86db-c1a7f0807fd3` | `c974693f-1848-4c2e-8b7a-d3cdbf16771f` |
| 28 | NEW a woman in her mid-forties of Persian descent, dark wavy hai | pass 12 t2i | `—` | `0aeef1b2-eb0c-459a-90c8-3be4169bbff6` | `17b873eb-adb6-4cbc-8391-b0b85a5765a1` |
| 29 | NEW Scandinavian man, late twenties (pass 11) | pass 11 t2i | `—` | `6ae8f775-052c-4ef9-bcc3-43599020daa3` | `81eded47-8e54-45f0-937d-b80342714a23` |
| 30 | NEW Korean man, late forties (pass 11) | pass 11 t2i | `—` | `14bfb3fc-6cc9-4364-b137-b8070689d885` | `b6f696de-7a35-403a-9cef-5312785f6abd` |

Pose/expression rules that produced the on-campaign new faces: strict profile or three-quarter turned away, nose line against the wall, eyes closed / down / softly ahead, mouth closed, no smile, knit/linen/cotton, no jewellery. Cap eyes-closed tilted heads at one in four.

## 3. Reference hierarchy (files in `moodboard/`)
| Tier | Files | Governs |
|---|---|---|
| G | `G1_people_horizontal_band_light_REAL.png` | People shading: horizontal band at eye level, top/bottom ease darker, sides and corners untouched |
| E | `E1..E6` (essos.com + guide posts), `originals_8people_contact.jpg` | The base people look: plain wall, soft side key, Portra colour, faithful skin, hopeful |
| A | `A1..A9` (organic IG posts) | Still-life mood: corner darkening anchored to the light (measured 1.9–2.4 stops to the far corner); used at ~80% |
| F | `F1` (carousel) | Dim text-backdrop set: globally ~3 stops under, near-neutral, one residual light area |
| B / C / D | realism refs / designed posts / external | Skin realism; colours in use; D is all AI, idea-only |
Essos site facts used for tone (from `pass11_research.json`): "Book Safe Medical Procedures Worldwide"; Verified-Not-Listed / No Middlemen / Always On Your Side; 30+ surgeon Medical Board; site palette cream `#F5F1E5`, near-black `#171715`, pearl white `#EBE4D1`; PSTimes serif + ABC Repro sans; no purple/rose/peach on the site (social-only).

## 4. Scenes and dim backdrops: current state
- Scenes must be generated from text (one frame per journey moment), not edited from old seeds; light = low warm late-afternoon or lamp light through a window, lived-in detail, ≤2 props, subject off-centre; sun out of frame; no airport aprons/tail fins, no car tailgates/badges, no signage. Best presets: Lived-in Portra, Hotel's own photo. The corner darkening is applied numerically after generation (`postprocess_pass11.py`, far corner ≈0.55× centre, anchored away from the light); prompts cannot set a dose.
- Keepers from pass 11: scenes 59, 58, 63, 57, 55; dim 66, 68, 72, 73, 74, 77 (`essos_pass11_selects_2026-09-29.pdf`). Do not use 35–38, 43, 44, 52–54 (airline livery, car badge, cropped foot, wrong room).
- Dim set: pull the amber cast ~25% (done in `postprocess_pass11.py`); purple only through a luminance mask (L<25).

## 5. Rules learned the hard way (every prompt)
1. "no halo, rim-light outline or cut-out edge". 2. "no borders or film-frame edges" whenever film is named. 3. "no room, furniture or window visible" for plain walls. 4. Identity clause verbatim: "keep the same face, eyes, nose shape and size, lips, skin tone, hair, clothing, pose and head angle". 5. Percentages are ignored; state doses as comparisons or post-process. 6. Never paste the people realism block into scene prompts. 7. Test 3 before a full batch when a template changes. 8. Choose sources by person, not by image.

## 6. File map
- Log with every pass, mistake and spec change: `ESSOS_IMAGE_LOG.md` · brief: `PASS11_BRIEF.md` · research: `pass11_research.json` · review: `pass11_review.json`
- Specs: `pass11_spec_people.json`, `pass11_spec_scenes.json` · builders: `build_pass11_requests.py`, `build_pass13_requests.py` · post: `postprocess_pass11.py` · PDF: `build_catalogue_pdf.py`
- Indexes (job IDs + URLs): `essos_30faces_2026-09-29.json`, `essos_30faces_clean_2026-09-29.json`, `essos_pass11_main/dim/selects_*.json`
- Sheets: `essos_30faces_contact_*.jpg`, `essos_30faces_clean_contact_*.jpg`, `essos_pass11_*_contact_*.jpg`

## 7. Open items
- Scenes need a pass 12 on the text-only route (spec changes are in the log, section "Pass 12 spec changes").
- People "lighter/hopeful" variant should be a masked exposure lift, not a prompt.
- Automated gates (logo/text, body parts, corner ratio, wall hue, face ΔL) are specified but not built.
