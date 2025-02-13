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

    def has_closed_path(self):
        """
        Verifica se o grafo possui um caminho fechado (ciclo simples).
        """
        visited = set()

        def dfs(node, parent):
            visited.add(node)
            for neighbor in self.graph[node]:
                if neighbor not in visited:
                    if dfs(neighbor, node):
                        return True
                elif neighbor != parent:
                    return True
            return False

        for node in self.graph:
            if node not in visited:
                if dfs(node, None):
                    return True
        return False

    def are_isomorphic(graph_a, graph_b):
        """
        Verifica se dois grafos são isomorfos.
        
        :param graph_a: Instância da classe Graph representando o primeiro grafo.
        :param graph_b: Instância da classe Graph representando o segundo grafo.
        :return: True se os grafos forem isomorfos, False caso contrário.
        """
        # Verifica se os números de vértices e arestas são iguais
        if len(graph_a.graph) != len(graph_b.graph) or len(graph_a.edges) != len(graph_b.edges):
            return False

        # Obtém os graus dos vértices de ambos os grafos
        degrees_a = sorted([len(neighbors) for neighbors in graph_a.graph.values()])
        degrees_b = sorted([len(neighbors) for neighbors in graph_b.graph.values()])

        # Se os graus não forem iguais, os grafos não são isomorfos
        if degrees_a != degrees_b:
            return False

        # Para casos mais complexos, podemos usar permutações dos vértices
        # Aqui usamos uma abordagem simplificada
        def adjacency_list(graph):
            return {node: sorted(list(neighbors)) for node, neighbors in graph.graph.items()}

        adj_a = adjacency_list(graph_a)
        adj_b = adjacency_list(graph_b)

        # Tenta mapear os nós de A para os nós de B
        for permutation in permutations(adj_b.keys()):
            mapping = dict(zip(adj_a.keys(), permutation))
            if all(
                sorted([mapping[neighbor] for neighbor in adj_a[node]]) == sorted(adj_b[mapping[node]])
                for node in adj_a
            ):
                return True

        return False