def longest_palindrome_substring(s: str) -> str:
    s_len = len(s)
    if s_len == 1:
        return s

    start = 0
    end = 0
    max_substring_len = 0

    def expand_from_center(left, right):
        nonlocal start, end, max_substring_len
        while left >= 0 and right <= s_len - 1 and s[left] == s[right]:
            curr_len = right - left
            if curr_len > max_substring_len:
                max_substring_len = curr_len
                start = left
                end = right
            left -= 1
            right += 1

    for i in range(s_len):
        # odd length substring check
        expand_from_center(i, i)
        # even length substring check
        expand_from_center(i, i + 1)
    return s[start : end + 1]


res = longest_palindrome_substring("babad")
print(res)
assert "bab" == res or "aba" == res, "babad longest palindrome substring is bab or aba"

res = longest_palindrome_substring("cbbd")
print(res)
assert "bb" == res, "bb longest palindrome substring of cbbd"

res = longest_palindrome_substring("aacabdkacaa")
print(res)
assert "aca" == res, "aca longest laindrome substring of aacabdkacaa"
