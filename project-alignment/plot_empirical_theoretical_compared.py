import math
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.animation as animation
# Run run_alignment_analysis.py to populate the runtimes
from _runtimes import runtimes


def main(theoretical_big_o, coeff, theoretical_label, table_name, test_name: str):
    nn, times = zip(*runtimes)

    # Plot empirical values
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(nn, times, marker='o')  # type: ignore

    predicted_runtime = [
        coeff * theoretical_big_o(n)
        for n, t in runtimes
    ]

    # Plot theoretical fit
    ax.plot(
        nn,
        predicted_runtime,
        c='k',
        ls=':',
        lw=2,
        alpha=0.5
    )

    # Update title, legend, and axis labels as needed
    ax.legend(['Observed', theoretical_label])
    ax.set_xlabel('n')
    ax.set_ylabel('Runtime (sec)')
    ax.set_title(f'Time for {table_name} on Graph')

    folder_path = Path("_analysis")
    folder_path.mkdir(exist_ok=True)

    # fig.show()
    fig.savefig(f'_analysis/{test_name}_empirical.svg')
    plt.show()


if __name__ == '__main__':
    # MODIFICATION: The theoretical runtime for m=n=N is O(N*N) or O(N^2)
    def theoretical_big_o(n):
        return n


    # MODIFICATION: Fill this in from the output of compute_coefficient.py
    coeff_align = 0.0047319129599465255

    main(
        theoretical_big_o=theoretical_big_o,
        coeff=coeff_align,
        theoretical_label='Theoretical $O(n)$',  # Updated label
        table_name="Alignment",
        test_name='align'
    )