from scc import find_sccs


def load_graph(file_path: str, max_edges: int = None) -> dict[str, list[str]]:
    graph = {}
    edge_count = 0
    with open(file_path, "r") as f:
        for line in f:
            if line.startswith("#"):
                continue
            parts = line.strip().split()
            if len(parts) != 2:
                continue
            u, v = parts
            if u not in graph:
                graph[u] = []
            graph[u].append(v)
            if v not in graph:
                graph[v] = []
            edge_count += 1
            if max_edges and edge_count >= max_edges:
                break
    return graph


graph = load_graph("soc-Slashdot0902.txt", max_edges=10000)

sccs = find_sccs(graph)

print(f"Number of SCCs: {len(sccs)}")
sizes = [len(scc) for scc in sccs]
print(f"Largest SCC size: {max(sizes)}")
print(f"Average SCC size: {sum(sizes) / len(sccs):.2f}")