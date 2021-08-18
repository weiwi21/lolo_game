
import pygame.transform

DIMENSION = 60


# set parent class for all game objects/pieces
class GameObject:
    def __init__(self, id, type, block_vision, movable, walk_overable):
        self.block_vision = block_vision
        self.movable = movable
        self.walk_overable = walk_overable
        self.type = type
        self.id = id
        self.dimension = (DIMENSION, DIMENSION)

    def name(self):
        return self.type


# all following classes are subclasses of the game piece and will set some base values
class Bridge(GameObject):
    def __init__(self):
        super().__init__(6, "BRIDGE", False, False, True)
        self.IMAGES = []
        image = pygame.transform.scale(pygame.image.load("images/bridge.gif"), (DIMENSION, DIMENSION))
        self.IMAGES.append(image)
        self.current_image = self.IMAGES[0]


class Rock(GameObject):
    def __init__(self):
        super().__init__(8 , "ROCK",True, False, False)
        self.IMAGES = []
        image = pygame.transform.scale(pygame.image.load("images/rock.gif"), (DIMENSION, DIMENSION))
        self.IMAGES.append(image)
        self.current_image = self.IMAGES[0]


class River(GameObject):
    def __init__(self):
        super().__init__(11 , "RIVER", False, False, False)
        self.IMAGES = []
        image = pygame.transform.scale(pygame.image.load("images/water.gif"), (DIMENSION, DIMENSION))
        self.IMAGES.append(image)
        self.current_image = self.IMAGES[0]


class Box(GameObject):
    def __init__(self):
        super().__init__(2, "BOX", True, True, False)
        self.IMAGES = []
        image = pygame.transform.scale(pygame.image.load("images/box.gif"), (DIMENSION, DIMENSION))
        self.IMAGES.append(image)
        self.current_image = self.IMAGES[0]


class Heart(GameObject):
    def __init__(self):
        super().__init__(4, "HEART", False, False, True)
        self.IMAGES = []
        image = pygame.transform.scale(pygame.image.load("images/heart.gif"), (DIMENSION, DIMENSION))
        self.IMAGES.append(image)
        self.current_image = self.IMAGES[0]


# subclass of heart class re-sets some defaults
class PowerHeart(Heart):
    def __init__(self):
        super().__init__()
        self.type = "SUPER_HEART"
        self.id = 10
        self.IMAGES = []
        image = pygame.transform.scale(pygame.image.load("images/powerheart.gif"), (DIMENSION, DIMENSION))
        self.IMAGES.append(image)
        self.current_image = self.IMAGES[0]
        self.power_count = 2


class Lolo(GameObject):
    # stores locations for all of the images that lolo uses
    def __init__(self):
        super().__init__(1, "LOLO", False, True, False)
        self.power_count = 0
        self.IMAGES = []
        self.direction = "DOWN"
        location = ["lolo_s_l", "lolo_s_r", "lolo_n_l", "lolo_n_r", "lolo_e_l",
                         "lolo_e_r", "lolo_w_l", "lolo_w_r", "lolo_win",
                         "dead_w", "dead_e"]

        for image_location in location:
            file_location = "images/" + image_location + ".gif"
            image = pygame.transform.scale(pygame.image.load(file_location), (DIMENSION, DIMENSION))
            self.IMAGES.append(image)
        self.current_image = self.IMAGES[0]
        self.current_image_index = 0

    # some base classes to update values in the lolo
    def obtain_heart(self):
        self.power_count += 2

    def shoot(self):
        self.power_count -= 1

    def set_image(self, index):
        self.current_image = self.IMAGES[index]
        self.current_image_index = index

    # used to change image for lolo
    def update(self, direction):
        if direction == "UP":
            self.direction = direction
            if self.current_image_index != 2:
                self.set_image(2)
            else:
                self.set_image(3)
        if direction == "DOWN":
            self.direction = direction
            if self.current_image_index != 0:
                self.set_image(0)
            else:
                self.set_image(1)
        if direction == "LEFT":
            self.direction = direction
            if self.current_image_index != 6:
                self.set_image(6)
            else:
                self.set_image(7)
        if direction == "RIGHT":
            self.direction = direction
            if self.current_image_index != 4:
                self.set_image(4)
            else:
                self.set_image(5)

        if direction == "DEAD":
            if self.current_image_index % 2 == 0:
                self.set_image(9)
            else:
                self.set_image(10)

        if direction == "WIN":
            self.set_image(8)


class Snake(GameObject):
    # set images for snake
    def __init__(self):
        super().__init__(3, "SNAKE", True, False, False)
        self.IMAGES = []
        snake_east = pygame.transform.scale(pygame.image.load("images/snake_east.gif"), (DIMENSION, DIMENSION))
        self.IMAGES.append(snake_east)
        snake_west = pygame.transform.scale(pygame.image.load("images/snake_east.gif"), (DIMENSION, DIMENSION))
        self.IMAGES.append(snake_west)
        egg = pygame.transform.scale(pygame.image.load("images/egg.gif"), (DIMENSION, DIMENSION))
        self.IMAGES.append(egg)
        self.current_image = self.IMAGES[0]
        self.is_egg = False

    # changes image for snake
    def shot(self):
        self.is_egg = True
        self.type = "EGG"
        self.movable = True
        self.current_image = self.IMAGES[2]

    def back(self):
        self.is_egg = False
        self.type = "SNAKE"
        self.movable = False
        self.current_image = self.IMAGES[0]


class Medusa(GameObject):
    def __init__(self):
        super().__init__(7, "MEDUSA", True, False, False)
        self.IMAGES = []
        image = pygame.transform.scale(pygame.image.load("images/medusa.gif"), (DIMENSION, DIMENSION))
        self.IMAGES.append(image)
        smile = pygame.transform.scale(pygame.image.load("images/smiling_medusa.gif"), (DIMENSION, DIMENSION))
        self.IMAGES.append(smile)
        self.current_image = self.IMAGES[0]

    def update(self):
        self.current_image = self.IMAGES[1]


class Tree(GameObject):
    def __init__(self):
        super(Tree, self).__init__(9, "TREE", False, False, False)
        self.IMAGES = []
        image = pygame.transform.scale(pygame.image.load("images/tree.gif"), (DIMENSION, DIMENSION))
        self.IMAGES.append(image)
        self.current_image = self.IMAGES[0]


class Treasure(GameObject):
    def __init__(self):
        super().__init__(5, "TREASURE", False, False, True)
        self.available = False
        self.IMAGES = []
        image = pygame.transform.scale(pygame.image.load("images/treasure.gif"), (DIMENSION, DIMENSION))
        self.IMAGES.append(image)
        open = pygame.transform.scale(pygame.image.load("images/open_treasure.gif"), (DIMENSION, DIMENSION))
        self.IMAGES.append(open)
        self.current_image = self.IMAGES[0]

    def complete(self):
        self.available = True
        self.type = "OPEN_TREASURE"
        self.current_image = self.IMAGES[1]
