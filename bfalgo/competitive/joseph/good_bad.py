"""圆桌旁围坐着2n个人。其中n个人是好人，另外n个人是坏人。从第一个人开始数，数到第m个人，赶走该人。
然后从下一个人开始数，再将第m个人赶走。依次进行。
预先应该如何安排好人和坏人的座位，才能使得赶走n个人后，剩下的n个人都是好人？

输入：多组数据，每组n,m<32767
输出：对每组数据，输出2n个大写字母，GB分别表示好人和坏人，50个字母为一行，不允许出现空白。
[罗勇军：算法竞赛入门到进阶]
"""


def get_seats(n: int, m: int) -> str:
    seat_numbers = [i for i in range(2 * n)]
    pos = 0
    total = 2 * n
    for _ in range(n):
        pos += m - 1
        pos = pos % total
        seat_numbers.pop(pos)
        total -= 1
        print(seat_numbers, pos, total)

    seats = ['B'] * 2 * n
    for ind in seat_numbers:
        seats[ind] = 'G'

    return ''.join(seats)


if __name__ == "__main__":
    n, m = [int(a) for a in input("n, m=").split()]
    seats = get_seats(n, m)
    print(seats)
