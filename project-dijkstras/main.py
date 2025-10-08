import argparse
import math
import random
from time import time

# These imports are assumed to exist from your project structure
# If they are in the same directory, this will work.
# Otherwise, you might need to adjust the import paths.
from plotting import plot_points, draw_path, circle_point, title, show_plot, plot_weights
from network_routing import find_shortest_path_with_linear_pq, find_shortest_path_with_heap


def rand1to1():
    """Returns a random float between -1.0 and 1.0."""
    return (random.random() - 0.5) * 2


def _get_points(size: int, distribution: str):
    """Generates a list of (x, y) coordinates based on a specified distribution."""
    distribution = distribution.lower()

    if distribution in ['normal', 'gaussian']:
        def rand_func():
            return random.normalvariate(0, 0.4), random.normalvariate(0, 0.4)
    elif distribution == 'uniform':
        def rand_func():
            return rand1to1(), rand1to1()
    elif distribution in ['oval', 'circular', 'circle']:
        def rand_func():
            while (x := rand1to1()) ** 2 + (y := rand1to1()) ** 2 > 0.98 ** 2:
                pass  # generate x,y pairs until they fit in the circle
            return x, y
    elif distribution in ['spherical', 'sphere']:
        def rand_func():
            while (x := rand1to1()) ** 2 + (y := rand1to1()) ** 2 + (rand1to1()) > 0.98 ** 2:
                pass  # generate x,y,z pairs until they fit in the sphere
            return x, y  # only return the x,y part
    else:
        raise NotImplementedError(f'Random distribution of type: {distribution}')

    return [rand_func() for _ in range(size)]


def dist(p1, p2, noise):
    """Calculates the distance between two points with optional noise."""
    if noise == -1:
        return random.random()
    raw_dist = math.dist(p1, p2)
    return max(0.0, raw_dist + random.normalvariate(mu=0, sigma=noise))


def generate_graph(seed: int, size: int, density: float, noise: float, distribution='gaussian') -> tuple[
    list[tuple[float, float]],  # The positions
    dict[int, dict[int, float]]  # The graph
]:
    """Generates a random graph with specified properties."""
    random.seed(seed)
    positions = _get_points(size, distribution)
    edges_per_node = int(round((size - 1) * density))
    if edges_per_node == 0 and size > 1 and density > 0:
        edges_per_node = 1

    weights = {}
    for source in range(size):
        weights[source] = {}
        # Ensure target is not the same as the source for the sample
        possible_targets = [i for i in range(size) if i != source]

        # Handle cases where edges_per_node is larger than possible targets
        num_targets = min(edges_per_node, len(possible_targets))

        for target in random.sample(possible_targets, num_targets):
            weights[source][target] = dist(positions[source], positions[target], noise)

    return positions, weights


def run_experiment(seed: int, size: int, density: float, noise: float, distribution: str, source: int, target: int):
    """
    Generates a graph, runs both shortest path algorithms, and returns their runtimes.
    This version is optimized for data collection and does no plotting.
    """
    # Generate the graph
    _, weights = generate_graph(seed, size, density, noise, distribution)

    # Time Heap PQ implementation
    start_heap = time()
    find_shortest_path_with_heap(weights, source, target)
    end_heap = time()
    heap_time = end_heap - start_heap

    # Time Linear PQ (Array) implementation
    start_linear = time()
    find_shortest_path_with_linear_pq(weights, source, target)
    end_linear = time()
    linear_time = end_linear - start_linear

    return heap_time, linear_time


def visualize_single_run(seed: int, size: int, density: float, noise: float, distribution: str, source: int,
                         target: int):
    """
    Generates a graph, runs both algorithms, prints detailed results, and creates a plot.
    This is the original functionality of the `main` function for visualization.
    """
    start_gen = time()
    positions, weights = generate_graph(seed, size, density, noise, distribution)
    end_gen = time()
    num_edges = sum(len(edges) for edges in weights.values())
    print(f'Time to generate network of {size} nodes and {num_edges} edges: {round(end_gen - start_gen, 4)}')

    print(f'Direct cost from {source} to {target}: {weights.get(source, {}).get(target, math.inf)}')

    plot_points(positions)
    if num_edges < 50:
        plot_weights(positions, weights)

    circle_point(positions[source], c='r')
    circle_point(positions[target], c='b')

    # --- Heap PQ Run ---
    start_heap = time()
    path_heap, cost_heap = find_shortest_path_with_heap(weights, source, target)
    end_heap = time()
    heap_time = end_heap - start_heap
    print("\n-- Heap PQ --")
    print(f'Path: {path_heap}')
    print(f'Cost: {cost_heap}')
    print(f'Time: {heap_time}')
    draw_path(positions, path_heap)  # Draw the path found by heap

    # --- Linear PQ (Array) Run ---
    start_linear = time()
    path_linear, cost_linear = find_shortest_path_with_linear_pq(weights, source, target)
    end_linear = time()
    linear_time = end_linear - start_linear
    print("\n-- Linear Array PQ --")
    print(f'Path: {path_linear}')
    print(f'Cost: {cost_linear}')
    print(f'Time: {linear_time}')

    # Update title and show plot
    title(f'Size={size}, Density={density}, Heap={round(heap_time, 4)}s, Array={round(linear_time, 4)}s')
    show_plot()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Analyze shortest path algorithm performance.")
    parser.add_argument('--collect-data', action='store_true', help='Run in data collection mode.')
    # Default values for visualization mode below are not used for data collection
    parser.add_argument('-n', type=int, default=50, help='The number of points to generate.')
    parser.add_argument('--seed', type=int, default=312, help='Random seed.')
    parser.add_argument('--density', type=float, default=0.2, help='Fraction of non-inf edges.')
    parser.add_argument('--noise', type=float, default=0.05, help='How non-euclidean are the edge weights.')
    parser.add_argument('--distribution', type=str, default='uniform', help='Distribution of graph points.')
    parser.add_argument('--source', type=int, default=0, help='Starting node.')
    parser.add_argument('--target', type=int, default=None, help='Target node.')

    args = parser.parse_args()

    # --- DATA COLLECTION SCRIPT ---
    # This script will run regardless of the --collect-data flag for simplicity.

    print("Running data collection for specified tables...")

    # Define the exact sizes and densities you need
    sizes = [500, 1000, 1500, 2000, 2500, 3000, 3500]
    densities_to_test = [0.6, 1.0]

    # Print a header that matches your table, but we will print in CSV for easy copy/pasting
    print("\nN,Density,Heap_Time_ms,Linear_PQ_Time_ms")

    for density_val in densities_to_test:
        for n in sizes:
            # Ensure source and target are valid for the current size 'n'
            source_node = 0
            target_node = n - 1

            heap_t, linear_t = run_experiment(seed=args.seed,
                                              size=n,
                                              density=density_val,
                                              noise=args.noise,
                                              distribution=args.distribution,
                                              source=source_node,
                                              target=target_node)

            # Convert times to milliseconds (ms) by multiplying by 1000
            heap_t_ms = heap_t * 1000
            linear_t_ms = linear_t * 1000

            # Print the results in CSV format
            print(f"{n},{density_val},{heap_t_ms},{linear_t_ms}")

    print("\nData collection complete.")
