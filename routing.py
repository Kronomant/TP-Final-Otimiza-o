import igraph as graph
class Route:
    def __init__(self, routes=None, demands=0, cost=0):
        self.routes = routes if routes is not None else []
        self.demands = demands
        self.cost = cost

    def __str__(self):
        return f"{self.routes}, demanda: {self.demands}"
    
    def print_cost(self):
         return f"{self.routes}, custo: {self.cost}"
    
    

def get_gain(graph: graph.Graph, demands)-> list[Route]:
        cost = {}
        routes = []
        for v in graph.es:
            if v.source == 0:
                cost[v.target] = v["peso"]
            else:
                profit = cost[v.source] + cost[v.target] - v["peso"]
                route = Route([v.source, v.target], demands[v.source - 1] + demands[v.target - 1], profit)
                routes.append(route)
            
        return sorted(routes, key=lambda route: route.cost, reverse=True)


def solver(graph: graph.Graph, demands):
    routes = get_gain(graph, demands)    

    i = 0
    while i < len(routes):
        currentR = routes[i]
        j = 0
        while j < len(routes):
            targetR = routes[j]
            if(verify_fusion(currentR, targetR)):
                
                remove_member = common_member(currentR.routes, targetR.routes)
                total_demand = (currentR.demands + targetR.demands) - demands[remove_member - 1]

                if total_demand < 40:
                    fusion_route = Route(makes_fusion(currentR.routes, targetR.routes), total_demand)
                    routes.remove(targetR)
                    routes.remove(currentR)
                    currentR = fusion_route
                    routes.append(fusion_route)
            j+=1
        i+=1
    
    return routes
    
    
def verify_fusion(origin: Route, target: Route):
    if set(origin.routes) == set(target.routes):
        return False

    common_nodes = set([origin.routes[0], origin.routes[-1]])
    if any(node in common_nodes for node in target.routes):
        return True

    return False

def common_member(a, b):
    set_a = set(a)
    set_b = set(b)

    common_elements = set_a.intersection(set_b)

    if common_elements:
        return common_elements.pop()
    else:
        return 0

def makes_fusion(a, b):
    if a[0] == b[0]:
        solution = b + a[1:]
    elif a[0] == b[-1]:
        solution = b + a[1:]
    elif a[-1] == b[0]:
        solution = a + b[1:]
    else:
        solution = a + b[:-1][::-1]

    return list(set(solution))

def get_unique_routes(routes):
    sorted_routes = sorted(routes, key=lambda x: len(x.routes), reverse=True)

    unique_routes = []
    unique_routes.append(sorted_routes[0])
    
    i = 1
    for i in range(len(unique_routes)):
        rota_atual = unique_routes[i]

        for j in range(len(sorted_routes)):
            if i != j:
                outra_rota = sorted_routes[j]
                if set(rota_atual.routes).isdisjoint(outra_rota.routes):
                    unique_routes.append(sorted_routes[j])
                    break

    return unique_routes

def verify_routes(routes, n):
    c = sorted(routes, key=lambda x: len(x.routes), reverse=True)

    supplied = [False] * (n + 1)
    solution = []
    should_append = False

    for r in c:
        for x in r.routes:
            if not supplied[x]:
                supplied[x] = True
                should_append = True

        if should_append:
            solution.append(r)
        should_append = False

    return solution


def get_route_time(graph:graph.Graph, route: Route):

    total_time = 0
    routes = []
    routes.append(0)
    routes += route.routes
    routes.append(0)

    for i in range(len(routes) - 1):
        aresta_idx = graph.get_eid(routes[i], routes[i+1], error=False)
        if aresta_idx != -1:
            peso = graph.es[aresta_idx]["peso"]
            total_time+= peso * 3
    
    return total_time

def get_total_time(graph:graph.Graph, routes: list[Route], num_cars: int):

    routes_times = []
    print('Rotas e respectivas tempos')
    for route in routes:
       time = get_route_time(graph, route)
       print(f"Rota: {route} - tempo: {time}")
       routes_times.append(time)

    car_times = [sum(routes_times[i::num_cars]) for i in range(num_cars)]

    return car_times 
