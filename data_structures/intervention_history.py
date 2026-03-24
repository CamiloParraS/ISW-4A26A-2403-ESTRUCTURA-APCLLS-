""

from typing import Optional


class _Node:
    def __init__(self, data: str):
        self.data: str = data
        self.next: Optional["_Node"] = None


class InterventionHistory:

    def __init__(self):
        self._head: Optional[_Node] = None
        self._size: int = 0

    def append(self, procedure: str) -> None:
        node = _Node(procedure)
        if self._head is None:
            self._head = node
        else:
            current = self._head
            while current.next:
                current = current.next
            current.next = node
        self._size += 1

    def to_list(self) -> list[str]:
        result, current = [], self._head
        while current:
            result.append(current.data)
            current = current.next
        return result

    def size(self) -> int:
        return self._size
