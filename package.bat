@echo off
REM 使用 pyinstaller 命令打包 Python 脚本
pyinstaller --onefile --distpath . --icon=chatgpt.ico .\chatgpt.py

REM 打包完成后，暂停命令行窗口以查看结果
pause