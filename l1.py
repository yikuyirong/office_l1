# !usr/bin/env python3
# -*- coding: utf-8 -*-

def l2l(l):
    l1 = l[:]
    l2 = l[:]

    l1.append(0)
    l2.insert(0, 0)

    result = []

    i = 0
    while i <= len(l):
        result.append(l1[i] + l2[i])
        # print(i,result[i])
        i = i + 1

    return result[1:-1]

def t(max):

    index = 1

    tmp = []

    while index < max:

        if index == 1:
            tmp = [1]
            yield tmp
        else:
            tmp = l2l(tmp)
            tmp.append(1)
            tmp.insert(0,1)
            yield tmp
            pass

        index = index + 1

T = t(20)

for x in T:
    print(x)
