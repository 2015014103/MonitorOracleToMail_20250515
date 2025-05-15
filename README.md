# 邮件发送器与Oracle数据库监控工具

这是一个功能完善的应用程序，包含两个主要功能：
1. 基于Flask开发的简单邮件发送应用，支持本地运行和Vercel部署
2. Oracle数据库监控工具，可监控指定表的字段状态并发送告警邮件

## 项目文件说明

| 文件名 | 功能描述 |
|--------|---------|
| app.py | 主要的Flask应用程序，包含邮件发送功能和Web服务器 |
| monitor_oracle.py | Oracle数据库监控工具，用于检测表状态并发送告警邮件 |
| index.html | Web界面前端页面，提供友好的邮件发送表单 |
| config.ini | 配置文件，包含SMTP服务器设置和Oracle数据库连接信息 |
| config.ini.example | 配置文件示例，不包含敏感信息，用于GitHub分享 |
| requirements.txt | 项目依赖列表，用于安装必要的Python包 |
| vercel.json | Vercel部署配置文件，用于云端部署 |

## 功能特点

### 邮件发送功能
- 支持SMTP和SMTP SSL连接
- 支持TLS加密
- 友好的Web界面
- 详细的日志记录
- 支持环境变量配置
- 跨域请求支持

### Oracle数据库监控功能
- 监控指定表字段状态
- 支持多邮箱告警通知
- 自动提取并发送作业名称和错误日志
- 自定义检查间隔时间

## 系统要求

- Python 3.8或更高版本
- pip包管理器
- 支持SMTP的邮箱账号（如QQ邮箱、企业邮箱等）
- Oracle数据库（如需使用监控功能）

## 本地开发环境设置

1. 克隆项目：
   ```bash
   git clone <repository-url>
   cd email-oracle-monitor
   ```

2. 创建并激活虚拟环境（推荐）：
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate

   # Linux/Mac
   python3 -m venv venv
   source venv/bin/activate
   ```

3. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

4. 配置邮件服务器：

   a. 创建`config.ini`文件（可以复制config.ini.example）：
   ```ini
   [SMTP]
   server = smtp.example.com
   port = 465  # 使用SSL时为465，普通SMTP为25
   username = your_email@example.com
   password = your_password
   sender_email = your_email@example.com
   ```

   b. 或使用环境变量：
   ```bash
   # Windows
   set SMTP_SERVER=smtp.example.com
   set SMTP_PORT=465
   set SMTP_USERNAME=your_email@example.com
   set SMTP_PASSWORD=your_password
   set SENDER_EMAIL=your_email@example.com

   # Linux/Mac
   export SMTP_SERVER=smtp.example.com
   export SMTP_PORT=465
   export SMTP_USERNAME=your_email@example.com
   export SMTP_PASSWORD=your_password
   export SENDER_EMAIL=your_email@example.com
   ```

5. 运行应用：
   ```bash
   python app.py
   ```

6. 访问应用：
   打开浏览器访问 http://localhost:8080

## Vercel部署

1. Fork或克隆此仓库到你的GitHub账号

2. 在Vercel中配置：
   - 连接你的GitHub仓库
   - 选择Python框架
   - 设置构建命令：`pip install -r requirements.txt`
   - 设置输出目录：`/`

3. 配置环境变量：
   在Vercel项目设置中添加以下环境变量：
   - `SMTP_SERVER`
   - `SMTP_PORT`
   - `SMTP_USERNAME`
   - `SMTP_PASSWORD`
   - `SENDER_EMAIL`

## Oracle数据库监控使用方法

1. 配置数据库连接和监控参数：
   编辑`config.ini`文件中的`[ORACLE]`和`[MONITOR]`部分：

   ```ini
   [ORACLE]
   # Oracle数据库连接信息
   username = your_db_username
   password = your_db_password
   dsn = host:port/service_name

   [MONITOR]
   # 监控配置
   table_name = JOB_CONFIG
   field_name = JOB_STATUS
   condition_value = Error
   # 接收告警邮件的邮箱地址，多个邮箱用逗号分隔
   receiver_email = user1@example.com,user2@example.com
   check_interval = 300
   email_subject = ETL状态监控报警
   ```

2. 运行监控工具：
   ```bash
   python monitor_oracle.py
   ```

3. 监控处理流程：
   - 工具会按配置的间隔时间定期连接Oracle数据库
   - 检查指定表中指定字段是否有值等于配置的条件值
   - 当发现匹配的记录时，自动提取该记录的JOB_NAME和JOB_RESULT_LOG信息
   - 生成包含详细信息的邮件正文，并发送给所有配置的收件人

## 常见问题解决

### 1. 无法连接到SMTP服务器
- 检查服务器地址和端口是否正确
- 确认网络连接是否正常
- 检查防火墙设置

### 2. 认证失败
- 确认用户名和密码是否正确
- 对于QQ邮箱，确保使用的是授权码而不是登录密码
- 检查邮箱服务是否开启了SMTP功能

### 3. SSL/TLS错误
- 确认使用了正确的端口（SSL: 465, TLS: 587, 普通SMTP: 25）
- 检查服务器是否支持SSL/TLS
- 确认证书设置是否正确

### 4. 应用无法启动
- 检查Python版本是否兼容
- 确认所有依赖都已正确安装
- 检查端口8080是否被占用
- 查看应用日志获取详细错误信息

### 5. Oracle监控问题
- 确保已安装cx_Oracle包
- 验证数据库连接信息是否正确
- 检查表名和字段名是否存在于数据库中

## 安全建议

1. 不要在代码中硬编码敏感信息
2. 在生产环境中使用环境变量而不是配置文件
3. 定期更新依赖包以修复安全漏洞
4. 使用强密码和授权码
5. 在生产环境中启用SSL/TLS加密

## 日志说明

应用程序使用Python的logging模块记录日志，包含以下级别：
- DEBUG：详细的调试信息
- INFO：一般信息
- WARNING：警告信息
- ERROR：错误信息

日志会显示在控制台中，可通过查看日志来诊断问题。

## 贡献指南

欢迎提交Issue和Pull Request来改进这个项目。在提交PR之前，请确保：
1. 代码符合PEP 8规范
2. 添加了必要的测试
3. 更新了相关文档

## 许可证

MIT License
