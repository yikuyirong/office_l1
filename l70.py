import requests_async
import asyncio
import re
import json
import demjson
import os
import shutil
import rarfile
import zipfile

root_dir = "空中课堂"


async def fetch_datas(url):
    if not os.path.isdir(root_dir):
        os.mkdir(root_dir)

    # 清除所有临时数据
    for file in map(lambda f: os.path.join(root_dir, f), filter(lambda f: f.endswith("tmp"), os.listdir(root_dir))):
        if os.path.isfile(file):
            os.remove(file)

    resp = await requests_async.get(url=url)

    result = re.search(r"\[[.\s\S]*\]", resp.text).group()

    result = demjson.decode(result)

    return list(filter(lambda r: r["name1"] == "三年级" and r["name2"] in ["语文", "数学", "英语"], result))


def get_filename_from_url(url):
    d, f = os.path.splitext(re.split("/", url)[-1])
    return f"{d}{f[0:4]}"


async def download_item(index, item):
    # 确定下载目录
    path = os.path.join(root_dir, item["name2"])
    if not os.path.isdir(path):
        os.mkdir(path)

    tasks = []

    for i, url in enumerate([item["downloadurl"], item["looksrc"]]):
        ext = os.path.splitext(get_filename_from_url(url))[1]  # 文件扩展名
        filename = f"{item['name3']}_{item['name']}{ext}"  # 文件名
        tasks.append((f"{index}_{i}", item["name2"], filename, url))

    await asyncio.gather(*[download_file(v1, v2, v3, v4) for v1, v2, v3, v4 in tasks])


async def download_file(index, path, filename, url):
    # 视频已经存在就跳过

    tmp_filename = os.path.join(root_dir, f"{filename}.tmp")
    true_filename = os.path.join(root_dir, path, filename)

    if not os.path.isfile(true_filename):

        print(f"协程{index} 下载文件... {filename}")

        resp = await requests_async.get(url)

        await resp.close()

        if resp.status_code == 200:

            with open(tmp_filename, "wb") as file:
                file.write(resp.content)

            # 移至下载目录
            shutil.move(tmp_filename, true_filename)

            # 压缩文件直接解压,并删除压缩包
            dirname, extensionname = os.path.splitext(true_filename)

            if extensionname.upper() in [".RAR", ".ZIP"]:

                if not os.path.isdir(dirname):
                    os.mkdir(dirname)

                if extensionname.upper() == ".RAR":
                    with rarfile.RarFile(true_filename) as c:
                        c.extractall(dirname)
                else:
                    with zipfile.ZipFile(true_filename) as c:
                        for name in c.namelist():
                            c.extract(name, dirname)

                            # os.rename(os.path.join(dirname,name),os.path.join(dirname,name.encode("cp437").decode("gbk")))

                # os.remove(true_filename)

            print(f"协程{index} 下载成功 {true_filename}")

        else:
            resp.raise_for_status()


async def main():
    url = "http://db.jndjg.cn/course/getDate.js"

    print(f"获取数据 {url}")

    items = await fetch_datas(url)

    async def consumer(x):
        while len(items) > 0:
            await download_item(x, items.pop(0))

    await asyncio.gather(*[consumer(x) for x in range(0, 6)])


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
