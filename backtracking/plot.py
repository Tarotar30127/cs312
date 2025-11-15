import math
import matplotlib.pyplot as plt
from _greedy_runtimes import runtimes  # Imports from _greedy_tour_runtimes.py


def theoretical_big_o(n):
    """
    Theoretical complexity for the unoptimized Greedy Tour: O(N^4)
    """
    if n <= 0:
        return 1
    return n ** 2.5


def compute_coefficient(observed_performance, theoretical_order_func):
    """
    Calculates c = time / O(N^4) for each data point.
    """
    coeffs = []
    for n, time_ms in observed_performance:
        if n < 10:  # Filter out very small N where model is unstable
            continue
        theory = theoretical_order_func(n)
        if theory > 0:
            coeffs.append(time_ms / theory)
    return coeffs


def get_n_values_for_coeffs(observed_performance):
    """
    Gets the N values corresponding to the calculated coefficients.
    """
    return [n for n, time_ms in observed_performance if n >= 10]


def main():
    print("Calculating coefficient for Greedy TSP O(N^4)...")

    coeffs = compute_coefficient(runtimes, theoretical_big_o)

    if not coeffs:
        print("Error: No valid data (with N >= 10) to compute coefficient.")
        return

    # Average coefficient
    coeff = sum(coeffs) / len(coeffs)
    print(f"Calculated Coefficient (c): {coeff:.6e}")

    # --- Plot coefficient stability ---
    n_values_for_coeffs = get_n_values_for_coeffs(runtimes)

    # This is a bit of a hack, but matches the compute_coefficient filter
    n_values_for_plot = [n for n, _ in runtimes if n >= 10]

    # We must also get the *actual* coefficients, not re-calculate
    coeffs_for_plot = [time_ms / theoretical_big_o(n) for n, time_ms in runtimes if n >= 10]

    fig1 = plt.figure(1, figsize=(10, 6))
    ax1 = fig1.add_subplot(111)

    ax1.scatter(n_values_for_plot, coeffs_for_plot, label='Calculated c', c='C0', alpha=0.7)
    xlim = ax1.get_xlim()
    ax1.plot(xlim, [coeff, coeff], ls=':', c='k', label=f'Avg. c = {coeff:.2e}')
    ax1.set_xlim(xlim)
    ax1.set_title('Coefficient (c = time / N!) Stability')
    ax1.set_xlabel('Problem Size (N)')
    ax1.set_ylabel('Computed Coefficient (c)')
    ax1.legend()
    fig1.savefig('Emp_greedy_coefficient_stability.svg')
    print("Saved 'Emp_greedy_coefficient_stability.svg'")

    # --- Plot theoretical vs observed ---
    print("Plotting observed vs. theoretical runtime...")

    all_n = [n for n, _ in runtimes]
    observed_times = [t for _, t in runtimes]

    # Use a sorted list of unique N values for the prediction line
    unique_sorted_n = sorted(list(set(all_n)))
    predicted_times = [coeff * theoretical_big_o(n) for n in unique_sorted_n]

    fig2 = plt.figure(2, figsize=(10, 6))
    ax2 = fig2.add_subplot(111)

    ax2.scatter(all_n, observed_times, marker='o', c='C0', label='Observed Runtimes', alpha=0.7)
    ax2.plot(unique_sorted_n, predicted_times, c='gray', ls=':', lw=2,
             marker='o', markersize=8,
             label=f'Predicted O(n^2.5))')

    ax2.legend()
    ax2.set_xlabel('Problem Size (n)')
    ax2.set_ylabel('Runtime (ms)')
    ax2.set_title('Runtime for O(n^2.5) Greedy')

    # --- MODIFICATION: Log scale lines removed ---
    #ax2.set_xscale('log')
    #ax2.set_yscale('log')
    ax2.grid(True, which="both", ls="--", alpha=0.5)

    fig2.savefig('Emp_greedy_runtime_graph_core_th.svg')  # Saved as a new file
    print("Saved 'Emp_greedy_runtime_graph_linear.svg'")

    plt.show()


if __name__ == '__main__':
    main()
