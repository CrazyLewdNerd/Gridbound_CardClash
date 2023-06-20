import random
from typing import List, Tuple
import math
import pygame
from hexagon import FlatTopHexagonTile, HexagonTile

# Constants for colors
BROWN = (72, 38, 13)
GRAY = (128, 128, 128)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
WOOD_TILE_CNT_WIDTH = 2
WOOD_TILE_CNT_HEIGHT = 2


class Map:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.background = pygame.image.load("wood.jpg")
        self.background = pygame.transform.scale(self.background, (self.screen_width // WOOD_TILE_CNT_WIDTH, self.screen_height // WOOD_TILE_CNT_HEIGHT))
        self.hexagons = self.init_hexagons()
        #TODO call utils

    @staticmethod
    def create_hexagon(position, radius=50, flat_top=False) -> HexagonTile:
        """Creates a hexagon tile at the specified position"""
        class_ = FlatTopHexagonTile if flat_top else HexagonTile
        return class_(radius, position, colour=BROWN)

    def init_hexagons(self):
        hexagons = []
        radius = 29
        mininal_radius = radius * math.cos(math.radians(30))
        row_layout = [1, 2, 3, 4, 3, 4, 3, 4, 3, 4, 3, 2, 1]

        # Adjust the horizontal and vertical spacing between hexagons
        horizontal_spacing = radius * 1.8  # Adjust the horizontal spacing
        vertical_spacing = 0.8  # Adjust the vertical spacing

        # Calculate the total width and height of the hexagon grid
        grid_width = max(row_layout) * mininal_radius * 2
        grid_height = (len(row_layout) - 1) * radius * 2 * vertical_spacing + radius * 2

        # Calculate the starting position to center the hexagons on the screen
        x_offset = (self.screen_width - grid_width) // 2
        y_offset = (self.screen_height - grid_height) // 2

        x_start = x_offset + mininal_radius
        y_start = y_offset

        # Define the letters for the column IDs
        letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

        for row, num_hexagons in enumerate(row_layout):
            x = x_start + (max(row_layout) - num_hexagons) * mininal_radius
            y = y_start + row * radius * 2 * vertical_spacing

            for column in range(num_hexagons):
                hex_id = f"{letters[column]}{row + 1}"

                hexagon = HexagonTile(radius, (x, y), BROWN, id=hex_id)

                hexagons.append(hexagon)
                x += horizontal_spacing

        return hexagons

    def render(self, screen):
        """Renders hexagons on the screen"""
        screen.fill((0, 0, 0))
        #tile the screen
        assert(WOOD_TILE_CNT_HEIGHT == 2 and WOOD_TILE_CNT_HEIGHT == 2)
        screen.blit(pygame.transform.flip(self.background, False,  False), (0, 0))
        screen.blit(pygame.transform.flip(self.background, True ,  False), (self.screen_width/WOOD_TILE_CNT_WIDTH, 0))
        screen.blit(pygame.transform.flip(self.background, False,  True ), (0, self.screen_height / WOOD_TILE_CNT_HEIGHT))
        screen.blit(pygame.transform.flip(self.background, True ,  True ), (self.screen_width/WOOD_TILE_CNT_WIDTH, self.screen_height / WOOD_TILE_CNT_HEIGHT))
        #for w in range(0, WOOD_TILE_CNT_WIDTH):
        #    for h in range(0, WOOD_TILE_CNT_HEIGHT):
        #        angle+=90
        #        rotated_image = pygame.transform.rotate(self.image, 180)
        #        if w == 0:
        #            screen.blit(self.flipped_image, (w * self.screen_width / WOOD_TILE_CNT_WIDTH, h * self.screen_height / WOOD_TILE_CNT_HEIGHT))
        #        else:
        #            screen.blit(self.image, (w * self.screen_width / WOOD_TILE_CNT_WIDTH, h * self.screen_height / WOOD_TILE_CNT_HEIGHT))
        for hexagon in self.hexagons:
            hexagon.render(screen, display_id=True)
            hexagon.render_highlight(screen, border_colour=BLACK)
        # pygame.display.flip()

    def get_hexagon(self, id):
        for hexagon in self.hexagons:
            if hexagon.id == id:
                return hexagon
        raise Exception('map 96')

#def main():
#    """Main function"""
#    pygame.init()
#    screen = pygame.display.set_mode((self.screen_width, self.screen_height))
#    clock = pygame.time.Clock()
#    game_map = Map()
#
#    terminated = False
#    while not terminated:
#        for event in pygame.event.get():
#            if event.type == pygame.QUIT:
#                terminated = True
#
#        game_map.render(screen)
#        pygame.image.save(screen, 'test.png')
#        clock.tick(5)
#    pygame.display.quit()
