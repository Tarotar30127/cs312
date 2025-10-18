import matplotlib.pyplot as plt
import math

# Try to import the runtimes.
# This assumes _runtimes.py is in the same directory
try:
    from _runtimes import runtimes
except ImportError:
    print("Error: Could not find _runtimes.py.")
    print("Please create it with your timing data (in seconds).")
    print("It should look like: runtimes = [(10, 0.001), (100, 0.012), ...]")
    # Use dummy data so the script can still run
    runtimes = [
        (10, 0.045),
        (100, 0.491),
        (1000, 4.249),
        (10000, 35.558),
        (20000, 58.881),
        (40000, 118.304),
        (50000, 154.797),
    ]
    if not runtimes:
        exit()


def theoretical_big_o(n):
    """
    Theoretical complexity for Divide-and-Conquer Convex Hull: O(N log N)
    """
    if n <= 1:
        # O(N log N) is not well-defined for N=1 or N=0.
        # Return a small value or 1.
        return 1
    # Use natural log (math.log) or log base 2 (math.log2)
    # The coefficient 'c' will adjust for the base.
    return n * math.log(n)


def compute_coefficient(observed_performance, theoretical_order_func):
    """
    Calculates c = time / O(N log N) for each data point.
    """
    coeffs = []
    for n, time_sec in observed_performance:
        # Skip small N values (e.g., < 100)
        # Their runtimes are often dominated by constant overhead
        # and will skew the coefficient calculation.
        if n < 100:
            continue

        theory = theoretical_order_func(n)
        if theory > 0:
            coeffs.append(time_sec / theory)
    return coeffs


def main():
    # --- Part 1: Calculate the coefficient (from your first script) ---
    print("Calculating coefficient...")

    coeffs = compute_coefficient(runtimes, theoretical_big_o)

    if not coeffs:
        print("Error: No valid data to compute coefficient.")
        print("Make sure runtimes has N > 100.")
        return

    # Get the average coefficient
    coeff = sum(coeffs) / len(coeffs)
    print(f"Calculated Coefficient (c): {coeff}")

    # --- Part 2: Plot the coefficient stability (from your first script) ---

    # We get the N values that were *used* for the coefficient
    n_values_for_coeffs = [n for n, t in runtimes if n >= 100]

    fig1 = plt.figure(1)
    ax1 = fig1.add_subplot(111)

    ax1.scatter(n_values_for_coeffs, coeffs, label='Calculated c')
    xlim = ax1.get_xlim()
    ax1.plot(xlim, [coeff, coeff], ls=':', c='k', label=f'Avg. c = {coeff:.2e}')
    ax1.set_xlim(xlim)
    ax1.set_title('Coefficient (c = time / (N log N)) Stability')
    ax1.set_xlabel('Number of Points (N)')
    ax1.set_ylabel('Computed Coefficient (c)')
    ax1.legend()
    fig1.savefig('hull_coefficient_stability.svg')
    print("Saved 'hull_coefficient_stability.svg'")

    # --- Part 3: Plot theoretical vs. observed (from your second script) ---
    print("Plotting observed vs. theoretical runtime...")

    # Get all N values and their corresponding observed times
    all_n = [n for n, t in runtimes]
    observed_times = [t for n, t in runtimes]

    # Calculate predicted runtime for *all* N values using the *single* avg coefficient
    predicted_times = [
        coeff * theoretical_big_o(n)
        for n in all_n
    ]

    fig2 = plt.figure(2)
    ax2 = fig2.add_subplot(111)

    # Plot empirical (observed) values
    ax2.scatter(all_n, observed_times, marker='o', c='blue', label='Observed Runtime')

    # Plot theoretical fit
    # Sort by N to ensure the line plots correctly
    sorted_data = sorted(zip(all_n, predicted_times))
    sorted_n = [n for n, t in sorted_data]
    sorted_pred_t = [t for n, t in sorted_data]

    ax2.plot(
        sorted_n,
        sorted_pred_t,
        c='k',
        ls=':',
        lw=2,
        label=f'Theoretical Fit (c * N log N)'
    )

    ax2.legend()
    ax2.set_xlabel('Number of Points (N)')
    ax2.set_ylabel('Runtime (seconds)')
    ax2.set_title('Runtime for Convex Hull')

    # Optional: Use log scales for better visualization
    # O(N log N) looks almost linear on a log-log plot
    ax2.set_xscale('log')
    ax2.set_yscale('log')
    ax2.set_title('Runtime for Divide and Conquer Convex Hull')
    ax2.grid(True, which="both", ls="--", alpha=0.5)

    fig2.savefig('hull_empirical_graph.svg')
    print("Saved 'hull_empirical_graph.svg'")

    # Show both plots at the end
    plt.show()


if __name__ == '__main__':
    main()