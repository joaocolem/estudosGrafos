from pyvis.network import Network
from collections import defaultdict
import random
import webbrowser

class GraphView:
    def __init__(self, graph, num_components, is_eulerian, vertex_degrees, is_complete, components):
        self.graph = graph
        self.num_components = num_components
        self.is_eulerian = is_eulerian
        self.vertex_degrees = vertex_degrees
        self.is_complete = is_complete
        self.components = components  

    def plot_graph(self):
        net = Network(notebook=True)

        colors = self.generate_colors(len(self.components))

        node_to_component = {}
        for i, component in enumerate(self.components):
            for node in component:
                node_to_component[node] = i  

        for node in self.graph.graph:
            component_id = node_to_component.get(node, -1)
            net.add_node(
                node,
                label=str(node),
                shape="circle",
                font={"size": 20, "color": "black"},
                color=colors[component_id] if component_id >= 0 else "#97C2FC"  
            )

        edge_count = defaultdict(int)

        for edge in self.graph.edges:
            if len(edge) == 2:
                u, v = edge
                edge_count[(min(u, v), max(u, v))] += 1

        for (u, v), count in edge_count.items():
            net.add_edge(u, v)

            for i in range(1, count):
                intermediate_node = f"{u}-{v}-int-{i}"
                net.add_node(
                    intermediate_node,
                    size=0,
                    color="#FFCC00",
                    label=""  
                )
                net.add_edge(u, intermediate_node)
                net.add_edge(v, intermediate_node)

        net.show("grafo_interativo_completos.html")

        with open("grafo_interativo_completos.html", "a", encoding="utf-8") as f:
            f.write(f"""
            <meta charset="UTF-8">
            <style>
                /* Estilo para as informações no canto superior esquerdo */
                #info-container {{
                    position: absolute;
                    top: 10px;
                    left: 10px;
                    background-color: rgba(255, 255, 255, 0.8);
                    padding: 10px;
                    border-radius: 5px;
                    font-family: Arial, sans-serif;
                    color: #333;
                    font-size: 14px;
                }}
            </style>
            <div id="info-container">
                <p><strong>Quantidade de componentes conexos:</strong> {self.num_components}</p>
                <p><strong>O grafo é euleriano?</strong> {self.is_eulerian}</p>
                <p><strong>O grafo é completo?</strong> {self.is_complete}</p>
                <p><strong>Graus dos vértices:</strong></p>
                <ul>
                    {''.join([f'<li>Vértice {node}: {degree} conexões</li>' for node, degree in self.vertex_degrees.items()])}
                </ul>
            </div>
            <script type="text/javascript">
                var network = new vis.Network(container, data, options);

                // Adicionando evento de clique no nó
                network.on("click", function(params) {{
                    if (params.nodes.length > 0) {{
                        var nodeId = params.nodes[0];  // ID do nó clicado
                        console.log("Nó clicado: " + nodeId);
                    }}
                }});
            </script>
            """)

        # Abre automaticamente o HTML gerado
        webbrowser.open("grafo_interativo_completos.html")

    def generate_colors(self, num_components):
        """
        Gera uma lista de cores distintas para os componentes.
        :param num_components: O número de componentes para os quais queremos gerar cores.
        :return: Lista de cores.
        """
        colors = []
        for _ in range(num_components):
            color = "#{:02x}{:02x}{:02x}".format(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            colors.append(color)
        return colors
