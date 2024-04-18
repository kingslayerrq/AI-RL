import random
import sys
import numpy as np

class Game:

    def chooseFromDict(p):
        choice = random.choices(range(1, len(p) + 1), weights=p, k=1)[0]
        return choice


    def rollDice(nDice, nSides):
        return [random.randint(1, nSides) for _ in range(nDice)]



    def chooseDice(Score, OpponentScore, LoseCount, WinCount, NDice, M):
        f = []
        for k in range(1, NDice + 1):
            wins = WinCount[Score, OpponentScore, k]
            losses = LoseCount[Score, OpponentScore, k]
            total = wins + losses
            f.append(wins / total if total > 0 else 0.5)  # Default to 0.5 if no trials

        # Calculate the probabilities of selecting each dice count
        T = sum([WinCount[Score, OpponentScore, k] + LoseCount[Score, OpponentScore, k] for k in range(1, NDice + 1)])
        probabilities = [(T * fk + M) / (T * fk + NDice * M) for fk in f]
        return Game.chooseFromDict(probabilities)
    
    def PlayGame(NDice, NSides, LTarget, UTarget, LoseCount, WinCount, M):

        scores = [0, 0]  # Initial scores for two players
        current_player = 0

        while True:
            opponent = 1 - current_player
            dice_to_roll = Game.chooseDice(scores[current_player], scores[opponent], LoseCount, WinCount, NDice, M)
            roll_result = sum(Game.rollDice(dice_to_roll, NSides))
            scores[current_player] += roll_result

 
            print("Player", current_player, "rolled", dice_to_roll, "dice and got", scores[current_player], "points.")
            if LTarget <= scores[current_player] <= UTarget:
                WinCount[scores[current_player] - roll_result, scores[opponent], dice_to_roll] += 1
                break
            elif scores[current_player] > UTarget:
                LoseCount[scores[current_player] - roll_result, scores[opponent], dice_to_roll] += 1
                break

            current_player = opponent  # Switch turns
    
    def extractAnswer(WinCount, LoseCount):
        best_moves = np.zeros(WinCount.shape[:-1])
        win_probs = np.zeros(WinCount.shape[:-1])
        for i in range(WinCount.shape[0]):
            for j in range(WinCount.shape[1]):
                total = WinCount[i, j, :] + LoseCount[i, j, :]
                probs = np.zeros_like(WinCount[i, j, :], dtype=float)
                np.divide(WinCount[i, j, :], total, out=probs, where=total != 0)

                best_moves[i, j] = np.argmax(probs)
                win_probs[i, j] = np.max(probs)
        return best_moves, win_probs

    def prog3(NDice, NSides, LTarget, UTarget, NGames, M):
        LoseCount = np.zeros((LTarget, LTarget, NDice + 1), dtype=int)
        WinCount = np.zeros((LTarget, LTarget, NDice + 1), dtype=int)

        for _ in range(NGames):
            Game.PlayGame(NDice, NSides, LTarget, UTarget, LoseCount, WinCount, M)

        best_moves, win_probs = Game.extractAnswer(WinCount, LoseCount)
        print("Play:\n", best_moves)
        print("Prob:\n", win_probs)

if  __name__ == "__main__":
    # parse cmd input arg
    if len(sys.argv) != 7:
        print("Invalid arg count!!", file=sys.stderr)
        sys.exit(0)
    Ndice = int(sys.argv[1])
    NSides = int(sys.argv[2])
    LTarget = int(sys.argv[3])
    UTarget = int(sys.argv[4])
    NGames = int(sys.argv[5])
    M = int(sys.argv[6])
    Game.prog3(Ndice, NSides, LTarget, UTarget, NGames, M)




