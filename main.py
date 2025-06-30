import json
from itertools import permutations

# === Helpers ===

def normalize_plant_name(name):
    return name.strip().capitalize()

def to_grid(layout, rows, cols):
    return [layout[i*cols:(i+1)*cols] for i in range(rows)]

def get_neighbors(grid, row, col):
    neighbors = []
    rows, cols = len(grid), len(grid[0])
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            nr, nc = row + dr, col + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                neighbors.append(grid[nr][nc])
    return neighbors

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

def total_score(layout, companion_data, rows, cols):
    grid = to_grid(layout, rows, cols)
    return sum(score_cell(grid, r, c, companion_data) for r in range(rows) for c in range(cols))

# === The function we can import ===

def run_optimizer():
    # Load companion data
    with open("companion_plants_full.json", "r", encoding="utf-8") as f:
        companion_data = json.load(f)

    # Ask for grid dimensions
    rows = int(input("Enter number of rows: "))
    cols = int(input("Enter number of columns: "))
    total_cells = rows * cols

    # Fill plant pool
    plant_pool = []
    print(f"Enter up to {total_cells} plant names. Type 'exit' to finish early.")
    for i in range(total_cells):
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

    # Fill remaining with None
    while len(plant_pool) < total_cells:
        plant_pool.append(None)

    # Optimize
    best_layout = None
    best_score = float('-inf')
    for perm in set(permutations(plant_pool)):
        score = total_score(perm, companion_data, rows, cols)
        if score > best_score:
            best_score = score
            best_layout = perm

    best_grid = to_grid(best_layout, rows, cols)
    return best_grid, rows, cols, best_score

# === Only print if run directly ===
if __name__ == "__main__":
    grid, rows, cols, score = run_optimizer()
    print("\n🌱 Best layout:")
    for row in grid:
        print(row)

    print(f"\nTotal score: {score}")
    print("\n📊 Individual cell scores:")
    for r in range(rows):
        row_scores = []
        for c in range(cols):
            s = score_cell(grid, r, c, {})
            row_scores.append(f"{s:>3}")
        print(" | ".join(row_scores))