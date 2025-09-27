import random
import sys
from time import time

GRAPH = dict[str, list[str]]
sys.setrecursionlimit(10000)


def prepost(graph: GRAPH) -> list[dict[str, list[int]]]:
    """
    Return a list of DFS trees.
    Each tree is a dict mapping each node label to a list of [pre, post] order numbers.
    The graph should be searched in order of the keys in the dictionary.
    """
    counter: list[int] = [1]
    visited = set()
    dfs_trees = []
    for node in graph:
        if node not in visited:
            current_tree: dict[str, list[int]] = {}
            prepost_helper(graph, node, visited, current_tree, counter)
            dfs_trees.append(current_tree)
    return dfs_trees


def prepost_helper(graph: GRAPH, node: str, visited: set, current_tree: dict, counter: list[int]):
    """
    A recursion helper to start a new dfs
    """
    visited.add(node)
    current_tree[node] = [counter[0], 0]
    counter[0] += 1
    for neighbor in graph[node]:
        if neighbor not in visited:
            prepost_helper(graph, neighbor, visited, current_tree, counter)
    current_tree[node][1] = counter[0]
    counter[0] += 1






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
