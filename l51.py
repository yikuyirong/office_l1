import random


def getRandEquation():

    chufa_count = 0

    while True:
        x = random.randint(2, 10)
        y = random.randint(10, 999)
        z = random.randint(0, x - 1)

        if random.randint(1,8) == 4: #生成乘法算式
            if chufa_count > 3:
                chufa_count = 0
                yield (f"{y}×{x}=", f"{x*y}")

        else: #生成除法算式
            result = x * y + z
            if result > 100 and result < 1000:
                chufa_count = chufa_count + 1
                yield (f"{result}÷{x}=", f"{y}..{z}" if z != 0 else f"{y}")


if __name__ == '__main__':
    g = getRandEquation()
    print(next(g))
