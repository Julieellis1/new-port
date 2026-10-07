#!/usr/bin/env python3
"""Dark macOS browser mockup cover for the DollyTeens demo (matches existing work-*.png covers)."""
import os, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1600, 1200
RADIUS = 22
TITLE_H = 78
WIN_W = 1460
TOP_MARGIN = 70
CAPTION_Y = 1105

FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONTB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
url_font = ImageFont.truetype(FONT, 27)
cap_font = ImageFont.truetype(FONTB, 42)

BG = (13, 13, 15)
TITLE_BG = (38, 38, 43)
PILL_BG = (22, 22, 26)
LINE = (70, 70, 78)

def backdrop(w, h):
    img = Image.new("RGB", (w, h), BG)
    d = ImageDraw.Draw(img)
    glow = Image.new("L", (w, h), 0)
    gd = ImageDraw.Draw(glow)
    gd.ellipse([w//2 - 700, h//2 - 500, w//2 + 700, h//2 + 500], fill=26)
    glow = glow.filter(ImageFilter.GaussianBlur(220))
    img = Image.composite(Image.new("RGB", (w, h), (30, 30, 34)), img, glow)
    return img

def draw_tracked(d, cx, y, text, font, fill, tracking=10):
    widths = [d.textlength(ch, font=font) for ch in text]
    total = sum(widths) + tracking * (len(text) - 1)
    x = cx - total / 2
    for ch, wch in zip(text, widths):
        d.text((x, y), ch, font=font, fill=fill)
        x += wch + tracking

def mockup(src_path, url, caption, out_path):
    shot = Image.open(src_path).convert("RGB")
    scale = WIN_W / shot.width
    shot = shot.resize((WIN_W, int(shot.height * scale)), Image.LANCZOS)
    shot_w, shot_h = shot.size
    win_h = TITLE_H + shot_h

    window = Image.new("RGBA", (WIN_W, win_h), (0, 0, 0, 0))
    d = ImageDraw.Draw(window)
    d.rounded_rectangle([0, 0, WIN_W - 1, win_h - 1], radius=RADIUS, fill=(20, 20, 22, 255))
    d.rounded_rectangle([0, 0, WIN_W - 1, TITLE_H + RADIUS], radius=RADIUS, fill=TITLE_BG + (255,))
    d.rectangle([0, TITLE_H, WIN_W, TITLE_H + RADIUS], fill=TITLE_BG + (255,))
    d.line([(0, TITLE_H), (WIN_W, TITLE_H)], fill=LINE + (255,), width=2)
    for i, col in enumerate([(255, 95, 87), (254, 188, 46), (40, 200, 64)]):
        x = 40 + i * 40
        d.ellipse([x - 12, TITLE_H // 2 - 12, x + 12, TITLE_H // 2 + 12], fill=col + (255,))
    pill_w = 560
    px0 = (WIN_W - pill_w) // 2
    d.rounded_rectangle([px0, TITLE_H // 2 - 24, px0 + pill_w, TITLE_H // 2 + 24], radius=24, fill=PILL_BG + (255,))
    bb = d.textbbox((0, 0), url, font=url_font)
    d.text((px0 + (pill_w - (bb[2] - bb[0])) / 2, TITLE_H // 2 - (bb[3] - bb[1]) / 2 - bb[1]),
           url, font=url_font, fill=(150, 150, 158, 255))
    mask = Image.new("L", (WIN_W, win_h), 0)
    md = ImageDraw.Draw(mask)
    md.rounded_rectangle([0, 0, WIN_W - 1, win_h - 1], radius=RADIUS, fill=255)
    body = Image.new("RGBA", (WIN_W, win_h), (20, 20, 22, 255))
    body.paste(shot, (0, TITLE_H))
    window = Image.alpha_composite(window, Image.composite(body, Image.new("RGBA", window.size, (0, 0, 0, 0)), mask))
    d = ImageDraw.Draw(window)
    d.rounded_rectangle([0, 0, WIN_W - 1, TITLE_H + RADIUS], radius=RADIUS, fill=TITLE_BG + (255,))
    d.rectangle([0, TITLE_H, WIN_W, TITLE_H + RADIUS], fill=TITLE_BG + (255,))
    d.line([(0, TITLE_H), (WIN_W, TITLE_H)], fill=LINE + (255,), width=2)
    for i, col in enumerate([(255, 95, 87), (254, 188, 46), (40, 200, 64)]):
        x = 40 + i * 40
        d.ellipse([x - 12, TITLE_H // 2 - 12, x + 12, TITLE_H // 2 + 12], fill=col + (255,))
    d.rounded_rectangle([px0, TITLE_H // 2 - 24, px0 + pill_w, TITLE_H // 2 + 24], radius=24, fill=PILL_BG + (255,))
    d.text((px0 + (pill_w - (bb[2] - bb[0])) / 2, TITLE_H // 2 - (bb[3] - bb[1]) / 2 - bb[1]),
           url, font=url_font, fill=(150, 150, 158, 255))
    d.rounded_rectangle([1, 1, WIN_W - 2, win_h - 2], radius=RADIUS, outline=(85, 85, 95, 255), width=2)

    canvas = backdrop(W, H).convert("RGBA")
    ox = (W - WIN_W) // 2
    canvas.paste(window, (ox, TOP_MARGIN), window)
    d = ImageDraw.Draw(canvas)
    draw_tracked(d, W // 2, CAPTION_Y, caption, cap_font, (245, 245, 247, 255), tracking=12)
    canvas.convert("RGB").save(out_path)
    print("saved", out_path)

if __name__ == "__main__":
    src = sys.argv[1]
    out = os.path.expanduser("~/workspace/new-port-repo/assets/img/work-dollyteens.png")
    mockup(src, "dollyteens.school", "DOLLYTEENS \u00b7 KIDDIES COLLEGE", out)
