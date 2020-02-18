import smtplib
import os
from email import encoders
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
from email.utils import formataddr, parseaddr
from PIL import Image
import io


def main():
    server = "smtp.126.com"

    login_name = "yikuyirong"
    login_password = "happy9001"

    from_mail = "yikuyirong@126.com"
    to_mail = "409001311@qq.com"
    # to_mail = "42010461@qq.com"

    msg = MIMEMultipart()
    msg["From"] = formataddr(("亦枯亦荣", from_mail))
    # msg["To"] = formataddr(("efg",to_mail))
    msg["Subject"] = Header("你好", "utf-8")

    def getImageBytes(image: Image):
        with io.BytesIO() as bytes:
            image.save(bytes, "JPEG")
            return bytes.getvalue()

    msg.attach(MIMEText("这是一封来自Python的邮件...", "plain", "utf-8"))

    image_part = MIMEImage(getImageBytes(Image.new("RGB", (100, 100), "green")))
    image_part.add_header("Content-Disposition", "attachment", filename="123.jpg")

    msg.attach(image_part)

    dir = "百度文库"

    for file in map(lambda f: os.path.join(dir, f), os.listdir(dir)):
        with open(file, "rb") as f:
            file_part = MIMEApplication(f.read())
            file_part.add_header("Content-Disposition", "attachment", filename=file)
            msg.attach(file_part)

    with smtplib.SMTP(server, 25) as smtp:
        smtp.set_debuglevel(1)
        smtp.login(login_name, login_password)
        smtp.sendmail(from_mail, to_mail, msg.as_string())

    print("Send mail success...")


if __name__ == '__main__':
    main()
