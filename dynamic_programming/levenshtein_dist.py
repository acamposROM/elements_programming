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