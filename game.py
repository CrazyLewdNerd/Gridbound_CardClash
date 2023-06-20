from map import Map
from random import sample
from game_object import Crate, Player
from game_utils import get_image
from random import shuffle


class Game:
    def __init__(self, screen_width, screen_height, character_sheet_list, id):
        self.map = Map(screen_width, screen_height)
        self.game_object_dict = {}
        self.id = id
        self.current_turn = 0
        # self.pcs[self.current_turn] gives current player.
        # (self.pcs[self.current_turn] + 1) % len(self.pcs) gives the next turn number.
        self.round_counter = 1  # starts at round 1.
        self.on_start_funcs = []  # populate with stuff like regeneration at the start of turn
        self.on_end_funcs = []  # populate with stuff like poison at end of the turn
        self.pcs = []
        # populate game objects on hexagons
        side_length = 1.3 * self.map.hexagons[0].radius
        player_hexes = ['B5', 'B9']  # TODO add support for more than 2 players
        for hexagon in self.map.hexagons:
            self.game_object_dict[hexagon.id] = []
            if hexagon.id in player_hexes:
                i = player_hexes.index(hexagon.id)
                player_image = get_image(character_sheet_list[i].token_img, (side_length, side_length))
                self.pcs.append(Player(hexagon, player_image, character_sheet_list[i]))
                self.game_object_dict[hexagon.id].append(self.pcs[-1])
        # shuffle(self.pcs) TODO

        crate_image = get_image('crate.png', (side_length, side_length))
        crateable_hexes = self.map.hexagons[:len(self.map.hexagons) // 2]
        crateable_hexes = [crateable_hex for crateable_hex in crateable_hexes if not crateable_hex.id in player_hexes]
        for hexagon in sample(crateable_hexes, 4):
            self.game_object_dict[hexagon.id].append(Crate(hexagon, crate_image))

        for i, hexagon in enumerate(self.map.hexagons[:len(self.map.hexagons) // 2]):
            for obj in self.game_object_dict[hexagon.id]:
                if obj.__class__ is not Player:
                    mirror_hex = self.map.hexagons[-i - 1]
                    self.game_object_dict[mirror_hex.id].append(Crate(mirror_hex, crate_image))

        # start the game
        self.start_turn()

    def render(self, screen):
        self.map.render(screen)
        for hex_id, obj_list in self.game_object_dict.items():
            for obj in obj_list:
                obj.render(screen)

    def card_finder(self, card_search_txt):
        try:
            return int(card_search_txt) - 1     # if the user put an int, that's the index they want
        except Exception as e:
            print('not int')

    def start_turn(self):
        for func in self.on_start_funcs:
            func()

    def end_turn(self):
        for func in self.on_end_funcs:
            func()

    def play_card(self, card, target):
        active_pc = self.pcs[self.current_turn]
        card = active_pc.hand.pop(self.card_finder(card))
        card.activate(self, target)
        active_pc.discard_pile.append(card)