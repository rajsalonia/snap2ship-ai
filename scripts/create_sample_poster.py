"""Draw an original, explicitly fictional, non-sensitive demo poster."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
image = Image.new("RGB", (1000, 1320), "#e9efda")
draw = ImageDraw.Draw(image)


def font(size, bold=False):
    candidates = [Path("C:/Windows/Fonts") / ("arialbd.ttf" if bold else "arial.ttf"),
                  Path("/usr/share/fonts/truetype/dejavu") / ("DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf")]
    for path in candidates:
        if path.is_file():
            return ImageFont.truetype(str(path), size)
    return ImageFont.load_default(size=size)


draw.rounded_rectangle((45, 40, 955, 1280), radius=35, fill="#254e40")
draw.text((92, 90), "THE STUDENT COMMUNITY PRESENTS", font=font(22, True), fill="#d9ed99")
draw.text((87, 170), "CAMPUS", font=font(105, True), fill="#f7f5e8")
draw.text((87, 280), "CREATE DAY", font=font(105, True), fill="#d9ed99")
draw.text((93, 438), "14 NOVEMBER 2026", font=font(43, True), fill="#f7f5e8")
draw.text((93, 505), "Student Activity Centre", font=font(32), fill="#bdcfb4")
draw.line((93, 590, 905, 590), fill="#68846a", width=2)
for y, when, title in [(645, "10:00 AM", "Design Jam"), (790, "12:00 PM", "Web Workshop"), (935, "3:00 PM", "Project Showcase")]:
    draw.text((93, y), when, font=font(23, True), fill="#d9ed99")
    draw.text((93, y + 40), title, font=font(42, True), fill="#f7f5e8")
draw.rounded_rectangle((90, 1100, 910, 1180), radius=15, fill="#d9ed99")
draw.text((120, 1120), "BRING A LAPTOP + STUDENT ID", font=font(29, True), fill="#254e40")
draw.text((105, 1220), "FICTIONAL SAMPLE POSTER - FOR DEMONSTRATION ONLY", font=font(19, True), fill="#bdcfb4")
for destination in [ROOT / "frontend/public/sample-poster.png", ROOT / "examples/sample-poster.png"]:
    destination.parent.mkdir(parents=True, exist_ok=True)
    image.save(destination, optimize=True)
print("Created original fictional sample poster (1000 x 1320).")
