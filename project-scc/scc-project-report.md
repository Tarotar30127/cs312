# Project Report - Network Analysis SCCs

## Baseline

### Design Experience

*I talked with Kyle Mak and Collin Verbanatz about baseline. We talked about the pros and cons of using a list compare to
a set for keeping track of visited nodes. A set is the best because it doesn't allow duplicates. You keep track of 
pre- and post-numbers by implementing some kind of counter. We walked through a few problems by hand and *

### Theoretical Analysis - Pre/Post Order Traversal

#### Time 
'''
def prepost(graph: GRAPH) -> list[dict[str, list[int]]]:
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
    visited.add(node)
    current_tree[node] = [counter[0], 0]
    counter[0] += 1
    for neighbor in graph[node]:
        if neighbor not in visited:
            prepost_helper(graph, neighbor, visited, current_tree, counter)
    current_tree[node][1] = counter[0]
    counter[0] += 1
'''

#### Space

*Fill me in*

### Empirical Data

| density factor | size  | V | E | runtime |
|----------------|-------|---|---|---------|
| 0.25           | 10    |   |   |         |
| 0.25           | 20    |   |   |         |
| 0.25           | 100   |   |   |         |
| 0.25           | 200   |   |   |         |
| 0.25           | 1000  |   |   |         |
| 0.25           | 2000  |   |   |         |
| 0.25           | 10000 |   |   |         |
| 0.5            | 10    |   |   |         |
| 0.5            | 20    |   |   |         |
| 0.5            | 100   |   |   |         |
| 0.5            | 200   |   |   |         |
| 0.5            | 1000  |   |   |         |
| 0.5            | 2000  |   |   |         |
| 0.5            | 10000 |   |   |         |
| 1              | 10    |   |   |         |
| 1              | 20    |   |   |         |
| 1              | 100   |   |   |         |
| 1              | 200   |   |   |         |
| 1              | 1000  |   |   |         |
| 1              | 2000  |   |   |         |
| 1              | 10000 |   |   |         |
| 2              | 10    |   |   |         |
| 2              | 20    |   |   |         |
| 2              | 100   |   |   |         |
| 2              | 200   |   |   |         |
| 2              | 1000  |   |   |         |
| 2              | 2000  |   |   |         |
| 2              | 10000 |   |   |         |
| 3              | 10    |   |   |         |
| 3              | 20    |   |   |         |
| 3              | 100   |   |   |         |
| 3              | 200   |   |   |         |
| 3              | 1000  |   |   |         |
| 3              | 2000  |   |   |         |
| 3              | 10000 |   |   |         |


### Comparison of Theoretical and Empirical Results

- Theoretical order of growth: *copy from section above* 
- Measured constant of proportionality for theoretical order: 

![img](img.png)

- Empirical order of growth (if different from theoretical): 

![img](img.png)


*Fill me in*

## Core

### Design Experience

*Fill me in*

### Theoretical Analysis - SCC

#### Time 

*Fill me in*

#### Space

*Fill me in*

### Empirical Data

| size  | density factor | V+E | runtime |
|-------|----------------|-----|---------|
| 10    | 0.25           |     |         |
| 20    | 0.25           |     |         |
| 100   | 0.25           |     |         |
| 200   | 0.25           |     |         |
| 1000  | 0.25           |     |         |
| 2000  | 0.25           |     |         |
| 10000 | 0.25           |     |         |
| 10    | 0.5            |     |         |
| 20    | 0.5            |     |         |
| 100   | 0.5            |     |         |
| 200   | 0.5            |     |         |
| 1000  | 0.5            |     |         |
| 2000  | 0.5            |     |         |
| 10000 | 0.5            |     |         |
| 10    | 1              |     |         |
| 20    | 1              |     |         |
| 100   | 1              |     |         |
| 200   | 1              |     |         |
| 1000  | 1              |     |         |
| 2000  | 1              |     |         |
| 10000 | 1              |     |         |
| 10    | 2              |     |         |
| 20    | 2              |     |         |
| 100   | 2              |     |         |
| 200   | 2              |     |         |
| 1000  | 2              |     |         |
| 2000  | 2              |     |         |
| 10000 | 2              |     |         |
| 10    | 3              |     |         |
| 20    | 3              |     |         |
| 100   | 3              |     |         |
| 200   | 3              |     |         |
| 1000  | 3              |     |         |
| 2000  | 3              |     |         |
| 10000 | 3              |     |         |


### Comparison of Theoretical and Empirical Results

- Theoretical order of growth: *copy from section above* 
- Measured constant of proportionality for theoretical order: 
- Empirical order of growth (if different from theoretical): 
- Measured constant of proportionality for empirical order: 

![img](img.png)

*Fill me in*

## Stretch 1

### Design Experience

*Fill me in*

### Articulation Points Discussion 

*Fill me in*

## Stretch 2

### Design Experience

*Fill me in*

### Dataset Description

*Fill me in*

### Findings Discussion

*Fill me in*

## Project Review

*Fill me in*
