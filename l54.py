
from PIL import Image,ImageFilter

def main():

    filename = r"avlang-fid-9-images\L.P.VISION作品：梦红尘 无圣光 [22P]-17.jpg"

    image = Image.open(filename)

    # t_img = image.convert("L")

    # t_img =image.filter(ImageFilter.BLUR)

    # (r,g,b) = image.split()

    # Image.blend(image,t_img,1).show()

    # t_img = Image.eval(image,lambda x: 255 - x)

    # print(t_img.getbbox())

    # datas = []
    #
    # for data in image.getdata():
    #     datas.append((0,data[1],0))
    #
    #
    # image.putdata(datas)

    image.resize().show()

    # image.show()

    # t_img.show()






    # with open(filename,"rb") as f:
    #     image = Image.open(f)
    #     image.show()



if __name__ == '__main__':
    main()