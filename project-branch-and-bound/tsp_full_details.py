import matplotlib.pyplot as plt

from tsp_core import (generate_network, Timer, Solver)
from tsp_plot import (plot_network, plot_tour, plot_solutions, plot_coverage,
                      plot_queue_size,
                      plot_solution_evolution,
                      plot_edge_probability)
from tsp_run import format_text_summary, format_plot_summary
from tsp_solve import (random_tour, greedy_tour, dfs, branch_and_bound, branch_and_bound_smart)


def main(n, solvers: list, timeout=60, **kwargs):
    # 1. Generate network
    print(f'Generating network of size {n} with args: {kwargs}')
    locations, edges = generate_network(n, **kwargs)

    all_stats = {}

    # 2. Run Solvers
    for find_tour in solvers:
        name = find_tour.__name__
        print(f"Running {name}...")

        timer = Timer(timeout)
        stats = find_tour(edges, timer)

        # Safety check for None returns
        if stats is None:
            stats = []

        all_stats[name] = stats

        if stats:
            print(format_text_summary(name, stats[-1]))
        print(f'Total solutions found: {len(stats)}\n')

    # 3. Report and Plot
    n_plots = 3
    fig, axs = plt.subplots(n_plots, 1, figsize=(10, 18))

    # --- Plot 1: Solution Quality (Cost) ---
    # CHANGED: Swapped plot_coverage for plot_solutions
    plot_solutions(all_stats, ax=axs[0])
    axs[0].set_title(f"Solution Quality (Cost vs Time) (N={n})")
    axs[0].set_ylabel("Cost (Lower is Better)")

    # Annotate Final Cost
    for name, stats in all_stats.items():
        if stats:
            last_stat = stats[-1]
            final_score = last_stat.score
            final_time = last_stat.time

            # Label point with the final cost
            axs[0].annotate(f"{final_score:.1f}", xy=(final_time, final_score),
                            xytext=(5, 5), textcoords='offset points', fontweight='bold')

    # --- Plot 2: Queue Size ---
    plot_queue_size(all_stats, ax=axs[1])
    axs[1].set_title("Max Queue Size over Time")

    # --- Plot 3: Edge Probability ---
    plot_edge_probability(all_stats, edges, ax=axs[2])
    axs[2].set_title("Edge Probability (Consensus on Best Paths)")

    plt.tight_layout()
    plt.savefig('stretch1_full_analysis.png', dpi=300)
    print("Graph saved as 'stretch1_full_analysis.png'")
    plt.show()


if __name__ == '__main__':
    main(
        10,  # Keep N small (10-12) so DFS finishes
        [dfs, branch_and_bound],
        euclidean=True,
        reduction=0.2,
        normal=False,
        seed=350,
        timeout=60
    )