def can_be_extended_to_solution(perm):
    i = len(perm) - 1
    for j in range(i):
        if i - j == abs(perm[i] - perm[j]):
            return False
    return True

def extend(perm, n ):
    count=0;
    if len(perm) == n:
        print(perm)
        count=1
        return count;

    for k in range(n):
        if k not in perm:
            perm.append(k)

            if can_be_extended_to_solution(perm):
                count=count+extend(perm, n)

            perm.pop()
    return count

total=extend(perm = [], n = 8)
print(total)
