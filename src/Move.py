from Utils import *

# Represents a single move that a piece has reported it can make,
# and an optional child move if a second or third jump can be made after
# it.
class Move:

    # Constructs a new Move.
    # board: The board that this move would act on. Used to calculate risk level.
    # src: A Point where the piece that can make the move currently is.
    # dst: A Point where the move would place the piece.
    # jump: Whether the move is a jump.
    # king: Whether the move will result in the piece newly becoming kinged.
    # regicidal: Whether the move will result in the taking of an enemy's king.
    def __init__(self, board, src, dst, jump, king, regicidal, parent = None):
        self.board = board
        self.src = src
        self.dst = dst
        self.jump = jump
        self.king = king
        self.regicidal = regicidal
        self.child = None
        self.parent = parent
        if self.parent:
            # Only jumps can have a child move
            assert self.parent.jump
            self.parent.child = self

    # Gets a list containing this move and all its descendents
    def unpack(self):
        allMoves = [self]                    
        # If this move has a child then recurse to add it to the list.
        if self.child is not None:
            allMoves += self.child.unpack()
        
        return allMoves
    
    # Returns the final destination Point of this move and any descendants
    def finalDst(self):
        if self.child is None:
            return self.dst
        else:
            return self.child.finalDst()
        
    # Returns a list of the pieces that this move and its descendents jump.
    def victims(self, board):
        victs = []
        if self.jump:
            victim = board[self.src + (self.dst - self.src) / 2]
            victs.append(victim)
            if self.child is not None:                
                victs += self.child.victims(board)
            return victs
        else:
            # Non-jump moves have no victims
            return []

    def score(self):
        # This is where a move's utility value is calculated.
        # King: 2 points
        # Jump: 1 point
        # Killing a king adds 1 point to any move
        # We'll definitely want to change this experimentally
        base = self.king * 2 + self.jump + self.regicidal

        # Reduce utility of moving a piece out of the back row
        # (WHITE piece) Moving away from back row : -0.25 points
        if self.src.y == 0:
            base -= 0.5

        # Reduce utility of moving piece into center 2 squares
        # Move into center: -0.2 points
        if self.dst.x == 3 or self.dst.x == 4:
            base -= 0.2

        # Add the score of the best move chained to this one.
        if self.child:
            base += self.child.score()
                
        # Calculate risk
        base += self.risk()
        
        return base

    # Returns a negative number indicating the riskiness a move poses to this piece.
    def risk(self):
        # Where this piece would end up if took the move and all its children.
        dst = self.finalDst()
        dstDiags = self.board.getDiagonals(dst)
        # A list of victims that the move would take, which would
        # then be free as destinations for enemy jumps.
        victimPositions = [c.position for c in self.victims(self.board)]

        
        parent = self
        checker = None
        while checker is None:
            checker = self.board[parent.src]
            parent = parent.parent
        assert checker is not None

        # Pieces that might be able to jump this piece when it's at the destination
        threats = [self.board[point] for point in dstDiags if self.board.onBoard(point) and self.board.occupied(point) and self.board[point].red != checker.red]

        risk = 0

        for piece in threats:
            if piece is None or piece.position in victimPositions:
                # Skip it if it's None or if this move would take it
                continue
            twoAhead = piece.position + ((dst - piece.position) * 2)
            if self.board.onBoard(twoAhead) and (not self.board.occupied(twoAhead) or twoAhead in victimPositions or twoAhead == self.src):
                # The piece could jump this at the destination.
                risk -= 2 + checker.kinged
        
        return risk

    def __str__(self, score=True, direction=True):
        if score:
            r = "%s: " % self.score()
        else:
            r = ""
        
        if self.jump:
            r += "jump "
        r += "%s%s to %s%s" % (
            "ABCDEFGH"[self.src.x], self.src.y + 1,
            "ABCDEFGH"[self.dst.x], self.dst.y + 1
            )
        if self.king:
            r += " and king"

        if self.child:
            r += " -> %s" % self.child.__str__(score=False)

        if direction and self.jump:
            if "in Dir" in r:
                r = r[0:r.find(" in Dir")]
            r += ' in Dir: %s' % ((self.dst - self.src) / 2)

        return r

    # Less than and greater than implementations for list sorting

    def __lt__(self, other):
        return self.score() < other.score()
    
    def __gt__(self, other):
        return self.score() > other.score()

    def __eq__(self, other):
        return self.score() == other.score()
