import os
from lxml import etree
import cairosvg

INPUT_SVG = "C:\\Users\\max\\Desktop\\Real Estate Blueprint Analyzer\\cubicasa5k\\high_quality_architectural\\164\\model.svg"
ORIGINAL_DIR = "original"
MASKED_DIR = "masked"

FURNITURE_CLASSES = [
    "FixedFurniture",
    "Sink",
    "Closet",
    "Toilet",
    "Bathtub",
    "Cabinet",
    "Wardrobe"
]

FURNITURE_IDS = [
    "FixedFurnitureSet"
]

os.makedirs(ORIGINAL_DIR, exist_ok=True)
os.makedirs(MASKED_DIR, exist_ok=True)

original_png_path = os.path.join(ORIGINAL_DIR, "original.png")
cairosvg.svg2png(url=INPUT_SVG, write_to=original_png_path)
print(f"Original saved → {original_png_path}")

parser = etree.XMLParser(remove_blank_text=True)
tree = etree.parse(INPUT_SVG, parser)
root = tree.getroot()

# Extract namespace
nsmap = root.nsmap.copy()
ns = {"svg": nsmap.get(None)} if None in nsmap else {}

for furniture_id in FURNITURE_IDS:
    elements = root.xpath(f"//*[@id='{furniture_id}']", namespaces=ns)
    for el in elements:
        parent = el.getparent()
        if parent is not None:
            parent.remove(el)

for cls in FURNITURE_CLASSES:
    elements = root.xpath(f"//*[contains(@class, '{cls}')]", namespaces=ns)
    for el in elements:
        parent = el.getparent()
        if parent is not None:
            parent.remove(el)


temp_svg = "temp_cleaned.svg"
tree.write(temp_svg)

masked_png_path = os.path.join(MASKED_DIR, "masked.png")
cairosvg.svg2png(url=temp_svg, write_to=masked_png_path)
print(f"Masked saved → {masked_png_path}")

os.remove(temp_svg)

print("Furniture removal completed successfully.")
