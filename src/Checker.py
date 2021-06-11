from Utils import *

class Checker:

    # Whether this piece has been kinged and can move backwards.
    kinged = False
    # Whether this is a red piece, otherwise it's white
    red = False
    position = None

    def __init__(self, x, y, red):        
        self.red = red
        self.kinged = False

    # Returns a list of all the board positions that are diagonal of this pieces.
    # These form its adjacency space.
    def getDiagonals(self, board):
        diagCoords = [
            Point(self.x - 1, self.y - 1),
            Point(self.x - 1, self.y + 1),
            Point(self.x + 1, self.y - 1),
            Point(self.x + 1, self.y + 1)
        ]

        diags = []
        for c in diagCoords:
            if c.x > 0 and c.y > 0 and c.x < 8 and c.y < 8:
                diags.append(c)
        return diags

    def calculateMoves(self, board):
        diags = self.getDiagonals(board)

        # Empty squares this piece could move to
        moves = [m for m in diags if not board.occupied(m)]

        enemies = [e for e in diags if board[e]]
                
    def __str__(self):
        return "%s%s" % ('r' if self.red else 'w', 'k' if self.kinged else '')