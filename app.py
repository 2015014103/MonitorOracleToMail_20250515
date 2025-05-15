from flask import Flask, render_template, request, jsonify, send_from_directory
import smtplib
import configparser
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import ssl
from flask_cors import CORS
import os
import logging
import sys

# 设置更详细的日志记录
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

logger.info("Starting application initialization...")

# 读取配置文件
config = configparser.ConfigParser()

# 获取脚本所在目录（考虑PyInstaller打包情况）
if getattr(sys, 'frozen', False):
    # 如果是打包后的EXE
    application_path = os.path.dirname(sys.executable)
    config_path = os.path.join(application_path, 'config.ini')
    
    # 如果外部没有配置文件，则尝试从打包资源中获取
    if not os.path.exists(config_path):
        bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
        config_path = os.path.join(bundle_dir, 'config.ini')
else:
    # 普通Python脚本运行
    config_path = 'config.ini'

logger.info(f"Attempting to read config file from: {os.path.abspath(config_path)}")
config.read(config_path, encoding='utf-8')

# 获取邮件配置
smtp_server = os.environ.get('SMTP_SERVER') or config['SMTP']['server']
smtp_port = int(os.environ.get('SMTP_PORT') or config['SMTP']['port'])
smtp_username = os.environ.get('SMTP_USERNAME') or config['SMTP']['username']
smtp_password = os.environ.get('SMTP_PASSWORD') or config['SMTP']['password']
sender_email = os.environ.get('SENDER_EMAIL') or config['SMTP']['sender_email']

logger.info(f"Configuration loaded successfully")
logger.debug(f"SMTP Server: {smtp_server}")
logger.debug(f"SMTP Port: {smtp_port}")
logger.debug(f"Username: {smtp_username}")

@app.route('/')
def serve_html():
    return send_from_directory('.', 'index.html')

@app.route('/send_email', methods=['POST'])
def send_email():
    try:
        receiver_email = request.form['receiver_email']
        subject = request.form['subject']
        body = request.form['body']

        logging.debug(f"SMTP Server: {smtp_server}")
        logging.debug(f"SMTP Port: {smtp_port}")
        logging.debug(f"SMTP Username: {smtp_username}")
        logging.debug(f"Sender Email: {sender_email}")

        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))

        logging.info(f"Connecting to SMTP server: {smtp_server}:{smtp_port}")
        
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        
        logging.debug(f"Attempting to connect to {smtp_server}:{smtp_port}")
        if smtp_port == 465:
            # Use SSL
            logging.debug("Using SSL connection")
            with smtplib.SMTP_SSL(smtp_server, smtp_port, context=context) as server:
                logging.debug("SSL connection established")
                server.login(smtp_username, smtp_password)
                logging.debug("Login successful")
                server.sendmail(sender_email, receiver_email, message.as_string())
                logging.debug("Email sent successfully")
        else:
            # Use TLS
            logging.debug("Using TLS connection")
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.set_debuglevel(1)
                logging.debug("Connection established")
                server.ehlo()
                if server.has_extn('STARTTLS'):
                    logging.debug("STARTTLS supported, initiating")
                    server.starttls(context=context)
                    server.ehlo()
                else:
                    logging.warning("STARTTLS not supported by the server")
                server.login(smtp_username, smtp_password)
                logging.debug("Login successful")
                server.sendmail(sender_email, receiver_email, message.as_string())
                logging.debug("Email sent successfully")
        
        logging.info("Email sent successfully")
        return jsonify({'message': '邮件发送成功!', 'category': 'success'}), 200
    except smtplib.SMTPAuthenticationError as e:
        logging.error(f"Authentication failed: {str(e)}")
        return jsonify({'message': '认证失败，请检查用户名和密码', 'category': 'error'}), 400
    except Exception as e:
        if str(e) == "(-1, b'\\x00\\x00\\x00')":
            logging.warning("Received unexpected response from server, but email likely sent successfully")
            return jsonify({'message': '邮件可能已成功发送', 'category': 'success'}), 200
        logging.error(f"Unexpected error: {str(e)}", exc_info=True)
        return jsonify({'message': '发送邮件时出错，请稍后重试', 'category': 'error'}), 500

if __name__ == '__main__':
    try:
        logger.info("Starting Flask application...")
        print("="*50)
        print("Application is starting...")
        print("URL: http://localhost:8080")
        print("Press CTRL+C to quit")
        print("="*50)
        app.run(debug=True, host='0.0.0.0', port=8080, use_reloader=False)
    except Exception as e:
        logger.error(f"Failed to start application: {str(e)}")
        print(f"Error starting application: {str(e)}")
        print("="*50)
        print("Debug information:")
        print(f"Current working directory: {os.getcwd()}")
        print(f"Python version: {sys.version}")
        print("="*50)