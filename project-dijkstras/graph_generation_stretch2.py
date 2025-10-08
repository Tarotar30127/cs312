import networkx as nx
import random
import matplotlib.pyplot as plt


# This is a placeholder for your actual Dijkstra's implementation.
# The generator will call this function to find and highlight the path.
# Make sure your function returns the path as a list of nodes and the total cost.
def find_shortest_path(graph, source, target):
    """
    A placeholder for your Dijkstra's algorithm implementation.
    This example uses networkx's built-in function for demonstration.
    Replace this with a call to your own implementation.
    """
    try:
        # For demonstration, we use the networkx implementation.
        # In your project, you would call your own function, like:
        # path, cost = find_shortest_path_with_heap_pq(graph, source, target)
        cost, path = nx.single_source_dijkstra(graph, source, target, weight='weight')
        return path, cost
    except nx.NetworkXNoPath:
        return [], float('inf')


def generate_task_dag(num_nodes, edge_prob, max_weight=20):
    """
    Generates a random Directed Acyclic Graph (DAG) suitable for modeling task dependencies.

    Args:
        num_nodes (int): The number of tasks (nodes).
        edge_prob (float): The probability (0 to 1) of a dependency (edge)
                           existing between any two tasks.
        max_weight (int): The maximum duration (weight) for any task.

    Returns:
        networkx.DiGraph: The generated graph where node weights represent task durations.
    """
    G = nx.DiGraph()

    # Add nodes with a random 'weight' attribute representing task duration.
    for i in range(num_nodes):
        weight = random.randint(1, max_weight)
        G.add_node(i, weight=weight)

    # Add edges probabilistically, ensuring the graph remains acyclic.
    # By only allowing edges from a lower-index node to a higher-index node (i < j),
    # we guarantee no cycles can form.
    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            if random.random() < edge_prob:
                # In a routing problem, edge weights matter. In a task graph (like this),
                # node weights (task durations) are often more important. We will
                # assign a random weight to the edge for compatibility with Dijkstra's.
                edge_weight = random.randint(1, 10)
                G.add_edge(i, j, weight=edge_weight)

    return G


def run_and_visualize(graph_size_name, num_nodes, edge_prob):
    """
    Generates a graph, finds the shortest path, and saves a visualization.
    """
    print(f"--- Generating {graph_size_name} Graph ({num_nodes} nodes) ---")

    # 1. Generate the graph
    graph = generate_task_dag(num_nodes, edge_prob)

    # Define source and target nodes
    source_node = 0
    target_node = num_nodes - 1

    # 2. Run your shortest path algorithm on the generated graph
    path, cost = find_shortest_path(graph, source_node, target_node)

    print(f"Shortest path from {source_node} to {target_node}: {path}")
    print(f"Total path cost: {cost}")

    # 3. Visualize the graph and the path
    pos = nx.spring_layout(graph, seed=42)
    plt.figure(figsize=(12, 8))

    nx.draw(graph, pos, with_labels=True, node_size=1500, node_color='lightblue', font_size=10)

    edge_labels = nx.get_edge_attributes(graph, 'weight')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels)

    if path:
        path_edges = list(zip(path, path[1:]))
        nx.draw_networkx_nodes(graph, pos, nodelist=path, node_color='lightgreen', node_size=1500)
        nx.draw_networkx_edges(graph, pos, edgelist=path_edges, edge_color='red', width=2)

    plt.title(f"{graph_size_name} Graph ({num_nodes} nodes) - Path from {source_node} to {target_node}")

    # Save the figure to a file instead of displaying it
    file_name = f"{graph_size_name}_graph.png"
    plt.savefig(file_name)
    plt.close()  # Close the plot to free up memory

    print(f"💾 Figure saved as '{file_name}'\n")


# --- Main execution block for Stretch 2 ---
if __name__ == "__main__":
    # Run the generation and pathfinding for three different graph sizes
    run_and_visualize(graph_size_name="Small", num_nodes=8, edge_prob=0.5)
    run_and_visualize(graph_size_name="Medium", num_nodes=20, edge_prob=0.3)
    run_and_visualize(graph_size_name="Large", num_nodes=50, edge_prob=0.15)