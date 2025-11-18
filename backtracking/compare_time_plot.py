import matplotlib.pyplot as plt
import math
from utils import Timer, generate_network  # Assuming you have a generate_edges function

# Import your algorithm functions
from tsp_solve_backtracking import random_tour, greedy_tour, backtracking, backtracking_bssf


def plot_solution_stats(stats_list: list, label: str):
    """
    Helper function to plot a list of SolutionStats objects.
    Uses a step plot to show when the solution improves.
    """
    if not stats_list:
        print(f"No solutions found for {label}")
        return

    # Add a starting point at time 0 with infinity cost (or first solution)
    times = [0]
    scores = [stats_list[0].score]  # Start with the first found score

    # Extract time and score from each improving solution
    for stat in stats_list:
        times.append(stat.time)
        scores.append(stat.score)

    # Ensure the plot extends to the end of the time limit
    times.append(TIME_LIMIT)
    scores.append(scores[-1])  # Hold the last best score

    plt.step(times, scores, where='post', label=label)


# --- Main Plotting Script ---
if __name__ == "__main__":
    # --- Parameters ---
    N = 50  # Number of nodes (use 50 as recommended)
    TIME_LIMIT = 60  # 60 seconds
    SEED = 42  # Use the same seed for a fair comparison

    print(f"Generating graph with N={N}, Seed={SEED}...")
    # You must have a function to generate the graph
    # This function is in utils.py in the project skeleton
    locations, edges = generate_network(N, SEED)
    print("Graph generated.")

    # --- Run Algorithms ---
    print("Running Greedy...")
    greedy_stats = greedy_tour(edges, Timer(TIME_LIMIT))

    print("Running Random...")
    random_stats = random_tour(edges, Timer(TIME_LIMIT))

    print("Running BSSF Backtracking...")
    bssf_stats = backtracking_bssf(edges, Timer(TIME_LIMIT))

    print("Running Basic Backtracking (this will be very slow)...")
    # For N=50, this will not find a solution in 60s
    basic_stats = backtracking(edges, Timer(TIME_LIMIT))
    print("All algorithms complete.")

    # --- Create Plot ---
    plt.figure(figsize=(12, 8))

    plot_solution_stats(greedy_stats, "Greedy")
    plot_solution_stats(random_stats, "Random")
    plot_solution_stats(bssf_stats, "BSSF Backtracking")
    plot_solution_stats(basic_stats, "Basic Backtracking")

    plt.title(f"TSP Solution Cost vs. Time (N={N}, Time Limit={TIME_LIMIT}s)")
    plt.xlabel("Time (seconds)")
    plt.ylabel("Solution Cost (Best So Far)")
    plt.legend()
    plt.grid(True, which="both", ls="--", alpha=0.5)

    # Use a log scale on the y-axis to see differences better
    # especially if basic_stats is at infinity
    plt.yscale('log')

    plt.ylim(bottom=1)  # Set a reasonable lower limit for the log scale
    plt.xlim(0, TIME_LIMIT)

    print("Displaying plot...")
    plt.show()