"""Calculates length for progress-bars.

Answers the question:
- How many pixels should a bar be, to represents this much of percentage"""


bar_length = 97  # In pixels. How long should a bar be, when its in 100%

steps = {}
for percent in range(1, 101, 1):
    pixels = round(bar_length * (100 - percent) / 100)
    steps[percent] = pixels

for p, px in steps.items():
    print(f"{p}% -> {px} pixels")
