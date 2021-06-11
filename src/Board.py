# Represents an 8x8 checker board
from typing import Sequence
import itertools
from Checker import Checker

from Utils import Point


class Board:
    squares = [
    ]

    def __init__(self):
        self.reset()

    # Indexer for getting a square of the board
    # If given a single integer index, returns a column at x.
    # If given two integer indices or a single point index,
    # returns a square at x,y.
    def __getitem__(self, indices):
        if not isinstance(indices, tuple):
            indices = tuple([indices])

        if len(indices) == 1:
            if (isinstance(indices[0], Point)):
                return self[indices[0].x, indices[0].y]
            else: # Assume it's an integer
                return self.squares[indices[0]]
        elif len(indices) == 2:
            return self.squares[indices[0]][indices[1]]
        else:
            raise "Invalid number of indices: expected 2 or 1."

    # Indexer for setting a square of the board
    # If given a single integer index, sets a column at x.
    #   value should be an array containing a Checker or None in each position.
    # If given two integer indices or a single point index,
    # sets a square at x,y.
    #   value should be a Checker or None.
    def __setitem__(self, indices, value):
        if not isinstance(indices, tuple):
            indices = tuple([indices])

        if len(indices) == 1:
            if (isinstance(indices[0], Point)):
                self[indices[0].x, indices[0].y] = value
            else: # Assume it's an integer
                self.squares[indices[0]] = value
        elif len(indices) == 2:
            self.squares[indices[0]][indices[1]] = value
        else:
            raise "Invalid number of indices: expected 2 or 1."

    def __len__(self):
        # This should always be 8 but magic numbers make
        # for late nights.
        return len(self.squares)

    # Returns whether the square at the point is occupied
    def occupied(self, point):
        if point.x >= 0 and point.x < len(self.squares) and point.y >= 0 and point.y < len(self.squares[0]):
            return not not self[point.x, point.y]
        else:
            # Everything off the board is occupied I guess
            return True

    def reset(self):
        self.squares = []
        for x in range(0, 8):
            self.squares.append([])
            for y in range(0, 8):
                if y < 3 or y > 4:
                    if x % 2 == y % 2:
                        self.squares[x].append(Checker(x, y, y > 4))
                    else:
                        self.squares[x].append(None)    
                else:
                    self.squares[x].append(None)     

    def __str__(self):
        r = ""
        for x in range(0, 8):
            column = []
            for y in range(0, 8):
                column.append(str(self.squares[x][y]) if self.squares[x][y] else '')            
            r += str(column) + ("\n" if x < 7 else "")
        return r
