import math

import matplotlib.pyplot as plt
import numpy as np
from utils import Timer, generate_network
from tsp_solve_backtracking import backtracking, backtracking_bssf, greedy_tour, random_tour


def plot_results(solutions_reg, solutions_bssf, solutions_greedy, solutions_random, wall_time):
    """
    Plots the solution cost vs time for all 4 algorithms.
    Style: Scatter plot (dots), Y-axis increments by 5.
    Adjusted to zoom in and clearly show each dot.
    """
    plt.figure(figsize=(12, 8))

    def get_points(solutions):
        x = []
        y = []
        if not solutions:
            return x, y

        iterable_solutions = solutions if isinstance(solutions, list) else [solutions]

        for sol in iterable_solutions:
            if hasattr(sol, 'time'):
                x.append(sol.time)
            else:
                x.append(0)
            y.append(sol.score)
        return x, y

    # Extract points
    x_reg, y_reg = get_points(solutions_reg)
    x_bssf, y_bssf = get_points(solutions_bssf)
    x_greedy, y_greedy = get_points(solutions_greedy)
    x_rand, y_rand = get_points(solutions_random)

    # Plot Greedy (Blue)
    if x_greedy:
        plt.scatter(x_greedy, y_greedy, color='blue', label='Greedy', marker='o', s=60, zorder=5)

    # Plot Random (Orange)
    if x_rand:
        plt.scatter(x_rand, y_rand, color='orange', label='Random', marker='.', s=50)

    # Plot Regular Backtracking (Red)
    if x_reg:
        plt.scatter(x_reg, y_reg, color='red', label='Regular Backtracking', marker='.', s=50)

    # Plot BSSF Backtracking (Green)
    if x_bssf:
        plt.scatter(x_bssf, y_bssf, color='green', label='BSSF Backtracking', marker='.', s=50)

    # --- Dynamic Zooming and Y-Axis Styling (Integers, Increment by 5) ---
    all_times = x_reg + x_bssf + x_greedy + x_rand
    all_scores = y_reg + y_bssf + y_greedy + y_rand

    if all_scores:
        # Y-axis limits
        min_cost = math.floor(min(all_scores))
        max_cost = math.ceil(max(all_scores))

        # Ensure y_min starts at 0 or below, and pad max_cost
        y_min_plot = max(0, min_cost - 2)  # Start at 0 or slightly below min cost
        y_max_plot = max_cost + 2  # Pad max cost slightly

        # Calculate ticks starting from a multiple of 5, or 0 if appropriate
        start_tick = (y_min_plot // 5) * 5
        if start_tick > y_min_plot:  # if start_tick is just above y_min_plot, go down one step
            start_tick -= 5

        end_tick = ((y_max_plot // 5) + 1) * 5

        yticks = np.arange(start_tick, end_tick + 1, 5)  # +1 to ensure end_tick is included
        plt.yticks(yticks)
        plt.ylim(y_min_plot, y_max_plot)  # Apply calculated Y limits

    # X-axis limits
    if all_times:
        max_time_data = max(all_times)
        # Set x_max to slightly beyond the last data point, but not more than wall_time
        x_max_plot = min(wall_time, max_time_data * 1.1 + 1)  # 10% padding + 1 second

        # Add a small negative padding (2% of the range) so points at x=0 are fully visible
        # instead of being cut in half by the axis line.
        x_padding = x_max_plot * 0.02
        plt.xlim(-x_padding, x_max_plot)

    plt.grid(True, linestyle='--', alpha=0.6)
    plt.xlabel("Time (seconds)")
    plt.ylabel("Cost (Increments of 5)")
    plt.title(f"TSP Solution Cost vs. Time (Dots - Zoomed)")
    plt.legend()

    output_file = "tsp_plot_dots_zoomed.png"
    plt.savefig(output_file)
    print(f"\nPlot saved to: {output_file}")


def main():
    # --- Configuration ---
    N_CITIES = 15
    TIME_LIMIT_SEC = 60
    GRAPH_SEED = 42
    # ---------------------

    print("... TSP Algorithm Comparison ...")
    print(f"Settings: N={N_CITIES}, Time Limit={TIME_LIMIT_SEC}s, Seed={GRAPH_SEED}")

    locations, edges = generate_network(
        N_CITIES,
        euclidean=True,
        reduction=0.2,
        normal=False,
        seed=GRAPH_SEED,
    )

    # ... Run 1: Greedy ...
    print("\n... Greedy ...")
    timer_greedy = Timer(TIME_LIMIT_SEC)
    solutions_greedy = greedy_tour(edges, timer_greedy)

    if solutions_greedy:
        if isinstance(solutions_greedy, list):
            print(f"Cost: {solutions_greedy[-1].score}")
        else:
            print(f"Cost: {solutions_greedy.score}")
            solutions_greedy = [solutions_greedy]
    else:
        print("Cost: None")

    # ... Run 2: Random ...
    print("\n... Random ...")
    timer_rand = Timer(TIME_LIMIT_SEC)
    solutions_random = random_tour(edges, timer_rand)

    if solutions_random:
        if isinstance(solutions_random, list):
            print(f"Cost: {solutions_random[-1].score}")
        else:
            print(f"Cost: {solutions_random.score}")
            solutions_random = [solutions_random]
    else:
        print("Cost: None")

    # ... Run 3: Regular Backtracking ...
    print("\n... Regular Backtracking ...")
    timer_reg = Timer(TIME_LIMIT_SEC)
    solutions_reg = backtracking(edges, timer_reg)
    if solutions_reg:
        best_score_reg = solutions_reg[-1].score
        print(f"Cost: {best_score_reg}")
    else:
        best_score_reg = math.inf
        print("Cost: None")

    # ... Run 4: BSSF Backtracking ...
    print("\n... BSSF Backtracking ...")
    timer_bssf = Timer(TIME_LIMIT_SEC)
    solutions_bssf = backtracking_bssf(edges, timer_bssf)
    if solutions_bssf:
        best_score_bssf = solutions_bssf[-1].score
        print(f"Cost: {best_score_bssf}")
    else:
        best_score_bssf = math.inf
        print("Cost: None")

    # ... Generate Plot ...
    print("\n... Generating Plot ...")
    plot_results(solutions_reg, solutions_bssf, solutions_greedy, solutions_random, TIME_LIMIT_SEC)


if __name__ == "__main__":
    main()