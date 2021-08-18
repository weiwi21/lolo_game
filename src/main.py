import os.path
import sys

from event_handler import *
from display import *
from game_board import *


def main():
    args = sys.argv[1:]

    location = args[0] if len(args) > 0 else "setting3.pzl"
    if not os.path.isfile(location):
        print("\nThe file " + location + " does not exist.")
        sys.exit(1)

    # Initiate the pygame
    pygame.init()

    # Set's some default values
    pygame.display.set_caption('Lolo Game')
    display = Display()
    game_board = GameBoard(location, display)

    # Check if the puzzle input is the correct settings
    if game_board.can_play:

        # Sets the rest of the settings
        display.set_board(game_board.board)
        display.draw_board()
        event_handler = EventHandler(display, game_board)

        # Starts your game loop and the loop will end when the event handler returns false
        running = True
        while running:
            for event in pygame.event.get():
                running = event_handler.listen(event)
    else:
        print("Please enter a valid game board in the setting or the valid dimensions")


if __name__ == '__main__':
    main()
