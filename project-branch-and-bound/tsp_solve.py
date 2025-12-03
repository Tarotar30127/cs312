import heapq
import math
import random

from tsp_core import Tour, SolutionStats, Timer, score_tour, Solver
from tsp_cuttree import CutTree

PARAMS_FOR_SMART_BRANCH_AND_BOUND_SMART_TEST = {
    "n": 30,
    "euclidean": True,
    "reduction": 0.2,
    "normal": False,
    "seed": 312,
    "timeout": 20
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


def dfs(edges, timer):
    num_nodes = len(edges)
    cut_tree = CutTree(num_nodes)
    max_queue_size = 1
    n_nodes_expanded = 0
    n_nodes_pruned = 0
    n_leaves_covered = 0
    fraction_leaves_covered = 0.0

    greedy_solution_list = greedy_tour(edges, timer)

    if greedy_solution_list:
        initial_bssf = greedy_solution_list[-1]
        best_tour = initial_bssf.tour
        best_score = initial_bssf.score
        best_time = initial_bssf.time
    else:
        best_tour = []
        best_score = math.inf
        best_time = timer.time()

    bssf = SolutionStats(
        tour=best_tour,
        score=best_score,
        time=best_time,
        max_queue_size=max_queue_size,
        n_nodes_expanded=n_nodes_expanded,
        n_nodes_pruned=n_nodes_pruned,
        n_leaves_covered=n_leaves_covered,
        fraction_leaves_covered=fraction_leaves_covered
    )

    stack = [(0, 0.0, 0)]
    path = [0]
    visited = {0}

    max_queue_size = max(1, max_queue_size)

    while stack:
        max_queue_size = max(max_queue_size, len(stack))

        if timer.time_out():
            bssf.time = timer.time()
            bssf.max_queue_size = max_queue_size
            bssf.n_nodes_expanded = n_nodes_expanded
            bssf.n_nodes_pruned = n_nodes_pruned
            bssf.n_leaves_covered = n_leaves_covered
            bssf.fraction_leaves_covered = cut_tree.fraction_leaves_covered()
            return [bssf]

        current_node, current_cost, neighbor_index = stack[-1]

        if neighbor_index == 0:
            n_nodes_expanded += 1

        if current_cost >= bssf.score:
            n_nodes_pruned += 1
            cut_tree.cut(path)
            stack.pop()
            visited.remove(current_node)
            path.pop()
            continue

        found_next_node = False
        for i in range(neighbor_index, num_nodes):
            neighbor = i
            stack[-1] = (current_node, current_cost, i + 1)

            cost_to_neighbor = edges[current_node][neighbor]

            if neighbor not in visited and cost_to_neighbor != math.inf:
                new_cost = current_cost + cost_to_neighbor

                if new_cost >= bssf.score:
                    n_nodes_pruned += 1
                    cut_tree.cut(path + [neighbor])
                    continue

                if len(path) + 1 == num_nodes:
                    n_leaves_covered += 1
                    cut_tree.cut(path + [neighbor])

                    cost_to_start = edges[neighbor][0]

                    if cost_to_start != math.inf:
                        total_cost = new_cost + cost_to_start

                        if total_cost < bssf.score:
                            bssf.tour = path.copy() + [neighbor]
                            bssf.score = total_cost
                            bssf.time = timer.time()
                else:
                    visited.add(neighbor)
                    path.append(neighbor)
                    stack.append((neighbor, new_cost, 0))
                    found_next_node = True
                    break

        if not found_next_node:
            stack.pop()
            visited.remove(current_node)
            path.pop()

    bssf.time = timer.time()
    bssf.max_queue_size = max_queue_size
    bssf.n_nodes_expanded = n_nodes_expanded
    bssf.n_nodes_pruned = n_nodes_pruned
    bssf.n_leaves_covered = n_leaves_covered
    bssf.fraction_leaves_covered = 1.0
    return [bssf]


class MatrixClass:
    __slots__ = ['matrix', 'lower_bound', 'path', 'unvisited', 'actual_cost']

    def __init__(self, matrix, lower_bound, path, unvisited, actual_cost=0.0):
        self.matrix = matrix
        self.lower_bound = lower_bound
        self.path = path
        self.unvisited = unvisited
        self.actual_cost = actual_cost

    def reduce_matrix(self):
        reduction_cost = 0
        matrix = self.matrix
        n = len(matrix)
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

    def update_matrix(self, city_index, edges):
        current_city = self.path[-1]
        new_matrix = [row[:] for row in self.matrix]

        reduced_edge_cost = self.matrix[current_city][city_index]
        if reduced_edge_cost == math.inf:
            return MatrixClass(new_matrix, math.inf, self.path + [city_index], set(), math.inf)

        actual_edge_cost = edges[current_city][city_index]
        if actual_edge_cost == math.inf:
            return MatrixClass(new_matrix, math.inf, self.path + [city_index], set(), math.inf)

        n = len(new_matrix)
        for i in range(n):
            new_matrix[current_city][i] = math.inf
            new_matrix[i][city_index] = math.inf

        start_city = self.path[0]
        new_matrix[city_index][start_city] = math.inf

        new_path = self.path + [city_index]
        new_unvisited = self.unvisited.copy()
        new_unvisited.remove(city_index)
        child_state = MatrixClass(new_matrix, self.lower_bound + reduced_edge_cost, new_path, new_unvisited,
                                  self.actual_cost + actual_edge_cost)
        reduction_cost = child_state.reduce_matrix()
        if reduction_cost == math.inf:
            child_state.lower_bound = math.inf
            child_state.actual_cost = math.inf
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
        initial_matrix, 0, [0], set(range(1, n)), 0
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
                total_cost = current_state.actual_cost + return_cost
                if total_cost < bssf:
                    bssf = total_cost
                    best_solution_path = current_state.path
            continue
        current_city = current_state.path[-1]
        candidate_cities = list(current_state.unvisited)

        potential_children = []

        for next_city in candidate_cities:
            child = current_state.update_matrix(next_city, edges)
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
    return [SolutionStats(
        tour=best_solution_path,
        score=bssf,
        time=timer.time(),
        max_queue_size=max_queue_size,
        n_nodes_expanded=count,
        n_nodes_pruned=pruned,
        n_leaves_covered=0,
        fraction_leaves_covered=0.0
    )]


def branch_and_bound_smart(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:
    return []

