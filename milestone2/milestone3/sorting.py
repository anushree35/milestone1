def merge_sort(list, key=None, reverse=False):
    if len(list) <= 1:
        return list

    mid = len(list) // 2
    left_half = merge_sort(list[:mid], key=key, reverse=reverse)
    right_half = merge_sort(list[mid:], key=key, reverse=reverse)

    return merge(left_half, right_half, key=key, reverse=reverse)

def _merge(left, right, key=None, reverse=False):
    merged = []
    i = j = 0

    while i < len(left) and j < len(right):
        left_key = key(left[i]) if key else left[i]
        right_key = key(right[j]) if key else right[j]

        if (left_key > right_key) if reverse else (left_key <= right_key):
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

    pivot = key(lst[len(lst) // 2]) if key else lst[len(lst) // 2]
 
    less    = [x for x in lst if (key(x) if key else x) < pivot]
    equal   = [x for x in lst if (key(x) if key else x) == pivot]
    greater = [x for x in lst if (key(x) if key else x) > pivot]
 
    if reverse:
        return quick_sort(greater, key=key, reverse=True) + equal + quick_sort(less, key=key, reverse=True)
    return quick_sort(less, key=key) + equal + quick_sort(greater, key=key)
