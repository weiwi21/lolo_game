from game_object import *


# factory class for game cell initiation
class GameObjectFactory:
    def __init__(self):
        self.id_list = {
            '1': self.lolo,
            '2': self.box,
            '3': self.snake,
            '4': self.heart,
            '5': self.treasure,
            '6': self.bridge,
            '7': self.medusa,
            '8': self.rock,
            '9': self.tree,
            '10': self.power_heart,
            '11': self.river
        }

    def get(self, id):
        if not id or id == '0':
            return None
        return self.id_list[id]()

    def lolo(self):
        return Lolo()

    def box(self):
        return Box()

    def snake(self):
        return Snake()

    def heart(self):
        return Heart()

    def treasure(self):
        return Treasure()

    def bridge(self):
        return Bridge()

    def medusa(self):
        return Medusa()

    def rock(self):
        return Rock()

    def tree(self):
        return Tree()

    def power_heart(self):
        return PowerHeart()

    def river(self):
        return River()
