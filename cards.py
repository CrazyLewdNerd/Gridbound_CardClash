

class Card:
    def __init__(self, name, description, type):
        self.name = name
        self.description = description
        self.type = type

    def __str__(self):
        return f'{self.name}'  # TODO

    def activate(self, game, target):
        card_type_func = {
            'Basic Move' : self.basic_move_type,
        }
        card_type_func[self.type](game, target)
#    def get_target_enemy(self, game, nearest = True):

    def basic_move_type(self, game, target):
        active_pc = game.pcs[game.current_turn]
        if self.name == 'charge':
            print(active_pc.hexagon.compute_neighbours(game.map.hexagons))
            active_pc.move(active_pc.hexagon.compute_neighbours(game.map.hexagons)[0])

# TODO class specific decks
generic_deck = [
    Card(name='Charge', description='you run at them to prepare to strike',type='Basic Move'),
    Card(name='Charge', description='you run at them to prepare to strike',type='Basic Move'),
    Card(name='Charge', description='you run at them to prepare to strike',type='Basic Move'),
    Card(name='Charge', description='you run at them to prepare to strike',type='Basic Move'),
    Card(name='Charge', description='you run at them to prepare to strike',type='Basic Move'),
    Card(name='Charge', description='you run at them to prepare to strike',type='Basic Move'),
    Card(name='Charge', description='you run at them to prepare to strike',type='Basic Move'),
    Card(name='Charge', description='you run at them to prepare to strike',type='Basic Move'),
    Card(name='Charge', description='you run at them to prepare to strike',type='Basic Move'),
    Card(name='Charge', description='you run at them to prepare to strike',type='Basic Move'),
]
