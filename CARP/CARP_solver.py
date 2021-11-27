import numpy as np
import sys
import argparse
import random
import queue


class Question:
    def __init__(self, name='', vertices=0, depot=0, required_edges=0, non_required_edges=0, vehicles=0, capacity=0,
                 total_cost=0):
        self.name = name
        self.vertices = vertices
        self.depot = depot
        self.required_edges = required_edges
        self.non_required_edges = non_required_edges
        self.vehicles = vehicles
        self.capacity = capacity
        self.total_cost = total_cost


class Node:
    def __init__(self, name: int):
        self.name = name
        self.edges = []
        self.is_visited = False
        self.distance = {}

    def add_edge(self, edge):
        self.edges.append(edge)

    def set_visited(self):
        self.is_visited = True

    def unset_visited(self):
        self.is_visited = False

    def initial_distance(self, n):
        for i in range(n):
            self.distance[i] = 100000000000000
        self.distance[self.name] = 0


class Edge:
    def __init__(self, node1: Node, node2: Node, cost: int, demand: int):
        self.node1 = node1
        self.node2 = node2
        self.cost = cost
        self.demand = demand


class Graph:
    def __init__(self):
        self.nodes = []

    def add_node(self, node):
        self.nodes.append(node)


def dijkstra(graph: Graph, s: int):
    source = graph.nodes[s]
    source.set_visited()
    heap = queue.PriorityQueue()
    heap.put((0, source.name))
    while not heap.empty():
        (current_distance, current_node) = heap.get()
        for edge in graph.nodes[current_node].edges:
            if edge.node1.name == graph.nodes[current_node].name:
                neighbour = edge.node2
            else:
                neighbour = edge.node1
            if not neighbour.is_visited:
                neighbour.set_visited()
                source.distance[neighbour.name] = current_distance + edge.cost
                heap.put((current_distance + edge.cost, neighbour.name))
            else:
                if source.distance[neighbour.name] > current_distance + edge.cost:
                    source.distance[neighbour.name] = current_distance + edge.cost
                    heap.put((current_distance + edge.cost, neighbour.name))
    for node in graph.nodes:
        node.unset_visited()


def easiest_solution(graph: Graph, required_edges: list[Edge], depot: int):
    cost = 0
    ans = "s "
    for edge in required_edges:
        cost += graph.nodes[depot].distance[edge.node1.name] + edge.cost + edge.node2.distance[depot]
        ans += "0,(%d,%d),0," % (edge.node1.name, edge.node2.name)
    print(ans[:-1])
    print("q " + str(cost))


def main(argv):
    parse = argparse.ArgumentParser()
    parse.add_argument('file_path', metavar='CARP instance file', type=str, nargs='+')
    parse.add_argument('-t', metavar='termination', type=int, required=True)
    parse.add_argument('-s', metavar='random seed', required=True)
    args = parse.parse_args(argv)
    file_path = str(args.file_path)[2:-2]
    termination = args.t
    random_seed = args.s
    question = Question()
    # print(file_path, termination, random_seed)
    graph = Graph()
    tmp_edges = []
    with open(file_path, 'r') as input_file:
        line = input_file.readline()
        question.name = line[line.find(':') + 1:].strip()
        line = input_file.readline()
        question.vertices = int(line[line.find(':') + 1:].strip())
        line = input_file.readline()
        question.depot = int(line[line.find(':') + 1:].strip())
        line = input_file.readline()
        question.required_edges = int(line[line.find(':') + 1:].strip())
        line = input_file.readline()
        question.non_required_edges = int(line[line.find(':') + 1:].strip())
        line = input_file.readline()
        question.vehicles = int(line[line.find(':') + 1:].strip())
        line = input_file.readline()
        question.capacity = int(line[line.find(':') + 1:].strip())
        line = input_file.readline()
        question.total_cost = int(line[line.find(':') + 1:].strip())
        line = input_file.readline()
        for i in range(question.vertices + 1):
            node = Node(i)
            node.initial_distance(question.vertices + 1)
            graph.add_node(node)
        for i in range(question.required_edges + question.non_required_edges):
            line = input_file.readline().split()
            # print(line)
            node1 = graph.nodes[int(line[0])]
            node2 = graph.nodes[int(line[1])]
            edge = Edge(node1, node2, int(line[2]), int(line[3]))
            if edge.demand != 0:
                tmp_edges.append(edge)
            node1.add_edge(edge)
            node2.add_edge(edge)
            # print(line)
    for node in graph.nodes:
        dijkstra(graph, node.name)
    easiest_solution(graph,tmp_edges,question.depot)
    # print('complete')


if __name__ == '__main__':
    main(sys.argv[1:])
