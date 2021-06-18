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

    # returns:
    #   moves: list of single moves the checker can take
    #   multiJumps: list of multiple jumps the checker can take
    def calculateMoves(self, board):
        diags = self.getDiagonals(board)

        # Empty squares this piece could move to
        moves = [Move(self.position, m, False, not self.kinged and m.y == 0 if self.red else m.y == 8, False) for m in diags 
                if not board.occupied(m) and (self.kinged or (m.y - self.position.y < 0) == self.red)]

        jumps = self.calculateJumps(board, diags)

        moves += jumps

        moves.sort(reverse=True)

        return moves

    # Recursively calculates jumps that can be performed following an initial jump.
    # Contrary to the rules Michael learned in 1st grade, multi-jumps can only
    # be done in a straight line- no zigzagging.
    #
    # Parameters:
    #   board:      The instance of the Board class being used by the current game.
    #   parentMove: The Move instance that should parent any jumps found from here.
    # Returns:
    #   parentMove, with any valid jump set to its child
    def calculateChainJumps(self, board, parentMove):
        jumpStart = parentMove.dst
        jumpDirection = (jumpStart - parentMove.src) / 2
        oneAhead = jumpStart + jumpDirection
        twoAhead = oneAhead + jumpDirection

        if not board.onBoard(twoAhead):
            # Jumping two ahead would be off the board
            return parentMove

        if board.occupied(oneAhead) and board[oneAhead].red != self.red and not board.occupied(twoAhead):
            print("Can jump from %s to %s" % (jumpStart, twoAhead))
            king = not self.kinged and twoAhead.y == 0 if self.red else twoAhead.y == 7
            # Construct the jump, setting it to the child of parentMove
            nextJump = Move(jumpStart, twoAhead, True, king, board[oneAhead].kinged, parentMove)
            # Recurse to chain on jumps possible from this next jump
            self.calculateChainJumps(board, nextJump)
        elif 'DEBUG' in globals() and DEBUG:
            print("Cannot jump from %s to %s: %s" % (jumpStart, twoAhead, "\n".join(filter(lambda s:len(s) > 0, [
                "One ahead not occupied" if not board.occupied(oneAhead) else "",
                "One ahead is same color" if board.occupied(oneAhead) and board[oneAhead].red == self.red else "",
                "Two ahead is occupied" if board.occupied(twoAhead) else ""
            ]))))

        return parentMove

    # board: current board state
    # diags: array of diagonals the piece can possible move to
    # returns:
    #   jumps: array of moves that involve a jump, with subsequent jumps in their child heirarchy as applicable.
    def calculateJumps(self, board, diags):
        # A list of valid jumps that this piece can make.
        jumps = []
        # Calculate all the initial jumps possible from the current position
        for neighbor in diags:
            # Whether the neighbor has a jumpable piece
            jumpable = board.occupied(neighbor) and board[neighbor].red != self.red
            # The square two ahead of this checker in the direction from this to neighbor
            twoAhead = (neighbor + (neighbor - self.position))
            # Whether this piece can move into twoAhead
            canMove = (self.kinged or (twoAhead.y - self.position.y < 0) == self.red)
            # If the move is legal, the neighbor has a jumpable piece, and there's nothing on the
            # square two ahead, then add to the list of jumps.
            if jumpable and canMove and not board.occupied(twoAhead):
                # Whether the jump would result in this piece being newly kinged.
                king = not self.kinged and twoAhead.y == 0 if self.red else twoAhead.y == 7
                jumps.append(Move(self.position, twoAhead, True, king, board[neighbor].kinged))

        # calculate possible squares in a straight line that can be multi-jumped to
        for j in jumps:
            self.calculateChainJumps(board, j)

        return jumps

    # Move checker to new position on board
    # move: Move object
    # board: Board object
    def move(self, move, board):
        board[self.position] = None
        if not self.kinged:
            self.kinged = move.king
        self.position = move.dst
        board[self.position] = self

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