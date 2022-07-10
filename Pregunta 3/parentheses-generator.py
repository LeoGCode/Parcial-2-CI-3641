def _generate_parenthesis(n, Open, close, s, ans):
    if Open == n and close == n:
        ans.append(s)
        return
    if Open < n:
        _generate_parenthesis(n, Open + 1, close, s + "{", ans)
    if close < Open:
        _generate_parenthesis(n, Open, close + 1, s + "}", ans)


def generate_parenthesis(n):
    ans = []
    _generate_parenthesis(n, 0, 0, "", ans)
    for i in ans:
        yield i


if __name__ == '__main__':
    n = 3
    for s in generate_parenthesis(n):
        print(s)
