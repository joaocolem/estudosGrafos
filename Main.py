from graph import Graph
from graph_view import GraphView
from itertools import permutations  # Necessário para a função de isomorfismo

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

class Main:
 @staticmethod
 def run():
     # Grafo principal
     edges = [[1, 2], [1, 2], [2, 1], [3, 4], [4, 1], [5, 6]]
     graph = Graph(edges)

     # Calcula as propriedades do grafo
     components = graph.find_connected_components()
     num_components = len(components)
     is_eulerian = graph.is_eulerian()
     vertex_degrees = graph.get_vertex_degrees()
     is_complete = graph.is_complete()
     has_cycle = graph.has_cycle()
     is_bipartite = graph.is_bipartite()
     has_closed_path = graph.has_closed_path()

     # Cria um segundo grafo para verificar isomorfismo
     edges_b = [[7, 8], [8, 9], [9, 7], [10, 11]]  # Exemplo de outro grafo
     graph_b = Graph(edges_b)

     # Verifica se os grafos são isomorfos
     is_isomorphic = are_isomorphic(graph, graph_b)

     # Imprime informações sobre os grafos
     print("\nVerificação de Isomorfismo:")
     print(f"Os grafos principal e B são isomorfos? {'Sim' if is_isomorphic else 'Não'}")

     # Cria a visualização do grafo
     view = GraphView(
         graph,
         num_components,
         is_eulerian,
         vertex_degrees,
         is_complete,
         has_cycle,
         is_bipartite,
         has_closed_path,
         components,
     )

     # Plota o grafo interativo
     view.plot_graph()

if __name__ == "__main__":
 Main.run()