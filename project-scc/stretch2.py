import scc


def main():
    graph = {}
    max_to_node = -1
    max_edge = 10000

    with open("soc-Slashdot0902.txt", "r") as file:
        for line in file:
            if line.startswith("#"):
                continue

            from_node_str, to_node_str = line.strip().split()

            # Convert nodes to integers for comparison
            from_node = int(from_node_str)
            to_node = int(to_node_str)

            # Build the graph dictionary (using integer keys for consistency)
            if from_node not in graph:
                graph[from_node] = []
            graph[from_node].append(to_node)

            # Check if the current destination node is the largest seen yet
            if to_node > max_to_node:
                max_to_node = to_node
                max_edge = (from_node, to_node)

    print(f"Graph construction complete.")

    if max_edge:
        print(f"The maximum edge found is from node {max_edge[0]} to node {max_edge[1]}.")
    else:
        print("No edges found in the file.")

    # Your other analysis can continue from here
    # For example:
    strong_comp = scc.find_sccs(graph)
    print(f"Found {len(strong_comp)} strongly connected components.")


if __name__ == '__main__':
    main()
