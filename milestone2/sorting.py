def insertion_sort(records, by):
    for i in range(1, len(records)):
        key_record = records[i]
        j = i - 1
        while j >= 0 and _get_key(records[j], by) > _get_key(key_record, by):
            records[j + 1] = records[j]
            j -= 1
        records[j + 1] = key_record

def selection_sort(records, by):
    for i in range(len(records)):
        min_index = i
        for j in range(i + 1, len(records)):
            if _get_key(records[j], by) < _get_key(records[min_index], by):
                min_index = j
        records[i], records[min_index] = records[min_index], records[i]

def recursive_binary_search(records, target_id, low, high):
    if low > high:
        return -1
    mid = (low + high) // 2
    mid_id = records[mid].student.student_id

    if mid_id == target_id:
        return mid
    elif mid_id < target_id:
        return recursive_binary_search(records, target_id, mid + 1, high)
    else:
        return recursive_binary_search(records, target_id, low, mid - 1)
    

def _get_key(record, by):
    if by == 'name':
        return record.student.name
    elif by == 'id':
        return record.student.student_id
    elif by == 'date':
        return record.enroll_date
    else:
        raise ValueError("Invalid sorting key")
   
