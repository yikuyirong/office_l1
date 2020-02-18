from datetime import datetime

import collections

c = dir(collections)

print(c)

print((filter(lambda r: not r.startswith("_"), c)))

l = [1,2,3,4]

print(list(filter(lambda r:r>1,l)))
