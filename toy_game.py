import numpy as np
from dataclasses import dataclass
from typing import List
    
@dataclass
class NormalProcess:
    mean: float
    stdev: float

    def draw_outcome(self) -> float:
        return np.random.normal(loc=self.mean, scale=self.stdev)

@dataclass
class Team:
    players: List[NormalProcess]

    def draw_scores(self) -> list:
        scores = [player.draw_outcome() for player in self.players]
        return scores

    def sum_highest_point_totals(self, n) -> float:
        top_scores = sorted(self.draw_scores())[-n:]
        return sum(top_scores)
        #return max(self.draw_scores())

def run_simulation(trials: int, n_scores: int, teams: List[Team]) -> List[List[float]]:
    results = []
    for team in teams:
        team_results = []
        for _ in range(trials):
            sum_high_scores = team.sum_highest_point_totals(n_scores)
            team_results.append(sum_high_scores)
        results.append(team_results)
    
    return results

if __name__ == "__main__":
    
    ################################################################################
    # QB
    ################################################################################
    team_1_roster = [
        NormalProcess(20, 20*.55), # Jalen Hurts
        NormalProcess(18, 18*.58), # Jayden Daniels
    ]
    team_1 = Team(team_1_roster)

    team_2_roster = [
        NormalProcess(20.5, 20.5*.35), # Patrick Mahomes
        NormalProcess(17, 17*.44), # Kirk Cousins
        NormalProcess(15, 15*.5), # Derek Carr
    ]
    team_2 = Team(team_2_roster)

    team_8_roster = [
        NormalProcess(20, 20*.55), # Jalen Hurts
        NormalProcess(18, 18*.58), # Jayden Daniels
        NormalProcess(15, 15*.5), # Derek Carr
    ]
    team_8 = Team(team_8_roster)
    
    ################################################################################
    # WR
    ################################################################################
    team_3_roster = [
        NormalProcess(16.24, 16.24*.584), # Mike Evans, 26
        NormalProcess(13.5, 13.5*.65), # Tank Dell (unofficial), 35
        NormalProcess(12, 12*.7), # Christian Watson, 66
        NormalProcess(11.7, 11.7*.72), # Jordan Addison, 95
        NormalProcess(11, 11*.72), # Rashid Shaheed, 115
        NormalProcess(10, 10*.8), # Gabe Davis, 135
        NormalProcess(10, 10*.65), # Jahan Dotson, 146
        NormalProcess(9, 9*.75), # Rashod Bateman, 175
    ]
    team_3 = Team(team_3_roster)

    team_4_roster = [
        NormalProcess(17.28, 17.28*.482), # Amon-Ra St. Brown, 4
        NormalProcess(13.51, 13.51*.627), # DeVonta Smith, 24
        NormalProcess(13.5, 13.5*.549), # Stefon Diggs, 44
        NormalProcess(12, 12*.7), # Christian Watson, 84
        NormalProcess(11, 11*.6), # Ladd McConkey, 97
        NormalProcess(11, 11*.72), # Rashid Shaheed, 117
        NormalProcess(10, 10*.65), # Adonai Mitchell, 144
        NormalProcess(9, 9*.75), # Michael Wilson, 157
    ]
    team_4 = Team(team_4_roster)

    team_9_roster = [
        NormalProcess(17.28, 17.28*.482), # Amon-Ra St. Brown, 4
        NormalProcess(13.51, 13.51*.627), # DeVonta Smith, 24
        NormalProcess(13.5, 13.5*.549), # Stefon Diggs, 44
        NormalProcess(12, 12*.7), # Christian Watson, 84
        NormalProcess(11, 11*.6), # Ladd McConkey, 97
        NormalProcess(11, 11*.72), # Rashid Shaheed, 117
        NormalProcess(10, 10*.65), # Adonai Mitchell, 144
        #NormalProcess(9, 9*.75), # Michael Wilson, 157
    ]
    team_9 = Team(team_9_roster)

    # Drafting a hurt guy who could be worth points later
    team_10_roster = [
        NormalProcess(17.28, 17.28*.482), # Amon-Ra St. Brown, 4
        NormalProcess(13.51, 13.51*.627), # DeVonta Smith, 24
        NormalProcess(13.5, 13.5*.549), # Stefon Diggs, 44
        NormalProcess(12, 12*.7), # Christian Watson, 84
        #NormalProcess(11, 11*.6), # Ladd McConkey, 97
        NormalProcess(13, 13*.55), # Hurt Player, 97
        NormalProcess(11, 11*.72), # Rashid Shaheed, 117
        NormalProcess(10, 10*.65), # Adonai Mitchell, 144
        NormalProcess(9, 9*.75), # Michael Wilson, 157
    ]
    team_10 = Team(team_10_roster)

    ################################################################################
    # TE
    ################################################################################
    team_5_roster = [
        NormalProcess(11, 11*.7), # Kyle Pitts
        NormalProcess(10.5, 10.5*.68), # Trey McBride
    ]
    team_5 = Team(team_5_roster)

    team_6_roster = [
        NormalProcess(11, 11*.74), # Kyle Pitts
        NormalProcess(8.5, 8.5*.75), # Tyler Conklin
        NormalProcess(7.8, 7.8*.76), # Cade Otton
    ]
    team_6 = Team(team_6_roster)

    team_7_roster = [
        NormalProcess(11, 11*.74), # Kyle Pitts
        NormalProcess(8.5, 8.5*.75), # Tyler Conklin
    ]
    team_7 = Team(team_7_roster)

    # Run simulation
    trials = 100000
    position_key = {
        'team_1': (team_1, 1),
        'team_2': (team_2, 1),
        'team_8': (team_8, 1),
        'team_3': (team_3, 3),
        'team_4': (team_4, 3),
        'team_9': (team_9, 3),
        'team_10': (team_10, 3),
        'team_5': (team_5, 1),
        'team_6': (team_6, 1),
        'team_7': (team_7, 1),
    }

    results = []
    for k,v in position_key.items():
        result = run_simulation(trials, v[-1], [v[0]])
        results.append(result)
        print(f"{k}: {round(sum(result[0]) / len(result[0]), 2)}")
    
    # Display results
    #for i, team_results in enumerate(results, 1):
    #    print(f"Team {i} averaged {round(sum(team_results) / len(team_results), 2)} points.")

