import pygambit

def solve_game(payoffs):
    n_rows = len(payoffs)
    n_cols = len(payoffs[0]) if n_rows > 0 else 0

    game = pygambit.Game.new_table([n_rows, n_cols])
    game.players[0].label = "Farmer A"
    game.players[1].label = "Farmer B"
    
    strategy_labels = ["Low", "Medium", "High"]
    for i in range(n_rows):
        game.players[0].strategies[i].label = strategy_labels[i]
    for j in range(n_cols):
        game.players[1].strategies[j].label = strategy_labels[j]
    
    p1, p2 = game.players
    for i in range(n_rows):
        for j in range(n_cols):
            game[i, j][p1] = payoffs[i][j][0]
            game[i, j][p2] = payoffs[i][j][1]
    
    result = pygambit.nash.enummixed_solve(game, rational=False)
    equilibria = []

    for profile in result.equilibria:
        eq = {
            "Farmer A": [float(profile[p1][s]) for s in p1.strategies],
            "Farmer B": [float(profile[p2][s]) for s in p2.strategies]
        }
        equilibria.append(eq)
    
    return equilibria

payoffs = [ # payoff matrix
    [(5,5), (2,6), (1,3)],
    [(6,2), (3,3), (0,1)],
    [(3,1), (1,0), (-1,-1)]
]


equilibria = solve_game(payoffs)

if not equilibria:
    print("No equilibria found.")
else:
    for i, eq in enumerate(equilibria, 1):
        print(f"\nEquilibrium {i}:")
        for player, probs in eq.items():
            print(f"{player}:")
            for strat, prob in zip(["Low", "Medium", "High"], probs):
                print(f"  {strat}: {prob:.2f}")
