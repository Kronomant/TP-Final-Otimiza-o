import igraph as graph
class Route:
    def __init__(self, routes=None, demands=0, time=0, cost=0):
        self.routes = routes if routes is not None else []
        self.demands = demands
        self.cost = cost
        self.time = time

    def __str__(self):
        return f"{self.routes}, demanda: {self.demands}, tempo: {self.time}"
    
    def print_cost(self):
         return f"{self.routes}, custo: {self.cost}"
    
    

def get_gain(graph: graph.Graph, demands, times)-> list[Route]:
        cost = {}
        routes = []
        for v in graph.es:
            if v.source == 0:
                cost[v.target] = v["peso"]
            else:
                profit = cost[v.source] + cost[v.target] - v["peso"]
                route = Route([v.source, v.target], demands[v.source - 1] + demands[v.target - 1], times[v.source - 1] + times[v.target - 1], profit)
                routes.append(route)
            
        return sorted(routes, key=lambda route: route.cost, reverse=True)


def solver(graph: graph.Graph, demands, times, limit_demand, limit_time):
    routes = get_gain(graph, demands, times)

    i = 0
    while i < len(routes):
        currentR = routes[i]
        j = i + 1

        while j < len(routes):
            targetR = routes[j] 
            remove_members = common_member(currentR.routes, targetR.routes)

            if not set(targetR.routes).issubset(currentR.routes):
                total_demand = (currentR.demands + targetR.demands)
                total_time = (currentR.time + targetR.time)

                for member in remove_members:
                    targetR.routes.remove(member)
                    targetR.demands -= demands[member - 1]
                    targetR.time -= times[member - 1]
                    total_demand -= demands[member - 1]
                    total_time -= times[member - 1]

                if total_demand <= limit_demand and total_time <= limit_time:
                    fusion_route = Route(makes_fusion(currentR.routes, targetR.routes), total_demand, total_time)
                    routes.remove(targetR)
                    routes[i] = fusion_route
                    currentR = fusion_route
                else:
                    j += 1
            elif set(targetR.routes) <= set(currentR.routes) and targetR.routes != currentR.routes:
                routes.remove(targetR)
            else:
                j += 1

        i += 1

    return routes
    
    


def common_member(a, b):
    set_a = set(a)
    set_b = set(b)

    common_elements = set_a.intersection(set_b)
    
    if common_elements:
        return common_elements
    else:
        return []

def makes_fusion(a, b):
    set_a = set(a)
    set_b = set(b)

    #list -> set
    #set -> list

    common_elements = set_a.intersection(set_b)
    #print('COMMON ELEMENTS', common_elements)

    for element in common_elements:
        set_b.remove(element)

    list_b = list(set_b)
    #print('LIST B', list_b)

    
    solution = list_b + a
    # verifica se tem ligação
   

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

def read_file_txt(file):
    demands = []
    times = []
    edge_weights = []
    try:
        with open(file, 'r') as arquivo:
            linha = arquivo.readline().split()
            limit_demand = float(linha[0])
            limit_time = float(linha[1])

            linha = arquivo.readline().split()

            for linha in arquivo:
                if linha.strip() == "":
                    break
                dados = linha.split()
                demands.append(float(dados[0]))
                times.append(float(dados[1]))

            for linha in arquivo:
                if linha.strip() == "":
                    break
                
                pesos = linha.split()
                edge_weights.extend([int(pesos[0]), int(pesos[1]), float(pesos[2])])

    except FileNotFoundError:
        print(f"Arquivo {file} não encontrado.")
        return None, None, None, None

    return limit_demand, limit_time, demands, times, edge_weights
