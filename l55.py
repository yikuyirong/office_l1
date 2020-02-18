from flask import Flask, send_file
import io
import os
from PIL import Image

import l47
import l52

app = Flask(__name__)

dir = "百度文库"


@app.route("/<doc_key>")
def main(doc_key):
    try:

        url = rf"https://wenku.baidu.com/view/{doc_key}.html"

        filename = l52.fetch_baiduwenku(url)

        return send_file(filename, attachment_filename=filename)
    except BaseException as e:
        return f"发生错误 {str(e)}"
