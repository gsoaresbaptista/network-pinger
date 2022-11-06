import operator
from functools import reduce
from typing import List, Any, Iterable
from itertools import product


def merge_alternatively(left: Iterable[Any], right: Iterable[Any]) -> List[Any]:
    '''Merge two lists alternatively.

    Example:
        - list_1 = [0, 1, 2, 3, 4]
        - list_2 = [5, 6, 7, 8, 9]
        - result = [0, 5, 1, 6, 2, 7, 3, 8, 4, 9]
    :param left - list[Any], first list to merge
    :param right - list[Any], second list to merge
    :return list[Any], merged list
    '''
    return list(
        reduce(
            operator.add,
            zip(left, right),
        )
    )


def join_list(left: Iterable[Any], right: Iterable[Any]) -> List[Any]:
    '''Join elements from two lists, Used to construct csv file columns.

    Example:
        - list_1 = [0, 1, 2, 3, 4]
        - list_2 = [5, 6, 7, 8, 9]
        - result = [0_5, 1_6, 2_7, 3_8, 4_9]
    :param left - list[Any], first list to join
    :param right - list[Any], second list to join
    :return list[Any], joined list
    '''
    return [f"{type}_{column}" for type, column in (product(left, right))]
