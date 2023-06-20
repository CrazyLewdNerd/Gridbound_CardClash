import pygame
from game import Game
from time import sleep

SCREEN_MULTIPLIER = 32  # 9x20 is the common phone aspect ratio...ish
SCREEN_WIDTH = 9 * SCREEN_MULTIPLIER
SCREEN_HEIGHT = 20 * SCREEN_MULTIPLIER


class GameManager:
    def __init__(self):
        self.game_list = []

        # pygame.display.set_mode((0, 0), pygame.NOFRAME)  # Create a window with no frame
        self.screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))  # Create a virtual screen surface
        pygame.init()  # Initialize pygame after creating the virtual screen surface
        # self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        self.clock = pygame.time.Clock()
        self.time_counter = 0
        self.game_counter = 0 #this is NOT how many games are active, but rather used to assign a unique id

    def new_game(self, character_sheet_list):
        self.game_list.append(Game(SCREEN_WIDTH, SCREEN_HEIGHT, character_sheet_list, self.game_counter))
        self.game_counter += 1

    def render(self):
        for i, current_game in enumerate(self.game_list):
            current_game.render(self.screen)
            # pygame.display.flip()
            pygame.image.save(self.screen, f"test_{i}.png")
            #self.time_counter += self.clock.tick(5)
            #if self.time_counter >= 5000:  # Switch game every 5 seconds
            #    self.switch_game()
            #    self.time_counter = 0
            #else:
            #    pygame.time.delay(100)  # Delay 100 milliseconds between frames

    def play_card(self, author, card, game_id, target=None):
        for current_game in self.game_list:
            if game_id == current_game.id and author == current_game.pcs[current_game.current_turn].id:
                return current_game.play_card(card, target)
        return 'play_card failed'


if __name__ == "__main__":
    game_manager = GameManager()
    while True:
        game_manager.render()
        sleep(5)
