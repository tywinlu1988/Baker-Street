#!/usr/bin/env python3
"""
Payoff Matrix Builder — Game theory analysis tool.
Usage: python3 payoff_matrix.py <player1_options> <player2_options> <payoffs_csv>

Input: Two lists of strategy names and a CSV of payoffs.
Output: Formatted payoff matrix with Nash equilibrium identification.

Part of the Sherlock Framework shared tool library (v0.4.2+).
"""
import sys, csv, io, json

def build_matrix(p1_strategies, p2_strategies, payoffs):
    """Construct and display a 2-player payoff matrix."""
    matrix = {}
    for i, p1s in enumerate(p1_strategies):
        for j, p2s in enumerate(p2_strategies):
            matrix[(p1s, p2s)] = payoffs[i][j]

    # Find Nash equilibria (simple pure-strategy check)
    equilibria = []
    for i, p1s in enumerate(p1_strategies):
        for j, p2s in enumerate(p2_strategies):
            p1_payoff = payoffs[i][j][0]
            p2_payoff = payoffs[i][j][1]

            # Check if P1 can improve by deviating
            p1_can_improve = False
            for k in range(len(p1_strategies)):
                if k != i and payoffs[k][j][0] > p1_payoff:
                    p1_can_improve = True
                    break

            # Check if P2 can improve by deviating
            p2_can_improve = False
            for k in range(len(p2_strategies)):
                if k != j and payoffs[i][k][1] > p2_payoff:
                    p2_can_improve = True
                    break

            if not p1_can_improve and not p2_can_improve:
                equilibria.append((p1s, p2s, payoffs[i][j]))

    result = {
        "matrix": {f"{p1s} vs {p2s}": f"({p[0]}, {p[1]})" for (p1s, p2s), p in matrix.items()},
        "nash_equilibria": [{"strategies": [s1, s2], "payoffs": p} for s1, s2, p in equilibria],
        "dominant_strategies": {
            "player1": find_dominant(p1_strategies, p2_strategies, payoffs, 0),
            "player2": find_dominant(p2_strategies, p1_strategies,
                                    [[(p[1], p[0]) for p in row] for row in payoffs], 0)
        }
    }
    print(json.dumps(result, indent=2))
    return result

def find_dominant(my_strategies, opp_strategies, payoffs, player_idx):
    """Find strictly dominant strategies for a player."""
    dominant = []
    for i, s in enumerate(my_strategies):
        is_dominant = True
        for j in range(len(my_strategies)):
            if i == j: continue
            better_in_all = True
            for k in range(len(opp_strategies)):
                if payoffs[i][k][player_idx] <= payoffs[j][k][player_idx]:
                    better_in_all = False
                    break
            if better_in_all:
                break
        else:
            is_dominant = False
        if is_dominant:
            dominant.append(s)
    return dominant if dominant else None

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Parse from command line: python3 payoff_matrix.py "A,B" "X,Y" "3,2;1,1;0,0;2,3"
        p1 = sys.argv[1].split(",")
        p2 = sys.argv[2].split(",")
        pairs = [pair.split(",") for pair in sys.argv[3].split(";")]
        payoffs = [[(int(pairs[i*len(p2)+j][0]), int(pairs[i*len(p2)+j][1]))
                     for j in range(len(p2))] for i in range(len(p1))]
        build_matrix(p1, p2, payoffs)
    else:
        # Example
        p1 = ["Cooperate", "Defect"]
        p2 = ["Cooperate", "Defect"]
        payoffs = [[(3,3), (0,5)], [(5,0), (1,1)]]
        build_matrix(p1, p2, payoffs)
