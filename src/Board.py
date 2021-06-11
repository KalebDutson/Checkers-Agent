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
            raise Exception("Invalid number of indices: expected 2 or 1.")

    # Set a square to a specific piece
    # indices is the tuple (x,y)
    # checker is a Checker object at x,y
    def __setitem__(self, indices, checker):
        assert isinstance(indices, tuple) and len(indices) == 2
        self.squares[indices[0]][indices[1]] = checker

    def __len__(self):
        # This should always be 8 but magic numbers make
        # for late nights.
        return len(self.squares)

    # Returns whether the square at the point is occupied
    # point is the tuple (x,y)
    def occupied(self, point):
        return not not self[point[0]][point[1]]

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

    # clear board of all checkers
    def clear(self):
        self.squares = [
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
        ]



    def __str__(self):
        strBoard = []
        for x in range(0, 8):
            strBoard.append([])
            for y in range(0, 8):
                strBoard[x].append(str(self.squares[x][y]) if self.squares[x][y] else '')

        return str(strBoard)
