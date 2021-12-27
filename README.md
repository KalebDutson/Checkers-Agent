# Checkers Agent

## Installing Dependencies

Python Version: Python 3.8

The only dependency is PyGame. To install, use the following command:
```bash
pip install pygame
```
<br>

## Running the game
Navigate to the main project directory **Checkers-Agent**.

Run the following to launch the game:
```bash
python3 src/main.py
```
<br>

## Testing Mode
Testing mode allows you to control who's turn it is, add / remove pieces to the board, and print a piece's list of moves
to the terminal.
#### Hotkeys
* `T`: Activate testing mode
* `R`: Reset board
* `C`: Clear board of all pieces
* `K`: King / un-king piece at mouse location
* `P`: Print available moves of the piece at mouse location
* `B`: Print board to console.
* `A`: Auto-play: let the AI control both colors very quickly and automatically start new games.
* `ENTER`: Switch player turn
* `SPACE`: Execute best move for player of current turn
* `Left Mouse`: Add a **RED** piece to the board. Left click again to remove.
* `Right Mouse`: Add a **WHITE** piece to the board. Right click again to remove.
* `Middle Mouse`: Print info of checker at mouse location.
