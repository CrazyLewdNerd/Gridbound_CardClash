character_sheet_count = 0
class CharacterSheet:
    def __init__(self, player, character_name, deck, token_img='player.png'):
        global character_sheet_count
        self.player = player
        self.character_name = character_name
        self.deck = deck.copy()     # TODO copy innards
        self.token_img = token_img
        self.id = character_sheet_count
        character_sheet_count += 1
