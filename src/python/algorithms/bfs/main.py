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

import time
import yaml

parser = argparse.ArgumentParser()
parser.add_argument('--map', type=str, default=None, help='Map to test')
parser.add_argument('--root_path', type=str, default=None, help='Path to the project root')
parser.add_argument('--route', type=str, default='/usr/local/share/master-ipr/map1/map1.csv', help='Route to the desired map')
parser.add_argument('--start_x', type=int, default=2, help='Starting X coord')
parser.add_argument('--start_y', type=int, default=2, help='Starting Y coord')
parser.add_argument('--end_x', type=int, default=7, help='Ending X coord')
parser.add_argument('--end_y', type=int, default=2, help='Ending Y coord')
args = parser.parse_args()

# Node class
class Node:
    def __init__(self, x, y, myId, parentId):
        self.x = x # X coord
        self.y = y # Y coord
        self.myId = myId # Node ID
        self.parentId = parentId # Parent ID
    def dump(self):
        print("---------- x "+str(self.x)+\
                         " | y "+str(self.y)+\
                         " | id "+str(self.myId)+\
                         " | parentId "+str(self.parentId))

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
nodes = []

# Starting position Node
init = Node(start_x, start_y, 0, -2)
nodes.append(init)

# Map 2D matrix
charMap = []

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

# Load map from file
with open(map) as f:
    line = f.readline()
    while line:
        charLine = line.strip().split(',')
        charMap.append(charLine)
        line = f.readline()

# Load start and end positions
charMap[start_x][start_y] = '3' # 3: start
charMap[end_x][end_y] = '4' # 4: goal

done = False  # Exit loop when done
goalParentId = -1  # -1: goal node temp parentId

# Main algorithm
end = 0
start = time.time()
while not done:
    print("--------------------- number of nodes: "+str(len(nodes)))
    for node in nodes:
        node.dump()

        # up
        tmpX = node.x - 1
        tmpY = node.y
        if( charMap[tmpX][tmpY] == '4' ):
            end = time.time() - start
            print("up: GOALLLL!!!")
            goalParentId = node.myId
            done = True
            break
        elif ( charMap[tmpX][tmpY] == '0' ):
            print("up: mark visited")
            newNode = Node(tmpX, tmpY, len(nodes), node.myId)
            charMap[tmpX][tmpY] = '2'
            nodes.append(newNode)

        # down
        tmpX = node.x + 1
        tmpY = node.y
        if( charMap[tmpX][tmpY] == '4' ):
            end = time.time() - start
            print("down: GOALLLL!!!")
            goalParentId = node.myId
            done = True
            break
        elif ( charMap[tmpX][tmpY] == '0' ):
            print("down: mark visited")
            newNode = Node(tmpX, tmpY, len(nodes), node.myId)
            charMap[tmpX][tmpY] = '2'
            nodes.append(newNode)

        # right
        tmpX = node.x
        tmpY = node.y + 1
        if( charMap[tmpX][tmpY] == '4' ):
            end = time.time() - start
            print("right: GOALLLL!!!")
            goalParentId = node.myId
            done = True
            break
        elif ( charMap[tmpX][tmpY] == '0' ):
            print("right    : mark visited")
            newNode = Node(tmpX, tmpY, len(nodes), node.myId)
            charMap[tmpX][tmpY] = '2'
            nodes.append(newNode)

        # left
        tmpX = node.x
        tmpY = node.y - 1
        if( charMap[tmpX][tmpY] == '4' ):
            end = time.time() - start
            print("left: GOALLLL!!!")
            goalParentId = node.myId
            done = True
            break
        elif ( charMap[tmpX][tmpY] == '0' ):
            print("left: mark visited")
            newNode = Node(tmpX, tmpY, len(nodes), node.myId)
            charMap[tmpX][tmpY] = '2'
            nodes.append(newNode)

print("%%%%%%%%%%%%%%%%%%%")
ok = False
num_nodes = 0
while not ok:
    for node in nodes:
        if( node.myId == goalParentId ):
            if charMap[node.x][node.y] != '3':
                charMap[node.x][node.y] = '5'
            node.dump()
            num_nodes += 1
            goalParentId = node.parentId
            if( goalParentId == -2):
                print("%%%%%%%%%%%%%%%%%2")
                ok = True

dumpMap()
print('\033[1;34m-----------------\033[0m')
print('\033[1;34mNumber of nodes in path: {}\033[0m'.format(num_nodes))
print('\033[1;34mEvaluated nodes: {}\033[0m'.format(len(nodes)))
print('\033[1;34mTime until finding the goal: {} ms\033[0m'.format(end*1000))
print('\033[1;34m-----------------\033[0m')
