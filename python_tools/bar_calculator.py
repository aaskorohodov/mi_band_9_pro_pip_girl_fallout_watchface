bar_length = 97

steps = {}
for percent in range(1, 101, 1):
    pixels = round(bar_length * (100 - percent) / 100)
    steps[percent] = pixels

for p, px in steps.items():
    print(f"{p}% -> {px} pixels")
