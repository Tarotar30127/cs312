import matplotlib.pyplot as plt


def plot_stretch2_metrics(stats, algo_name="Backtracking BSSF"):
    # 1. Sort the stats by time so the line plot connects points in order
    stats.sort(key=lambda x: x.time)

    times = [s.time for s in stats]
    max_queues = [s.max_queue_size for s in stats]
    nodes_expanded = [s.n_nodes_expanded for s in stats]
    nodes_pruned = [s.n_nodes_pruned for s in stats]
    leaves_covered = [s.fraction_leaves_covered for s in stats]

    fig, axs = plt.subplots(2, 2, figsize=(13, 9))
    axs = axs.flatten()

    # Plot 1: Max Queue
    axs[0].plot(times, max_queues, marker='o', linestyle='-')
    axs[0].set_title(f"Max Queue Size vs Time\n({algo_name})")
    axs[0].set_xlabel("Time (s)")
    axs[0].set_ylabel("Max Queue Size")
    axs[0].grid(True, which='both', linestyle='--', linewidth=0.5)

    # Plot 2: Nodes Expanded
    axs[1].plot(times, nodes_expanded, marker='o', color='green', linestyle='-')
    axs[1].set_title(f"Nodes Expanded vs Time\n({algo_name})")
    axs[1].set_xlabel("Time (s)")
    axs[1].set_ylabel("# Nodes Expanded")
    axs[1].grid(True, which='both', linestyle='--', linewidth=0.5)

    # Plot 3: Nodes Pruned
    axs[2].plot(times, nodes_pruned, marker='o', color='red', linestyle='-')
    axs[2].set_title(f"Nodes Pruned vs Time\n({algo_name})")
    axs[2].set_xlabel("Time (s)")
    axs[2].set_ylabel("# Nodes Pruned")
    axs[2].grid(True, which='both', linestyle='--', linewidth=0.5)

    # Plot 4: Fraction Leaves
    axs[3].plot(times, leaves_covered, marker='o', color='purple', linestyle='-')
    axs[3].set_title(f"Fraction Leaves Covered vs Time\n({algo_name})")
    axs[3].set_xlabel("Time (s)")
    axs[3].set_ylabel("Fraction Leaves Covered")
    axs[3].grid(True, which='both', linestyle='--', linewidth=0.5)

    plt.tight_layout()
    plt.savefig("stretch2_plots.png")
    plt.show()


if __name__ == '__main__':
    from tsp_solve_backtracking import backtracking_bssf
    from utils import generate_network, Timer
    import random

    # --- MODIFIED SECTION START ---

    all_stats = []

    # We loop through a range of city sizes (e.g., 10 to 15)
    # This creates problems of increasing difficulty to fill the graphs
    print("Running experiments...")

    # Depending on your algorithm speed, adjust this range.
    # Backtracking is O(n!), so small increases in N create large time jumps.
    size_range = range(10, 18)

    for n in size_range:
        # Use a random seed per N to get variation, or fixed to be reproducible
        seed = 42 + n
        locations, edges = generate_network(n, reduction=0.2, seed=seed)

        # Run the solver
        # We give it a generous time limit so larger N's can finish
        run_stats = backtracking_bssf(edges, Timer(60))

        # Assuming 'run_stats' is a list (even if it only has 1 item)
        # We extend our master list with these results
        if isinstance(run_stats, list):
            all_stats.extend(run_stats)
        else:
            # Fallback if your function returns a single object instead of a list
            all_stats.append(run_stats)

        print(f"Finished n={n}")

    # Plot the aggregated data from all runs
    plot_stretch2_metrics(all_stats, algo_name="Backtracking BSSF")
