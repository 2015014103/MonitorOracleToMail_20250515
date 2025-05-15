# 邮件发送器与Oracle数据库监控
C:\Users\Administrator\AppData\Local\Programs\Python\Python312\python.exe app.py

这是一个基于 Flask 开发的简单邮件发送应用程序，支持本地运行和 Vercel 部署。同时包含一个Oracle数据库监控工具，可监控指定表的字段状态并发送告警邮件。

## 项目文件说明2

| 文件名 | 功能描述 |
|--------|---------|
| app.py | 主要的Flask应用程序，包含邮件发送功能和Web服务器 |
| monitor_oracle.py | Oracle数据库监控工具，用于检测表状态并发送告警邮件 |
| index.html | Web界面前端页面，提供友好的邮件发送表单 |
| config.ini | 配置文件，包含SMTP服务器设置和Oracle数据库连接信息 |
| config.ini.example | 配置文件示例，不包含敏感信息，用于GitHub分享 |
| requirements.txt | 项目依赖列表，用于安装必要的Python包 |
| build_exe.py | 打包脚本，用于将应用打包成可执行文件 |
| build_exe.bat | Windows批处理脚本，用于执行打包命令 |
| EmailSender.spec | PyInstaller规格文件，用于邮件发送器的打包配置 |
| OracleMonitor.spec | PyInstaller规格文件，用于Oracle监控器的打包配置 |
| vercel.json | Vercel部署配置文件，用于云端部署 |
| README.md | 项目文档，包含安装、配置和使用说明 |

## 功能特点

- 支持 SMTP 和 SMTP SSL 连接
- 支持 TLS 加密
- 友好的 Web 界面
- 详细的日志记录
- 支持环境变量配置
- 跨域请求支持
- Oracle数据库监控功能
  - 监控指定表字段状态
  - 支持多邮箱告警通知
  - 自动提取并发送作业名称和错误日志

## 系统要求

- Python 3.8 或更高版本
- pip 包管理器
- 支持 SMTP 的邮箱账号（如 QQ 邮箱、企业邮箱等）

## 本地开发环境设置

1. 克隆项目：
   ```bash
   git clone <repository-url>
   cd sendEmail-main
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

   a. 创建 `config.ini` 文件：
   ```ini
   [SMTP]
   server = smtp.example.com
   port = 465  # 使用 SSL 时为 465，普通 SMTP 为 25
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

## Vercel 部署

1. Fork 或克隆此仓库到你的 GitHub 账号

2. 在 Vercel 中配置：
   - 连接你的 GitHub 仓库
   - 选择 Python 框架
   - 设置构建命令：`pip install -r requirements.txt`
   - 设置输出目录：`/`

3. 配置环境变量：
   在 Vercel 项目设置中添加以下环境变量：
   - `SMTP_SERVER`
   - `SMTP_PORT`
   - `SMTP_USERNAME`
   - `SMTP_PASSWORD`
   - `SENDER_EMAIL`

## 常见问题解决

### 1. 无法连接到 SMTP 服务器
- 检查服务器地址和端口是否正确
- 确认网络连接是否正常
- 检查防火墙设置

### 2. 认证失败
- 确认用户名和密码是否正确
- 对于 QQ 邮箱，确保使用的是授权码而不是登录密码
- 检查邮箱服务是否开启了 SMTP 功能

### 3. SSL/TLS 错误
- 确认使用了正确的端口（SSL: 465, TLS: 587, 普通 SMTP: 25）
- 检查服务器是否支持 SSL/TLS
- 确认证书设置是否正确

### 4. 应用无法启动
- 检查 Python 版本是否兼容
- 确认所有依赖都已正确安装
- 检查端口 8080 是否被占用
- 查看应用日志获取详细错误信息

## 安全建议

1. 不要在代码中硬编码敏感信息
2. 在生产环境中使用环境变量而不是配置文件
3. 定期更新依赖包以修复安全漏洞
4. 使用强密码和授权码
5. 在生产环境中启用 SSL/TLS 加密

## 日志说明

应用程序使用 Python 的 logging 模块记录日志，包含以下级别：
- DEBUG：详细的调试信息
- INFO：一般信息
- WARNING：警告信息
- ERROR：错误信息

日志会显示在控制台中，可通过查看日志来诊断问题。

## 贡献指南

欢迎提交 Issue 和 Pull Request 来改进这个项目。在提交 PR 之前，请确保：
1. 代码符合 PEP 8 规范
2. 添加了必要的测试
3. 更新了相关文档

## 许可证

MIT License

## Oracle数据库监控工具

除了基本的邮件发送功能外，本项目还提供了一个用于监控Oracle数据库的工具。该工具可检测指定表中的字段状态，当状态为错误时自动发送通知邮件。

### 功能特点

- 定期检查Oracle数据库中指定表的字段值
- 当字段值为指定条件（如"Error"）时发送告警邮件
- 支持向多个邮箱地址发送通知
- 邮件内容自动包含作业名称(JOB_NAME)和错误日志(JOB_RESULT_LOG)等详细信息
- 可自定义检查间隔时间
- 详细的日志记录

### 使用方法

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
   # 例如: user1@example.com,user2@example.com
   receiver_email = your_email@example.com
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

### 注意事项

- 确保已安装cx_Oracle包（`pip install cx_Oracle`）
- 如需修改监控逻辑，可以直接编辑`monitor_oracle.py`文件
- 监控工具以无限循环方式运行，可使用Ctrl+C终止，或考虑设置为系统服务
- 在生产环境中，建议使用守护进程或任务调度工具来管理此监控程序
