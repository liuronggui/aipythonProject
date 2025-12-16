import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email.header import Header
from email import encoders
import schedule
import time
import os

mail_host = "smtp.qq.com"
mail_port = 465
mail_user = "2030576660@qq.com"
mail_pass = "jjpzzcrgwxlwdcfe"

sender = mail_user
to_list = ["1224472501@qq.com"]
cc_list = ["liuronggui001@gmail.com"]
bcc_list = ["liuronggui0001@gmail.com"]


def send_mail():
    subject = "测试嵌入图片和文本附件的HTML邮件"
    image_path = "2.jpg"
    attachment_path = "qq授权码"  # 文本附件路径

    html_content = """
    <h2>邮件正文嵌入图片和文本附件示例</h2>
    <p>下方是嵌入的图片：</p>
    <img src="cid:image1">
    """

    message = MIMEMultipart()
    message["From"] = Header(sender)
    message["To"] = Header(", ".join(to_list))
    message["Subject"] = Header(subject, "utf-8")

    # 添加HTML正文
    message.attach(MIMEText(html_content, "html", "utf-8"))

    # 添加图片
    if os.path.exists(image_path):
        with open(image_path, "rb") as f:
            img = MIMEImage(f.read())
            img.add_header("Content-ID", "<image1>")
            message.attach(img)

    # 添加文本附件
    if os.path.exists(attachment_path):
        with open(attachment_path, "rb") as f:
            mime = MIMEBase("application", "octet-stream")
            mime.set_payload(f.read())
            encoders.encode_base64(mime)
            mime.add_header(
                "Content-Disposition",
                "attachment",
                filename=("utf-8", "", os.path.basename(attachment_path))
            )
            message.attach(mime)

    all_recipients = to_list + cc_list + bcc_list

    try:
        with smtplib.SMTP_SSL(mail_host, mail_port) as server:
            server.login(mail_user, mail_pass)
            server.sendmail(sender, all_recipients, message.as_string())
            print("邮件发送成功")
    except Exception as e:
        print("邮件发送失败:", e)


schedule.every(1).minutes.do(send_mail)

if __name__ == '__main__':
    while True:
        schedule.run_pending()
        time.sleep(1)
