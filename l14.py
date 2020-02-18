
import base64

from PIL import Image
from PIL.ImageFile import ImageFile


path = "D:\download\MM\8349635\蕾丝兔宝宝2\TMP-编号-2012-03B-3B-38.jpg"

image:ImageFile = Image.open(path)

image = image.rotate(180)

image.show()



