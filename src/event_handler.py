import pygame
import threading


class EventHandler():
    def __init__(self, display, game_board):
        # Set some defaults
        self.lock = threading.Lock()
        self.display = display
        self.game_board = game_board
        self.game_over = False
        self.snakes = []
        self.dead = False

    # Listener class that is being called by the main class.
    def listen(self, event):

        # Checks event type
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.KEYDOWN:
            # If the game is over it will lock the player out from doing anything that can interact with the character
            if not self.game_over:
                # Takes the movement keys, tells the game board to move the game pieces and checks for win or death
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.game_board.lolo_move(-1, 0, "LEFT")
                    self.check()
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.game_board.lolo_move(1, 0, "RIGHT")
                    self.check()
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.game_board.lolo_move(0, -1, "UP")
                    self.check()
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.game_board.lolo_move(0, 1, "DOWN")
                    self.check()
                elif event.key == pygame.K_SPACE:
                    # Checks if the shot lands and starts timer if shot lands
                    shot = self.game_board.shoot()
                    if shot is not None:
                        self.snakes.append(shot.occupied)
                        t = threading.Timer(5, self.convert_snake)
                        t.start()

            # If the game is over, press return to exit the game
            if event.key == pygame.K_RETURN:
                if self.game_over:
                    return False
            # If the user hits the escape exit the game
            elif event.key == pygame.K_ESCAPE:
                return False

            # If the user hits the r key the game resets
            elif event.key == pygame.K_r:
                self.game_board.reset()
                self.game_over = False
                self.display.set_board(self.game_board.board)
                self.display.draw_board()

        return True

    # Runs all the checks after the move
    def check(self):
        if self.game_board.check_medusa():
            self.die()
            self.dead = True
        if self.game_board.win and not self.dead:
            self.win_game()

    # tells the game board to end the game, displays the text, and locks the movement and shooting keys
    def die(self):
        self.game_board.end_game()
        self.display.draw_text('Game Over')
        self.game_over = True

    # Tells the game board to end/win the game, displays the text, locks the movement and shooting keys
    def win_game(self):
        self.game_board.win_game()
        self.display.draw_text('You Win!')
        self.game_over = True

    # locks other threads to prevent a 2nd call when the method is running, tells egg to go back to snake
    def convert_snake(self):
        self.lock.acquire()

        self.game_board.snake_return(self.snakes[0])
        self.snakes.pop(0)

        self.lock.release()



