"""某部队进行新兵队列训练，将新兵从一开始按顺序依次编号，并排成一行横队，训练的规则如下：从头开始一至二报数，
凡报到二的出列，剩下的向小序号方向靠拢，再从头开始进行一至三报数，凡报到三的出列，剩下的向小序号方向靠拢，
继续从头开始进行一至二报数。。。，以后从头开始轮流进行一至二报数、一至三报数直到剩下的人数不超过三人为止。

Input: 本题有多个测试数据组，第一行为组数N，接着为N行新兵人数，新兵人数不超过5000。
Output: 共有N行，分别对应输入的新兵人数，每行输出剩下的新兵最初的编号，编号之间有一个空格。

Refs: 
1. https://acm.hdu.edu.cn/showproblem.php?pid=1276
"""
from linked_list import LinkedList

if __name__ == "__main__":
    t = int(input())
    for _ in range(t):
        N = int(input())
        ll = LinkedList()
        for i in range(N):
            ll.append(i)

        k = 2
        while ll.size() > 3:
            for cnt, node in enumerate(ll):
                if (cnt + 1) % k == 0:
                    # print(f"remove idx(k={k}): {cnt+1}")
                    ll.remove(node)

            if k == 2:
                k = 3
            else:
                k = 2

        remains = []
        for node in ll:
            remains.append(node.data)

        print(" ".join([str(n + 1) for n in remains]))
