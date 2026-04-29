from heapq import merge


def merge_sort(list, key=None, reverse=False):
    if len(list) <= 1:
        return list

    mid = len(list) // 2
    left = merge_sort(list[:mid], key=key, reverse=reverse)
    right = merge_sort(list[mid:], key=key, reverse=reverse)

    return merge(left, right, key=key, reverse=reverse)

def _merge(left, right, key=None, reverse=False):
    merged = []
    i = j = 0

    while i < len(left) and j < len(right):

        if (key(left[i]) > key(right[j])) if reverse else (key(left[i]) <= key(right[j])):
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1

    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged

def quick_sort(list, key=None, reverse=False):
    if len(list) <= 1:
        return list
    k = key or (lambda x: x)
    pivot = k(list[len(list) // 2])

    less    = [x for x in list if k(x) < pivot]
    equal   = [x for x in list if k(x) == pivot]
    greater = [x for x in list if k(x) > pivot]
 
    if reverse:
        return quick_sort(greater, key=key, reverse=True) + equal + quick_sort(less, key=key, reverse=True)
    return quick_sort(less, key=key) + equal + quick_sort(greater, key=key)
