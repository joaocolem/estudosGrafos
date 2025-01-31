from collections import defaultdict, deque

class Graph:
    def __init__(self, edges):
        self.graph = defaultdict(set)
        self.edges = []
        if self._is_valid_graph(edges):
            self._build_graph(edges)
        else:
            raise ValueError("Invalid graph: edges must be pairs of vertices.")

    def _is_valid_graph(self, edges):
        return all(isinstance(edge, list) and len(edge) == 2 for edge in edges)

    def _build_graph(self, edges):
        for u, v in edges:
            self.graph[u].add(v)
            self.graph[v].add(u)
            self.edges.append((u, v))

    def _dfs(self, node, visited, parent=None):
        visited.add(node)
        for neighbor in self.graph[node]:
            if neighbor not in visited:
                if self._dfs(neighbor, visited, node):
                    return True
            elif neighbor != parent:
                return True
        return False

    def find_connected_components(self):
        visited = set()
        components = []
        for node in self.graph:
            if node not in visited:
                component = []
                self._dfs_collect(node, visited, component)
                components.append(component)
        return components

    def _dfs_collect(self, node, visited, component):
        visited.add(node)
        component.append(node)
        for neighbor in self.graph[node]:
            if neighbor not in visited:
                self._dfs_collect(neighbor, visited, component)

    def is_complete(self):
        n = len(self.graph)
        for node in self.graph:
            if len(self.graph[node]) != n - 1:
                return False
        return True

    def has_cycle(self):
        visited = set()
        for node in self.graph:
            if node not in visited:
                if self._dfs(node, visited):
                    return True
        return False

    def is_bipartite(self):
        color = {}
        def bfs(start):
            queue = deque([start])
            color[start] = 0
            while queue:
                node = queue.popleft()
                for neighbor in self.graph[node]:
                    if neighbor not in color:
                        color[neighbor] = 1 - color[node]
                        queue.append(neighbor)
                    elif color[neighbor] == color[node]:
                        return False
            return True
        
        for node in self.graph:
            if node not in color:
                if not bfs(node):
                    return False
        return True

    def get_vertex_degrees(self):
        return {node: len(neighbors) for node, neighbors in self.graph.items()}

    def is_eulerian(self):
        degrees = self.get_vertex_degrees()
        odd_count = sum(1 for degree in degrees.values() if degree % 2 != 0)
        return odd_count == 0
