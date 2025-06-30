import json
from itertools import permutations

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

def optimize_layout(plant_pool, companion_data, rows, cols):
    best_layout = None
    best_score = float('-inf')
    for perm in set(permutations(plant_pool)):
        score = total_score(perm, companion_data, rows, cols)
        if score > best_score:
            best_score = score
            best_layout = perm
    best_grid = to_grid(best_layout, rows, cols)
    return best_grid, best_score
