from typing import Any


class Node:
    def __init__(self, data: Any):
        self.data = data
        self.next = None
        self.prev = None

    def __eq__(self, other):
        return self.data == other.data


class LinkedList:
    def __init__(self, head: Node = None):
        self.head = head

    def __iter__(self):
        current = self.head
        while current is not None:
            yield current
            current = current.next

    def append(self, data: Any):
        node = Node(data)
        # if new list, set head
        # else, find the tail and append the new node to it
        if self.head is None:
            self.head = node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = node
            node.prev = current

    def remove(self, node):
        # if head (node.prev is None), prev=None
        # if tail (node.next is None), next=None
        # else
        prev_node = node.prev
        next_node = node.next
        if prev_node is None:
            self.head = next_node
        elif next_node is None:
            prev_node.next = None
        else:
            next_node.prev = prev_node
            prev_node.next = next_node

        # is it necessary?
        node = None

    def size(self):
        current = self.head
        count = 0
        while current is not None:
            count += 1
            current = current.next

        return count
