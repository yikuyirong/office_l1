
import re

content = '''映门淮水绿，留骑主人心。
明月随良掾，春潮夜夜深。'''

# imgs_name = "".join(re.findall(r'[^*"/:?\\|<>]', a.text, re.S))

result = "_".join(re.findall(r'[^，。\s]+', content, re.S))

print(result)

