from math import inf as INFINITY
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
    def __init__(self, board, src, dst, jump, king, regicidal, escapesDanger, parent = None):
        self.board = board
        self.src = src
        self.dst = dst
        self.jump = jump
        self.king = king
        self.regicidal = regicidal
        self.child = None
        self.parent = parent
        self.escapesDanger = escapesDanger
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

    # Returns whether leaf child of this move tree is a kinging move.
    def finalKing(self):
        if self.child is None:
            return self.king
        else:
            return self.child.finalKing()
        
    # Returns a list of the pieces that this move and its descendents jump.
    def victims(self):
        victs = []
        if self.jump:
            victim = self.board[self.src + (self.dst - self.src) / 2]
            victs.append(victim)
            if self.child is not None:                
                victs += self.child.victims()
            return victs
        else:
            # Non-jump moves have no victims
            return []

    def score(self):
        
        # The checker that this move would manipulate.
        # This is the root move's piece if this is a child jump.
        checker = self.getChecker()
        victims = self.victims()

        # Return infinity if this move will win the game.
        if checker is not None:
            if all(map(lambda piece: piece in victims, self.board.getCheckers(not checker.red))):
                return INFINITY

        # This is where a move's utility value is calculated.
        # We'll definitely want to change this experimentally        
        base = self.king * 2 + self.jump * 1.1 + self.regicidal
        

        if not checker is None:
            base += self.escapesDanger * (2 if checker.kinged else 1)

        # Reduce utility of moving a piece out of the back row
        # Moving away from back row : -0.25 points
        if not checker is None and self.src.y == (7 if checker.red else 0):
            base -= 0.25

        # Reduce utility of moving a non-king piece into center 2 squares
        # Move into center: -0.2 points
        if self.dst.x == 3 or self.dst.x == 4:
            base -= 0.2
            if checker is not None and checker.kinged:
                base += 0.1

        # Increase the utility of moving a non-king piece toward the king row.
        if not checker is None and not checker.kinged and (self.src.y > self.dst.y if checker.red else self.src.y < self.dst.y):
            base += 0.3

        # Add the score of the best move chained to this one.
        if self.child:
            base += self.child.score()
                
        # Calculate risk.
        # If the piece is kinged and there's no risk to this move then
        # disincentives are negated by this call.
        base += self.risk(base)
        
        return base

    def getChecker(self):        
        checker = self.board[self.src]
        if checker is None:
            return self.parent.getChecker()
        else:
            return checker

    # Returns a negative number indicating the riskiness a move poses to this piece.
    def risk(self, base = 0):
        # Where this piece would end up if took the move and all its children.
        dst = self.finalDst()
        dstDiags = self.board.getDiagonals(dst)
        # A list of victims that the move would take, which would
        # then be free as destinations for enemy jumps.
        victimPositions = [c.position for c in self.victims()]

        checker = self.getChecker()

        # Pieces that might be able to jump this piece when it's at the destination
        threats = [self.board[point] for point in dstDiags if self.board.onBoard(point) and self.board.occupied(point) and self.board[point].red != checker.red]

        risk = 0

        for piece in threats:
            if piece is None or piece.position in victimPositions:
                # Skip it if it's None or if this move would take it
                continue
            twoAhead = piece.position + ((dst - piece.position) * 2)
            onBoard = self.board.onBoard(twoAhead)
            openForJump = (not self.board.occupied(twoAhead) or twoAhead in victimPositions or twoAhead == self.src)
            pieceCanJump = piece.kinged or (piece.position.y > twoAhead.y if piece.red else piece.position.y < twoAhead.y)
            if onBoard and openForJump and pieceCanJump:
                # The piece could jump this at the destination.
                risk -= 1 + checker.kinged
        

        if risk == 0 and checker.kinged and base < 0:
            # Kings should ignore disincentives to center or move from
            # back if there's no risk to doing so.
            return -base
        else:
            return risk

    def __str__(self, score=True, direction=True):
        if score:
            r = "%s: " % self.score()
        else:
            r = ""

        if self.escapesDanger:
            r += "escape by "
        
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
