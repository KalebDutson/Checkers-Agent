class CheckersPlayer:
    # Create new player
    # board: Board player is playing on
    # red: boolean, if the player's color is red
    # human: boolean, if the player is a human player
    def __init__(self, board, red, human):
        self.board = board
        self.red = red
        self.human = human

    # Determine the best move and move checker
    def executeBestMove(self):
        move, checker = self.calculateBestMove()
        if move or checker is not None:
            self.moveChecker(checker, move)
        else:
            print("%s has no moves it can make!!" % str(self))

    def moveChecker(self, checker, move):
        checker.move(move, self.board)

    # Return list of all checkers on board
    def getCheckers(self):
        checkers = []
        for i in range(0, len(self.board.squares)):
            for j in range(0, len(self.board.squares[i])):
                checker = self.board.squares[i][j]
                if checker is not None and checker.red == self.red:
                    checkers.append(checker)
        return checkers

    # Calculates the best possible move from all pieces on board
    # returns tuple (absBest, bestChecker)
    def calculateBestMove(self):
        checkers = self.getCheckers()

        # Absolute best move possible
        absBest = None
        # Checker the best move belongs to
        bestChecker = None

        for checker in checkers:
            moves = checker.calculateMoves(self.board)
            # ignore pieces that have no possible moves
            if len(moves) < 1:
                continue
            # Relative best move, the best move this checker can make
            # assumes that checker.calculateMoves returns a sorted list of moves with the best move at index 0
            relBest = moves[0]
            if absBest is None:
                absBest = relBest
                bestChecker = checker
            else:
                # compare and take best move
                if absBest < relBest:
                    absBest = relBest
                    bestChecker = checker

        return absBest, bestChecker

    def __str__(self):
        return '%s Player' % ('Red' if self.red else 'White')
