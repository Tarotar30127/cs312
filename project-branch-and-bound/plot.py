import time
import math
import matplotlib.pyplot as plt

# Adjust imports to match your file structure
from tsp_core import generate_network, Timer
from tsp_solve import branch_and_bound


def theoretical_big_o(n):
    """ Formula: O(n^3 * 4^n) """
    if n <= 0: return 1
    return (n ** 3) * (4 ** n)


def run_benchmark_2d_ms():
    # 1. Setup
    # We stop at 13 or 14 because B&B grows incredibly fast in linear time
    n_values = range(5, 14)
    timeout_sec = 5

    # Your specific coefficient
    coeff = 1.1134e-10

    observed_times = []
    theoretical_times = []
    valid_ns = []

    print(f"| {'N':<3} | {'Time (ms)':<12} |")
    print(f"|{'-' * 5}|{'-' * 14}|")

    # 2. Collect Data
    for n in n_values:
        try:
            _, edges = generate_network(n, seed=42 + n, euclidean=True)
        except Exception:
            continue

        timer = Timer(timeout_sec)

        # Measure Observed Time
        start = time.perf_counter()
        branch_and_bound(edges, timer)
        end = time.perf_counter()

        # CONVERT TO MILLISECONDS
        obs_time_ms = (end - start) * 1000

        # Calculate Theoretical Time in MILLISECONDS
        pred_time_ms = (coeff * theoretical_big_o(n)) * 1000

        # Only plot if we didn't timeout (or just barely did)
        if obs_time_ms < timeout_sec * 1000:
            valid_ns.append(n)
            observed_times.append(obs_time_ms)
            theoretical_times.append(pred_time_ms)
            print(f"| {n:<3} | {obs_time_ms:<12.2f} |")
        else:
            print(f"| {n:<3} | {'Timeout':<12} |")
            # Stop the loop if we hit the wall to avoid waiting forever
            break

    if not valid_ns:
        print("No valid data to plot.")
        return

    # 3. Plotting
    plt.figure(figsize=(10, 6))

    # Plot Observed Data
    plt.plot(valid_ns, observed_times, 'bo-', label='Observed (ms)', linewidth=2)

    # Plot Theoretical Data
    plt.plot(valid_ns, theoretical_times, 'r--^', label='Theoretical (ms)', linewidth=2)

    # Axis Labels
    plt.xlabel('Problem Size (N Cities)', fontsize=12)
    plt.ylabel('Time (ms)', fontsize=12)
    plt.title('Branch & Bound Runtime (Linear Scale)', fontsize=14)

    # Force plain numbers (e.g., 1000, 2000) instead of scientific notation (1e3)
    plt.ticklabel_format(style='plain', axis='y')

    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(fontsize=11)

    print("\nDisplaying graph...")
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    run_benchmark_2d_ms()