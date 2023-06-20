from random import shuffle

game_object_counter = 0
class GameObject:
    def __init__(self, hexagon, sprite):
        global game_object_counter
        self.hexagon = hexagon
        self.sprite = sprite
        self.id = game_object_counter
        game_object_counter += 1

    def update(self, game):
        pass

    def render(self, screen):
        side_length = self.sprite.get_rect().width
        x = self.hexagon.position[0] - (side_length // 2)
        y = self.hexagon.position[1] + (self.hexagon.radius - (side_length / 2))
        if self.sprite is not None:
            screen.blit(self.sprite, (x, y))

    def move(self, new_hex):
        self.hexagon = new_hex

    def on_destroy(self):
        pass


class Player(GameObject):
    def __init__(self, hexagon, sprite, character_sheet):
        self.character_sheet = character_sheet
        self.deck = character_sheet.deck
        shuffle(self.deck)
        self.hand = []
        self.discord_pile = []
        self.draw(7)
        super().__init__(hexagon, sprite)

    def draw(self, count):
        for i in range(0, count):
            if len(self.deck) == 0:
                self.deck = self.discord_pile
                shuffle(self.deck)
                self.discord_pile = []
            self.hand.append(self.deck.pop())



class Crate(GameObject):
    def __init__(self, *params):
        super().__init__(*params)
