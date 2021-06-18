from Utils import *

# Represents a single move that a piece has reported it can make.
class Move:

    # Constructs a new Move.
    # src: A Point where the piece that can make the move currently is.
    # dst: A Point where the move would place the piece.
    # jump: Whether the move is a jump.
    # king: Whether the move will result in the piece newly becoming kinged.
    # regicidal: Whether the move will result in the taking of an enemy's king.
    def __init__(self, src, dst, jump, king, regicidal, parent = None):
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

    def score(self):
        # This is where a move's utility value is calculated.
        # King: 2 points
        # Jump: 1 point
        # Killing a king adds 1 point to any move
        # We'll definitely want to change this experimentally
        base = self.king * 2 + self.jump + self.regicidal

        # Add the score of the best move chained to this one.
        if self.child:
            base += self.child.score()
        
        return base

    def __str__(self, score=True):
        if score:
            r = "%s: " % self.score()
        else:
            r = ""
        
        if self.jump:
            r += "jump "
        r += "%s%s to %s%s" % (
            "ABCDEFGH"[self.src.x], self.src.y,
            "ABCDEFGH"[self.dst.x], self.dst.y
            )
        if self.king:
            r += " and king"

        if self.child:
            r += " -> %s" % self.child.__str__(score=False)
            
        
        return r

    # Less than and greater than implementations for list sorting

    def __lt__(self, other):
        return self.score() < other.score()
    
    def __gt__(self, other):
        return self.score() > other.score()