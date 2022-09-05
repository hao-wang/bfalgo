"""有一群人，打乒乓球比赛，两两捉对撕杀，每两个人之间最多打一场比赛。
球赛的规则如下：
如果A打败了B，B又打败了C，而A与C之间没有进行过比赛，那么就认定，A一定能打败C。
如果A打败了B，B又打败了C，而且，C又打败了A，那么A、B、C三者都不可能成为冠军。
根据这个规则，无需循环较量，或许就能确定冠军。你的任务就是面对一群比赛选手，在经过了若干场撕杀之后，
确定是否已经实际上产生了冠军。

Input
输入含有一些选手群，每群选手都以一个整数n(n<1000)开头，后跟n对选手的比赛结果，比赛结果以一对选手名字（中间
隔一空格）表示，前者战胜后者。如果n为0，则表示输入结束。
 
Output
对于每个选手群，若你判断出产生了冠军，则在一行中输出“Yes”，否则在一行中输出“No”。
 
Sample Input
3
Alice Bob
Smith John
Alice Smith
5
a c
c d
d e
b e
a d
0
 
Sample Output
Yes
No

Refs:
1. https://acm.hdu.edu.cn/showproblem.php?pid=2094
"""


def has_winner(matches):
    all = set()
    losers = set()
    for a, b in matches:
        all.add(a)
        all.add(b)
        losers.add(b)

    if len(all - losers) == 1:
        return True
    else:
        return False


if __name__ == "__main__":
    while True:
        n = int(input())
        if n == 0:
            break

        matches = []
        for _ in range(n):
            match = input().split()
            matches.append(match)

        if has_winner(matches):
            print("Yes")
        else:
            print("No")
