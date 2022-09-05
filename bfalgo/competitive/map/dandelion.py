""" Every girl likes shopping,so does dandelion.Now she finds the shop is increasing the 
price every day because the Spring Festival is coming .She is fond of a shop which is 
called "memory". Now she wants to know the rank of this shop's price after the change of 
everyday.
 
Input
One line contains a number n ( n<=10000),stands for the number of shops.
Then n lines ,each line contains a string (the length is short than 31 and only contains 
lowercase letters and capital letters.)stands for the name of the shop.
Then a line contains a number m (1<=m<=50),stands for the days .
Then m parts, every parts contains n lines , each line contains a number s and a string p,
stands for this day, the shop p's price has increased s.
 

Output
Contains m lines ,In the ith line print a number of the shop "memory" 's rank after the 
i-th day. We define the rank as "if there are t shops' price is higher than the "memory", 
then its rank is t+1.
 
Sample Input
3
memory
kfc
wind
2
49 memory
49 kfc
48 wind
80 kfc
85 wind
83 memory
 
Sample Output
1
2

Refs:
1. https://acm.hdu.edu.cn/showproblem.php?pid=2648
"""
from collections import defaultdict


def shopping():
    n = int(input())
    for _ in range(n):
        input()

    m = int(input())
    prices = defaultdict(int)
    for _ in range(m):
        for _ in range(n):
            rise, shop = input().split()
            rise = int(rise)
            prices[shop] += rise

        rank = 1
        for pr in prices.items():
            if pr[1] > prices['memory']:
                rank += 1

        print(rank)


if __name__ == "__main__":
    shopping()
