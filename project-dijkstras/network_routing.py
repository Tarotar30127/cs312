class HeapPriorityQueue:
    def __init__(self):
        self.map_of_distance = {}
        self.position = {}
        self.nodes = []

    def insert(self, node, distance_to_target):
        self.nodes.append(node)
        self.position[node] = (len(self.nodes)-1)
        self.map_of_distance[node] = distance_to_target

    def delete_min(self):
        if not self.nodes:
            return None
        min_node = self.nodes[0]
        last_node = self.nodes.pop()
        if not self.nodes:
            self.position.pop(min_node)
            self.map_of_distance.pop(min_node)
            return min_node
        self.nodes[0] = last_node
        self.position[last_node] = 0
        self.shift_down(0)
        self.position.pop(min_node)
        self.map_of_distance.pop(min_node)

    def decrease_key(self, node, new_distance):
        self.map_of_distance[node] = new_distance
        position_of_node = self.position[node]
        HeapPriorityQueue.bubble_up(self, position_of_node)

    def bubble_up(self, index):
        parent_index = (index - 1) // 2
        while index > 0 and self.map_of_distance[self.nodes[index]] < self.map_of_distance[self.nodes[parent_index]]:
            child_node = self.nodes[index]
            parent_node = self.nodes[parent_index]
            self.nodes[index], self.nodes[parent_index] = parent_node, child_node
            self.position[child_node] = parent_index
            self.position[parent_node] = index
            index = parent_index
            parent_index = (index - 1) // 2

    def shift_down(self, index):
        heap_size = len(self.nodes)
        while (2 * index + 1) < heap_size:
            left_child_index = 2 * index + 1
            right_child_index = 2 * index + 2
            smallest_child_index = left_child_index
            if (right_child_index < heap_size and
                    self.map_of_distance[self.nodes[right_child_index]] < self.map_of_distance[
                        self.nodes[left_child_index]]):
                smallest_child_index = right_child_index

            if self.map_of_distance[self.nodes[index]] <= self.map_of_distance[self.nodes[smallest_child_index]]:
                break
            parent_node = self.nodes[index]
            child_node = self.nodes[smallest_child_index]
            self.nodes[index], self.nodes[smallest_child_index] = child_node, parent_node
            self.position[parent_node] = smallest_child_index
            self.position[child_node] = index

            index = smallest_child_index


def find_shortest_path_with_heap(
        graph: dict[int, dict[int, float]],
        source: int,
        target: int
) -> tuple[list[int], float]:
    """
    Find the shortest (least-cost) path from `source` to `target` in `graph`
    using the heap-based algorithm.

    Return:
        - the list of nodes (including `source` and `target`)
        - the cost of the path
    """



def find_shortest_path_with_linear_pq(
        graph: dict[int, dict[int, float]],
        source: int,
        target: int
) -> tuple[list[int], float]:
    """
    Find the shortest (least-cost) path from `source` to `target` in `graph`
    using the array-based (linear lookup) algorithm.

    Return:
        - the list of nodes (including `source` and `target`)
        - the cost of the path
    """
    distance = {}
    previous = {}
    priority_queue = {}
    for node in graph:
        if node == source:
            distance[node] = 0
            priority_queue[node] = 0
        else:
            distance[node] = float('inf')
            priority_queue[node] = float('inf')
        previous[node] = None

    while priority_queue:
        current_node = min(priority_queue, key=lambda n: distance[n])
        priority_queue.pop(current_node)
        if current_node == target:
            break
        for neighbor, weight in graph.get(current_node, {}).items():
            new_distance = distance[current_node] + weight
            if new_distance < distance[neighbor]:
                distance[neighbor] = float(new_distance)
                previous[neighbor] = float(current_node)
    if distance[target] == float('inf'):
        return [], float('inf')
    path = []
    current = target
    while current is not None:
        path.insert(0, current)
        current = previous[current]
    return path, distance[target]
