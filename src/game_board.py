from game_cell import *


class GameBoard:
    def __init__(self, location, display):
        # open file
        self.file_location = "puzzles/" + location
        # set some defaults
        self.display = display
        self.win = False
        # calls the init
        self.__init_()

    def __init_(self):
        # set more defaults
        self.scale = 0
        self.heart = 0
        self.win = False

        # create game board temporary array
        arr = []
        file = open(self.file_location, "r")
        # read lines and manipulate information
        lines = file.readlines()
        scale = lines[0][:-1].split(' ')
        self.scale = (int(scale[0]), int(scale[1]))
        self.display.set_screen(scale)
        lines.pop(0)

        # read in id from file, based off id create cell and fill into game board array
        y = 0
        for line in lines:
            new_line = line[:-1]
            cells = new_line.split(' ')
            temp = []
            x = 0
            for cell_id in cells:
                # saves the locations of the treasure, lolo, and the number of hearts
                if cell_id == '1':
                    self.lolo = [x, y]
                elif cell_id == '4' or cell_id == '10':
                    self.heart += 1
                elif cell_id == '5':
                    self.treasure = [x, y]
                game_cell = GameCell(x, y, cell_id)
                temp.append(game_cell)
                x += 1
            y += 1
            arr.append(temp)

        # set game board
        self.board = arr

        # check if the scale input and the game board dimensions are the same
        if len(arr) != self.scale[1] or len(arr[0]) != self.scale[0]:
            self.can_play = False
        else:
            self.can_play = True

        file.close()

    def lolo_move(self, x_direction, y_direction, direction):
        # Sets local variable of x and y coordinates of lolo
        x = self.lolo[0]
        y = self.lolo[1]

        # Check some boundary conditions
        can_move = False
        if x_direction < 0 and x != 0 or x_direction > 0 and x != self.scale[0] - 1:
            can_move = True
        if y_direction < 0 and y != 0 or y_direction > 0 and y != self.scale[1] - 1:
            can_move = True

        if can_move:
            # Takes the cell that lolo will move to and the one that lolo is currently in.
            move_to = self.board[y + y_direction][x + x_direction]
            current = self.board[y][x]

            # Checks if the move is valid
            print(self.check(current, move_to, x_direction, y_direction))
            if self.check(current, move_to, x_direction, y_direction):
                if move_to.occupied is not None:

                    # Update some values and run some checks
                    cell_type = move_to.get_name()
                    if "HEART" in cell_type or "TREASURE" in cell_type or cell_type == "BRIDGE":
                        if "HEART" in cell_type:
                            self.heart -= 1

                        if cell_type == "SUPER_HEART":
                            current.occupied.power_count += move_to.occupied.power_count

                        if self.heart == 0:
                            self.board[self.treasure[1]][self.treasure[0]].occupied.complete()

                        if cell_type == "OPEN_TREASURE":
                            self.win = True
                            self.win_game()

                        # move lolo location and update location in the list variable
                        current.occupied.update(direction)
                        move_to.change_cell(current.occupied)
                        current.empty()
                        self.lolo[0] = x + x_direction
                        self.lolo[1] = y + y_direction

                    elif cell_type == "BOX" or cell_type == "EGG":
                        # find cell box will move to and move box and lolo
                        current.occupied.update(direction)
                        box_move_to = self.board[move_to.locationY + y_direction][move_to.locationX + x_direction]
                        box_move_to.change_cell(move_to.occupied)
                        move_to.change_cell(current.occupied)
                        current.empty()
                        self.lolo[0] = x + x_direction
                        self.lolo[1] = y + y_direction

                else:
                    # Moves lolo and updates location in the list variable
                    current.occupied.update(direction)
                    move_to.change_cell(current.occupied)
                    current.empty()
                    self.lolo[0] = x + x_direction
                    self.lolo[1] = y + y_direction

            # Draw the board after the board is updated
            self.display.draw_board()

    def check(self, current, move_to, x_direction, y_direction):
        # Takes the type of the cell that was inputted
        cell_type = current.get_name()

        # If the cell that the current cell has to move to is none then it can proceed otherwise run the checks
        if move_to.occupied is not None:
            # Check is lolo's move is allowed, if lolo is moving another object, check if that object is allowed to move
            if move_to.occupied.walk_overable and cell_type == "LOLO":
                return True
            elif move_to.occupied.movable and cell_type == "LOLO":
                new_x = x_direction + move_to.locationX
                new_y = y_direction + move_to.locationY
                can_move = False
                if x_direction < 0 and new_x >= 0 or x_direction > 0 and new_x <= self.scale[0] - 1:
                    can_move = True
                if y_direction < 0 and new_y >= 0 or y_direction > 0 and new_y <= self.scale[1] - 1:
                    can_move = True
                if can_move:
                    return self.check(move_to, self.board[new_y][new_x], x_direction, y_direction)
                else:
                    return False
            else:
                return False
        return True

    def check_medusa(self):
        # Local variable for lolo location
        x = self.lolo[0]
        y = self.lolo[1]

        # Takes the row and column that lolo is in
        lolo_x = self.board[y]
        lolo_y = []
        for row in self.board:
            lolo_y.append(row[x])

        # Split the row and column into lists that go from lolo to the boundary of the board
        lolo_left = lolo_x[lolo_x.index(self.board[y][x]):: -1]
        lolo_right = lolo_x[lolo_x.index(self.board[y][x]):: 1]
        lolo_up = lolo_y[lolo_y.index(self.board[y][x]):: -1]
        lolo_down = lolo_y[lolo_y.index(self.board[y][x]):: 1]

        # Check if any of lolo is seen in any of the lists
        if not self.vision_check(lolo_left) \
                and not self.vision_check(lolo_right) \
                and not self.vision_check(lolo_up) \
                and not self.vision_check(lolo_down):
            return False

        return True

    def vision_check(self, arr):
        # check if vision is blocked or if medusa is present
        for cell in arr:
            if cell.get_name() == "MEDUSA":
                cell.occupied.update()
                return True
            if cell.get_name() is not None:
                if cell.occupied.block_vision:
                    return False
        return False

    def shoot(self):
        # get lolo
        x = self.lolo[0]
        y = self.lolo[1]
        lolo = self.board[y][x].occupied

        # check if ability is available
        if lolo.power_count > 0:
            lolo.power_count -= 1
            direction = lolo.direction

            lolo_x = self.board[y]
            lolo_y = []
            for row in self.board:
                lolo_y.append(row[x])
            arr = None

        # gets all cells in the direction lolo is shooting
            if direction == "LEFT":
                arr = lolo_x[lolo_x.index(self.board[y][x]):: -1]
            elif direction == "RIGHT":
                arr = lolo_x[lolo_x.index(self.board[y][x]):: 1]
            elif direction == "UP":
                arr = lolo_y[lolo_y.index(self.board[y][x]):: -1]
            else:
                arr = lolo_y[lolo_y.index(self.board[y][x]):: 1]

            arr.pop(0)

        # check if the shot will connect with a snake and sets snake to egg
            for cell in arr:
                if cell.occupied is not None:
                    if cell.occupied.type == "SNAKE" or cell.occupied.type == "EGG":
                        cell.occupied.shot()
                        self.display.draw_board()
                        return cell
                    elif not cell.occupied.type == "BRIDGE" or not cell.occupied.type == "RIVER":
                        return None
        return None

    # returns egg back to snake
    def snake_return(self, snake):
        snake.back()
        self.display.draw_board()

    # set lolo to dead
    def end_game(self):
        x = self.lolo[0]
        y = self.lolo[1]

        lolo = self.board[y][x]
        lolo.occupied.update("DEAD")
        self.display.draw_board()

    # set lolo to win
    def win_game(self):
        x = self.lolo[0]
        y = self.lolo[1]
        lolo = self.board[y][x]
        lolo.occupied.update("WIN")
        self.display.draw_board()

    # resets the board and resets lolo image
    def reset(self):
        self.__init_()