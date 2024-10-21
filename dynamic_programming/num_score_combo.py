def pp_2d(matrix):
    for r in matrix:
        print(r)


def count_sequences(scores, final_score):
    counts = [0] * (final_score + 1)
    counts[0] = 1
    for s in scores:
        for i in range(final_score + 1):
            if i - s >= 0:
                counts[i] += counts[i - s]
    return counts[-1]


def count_permutations(scores, final_score):
    counts = [0] * (final_score + 1)
    counts[0] = 1
    for i in range(final_score + 1):
        for s in scores:
            if i - s >= 0:
                counts[i] += counts[i - s]
    print(counts)
    return counts[-1]


def get_all_sequences_final_score(scores, final_score):
    sequences = []
    for i in range(0, final_score + 1):
        sequences.append([])
        for s in scores:
            prev = i - s
            if prev < 0:
                continue
            if not sequences[prev] and prev == 0:
                sequences[i].append([s])
            if sequences[prev]:
                for prev_seq in sequences[prev]:
                    new_seq = prev_seq + [s]
                    sequences[i].append(new_seq)

    return sequences[-1]


def num_score_combo(scores, final_score):
    final_score += 1
    num_of_combos = [0] * final_score
    for score in scores:
        for k in range(score, final_score):
            if k == score:
                num_of_combos[k] = 1
            num_of_combos[k] += num_of_combos[k - score]
    print(f"{num_of_combos}")
    return num_of_combos[-1]


def team_distinct_interleave(s, t, scores):
    # first we need to calculate all possible sequences for the given score
    # ex if the score is 5 and scores [2,3] we will have [[2,3], [3,2]]
    # we just need the lengths of these to know that team S scored twice
    # with the score of 5. We will use that later to figure out all the distinct scoring sequences
    # given another team T.
    s_plays_seq = get_all_sequences_final_score(scores, s)
    t_plays_seq = get_all_sequences_final_score(scores, t)

    # we have all the sequences but we just really need lengths
    # of each possible sequence for this problem
    s_plays = [len(s) for s in s_plays_seq]
    t_plays = [len(t) for t in t_plays_seq]
    
    # from math import factorial
    # Use combinatorics to calculate the number of interleavings
    # Formula: C(n + m, n) = (n + m)! / (n! * m!)
    # We divide by n! * m! to remove overcounted combinations
    # ex: s1 s2 t1. s2 s1 t1. Team S scored 2 times in a row
    # but we dont care about the unique play number for this problem
    # it should be just s s t. Which is why we need to divide to remove
    # those extra counts
    # return factorial(s_plays + t_plays) // (factorial(s_plays) * factorial(t_plays))

    # we can use DP to speed things up
    def dp_interleaving(S, T):
        # Create an S X T to save previous combination recurrences
        dp = [[0] * (T + 1) for _ in range(S + 1)]
        for i in range(S + 1):
            for j in range(T + 1):
                # if j = 0, there is only 1 way to choose 0 items from i
                # if j = i there is only 1 way to chooose i items from i
                if j == 0 or i == 0:
                    dp[i][j] = 1
                else:
                    # dp recurrence relation for interleaving
                    # C(n,k)=C(n,k−1) + C(n−1,k)
                    # interleaving n with k is the same as interleaving n with k-1 + n-1 with k.
                    # We choose to place either team Ts score or Team Ss and we need to add for both those
                    # possibilities
                    dp[i][j] = dp[i - 1][j] + dp[i][j - 1]

        print(dp)
        return dp

    # depending on the final_score and plays, we can have N number of valid sequences
    # but in a game, only one sequence will be valid. so in order to calculate
    # all possible distinct scoring sequences between S and T, we need to
    # to find the interleaving relation of each sequence that may have occurred for S and T

    # first create the DP table once with the max values in each list
    dp_table = dp_interleaving(max(s_plays), max(t_plays))
    scoring_sequences = 0

    # iterate through each possible sequence of play for each team and find the
    # interleaving relation
    for sp in s_plays:
        for tp in t_plays:
            scoring_sequences += dp_table[sp][tp]
    return scoring_sequences

def teams_lead_change(s, t, scores):
    # first we need to calculate all possible sequences for the given score
    # ex if the score is 5 and scores [2,3] we will have [[2,3], [3,2]]
    # we just need the lengths of these to know that team S scored twice
    # with the score of 5. We will use that later to figure out all the distinct scoring sequences
    # given another team T.
    s_plays_seq = get_all_sequences_final_score(scores, s)
    t_plays_seq = get_all_sequences_final_score(scores, t)
    print(s_plays_seq)
    print(t_plays_seq)
    
    def find_max_leads_btwn_two_seq(sp, tp, s_score, t_score):
        return 0
    
    for sp in s_plays_seq:
        for tp in t_plays_seq:
            print()
    
    return 0

# scores = [2, 3, 7]
# res = num_score_combo(scores, 12)
scores = [2, 3]
# get_all_sequences_final_score(scores, 12)
# count_permutations(scores, 4)
# count_sequences(scores, 12)

# res = team_distinct_interleave(6, 4, scores)
# print(res)

teams_lead_change(6, 4, scores)