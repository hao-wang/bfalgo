使用regularization来避免不稳定性。Ridge regression引入的项，原本是为了解决共线性问题——两个参数如果线性相关，似然函数就会存在一个长长的“谷”（增加p1的同时也增加p2，似然函数可以保持不变）。对拟合结果没啥影响，但对于确定参数有影响。

Compare y as 0-9, to that of one-hot encoded.