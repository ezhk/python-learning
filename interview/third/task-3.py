#!/usr/bin/env python3

"""
3. Создать два списка с различным количеством элементов.
В первом должны быть записаны ключи, во втором — значения.
Необходимо написать функцию, создающую из данных ключей и значений словарь.
Если ключу не хватает значения,
в словаре для него должно сохраняться значение None.
Значения, которым не хватило ключей, необходимо отбросить.

$ ./task-3.py
{1: 'a', 2: 'b', 3: 'c', 4: None, 5: None}
"""


def get_zipped_dict(l_list, r_list):
    len_diff = len(l_list) - len(r_list)
    if len_diff > 0:
        r_list.extend([None] * len_diff)

    return {k: v for k, v in zip(l_list, r_list)}


if __name__ == "__main__":
    LEFT_LIST = [1, 2, 3, 4, 5]
    RIGHT_LIST = ["a", "b", "c"]

    print(get_zipped_dict(LEFT_LIST, RIGHT_LIST))
