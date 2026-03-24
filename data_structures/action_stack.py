""

from typing import Any, Optional


class ActionStack:

    def __init__(self):
        self._items: list = []

    def push(self, item: Any) -> None:
        self._items.append(item)

    def pop(self) -> Optional[Any]:
        return self._items.pop() if self._items else None

    def peek(self) -> Optional[Any]:
        return self._items[-1] if self._items else None

    def is_empty(self) -> bool:
        return len(self._items) == 0

    def size(self) -> int:
        return len(self._items)

    def to_list(self) -> list:
        return list(reversed(self._items))
