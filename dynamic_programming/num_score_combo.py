def pp_2d(matrix):
    for r in matrix:
        print(r)

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

    print(sequences[-1])
    print(len(sequences[-1]))
    return 0

def num_score_combo(scores, final_score):
    final_score += 1
    num_of_combos = [0] * final_score
    for score in scores:
        for k in range(score, final_score):
            if k == score:
                num_of_combos[k] = 1
            num_of_combos[k] += num_of_combos[k - score] 
    print(f'{num_of_combos}')
    return num_of_combos[-1]

# scores = [2, 3, 7]
#res = num_score_combo(scores, 12)
scores = [2, 3, 7]
get_all_sequences_final_score(scores, 12)
