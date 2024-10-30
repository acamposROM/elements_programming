def pp_2d_word(s, t, matrix):
    print('   _', end='  ')
    for c in t:
        print(c, end= '  ')
    print()
    for i, r in enumerate(matrix):
        if i == 0:
            print('_', end=' ')
        else:
            print(s[i-1], end=' ')
        print(r)

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
        #print(p_s)
        #print(p_t)
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

levenshtein_dist("bar", "")
levenshtein_dist("", "bar")
levenshtein_dist("car", "bar")
levenshtein_dist("car", "bat")
#levenshtein_dist("bar", "cat")
#levenshtein_dist("hello", "world")
