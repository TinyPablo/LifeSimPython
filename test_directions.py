import pytest
import math
import random
from direction import Direction
from direction_check import get_relative_direction, get_relative_direction_old


def test_relative_direction_equivalence():
    """Porównuje wyniki metod old i new dla wszystkich możliwych par kierunków."""
    all_dirs = list(Direction)

    for current in all_dirs:
        for rel in all_dirs:
            old_result = get_relative_direction_old(current, rel)
            new_result = get_relative_direction(current, rel)
            assert (
                old_result == new_result
            ), f"Błąd dla ({current}, {rel}): old={old_result}, new={new_result}"


def test_randomized_direction_equivalence():
    """Testuje losowo 100 par kierunków z Direction.random()"""
    for _ in range(100):
        current = Direction.random()
        rel = Direction.random()
        old_result = get_relative_direction_old(current, rel)
        new_result = get_relative_direction(current, rel)
        assert (
            old_result == new_result
        ), f"Niezgodność przy losowej parze: {current}, {rel}"


def test_direction_mod_index_safety():
    """Sprawdza czy obliczenia kątów nie wychodzą poza dopuszczalny zakres (mod 2π)."""
    dirs = list(Direction)
    for _ in range(100):
        current = Direction.random()
        rel = Direction.random()
        # kąt wynikowy
        angle = math.atan2(current.value[1], current.value[0]) + math.atan2(rel.value[1], rel.value[0])
        # testuje, że po mod 2π kąt jest w zakresie [0, 2π)
        mod_angle = angle % (2 * math.pi)
        assert 0 <= mod_angle < 2 * math.pi, f"Kąt poza zakresem: {mod_angle}"


def test_direction_random_returns_enum():
    """Sprawdza, że Direction.random() zwraca poprawny element Direction."""
    for _ in range(50):
        d = Direction.random()
        assert isinstance(d, Direction), f"Zwrócono nie-Enum: {d}"
