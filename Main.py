from graph import Graph
from graph_view import GraphView

class Main:
    @staticmethod
    def run():
        edges = [[1, 2], [1, 2], [2, 1], [3, 4], [4, 1], [5, 6], [6, ], [8]]
        
        graph = Graph(edges)
        
        components = graph.find_connected_components()
        num_components = len(components)
        is_eulerian = graph.is_eulerian()
        vertex_degrees = graph.get_vertex_degrees() 
        is_complete = graph.is_complete()

        view = GraphView(graph, num_components, is_eulerian, vertex_degrees, is_complete, components)
        view.plot_graph()


if __name__ == "__main__":
    Main.run()
