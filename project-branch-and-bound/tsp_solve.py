import heapq
import math
import random

from tsp_core import Tour, SolutionStats, Timer, score_tour, Solver
from tsp_cuttree import CutTree

PARAMS_FOR_SMART_BRANCH_AND_BOUND_SMART_TEST = {
    "n": 15,
    "euclidean": True,
    "reduction": 0.2,
    "normal": False,
    "seed": 100,
    "timeout": 40
}


def random_tour(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:
    stats = []
    n_nodes_expanded = 0
    n_nodes_pruned = 0
    cut_tree = CutTree(len(edges))

    while True:
        if timer.time_out():
            return stats

        tour = random.sample(list(range(len(edges))), len(edges))
        n_nodes_expanded += 1

        cost = score_tour(tour, edges)
        if math.isinf(cost):
            n_nodes_pruned += 1
            cut_tree.cut(tour)
            continue

        if stats and cost > stats[-1].score:
            n_nodes_pruned += 1
            cut_tree.cut(tour)
            continue

        stats.append(SolutionStats(
            tour=tour,
            score=cost,
            time=timer.time(),
            max_queue_size=1,
            n_nodes_expanded=n_nodes_expanded,
            n_nodes_pruned=n_nodes_pruned,
            n_leaves_covered=cut_tree.n_leaves_cut(),
            fraction_leaves_covered=cut_tree.fraction_leaves_covered()
        ))

    if not stats:
        return [SolutionStats(
            [],
            math.inf,
            timer.time(),
            1,
            n_nodes_expanded,
            n_nodes_pruned,
            cut_tree.n_leaves_cut(),
            cut_tree.fraction_leaves_covered()
        )]


class MySolutionStats:
    def __init__(self):
        self.solutionList = []
        self.lowest = math.inf

    def return_list(self):
        return self.solutionList

    def add(self, tour, cost, time, max_q, n_exp, n_prun, n_leaves, frac_leaves):
        if cost < self.lowest:
            self.lowest = cost
            new_solution_stat = SolutionStats(
                tour=tour,
                score=cost,
                time=time,
                max_queue_size=max_q,
                n_nodes_expanded=n_exp,
                n_nodes_pruned=n_prun,
                n_leaves_covered=n_leaves,
                fraction_leaves_covered=frac_leaves
            )
            self.solutionList.append(new_solution_stat)


def greedy_tour(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:
    solution = MySolutionStats()
    n_nodes_expanded = 0
    n_nodes_pruned = 0
    for i in range(1):
        if timer.time_out():
            return solution.return_list()
        current_node = i
        tour = [i]
        visited = {i}
        current_cost = 0.0
        n_nodes_expanded += 1

        while len(visited) < len(edges):
            best_distance = math.inf
            next_node = -1

            for neighbor in range(len(edges)):
                if neighbor not in visited:
                    distance = edges[current_node][neighbor]
                    if distance < best_distance:
                        best_distance = distance
                        next_node = neighbor

            if next_node == -1:
                break

            tour.append(next_node)
            visited.add(next_node)
            current_cost += best_distance
            current_node = next_node
            n_nodes_expanded += 1

        if len(tour) == len(edges):
            cost_to_start = edges[current_node][i]
            if cost_to_start == math.inf:
                continue

            current_cost += cost_to_start
            final_tour = tour
            solution.add(
                tour=final_tour,
                cost=current_cost,
                time=timer.time(),
                max_q=1,
                n_exp=n_nodes_expanded,
                n_prun=n_nodes_pruned,
                n_leaves=0,
                frac_leaves=0.0
            )

    return solution.return_list()


def dfs(edges, timer, stack, bssf_cost, stats_history):
    n = len(edges)
    cut_tree = CutTree(n)

    max_queue_size = 1
    n_expanded = 0
    n_pruned = 0

    while stack:
        if timer.time_out():
            return stats_history

        if len(stack) > max_queue_size:
            max_queue_size = len(stack)

        current_state = stack.pop()

        if current_state.lower_bound >= bssf_cost:
            n_pruned += 1
            cut_tree.cut(current_state.path)
            continue

        if len(current_state.path) == n:
            last_city = current_state.path[-1]
            first_city = current_state.path[0]

            if edges[last_city][first_city] < math.inf:
                total_cost = current_state.lower_bound + edges[last_city][first_city]

                if total_cost < bssf_cost:
                    bssf_cost = total_cost
                    bssf_tour = current_state.path

                    stats_history.append(SolutionStats(
                        tour=bssf_tour,
                        score=bssf_cost,
                time=timer.time(),
                max_queue_size=max_queue_size,
                        n_nodes_expanded=n_expanded,
                        n_nodes_pruned=n_pruned,
                        n_leaves_covered=cut_tree.n_leaves_cut(),
                fraction_leaves_covered=cut_tree.fraction_leaves_covered()
                    ))
            continue

        n_expanded += 1
        children = []

        for next_city in current_state.unvisited:
            child = current_state.create_child(next_city, edges)

            if child.lower_bound < bssf_cost:
                children.append(child)
            else:
                n_pruned += 1
                cut_tree.cut(child.path)

        children.sort(key=lambda x: x.lower_bound, reverse=True)
        stack.extend(children)

    return stats_history


class MatrixClass:
    __slots__ = ['matrix', 'lower_bound', 'path', 'unvisited']

    def __init__(self, matrix, lower_bound, path, unvisited):
        self.matrix = matrix
        self.lower_bound = lower_bound
        self.path = path
        self.unvisited = unvisited

    def reduce_matrix(self):
        reduction_cost = 0
        n = len(self.matrix)
        for r in range(n):
            row = self.matrix[r]
            min_val = math.inf
            has_vals = False
            for val in row:
                if val < min_val:
                    min_val = val
                if val != math.inf:
                    has_vals = True
            if not has_vals:
                continue

            if min_val == math.inf:
                return math.inf

            if min_val > 0:
                reduction_cost += min_val
                for c in range(n):
                    if self.matrix[r][c] != math.inf:
                        self.matrix[r][c] -= min_val

        for c in range(n):
            min_val = math.inf
            has_vals = False

            for r in range(n):
                val = self.matrix[r][c]
                if val < min_val:
                    min_val = val
                if val != math.inf:
                    has_vals = True

            if not has_vals:
                continue

            if min_val == math.inf:
                return math.inf

            if min_val > 0:
                reduction_cost += min_val
                for r in range(n):
                    if self.matrix[r][c] != math.inf:
                        self.matrix[r][c] -= min_val

        self.lower_bound += reduction_cost
        return reduction_cost

    def create_child(self, city_index, edges):
        current_city = self.path[-1]
        new_matrix = [row[:] for row in self.matrix]

        edge_cost = self.matrix[current_city][city_index]
        n = len(new_matrix)
        for i in range(n):
            new_matrix[current_city][i] = math.inf
            new_matrix[i][city_index] = math.inf

        start_city = self.path[0]
        new_matrix[city_index][start_city] = math.inf

        new_path = self.path + [city_index]
        new_unvisited = self.unvisited.copy()
        new_unvisited.remove(city_index)

        child_state = MatrixClass(new_matrix, self.lower_bound + edge_cost, new_path, new_unvisited)
        child_state.reduce_matrix()
        return child_state


def branch_and_bound(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:
    n = len(edges)
    initial_matrix = [row[:] for row in edges]
    greedy_solutions = greedy_tour(edges, timer)
    if greedy_solutions:
        initial_best = greedy_solutions[-1]
        bssf = initial_best.score
        best_solution_path = initial_best.tour
    else:
        bssf = math.inf
        best_solution_path = []

    root_state = MatrixClass(
        initial_matrix,
        0,
        [0],
        set(range(1, n))
    )
    root_state.reduce_matrix()
    stack = [root_state]

    count = 0
    pruned = 0
    max_queue_size = 0
    k = 4

    while stack and not timer.time_out():
        if len(stack) > max_queue_size:
            max_queue_size = len(stack)

        current_state = stack.pop()
        if current_state.lower_bound >= bssf:
            pruned += 1
            continue

        if not current_state.unvisited:
            last_city = current_state.path[-1]
            start_city = current_state.path[0]
            return_cost = edges[last_city][start_city]

            if return_cost < math.inf:
                total_cost = score_tour(current_state.path, edges)
                if total_cost < bssf:
                    bssf = total_cost
                    best_solution_path = current_state.path.copy()
            continue

        current_city = current_state.path[-1]
        candidate_cities = list(current_state.unvisited)
        potential_children = []

        for next_city in candidate_cities:
            child = current_state.create_child(next_city, edges)
            if child.lower_bound < bssf:
                potential_children.append(child)
            else:
                pruned += 1

        potential_children.sort(key=lambda x: x.lower_bound)
        if len(potential_children) > k:
            pruned += (len(potential_children) - k)
            best_children = potential_children[:k]
        else:
            best_children = potential_children

        stack.extend(reversed(best_children))
        count += 1

    results = []
    if best_solution_path:
        results.append(SolutionStats(
            tour=best_solution_path.copy() if isinstance(best_solution_path, list) else best_solution_path,
            score=bssf,
            time=timer.time(),
            max_queue_size=max_queue_size,
            n_nodes_expanded=count,
            n_nodes_pruned=pruned,
            n_leaves_covered=0,
            fraction_leaves_covered=0.0
        ))
    return results


def branch_and_bound_smart(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:
    n = len(edges)
    initial_matrix = [row[:] for row in edges]
    cut_tree = CutTree(n)
    results = []
    
    greedy_solutions = greedy_tour(edges, timer)
    for stat in greedy_solutions:
        results.append(stat)
    
    if len(greedy_solutions) > 0:
        score_to_beat = greedy_solutions[-1].score
    else:
        score_to_beat = math.inf
    
    priority_queue = []
    counter = 0
    
    n_nodes_expanded = 0
    n_nodes_pruned = 0
    max_queue_size = 1

    root_state = MatrixClass(initial_matrix, 0, [0], set(range(1, n)))
    root_state.reduce_matrix()
    root_priority = root_state.lower_bound if root_state.lower_bound != math.inf else float('inf')
    
    heapq.heappush(priority_queue, (root_priority, counter, root_state))
    counter += 1
    
    MAX_QUEUE_SIZE = 50000
    
    while not timer.time_out() and len(priority_queue) > 0:
        current_queue_size = len(priority_queue)
        if current_queue_size > max_queue_size:
            max_queue_size = current_queue_size
        
        if current_queue_size > MAX_QUEUE_SIZE:
            temp_list = []
            while len(priority_queue) > 0:
                temp_list.append(heapq.heappop(priority_queue))
            
            temp_list.sort(key=lambda x: x[0])
            keep_count = int(len(temp_list) * 0.7)
            
            for item in temp_list[:keep_count]:
                heapq.heappush(priority_queue, item)
            
            for item in temp_list[keep_count:]:
                n_nodes_pruned += 1
                cut_tree.cut(item[2].path)
        
        _, _, current_state = heapq.heappop(priority_queue)
        n_nodes_expanded += 1

        if current_state.lower_bound >= score_to_beat:
            n_nodes_pruned += 1
            cut_tree.cut(current_state.path)
            continue

        path_len = len(current_state.path)
        
        if path_len == n:
            tour = list(current_state.path)
            cost = 0
            for i in range(len(tour)):
                next_i = (i + 1) % len(tour)
                cost += edges[tour[i]][tour[next_i]]
            
            if cost != math.inf and cost <= score_to_beat:
                score_to_beat = cost
                results.append(SolutionStats(
                    tour=tour,
                    score=cost,
                        time=timer.time(),
                        max_queue_size=max_queue_size,
                    n_nodes_expanded=n_nodes_expanded,
                    n_nodes_pruned=n_nodes_pruned,
                        n_leaves_covered=cut_tree.n_leaves_cut(),
                        fraction_leaves_covered=cut_tree.fraction_leaves_covered()
                ))
        else:
            children = []
            
            for next_city in current_state.unvisited:
                if current_state.matrix[current_state.path[-1]][next_city] == math.inf:
                    continue
                
                child = current_state.create_child(next_city, edges)
                
                if score_to_beat < child.lower_bound:
                    n_nodes_pruned += 1
                    cut_tree.cut(child.path)
                else:
                    # Use lower_bound directly as priority for best-first search
                    child_priority = child.lower_bound if child.lower_bound != math.inf else float('inf')
                    
                    children.append((child_priority, counter, child))
                    counter += 1
            
            if len(children) > 0:
                children.sort(key=lambda x: x[0])
                max_children_to_keep = min(20, len(children))
                bound_multiplier = 3.0
                
                best_bound = children[0][0]
                keep_children = []
                keep_indices = set()
                for i, child in enumerate(children):
                    if child[0] <= best_bound * bound_multiplier:
                        keep_children.append(child)
                        keep_indices.add(i)
                
                if len(keep_children) < max_children_to_keep:
                    for i, child in enumerate(children):
                        if i not in keep_indices:
                            keep_children.append(child)
                            keep_indices.add(i)
                            if len(keep_children) >= max_children_to_keep:
                                break
                for i, child in enumerate(children):
                    if i not in keep_indices:
                        n_nodes_pruned += 1
                        cut_tree.cut(child[2].path)
                for child in keep_children:
                    heapq.heappush(priority_queue, child)

    return results
