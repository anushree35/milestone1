class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
    
class LinkedQueue:
    def __init__(self):
        self._head = None
        self._tail = None
        self._size = 0
    
    def enqueue(self, item):
        new_node = Node(item)
        if self._tail is None:
            self._head = new_node
            self._tail = new_node
        else:
            self._tail.next = new_node
            self._tail = new_node
        self._size += 1

    def dequeue(self):
        if self._head is None:
            raise ValueError("Can't dequeue from an empty list")
        item = self._head.data
        self._head = self._head.next
        if self._head is None:
            self._tail = None
        self._size -= 1
        return item
    
    def is_empty(self):
        return self._size == 0
    
    def __len__(self):
        return self._size
    
    def __repr__(self):
        items = []
        current = self._head
        while current is not None:
            items.append(repr(current.data))
            current = current.next
        return "LinkedQueue([" + ", ".join(items) + "])"

