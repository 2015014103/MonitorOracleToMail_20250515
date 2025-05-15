import os
import sys
import shutil
import subprocess
import datetime

def find_pyinstaller():
    """寻找PyInstaller可执行文件路径"""
    # 尝试在脚本目录或者PATH中找到pyinstaller
    try:
        # 使用where命令(Windows)或which命令(Unix)查找pyinstaller
        if os.name == 'nt':  # Windows
            result = subprocess.run(['where', 'pyinstaller'], 
                                   capture_output=True, text=True, check=True)
            paths = result.stdout.strip().split('\n')
            return paths[0] if paths else None
        else:  # Unix-like
            result = subprocess.run(['which', 'pyinstaller'], 
                                   capture_output=True, text=True, check=True)
            return result.stdout.strip()
    except (subprocess.SubprocessError, IndexError):
        return None

def build_exe():
    """构建EXE文件"""
    print("正在打包Oracle监控工具为EXE文件...")
    
    # 创建dist和build目录（如果不存在）
    os.makedirs('dist', exist_ok=True)
    os.makedirs('build', exist_ok=True)
    
    # 寻找pyinstaller路径
    pyinstaller_path = find_pyinstaller()
    if not pyinstaller_path:
        print("错误: 无法找到PyInstaller。请确保已正确安装: pip install pyinstaller")
        return False
    
    # 确保配置文件存在
    if not os.path.exists('config.ini'):
        print("警告: 未找到config.ini文件")
        
    # 构建monitor_oracle.exe
    monitor_cmd = [
        pyinstaller_path,
        '--onefile',  # 创建单个可执行文件
        '--name', 'OracleMonitor',
        '--add-data', 'config.ini;.',  # 将config.ini添加到EXE中
        'monitor_oracle.py'
    ]
    
    print("执行命令:", " ".join(monitor_cmd))
    try:
        subprocess.run(monitor_cmd, check=True)
        print("Oracle监控工具打包成功!")
    except subprocess.SubprocessError as e:
        print(f"打包Oracle监控工具时出错: {str(e)}")
        return False
    
    # 构建邮件发送器app.exe
    app_cmd = [
        pyinstaller_path,
        '--onefile',  # 创建单个可执行文件
        '--name', 'EmailSender',
        '--add-data', 'config.ini;.',  # 将config.ini添加到EXE中
        'app.py'
    ]
    
    print("\n执行命令:", " ".join(app_cmd))
    try:
        subprocess.run(app_cmd, check=True)
        print("邮件发送器打包成功!")
    except subprocess.SubprocessError as e:
        print(f"打包邮件发送器时出错: {str(e)}")
        return False
    
    # 创建release目录
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    release_dir = f"sendEmail_oracle_monitor_exe_{timestamp}"
    os.makedirs(release_dir, exist_ok=True)
    
    # 复制文件到release目录
    try:
        # 复制可执行文件
        shutil.copy2(os.path.join('dist', 'OracleMonitor.exe'), release_dir)
        shutil.copy2(os.path.join('dist', 'EmailSender.exe'), release_dir)
        
        # 复制配置文件
        shutil.copy2('config.ini', release_dir)
        
        # 复制README
        if os.path.exists('README.md'):
            shutil.copy2('README.md', release_dir)
            
        print(f"\n文件已复制到 {release_dir} 目录")
    except Exception as e:
        print(f"复制文件时出错: {str(e)}")
        return False
    
    print("\n打包完成!")
    print(f"可执行文件位于: {os.path.abspath(release_dir)}")
    return True

if __name__ == "__main__":
    build_exe() 