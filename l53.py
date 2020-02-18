
from PIL import Image
import os
import cv2


def main():

    try:

        video_dir = "Video"

        if not os.path.isdir(video_dir):
            os.mkdir(video_dir)


        images_dir = "avlang-fid-9-images"

        video_size = (1920,1080)

        #videowriter = cv2.VideoWriter(os.path.join(video_dir,f"{images_dir}.mp4"),cv2.VideoWriter_fourcc(*"x264"),1,video_size)
        videowriter = cv2.VideoWriter(os.path.join(video_dir,f"{images_dir}.mp4"),0x00000021,1,video_size)

        for imagefile in sorted(os.listdir(images_dir)):
            try:
                filename = os.path.join(images_dir,imagefile)
                image = cv2.imread(os.path.join(images_dir,imagefile))
                videowriter.write(image)
                print(f"添加文件成功{filename}")
            except BaseException as e:
                print(f"\033[1;31m添加文件失败\033[0m{filename}")

        videowriter.release()

    except Exception as e:

        print(f"\033[1;31m{str(e)}\033[0m")



if __name__ == '__main__':
    main()
