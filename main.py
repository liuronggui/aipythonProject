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
mail_user = os.getenv("MAIL_USER", "2030576660@qq.com")
# 建议用环境变量提供授权码，避免把敏感信息写进代码仓库：
# Windows PowerShell:
#   $env:MAIL_PASS="你的QQ邮箱SMTP授权码"
mail_pass = os.getenv("MAIL_PASS", "")

# 每天定时发送的时间（本机时间，24小时制），例如 "09:00" / "21:30"
send_time = os.getenv("SEND_TIME", "14:15")

sender = mail_user
to_list = ["1224472501@qq.com"]
cc_list = ["liuronggui001@gmail.com"]
bcc_list = ["liuronggui0001@gmail.com"]


def send_mail():
    subject = "测试嵌入图片和文本附件的HTML邮件"
    base_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(base_dir, "2.jpg")
    attachment_path = os.path.join(base_dir, "qq授权码")  # 文本附件路径

    html_content = """
    <h2>邮件正文嵌入图片和文本附件示例</h2>
    <p>下方是嵌入的图片：</p>
    <img src="cid:image1">
    """

    if not mail_pass:
        raise ValueError("请先设置环境变量 MAIL_PASS 为QQ邮箱SMTP授权码（PyCharm: Run/Debug Configurations -> Environment variables）。")

    message = MIMEMultipart()
    message["From"] = Header(sender)
    message["To"] = Header(", ".join(to_list))
    if cc_list:
        message["Cc"] = Header(", ".join(cc_list))
    message["Subject"] = Header(subject, "utf-8")

    # 添加HTML正文
    message.attach(MIMEText(html_content, "html", "utf-8"))

    # 添加图片
    if os.path.exists(image_path):
        with open(image_path, "rb") as f:
            img = MIMEImage(f.read())
            img.add_header("Content-ID", "<image1>")
            message.attach(img)
    else:
        print(f"未找到图片文件: {image_path}")

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
    else:
        print(f"未找到附件文件: {attachment_path}")

    all_recipients = to_list + cc_list + bcc_list

    server = None
    sent_ok = False
    try:
        server = smtplib.SMTP_SSL(mail_host, mail_port, timeout=30)
        server.login(mail_user, mail_pass)
        server.sendmail(sender, all_recipients, message.as_string())
        sent_ok = True
        print("邮件发送成功")
    except Exception as e:
        print("邮件发送失败:", e)
    finally:
        if server is not None:
            # 一些服务器会在 QUIT/关闭连接阶段直接断开，导致抛异常（但邮件已发送成功）。
            # 这里忽略关闭阶段异常，避免“发送成功却显示失败”。
            try:
                server.quit()
            except Exception:
                try:
                    server.close()
                except Exception:
                    pass


schedule.every().day.at(send_time).do(send_mail)

if __name__ == '__main__':
    print(f"已启动：每天 {send_time} 定时发送邮件（本机时间）。按 Ctrl+C 退出。")
    while True:
        schedule.run_pending()
        time.sleep(1)
