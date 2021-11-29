import numpy as np
import sys
import argparse
import random
import queue
import time


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


def path_scanning(graph: Graph, required_edges: list[Edge], depot: int, capacity: int, use_rule: int):
    cost = 0
    ans = "s 0,"
    current_position = depot
    left_capacity = capacity
    while len(required_edges) > 0:
        if use_rule == 7:
            next_edge, head, tail, moving_cost = edge_selection(required_edges, left_capacity, current_position,
                                                                random.randint(1, 6),
                                                                depot, left_capacity, capacity)
        else:
            next_edge, head, tail, moving_cost = edge_selection(required_edges, left_capacity, current_position,
                                                                use_rule,
                                                                depot, left_capacity, capacity)
        if next_edge is not None:
            required_edges.remove(next_edge)
            cost += moving_cost + next_edge.cost
            ans += generate_unit_ans_string(head.name, tail.name)
            current_position = tail.name
            left_capacity -= next_edge.demand
        else:
            ans += "0,0,"
            cost += graph.nodes[current_position].distance[depot]
            current_position = depot
            left_capacity = capacity
    ans += "0"
    cost += graph.nodes[current_position].distance[depot]
    return cost, ans
    # print(ans)
    # print("q " + str(cost))


def generate_unit_ans_string(head: int, tail: int) -> str:
    return "(%d,%d)," % (head, tail)


# return all edges which are closest to the current position
def edge_selection(required_edges: list[Edge], left_capacity: int, current_position: int, use_rule: int, depot: int,
                   current_capacity: int, capacity: int) -> (
        Edge, int, int, int):
    min_distance = 10000000000000
    ans = None
    head = None
    tail = None
    for edge in required_edges:
        if edge.demand > left_capacity:
            continue
        else:
            if edge.node1.distance[current_position] > edge.node2.distance[current_position]:
                current_head = edge.node2
                current_tail = edge.node1
                current_distance = edge.node2.distance[current_position]
            else:
                current_head = edge.node1
                current_tail = edge.node2
                current_distance = edge.node1.distance[current_position]
            if current_distance < min_distance:
                ans = edge
                head = current_head
                tail = current_tail
                min_distance = current_distance
            elif current_distance == min_distance:
                if use_rule == 1:
                    decision = rule1(head, current_head, depot)
                elif use_rule == 2:
                    decision = rule2(head, current_head, depot)
                elif use_rule == 3:
                    decision = rule3(ans, edge)
                elif use_rule == 4:
                    decision = rule4(ans, edge)
                elif use_rule == 5:
                    decision = rule5(head, current_head, depot, current_capacity, capacity)
                else:
                    decision = rule_random()
                if decision == 2:
                    ans = edge
                    head = current_head
                    tail = current_tail
                    min_distance = current_distance

    return ans, head, tail, min_distance


def rule1(node1: Node, node2: Node, depot: int) -> int:
    if node1.distance[depot] > node2.distance[depot]:
        return 1
    else:
        return 2


def rule2(node1: Node, node2: Node, depot: int) -> int:
    if node1.distance[depot] < node2.distance[depot]:
        return 1
    else:
        return 2


def rule3(edge1: Edge, edge2: Edge) -> int:
    if edge1.demand / edge1.cost > edge2.demand / edge2.cost:
        return 1
    else:
        return 2


def rule4(edge1: Edge, edge2: Edge) -> int:
    if edge1.demand / edge1.cost < edge2.demand / edge2.cost:
        return 1
    else:
        return 2


def rule5(node1: Node, node2: Node, depot: int, current_capacity: int, capacity: int) -> int:
    if current_capacity < 0.5 * capacity:
        return rule1(node1, node2, depot)
    else:
        return rule2(node1, node2, depot)


def rule_random() -> int:
    if random.randint(0, 99) > 66:
        return 1
    else:
        return 2


def main(argv):
    start_time = time.process_time()
    parse = argparse.ArgumentParser()
    parse.add_argument('file_path', metavar='CARP instance file', type=str, nargs='+')
    parse.add_argument('-t', metavar='termination', type=int, required=True)
    parse.add_argument('-s', metavar='random seed', required=True)
    args = parse.parse_args(argv)
    file_path = str(args.file_path)[2:-2]
    termination = args.t
    random_seed = args.s
    random.seed(random_seed)
    question = Question()
    # print(file_path, termination, random_seed)
    graph = Graph()
    required_edges = []
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
                required_edges.append(edge)
            node1.add_edge(edge)
            node2.add_edge(edge)
            # print(line)
    for node in graph.nodes:
        dijkstra(graph, node.name)
    # easiest_solution(graph, tmp_edges, question.depot)
    min = 1000000000000000000000
    ans = None
    max = 0
    ans = None
    i = 0
    while True:
        i += 1
        re = required_edges.copy()
        random.shuffle(re)
        current_cost, current_ans = path_scanning(graph, re, question.depot, question.capacity, i % 7 + 1)
        if current_cost > max:
            max = current_cost
        if current_cost < min:
            min = current_cost
            ans = current_ans
        if termination - time.process_time() + start_time < 2:
            break
    print(ans)
    print("q " + str(min))
    print(time.process_time() - start_time)
    # print('complete')


if __name__ == '__main__':
    main(sys.argv[1:])
