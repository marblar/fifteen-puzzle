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
        self._key = hash(tuple(tiles))
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
        return self._key == other._key

    def __hash__(self):
        return self._key

    def _coordinatesOf(self,value):
        index = self._rows.index(value)
        y = index / self.dimension
        x = index % self.dimension
        return (x,y)

    def _manhattanDistance(self,k,other):
        x1,y1 = other._coordinatesOf(k)
        x2,y2 = self._coordinatesOf(k)
        return abs(x1-x2) + abs(y1-y2)

    def heuristic(self,other):
        return sum(self._manhattanDistance(k,other) for k in range(1,self.dimension**2))

    def _inversions(self):
        parity = 0
        for (idx,tile) in enumerate(self._rows):
            if tile == 0:
                continue
            for other in self._rows[idx+1:]:
                if other == 0:
                    continue
                if tile > other:
                    parity+=1
        return parity

    def solvable(self):
        isOdd = self.dimension % 2
        inversionsEven = not self._inversions() % 2
        
        if isOdd:
            return inversionsEven 
        else:
           (column, row) = self._coordinatesOf(0)
           row_from_bottom = self.dimension - row
           oddRowFromBottom = row_from_bottom % 2
           return inversionsEven == oddRowFromBottom

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
    if not start.solvable():
        return None
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
    if not start.solvable():
        return None
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
            newVertex = nextVertex not in visited
            if newVertex or w < distance[nextVertex]:
                provenance[nextVertex] = currentVertex
                distance[nextVertex] = w
                if newVertex:
                    pprime = w + nextVertex.heuristic(end)
                    heappush(queue,(pprime,nextVertex))
                    visited.add(nextVertex)
    return None

if __name__=='__main__':
    dim = 4
    end = Board(tiles(dim),dim)
    start = generate_random_board(dim)
    solution = a_star(start,end)
    for board in reversed(solution) if solution else ["No solution for:", start]:
        print board
        print "\n"
