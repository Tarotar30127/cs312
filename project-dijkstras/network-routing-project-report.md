# Project Report - Network Routing

## Baseline

### Design Experience

*I talked to Kyle Mak and Collin Verbanatz about the Dijkstra algorithm. We when through the homework again and the graph.
Then we took a look at the sudo code and code. The graph is a dictionary representing the network. The keys are integer 
IDS nodes and the values are another dictionary where keys are neighboring node IDs and values are the floating-point 
costs of the edges or the weights. The source is the integer ID of the starting node and the target is the integer ID 
of the destination node. The function must return a list of integers representing the nodes in the shortest path from 
source to target. If no path exists, this should be an empty list [] and a float representing the total cost of that path. 
If no path exists, this should be float('inf').*

### Theoretical Analysis - Dijkstra's With Linear PQ

#### Time 

```python

def find_shortest_path_with_linear_pq(...):                       # O(V^2) 
    distance = {}                                                 # O(1) Constant
    previous = {}                                                 # O(1) Constant
    priority_queue = {}                                           # O(1) Constant
    for node in graph:                                            # O(V) loop of all vertex
        if node == source:                                        # O(1) inside loop constant
            distance[node] = 0                                    # O(1) inside loop constant 
            priority_queue[node] = 0                              # O(1) inside loop constant
        else:                                                     # O(1) constant
            distance[node] = float('inf')                         # O(1) constant
            priority_queue[node] = float('inf')                   # O(1) constant
        previous[node] = None                                     # O(1) constant
    while priority_queue:                                         # O(V) loop until all vertexes are looked through
        current_node = min(priority_queue, key=lambda n: distance[n]) # O(V) looking through all vertex find lowest 
        priority_queue.pop(current_node)                          # O(1) remove vertex
        if current_node == target:                                # O(1) checking a constant
            break                                                 # O(1) break
                                                                  # Runs for each neighbor and across all outer loops is O(E)
        for neighbor, weight in graph.get(current_node, {}).items():  # O(V) but for the total work including the while loop is O(E)
            new_distance = distance[current_node] + weight        # O(1) addition
            if new_distance < distance[neighbor]:                 # O(1) comparing constants
                distance[neighbor] = float(new_distance)          # O(1) updating constants
                previous[neighbor] = float(current_node)          # O(1) updating constant
    if distance[target] == float('inf'):                          # O(1) comparing constants
        return [], float('inf')                                   # O(1) constant
    path = []                                                     # O(1) constant
    current = target                                              # O(1) constant
    while current is not None:                                    # O(k) worst case O(V) going through all vertex
        path.insert(0, current)                                   # O(k) constant
        current = previous[current]                               # O(1) updating constant
    return path, distance[target]                                 # O(1)

```
*Dijkstra's algorithm is different for Depth-First Search because it has an extra step in finding the unvisited node 
with the smallest distance. This determines the final time complexity which is O(V^2)*

#### Space
```python
def find_shortest_path_with_linear_pq(...):                       # O(V) 
    distance = {}                                                 # O(V) will get vertex big
    previous = {}                                                 # O(1) will get as big as the vertexes
    priority_queue = {}                                           # O(1) will get as big as the vertexes
    for node in graph:                                            # O(V) loops through vertex times
        if node == source:                                        # O(1) inside loop constant
            distance[node] = 0                                    # O(1) constant add value
            priority_queue[node] = 0                              # O(1) constant give value
        else:                                                     # O(1) constant
            distance[node] = float('inf')                         # O(1) constant assign value
            priority_queue[node] = float('inf')                   # O(1) constant assign value
        previous[node] = None                                     # O(1) constant assign value
    while priority_queue:                                         # O(1) loop 
        current_node = min(priority_queue, key=lambda n: distance[n]) # O(1) space
        priority_queue.pop(current_node)                          # O(1) remove vertex
        if current_node == target:                                # O(1) checking a constant
            break                                                 # O(1) break
                                                                 
        for neighbor, weight in graph.get(current_node, {}).items():  # O(1) loop
            new_distance = distance[current_node] + weight        # O(1) addition
            if new_distance < distance[neighbor]:                 # O(1) comparing constants
                distance[neighbor] = float(new_distance)          # O(1) updating constants
                previous[neighbor] = float(current_node)          # O(1) updating constant
    if distance[target] == float('inf'):                          # O(1) comparing constants
        return [], float('inf')                                   # O(1) constant
    path = []                                                     # O(1) constant
    current = target                                              # O(1) constant
    while current is not None:                                    # O(1) constant
        path.insert(0, current)                                   # O(k) constant
        current = previous[current]                               # O(1) updating constant
    return path, distance[target]                                 # O(1)

```
*The dijkstra algorithm uses four main data structures which are distance, previous, priority_queue, and path. Each one 
requires O(V) space because the size depends on the input of vertexes. Therefore, i conclude that the Space Complexity is 
O(V).*

### Empirical Data - Dijkstra's With Linear PQ
| V    | E         | Time (sec) |
|------|-----------|------------|
| 500  | 75000.0   | 0.009      |
| 1000 | 300000.0  | 0.039      |
| 1500 | 675000.0  | 0.086      |
| 2000 | 1200000.0 | 0.154      |
| 2500 | 1875000.0 | 0.243      |
| 3000 | 2700000.0 | 0.337      |
| 3500 | 3675000.0 | 0.489      |

### Comparison of Theoretical and Empirical Results - Dijkstra's With Linear PQ

- Theoretical order of growth: O(V^2) 
- Empirical order of growth (if different from theoretical): 3.856836644345053e-08

![baseline_empirical.png](baseline_empirical.png)

*My theoretical order of growth was O(v^2) which fit my observed data. There was an outlier however most of the data fit
my theoretical order of growth therefore i saw no reason to find a empirical order of growth*

## Core

### Design Experience

*I talked to Kyle Mak and Collin Verbanatz about the implementing dijkstra's algorithm by using heaps. *

### Theoretical Analysis - Dijkstra's With Heap PQ

#### Time 

*Fill me in*

#### Space

*Fill me in*

### Empirical Data - Dijkstra's With Heap PQ

| N    | Density | time (ms) |
|------|---------|-----------|
| 500  | .2      |           |
| 1000 | .2      |           |
| 1500 | .2      |           |
| 2000 | .2      |           |
| 2500 | .2      |           |
| 3000 | .2      |           |
| 3500 | .2      |           |



### Comparison of Theoretical and Empirical Results - Dijkstra's With Heap PQ

- Theoretical order of growth: *copy from section above* 
- Empirical order of growth (if different from theoretical): 

![img](img.png)

*Fill me in*

### Relative Performance Of Linear versus Heap PQ Performance

*Fill me in*

## Stretch 1

### Design Experience

*Fill me in*

### Empirical Data

| N    | Density | heap time (ms) | linear PQ time (ms) |
|------|---------|----------------|---------------------|
| 500  | .6      |                |                     |
| 1000 | .6      |                |                     |
| 1500 | .6      |                |                     |
| 2000 | .6      |                |                     |
| 2500 | .6      |                |                     |
| 3000 | .6      |                |                     |
| 3500 | .6      |                |                     |


| N    | Density | heap time (ms) | linear PQ time (ms) |
|------|---------|----------------|---------------------|
| 500  | 1       |                |                     |
| 1000 | 1       |                |                     |
| 1500 | 1       |                |                     |
| 2000 | 1       |                |                     |
| 2500 | 1       |                |                     |
| 3000 | 1       |                |                     |
| 3500 | 1       |                |                     |

### Plot

*Fill me in*

### Discussion

*Fill me in*

## Stretch 2

### Design Experience

*Fill me in*

### Provided Graph Generation Algorithm Explanation

*Fill me in*

### Selected Graph Generation Algorithm Explanation

*Fill me in*

#### Screenshots of Working Graph Generation Algorithm

![img](small.png)

![img](medium.png)

![img](large.png)

## Project Review

*Fill me in*

