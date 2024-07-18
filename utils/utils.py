import smtplib
from email.mime.text import MIMEText


class EmailManager:
    def __init__(self, smtp_address='smtp.qq.com', sendmail='productivitypro@foxmail.com', send_name='no_replay', smtp_pwd='', smtp_port=587):
        self.smtp_address = smtp_address
        self.sendmail = sendmail
        self.send_name = send_name
        self.smtp_pwd = smtp_pwd
        self.smtp_port = smtp_port

    def send_email(self, to_addr, subject, content):
        msg = MIMEText(content)
        msg['Subject'] = subject
        msg['From'] = self.send_name
        msg['To'] = to_addr

        server = smtplib.SMTP(self.smtp_address, self.smtp_port)
        server.starttls()
        server.login(self.sendmail, self.smtp_pwd)
        server.sendmail(self.sendmail, to_addr, msg.as_string())
        server.quit()


def test_email():
    emailM = EmailManager()
    # 使用示例：
    emailM.send_email('1257074159@qq.com', '每日报告提醒', '今日报告已生成，请查收。')


if __name__ == '__main__':
    test_email()