from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import os
from time import sleep
import l47
from PIL import Image
import re

dir = "百度文库"


def fetch_baiduwenku(url):

    browser = None
    try:

        if not re.match(r"^https://wenku.baidu.com/view/[0-9a-z]{24,}\.html", url):
            raise Exception(f"{url}不是合法的百度文库URL")

        browser = webdriver.Firefox(executable_path=r"C:\Program Files\Mozilla Firefox\geckodriver.exe")
        # browser = webdriver.Chrome(executable_path=r"C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe")

        browser.get(url)

        sleep(2)

        title = "Title"

        try:
            ele = browser.find_element_by_class_name("doc-header-title")

            title = ele.text

        except:
            pass

        # 去除广告
        try:
            eles = browser.find_elements_by_class_name("fix-searchbar-wrap")

            for ele in eles:
                browser.execute_script("arguments[0].style.visibility='hidden'", ele)

        except NoSuchElementException:
            print("1")
            pass

        # 去除共享标签
        try:
            eles = browser.find_elements_by_xpath(r"//div[starts-with(@class,'doc-tag')]")
            for ele in eles:
                # pass
                browser.execute_script("arguments[0].style.visibility='hidden'", ele)
        except NoSuchElementException:
            print("2")
            pass

        # # 去除共享标签
        # try:
        #     ele = browser.find_element_by_xpath(r"//div[@class='doc-tag-wrap super-vip fixed']")
        #     if ele:
        #         browser.execute_script("arguments[0].style.visibility='hidden'", ele)
        # except NoSuchElementException:
        #     pass

        # 去除工具栏
        try:
            eles = browser.find_elements_by_xpath(r"//div[starts-with(@class,'reader-tools-bar')]")

            for ele in eles:
                browser.execute_script("arguments[0].style.visibility='hidden'", ele)
        except NoSuchElementException:
            pass

        # 去除全屏按钮
        try:
            ele = browser.find_element_by_xpath(
                r"//a[@class='ic reader-fullScreen xllDownloadLayerHit_left top-right-fullScreen']")
            if ele:
                browser.execute_script("arguments[0].style.visibility='hidden'", ele)
        except NoSuchElementException:
            print("4")
            pass

        try:
            xpath = r"//span[@class='moreBtn goBtn']"

            gobutton = browser.find_element_by_xpath(xpath)

            if gobutton:
                browser.execute_script("arguments[0].scrollIntoView();", gobutton)
                browser.execute_script('window.scrollBy(0,-200)')
                gobutton.click()

        except NoSuchElementException:
            pass

        xpath = r"//div[contains(@class,'reader-page')]"

        pages = browser.find_elements_by_xpath(xpath)

        if len(pages):
            if not os.path.isdir(dir):
                os.mkdir(dir)

            files = []

            browser.execute_script('window.scrollBy(0,-100000)')
            sleep(1)

            for (index, page) in enumerate(pages):
                browser.execute_script("arguments[0].scrollIntoView();", page)
                sleep(1)

                file = os.path.join(dir, f"{index}.png")
                page.screenshot(file)

                with Image.open(file) as image:
                    image = image.convert("RGB")
                    image.save(f"{file}.jpg", "JPEG")

                os.remove(file)

                files.append(f"{file}.jpg")

            file_pdf = os.path.join(dir, f"{title}.pdf")

            l47.gen_pdf(files, file_pdf)

            for file in files:
                os.remove(file)

            return file_pdf

        else:
            raise Exception("未切出有效的图片")

    except BaseException as e:
        raise e
    finally:
        try:
            browser.close()
        except:
            pass


def main():

    url = input("请输入要下载的文库链接：")

    try:
        file_pdf = fetch_baiduwenku(url)
        os.startfile(file_pdf)
    except BaseException as e:
        print(f"\033[1;31m{str(e)}\033[0m")
        pass




if __name__ == '__main__':
    main()
