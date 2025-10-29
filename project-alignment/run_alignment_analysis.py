from pprint import pprint
from time import time
from pathlib import Path

from alignment import align  # ✅ Use your core_align function


def _analyze_alignment(N: int, algorithm, **kwargs):
    """Runs the alignment for a given input size N and returns runtime."""
    def read_sequence(file: Path) -> str:
        return ''.join(file.read_text().splitlines())

    seq1 = read_sequence(Path('test_files/bovine_coronavirus.txt'))[:N]
    seq2 = read_sequence(Path('test_files/murine_hepatitus.txt'))[:N]

    start = time()
    algorithm(seq1, seq2, **kwargs)
    end = time()

    runtime = end - start
    return N, runtime


def _compute_average_runtimes(runtimes):
    groups = {}
    for n, runtime in runtimes:
        if n not in groups:
            groups[n] = []
        groups[n].append(runtime)

    return [
        (
            size,
            round((sum(times) / len(times)) * 1000, 3)  # convert to ms
        )
        for size, times in groups.items()
    ]


def _print_markdown_table(ave_runtimes, headers):
    header_widths = [len(header) for header in headers]

    rows = [
        '| ' + ' | '.join(headers) + ' |',
        '| ' + ' | '.join('-' * len(header) for header in headers) + ' |'
    ]

    for row in ave_runtimes:
        formatted_row = '| ' + ' | '.join(
            f'{field:<{width}}' for field, width in zip(row, header_widths)
        ) + ' |'
        rows.append(formatted_row)

    print('\n'.join(rows))


def main(sizes, algorithm, file_name="_runtimes.py", **kwargs):
    """Runs timing experiments for each input size."""
    runtimes = []
    for size in sizes:
        print(f'Running with size {size}...')
        for iteration in range(10):
            n, runtime = _analyze_alignment(size, algorithm, **kwargs)
            runtimes.append((n, runtime))

    ave_runtimes = _compute_average_runtimes(runtimes)

    print("\nCopy this Markdown table into your report:\n")
    _print_markdown_table(
        ave_runtimes,
        [' N     ', 'Time (ms)']
    )

    with open(file_name, 'w') as file:
        print('runtimes = ', end='', file=file)
        pprint(runtimes, file)

    print(f"\n{file_name} written successfully.\n")


if __name__ == '__main__':
    sizes = [500, 1000, 1500, 2000, 2500, 3000]

    main(
        sizes=sizes,
        algorithm=align,
        match_award=-3,
        sub_penalty=1,
        indel_penalty=5,
        banded_width=3
    )