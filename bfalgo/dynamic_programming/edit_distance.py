"""
Edit distance with both brute-force recursion and dynamic programming (and the latter
is much faster).
"""
import numpy as np
from time import perf_counter


def hemming_binary(c1: str, c2: str) -> bool:
    """Helper function to compare two characters. Hemming distance is defined between two
    strings of the same length, hence the name.

    Args:
        c1 ([type]): [description]
        c2 ([type]): [description]

    Returns:
        [type]: [description]
    """
    if c1 == c2:
        return 0
    else:
        return 1


def edit_distance_recursion(S: str, T: str) -> int:
    """Edit distance in brute-force recursion.

    Edit distance has different meanings (https://en.wikipedia.org/wiki/Edit_distance), we
    use the Levenshtein distance.

    Source / target is named arbitrarily to differentiate the two strings; it doesn't
    matter which is which.

    Args:
        S (str): "source" string
        T (str): "target" string

    Returns:
        int: edit distance
    """
    if len(S) == 0:
        return len(T)
    if len(T) == 0:
        return len(S)
    return (
        min(
            [
                edit_distance_recursion(S[:-1], T),
                edit_distance_recursion(S, T[:-1]),
                edit_distance_recursion(S[:-1], T[:-1]),
            ]
        )
        + hemming_binary(S[-1], T[-1])
    )


def edit_distance_dp(S: str, T: str) -> int:
    """Edit distance algorithm implemented with dynamic programming.

    Args:
        S : "source" string
        T : "target" string

    Returns:
        edit distance
    """
    dp_matrix = np.zeros((len(S) + 1, len(T) + 1))
    dp_matrix[0, :] = list(range(len(T) + 1))
    dp_matrix[:, 0] = list(range(len(S) + 1))
    for i in range(1, len(S) + 1):
        for j in range(1, len(T) + 1):
            dp_matrix[i, j] = min(
                [dp_matrix[i - 1, j], dp_matrix[i, j - 1], dp_matrix[i - 1, j - 1]]
            ) + hemming_binary(S[i - 1], T[j - 1])
    return dp_matrix[len(S), len(T)]
