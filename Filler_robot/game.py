import random


class Game():
    def __init__(self, name) -> None:
        self.name = name

        self.level = 1

        self.delta_turn = 50

        self.turn_min = 0


    def pour_game(self, turn) -> int:
        match self.level:
            case 1:
                self.turn_min = turn - self.delta_turn
                self.turn_max = turn + self.delta_turn
                turn = random.randint(self.turn_min, self.turn_max)
            case 2:
                self.turn_min = turn - self.delta_turn * 2
                self.turn_max = turn + self.delta_turn * 2
                turn = random.randint(self.turn_min, self.turn_max)
            case 3:
                self.turn_min = turn - self.delta_turn * 3
                self.turn_max = turn + self.delta_turn * 3
                turn = random.randint(self.turn_min, self.turn_max)
            case _:
                turn = turn
            
        return int(turn)
    

game_ruletka = Game('ruletka')
