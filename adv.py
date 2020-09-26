from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)


class Queue():
    def __init__(self):
        self.queue = []

    def enqueue(self, value):
        self.queue.append(value)

    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None

    def size(self):
        return len(self.queue)


class Stack():
    def __init__(self):
        self.stack = []

    def push(self, value):
        self.stack.append(value)

    def pop(self):
        if self.size() > 0:
            return self.stack.pop()
        else:
            return None

    def size(self):
        return len(self.stack)


# Print an ASCII map
# world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []


# grab total rooms from world.rooms
total_rooms = len(world.rooms)


# BFS returning shortest path to specified node
def bfs(starting_vertex, destination_vertex, get_neighbors):

    starting_path = [starting_vertex]
    q = [starting_path]
    visited = set()

    while len(q) > 0:

        curr_path = q.pop(0)
        curr_vertex = curr_path[-1]

        if curr_vertex not in visited:

            if curr_vertex == destination_vertex:
                return curr_path

            visited.add(curr_vertex)

            for neigh in get_neighbors(curr_vertex):
                q.append(curr_path + [neigh])


# dft to traverse to every node

def dft(starting_room, get_neighbors):

    traversal = []
    start = [starting_room]
    visited = set()

    while len(start) > 0:
        curr = start.pop()
        if curr not in visited:

            traversal.append(curr)
            visited.add(curr)

            for neighbor in get_neighbors(curr):
                start.append(neighbor)
    return traversal


# get neighbors function based on graph which will be slowly built up
graph = {}


def get_neighbors(current):
    neighbors = list(graph[current].values())
    return neighbors


def get_direction(current, next_room):

    for key, value in graph[current].items():

        if value == next_room:

            return key


def get_directions(id_list):
    directions = []

    for i in range(0, len(id_list) - 1):

        directions.append(get_direction(id_list[i], id_list[i + 1]))

    return directions


def opposite(d):
    if d == 'n':
        return 's'
    if d == 's':
        return 'n'
    if d == 'w':
        return 'e'
    if d == 'e':
        return 'w'

# Steps to build up a graph:


explored = set()
graph[player.current_room.id] = {}

for direction in player.current_room.get_exits():

    graph[player.current_room.id][direction] = '?'

while len(explored) < len(room_graph):

    previous = player.current_room.id
    direction = random.choice(player.current_room.get_exits())
    player.travel(direction)
    graph[previous][direction] = player.current_room.id

    if player.current_room.id not in graph:

        graph[player.current_room.id] = {}

        for direction in player.current_room.get_exits():

            graph[player.current_room.id][direction] = '?'
    graph[player.current_room.id][opposite(direction)] = previous

    if '?' not in get_neighbors(player.current_room.id):
        explored.add(player.current_room.id)

# create the traversal using BFT

traversal = dft(world.starting_room.id, get_neighbors)

# loop through the array traversal and fill in gap segments with find shortest path BFS

traversal_no_gaps = []


for i in range(len(traversal) - 1):

    traversal_no_gaps.append(traversal[i])

    if traversal[i + 1] not in get_neighbors(traversal[i]):

        gap = bfs(traversal[i], traversal[i + 1], get_neighbors)[1:-1]
        traversal_no_gaps = traversal_no_gaps + gap

traversal_no_gaps.append(traversal[-1])

# convert final traversal array into cardinal directions

# # Fill this out with directions to walk

traversal_path = get_directions(traversal_no_gaps)


# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")


#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
