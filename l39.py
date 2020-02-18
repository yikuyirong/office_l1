
import re

str = "1,1-2,7,8"

L = []

for v in  re.findall(r"[^,]+",str,re.S):
    if re.match(r"^\d+$",v):
        L.append(int(v))


    if re.match(r"^\d+-\d+$",v):
        (begin,end) = map(lambda x:int(x), re.split("-",v))
        while begin <= end:
            L.append(begin)
            begin = begin + 1

L = sorted(list(set(L)))

print(L)