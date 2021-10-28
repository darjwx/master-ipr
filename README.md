# master-ipr

- Asignatura: Introducción a la Planificación de Robots (IPR)

## Changes
#### BFS

Bfs-greedy takes bfs as a base and modifies the algorithm for a greedy approach (Depth First Search).
Instead of searching every node until the solution is found, whenever the algorithm find an obstacle, change movement direction following a 90 degree pattern:

```
[up, right, down, left]

```

#### Extras
1. Allowed movements are defined in a dict to move through them easily and remove redundancy.
2. Outputs have been improved: color coded maps and summary with number of nodes in path/cost of the path, number of evaluated nodes and time it takes to find a solution.
3. A-star algorithm implemented with 8 possible moves:

```
['up', 'upright', 'right', 'downright', 'down', 'downleft', 'left', 'upleft']

```
4. A-star can be run with randomly generated or unit (1) cost between nodes.
5. Best First Search algorithm implemented with randomly generated costs between nodes and 8 possible moves:

```
['up', 'upright', 'right', 'downright', 'down', 'downleft', 'left', 'upleft']

```
6. Comparisons between BFS and DFS and between A-star and BestFS (doc/comparison_algorithms.xlsx).
7. Start and End positions can be defined manually per map via argument parser.
8. Yaml file with each map coords info to make easier loading each map.
9. New map added (map 12).
10. Project uploaded to github with history of changes: [master-ipr](https://github.com/darjwx/master-ipr)

#### Usage
- Using map yaml loader

```
python main.py --root_path '<>/master-ipr/' --map map1
```
 --root_path: path to where the project is located.

 --map: name of the map you want to test (It has to be in the yaml file).

- Using custom coordinates

```
python main.py --route '<>/master-ipr/map1/map1.csv' --start 2 2 --end 7 2
```
 --route: route to the map csv file you want to test.

 --start: Start xy coord.

 --end: End xy coord.

- Extra arguments

--map_cost: when specified, enables non-unit cost between nodes in A-star.

#### Notes
* BFS-greedy, or better, DFS is a simple algorithm that only works in a few maps because of its lack of 'intelligence' and any kind of heuristics. In some maps it will never find a solution since its own generated path is blocking any new move as if it were an obstacle. This algorithm also creates very long paths, but since it evaluates less nodes than BFS, usually takes less time.

* BestFirstSearch is always a bit faster than A-star, but A-star has always better paths in terms of cost and evaluates less nodes. A-star is overall 16.4% better in terms of cost with a max value of 47.059%. This is explained by the fact that A-star is oriented towards the goal, where BestFS only consider the best node on each it.

* comparison_algorithms: Inside two tables can be found comparing each pair of algorithms: BFS vs DFS (unit) and BestFS vs A-star (non-unit). The numbers are the difference between each considered parameter. More detailed tables can be found in another tab for each studied map.
