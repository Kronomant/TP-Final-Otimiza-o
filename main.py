"""
Integrantes:

@Alice Cabral
@Lucas Milard de Souza Freitas
@Rossana de Oliveira Souza

"""

import igraph as graph
import routing


def print_routes(routes):
    for r in routes:
        print(r)

num_nodes = 10
edge_pairs = [(i, j) for i in range(num_nodes) for j in range(i + 1, num_nodes)]
g = graph.Graph(num_nodes, edge_pairs)

edge_weights = [
        12, 11, 7, 10, 10, 9, 8, 6, 12,
        8, 5, 9, 12, 14, 16, 17, 22,
        9, 15, 17, 8, 18, 14, 22,
        7, 9, 11, 12, 12, 17,
        3, 17, 7, 15, 18,
        18, 6, 15, 15,
        16, 8, 16,
        11, 11,
        10
    ]
g.es['peso'] = edge_weights



demands = [10, 15, 18, 17, 3, 5, 2, 4, 6]
time    = [14, 21, 16, 44, 23, 10, 34, 20, 18]


all_routes = routing.solver(g, demands, times=time)
print(f"Todas as Rotas: {len(all_routes)}")
print_routes(all_routes)

unique_routes = routing.get_unique_routes(all_routes)
#print(f"\nRotas unicas: {len(unique_routes)}")
#print_routes(unique_routes)

routes = routing.verify_routes(all_routes, len(demands))
#print(f"\nRotas necessárias: {len(routes)}")
#print_routes(routes)





