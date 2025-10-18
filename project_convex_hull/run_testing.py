import time
import random
# This imports the 'compute_hull_dvcq' function from your first file
# Make sure your first code block is saved as 'convex_hull.py'
from convex_hull import compute_hull_dvcq, compute_hull_other


def generate_random_points(distribution: str, n: int, seed: int | None) -> list[tuple[float, float]]:
    """
    Generates a list of n random (x, y) points.

    NOTE: This is a placeholder since 'generate.py' was not provided.
    If you have your own 'generate.py' file, you can delete this
    function and uncomment the line below:
    # from generate import generate_random_points
    """
    if seed is not None:
        random.seed(seed)

    points = []
    # Generates points in a 1000x1000 square
    for _ in range(n):
        x = random.uniform(0, 1000)
        y = random.uniform(0, 1000)
        points.append((x, y))
    return points


# --- Main Test Runner ---

# List of N values from your table
n_values = [10, 100, 1000, 10000, 20000, 40000, 50000]

# Use a consistent seed for fair comparison (from your main.py example)
test_seed = 312
test_distribution = 'uniform'

# Print the table header
print("| N     | time (ms) |")
print("|-------|-----------|")

# Run the test for each N
for n in n_values:
    # 1. Generate the points
    # We must use the *same* seed each time to be fair,
    # but we generate the points *outside* the timer.
    points = generate_random_points(test_distribution, n, test_seed)

    # 2. Time the compute_hull_dvcq function
    start_time = time.time()

    # Make sure to re-sort the points just as your original code does,
    # as the algorithm expects sorted points.
    # Note: your 'compute_hull_dvcq' already does this, but if it
    # didn't, you would add: points.sort(key=lambda p: p[0])

    #hull_points = compute_hull_dvcq(points)
    hull_points = compute_hull_other(points)

    end_time = time.time()

    # 3. Calculate duration in milliseconds
    duration_ms = (end_time - start_time) * 1000

    # 4. Print the result in the table format
    # The formatting ensures the columns line up
    print(f"| {n:<5} | {duration_ms:>9.3f} |")