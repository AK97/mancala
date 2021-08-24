from mancala.mancala import Game

def play():
    game = Game()

    while not game.isGameOver():
        Game.render(game.getBoard(perspective=game.whoseTurn()))
        inp = input(f"Player {game.whoseTurn()}, make a move: ")
        try:
            game.makeMove(int(inp))
        except ValueError as e:
            print(e)
            pass

    print("Game Over!")
    Game.render(game.getBoard())
    print(f"Winner: Player {game.winner()}")
    print(f"Score: [Player 1: {Game.getScore(game.getBoard())[0]}] [Player 2: {Game.getScore(game.getBoard())[1]}]")

play()