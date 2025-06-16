import cx_Oracle
import time
import configparser
import os
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import ssl
import sys
from logging.handlers import RotatingFileHandler

# 设置日志
def setup_logging():
    # 创建logs目录（如果不存在）
    log_dir = 'logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # 设置日志文件路径
    log_file = os.path.join(log_dir, 'oracle_monitor.log')
    
    # 创建日志处理器
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    
    # 设置日志格式
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    
    # 配置根日志记录器
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(file_handler)
    
    # 同时输出到控制台
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    return root_logger

logger = setup_logging()

def load_config():
    """加载配置文件"""
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
    
    # 读取配置文件
    try:
        config.read(config_path, encoding='utf-8')
        logger.info(f"已加载配置文件: {config_path}")
    except Exception as e:
        logger.error(f"读取配置文件失败: {str(e)}")
        raise
        
    return config

def connect_oracle(config):
    """连接Oracle数据库"""
    try:
        connection = cx_Oracle.connect(
            config['ORACLE']['username'],
            config['ORACLE']['password'],
            config['ORACLE']['dsn']
        )
        logger.info("成功连接到Oracle数据库")
        return connection
    except Exception as e:
        logger.error(f"连接数据库失败: {str(e)}")
        raise

def check_field_value(connection, table_name, field_name, condition_value):
    """检查指定表的字段值，并返回相关字段信息"""
    try:
        cursor = connection.cursor()
        # 修改查询，同时获取JOB_NAME和JOB_RESULT_LOG字段
        query = f"SELECT {field_name}, JOB_NAME, JOB_RESULT_LOG FROM {table_name} WHERE {field_name} = :value"
        cursor.execute(query, {'value': condition_value})
        results = cursor.fetchall()
        cursor.close()
        return results  # 返回满足条件的所有行
    except Exception as e:
        logger.error(f"查询数据失败: {str(e)}")
        raise

def send_email(config, subject, body, receiver_emails):
    """发送邮件
    
    Args:
        receiver_emails: 可以是单个邮箱字符串或多个邮箱组成的列表
    """
    try:
        # 如果是字符串，将其转换为列表
        if isinstance(receiver_emails, str):
            # 处理可能的多个邮箱（以逗号分隔）
            receiver_emails = [email.strip() for email in receiver_emails.split(',')]
        
        message = MIMEMultipart()
        message["From"] = config['SMTP']['sender_email']
        message["To"] = ', '.join(receiver_emails)  # 将多个收件人以逗号连接
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))

        smtp_server = config['SMTP']['server']
        smtp_port = int(config['SMTP']['port'])
        smtp_username = config['SMTP']['username']
        smtp_password = config['SMTP']['password']

        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE

        if smtp_port == 465:
            with smtplib.SMTP_SSL(smtp_server, smtp_port, context=context) as server:
                server.login(smtp_username, smtp_password)
                server.sendmail(config['SMTP']['sender_email'], receiver_emails, message.as_string())
        else:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.ehlo()
                if server.has_extn('STARTTLS'):
                    server.starttls(context=context)
                    server.ehlo()
                server.login(smtp_username, smtp_password)
                server.sendmail(config['SMTP']['sender_email'], receiver_emails, message.as_string())

        logger.info(f"邮件已成功发送到 {', '.join(receiver_emails)}")
    except Exception as e:
        logger.error(f"发送邮件失败: {str(e)}")
        raise

def monitor_database():
    """监控数据库主函数"""
    config = load_config()
    check_interval = int(config['MONITOR'].get('check_interval', 300))  # 默认5分钟检查一次
    connection = None
    
    while True:
        try:
            if connection is None or not connection.is_connected():
                connection = connect_oracle(config)
            
            table_name = config['MONITOR']['table_name']
            field_name = config['MONITOR']['field_name']
            condition_value = config['MONITOR']['condition_value']
            receiver_emails = config['MONITOR']['receiver_email']

            # 检查并获取满足条件的行
            results = check_field_value(connection, table_name, field_name, condition_value)
            
            if results and len(results) > 0:
                subject = config['MONITOR'].get('email_subject', '数据库监控告警')
                
                # 构建包含详细信息的邮件正文
                detail_body = f"检测到表 {table_name} 中以下作业状态为 {condition_value}：\n\n"
                for row in results:
                    # 根据查询结果的列顺序获取字段值
                    status, job_name, job_result_log = row
                    detail_body += f"作业名称: {job_name}\n"
                    detail_body += f"作业状态: {status}\n"
                    detail_body += f"错误日志: {job_result_log}\n"
                    detail_body += "-" * 50 + "\n"
                
                # 使用详细信息代替配置中的默认邮件正文
                body = detail_body
                send_email(config, subject, body, receiver_emails)

        except cx_Oracle.DatabaseError as e:
            logger.error(f"数据库错误: {str(e)}")
            if connection:
                try:
                    connection.close()
                except:
                    pass
            connection = None
            time.sleep(60)  # 数据库错误后等待1分钟再重试
            continue
            
        except Exception as e:
            logger.error(f"监控过程发生错误: {str(e)}", exc_info=True)
            if connection:
                try:
                    connection.close()
                except:
                    pass
            connection = None
            time.sleep(60)  # 其他错误后等待1分钟再重试
            continue
        
        logger.info(f"等待 {check_interval} 秒后进行下一次检查...")
        time.sleep(check_interval)

if __name__ == '__main__':
    try:
        logger.info("开始数据库监控...")
        monitor_database()
    except KeyboardInterrupt:
        logger.info("程序被用户中断")
    except Exception as e:
        logger.error(f"程序发生致命错误: {str(e)}", exc_info=True)
        raise 