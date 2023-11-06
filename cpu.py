import json
import random

class CPU:
    def __init__(self, state):
        self.state = state

    def calculate_reinforcements(self, player):
        player_territories = [i for i, terr in enumerate(self.state['territories']) if terr[player] > 0]
        base_reinforcements = max(len(player_territories) // 3, 3)

        continent_bonuses = sum(
            cont["bonus"] if all(self.state['territories'][territory][player] > 0 for territory in cont["territories"])
            else 0
            for cont in self.state['continents']
        )

        total_reinforcements = base_reinforcements + continent_bonuses
        return total_reinforcements

    def reinforcement_phase(self, player):
        reinforcements = self.calculate_reinforcements(player)
        player_territories = [i for i, terr in enumerate(self.state['territories']) if terr[player] > 0]

        for _ in range(reinforcements):
            random_territory = random.choice(player_territories)
            self.state['territories'][random_territory][player] += 1


    def attack_phase(self, attacker, defender):
        player_territories = [i for i, terr in enumerate(self.state['territories']) if terr[attacker] > 0]

        if not player_territories:
            return

        attacking_territory = random.choice(player_territories)

        neighboring_territories = [i for i, terr in enumerate(self.state['territories'][attacking_territory])
                                   if terr == defender]

        if not neighboring_territories:
            return

        defending_territory = random.choice(neighboring_territories)

        attacker_armies = self.state['territories'][attacking_territory][attacker]
        defender_armies = self.state['territories'][defending_territory][defender]

        attacker_dice = [random.randint(1, 6) for _ in range(min(attacker_armies, 3))]
        defender_dice = [random.randint(1, 6) for _ in range(min(defender_armies, 2))]

        attacker_dice.sort(reverse=True)
        defender_dice.sort(reverse=True)

        for i in range(min(len(attacker_dice), len(defender_dice))):
            if attacker_dice[i] > defender_dice[i]:
                self.state['territories'][defending_territory][defender] -= 1
            else:
                self.state['territories'][attacking_territory][attacker] -= 1

    def fortification_phase(self, player):
        player_territories = [i for i, terr in enumerate(self.state['territories']) if terr[player] > 0]

        if not player_territories:
            return

        from_territory = random.choice(player_territories)
        to_territory = random.choice(player_territories)

        while from_territory == to_territory:
            to_territory = random.choice(player_territories)

        transfer_units = random.randint(1, self.state['territories'][from_territory][player] - 1)

        self.state['territories'][from_territory][player] -= transfer_units
        self.state['territories'][to_territory][player] += transfer_units

    def print_state(self):
        print(json.dumps(self.state, indent=2))

state_of_the_game = {
    "territories": [
        [0, 0], [0, 0], [0, 0],
        [0, 0], [1, 0], [0, 0],
        [0, 0], [0, 0], [0, 0]
    ],
    "continents": [
        {"bonus": 2, "territories": [0, 1, 2]}, 
        {"bonus": 3, "territories": [3, 4, 5]}  
    ]
}


if __name__ == "__main__":
    cpu_player = CPU(state_of_the_game)
    player_number = 0  
    cpu_player.reinforcement_phase(player_number)
    cpu_player.attack_phase()
    cpu_player
    cpu_player.print_state()
