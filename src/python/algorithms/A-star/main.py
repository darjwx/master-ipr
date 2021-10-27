#! /usr/bin/env python

## Map level
### * 0: free
### * 1: ocupado (muro/obstáculo)
### * 2: visited
### * 3: start
### * 4: goal
### * 5: path

## Graph level
### * -2: starting node parentId
### * -1: goal node temp parentId

import argparse
from os import system
import numpy as np
np.random.seed(0)
from queue import PriorityQueue

import time
import yaml
import math

parser = argparse.ArgumentParser()
parser.add_argument('--map', type=str, default=None, help='Map to test')
parser.add_argument('--map_cost', action='store_true', help='Wheter to use non-unit map cost')
parser.add_argument('--root_path', type=str, default=None, help='Path to the project root')
parser.add_argument('--route', type=str, default='/usr/local/share/master-ipr/map1/map1.csv', help='Route to the desired map')
parser.add_argument('--start_x', type=int, default=2, help='Starting X coord')
parser.add_argument('--start_y', type=int, default=2, help='Starting Y coord')
parser.add_argument('--end_x', type=int, default=7, help='Ending X coord')
parser.add_argument('--end_y', type=int, default=2, help='Ending Y coord')
args = parser.parse_args()

# Node class
class Node:
    def __init__(self, x, y, myId, parentId, g, h, f):
        self.x = x # X coord
        self.y = y # Y coord
        self.myId = myId # Node ID
        self.parentId = parentId # Parent ID
        self.g = g # Cost to node
        self.h = h # Distance to goal
        self.f = f # Total cost

    # Override <
    def __lt__(self, node):
        if self.myId < node.myId:
            return True
        else:
            return False
    # Override <=
    def __le__(self, node):
        if self.myId <= node.myId:
            return True
        else:
            return False

    def dump(self):
        print("---------- x "+str(self.x)+\
                         " | y "+str(self.y)+\
                         " | id "+str(self.myId)+\
                         " | parentId "+str(self.parentId)+\
                         " | Cost "+str(self.f))


# Read conf map
if args.map is not None:
    with open(args.root_path + '/src/map_cfgs.yaml', 'r') as ymlfile:
        cfg = yaml.load(ymlfile)

    map = args.root_path + cfg[args.map]['route']
    start_x = cfg[args.map]['coords']['start_x']
    start_y = cfg[args.map]['coords']['start_y']
    end_x = cfg[args.map]['coords']['end_x']
    end_y = cfg[args.map]['coords']['end_y']

else:
    map = args.route
    start_x = args.start_x
    start_y = args.start_y
    end_x = args.end_x
    end_y = args.end_y

# List of Nodes
path = []

# Starting position Node
init = Node(start_x, start_y, 0, -2, 0, 0, 0)
path.append((init.f, init))

# Map 2D matrix
charMap = []
# Cost 2D matrix
costMap = []

# Print color coded map
def dumpMap():
    system('clear')
    for line in charMap:
        for i in range(len(line)):
            # Highlight path
            if line[i] == '5':
                print('\033[1;31m{}\033[0m'.format(line[i]), end='    ') # Red: path
            elif line[i] == '3' or line[i] == '4':
                print('\033[1;34m{}\033[0m'.format(line[i]), end='    ') # Blue: start and goal
            elif line[i] == '1':
                print('\033[1;40m{}\033[0m'.format(line[i]), end='    ') # Black: obstacles
            elif line[i] == '2':
                print('\033[1;32m{}\033[0m'.format(line[i]), end='    ') # Green: evaluated nodes
            else:
                print('\033[1;33m{}\033[0m'.format(line[i]), end='    ') # Yellow: non-evaluated nodes
        print('\n')

# Print cost matrix
def dumpCost():
    for line in costMap:
        for i in range(len(line)):
            print('\033[1;37m{}\033[0m'.format(line[i]), end='    ')
        print('\n')

# Load map from file
with open(map) as f:
    line = f.readline()
    while line:
        charLine = line.strip().split(',')
        charMap.append(charLine)
        if args.map_cost:
            costMap.append(np.random.randint(7,size=len(charLine)))
        else:
            costMap.append(np.ones(len(charLine), dtype=int))
        line = f.readline()

# Load start and end positions
charMap[start_x][start_y] = '3' # 3: start
charMap[end_x][end_y] = '4' # 4: goal

done = False  # Exit loop when done
goalParentId = -1  # -1: goal node temp parentId

# Allowed grid moves
moves = {'up': (-1,0),
         'upright': (-1,1),
         'right': (0,1),
         'downright': (1,1),
         'down': (1,0),
         'downleft': (1,-1),
         'left': (0,-1),
         'upleft': (-1,-1),}
# List to move through the dict
ids =  ['up', 'upright', 'right', 'downright', 'down', 'downleft', 'left', 'upleft']

# PriorityQueue to store nodes in cost order
eval = PriorityQueue()
id_nodes = 0

# Main algorithm
end = 0
start = time.time()
while not done:
    print("--------------------- number of nodes: "+str(id_nodes+1))
    p = path[-1][1]
    p.dump()

    # Cycle through allowed moves
    for id in ids:
        tmpX = p.x + moves[id][0]
        tmpY = p.y + moves[id][1]

        if charMap[tmpX][tmpY] == '4':
            end = time.time() - start
            print("GOALLLL!!!")
            goalParentId = p.myId
            goal_cost = p.g + costMap[tmpX][tmpY]
            done = True
            break
        elif charMap[tmpX][tmpY] == '0':
            print("Mark visited")
            id_nodes = id_nodes+1
            # Calculate cost
            g = p.g + costMap[tmpX][tmpY]
            dx = abs(tmpX - end_x)
            dy = abs(tmpY - end_y)
            D = 1
            D2 = math.sqrt(2)
            h = D * (dx+dy) + (D2 - 2*D) * min(dx,dy) # Diagonal distance
            f = g+h # Total cost
            newNode = Node(tmpX, tmpY, id_nodes, p.myId, g, h, f)
            charMap[tmpX][tmpY] = '2'
            eval.put((f, newNode))
        elif charMap[tmpX][tmpY] == '2':
            print('Mark in eval queue, recalculate cost')
            # Calculate cost
            g = p.g + costMap[tmpX][tmpY]
            dx = abs(tmpX - end_x)
            dy = abs(tmpY - end_y)
            D = 1
            D2 = math.sqrt(2)
            h = D * (dx+dy) + (D2 - 2*D) * min(dx,dy) # Diagonal distance
            f = g+h # Total cost

            # Check if evaluated node is already in eval queue
            for item in eval.queue:
                i = item[1]
                if i.x == tmpX and i.y == tmpY:
                    # Check is evaluated node has lower f
                    if i.f > f:
                        eval.queue.remove(item)
                        newNode = Node(tmpX, tmpY, i.myId, p.myId, g, h, f)
                        eval.put((f, newNode))
                        break


        elif charMap[tmpX][tmpY] == '5':
            print('Mark in path list, re-evaluate and update parent')
            # Calcular coste
            g = p.g + costMap[tmpX][tmpY]
            dx = abs(tmpX - end_x)
            dy = abs(tmpY - end_y)
            D = 1
            D2 = math.sqrt(2)
            h = D * (dx+dy) + (D2 - 2*D) * min(dx,dy) # Diagonal distance
            f = g+h # Total cost

            # Check if evaluated node is already in path list
            for it in range(len(path)):
                item = path[it][1]
                if item.x == tmpX and item.y == tmpY:
                    # Check is evaluated node has lower f
                    if item.f > f:
                        path.pop(it)
                        newNode = Node(tmpX, tmpY, item.myId, p.myId, g, h, f)
                        path.append(newNode)
                        break

        else:
            print("Obstacle")

    # Get node with best f
    path.append(eval.get())

print("%%%%%%%%%%%%%%%%%%%")
print(f"Time until finding the goal: {end*1000} ms")
ok = False
while not ok:
    for p in path:
        node = p[1]
        if( node.myId == goalParentId ):
            if charMap[node.x][node.y] != '3':
                charMap[node.x][node.y] = '5'
            node.dump()
            goalParentId = node.parentId
            if( goalParentId == -2):
                print("%%%%%%%%%%%%%%%%%2")
                ok = True

dumpMap()
print('\n')
dumpCost()

print('\033[1;34m-----------------\033[0m')
print('\033[1;34mPath distance: {}\033[0m'.format(goal_cost))
print('\033[1;34mEvaluated nodes: {}\033[0m'.format(id_nodes+1))
print('\033[1;34mTime until finding the goal: {} ms\033[0m'.format(end*1000))
print('\033[1;34m-----------------\033[0m')
