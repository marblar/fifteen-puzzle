from random import shuffle
from copy import deepcopy
from itertools import chain
from heapq import heappush,heappop

def tiles(dimension):
    return range(1,dimension**2) + [0]

def generate_random_board(dimension):
    current_tiles = tiles(dimension)
    shuffle(current_tiles)
    return Board(current_tiles,dimension)

def index(x,y,dimension):
    return x + y*dimension

class Board(object):
    def __init__(self,tiles,dimension):
        self._rows = tiles
        self.dimension = dimension

    def __str__(self):
        rows = [self._rows[i:i+self.dimension] for i in range(0, len(self._rows), self.dimension)]
        return "\n".join([str(row) for row in rows])

    def neighbors(self):
        (x,y) = self._coordinatesOf(0)
        neighborTiles = self._neighborTiles(x,y)
        neighborBoards = []
        for (xprime,yprime) in neighborTiles:
            grid = list(self._rows)
            dim = self.dimension
            grid[index(xprime,yprime,dim)], grid[index(x,y,dim)] = grid[index(x,y,dim)], grid[index(xprime,yprime,dim)]
            neighborBoards.append(Board(grid,self.dimension))
        return neighborBoards

    def _neighborTiles(self,x,y):
        candidates = [
            (x-1,y),
            (x+1,y),
            (x,y+1),
            (x,y-1)
        ]
        valid_components = range(self.dimension)
        return filter(lambda (s,t): 
                          s in valid_components and t in valid_components, 
                      candidates)

    def __eq__(self,other):
        return self._rows == other._rows

    def __hash__(self):
        immutable_me = tuple(self._rows)
        return hash(immutable_me)

    def _coordinatesOf(self,value):
        index = self._rows.index(value)
        y = index / self.dimension
        x = index % self.dimension
        return (x,y)

    def _manhattanDistance(self,k):
        # This only works for the usual success position, but runs much faster than the arbitrary case
        x1,y1 = (k % self.dimension, k / self.dimension)
        x2,y2 = self._coordinatesOf(k)
        return abs(x1-x2) + abs(y1-y2)

    def heuristic(self):
        return sum(self._manhattanDistance(k) for k in range(self.dimension**2 - 1))

def backtrack(vertex, provenance):
    path = []
    current = vertex
    try:
        while 1:
            path.append(current)
            current = provenance[current]
    except KeyError:
        pass
    return path


def BFS(start,end):
    provenance = {}
    visited = set([start])
    queue = [start]
    while queue:
        currentVertex = queue.pop()
        if currentVertex == end:
            return backtrack(currentVertex, provenance)
        for nextVertex in currentVertex.neighbors():
            if nextVertex in visited:
                continue
            provenance[nextVertex] = currentVertex
            visited.add(nextVertex)
            queue.append(nextVertex)
    return None

def a_star(start,end):
    provenance = {}
    visited = set([start])
    queue = [(0,start)]
    distance = { 
        start : 0 
    }
    while queue:
        (priority, currentVertex) = heappop(queue)
        if currentVertex == end:
            return backtrack(currentVertex, provenance)
        d = distance[currentVertex]
        for nextVertex in currentVertex.neighbors():
            w = d + 1
            if nextVertex not in visited or w < distance[nextVertex]:
                visited.add(nextVertex)
                provenance[nextVertex] = currentVertex
                pprime = w + nextVertex.heuristic()
                heappush(queue,(pprime,nextVertex))
                distance[nextVertex] = w
    return None

if __name__=='__main__':
    dim = 3
    end = Board(tiles(dim),dim)
    start = generate_random_board(dim)
    solution = a_star(start,end)
    for board in reversed(solution) if solution else ["No solution for:", start]:
        print board
        print "\n"
