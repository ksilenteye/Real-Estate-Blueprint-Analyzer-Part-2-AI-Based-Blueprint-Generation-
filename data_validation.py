import os
import cv2
import numpy as np

DATASET_DIR = "processed_dataset"
ORIGINAL_DIR = os.path.join(DATASET_DIR, "original")
MASKED_DIR = os.path.join(DATASET_DIR, "masked")

original_files = sorted(os.listdir(ORIGINAL_DIR))
masked_files = sorted(os.listdir(MASKED_DIR))

print(f"Total Original: {len(original_files)}")
print(f"Total Masked: {len(masked_files)}")

if len(original_files) != len(masked_files):
    print(" Mismatch in number of files.")
else:
    print(" File counts match.")

size_issues = []
difference_issues = []

for filename in original_files:

    orig_path = os.path.join(ORIGINAL_DIR, filename)
    mask_path = os.path.join(MASKED_DIR, filename)

    if not os.path.exists(mask_path):
        print(f" Missing masked file for {filename}")
        continue

    original = cv2.imread(orig_path)
    masked = cv2.imread(mask_path)

    # Size check
    if original.shape != masked.shape:
        size_issues.append(filename)

    # Difference check
    diff = cv2.absdiff(original, masked)
    diff_gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    nonzero = np.count_nonzero(diff_gray)

    # If difference too small, maybe nothing was removed
    if nonzero < 100:
        difference_issues.append(filename)

print("\n----- VALIDATION REPORT -----")

if size_issues:
    print(f" Size mismatch in {len(size_issues)} files")
else:
    print(" All image sizes consistent")

if difference_issues:
    print(f" Possible no-furniture-removed in {len(difference_issues)} files")
else:
    print(" Furniture differences detected properly")

print("Validation complete.")
