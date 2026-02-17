import cv2
import numpy as np
from pathlib import Path
import json
from tqdm import tqdm

class CubiCasaMasker:
    def __init__(self,
                 dataset_root="cubicasa5k/high_quality_architectural",
                 output_root="cubicasa_processed"):

        self.dataset_root = Path(dataset_root)
        self.output_root = Path(output_root)

        self.masked_dir = self.output_root / "masked"
        self.original_dir = self.output_root / "original"

        self.masked_dir.mkdir(parents=True, exist_ok=True)
        self.original_dir.mkdir(parents=True, exist_ok=True)

    def mask_furniture(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Mask non-white, non-black areas (likely furniture)
        furniture_mask = (gray > 30) & (gray < 220)

        masked = image.copy()
        masked[furniture_mask] = [255, 255, 255]

        return masked

    def process(self):
        metadata = []
        idx = 0

        for sample_dir in tqdm(sorted(self.dataset_root.iterdir())):
            if not sample_dir.is_dir():
                continue

            # Find all scaled floor images
            scaled_images = list(sample_dir.glob("*_scaled.png"))

            for img_path in scaled_images:
                image = cv2.imread(str(img_path))
                masked = self.mask_furniture(image)

                save_name = f"plan_{idx:05d}.png"

                masked_path = self.masked_dir / save_name
                original_path = self.original_dir / save_name

                cv2.imwrite(str(masked_path), masked)
                cv2.imwrite(str(original_path), image)

                metadata.append({
                    "id": idx,
                    "conditioning_image": str(masked_path),
                    "target_image": str(original_path),
                    "source_folder": sample_dir.name,
                    "floor_image": img_path.name
                })

                idx += 1

        with open(self.output_root / "metadata.json", "w") as f:
            json.dump(metadata, f, indent=2)

        print("Processing complete.")

if __name__ == "__main__":
    masker = CubiCasaMasker(
        dataset_root="cubicasa5k/high_quality_architectural",
        output_root="cubicasa_processed"
    )
    masker.process()
