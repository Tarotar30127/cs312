import random
import sys
from time import time

from graphs import generate_graph

GRAPH = dict[str, list[str]]
sys.setrecursionlimit(10000)


def prepost(graph: GRAPH) -> list[dict[str, list[int]]]:
    """
    Return a list of DFS trees.
    Each tree is a dict mapping each node label to a list of [pre, post] order numbers.
    The graph should be searched in order of the keys in the dictionary.
    """
    return []


def find_sccs(graph: GRAPH) -> list[set[str]]:
    """
    Return a list of the strongly connected components in the graph.
    The list should be returned in order of sink-to-source
    """
    return []


def classify_edges(graph: GRAPH, trees: list[dict[str, list[int]]]) -> dict[str, set[tuple[str, str]]]:
    """
    Return a dictionary containing sets of each class of edges
    """
    classification = {
        'tree/forward': set(),
        'back': set(),
        'cross': set()
    }

    return classification


def main(seed: int, n: int, density_factor: float):
    random.seed(seed)
    graph = generate_graph(n, density_factor)
    print('|V|', nnodes := len(graph))
    print('|E|', nedges := sum(len(edges) for edges in graph.values()))
    print('|V| + |E|', nnodes + nedges)

    start = time()

    # trees = prepost(graph)
    sccs = find_sccs(graph)

    duration = time() - start

    print('# SCCS', len(sccs))
    if n < 20:
        print('SCCS', sccs)

if __name__ == '__main__':
    main(int(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3]))
