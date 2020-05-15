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
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []


# Need to reverse incase we get stuck
reverse_direction = {'n': 's','s': 'n','w': 'e', 'e': 'w'}

# Go thru current room exits
# travel to exit

# If already travelled there, move back
# If not visited, mark as visited, add to set, add new direction to visit
# Add reverse steps to keep track of directions

def explore(starting_room, visited=set()):

    make_new_path = []

    for direction in player.current_room.get_exits():
        player.travel(direction)

        # Room already visited, reverse direction and move back
        if player.current_room.id in visited:
            player.travel(reverse_direction[direction])
            
        else:
            # Not been here before, add room, mark as visited
            # Move direction
            visited.add(player.current_room.id)
            make_new_path.append(direction)
            
            make_new_path = make_new_path + explore(player.current_room.id, visited)
            player.travel(reverse_direction[direction])
            make_new_path.append(reverse_direction[direction])

    return make_new_path

# no longer empty arr, passes in id to call func
traversal_path = explore(player.current_room.id)



# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
        
