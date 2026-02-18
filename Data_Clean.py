"""
This script processes the CubiCasa5K dataset by removing furniture elements from the SVG files and saving both the original and masked versions as PNG images. It uses the lxml library to parse and modify the SVG files, and cairosvg to convert them to PNG format.
Author: Kavya Bhardwaj
Test no. = 3
Final Cut
"""
import os
from lxml import etree
import cairosvg

ROOT_DIR = r"cubicasa5k\high_quality_architectural"
OUTPUT_DIR = "processed_dataset"

ORIGINAL_DIR = os.path.join(OUTPUT_DIR, "original")
MASKED_DIR = os.path.join(OUTPUT_DIR, "masked")

os.makedirs(ORIGINAL_DIR, exist_ok=True)
os.makedirs(MASKED_DIR, exist_ok=True)

FURNITURE_CLASSES = [
    "FixedFurniture",
    "Sink",
    "Closet",
    "Toilet",
    "Bathtub",
    "Cabinet",
    "Wardrobe"
]

FURNITURE_IDS = ["FixedFurnitureSet"]


def remove_furniture(svg_path):
    parser = etree.XMLParser(remove_blank_text=True)
    tree = etree.parse(svg_path, parser)
    root = tree.getroot()

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
    return tree

failed = []

for folder in os.listdir(ROOT_DIR):
    folder_path = os.path.join(ROOT_DIR, folder)
    svg_path = os.path.join(folder_path, "model.svg")

    if not os.path.isdir(folder_path):
        continue
    if not os.path.exists(svg_path):
        continue

    print(f"Processing → {folder}")

    try:
        original_output = os.path.join(ORIGINAL_DIR, f"{folder}.png")
        cairosvg.svg2png(url=svg_path, write_to=original_output)

        cleaned_tree = remove_furniture(svg_path)

        temp_svg = os.path.join(folder_path, "temp_cleaned.svg")
        cleaned_tree.write(temp_svg)

        masked_output = os.path.join(MASKED_DIR, f"{folder}.png")
        cairosvg.svg2png(url=temp_svg, write_to=masked_output)

        os.remove(temp_svg)
    except Exception as e:
        print(f"Failed → {folder} | {e}")
        failed.append(folder)
print("\n Dataset processing complete.")
print(f"Total Failed: {len(failed)}")
