# Mancala+

Python3 version of the board game [Mancala](https://harriscenter.org/wp-content/uploads/2020/03/mancala_rules.pdf). This implementation should work well for building and testing artificial intelligence models.

Traditionally, Mancala is played with 14 holes, each player having 6 in play and 1 hole for captured stones. Each hole in play begins with 4 stones. Here, the number of holes and the starting number of stones can both be customized, as well as starting positions and scores - hence **Mancala+**. This allowed for more varied gameplay and an enhanced environment for AI modules.

The game should be able to easily connect to any front-end graphical interface by utilizing the available methods.

## Quickstart / Try it

The game can be played from the command line by running `main.py`.

## Documentation / Usage Instructions

### Creating a game
Create an instance of class Game `game = Game()`  
This will generate a new game with default configuration.

Create a custom game by including arguments. `game = Game(pockets_per_side = 10, starting_stones_per_pocket = 5)` will begin a game with 10 holes on each side each beginning with 5 stones.

Additionally, a game can be started from a custom position by specifying a board to start from. Boards are lists of integers specifying the number of stones. The indices correlate with pockets starting at Player 1's first pocket and moving counter-clockwise to Player 2's scoring pocket. For example,
```python
board = [5, 5, 5, 5, 5, 0, 6, 6, 6, 6, 1, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0]
game = Game(board = board, starting_stones_per_pocket = 5, whoseTurn = 2)
```
will generate a game in progress that looks like this (if Player 1 is graphically on the bottom),
```
  5 5 5 5 5 5 5 5 5 5
0                     1
  5 5 5 5 5 0 6 6 6 6
```
with Player 2 to play next.

### Playing the game

A move can be made by simply calling the instance's `makeMove()` method.

The player whose turn it is can choose to play from the fourth pocket with `game.makeMove(4)`

### Static Methods
Call without an instance e.g. `Game.method(args)`

#### getScore

#### generateBoard

#### render

### Instance Methods
Call on an instance e.g. `game.method(args)`

#### getBoard

#### whoseTurn

#### history

#### isGameOver

#### winner

#### makeMove