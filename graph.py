from collections import defaultdict, deque

class Graph:
    def __init__(self, edges):
        if not self.is_valid_graph(edges):
            raise ValueError("A entrada fornecida não representa um grafo válido.")

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

    @staticmethod
    def is_valid_graph(edges):
        """Valida se a entrada representa um grafo genérico usando o Teorema de Handshaking."""
        if len(edges) == 0:
            return False
        
        vertex_degrees = defaultdict(int)
        num_edges = 0

        for edge in edges:
            if len(edge) == 2:
                u, v = edge
                vertex_degrees[u] += 1
                vertex_degrees[v] += 1
                num_edges += 1
            elif len(edge) == 1:
                u = edge[0]
                vertex_degrees[u] += 0
            else:
                return False

        total_degrees = sum(vertex_degrees.values())
        if total_degrees != 2 * num_edges:
            return False  

        return True


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
        vertex_degrees = {}  
        for node in self.graph:
            degree = len(self.graph[node])
            vertex_degrees[node] = degree  
        return vertex_degrees  

    def is_complete(self):
        n = len(self.graph)
        for node in self.graph:
            if len(self.graph[node]) != n - 1:
                return False
        return True

    def has_cycle(self):
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
        
        
    def bfs_check_bipartite(self, start):
        """Verifica se o grafo é bipartido usando BFS a partir de um vértice inicial."""
        color = {}
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

    def is_bipartite(self):
        """Verifica se o grafo é bipartido percorrendo todas as componentes conexas."""
        color = {}
        for node in self.graph:
            if node not in color:
                if not self.bfs_check_bipartite(node):
                    return False
        return True