from Utils import *

# Represents a single move that a piece has reported it can make.
class Move:

    def __init__(self, src, dst, jump, king):
        self.src = src
        self.dst = dst
        self.jump = jump
        self.king = king

    def score(self):
        # This is where a move's utility value is calculated.
        # King: 2 points
        # Jump: 1 point
        # We'll definitely want to change this experimentally
        return self.king * 2 + self.jump

    def __str__(self):
        r = "%s: " % self.score()
        if self.jump:
            r += "jump "
        r += "%s%s to %s%s" % (
            "ABCDEFGH"[self.src.x], self.src.y,
            "ABCDEFGH"[self.dst.x], self.dst.y
            )
        if self.king:
            r += " and king"
        
        return r

    def __lt__(self, other):
        return self.score() < other.score()
    
    def __gt__(self, other):
        return self.score() > other.score()