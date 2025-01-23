from pyvis.network import Network
from collections import defaultdict

class Graph:
    def __init__(self, edges):
        self.edges = edges
        self.normalize_edges()
        print(self.edges)
        self.graph = defaultdict(list)
        
        
        # Para garantir que todos os nós sejam considerados, incluindo os isolados
        all_nodes = set()
        for edge in edges:
            if len(edge) == 2:
                u, v = edge
                self.graph[u].append(v)
                self.graph[v].append(u)
                all_nodes.add(u)
                all_nodes.add(v)
            elif len(edge) == 1:  # Caso de nó isolado
                u = edge[0]
                all_nodes.add(u)
        
        # Garantir que todos os nós isolados estejam no grafo
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

    def is_complete(self):
        # Verifica se todos os vértices estão conectados a todos os outros
        n = len(self.graph)
        for node in self.graph:
            if len(self.graph[node]) != n - 1:
                return False
        return True
    
    def plot_graph(self):
        net = Network(notebook=True)

        # Garantir que todos os nós principais sejam adicionados antes das arestas
        for node in self.graph:
            net.add_node(
                node,
                label=str(node),  # Adiciona o label no nó principal
                shape="circle",   # Garante o formato de círculo
                font={"size": 20, "color": "black"},  # Define o tamanho e cor do texto
                color="#97C2FC"   # Cor do nó
            )

        # Dicionário para contar arestas múltiplas
        edge_count = defaultdict(int)

        # Contando as arestas entre dois nós
        for edge in self.edges:
            if len(edge) == 2:
                u, v = edge
                # Normaliza a ordem das arestas para evitar duplicatas invertidas
                edge_count[(min(u, v), max(u, v))] += 1

        # Adicionando arestas reais (normais) e criando nós intermediários para arestas duplicadas
        for (u, v), count in edge_count.items():
            # Adiciona sempre a primeira aresta real
            net.add_edge(u, v)

            # Cria nós intermediários para cada aresta duplicada
            for i in range(1, count):
                intermediate_node = f"{u}-{v}-int-{i}"
                net.add_node(
                    intermediate_node,
                    size=5,  # Nó intermediário menor
                    color="#FFCC00"  # Cor diferente para os nós intermediários
                )
                net.add_edge(u, intermediate_node)
                net.add_edge(v, intermediate_node)

        # Gerando a visualização interativa
        net.show("grafo_interativo_completos.html")


# Exemplo de uso
edges = [[1, 2], [1, 2], [2, 1], [3, 4], [4, 1], [5, 6], [5, 6], [4, 8], [8,6], [6,1]]  # Incluindo as arestas múltiplas e o nó isolado [8]
graph = Graph(edges)

# Exibindo as respostas
components = graph.find_connected_components()
print(f"Quantidade de componentes conexos: {len(components)}")
print("Componentes conexos:", components)
print("O grafo é euleriano?", graph.is_eulerian())
graph.print_vertex_degrees()
print("O grafo é completo?", graph.is_complete())

# Plotando o grafo
graph.plot_graph()
