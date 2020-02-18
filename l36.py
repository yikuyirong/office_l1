import re

str = "http://www.read-htm-tid-1917391.png"

str = "/cn/res/201912/30/20191230_4662126_S12500G-AF数据中心智能核心交换机_1256049_30003_0.jpg"

print(re.search(r"[^/]+.jpg$",str).group())





