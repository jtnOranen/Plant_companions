import json
from itertools import permutations

def normalize_plant_name(name):
    return name.strip().capitalize()

plant_pool = []
max_plants = 9

# === Load companion data ===
with open("companion_plants_full.json", "r", encoding="utf-8") as f:
    companion_data = json.load(f)

print("Enter up to 9 plant names. Type 'exit' to finish early.")

for i in range(max_plants):
    raw_input = input(f"Enter plant #{i+1}: ").strip()
    if raw_input.lower() == "exit":
        break
    if raw_input == "":
        print("Empty input. Please enter a valid plant name.")
        continue
    normalized = normalize_plant_name(raw_input)
    if normalized not in companion_data:
        print("Name not in list, it will be given neutral values")
    plant_pool.append(normalized)

# Fill the rest with None
while len(plant_pool) < max_plants:
    plant_pool.append(None)

print("\nYour normalized plant pool:")
print(plant_pool)

# === Helper to convert 1D list into 3x3 grid ===
def to_grid(layout):
    return [layout[i*3:(i+1)*3] for i in range(3)]

def get_neighbors(grid, target_row, target_col):
    neighbors = []
    for row_offset in [-1, 0, 1]:
        for col_offset in [-1, 0, 1]:
            if row_offset == 0 and col_offset == 0:
                continue  # Skip the target cell itself
            neighbor_row = target_row + row_offset
            neighbor_col = target_col + col_offset
            if 0 <= neighbor_row < 3 and 0 <= neighbor_col < 3:
                neighbors.append(grid[neighbor_row][neighbor_col])
    return neighbors


# === Score a single cell ===
def score_cell(grid, row, col, companion_data):
    plant = grid[row][col]
    if not plant:
        return 0
    neighbors = get_neighbors(grid, row, col)
    good = companion_data.get(plant, {}).get("good", [])
    bad = companion_data.get(plant, {}).get("bad", [])
    
    score = 0
    for n in neighbors:
        if not n:
            continue
        if n in good:
            score += 1
        elif n in bad:
            score -= 1
    return score

# === Score an entire 3x3 layout ===
def total_score(layout, companion_data):
    grid = to_grid(layout)
    return sum(score_cell(grid, r, c, companion_data) for r in range(3) for c in range(3))

# === Try all permutations ===
best_layout = None
best_score = float('-inf')

for perm in set(permutations(plant_pool)):
    score = total_score(perm, companion_data)
    if score > best_score:
        best_score = score
        best_layout = perm

# === Show result ===
best_grid = to_grid(best_layout)

print("\n🌱 Best layout:")
for row in best_grid:
    print(row)

print(f"\nTotal score: {best_score}")

print("\n📊 Individual cell scores:")
for row in range(3):
    row_scores = []
    for col in range(3):
        score = score_cell(best_grid, row, col, companion_data)
        row_scores.append(f"{score:>3}")  # Right-align for clarity
    print(" | ".join(row_scores))
