import math

from backtracking.utils import generate_network, Timer


def generate_benchmark_table(solver_func, n_values=None, base_seed=40, timeout=60):
    if n_values is None:
        n_values = [5, 10, 15, 20, 30, 50]

    print(f"| {'N':<3} | {'Seed':<4} | {'Solution':<10} | {'time (ms)':<9} |")
    print(f"|{'-' * 5}|{'-' * 6}|{'-' * 12}|{'-' * 11}|")

    for n in n_values:
        # 1. Set a reproducible seed for this N (so you can debug specific cases)
        current_seed = 40

        # 2. Generate the graph
        # We assume euclidean=True based on your previous config
        _, edges = generate_network(n, seed=40, euclidean=True)

        # 3. Initialize Timer
        timer = Timer(timeout)

        # 4. Run the Solver
        # Returns a list of SolutionStats, we want the last one (best found)
        stats_list = solver_func(edges, timer)

        # 5. Extract Data
        if stats_list:
            best_stat = stats_list[-1]
            score = round(best_stat.score, 2)
            # Timer usually records seconds, convert to ms
            time_ms = round(best_stat.time * 1000, 2)

            # If it timed out but found a solution, mark it
            if best_stat.time >= timeout:
                time_ms = f"> {int(timeout * 1000)} (T.O.)"
        else:
            score = "No Sol"
            time_ms = "Timeout"

        # 6. Print Row
        print(f"| {n:<3} | {current_seed:<4} | {score:<10} | {time_ms:<9} |")


if __name__ == '__main__':
    from tsp_solve import branch_and_bound, branch_and_bound_smart

    # Run the benchmark
    generate_benchmark_table(
        branch_and_bound,
        n_values=[5, 10, 15, 20, 30, 50],  # Warning: 30+ will likely timeout for exact B&B
        base_seed=40,
        timeout= 120  # Stop after 10 seconds per N
    )