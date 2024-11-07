def pp_2d_word(s, t, matrix, blank_head=True):
    print(' ', end='  ') # padding for 2d array printing
    if blank_head:
        print('_', end='  ')
    for c in t:
        print(c, end= '  ')
    print()
    for i, r in enumerate(matrix):
        if not blank_head:
            i += 1
        if i == 0:
            print('_', end=' ')
        else:
            print(s[i-1], end=' ')
        print(r)
    print()

# How many edits does it take to transform t to s?
def levenshtein_dist(s, t):
    # Two scenarios to calculate:
    # Starting from index n. If t[n] == s[n], move on to the next case levenshtein_dist(s[n-1], t[n-1])
    # If this isn't true then the second scenario splits into 3 recursive calls
    # a. check levenshtein_dist(s[n-2], t[n-2]) and set t[n-1] = s[n-1]
    # b. check levenshtein_dist(s[n-1], t[n-2]) and delete t[n-1]
    # c. check levenshtein_dist(s[n-2], t[n-1]) and append s[n-1] to the end of t[n-1]
    # we want to find the case that produces the minimum amount of edits between the 3 subcases.
    # How do we DP this?
    s_len = len(s) + 1
    t_len = len(t) + 1
    place_holder = s_len + t_len 
    dp = [[place_holder] * t_len for _ in range(s_len)]
    dp[0][0] = 0
    pp_2d_word(s, t, dp)
    
    def recurse(p_s, p_t):
        if p_s < 0 or p_t < 0:
            return place_holder 
        if dp[p_s][p_t] != place_holder:
            return dp[p_s][p_t]
        dp[p_s][p_t] = min(recurse(p_s - 1, p_t - 1), recurse(p_s, p_t - 1), recurse(p_s - 1, p_t))
        curr_s_char = s[p_s - 1] if p_s - 1 >= 0 else ""
        curr_t_char = t[p_t - 1] if p_t - 1 >= 0 else ""
        if curr_s_char != curr_t_char:
            dp[p_s][p_t] += 1
        return dp[p_s][p_t]

    recurse(s_len - 1, t_len - 1)
    pp_2d_word(s, t, dp)
    return dp[-1][-1]

def longest_common_subsequence(s, t):
    s_len = len(s) + 1
    t_len = len(t) + 1
    dp = [[0] * t_len for _ in range(s_len)]
    pp_2d_word(s, t, dp)
    dp[0][0] = 0
    for i in range(1, s_len):
        for j in range(1, t_len):
            dp[i][j] = dp[i-1][j-1] + 1 if s[i-1] == t[j-1] else max(dp[i][j-1], dp[i-1][j])

    pp_2d_word(s, t, dp)
    return dp[-1][-1]

def num_of_edits_string_to_palindrom(s):
    s_len = len(s)
    dp = [[0] * s_len for _ in range(s_len)]
    index_len = s_len - 1
    for j in range(s_len):
        i = 0
        while j <= index_len and i <= index_len:
            if i == j:
                dp[i][j] = 1
            elif s[i] != s[j]:
                if i + 1 > index_len:
                    dp[i][j] = dp[i][j-1]
                elif j - 1 < 0:
                    dp[i][j] = dp[i+1][j]
                else:
                    dp[i][j] = max(dp[i+1][j], dp[i][j-1])
            else:
                dp[i][j] = 2 + dp[i+1][j-1]
            j += 1
            i += 1
    pp_2d_word(s, s, dp, blank_head=False)
    print(f'Number of deletions needed: {s_len - dp[0][index_len]}\n')
    return s_len - dp[0][index_len]

# Apparently we do not need to care abou the case where both substrings
# have the same curr char and we can simplify the loop.
def chatgpt_is_interleave(s1: str, s2: str, t: str) -> bool:
    if len(s1) + len(s2) != len(t):
        return False
    s1_len = len(s1) + 1
    s2_len = len(s2) + 1
    
    dp = [[False] * s2_len for _ in range(s1_len)]
    dp[0][0] = True 

    for i in range(s1_len):
        for j in range(s2_len):
            if i > 0 and s1[i-1] == t[i+j-1]:
                dp[i][j] = dp[i][j] or dp[i-1][j]
            if j > 0 and s2[j-1] == t[i + j - 1]:
                dp[i][j] = dp[i][j] or dp[i][j - 1]

    return dp[s1_len - 1][s2_len - 1]

def valid_interleaving_string(t, s1, s2):
    s1_len = len(s1) + 1
    s2_len = len(s2) + 1
    t_len = len(t)
    if len(s1) + len(s2) != t_len:
        return False

    dp = [[0] * s1_len for _ in range(s2_len)]
    pp_2d_word(s2, s1, dp)
    dp[0][0] = 1
    i, j, n = 0, 0, 0
    pivot_points = []
    while n < t_len:
        curr_c = t[n]
        # When both strings match the current letter, we go right first. if we pop a pivot, we check if we already
        # visited the right cell with the last condition in the if
        if i+1 <= (s2_len - 1) and curr_c == s2[i] and j+1 <= (s1_len - 1) and curr_c == s1[j]:
            pivot_points.append((i, j, n))
            j += 1
        elif i+1 <= (s2_len - 1) and curr_c == s2[i]:
            i += 1
        elif j+1 <= (s1_len - 1) and curr_c == s1[j]:
            j += 1
        else:
            if pivot_points:
                i, j, n = pivot_points.pop()
                i += 1
            else:
                pp_2d_word(s2, s1, dp)
                print(False)
                return False
        n += 1
        dp[i][j] += 1

    pp_2d_word(s2, s1, dp)
    print(True)
    return True

# num_of_edits_string_to_palindrom("abdbca")
# num_of_edits_string_to_palindrom("racecar")
# num_of_edits_string_to_palindrom("character")
#valid_interleaving_string("gatacta", "gtaa", "atc")
#print(chatgpt_is_interleave("gatacta", "gtaa", "atc"))

print(longest_common_subsequence("cat", "cra"))
