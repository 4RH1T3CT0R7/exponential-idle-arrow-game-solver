#!/usr/bin/env python3
# solve_arrow_puzzle.py
# Универсальный решатель Vector Puzzle для easy, medium, hard и expert режимов.

import os
import sys
# Включаем папку скрипта в sys.path, чтобы находить easy.py, medium.py, hard.py, expert.py
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sympy import Matrix
from easy    import easy                 # Easy (3×3, mod 4)
from medium  import medium               # Medium (4×4, mod 4)
from hard    import hard  as hard_mod2   # Hard   (hex, mod 2)
from expert  import hard  as expert_mod6 # Expert (hex, mod 6)

# Длины столбцов для hex-режимов
COL_LENS = [4, 5, 6, 7, 6, 5, 4]
MAX_LEN = max(COL_LENS)

def read_numbers(total, min_val, max_val, mode_desc):
    """
    Считывает ровно total чисел в диапазоне [min_val..max_val].
    Поддерживает ввод слитно или через пробелы.
    mode_desc — описание (e.g. "столбцам слева→направо").
    """
    prompt = (f"Введите {total} чисел ({min_val}–{max_val}) по {mode_desc}:\n"
              + f"(слитно, например '222221212...', или через пробел '2 2 2 ...')\n")
    while True:
        s = input(prompt).strip()
        parts = s.split()
        if len(parts) == total:
            try:
                nums = [int(x) for x in parts]
            except ValueError:
                print("Все значения должны быть целыми.")
                continue
        elif len(s) == total and all(ch.isdigit() for ch in s):
            nums = [int(ch) for ch in s]
        else:
            count = len(parts) if len(parts) > 1 else len(s)
            print(f"Нужно ровно {total} чисел, а введено {count}. Попробуйте снова.")
            continue
        if any(n < min_val or n > max_val for n in nums):
            print(f"Числа должны быть в диапазоне {min_val}–{max_val}.")
            continue
        return nums


def solve_square(nums, solver, size):
    # Перевод 1..4 → 0..3
    B = Matrix([n-1 for n in nums])
    X = solver(B)
    taps = [int(x) for x in X]
    print("\nРешение — сколько раз нажать каждую клетку (строка, столбец → раз):")
    for idx, t in enumerate(taps):
        r, c = divmod(idx, size)
        print(f" ({r+1},{c+1}) → {t}")


def solve_hex(nums, solver, mod):
    # Перевод вводимых 1..mod → 0..mod-1
    B = Matrix([n-1 for n in nums])
    X = solver(B)
    taps = [int(x) for x in X]

    # Вычисляем вертикальные отступы для каждой колонки
    offsets = [(MAX_LEN - length) // 2 for length in COL_LENS]

    # Формируем матрицу строк для вывода
    print("\nРешение — количество нажатий (hex-раскладка):")
    for row in range(MAX_LEN):
        line_parts = []
        idx = 0
        for col, length in enumerate(COL_LENS):
            off = offsets[col]
            if off <= row < off + length:
                # позиция в столбце
                tap = taps[idx + (row - off)]
                line_parts.append(f"{tap}")
            else:
                line_parts.append(" ")
            idx += length
        # разделяем пробелом
        print(" ".join(line_parts))


def main():
    print("Выберите режим:")
    print(" 1) easy   — 3×3, 4 ориентации (1=↑,2=→,3=↓,4=←)")
    print(" 2) medium — 4×4, 4 ориентации (1=↑,2=→,3=↓,4=←)")
    print(" 3) hard   — шестиугольник, mod 2 (1=↑,2=↓), ввод по столбцам")
    print(" 4) expert — шестиугольник, mod 6 (1..6), ввод по столбцам")
    choice = input("Введите номер (1–4): ").strip()

    if choice == '1':
        nums = read_numbers(9,  1, 4, "строкам слева→направо, сверху↓вниз")
        solve_square(nums, easy,   size=3)
    elif choice == '2':
        nums = read_numbers(16, 1, 4, "строкам слева→направо, сверху↓вниз")
        solve_square(nums, medium, size=4)
    elif choice == '3':
        nums = read_numbers(sum(COL_LENS), 1, 2, "столбцам слева→направо, сверху↓вниз (длины 4,5,6,7,6,5,4)")
        solve_hex(nums, hard_mod2, mod=2)
    elif choice == '4':
        nums = read_numbers(sum(COL_LENS), 1, 6, "столбцам слева→направо, сверху↓вниз (длины 4,5,6,7,6,5,4)")
        solve_hex(nums, expert_mod6, mod=6)
    else:
        print("Неверный выбор, запустите снова и введите 1–4.")

if __name__ == '__main__':
    main()
