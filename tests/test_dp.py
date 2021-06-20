from bfalgo.dynamic_programming import edit_distance
import pytest
from time import perf_counter


class TestEditDistance:
    @pytest.mark.parametrize(
        'S, T, result',
        [
            ('a', 'b', 1),
            ('a', 'ab', 1),
            ('a', 'abc', 2),
            ('abc', 'a', 2),
            ('abc', 'c', 2),
            ('ab', 'bcd', 3),
            ('abcde', 'adef', 3),
            ('adefghik', 'abcdehg', 6),
        ],
    )
    def test_edit_distance(self, S, T, result):
        t1 = perf_counter()
        for i in range(10):
            edit_distance.edit_distance_recursion(S, T)
        t2 = perf_counter()
        t_br = t2 - t1

        t1 = perf_counter()
        for i in range(10):
            edit_distance.edit_distance_dp(S, T)
        t2 = perf_counter()
        t_dp = t2 - t1

        # DP is more advantageous for long strings.
        if len(S) > 1 and len(T) > 1:
            assert t_dp < t_br
        else:
            assert t_dp > t_br

        # d(S, T) == d(T, S)
        assert edit_distance.edit_distance_recursion(
            S, T
        ) == edit_distance.edit_distance_recursion(T, S)

        # d_br == d_dp
        assert edit_distance.edit_distance_recursion(
            S, T
        ) == edit_distance.edit_distance_dp(T, S)

        assert edit_distance.edit_distance_dp(S, T) == result
