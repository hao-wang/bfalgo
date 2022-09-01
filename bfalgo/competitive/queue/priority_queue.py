"""Priority Queue
可以由堆实现，也可以由多种其他方法实现。
我们想要实现的是一个在优先级相同时，能够按照入队列的顺序排序的优先队列。

看病要排队这个是地球人都知道的常识。
不过经过细心的0068的观察，他发现了医院里排队还是有讲究的。0068所去的医院有三个医生（汗，这么少）同时看病。
而看病的人病情有轻重，所以不能根据简单的先来先服务的原则。所以医院对每种病情规定了10种不同的优先级。
级别为10的优先权最高，级别为1的优先权最低。医生在看病时，则会在他的队伍里面选择一个优先权最高的人进行诊治。
如果遇到两个优先权一样的病人的话，则选择最早来排队的病人。

现在就请你帮助医院模拟这个看病过程。

Ref:
1. HDU1873: https://acm.hdu.edu.cn/showproblem.php?pid=1873
"""
import heapq
import itertools

counter = itertools.count(start=1)


class HPriorityQueue:
    def __init__(self):
        self.pq = []

    def insert(self, priority):
        count = next(counter)
        entry = [-priority, count]
        heapq.heappush(self.pq, entry)

    def pop(self):
        try:
            _, count = heapq.heappop(self.pq)
            print(count)
        except Exception as e:
            print("EMPTY")

    def peek(self):
        pass


if __name__ == "__main__":
    qu = [HPriorityQueue() for _ in range(3)]
    N = int(input())
    for i in range(N):
        record = input().split()
        if len(record) == 2:
            direction = "OUT"
            doc_num = int(record[1])
            qu[doc_num].pop()
        else:
            direction = "IN"
            doc_num = int(record[1])
            priority = int(record[2])
            qu[doc_num].insert(priority)
