from Utils import *

# Represents a single move that a piece has reported it can make.
class Move:

    def __init__(self, from, to, jump, king):
        self.from = from
        self.to = to
        self.jump = jump
        self.king = king

    def score(self):
        # This is where a move's utility value is calculated.
        # King: 2 points
        # Jump: 1 point
        # We'll definitely want to change this experimentally
        return self.king * 2 + self.jump