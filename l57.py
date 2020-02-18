from PIL import Image
import io

import hashlib



def main():
    with io.BytesIO() as bytes:
        Image.new("RGB", (100, 100), "green").save(bytes, "JPEG")

        md5 = hashlib.md5()



        md5.update(bytes.getvalue())
        value = md5.hexdigest()
        print(value)

        print("你好".encode(encoding="utf-8").decode(encoding="utf-8"))


if __name__ == '__main__':
    main()
