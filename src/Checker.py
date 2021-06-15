from pygame.event import post
from Utils import *
from Move import *

class Checker:

    # Whether this piece has been kinged and can move backwards.
    kinged = False
    # Whether this is a red piece, otherwise it's white
    red = False
    position = None

    def __init__(self, x, y, red):        
        self.red = red
        self.kinged = False
        self.position = Point(x,y)

    # Returns a list of all the board positions that are diagonal of this pieces.
    # These form its adjacency space.
    def getDiagonals(self, board):
        diagCoords = [
            Point(self.position.x - 1, self.position.y - 1),
            Point(self.position.x - 1, self.position.y + 1),
            Point(self.position.x + 1, self.position.y - 1),
            Point(self.position.x + 1, self.position.y + 1)
        ]

        return [c for c in diagCoords if c.x >= 0 and c.y >= 0 and c.x < 8 and c.y < 8]

    def calculateMoves(self, board):
        diags = self.getDiagonals(board)

        # Empty squares this piece could move to
        moves = [Move(self.position, m, False, not self.kinged and m.y == 0 if self.red else m.y == 8, False) for m in diags 
                if not board.occupied(m) and (self.kinged or (m.y - self.position.y < 0) == self.red)]

        jumps = []
        for neighbor in diags:
            position = self.position
            # maximum amount of consecutive jumps that can be made is 3
            maxJumps = 3
            for i in range(0, maxJumps):
                position, jump = self.calculateJumps(board, neighbor, position, self.kinged)
                if position is None and jump is None:
                    break
                if position == self.position:
                    break
                print('Position:', position)
                print('self.position:', self.position)
                print(position == self.position)
                jumps.append(jump)

            # if board.occupied(neighbor) and board[neighbor].red != self.red and not board.occupied(neighbor + (neighbor - self.position)) and (self.kinged or ((neighbor + (neighbor - self.position)).y - self.position.y < 0) == self.red):
            #     # print(board[neighbor].kinged)
            #     dst = neighbor + (neighbor - self.position)
            #     king = not self.kinged and (neighbor + (neighbor - self.position)).y == 0 if self.red else (neighbor + (neighbor - self.position)).y == 7
            #     jumps.append(Move(self.position, dst, True, king, board[neighbor].kinged))
            #
            #     # TODO: testing multiple jumps
            #     # maximum amount of consecutive jumps that can be made is 3 (subtract 1 since a jump has already been found)
            #     maxJumps = 2



        moves += jumps

        moves.sort(reverse=True)

        return moves

    def calculateJumps(self, board, neighbor, position, kinged):
        if board.occupied(neighbor) and board[neighbor].red != self.red and not board.occupied(neighbor + (neighbor - position)) and (kinged or ((neighbor + (neighbor - position)).y - position.y < 0) == self.red):
            dst = neighbor + (neighbor - self.position)
            king = not kinged and (neighbor + (neighbor - position)).y == 0 if self.red else (neighbor + (neighbor - position)).y == 7
            jump = Move(position, dst, True, king, board[neighbor].kinged)
            return dst, jump

        return None, None

    def becomeKing(self):
        self.kinged = True

    def deKing(self):
        self.kinged = False

    def __eq__(self, value):
        if isinstance(value, str):
            return str(self) == value
        elif isinstance(value, Checker):
            return self.x == value.x and self.y == value.y and self.red == value.red and self.kinged == value.kinged
        else:
            return False

    def __ne__(self, value):
        if isinstance(value, str):
            return str(self) != value
        elif isinstance(value, Checker):
            return self.position != value.position or self.red != value.red or self.kinged != value.kinged
        else:
            return True

    def __str__(self):
        return "%s%s" % ('r' if self.red else 'w', 'k' if self.kinged else '')