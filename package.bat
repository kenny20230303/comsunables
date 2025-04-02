@echo off
echo ===================================
echo 正在打包应用为可执行文件...
echo ===================================

cd /d "%~dp0"
python build.py

echo.
echo 如果打包成功，请运行dist目录中的start.bat启动应用
echo.
pause