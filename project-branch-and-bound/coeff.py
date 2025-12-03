import math
import time
import matplotlib.pyplot as plt

# Assuming these exist in your project based on previous code
from tsp_core import generate_network, Timer
from tsp_solve import branch_and_bound


def collect_runtimes(n_start=10, n_end=15, samples_per_n=3):
    """
    Generates random TSP problems for N in range [n_start, n_end],
    runs branch_and_bound, and measures wall-clock time.
    """
    data = []
    print(f"Collecting runtimes for N={n_start} to {n_end}...")
    print(f"| {'N':<3} | {'Avg Time (s)':<12} |")
    print("-" * 20)

    for n in range(n_start, n_end + 1):
        total_time = 0

        for i in range(samples_per_n):
            # Generate a consistent random network for this sample
            # (using seed ensures reproducibility if needed)
            _, edges = generate_network(n, seed=100 + n + i, euclidean=True)

            # Create a timer with a long timeout so it doesn't cut off execution
            timer = Timer(300)

            # Measure strictly the execution time
            start_clock = time.perf_counter()
            branch_and_bound(edges, timer)
            end_clock = time.perf_counter()

            total_time += (end_clock - start_clock)

        avg_time = total_time / samples_per_n

        # Format: (vertices, edges, time)
        # Note: Edges in a complete graph is n^2, though the formula mainly uses v
        data.append((n, n ** 2, avg_time))
        print(f"| {n:<3} | {avg_time:<12.5f} |")

    return data


def compute_coefficient(observed_performance, theoretical_order):
    return [
        time / theoretical_order(v, e) for v, e, time in observed_performance
    ]


def main():
    # 1. Collect Data Real-time
    # Warning: N > 16 might take a very long time for exact Branch & Bound
    runtimes = collect_runtimes(n_start=8, n_end=14)

    # 2. Define Theoretical Complexity
    # For B&B TSP: O(n^2 * 2^n) is a common average-case estimation.
    # n^2 = matrix reduction cost
    # 2^n = effective search space (much smaller than n! due to pruning)
    def theoretical_big_o(v, e):
        return (v ** 3) * (4 ** v)

    # 3. Calculate Coefficients
    coeffs = compute_coefficient(runtimes, theoretical_big_o)

    # 4. Calculate Mean Coefficient
    # We slice [1:] to skip the first small N where overhead might skew results
    used_coeffs = coeffs[1:] if len(coeffs) > 1 else coeffs

    coeff = sum(used_coeffs) / len(used_coeffs)
    print(f"\nCalculated Coefficient: {coeff:.4e}")

    # 5. Plot Results
    plt.figure(figsize=(10, 6))
    plt.bar(range(len(coeffs)), coeffs, color='skyblue', label='Observed / Theoretical')

    # Draw the mean line
    xlim = plt.xlim()
    plt.plot(xlim, [coeff, coeff], ls='--', c='red', linewidth=2, label=f'Mean Coeff = {coeff:.2e}')
    plt.xlim(xlim)

    plt.title(f'Branch & Bound Complexity Analysis\nTheoretical: O($n^2 2^n$)', fontsize=14)
    plt.xlabel('Test Cases (Increasing N)', fontsize=12)
    plt.ylabel('Coefficient constant C', fontsize=12)
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()


if __name__ == '__main__':
    main()