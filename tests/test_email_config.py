import smtplib
import configparser
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import ssl

print("脚本开始执行")

# 读取配置文件
config = configparser.ConfigParser()
config.read('config.ini', encoding='utf-8')  # 明确指定使用UTF-8编码
print("配置文件已读取")

# 获取邮件配置
smtp_server = config['SMTP']['server']
smtp_port = config['SMTP']['port']
smtp_username = config['SMTP']['username']
smtp_password = config['SMTP']['password']
sender_email = config['SMTP']['sender_email']  # 使用SMTP用户名作为发件人邮箱
print(f"SMTP配置: 服务器={smtp_server}, 端口={smtp_port}, 用户名={smtp_username}")

# 创建测试邮件
receiver_email = "903773589@qq.com"  # 替换为您的测试接收邮箱
message = MIMEMultipart()
message["From"] = sender_email
message["To"] = receiver_email
message["Subject"] = "测试邮件服务器配置"
body = "这是一封测试邮件,用于验证邮件服务器配置是否正确。"
message.attach(MIMEText(body, "plain"))
print("测试邮件已创建")

try:
    print("尝试连接SMTP服务器...")
    # 创建SSL上下文
    context = ssl.create_default_context()
    
    with smtplib.SMTP_SSL(smtp_server, int(smtp_port), context=context) as server:
        print("已连接到SMTP服务器，尝试登录...")
        server.set_debuglevel(1)  # 启用调试模式
        server.login(smtp_username, smtp_password)
        print("登录成功，尝试发送邮件...")
        server.sendmail(sender_email, receiver_email, message.as_string())
        print("邮件已发送到服务器队列")
        # 不发送 QUIT 命令，直接关闭连接
        server.close()
    print("测试邮件发送成功!")
except smtplib.SMTPAuthenticationError:
    print("认证失败，请检查用户名和密码")
except smtplib.SMTPException as e:
    print(f"SMTP错误: {e}")
except ssl.SSLError as e:
    print(f"SSL错误: {e}")
except Exception as e:
    print(f"发送邮件时出错: {e}")

print("脚本执行结束")