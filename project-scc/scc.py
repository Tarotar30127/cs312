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


def reverse_graph(graph: GRAPH) -> dict[str, list[str]]:
    reverse_dict = {node: [] for node in graph}
    for node, neighbors in graph.items():
        for neighbor in neighbors:
            reverse_dict[neighbor].append(node)
    return reverse_dict


def find_sccs(graph: GRAPH) -> list[set[str]]:
    """
    Return a list of the strongly connected components in the graph.
    The list should be returned in order of sink-to-source
    """
    reverse = reverse_graph(graph)
    reversed_prepost = prepost(reverse)
    node_post = {}
    for tree in reversed_prepost:
        for node, (pre, post) in tree.items():
            node_post[node] = post

    sorted_nodes = sorted(node_post.keys(), key=lambda n: node_post[n], reverse=True)
    visited = set()
    sccs = []

    def find_scc(start, neighbors):
        visited.add(start)
        neighbors.add(start)
        for neighbor in graph[start]:
            if neighbor not in visited:
                find_scc(neighbor, neighbors)

    for node in sorted_nodes:
        if node not in visited:
            component = set()
            find_scc(node, component)
            sccs.append(component)

    return sccs


def classify_edges(graph: GRAPH, trees: list[dict[str, list[int]]]) -> dict[str, set[tuple[str, str]]]:
    """
    Return a dictionary containing sets of each class of edges
    """
    classification = {
        'tree/forward': set(),
        'back': set(),
        'cross': set()
    }
    for tree in trees:
        for leaf1 in tree:
            for leaf2 in graph.get(leaf1, []):
                if leaf2 not in tree:
                    classification['cross'].add((leaf1, leaf2))
                    continue

                pre_u, post_u = tree[leaf1]
                pre_v, post_v = tree[leaf2]

                if pre_u < pre_v and post_v < post_u:
                    classification['tree/forward'].add((leaf1, leaf2))
                elif pre_v < pre_u and post_u < post_v:
                    classification['back'].add((leaf1, leaf2))
                else:
                    classification['cross'].add((leaf1, leaf2))

    return classification
