from pygame.event import post
from Utils import *
from Move import *
import random

class Checker:

    # Whether this piece has been kinged and can move backwards.
    kinged = False
    # Whether this is a red piece, otherwise it's white
    red = False
    position = None

    def __init__(self, x, y, red):        
        self.red = red
        self.kinged = False
        self.position = Point(x, y)

    # Returns a list of all the board positions that are diagonal of this piece.
    def getDiagonals(self, board):
        return board.getDiagonals(self.position)

    # returns:
    #   moves: list of single moves the checker can take
    #   inDanger: Whether this piece is in danger of being taken if it does not move.
    def calculateMoves(self, board, inDanger = False):
        diags = self.getDiagonals(board)

        # Empty squares this piece could move to
        moves = [Move(board, self.position, d, False, not self.kinged and (d.y == 0 if self.red else d.y == 7), inDanger, False)
                for d in diags
                if not board.occupied(d) and (self.kinged or (d.y - self.position.y < 0) == self.red)]

        jumps = self.calculateJumps(board, diags, inDanger)

        moves += jumps

        # Unpack all the moves into a flat list.
        moves = [val for sublist in [m.unpack() for m in moves] for val in sublist]

        moves.sort(reverse=True)

        return moves

    # Calculates the best move this piece could make out of all of its moves and returns it.
    # Returns None if this piece cannot move.
    def bestMove(self, board, threateningMoves = []):

        inDanger = len(threateningMoves) > 0

        # Get a list of possible moves, sorted by score in descending order
        moves = self.calculateMoves(board, inDanger)

        if len(moves) > 0:
            # If a checker has 2 or more moves with the same score,
            # randomly choose a move to be the relative best for this checker            
            if len(moves) > 1:
                bestScore = moves[0].score()                
                # Count how many moves have the best score
                tieCount = len(list(filter(lambda m: m.score() == bestScore, moves)))
                if tieCount > 1:
                    # Choose one of the tying moves
                    choiceIndex = random.randint(0, tieCount - 1)
                    return moves[choiceIndex]

                else:
                    return moves[0]
            else:
                # Return the first move because it's the best
                return moves[0]
        else:
            # This piece can't move.
            return None

    # Recursively calculates jumps that can be performed following an initial jump.
    # Contrary to the rules Michael learned in 1st grade, multi-jumps can only
    # be done in a straight line- no zigzagging.
    #
    # Parameters:
    #   board:      The instance of the Board class being used by the current game.
    #   parentMove: The Move instance that should parent any jumps found from here.
    # Returns:
    #   parentMove, with any valid jump set to its child
    def calculateChainJumps(self, board, parentMove, inDanger):
        jumpStart = parentMove.dst
        jumpDirection = (jumpStart - parentMove.src) / 2
        oneAhead = jumpStart + jumpDirection
        twoAhead = oneAhead + jumpDirection

        if not board.onBoard(twoAhead):
            # Jumping two ahead would be off the board
            return parentMove

        if board.occupied(oneAhead) and board[oneAhead].red != self.red and not board.occupied(twoAhead):
            king = not self.kinged and twoAhead.y == 0 if self.red else twoAhead.y == 7
            # Construct the jump, setting it to the child of parentMove
            nextJump = Move(board, jumpStart, twoAhead, True, king, board[oneAhead].kinged, inDanger, parentMove)
            # Recurse to chain on jumps possible from this next jump
            self.calculateChainJumps(board, nextJump, inDanger)

        elif 'DEBUG' in globals() and DEBUG:
            print("Cannot jump from %s to %s: %s" % (jumpStart, twoAhead, "\n".join(filter(lambda s:len(s) > 0, [
                "One ahead not occupied" if not board.occupied(oneAhead) else "",
                "One ahead is same color" if board.occupied(oneAhead) and board[oneAhead].red == self.red else "",
                "Two ahead is occupied" if board.occupied(twoAhead) else ""
            ]))))

        return parentMove

    # board: current board state
    # diags: array of diagonals the piece can possibly move to
    # returns:
    #   jumps: array of moves that involve a jump, with subsequent jumps in their child heirarchy as applicable.
    def calculateJumps(self, board, diags, inDanger):
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
                jumps.append(Move(board, self.position, twoAhead, True, king, inDanger, board[neighbor].kinged))

        # calculate possible squares in a straight line that can be multi-jumped to
        for j in jumps:
            self.calculateChainJumps(board, j, inDanger)

        return jumps

    # Move checker to new position on board and jump enemy checkers if applicable
    # Find the root Move, then execute all moves down to 'move' argument
    # move: Move object
    # board: Board object
    def move(self, move, board):
        self.__move(move, board, False, move.finalKing())

    # Private recursive implementation of move
    #   climbing: Whether this is a recursive call in the process of climbing to the root move
    #   king: Whether the first non-climbing call to this function was a kinging move.
    def __move(self, move, board, climbing, king):
        if move.parent is None:
            print("Executing %s" % move)
            # This is the root move, the base case
            victims = move.victims()
            checker = board[move.src]
            board[move.src] = None
            dst = move.finalDst()
            board[dst] = checker
            checker.position = dst

            # Clear the victims
            for v in victims:
                board[v.position] = None

            # King the piece if the originting move was a kinging move
            if king:
                checker.becomeKing()
        else:
            # Climb to the root parent and then execute it
            self.__move(move.parent, board, True, king)


    def becomeKing(self):
        self.kinged = True

    def deKing(self):
        self.kinged = False

    def __eq__(self, value):
        if isinstance(value, str):
            return str(self) == value
        elif isinstance(value, Checker):
            return self.position.x == value.position.x and self.position.y == value.position.y and self.red == value.red and self.kinged == value.kinged
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
        return "%s%s@%s%s" % ('r' if self.red else 'w', 'k' if self.kinged else '', "ABCDEFGH"[self.position.x], self.position.y + 1)