import math
import random
from utils import Tour, SolutionStats, Timer, score_tour, Solver
from cuttree import CutTree


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
    for i in range(len(edges)):
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


def backtracking(edges: list[list[float]], timer: Timer) -> SolutionStats | SolutionStats:
    stat = MySolutionStats()
    stack = []
    num_nodes = set(range(len(edges)))
    stack.append([0])

    while stack and not timer.time_out():

        current_path = stack.pop()
        current_node = current_path[-1]
        unvisited = num_nodes - set(current_path)
        if unvisited == set():
            tour = list(current_path)
            cost = score_tour(tour, edges)
            stat.add(tour, cost, timer.time(), 0, 0, 0, 0, 0.0)
        for i in unvisited:
            if edges[current_node][i] != math.inf:
                copy_temp = current_path.copy()
                copy_temp.append(i)
                stack.append(copy_temp)

    return stat.return_list()


def backtracking_bssf(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:
    num_nodes = len(edges)
    greedy_solution_list = greedy_tour(edges, timer)
    if greedy_solution_list:
        initial_bssf = greedy_solution_list[-1]
        bssf = SolutionStats(
            tour=initial_bssf.tour,
            score=initial_bssf.score,
            time=initial_bssf.time,
            max_queue_size=initial_bssf.max_queue_size,
            n_nodes_expanded=initial_bssf.n_nodes_expanded,
            n_nodes_pruned=initial_bssf.n_nodes_pruned,
            n_leaves_covered=initial_bssf.n_leaves_covered,
            fraction_leaves_covered=initial_bssf.fraction_leaves_covered
        )
    else:
        bssf = SolutionStats(
            tour=[],
            score=math.inf,
            time=timer.time(),
            max_queue_size=1,
            n_nodes_expanded=0,
            n_nodes_pruned=0,
            n_leaves_covered=0,
            fraction_leaves_covered=0.0
        )

    stack = [(0, 0.0, 0)]
    path = [0]
    visited = {0}

    bssf.max_queue_size = max(1, bssf.max_queue_size)

    while stack:
        bssf.max_queue_size = max(bssf.max_queue_size, len(stack))

        if timer.time_out():
            bssf.time = timer.time()
            return [bssf]

        current_node, current_cost, neighbor_index = stack[-1]

        if current_cost >= bssf.score:
            bssf.n_nodes_pruned += 1
            stack.pop()
            visited.remove(current_node)
            path.pop()
            continue

        found_next_node = False
        for i in range(neighbor_index, num_nodes):
            neighbor = i
            cost_to_neighbor = edges[current_node][neighbor]

            stack[-1] = (current_node, current_cost, i + 1)

            if neighbor not in visited and cost_to_neighbor != math.inf:

                new_cost = current_cost + cost_to_neighbor

                if new_cost >= bssf.score:
                    bssf.n_nodes_pruned += 1
                    continue

                if len(path) + 1 == num_nodes:
                    bssf.n_nodes_expanded += 1
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
    return [bssf]