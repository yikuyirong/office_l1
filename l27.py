
import re

# str = "神似女明星MaggieQ的網紅混血美女淫蕩國語自述幻想與男人肉棒啪啪 呻吟高潮白漿直流 擼管必備 "
#
# str = "神似女明星的網紅混血美女淫蕩國語自述幻想與男人肉棒啪啪 呻吟高潮白漿直流 擼管必備 "
#
# result = re.match("[a-zA-Z\u4E00-\u9FA5\s]+",str)
#

# href = re.match("[a-zA-Z\u4E00-\u9FA5\s]+",str)

# pattern = "read-htm-tid-\d+(-fpage-\d+)?.html"
pattern = "read"

href = "http://av.avlang4.co/read-htm-tid-1909132-fpage-6.html"

result = re.search(pattern, href)

print(result)
