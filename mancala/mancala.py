class Game:

    def __init__(self, board=None, whoseTurn: int=1, starting_stones_per_pocket: int=4, pockets_per_side: int=6):
        self._whoseTurn = whoseTurn if whoseTurn == 2 else 1
        # Create a board with (by default) 14 pockets. Starts at first pocket for player one and moves counter-clockwise
        # Visualization:
        #    13 12 11 10 09 08
        # 14                   07
        #    01 02 03 04 05 06

        # Validate inputs if given
        # Board elements must be integers
        if board and not all(isinstance(pocket, int) for pocket in board):
            raise ValueError("Custom board must be a list of integers.")
        # Board should have at least 4 total pockets
        if board and len(board) < 4:
            raise ValueError("Custom board must be at least 4 elements.")
        # Similarly, each side must have at least 1 pocket
        if pockets_per_side < 1:
            raise ValueError("Custom board must have at least one pocket per side.")
        # Prevent the existence negative stones
        if (starting_stones_per_pocket < 0) or (board and (pocket < 0 for pocket in board)):
            raise ValueError("Cannot have negative stones in a pocket.")

        # Start from a pre-setup board if given
        if board:
            self._board = board
            self._POCKETS_PER_SIDE = (len(board) - 2) // 2
            self._STONES_PER_POCKET = sum(board) // (len(board) - 2)

        # Otherwise generate a default board
        else:
            self._board = Game.generateBoard(starting_stones_per_pocket, pockets_per_side)
            self._POCKETS_PER_SIDE = pockets_per_side
            self._STONES_PER_POCKET = starting_stones_per_pocket

        self._history = [self.getBoard()]

    ## Static Methods

    @staticmethod
    def getScore(board: list, perspective: int=1) -> tuple:
        '''Set perspective to 2 if bottom of board is Player 2's side'''
        score = (board[len(board)//2 - 1], board[-1])
        if perspective == 2:
            return tuple(reversed(score))
        return score

    @staticmethod
    def generateBoard(starting_stones_per_pocket: int, pockets_per_side: int) -> list:
        half_board = [starting_stones_per_pocket] * pockets_per_side + [0]
        return half_board * 2

    @staticmethod
    def render(board: list) -> str:
        # Add leading 0 for spacing purposes
        # Note: Formatting will be misaligned if >99 stones in a hole
        board = [f"{b:02d}" for b in board]
        # Identify parts of the board
        p1side = board[0:(len(board)//2)-1]
        p1goal = board[(len(board)//2) -1]
        p2side = list(reversed(board[(len(board)//2):len(board)-1]))
        p2goal = board[-1]
        # Format, collate, and print the board's parts
        top_row = f"   {' '.join(p2side)}   "
        mid_row = f"{p2goal} {' '.join(['  ' for hole in p2side])} {p1goal}"
        bot_row = f"   {' '.join(p1side)}   "
        print("\n".join([top_row, mid_row, bot_row]))
        '''
        Example: default starting board
           04 04 04 04 04 04   
        00                   00
           04 04 04 04 04 04   
        '''

    # # Function to simulate a move on a given board. Maybe could be used for AI that considers possible future moves with depth.
    # @staticmethod
    # def visualizeMove(board: list, whoseTurn: int, move: int) -> list:
    #     test_game = Game(board = board, whoseTurn = whoseTurn)
    #     test_game.makeMove(move)
    #     return test_game.getBoard()

    ## Getters

    def getBoard(self, perspective: int=1) -> list:
        '''Set perspective to 2 to get rotated board'''
        if perspective == 2:
            flipped_board = self._board[len(self._board)//2:] + self._board[:len(self._board)//2]
            return flipped_board
        return self._board

    def whoseTurn(self):
        if self.isGameOver():
            return 0
        return self._whoseTurn

    def history(self) -> list:
        return self._history
    
    ## Game Logic

    def isGameOver(self) -> bool:
        score = Game.getScore(self.getBoard())
        winningScore = self._STONES_PER_POCKET * self._POCKETS_PER_SIDE
        # Game ends if one player has more than half the total possible points or if either side is cleared
        if max(score) > winningScore or self._emptySideExists():
            return True
        else:
            return False

    def winner(self) -> int:
        if self.isGameOver():
            score = Game.getScore(self.getBoard())
            if len(set(score)) == 1:
                return 3 # Tie
            return score.index(max(score)) + 1
        else:
            return None

    def _addStones(self, pocket:int, num_stones:int=1):
        # Pocket is the 0-indexed pocket of the board list
        self._board[pocket] += num_stones

    def _emptyPocket(self, pocket:int):
        # Empties the specified pocket
        self._board[pocket] = 0

    def _capturablePocket(self, pocket:int):
        # Returns the index of the pocket opposite to a specified one
        return (len(self.getBoard()) - 2) - pocket

    def _emptySideExists(self) -> bool:
        # Indicates if all of one player's holes are empty
        side_counts = (sum(self.getBoard()[:self._POCKETS_PER_SIDE]), sum(self.getBoard(perspective=2)[:self._POCKETS_PER_SIDE]))
        return 0 in side_counts

    def _collectRemainingStones(self):
        '''Adds remaining stones on each player's side to their respective scoring pockets'''
        board = self.getBoard()
        # Identify parts of the board
        p1_side = range(0, (len(board)//2) - 1)
        p1_goal = self._POCKETS_PER_SIDE
        p2_side = range((len(board)//2), len(board) -1 )
        p2_goal = len(board) - 1
        # Clean up board
        for pocket in p1_side:
            self._addStones(p1_goal, board[pocket])
            self._emptyPocket(pocket)
        for pocket in p2_side:
            self._addStones(p2_goal, board[pocket])
            self._emptyPocket(pocket)

    def _addToHistory(self, position:list):
        self._history.append(position)

    def makeMove(self, move: int):
        # Validity check - input must be an existing pocket
        if not (1 <= move <= self._POCKETS_PER_SIDE):
            raise ValueError(f"{move} is an invalid move. Must be between 1 and {self._POCKETS_PER_SIDE}.")

        # Validity check - moves can't be made once the game is over
        if self.isGameOver():
            raise RuntimeError("This game is already over. No further moves can be made.")

        # Adjust input to match board's index
        # If it's player 1's turn, moves 1 to 6 correlate with indices 0 to 5 (if 6 pockets)
        # If it's player 2's turn, moves 1 to 6 correlate with indices 7 to 12 (if 6 pockets)
        playerDependentOffset = (self.whoseTurn() - 1) * (self._POCKETS_PER_SIDE + 1) - 1
        move += playerDependentOffset
        own_side = [pocket+playerDependentOffset for pocket in range(0, self._POCKETS_PER_SIDE)] # Which pockets belong to you. Used later for identifying captures.

        # Validity check - chosen pocket must not be empty
        if self.getBoard()[move] == 0:
            raise ValueError(f"Invalid move. Chosen pocket {move - playerDependentOffset} is empty.")

        # Identify indices of scoring pockets
        if self.whoseTurn() == 1:
            own_goal = self._POCKETS_PER_SIDE
            opp_goal = len(self.getBoard()) - 1
        else:
            own_goal = len(self.getBoard()) - 1
            opp_goal = self._POCKETS_PER_SIDE
        
        # Pick up the stones, emptying the pocket
        num_stones = self.getBoard()[move]
        self._emptyPocket(move)

        # Distribute stones into the next pocket(s)
        active_pocket = move
        while num_stones > 0:
            active_pocket += 1
            active_pocket_idx = (active_pocket) % len(self.getBoard())
            # Don't drop stones into opponent's scoring pocket
            if active_pocket_idx == opp_goal:
                continue

            self._addStones(active_pocket_idx)
            num_stones -= 1

        # Capturing
        # Ending on an empty pocket on your own side allows capturing of the opponent's stones opposite your pocket
        # If the opponent's relevant pocket is empty there's no capture
        if not active_pocket_idx == own_goal:
            if active_pocket_idx in own_side:
                capturable_pocket = self._capturablePocket(active_pocket_idx)
                if self.getBoard()[active_pocket_idx] == 1 and self.getBoard()[capturable_pocket] > 0:
                    self._addStones(own_goal, self.getBoard()[active_pocket_idx])
                    self._addStones(own_goal, self.getBoard()[capturable_pocket])
                    self._emptyPocket(active_pocket_idx)
                    self._emptyPocket(capturable_pocket)

        # If this move has cleared the player's side, other player gets all stones remaining on their side
        if self._emptySideExists():
            self._collectRemainingStones()

        # Add this new position to the game's history
        self._addToHistory(self.getBoard())

        # Finishing the move in the scoring pocket allows playing again
        # If this is not the case, change whose turn it is
        if not active_pocket_idx == own_goal:
            self._whoseTurn = 2 if self.whoseTurn() == 1 else 1