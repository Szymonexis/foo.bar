def solution(M, F):
    x, y = max(int(M), int(F)), min(int(M), int(F))
    rest = 0
    while y > 0:
        rest += x // y
        x, y = y, x % y
    if x != 1:
        return "impossible"
    return str(rest - 1)