import matplotlib.pyplot as plt
import math

# Try to import the runtimes.
# This assumes _runtimes.py is in the same directory
try:
    from _runtimes import runtimes
except ImportError:
    print("Error: Could not find _runtimes.py.")
    print("Please create it with your timing data (in milliseconds).")
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
    '''
    runtimes = [
        (10, 0.039),
        (100, 0.280),
        (1000, 3.798),
        (10000, 38.348),
        (20000, 68.518),
        (40000, 148.208),
        (50000, 190.899),
    ]
    '''
    if not runtimes:
        exit()


def theoretical_big_o(n):
    """
    Theoretical complexity for Divide-and-Conquer Convex Hull: O(N log N)
    """
    if n <= 1:
        return 1
    return n * math.log(n)


def compute_coefficient(observed_performance, theoretical_order_func):
    """
    Calculates c = time / O(N log N) for each data point.
    """
    coeffs = []
    for n, time_ms in observed_performance:
        # Skip small N values which skew the coefficient
        if n < 100:
            continue

        theory = theoretical_order_func(n)
        if theory > 0:
            coeffs.append(time_ms / theory)
    return coeffs


def main():
    # --- Part 1: Calculate the coefficient ---
    print("Calculating coefficient...")

    coeffs = compute_coefficient(runtimes, theoretical_big_o)

    if not coeffs:
        print("Error: No valid data to compute coefficient.")
        print("Make sure runtimes has N > 100.")
        return

    # Get the average coefficient
    coeff = sum(coeffs) / len(coeffs)
    print(f"Calculated Coefficient (c): {coeff}")

    # --- Part 2: Plot the coefficient stability ---
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

    # --- Part 3: Plot theoretical vs. observed (Corrected and Cleaned) ---
    print("Plotting observed vs. theoretical runtime...")

    all_n = [n for n, t in runtimes]
    observed_times = [t for n, t in runtimes]

    predicted_times = [
        coeff * theoretical_big_o(n)
        for n in all_n
    ]

    # Create the figure and axes ONCE
    fig2 = plt.figure(2)
    ax2 = fig2.add_subplot(111)

    # Plot empirical (observed) values ONCE
    ax2.scatter(all_n, observed_times, marker='o', c='C0', label='Observed')

    # Plot theoretical fit ONCE
    sorted_data = sorted(zip(all_n, predicted_times))
    sorted_n = [n for n, t in sorted_data]
    sorted_pred_t = [t for n, t in sorted_data]

    ax2.plot(
        sorted_n,
        sorted_pred_t,
        c='gray',
        ls=':',
        lw=3,
        marker='o',
        markerfacecolor='C0',
        markeredgecolor='gray',
        label='Theoretical O(N log N)'
    )

    # Set labels and title ONCE
    ax2.legend()
    ax2.set_xlabel('Number of Points (N)')
    ax2.set_ylabel('Runtime (ms)')
    ax2.set_title('Runtime for Divide and Conquer Convex Hull')

    fig2.savefig('core_hull_theo_graph.svg')
    print("Saved 'core_hull_theo_graph.svg'")

    # Show both plots at the end
    plt.show()


if __name__ == '__main__':
    main()