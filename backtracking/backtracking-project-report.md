# Project Report - Backtracking

## Baseline

### Design Experience

*I talked to Kyle Mak and Collin and we walked through a couple homework problems and slides. Then we explained it to each
other. Some edge cases we discussed were empty input and single item input and no solutions. Greedy fails when the optimal
choice is not the globally optimal test. *

### Theoretical Analysis - Greedy

#### Time

```python
class MySolutionStats:
    def __init__(self):
        self.solutionList = []                                  # O(1) constant
        self.lowest = math.inf                                  # O(1) constant

    def return_list(self):
        return self.solutionList                                # O(1) returns constant

    def add(self, tour, cost, time, max_q, n_exp, n_prun, n_leaves, frac_leaves):
        if cost < self.lowest:                                  # O(1) constant
            self.lowest = cost                                  # O(1) constant
            new_solution_stat = SolutionStats(                  # O(n) Append to list n length
                tour=tour,
                score=cost,
                time=time,
                max_queue_size=max_q,
                n_nodes_expanded=n_exp,
                n_nodes_pruned=n_prun,
                n_leaves_covered=n_leaves,
                fraction_leaves_covered=frac_leaves
            )
            self.solutionList.append(new_solution_stat)          # O(1) append to list
            
def greedy_tour(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:
    solution = MySolutionStats()                                 # O(1) Create a new variable class 
    n_nodes_expanded = 0                                         # O(1) Constant
    n_nodes_pruned = 0                                           # O(1) constant
    for i in range(len(edges)):                                  # O(n) loops all edges
        if timer.time_out():                                     # O(1) Constant
            return solution.return_list()                        # O(1) constant
        current_node = i                                         # O(1) constant
        tour = [i]                                               # O(1) constant   
        visited = {i}                                            # O(1) constant
        current_cost = 0.0                                       # O(1) constant
        n_nodes_expanded += 1                                    # O(1) constant
        while len(visited) < len(edges):                         # O(n) runs edges - 1 times
            best_distance = math.inf                             # O(1) constant set var
            next_node = -1                                       # O(1) constant set var
            for neighbor in range(len(edges)):                   # O(n) loops number of edge times
                if neighbor not in visited:                      # O(1) compare constants
                    distance = edges[current_node][neighbor]     # O(1) check constants
                    if distance < best_distance:                 # O(1) compare constants
                        best_distance = distance                 # O(1) set constant
                        next_node = neighbor                     # O(1) set constant 
            if next_node == -1:                                  # O(1) set constant
                break                                            # O(1) constant

            tour.append(next_node)                               # O(1) add to list constant
            visited.add(next_node)                               # O(1) add to list constant 
            current_cost += best_distance                        # O(1) simple math constant
            current_node = next_node                             # O(1) set constant
            n_nodes_expanded += 1                                # O(1) simple math constant

        if len(tour) == len(edges):                              # O(1) set constant
            cost_to_start = edges[current_node][i]               # O(1) pull constant
            if cost_to_start == math.inf:                        # O(1) compare constant
                continue                                         # O(1) constant

            current_cost += cost_to_start                        # O(1) simple math
            final_tour = tour                                    # O(1) set constant
            solution.add(                                        # O(n) create new object 
                tour=final_tour,
                cost=current_cost,
                time=timer.time(),                               # O(1) constant
                max_q=1,
                n_exp=n_nodes_expanded,
                n_prun=n_nodes_pruned,
                n_leaves=0,
                frac_leaves=0.0
            )
    return solution.return_list()                                # O(1) constant
```

*The time complexity of the Greedy Algorithm is O(n^4) because of the outer for loop with a while loop with a nested 
inner loop plus the creating a new object n long makes the time complexity n^4.*

#### Space

```python
class MySolutionStats:
    def __init__(self):
        self.solutionList = []                                  # O(n) grows to n large
        self.lowest = math.inf                                  # O(1) space constant

    def return_list(self):
        return self.solutionList                                # O(1) space constant

    def add(self, tour, cost, time, max_q, n_exp, n_prun, n_leaves, frac_leaves):
        if cost < self.lowest:                                  # O(1) space constant
            self.lowest = cost                                  # O(1) space constant
            new_solution_stat = SolutionStats(                  # O(N) grows to n long
                tour=tour,
                score=cost,
                time=time,
                max_queue_size=max_q,
                n_nodes_expanded=n_exp,
                n_nodes_pruned=n_prun,
                n_leaves_covered=n_leaves,
                fraction_leaves_covered=frac_leaves
            )
            self.solutionList.append(new_solution_stat)          # O(1) space constant

def greedy_tour(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:

    solution = MySolutionStats()                                 # O(1) space constant
    n_nodes_expanded = 0                                         # O(1) space constant
    n_nodes_pruned = 0                                           # O(1) space constant
    for i in range(len(edges)):                                  # O(1) space constant
        if timer.time_out():                                     # O(1) space constant
            return solution.return_list()                        # O(1) space constant
        current_node = i                                         # O(1) space constant
        tour = [i]                                               # O(n) worst case grows to n long
        visited = {i}                                            # O(n) worst case grows to n long
        current_cost = 0.0                                       # O(1) space constant
        n_nodes_expanded += 1                                    # O(1) space constant

        while len(visited) < len(edges):                         # O(1) Constant overhead
            best_distance = math.inf                             # O(1) space constant
            next_node = -1                                       # O(1) space constant

            for neighbor in range(len(edges)):                   # O(1) constant overhead
                if neighbor not in visited:
                    distance = edges[current_node][neighbor]     # O(1) space constant
                    if distance < best_distance:
                        best_distance = distance                 # O(1) space constant
                        next_node = neighbor                     # O(1) space constant

            if next_node == -1:
                break                                            # O(1) space constant

            tour.append(next_node)                               # O(1) add space constant
            visited.add(next_node)                               # O(1) add to list space constant
            current_cost += best_distance                        # O(1) space constant
            current_node = next_node                             # O(1) space constant
            n_nodes_expanded += 1                                # O(1) space constant

        if len(tour) == len(edges):
            cost_to_start = edges[current_node][i]               # O(1) space constant
            if cost_to_start == math.inf:
                continue                                         # O(1) space constant

            current_cost += cost_to_start                        # O(1) space constant
            final_tour = tour                                    # O(1) space constant
            
            solution.add(                                        # O(n) goes to n long
                tour=final_tour,
                cost=current_cost,
                time=timer.time(),
                max_q=1,
                n_exp=n_nodes_expanded,
                n_prun=n_nodes_pruned,
                n_leaves=0,
                frac_leaves=0.0
            )

    return solution.return_list()                               # O(1) space constant
```

*My space complexity is O(n^2) because of the objects that grow to n length.*

### Empirical Data - Greedy


| N  | Time (ms) |
|----|-----------|
| 5  | 0.0208    |
| 10 | 0.0743    |
| 15 | 0.205     |
| 20 | 0.4323    |
| 25 | 0.7853    |
| 30 | 1.2464    |
| 35 | 1.7921    |
| 40 | 2.5356    |
| 45 | 3.317     |
| 50 | 4.2963    |


### Comparison of Theoretical and Empirical Results - Greedy

- Theoretical order of growth: O(n^4)
![greedy_runtime_graph_core_th.svg](greedy_runtime_graph_core_th.svg)
- Empirical order of growth (if different from theoretical): O(2.5)
![Emp_greedy_runtime_graph_core_th.svg](Emp_greedy_runtime_graph_core_th.svg)
## Core

### Design Experience

*Fill me in*

### Theoretical Analysis - Backtracking

#### Time 

*Fill me in*

#### Space

*Fill me in*

### Empirical Data - Backtracking

| N   | reduction | time (ms) |
|-----|-----------|-----------|
| 5   | 0         |           |
| 10  | 0         |           |
| 15  | 0         |           |
| 20  | 0         |           |
| 25  | 0         |           |
| 30  | 0         |           |
| 35  | 0         |           |
| 40  | 0         |           |
| 45  | 0         |           |
| 50  | 0         |           |

### Comparison of Theoretical and Empirical Results - Backtracking

- Theoretical order of growth: 
- Empirical order of growth (if different from theoretical): 

### Greedy v Backtracking

*Fill me in*

### Water Bottle Scenario 

#### Scenario 1

**Algorithm:** 

*Fill me in*

#### Scenario 2

**Algorithm:** 

*Fill me in*

#### Scenario 2

**Algorithm:** 

*Fill me in*


## Stretch 1

### Design Experience

*Fill me in*

### Demonstrate BSSF Backtracking Works Better than No-BSSF Backtracking 

*Fill me in*

### BSSF Backtracking v Backtracking Complexity Differences

*Fill me in*

### Time v Solution Cost

![Plot]()

*Fill me in*

## Stretch 2

### Design Experience

*Fill me in*


| N   | reduction | time (ms) |
|-----|-----------|-----------|
| 5   | 0         |           |
| 10  | 0         |           |
| 15  | 0         |           |
| 20  | 0         |           |
| 25  | 0         |           |
| 30  | 0         |           |
| 35  | 0         |           |
| 40  | 0         |           |
| 45  | 0         |           |
| 50  | 0         |           |
### Cut Tree

*Fill me in*

### Plots 

*Fill me in*

## Project Review

*Fill me in*
