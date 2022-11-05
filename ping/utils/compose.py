import operator
from functools import reduce
from typing import List, Any, Iterable
from itertools import product


def merge_alternatively(left: Iterable[Any], right: Iterable[Any]) -> List[Any]:
    '''.'''
    return list(
        reduce(
            operator.add,
            zip(left, right),
        )
    )


def join_list(left: Iterable[Any], right: Iterable[Any]) -> List[Any]:
    '''.'''
    return [f"{type}_{column}" for type, column in (product(left, right))]
