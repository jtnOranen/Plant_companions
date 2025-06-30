import matplotlib.pyplot as plt

def plot_grid(grid, rows, cols, score, show=True):
    fig, ax = plt.subplots(figsize=(cols, rows))
    for r in range(rows):
        for c in range(cols):
            plant = grid[r][c]
            ax.text(c, rows-1-r, plant if plant else "", ha='center', va='center', fontsize=10)
            ax.add_patch(plt.Rectangle((c-0.5, rows-1-r-0.5), 1, 1, fill=False))
    ax.set_xlim(-0.5, cols-0.5)
    ax.set_ylim(-0.5, rows-0.5)
    ax.set_aspect('equal')
    plt.gca().invert_yaxis()
    plt.title(f"🌱 Best layout (Score: {score})")
    plt.axis('off')
    if show:
        plt.show()
    return fig
