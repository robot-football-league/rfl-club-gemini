"""Generate high-quality identity assets for Gemini Flash FC."""

import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


def create_badge(path: Path):
    size = 512
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    center = size // 2
    r_outer = 230
    r_inner = 200

    # Outer glow ring
    for i in range(15):
        alpha = int(40 * (1 - i / 15))
        draw.ellipse(
            [center - r_outer - i, center - r_outer - i, center + r_outer + i, center + r_outer + i],
            outline=(0, 210, 255, alpha),
            width=2,
        )

    # Outer border circle - Electric Cyan & Indigo
    draw.ellipse(
        [center - r_outer, center - r_outer, center + r_outer, center + r_outer],
        fill=(10, 14, 26, 255),
        outline=(0, 210, 255, 255),
        width=8,
    )

    # Inner circle - Deep Space Blue
    draw.ellipse(
        [center - r_inner, center - r_inner, center + r_inner, center + r_inner],
        fill=(18, 30, 60, 255),
        outline=(30, 107, 255, 255),
        width=4,
    )

    # Background geometric grid / radial bursts
    for angle_deg in range(0, 360, 30):
        rad = math.radians(angle_deg)
        x1 = center + int(r_inner * 0.3 * math.cos(rad))
        y1 = center + int(r_inner * 0.3 * math.sin(rad))
        x2 = center + int(r_inner * 0.95 * math.cos(rad))
        y2 = center + int(r_inner * 0.95 * math.sin(rad))
        draw.line([(x1, y1), (x2, y2)], fill=(40, 70, 130, 120), width=2)

    # Central Gemini 4-pointed sparkle / diamond star
    # Outer diamond points
    p_top = (center, center - 120)
    p_bot = (center, center + 120)
    p_left = (center - 120, center)
    p_right = (center + 120, center)

    # Inner control curves for 4-point star
    c_tl = (center - 28, center - 28)
    c_tr = (center + 28, center - 28)
    c_bl = (center - 28, center + 28)
    c_br = (center + 28, center + 28)

    star_poly = [
        p_top, c_tr, p_right, c_br, p_bot, c_bl, p_left, c_tl
    ]

    # Star glow layers
    for expand in (16, 10, 5):
        glow_poly = []
        for x, y in star_poly:
            dx = (x - center) * (1 + expand / 100.0)
            dy = (y - center) * (1 + expand / 100.0)
            glow_poly.append((center + int(dx), center + int(dy)))
        draw.polygon(glow_poly, fill=(0, 229, 255, 40))

    # Star base fill - Google Blue / Cyan gradient simulation
    draw.polygon(star_poly, fill=(0, 210, 255, 255), outline=(255, 255, 255, 255))

    # Shaded halves for 3D gem look
    star_half_1 = [p_top, (center, center), p_left, c_tl]
    draw.polygon(star_half_1, fill=(255, 255, 255, 160))
    star_half_2 = [p_bot, (center, center), p_right, c_br]
    draw.polygon(star_half_2, fill=(30, 107, 255, 200))

    # Central bright spark
    draw.ellipse([center - 16, center - 16, center + 16, center + 16], fill=(255, 255, 255, 255))

    # Twin vertical bars / pillars (Gemini duality)
    bar_w = 8
    bar_h = 40
    draw.rectangle([center - 45 - bar_w, center - bar_h // 2, center - 45 + bar_w, center + bar_h // 2], fill=(242, 176, 30, 240))
    draw.rectangle([center + 45 - bar_w, center - bar_h // 2, center + 45 + bar_w, center + bar_h // 2], fill=(242, 176, 30, 240))

    # Top & Bottom Banners / Texts
    # Text fallback with PIL default font
    try:
        font_main = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 30)
        font_sub = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 20)
    except Exception:
        font_main = ImageFont.load_default()
        font_sub = ImageFont.load_default()

    # Draw Text Banners
    draw.text((center, center - 160), "GEMINI", fill=(255, 255, 255, 255), font=font_main, anchor="mm")
    draw.text((center, center + 160), "FLASH FC", fill=(0, 229, 255, 255), font=font_main, anchor="mm")
    draw.text((center, center + 185), "EST. 2026", fill=(242, 176, 30, 255), font=font_sub, anchor="mm")

    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path, format="PNG")
    print(f"Created badge: {path}")


def create_kit_home(path: Path):
    """Home Kit: Electric Gemini Blue with Cyan Speed Sashes and Crest."""
    size = 512
    img = Image.new("RGBA", (size, size), (31, 107, 235, 255))  # Electric Blue base
    draw = ImageDraw.Draw(img)

    # Deep navy side flank panels
    draw.polygon([(0, 0), (70, 0), (40, 512), (0, 512)], fill=(12, 22, 50, 255))
    draw.polygon([(512, 0), (442, 0), (472, 512), (512, 512)], fill=(12, 22, 50, 255))

    # Dynamic Diagonal Cyber Sashes in Cyan & White
    sash_color_cyan = (0, 229, 255, 240)
    sash_color_white = (255, 255, 255, 230)
    sash_color_glow = (0, 160, 255, 180)

    # Wide diagonal speed sash
    draw.polygon([(80, 0), (220, 0), (432, 512), (292, 512)], fill=sash_color_cyan)
    # Accent white pinstripes
    draw.polygon([(230, 0), (245, 0), (457, 512), (442, 512)], fill=sash_color_white)
    draw.polygon([(65, 0), (72, 0), (284, 512), (277, 512)], fill=sash_color_white)
    draw.polygon([(255, 0), (275, 0), (487, 512), (467, 512)], fill=sash_color_glow)

    # Collar design - Deep Navy V-neck with gold accent
    draw.polygon([(200, 0), (312, 0), (256, 75)], fill=(10, 14, 26, 255))
    draw.line([(200, 0), (256, 75), (312, 0)], fill=(242, 176, 30, 255), width=6)

    # Big Central Crest / Emblem on Chest
    center_x, center_y = 256, 260

    # Shield backing
    shield = [
        (center_x - 70, center_y - 70),
        (center_x + 70, center_y - 70),
        (center_x + 70, center_y + 20),
        (center_x, center_y + 85),
        (center_x - 70, center_y + 20),
    ]
    draw.polygon(shield, fill=(10, 14, 26, 255), outline=(0, 229, 255, 255), width=5)

    # Four-pointed spark inside shield
    p_top = (center_x, center_y - 50)
    p_bot = (center_x, center_y + 50)
    p_left = (center_x - 50, center_y)
    p_right = (center_x + 50, center_y)
    c_tl = (center_x - 12, center_y - 12)
    c_tr = (center_x + 12, center_y - 12)
    c_bl = (center_x - 12, center_y + 12)
    c_br = (center_x + 12, center_y + 12)
    star_poly = [p_top, c_tr, p_right, c_br, p_bot, c_bl, p_left, c_tl]
    draw.polygon(star_poly, fill=(0, 229, 255, 255), outline=(255, 255, 255, 255), width=2)
    draw.ellipse([center_x - 8, center_y - 8, center_x + 8, center_y + 8], fill=(255, 255, 255, 255))

    # Sponsor / Wordmark area below shield
    try:
        font_chest = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 32)
        font_sub = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 18)
    except Exception:
        font_chest = ImageFont.load_default()
        font_sub = ImageFont.load_default()

    draw.text((256, 390), "GEMINI", fill=(255, 255, 255, 255), font=font_chest, anchor="mm")
    draw.text((256, 422), "DEEPMIND", fill=(242, 176, 30, 255), font=font_sub, anchor="mm")

    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path, format="PNG")
    print(f"Created home kit: {path}")


def create_kit_away(path: Path):
    """Away Kit: Solar Amber / Gold with Obsidian Chevrons and Cyan Detailing."""
    size = 512
    # Solar Gold base
    img = Image.new("RGBA", (size, size), (242, 178, 30, 255))
    draw = ImageDraw.Draw(img)

    # Obsidian chevron stripes across the jersey
    stripe_dark = (18, 22, 34, 255)
    stripe_cyan = (0, 229, 255, 240)

    # Chevrons
    for y_offset in (-80, 40, 160, 280, 400):
        pts = [
            (0, y_offset + 50),
            (256, y_offset + 130),
            (512, y_offset + 50),
            (512, y_offset + 105),
            (256, y_offset + 185),
            (0, y_offset + 105),
        ]
        draw.polygon(pts, fill=stripe_dark)

        # Cyan border accent on chevron top
        draw.line([(0, y_offset + 50), (256, y_offset + 130), (512, y_offset + 50)], fill=stripe_cyan, width=4)

    # Dark Obsidian Collar
    draw.polygon([(200, 0), (312, 0), (256, 75)], fill=stripe_dark)
    draw.line([(200, 0), (256, 75), (312, 0)], fill=(0, 229, 255, 255), width=6)

    # Side Panels
    draw.polygon([(0, 0), (45, 0), (30, 512), (0, 512)], fill=stripe_dark)
    draw.polygon([(512, 0), (467, 0), (482, 512), (512, 512)], fill=stripe_dark)

    # Chest Crest
    center_x, center_y = 256, 260
    shield = [
        (center_x - 70, center_y - 70),
        (center_x + 70, center_y - 70),
        (center_x + 70, center_y + 20),
        (center_x, center_y + 85),
        (center_x - 70, center_y + 20),
    ]
    draw.polygon(shield, fill=stripe_dark, outline=(242, 178, 30, 255), width=5)

    # 4-point star in Solar Gold / White
    p_top = (center_x, center_y - 50)
    p_bot = (center_x, center_y + 50)
    p_left = (center_x - 50, center_y)
    p_right = (center_x + 50, center_y)
    c_tl = (center_x - 12, center_y - 12)
    c_tr = (center_x + 12, center_y - 12)
    c_bl = (center_x - 12, center_y + 12)
    c_br = (center_x + 12, center_y + 12)
    star_poly = [p_top, c_tr, p_right, c_br, p_bot, c_bl, p_left, c_tl]
    draw.polygon(star_poly, fill=(242, 178, 30, 255), outline=(255, 255, 255, 255), width=2)
    draw.ellipse([center_x - 8, center_y - 8, center_x + 8, center_y + 8], fill=(255, 255, 255, 255))

    # Text
    try:
        font_chest = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 32)
        font_sub = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 18)
    except Exception:
        font_chest = ImageFont.load_default()
        font_sub = ImageFont.load_default()

    draw.text((256, 390), "GEMINI", fill=stripe_dark, font=font_chest, anchor="mm")
    draw.text((256, 422), "FLASH FC", fill=(0, 229, 255, 255), font=font_sub, anchor="mm")

    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path, format="PNG")
    print(f"Created away kit: {path}")


if __name__ == "__main__":
    here = Path(__file__).resolve().parent.parent
    ident = here / "identity"
    create_badge(ident / "badge.png")
    create_kit_home(ident / "kit_home.png")
    create_kit_away(ident / "kit_away.png")
