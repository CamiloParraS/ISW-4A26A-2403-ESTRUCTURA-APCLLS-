""

from typing import Any, Optional


class BedArray:

    def __init__(self, capacity: int = 15):
        self._beds: list[Any] = [None] * capacity
        self.capacity = capacity

    def assign(self, index: int, patient: Any) -> bool:
        if 0 <= index < self.capacity and self._beds[index] is None:
            self._beds[index] = patient
            return True
        return False

    def release(self, index: int) -> Optional[Any]:
        if 0 <= index < self.capacity and self._beds[index] is not None:
            patient = self._beds[index]
            self._beds[index] = None
            return patient
        return None

    def get(self, index: int) -> Optional[Any]:
        return self._beds[index] if 0 <= index < self.capacity else None

    def is_free(self, index: int) -> bool:
        return 0 <= index < self.capacity and self._beds[index] is None

    def all_beds(self) -> list:
        return list(self._beds)

    def free_count(self) -> int:
        return sum(1 for b in self._beds if b is None)

    def occupied_count(self) -> int:
        return self.capacity - self.free_count()

    def first_free_index(self) -> Optional[int]:
        for i, bed in enumerate(self._beds):
            if bed is None:
                return i
        return None
