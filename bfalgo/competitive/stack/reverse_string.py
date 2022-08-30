"""输入Hello world, 输出!dlrow olleH"""


def reverse(input: str):
    input_list = list(input)
    output = []
    for _ in range(len(input)):
        output.append(input_list.pop())

    return ''.join(output)


if __name__ == "__main__":
    out = reverse("Hello world!")
    print(out)
