from collections import Counter

def mean(nums):
    if not nums:
        return 0.0
    return sum(nums) / len(nums)

def median(nums):
    if not nums:
        return 0.0
    s = sorted(nums)
    n = len(s)
    mid = n // 2
    if n % 2 == 1:
        return s[mid]
    return (s[mid - 1] + s[mid]) / 2

def mode(nums):
    if not nums:
        return None
    counts = Counter(nums)
    best_count = max(counts.values())
    if best_count == 1:
        return None
    best = [x for x, c in counts.items() if c == best_count]
    return min(best)
