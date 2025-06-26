min_bpm = 50
max_bpm = 200
steps = 21

bpm_values = []
for i in range(steps):
    bpm = min_bpm + i * (max_bpm - min_bpm) / (steps - 1)
    bpm_values.append(round(bpm))

for i, bpm in enumerate(bpm_values):
    print(f"{i*5}% -> {bpm} BPM")
