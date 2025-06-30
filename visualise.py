import matplotlib.pyplot as plt
from main import run_optimizer

def plot_grid(grid, rows, cols, score):
    fig, ax = plt.subplots(figsize=(cols, rows))
    for r in range(rows):
        for c in range(cols):
            plant = grid[r][c]
            # draw plant name
            ax.text(c, rows-1-r, plant if plant else "", 
                    ha='center', va='center', fontsize=10)
            # draw rectangle around the cell
            ax.add_patch(plt.Rectangle((c-0.5, rows-1-r-0.5), 1, 1, 
                                       fill=False, linewidth=1))
    ax.set_xlim(-0.5, cols-0.5)
    ax.set_ylim(-0.5, rows-0.5)
    ax.set_aspect('equal')
    plt.gca().invert_yaxis()
    plt.title(f"🌱 Best layout (Score: {score})")
    plt.axis('off')
    plt.show()

if __name__ == "__main__":
    grid, rows, cols, score = run_optimizer()
    plot_grid(grid, rows, cols, score)
