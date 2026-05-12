from __future__ import annotations
from typing import Optional, Callable, Iterator


class Node:
    def __init__(self, key: str, value: int, next: Optional["Node"] = None) -> None:
        self.key = key
        self.value = value
        self.next = next


# ------------------------------------------------------------
# Hash functions 
# ------------------------------------------------------------

def hash_function1(table: "HashTable", key: str) -> int:
    return ord(key[0]) % table.size

def hash_function2(table: "HashTable", key: str) -> int:
    '''
    Task 2
    You are to create an updated hash function that does a better job of 
    removing collisions. Full points for getting the number of collisions
    down to 3, and partial points for 4. Currently it's the same as 
    hash_function1 and needs to be updated
    '''

    # OK wellllll it gets down to 2. Was I supposed to do that?
    assignment = ord(key[0])
    if key[1]:
        augment1 = ord(key[1])
    else:
        augment1 = 0

    if key[2]:
        augment2 = ord(key[2])
    else:
        augment2 = 0
    
    
    return (assignment + augment1 + augment2) % table.size

# ------------------------------------------------------------
# Hash Table Class
# ------------------------------------------------------------

class HashTable:
    def __init__(self, size: int) -> None:
        self.size = size
        self.total = 0
        self.buckets: list[Optional[Node]] = [None] * size

    # --------------------------------------------------------
    # Core operations
    # --------------------------------------------------------

    def add(self, key: str, value: int, hf: Callable[["HashTable", str], int]) -> None:
        index = hf(self, key)
        head = self.buckets[index]

        # Replace existing key
        current = head
        while current:
            if current.key == key:
                current.value = value
                return
            current = current.next

        # Insert new node at head
        new_node = Node(key, value, head)
        self.buckets[index] = new_node
        self.total += 1

    def remove(self, key: str, hf: Callable[["HashTable", str], int]) -> bool:
        ''' 
        Task 3
        Here you should implement a remove method that will find a particular 
        key/value pair stored in the hash table and remove it. It should consider
        the edge cases described in the readme file. This function should return 
        True if the element is found and deleted, and False if not found
        '''
        # edge cases: removing bucket head when needed TODO
        #               removing middle of bucket when needed TODO
        #               removing end of linked list bucket when needed TODO
        #               provided key not found

        # plan: use key hash algo to find right index, the iter till right key
        assignment = ord(key[0])
        aug1, aug2 = 0, 0
        if key[1]:
            aug1 = ord(key[1])
        if key[2]:
            aug2 = ord(key[2])

        index = (assignment + aug1 + aug2) % self.size

        if self.buckets[index] is None:
            return False

        current = self.buckets[index] # this is the head of a linked list

        while current.key != key:
            if current.next is None and current.key != key:
                return False # key not found in the bucket it should be in
            prev = current
            current = current.next

        # Milestone: current.key == key, we found the right item
        # it could be beginning, middle, or end
        if current.next == self.buckets[index]: # if it's the head
            if current.next is None:
                self.buckets[index] = None
            else:
                self.buckets[index] = current.next
        # if it is not the head, then prev is defined
        else:
            prev.next = current.next
            # this works if current is tail or middle
            # ASSUMING prev is actually the prev node and not a copy



    def get(self, key: str, hf: Callable[["HashTable", str], int]) -> Optional[int]:
        index = hf(self, key)
        current = self.buckets[index]
        while current:
            if current.key == key:
                return current.value
            current = current.next
        return None

    # --------------------------------------------------------
    # dunder methods for easy interface
    # --------------------------------------------------------

    def __setitem__(self, key: str, value: int) -> None:
        self.add(key, value, hash_function1)

    def __getitem__(self, key: str) -> int:
        value = self.get(key, hash_function1)
        if value is None:
            raise KeyError(key)
        return value

    def __delitem__(self, key: str) -> None:
        if not self.remove(key, hash_function1):
            raise KeyError(key)

    def __contains__(self, key: str) -> bool:
        return self.get(key, hash_function1) is not None

    def __iter__(self) -> Iterator[str]:
        for bucket in self.buckets:
            current = bucket
            while current:
                yield current.key
                current = current.next

    # --------------------------------------------------------
    # Utility methods
    # --------------------------------------------------------

    def reset(self) -> None:
        self.buckets = [None] * self.size
        self.total = 0

    def collisions(self) -> int:
        '''
        Task 1
        You are to update this collisions function to actually compute the 
        number of collisions in the hash table. 
        '''

        num = 0

        for bucket in self.buckets:
            if bucket:
                current = bucket
                while current.next:
                    num += 1
                    current = current.next

        return num

    def display(self) -> None:
        # print out the hash table in a readable format.
        # best not alter the display function as it is used in evaluating the output.
        print(f"HashTable(size={self.size}, total={self.total})")
        for i, bucket in enumerate(self.buckets):
            print(f"bucket[{i}]", end="")
            current = bucket
            if not current:
                print(" -|")
                continue
            while current:
                print(f" -> (key={current.key}, value={current.value})", end="")
                current = current.next
            print(" -|")
        print()
