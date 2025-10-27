import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from time import time
from pathlib import Path
from alignment import align  # Assumes alignment.py is in the same folder

# Define the coefficient globally or pass it. Using it here for simplicity.
# This coefficient was found for the case where m=n.
# For m!=n, a more robust coefficient might be derived from a multi-variable regression,
# but using the given one is a good starting point for a theoretical surface.
THEORETICAL_COEFFICIENT = 4.841313827920842e-07


def read_sequence(file: Path) -> str:
    """Helper function to read and clean sequence files."""
    return ''.join(file.read_text().splitlines())


def _analyze_alignment_3d(m_size: int, n_size: int, algorithm, seq1_full, seq2_full, **kwargs):
    """Runs alignment for seq2 of length m and seq1 of length n."""

    seq1 = seq1_full[:n_size]
    seq2 = seq2_full[:m_size]

    start = time()
    algorithm(seq1, seq2, **kwargs)
    end = time()
    runtime = end - start

    return m_size, n_size, runtime


def main_3d():
    print("Loading sequences...")
    seq1_full = read_sequence(Path('test_files/bovine_coronavirus.txt'))
    seq2_full = read_sequence(Path('test_files/murine_hepatitus.txt'))
    print("Sequences loaded.")

    # Define the sizes for m (seq2) and n (seq1)
    m_sizes = [500, 1000, 1500, 2000, 2500]
    n_sizes = [500, 1000, 1500, 2000, 2500]

    # Store empirical results
    empirical_results = []

    print("Starting 3D analysis (m vs n vs time)...")
    for m in m_sizes:
        for n in n_sizes:
            runtimes = []
            for i in range(3):  # Run 3 iterations for averaging
                print(f"  Running m={m}, n={n} (iteration {i + 1}/3)...")
                _, _, runtime = _analyze_alignment_3d(m, n, align, seq1_full, seq2_full)
                runtimes.append(runtime)

            avg_runtime = sum(runtimes) / len(runtimes)
            print(f"  -> Avg. Runtime: {avg_runtime:.4f}s")
            empirical_results.append((m, n, avg_runtime))

    print("Analysis complete. Generating 3D plot...")

    # --- Plotting ---
    if not empirical_results:
        print("No empirical results to plot.")
        return

    # Extract empirical data
    mm_empirical, nn_empirical, times_empirical = zip(*empirical_results)

    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection='3d')

    # 1. Plot Empirical Data
    ax.scatter(mm_empirical, nn_empirical, times_empirical, c='blue', marker='o', label='Observed Runtime',
               depthshade=True)

    # 2. Plot Theoretical Surface O(n*m)
    # Create a finer grid for the theoretical surface for a smoother appearance
    m_grid = np.linspace(min(m_sizes), max(m_sizes), 50)
    n_grid = np.linspace(min(n_sizes), max(n_sizes), 50)
    M_grid, N_grid = np.meshgrid(m_grid, n_grid)

    # Calculate theoretical runtimes based on O(n*m)
    Theoretical_Times_Grid = THEORETICAL_COEFFICIENT * M_grid * N_grid

    ax.plot_surface(M_grid, N_grid, Theoretical_Times_Grid,
                    color='red', alpha=0.3, label='Theoretical $O(m \\cdot n)$',
                    rstride=5, cstride=5, edgecolor='none')  # rstride/cstride for mesh density

    # Add an empty plot to create a legend entry for the surface
    ax.plot([], [], [], color='red', alpha=0.5, label='Theoretical $O(m \\cdot n)$ Surface')

    ax.set_xlabel('m (seq2 length)')
    ax.set_ylabel('n (seq1 length)')
    ax.set_zlabel('Runtime (sec)')
    ax.set_title(f'Alignment Runtime with Theoretical $O(m \\cdot n)$ Fit (c={THEORETICAL_COEFFICIENT:.2e})')
    ax.legend()

    # Adjust view for better perspective
    ax.view_init(elev=30, azim=45)  # You can change these angles

    # Save the figure
    folder_path = Path("_analysis")
    folder_path.mkdir(exist_ok=True)
    fig.savefig(f'_analysis/align_3d_empirical_and_theoretical.svg')

    plt.show()


if __name__ == '__main__':
    main_3d()