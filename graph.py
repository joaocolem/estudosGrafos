from collections import defaultdict

class Graph:
    def __init__(self, edges):
        self.edges = edges
        self.normalize_edges()
        self.graph = defaultdict(list)

        all_nodes = set()
        for edge in edges:
            if len(edge) == 2:
                u, v = edge
                self.graph[u].append(v)
                self.graph[v].append(u)
                all_nodes.add(u)
                all_nodes.add(v)
            elif len(edge) == 1: 
                u = edge[0]
                all_nodes.add(u)

        for node in all_nodes:
            if node not in self.graph:
                self.graph[node] = []

    def normalize_edges(self):
        """Ordena os vértices de cada aresta para garantir consistência."""
        self.edges = [sorted(edge) for edge in self.edges if len(edge) == 2]

    def dfs(self, node, visited, component):
        stack = [node]
        while stack:
            current = stack.pop()
            if current not in visited:
                visited.add(current)
                component.add(current)
                for neighbor in self.graph[current]:
                    if neighbor not in visited:
                        stack.append(neighbor)

    def find_connected_components(self):
        visited = set()
        components = []

        for node in self.graph:
            if node not in visited:
                component = set()
                self.dfs(node, visited, component)
                components.append(component)

        return components

    def is_eulerian(self):
        components = self.find_connected_components()
        non_isolated_components = [comp for comp in components if len(comp) > 1]

        if len(non_isolated_components) != 1:
            return False

        for node in self.graph:
            if len(self.graph[node]) % 2 != 0:
                return False

        return True

    def print_vertex_degrees(self):
        for node in self.graph:
            degree = len(self.graph[node])
            print(f"Vértice {node} tem {degree} conexão(ões).")
            
    def get_vertex_degrees(self):
        vertex_degrees = {}  # Dicionário para armazenar os graus dos vértices
        for node in self.graph:
            degree = len(self.graph[node])
            vertex_degrees[node] = degree  # Armazenando o grau do vértice
        return vertex_degrees  # Retorna o dicionário com os graus


    def is_complete(self):
        n = len(self.graph)
        for node in self.graph:
            if len(self.graph[node]) != n - 1:
                return False
        return True