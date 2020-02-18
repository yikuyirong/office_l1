import pdfkit
import os


path_wk = r"C:\Program Files (x86)\wkhtmltopdf\bin\wkhtmltopdf.exe"

file = os.path.join(r"D:\Projects\Python3\Lesson\L1\Chineses","001.jpg")

print(file)

options = {"encoding":"cp936","page-size":"A4"}
config = pdfkit.configuration(wkhtmltopdf=path_wk)

with open(file,"r") as f:

    print(f)

    result = pdfkit.from_file(f.name,"abcd.pdf",options=options,configuration=config)

    print(result)