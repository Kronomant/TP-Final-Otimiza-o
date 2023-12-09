"""
Integrantes:

@Alice Cabral
@Isabela Regina Aguilar
@Lucas Milard de Souza Freitas
@Rossana de Oliveira Souza

"""

import igraph as graph
import routing


def print_routes(routes):
    for r in routes:
        print(r)

num_nodes = 30
edge_pairs = [(i, j) for i in range(num_nodes) for j in range(i + 1, num_nodes)]
g = graph.Graph(num_nodes, edge_pairs)

limit_demand, limit_time, demands, times, edge_weights = routing.read_file_txt("entrada.txt")

g.es['peso'] = edge_weights

all_routes = routing.solver(g, demands, times, limit_demand, limit_time)
print(f"Todas as Rotas: {len(all_routes)}")
print_routes(all_routes)

unique_routes = routing.get_unique_routes(all_routes)
print(f"\nRotas unicas: {len(unique_routes)}")
print_routes(unique_routes)

routes = routing.verify_routes(all_routes, len(demands))
#print(f"\nRotas necessárias: {len(routes)}")
#print_routes(routes)





