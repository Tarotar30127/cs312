import random
import math
from time import time
from pprint import pprint

from utils import generate_network, Timer, score_tour
from tsp_solve_backtracking import greedy_tour, backtracking   # change this to your actual filename (e.g., tsp_solvers)
# from plotting import plot_points, etc. (optional)


def generate_and_analyze_tour(seed: int, n: int, analyze) -> tuple[int, float]:
    """
    Generate a random TSP instance of size n, run the solver, and record runtime.
    """
    random.seed(seed)
    _, edges = generate_network(n=n, seed=seed)
    timer = Timer(time_limit=60)

    start = time()
    _ = analyze(edges, timer)
    duration = (time() - start) * 1000  # ms
    return n, duration


def _compute_average_runtimes(runtimes):
    """
    Average runtimes over multiple runs per size.
    """
    groups = {}
    for size, runtime in runtimes:
        if size not in groups:
            groups[size] = []
        groups[size].append(runtime)
    return [
        (size, round(sum(times) / len(times), 4))
        for size, times in groups.items()
    ]


def _print_markdown_table(ave_runtimes, headers):
    """
    Prints a Markdown table you can paste directly into your report.
    """
    header_widths = [len(header) for header in headers]
    rows = [
        '| ' + ' | '.join(headers) + ' |',
        '| ' + ' | '.join('-' * len(header) for header in headers) + ' |'
    ]
    for row in ave_runtimes:
        rows.append('| ' + ' | '.join(f'{field:<{width}}' for field, width in zip(row, header_widths)) + ' |')
    print('Copy this markdown table into your report:')
    print()
    print('\n'.join(rows))


def main():
    # You can tweak these sizes depending on how long your greedy_tour takes
    sizes = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50]
    runtimes = []
    print("Benchmarking backtracking...\n")

    for size in sizes:
        print(f'Running with size {size}')
        for iteration in range(3):  # repeat a few times for averaging
            n, runtime = generate_and_analyze_tour(
                seed=225 + iteration,
                n=size,
                analyze= backtracking
            )
            runtimes.append((n, runtime))

    ave_runtimes = _compute_average_runtimes(runtimes)
    print()
    _print_markdown_table(
        ave_runtimes,
        ['N', 'Time (ms)']
    )

    # Optionally save raw runtimes to file
    with open('_backtracking_runtimes.py', 'w') as file:
        print('runtimes = ', end='', file=file)
        pprint(runtimes, file)
        print('\n_backtracking_runtimes.py written')


if __name__ == '__main__':
    main()
