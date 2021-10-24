#! /usr/bin/env python

## A nivel mapa
### Del mapa original
### * 0: libre
### * 1: ocupado (muro/obstáculo)
### Nós
### * 2: visitado
### * 3: start
### * 4: goal

## A nivel grafo
### Nós
### * -2: parentId del nodo start
### * -1: parentId del nodo goal PROVISIONAL cuando aun no se ha resuelto

# Argument parser
import argparse
from os import system
from random import seed
from random import randint
seed(1)
from queue import PriorityQueue

import time
import yaml
import math

parser = argparse.ArgumentParser()
parser.add_argument('--map', type=str, default=None, help='Map to test')
parser.add_argument('--root_path', type=str, default=None, help='Path to the project root')
parser.add_argument('--route', type=str, default='/usr/local/share/master-ipr/map1/map1.csv', help='Route to the desired map')
parser.add_argument('--start_x', type=int, default=2, help='Starting X coord')
parser.add_argument('--start_y', type=int, default=2, help='Starting Y coord')
parser.add_argument('--end_x', type=int, default=7, help='Ending X coord')
parser.add_argument('--end_y', type=int, default=2, help='Ending Y coord')
args = parser.parse_args()

## Define Node class (A nivel grafo/nodo)

class Node:
    def __init__(self, x, y, myId, parentId, c):
        self.x = x
        self.y = y
        self.myId = myId
        self.parentId = parentId
        self.c = c

    # <
    def __lt__(self, node):
        if self.myId < node.myId:
            return True
        else:
            return False
    # <=
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
                         " | Cost "+str(self.c))


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
## `nodes` contendrá los nodos del grafo

path = []

## creamos primer nodo

init = Node(start_x, start_y, 0, -2, 0)
# init.dump()  # comprobar que primer nodo bien

## añadimos el primer nodo a `nodos`

path.append((init.c, init))

## creamos estructura de datos para mapa

charMap = []
costMap = []

## creamos función para volcar estructura de datos para mapa
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

def dumpCost():
    for line in costMap:
        for i in range(len(line)):
            print('\033[1;37m{}\033[0m'.format(line[i]), end='    ')
        print('\n')

## de fichero, (to parse/parsing) para llenar estructura de datos para mapa

with open(map) as f:
    line = f.readline()
    while line:
        charLine = line.strip().split(',')
        charMap.append(charLine)
        values = []
        for i in range(len(charLine)):
            v = randint(1,7)
            values.append(v)
        costMap.append(values)
        line = f.readline()

## a nivel mapa, integramos la info que teníamos de start & end

charMap[start_x][start_y] = '3' # 3: start
charMap[end_x][end_y] = '4' # 4: goal

## volcamos mapa por consola

dumpMap()

###### Empieza algoritmo

done = False  # clásica condición de parada del bucle `while`
goalParentId = -1  # -1: parentId del nodo goal PROVISIONAL cuando aun no se ha resuelto

start = time.time()
end = 0
moves = {'up': (-1,0),
         'upright': (-1,1),
         'right': (0,1),
         'downright': (1,1),
         'down': (1,0),
         'downleft': (1,-1),
         'left': (0,-1),
         'upleft': (-1,-1),}
ids = ['up', 'upright', 'right', 'downright', 'down', 'downleft', 'left', 'upleft']

# Heuristica: Nos quedamos con el mejor nodo que encontramos en cada it
eval = PriorityQueue()
id_nodes = 0
while not done:
    print("--------------------- number of nodes: "+str(len(path)))
    p = path[-1][1]
    p.dump()

    # Miramos los alrededores del nodo
    for id in ids:
        tmpX = p.x + moves[id][0]
        tmpY = p.y + moves[id][1]

        if charMap[tmpX][tmpY] == '4':
            end = time.time() - start
            print("GOALLLL!!!")
            goalParentId = p.myId  # aquí sustituye por real
            done = True
            break
        elif charMap[tmpX][tmpY] == '0':
            id_nodes = id_nodes+1
            print("Mark visited")
            # Calcular coste
            c = costMap[tmpX][tmpY] # Coste entre nodos.
            newNode = Node(tmpX, tmpY, id_nodes, p.myId, c)
            charMap[tmpX][tmpY] = '2'
            eval.put((c, newNode))
        else:
            print("Obstacle")

    # Buscamos el mejor nodo en función del coste
    path.append(eval.get())

    #charMap[path[-1][1].x][path[-1][1].y] = '5'

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
