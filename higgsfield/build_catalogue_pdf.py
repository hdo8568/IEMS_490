"""Build a PDF catalogue from a Higgsfield catalogue JSON (one image per page)."""
import json, sys, os, urllib.request, datetime
from PIL import Image
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image as RLImage, PageBreak, Spacer

src, out, cache = sys.argv[1], sys.argv[2], sys.argv[3]
items = json.load(open(src))
os.makedirs(cache, exist_ok=True)
ss = getSampleStyleSheet()
W, H = A4
maxw, maxh = W - 30*mm, H - 110*mm

def fetch(it):
    p = os.path.join(cache, it["id"] + ".jpg")
    if not os.path.exists(p):
        raw = p + ".src"
        urllib.request.urlretrieve(it["url"], raw)
        im = Image.open(raw).convert("RGB"); im.thumbnail((1600, 1600)); im.save(p, quality=88)
        os.remove(raw)
    return p

ts = lambda t: datetime.datetime.fromtimestamp(t, datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%SZ")
story = [Paragraph(f"Higgsfield catalogue — {os.path.basename(src)}", ss["Title"]),
         Paragraph(f"{len(items)} images · {ts(min(i['createdAt'] for i in items))} to {ts(max(i['createdAt'] for i in items))}", ss["Normal"]),
         PageBreak()]
for n, it in enumerate(items, 1):
    p = fetch(it); iw, ih = Image.open(p).size
    s = min(maxw/iw, maxh/ih)
    story += [Paragraph(f"{n}. {ts(it['createdAt'])} · {it['ar']} · {it['model']} · ref {it.get('ref','')}", ss["Heading4"]),
              RLImage(p, iw*s, ih*s), Spacer(1, 4*mm),
              Paragraph(f"<font size=7>{it['id']}</font>", ss["Normal"]),
              Paragraph(f"<font size=8>{it['prompt']}</font>", ss["Normal"])]
    if n < len(items): story.append(PageBreak())
SimpleDocTemplate(out, pagesize=A4, leftMargin=15*mm, rightMargin=15*mm, topMargin=12*mm, bottomMargin=12*mm).build(story)
print(out)
