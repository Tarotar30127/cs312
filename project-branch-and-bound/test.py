import math
import random
import time
import heapq
import copy


# ==========================================
# 1. MOCK DEPENDENCIES (So it runs standalone)
# ==========================================

class Timer:
    def __init__(self, limit):
        self.start_time = time.time()
        self.limit = limit

    def time_out(self):
        return (time.time() - self.start_time) > self.limit

    def time(self):
        return time.time() - self.start_time


class SolutionStats:
    def __init__(self, tour, score, time, max_queue_size, n_nodes_expanded, n_nodes_pruned, n_leaves_covered,
                 fraction_leaves_covered):
        self.tour = tour
        self.score = score
        self.time = time
        self.max_queue_size = max_queue_size
        self.n_nodes_expanded = n_nodes_expanded
        self.n_nodes_pruned = n_nodes_pruned
        self.n_leaves_covered = n_leaves_covered
        self.fraction_leaves_covered = fraction_leaves_covered

    def __repr__(self):
        return f"Stats(score={self.score:.3f}, time={self.time:.3f})"


class CutTree:
    def __init__(self, n):
        self.n = n

    def cut(self, path):
        pass

    def n_leaves_cut(self):
        return 0

    def fraction_leaves_covered(self):
        return 0.0


def score_tour(tour, edges):
    cost = 0
    for i in range(len(tour)):
        u, v = tour[i], tour[(i + 1) % len(tour)]
        cost += edges[u][v]
    return cost


def generate_network(n, seed=None, **kwargs):
    if seed is not None:
        random.seed(seed)
    # Generate random 2D points
    points = [(random.random() * 100, random.random() * 100) for _ in range(n)]

    # Create Adjacency Matrix (Euclidean)
    edges = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i == j:
                edges[i][j] = math.inf
            else:
                dist = math.sqrt((points[i][0] - points[j][0]) ** 2 + (points[i][1] - points[j][1]) ** 2)
                edges[i][j] = dist
    return points, edges


# ==========================================
# 2. YOUR SOLVER CODE
# ==========================================

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
    cut_tree = CutTree(n)

    results = []
    greedy_solutions = greedy_tour(edges, timer)

    if greedy_solutions:
        initial_best = greedy_solutions[-1]
        results.append(initial_best)
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
    k = 6  # NOTE: Your beam width is 6 here

    while stack and not timer.time_out():
        if len(stack) > max_queue_size:
            max_queue_size = len(stack)

        current_state = stack.pop()
        if current_state.lower_bound >= bssf:
            pruned += 1
            cut_tree.cut(current_state.path)
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

                    new_stat = SolutionStats(
                        tour=best_solution_path,
                        score=bssf,
                        time=timer.time(),
                        max_queue_size=max_queue_size,
                        n_nodes_expanded=count,
                        n_nodes_pruned=pruned,
                        n_leaves_covered=cut_tree.n_leaves_cut(),
                        fraction_leaves_covered=cut_tree.fraction_leaves_covered()
                    )
                    results.append(new_stat)
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
                cut_tree.cut(child.path)

        potential_children.sort(key=lambda x: x.lower_bound)
        if len(potential_children) > k:
            best_children = potential_children[:k]
            dropped_children = potential_children[k:]
            for child in dropped_children:
                pruned += 1
                cut_tree.cut(child.path)
        else:
            best_children = potential_children

        stack.extend(reversed(best_children))

        count += 1

    if not results and best_solution_path:
        results.append(SolutionStats(
            tour=best_solution_path,
            score=bssf,
            time=timer.time(),
            max_queue_size=max_queue_size,
            n_nodes_expanded=count,
            n_nodes_pruned=pruned,
            n_leaves_covered=cut_tree.n_leaves_cut(),
            fraction_leaves_covered=cut_tree.fraction_leaves_covered()
        ))

    return results


def branch_and_bound_smart(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:
    n = len(edges)
    initial_matrix = [row[:] for row in edges]
    cut_tree = CutTree(n)

    results = []
    greedy_solutions = greedy_tour(edges, timer)

    if greedy_solutions:
        initial_best = greedy_solutions[-1]
        results.append(initial_best)
        bssf = initial_best.score
        best_solution_path = initial_best.tour
    else:
        bssf = math.inf
        best_solution_path = []

    root_state = MatrixClass(
        initial_matrix, 0, [0], set(range(1, n)), 0
    )
    root_state.reduce_matrix()
    count = 0
    # PRIORITY = LOWER BOUND / DEPTH
    root_priority = root_state.lower_bound / max(1, len(root_state.path))  # avoid div by zero safely

    pq = [(root_priority, count, root_state)]
    heapq.heapify(pq)

    pruned = 0
    max_queue_size = 0

    while pq and not timer.time_out():
        if len(pq) > max_queue_size:
            max_queue_size = len(pq)

        _, _, current_state = heapq.heappop(pq)

        if current_state.lower_bound >= bssf:
            pruned += 1
            cut_tree.cut(current_state.path)
            continue

        if not current_state.unvisited:
            last_city = current_state.path[-1]
            start_city = current_state.path[0]
            if edges[last_city][start_city] < math.inf:

                total_cost = current_state.lower_bound  # Assuming Reduced Cost Matrix logic
                # Safest to recalculate/verify if your matrix logic is complex:
                # total_cost = current_state.actual_cost + edges[last_city][start_city]

                if total_cost < bssf:
                    bssf = total_cost
                    best_solution_path = current_state.path

                    new_stat = SolutionStats(
                        tour=best_solution_path,
                        score=bssf,
                        time=timer.time(),
                        max_queue_size=max_queue_size,
                        n_nodes_expanded=count,
                        n_nodes_pruned=pruned,
                        n_leaves_covered=cut_tree.n_leaves_cut(),
                        fraction_leaves_covered=cut_tree.fraction_leaves_covered()
                    )
                    results.append(new_stat)
            continue

        current_city = current_state.path[-1]
        candidate_cities = list(current_state.unvisited)

        for next_city in candidate_cities:
            child = current_state.update_matrix(next_city, edges)
            if child.lower_bound < bssf:
                child_priority = child.lower_bound / len(child.path)
                count += 1
                heapq.heappush(pq, (child_priority, count, child))
            else:
                pruned += 1
                cut_tree.cut(child.path)

    if not results and best_solution_path:
        results.append(SolutionStats(
            tour=best_solution_path,
            score=bssf,
            time=timer.time(),
            max_queue_size=max_queue_size,
            n_nodes_expanded=count,
            n_nodes_pruned=pruned,
            n_leaves_covered=cut_tree.n_leaves_cut(),
            fraction_leaves_covered=cut_tree.fraction_leaves_covered()
        ))

    return results


# ==========================================
# 3. SEED FINDER LOOP
# ==========================================

def find_winning_seed():
    print("--- Starting Seed Search ---")

    # PARAMETERS
    N_CITIES = 16  # Keep small enough to be fast, large enough to be tricky
    TIMEOUT = 2.0  # Seconds per run

    for seed in range(1, 200):
        # 1. Generate Problem
        locations, edges = generate_network(N_CITIES, seed=seed)

        # 2. Run Standard B&B
        # Note: We must Deep Copy edges because solvers might modify them!
        timer_bnb = Timer(TIMEOUT)
        bnb_stats = branch_and_bound(copy.deepcopy(edges), timer_bnb)
        if not bnb_stats:
            print(f"Seed {seed}: B&B Failed to return stats.")
            continue
        bnb_score = bnb_stats[-1].score

        # 3. Run Smart B&B
        timer_smart = Timer(TIMEOUT)
        smart_stats = branch_and_bound_smart(copy.deepcopy(edges), timer_smart)
        if not smart_stats:
            print(f"Seed {seed}: Smart Failed to return stats.")
            continue
        smart_score = smart_stats[-1].score

        print(f"Seed {seed}: BnB={bnb_score:.2f} vs Smart={smart_score:.2f}")

        # 4. Check for Win
        # Use a small epsilon for float comparison safety
        if smart_score < bnb_score - 0.0001:
            print("\n" + "=" * 40)
            print(f"VICTORY FOUND at SEED {seed}!")
            print(f"Standard B&B Score: {bnb_score}")
            print(f"Smart B&B Score:    {smart_score}")
            print("=" * 40)
            break


find_winning_seed()