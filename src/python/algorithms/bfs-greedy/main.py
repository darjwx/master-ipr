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

import time

parser = argparse.ArgumentParser()
parser.add_argument('--map', type=str, default='/usr/local/share/master-ipr/map1/map1.csv', help='Route to the desired map')
parser.add_argument('--start_x', type=int, default=2, help='Starting X coord')
parser.add_argument('--start_y', type=int, default=2, help='Starting Y coord')
parser.add_argument('--end_x', type=int, default=7, help='Ending X coord')
parser.add_argument('--end_y', type=int, default=2, help='Ending Y coord')
args = parser.parse_args()

## Define Node class (A nivel grafo/nodo)

class Node:
    def __init__(self, x, y, myId, parentId):
        self.x = x
        self.y = y
        self.myId = myId
        self.parentId = parentId
    def dump(self):
        print("---------- x "+str(self.x)+\
                         " | y "+str(self.y)+\
                         " | id "+str(self.myId)+\
                         " | parentId "+str(self.parentId))


## `nodes` contendrá los nodos del grafo

nodes = []

## creamos primer nodo

init = Node(args.start_x, args.start_y, 0, -2)
# init.dump()  # comprobar que primer nodo bien

## añadimos el primer nodo a `nodos`

nodes.append(init)

## creamos estructura de datos para mapa

charMap = []

## creamos función para volcar estructura de datos para mapa

def dumpMap():
    for line in charMap:
        print(line)

## de fichero, (to parse/parsing) para llenar estructura de datos para mapa

with open(args.map) as f:
    line = f.readline()
    while line:
        charLine = line.strip().split(',')
        charMap.append(charLine)
        line = f.readline()

## a nivel mapa, integramos la info que teníamos de start & end

charMap[args.start_y][args.start_x] = '3' # 3: start
charMap[args.end_x][args.end_y] = '4' # 4: goal

## volcamos mapa por consola

dumpMap()

###### Empieza algoritmo

done = False  # clásica condición de parada del bucle `while`
goalParentId = -1  # -1: parentId del nodo goal PROVISIONAL cuando aun no se ha resuelto

start = time.time()
end = 0
moves = {'up': (-1,0),
         'right': (0,1),
         'down': (1,0),
         'left': (0,-1)}
ids =  ['up', 'right', 'down', 'left']
n = 0

# Heuristica: Giros de 90 cuando se encuantra un obstaculo
while not done:
    print("--------------------- number of nodes: "+str(len(nodes)))
    node = nodes[-1]
    node.dump()
    tmpX = node.x + moves[ids[n]][0]
    tmpY = node.y + moves[ids[n]][1]
    if charMap[tmpX][tmpY] == '4':
        end = time.time() - start
        print("up: GOALLLL!!!")
        goalParentId = node.myId  # aquí sustituye por real
        done = True
        break
    elif charMap[tmpX][tmpY] == '0':
        print("up: mark visited")
        newNode = Node(tmpX, tmpY, len(nodes), node.myId)
        charMap[tmpX][tmpY] = '2'
        nodes.append(newNode)
    else:
        print("up: Obstacle")
        # Change movement direction
        n = n + 1
        if n >= len(ids):
            n = 0

    dumpMap()

print("%%%%%%%%%%%%%%%%%%%")
print(f"Time until finding the goal: {end*1000} ms")
ok = False
while not ok:
    for node in nodes:
        if( node.myId == goalParentId ):
            node.dump()
            goalParentId = node.parentId
            if( goalParentId == -2):
                print("%%%%%%%%%%%%%%%%%2")
                ok = True
