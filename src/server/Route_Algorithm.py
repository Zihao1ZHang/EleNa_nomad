from utils import *
from model.GeoDataModel import GeoData
from model.keys import google_elevation_api_key
from algorithm.Genetic_algorithm import GeneticAlgorithm
from algorithm.Astar_algorithm import Astar
from algorithm.Dijkstra_algorithm import Dijkstra
from algorithm.Shortest_algorithm import Shortest


def find_route(source, dest, method, percentage=1, is_max=1):
    # Initialize Geo map
    G = GeoData(source, dest, google_elevation_api_key)

    # run routing algorithm
    shortest = Shortest(G)
    shortest_route = shortest.search()
    if method == 'S':
        return shortest_route

    genetic = GeneticAlgorithm(G, shortest_route.length * percentage, is_max)
    astar = Astar(G, shortest_route.length * percentage, is_max)
    dijkstra = Dijkstra(G, shortest_route.length * percentage, is_max)

    astar_route = astar.search()
    dijkstra_route = dijkstra.search(elevation_factor=10, cur_iteration=100)
    genetic_route = genetic.cal_result()

    print("Shortest Route elevation gain: " + str(shortest_route.elevation))
    print("Maxium length allowed: " + str(shortest_route.length * percentage))
    if astar_route:
        print("Astar Route elevation gain: " + str(astar_route.elevation))
        print("Astar Route length: " + str(astar_route.length))
    else:
        print("Fail to find route using astar")

    print("Dijkstra Route length: " + str(dijkstra_route.length))
    print("Genetic Route length: " + str(genetic_route.length))
    print("Dijkstra Route elevation gain: " + str(dijkstra_route.elevation))
    print("Genetic Route elevation gain: " + str(genetic_route.elevation))

    # find the route satisified the requirement
    routes = [shortest_route, astar_route, dijkstra_route, genetic_route]
    final_route = get_result(is_max, routes)

    return final_route


if __name__ == "__main__":
    source = [-72.50962524612441, 42.375880221431004]
    dest = [-72.49934702117964, 42.370442879663926]

    route1 = find_route(source, dest, method='A', percentage=1.5, is_max=1)
