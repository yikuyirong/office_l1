
#!usr/bin/env python3

# -*- encoding: utf-8 -*-

from functools import reduce

import math

def normalize(name):
    return str(name).lower().title()

L = ['adam','LISA','barT']

print(list( map(normalize,L) ))



def prod(L):

    def t(x,y):
        return x*y

    return reduce(t,L)

L = [3,5,7,9]

print(prod(L))


#'123.456' -> 123.456

# DS = {'0':,'1':,'2':,'':,'':,'':,'':,'':,'':,'':,}


def str2float(s):

    index = (len(s) - s.index(".") - 1)

    s = s.replace(".","")

    def t(x,y):

        print("x",x,"y",y)

        return int(x) * 10 + int(y)

    return reduce(t,s) / math.pow(10,index)




