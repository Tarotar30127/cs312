import math
import time
import matplotlib.pyplot as plt

# Adjust these imports if your file names are different
from tsp_core import generate_network, Timer
from tsp_solve import branch_and_bound


# --- PART 1: GENERATE DATA (Since you don't have the file) ---
def get_generated_runtimes():
    """
    Generates runtimes on the fly to match the structure:
    (N, Seed, Score, Time_ms)
    """
    data = []
    # Adjust range as needed. N=15 might be slow for exact B&B.
    n_values = range(5, 14)
    timeout_sec = 5

    print("Generating Runtime Data...")
    print(f"| {'N':<3} | {'Seed':<6} | {'Time (ms)':<10} |")
    print(f"|{'-' * 5}|{'-' * 8}|{'-' * 12}|")

    for n in n_values:
        # Use a fixed seed strategy per N to get consistent results
        seed = 42 + n
        try:
            _, edges = generate_network(n, seed=seed, euclidean=True)
        except Exception:
            continue

        timer = Timer(timeout_sec)

        start = time.perf_counter()
        solutions = branch_and_bound(edges, timer)
        end = time.perf_counter()

        time_ms = (end - start) * 1000

        if solutions:
            score = solutions[-1].score
        else:
            score = math.inf

        # Only record if it didn't strictly timeout
        if time_ms < timeout_sec * 1000:
            # Format matches your requested structure: (N, Seed, Score, Time)
            row = (n, seed, score, time_ms)
            data.append(row)
            print(f"| {n:<3} | {seed:<6} | {time_ms:<10.2f} |")
        else:
            print(f"| {n:<3} | {seed:<6} | {'Timeout':<10} |")

    return data


# --- PART 2: YOUR PROVIDED LOGIC ---

def theoretical_big_o(n):
    """
    Theoretical complexity as defined in your snippet:
    O(N^4 * 2^N)
    """
    if n <= 0:
        return 1
    # formula: n^4 * 2^n
    return (n ** 4) * (2.2 ** n)


def compute_coefficient(observed_performance, theoretical_order_func):
    """
    Calculates c = time / O(N^4 * 2^N) for each data point.
    """
    coeffs = []
    for n, time_ms in observed_performance:
        theory = theoretical_order_func(n)
        if theory > 0:
            coeffs.append(time_ms / theory)
    return coeffs


def main():
    # 1. GET DATA
    # Instead of importing, we generate it here
    runtimes = get_generated_runtimes()

    print("\nCalculating coefficient for Branch and Bound O(N^4 * 1.5^N)...")

    # 2. Extract only (N, Time) from the 4-column data
    # The format in your file is: (N, Iterations/Seed, Score, Time)
    # So we take index 0 (N) and index 3 (Time)
    clean_runtimes = [(row[0], row[3]) for row in runtimes]

    coeffs = compute_coefficient(clean_runtimes, theoretical_big_o)

    if not coeffs:
        print("Error: No valid data to compute coefficient.")
        return

    # Average coefficient
    coeff = sum(coeffs) / len(coeffs)
    print(f"Calculated Coefficient (c): {coeff:.6e}")

    # --- Plot coefficient stability ---

    # Get N values for the plot (filtering same as compute_coefficient)
    n_values_for_plot = [n for n, _ in clean_runtimes if n >= 5]

    # Calculate individual coefficients for the scatter plot
    coeffs_for_plot = [time_ms / theoretical_big_o(n) for n, time_ms in clean_runtimes if n >= 5]

    fig1 = plt.figure(1, figsize=(10, 6))
    ax1 = fig1.add_subplot(111)

    ax1.scatter(n_values_for_plot, coeffs_for_plot, label='Calculated c', c='C0', alpha=0.7)
    xlim = ax1.get_xlim()
    ax1.plot(xlim, [coeff, coeff], ls=':', c='k', label=f'Avg. c = {coeff:.2e}')
    ax1.set_xlim(xlim)
    ax1.set_title(r'Coefficient Stability ($c = \frac{time}{N^4 \cdot 2.2^N}$)')
    ax1.set_xlabel('Problem Size (N cities)')
    ax1.set_ylabel('Computed Coefficient (c)')
    ax1.legend()
    fig1.savefig('tsp_bnb_coefficient_stability_em.svg')
    print("Saved 'tsp_bnb_coefficient_stability_em.svg'")

    # --- Plot theoretical vs observed ---
    print("Plotting observed vs. theoretical runtime...")

    all_n = [n for n, _ in clean_runtimes]
    observed_times = [t for _, t in clean_runtimes]

    # Use a sorted list of unique N values for the prediction line
    unique_sorted_n = sorted(list(set(all_n)))
    predicted_times = [coeff * theoretical_big_o(n) for n in unique_sorted_n]

    fig2 = plt.figure(2, figsize=(10, 6))
    ax2 = fig2.add_subplot(111)

    ax2.scatter(all_n, observed_times, marker='o', c='C0', label='Observed Runtimes', alpha=0.7)
    ax2.plot(unique_sorted_n, predicted_times, c='gray', ls=':', lw=2,
             marker='o', markersize=8,
             label=r'Predicted $O(N^4 \cdot 2.2^N)$')

    ax2.legend()
    ax2.set_xlabel('Problem Size (N cities)')
    ax2.set_ylabel('Runtime (ms)')
    ax2.set_title('Runtime for Branch and Bound TSP')

    # Log scale is usually helpful for exponential curves
    ax2.set_xscale('log')
    ax2.set_yscale('log')
    ax2.grid(True, which="both", ls="--", alpha=0.5)

    fig2.savefig('tsp_bnb_runtime_graph_em.svg')
    print("Saved 'tsp_bnb_runtime_graph_em.svg'")

    plt.show()


if __name__ == '__main__':
    main()