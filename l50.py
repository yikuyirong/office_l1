from PIL import Image, ImageDraw, ImageFont
import l51
import functools
import os
import l47

import uuid

total_width = 210 * 5
total_height = 297 * 5


def genQuestionPage(dir, index):
    cols = 4
    rows = 5

    title_font_size = 36
    question_font_size = 24
    # answer_font_size = 18

    # guid = uuid.uuid1()
    guid = ""

    image = Image.new("RGB", size=(total_width, total_height), color=(255, 255, 255))
    image_draw = ImageDraw.Draw(image)
    imagefont = functools.partial(ImageFont.truetype, font=r"c:\windows\fonts\simsun.ttc")

    # answer_font = imagefont(size=answer_font_size)
    # (answer_width, answer_height) = image_draw.textsize(text="test", font=answer_font)

    # 打印标题
    title = f"Page{index} {guid}"
    title_font = imagefont(size=title_font_size)
    (title_width, title_height) = image_draw.textsize(text=title, font=title_font)
    title_height = title_height + 10
    image_draw.text(xy=(total_width - title_width - 10, 10), text=title, fill=0, font=title_font)

    # 打印题目
    answer = []
    g = l51.getRandEquation()
    i = 1

    question_height = (total_height - title_height) / rows
    question_weight = total_width / cols

    for row in range(0, rows):
        for col in range(0, cols):
            (equ, result) = next(g)
            image_draw.text(
                xy=(col * question_weight + 10, row * question_height + title_height + 10),
                text=f"{i}、{equ}", fill=0,
                font=imagefont(size=question_font_size))

            answer.append("(%02d)%-6s" % (i, result))

            i = i + 1

    # 打印答案
    answer_line = [f"Page{index} {guid}"]

    # x_end = 0
    # while x_end < total_width:
    #     image_draw.line(xy=(x_end, total_height - answer_height * 5, x_end + 10, total_height - answer_height * 5), fill=0)
    #     x_end = x_end + 20
    #
    # image_draw.text(xy=(10, total_height - answer_height * 4), text=f"Page{index} {guid}", fill=0,font=answer_font)
    # image_draw.text(xy=(10, total_height - answer_height * 3), text=" ".join(answer[0:10]), fill=0, font=answer_font)
    # image_draw.text(xy=(10, total_height - answer_height * 2), text=" ".join(answer[10:20]), fill=0, font=answer_font)

    i = 0
    while i < len(answer):
        answer_line.append(" ".join(answer[i:i + 10]))
        i = i + 10

    image_file = os.path.join(dir, "%03d.jpg" % index)

    image.save(image_file, "JPEG")

    return (image_file, answer_line)


def genAnswerPage(dir, pagenum, answer_lines):
    image = Image.new("RGB", size=(total_width, total_height), color=(255, 255, 255))

    image_draw = ImageDraw.Draw(image)

    imagefont = ImageFont.truetype(font=r"c:\windows\fonts\simsun.ttc", size=18)

    (width, height) = image_draw.textsize("text", font=imagefont)

    i = 0
    for answer_line in answer_lines:

        for answer in answer_line:

            image_draw.text(xy=(10, i * height), text=answer, fill=0, font=imagefont)
            i = i + 1

        x_end = 0
        while x_end < total_width:
            image_draw.line(xy=(x_end, i * height + height / 2, x_end + 10, i * height + height / 2), fill=0)
            x_end = x_end + 20
        i = i + 1

    image_file = os.path.join(dir, "%03d.jpg" % pagenum)
    image.save(image_file, "JPEG")
    return image_file


def main():
    pagenum = input("输入需要生成的页数：")

    dir = input("输入生成文件位置：")

    if not os.path.isdir(dir):
        os.mkdir(dir)

    file_infos = [genQuestionPage(dir, i + 1) for i in range(0, int(pagenum))]

    files = list(map(lambda x: x[0], file_infos))

    answer_lines = list(map(lambda x: x[1], file_infos))

    # 生成答案页
    files.append(genAnswerPage(dir,int(pagenum) + 1, answer_lines))

    l47.gen_pdf(files, os.path.join(dir, "result.pdf"))


if __name__ == '__main__':
    main()
