from game_object_factory import *


class GameCell():
    # set values
    def __init__(self, locationX, locationY, id):
        self.locationX = locationX
        self.locationY = locationY
        gameObjectFactory = GameObjectFactory(id)
        self.occupied = gameObjectFactory.get()
        self.old = None

    # replaces old piece with new piece, old piece goes to self.old or goes to None
    def change_cell(self, piece):
        if self.occupied is not None:
            if "HEART" in self.occupied.type:
                self.old = None
            if self.occupied.type == "BRIDGE" or self.occupied.type == "TREASURE":
                self.old = self.occupied
        self.occupied = piece

    # empties cell and sets old cell back to current
    def empty(self):
        self.occupied = self.old

    # get image from game piece in the cell
    def get_image(self):
        if self.occupied is not None:
            return self.occupied.current_image
        else:
            return pygame.transform.scale(pygame.image.load("images/background.gif"), (DIMENSION, DIMENSION))

    # gets the name of the game piece in the cell
    def get_name(self):
        if self.occupied is not None:
            return self.occupied.name()
        else:
            return None
