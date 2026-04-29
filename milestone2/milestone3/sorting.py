def _get_key(record, field):
    if field == 'id':
        return record.student.student_id
    elif field == 'name':
        return record.student.name.lower()
    elif field == 'date':
        return record.enroll_date
    else:
        raise ValueError(f"Invalid sort field: '{field}'. Must be 'id', 'name', or 'date'.")
 
 
 
def merge_sort(lst, field):
    if len(lst) <= 1:
        return lst
 
    mid = len(lst) // 2
    left  = merge_sort(lst[:mid], field)
    right = merge_sort(lst[mid:], field)
    return _merge(left, right, field)
 
 
def _merge(left, right, field):
    merged = []
    i = j = 0
 
    while i < len(left) and j < len(right):
        if _get_key(left[i], field) <= _get_key(right[j], field):
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
 
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged
 
 
 
def quick_sort(lst, field, low, high):
    if low < high:
        pivot_index = _partition(lst, field, low, high)
        quick_sort(lst, field, low, pivot_index - 1)
        quick_sort(lst, field, pivot_index + 1, high)
 
 
def _partition(lst, field, low, high):
    pivot = _get_key(lst[high], field)
    i = low - 1
 
    for j in range(low, high):
        if _get_key(lst[j], field) <= pivot:
            i += 1
            lst[i], lst[j] = lst[j], lst[i]
 
    lst[i + 1], lst[high] = lst[high], lst[i + 1]
    return i + 1
