import os
import shutil
import subprocess
import sys
from pathlib import Path

# 项目根目录
ROOT_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
FLASK_DIR = ROOT_DIR / 'flask'
WEB_DIR = ROOT_DIR / 'web'
print(f'当前项目根目录: {ROOT_DIR}')
print(f'Flask目录是否存在: {FLASK_DIR.exists()}')
print(f'Web目录是否存在: {WEB_DIR.exists()}')
# Flask后端目录
FLASK_DIR = ROOT_DIR / 'flask'
# Vue前端目录
WEB_DIR = ROOT_DIR / 'web'
# 打包输出目录
DIST_DIR = ROOT_DIR / 'dist'
# 临时构建目录
BUILD_DIR = ROOT_DIR / 'build'


def check_requirements():
    """检查必要的依赖是否已安装"""
    print("检查必要的依赖...")
    
    # 检查Python版本
    python_version = sys.version_info
    print(f"当前Python版本: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    try:
        # 检查PyInstaller是否已安装
        subprocess.run([sys.executable, '-m', 'pip', 'show', 'pyinstaller'], 
                       check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("PyInstaller已安装")
    except subprocess.CalledProcessError:
        print("PyInstaller未安装，正在安装...")
        
        # 根据Python版本选择兼容的PyInstaller版本
        if python_version.major == 3 and python_version.minor >= 12:
            # Python 3.12+使用兼容的最新版本
            print("检测到Python 3.12+，将安装兼容的PyInstaller版本...")
            subprocess.run([sys.executable, '-m', 'pip', 'install', 'pyinstaller>=6.0.0'], check=True)
        elif python_version.major == 3 and python_version.minor >= 7 and python_version.minor < 12:
            # Python 3.7-3.11使用指定的5.6.2版本
            print("检测到Python 3.7-3.11，将安装PyInstaller 5.6.2...")
            subprocess.run([sys.executable, '-m', 'pip', 'install', 'pyinstaller==5.6.2'], check=True)
        else:
            # 其他版本使用兼容的版本
            print("检测到不常见的Python版本，将尝试安装兼容的PyInstaller版本...")
            subprocess.run([sys.executable, '-m', 'pip', 'install', 'pyinstaller'], check=True)
            
        print("PyInstaller安装完成")
    
    # 检查Node.js和npm是否已安装
    # 改进的Node.js检测逻辑
    node_path = shutil.which('node')
    npm_path = shutil.which('npm')
    
    if not node_path or not npm_path:
        print("错误: 需要安装Node.js和npm才能构建前端项目")
        print("请从https://nodejs.org下载并安装Node.js，并确保已添加到系统PATH环境变量")
        sys.exit(1)
    
    print(f"检测到Node.js路径: {node_path}")
    print(f"检测到npm路径: {npm_path}")
    print("Node.js和npm环境验证通过")


def build_frontend():
    """构建Vue前端项目"""
    print("\n开始构建前端项目...")
    os.chdir(WEB_DIR)
    
    # 安装前端依赖
    print("安装前端依赖...")
    subprocess.run(['npm', 'install'], check=True, shell=True)
    
    # 构建前端项目
    print("构建前端项目...")
    subprocess.run(['npm', 'run', 'build'], check=True, shell=True)
    
    print("前端项目构建完成")
    os.chdir(ROOT_DIR)


def build_backend():
    """使用PyInstaller打包Flask后端"""
    print("\n开始打包后端项目...")
    os.chdir(FLASK_DIR)
    
    # 创建spec文件
    spec_content = f'''\
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['app.py'],
    pathex=[r'{FLASK_DIR}'],
    binaries=[],
    datas=[
        (r'{WEB_DIR / "dist"}', 'web/dist'),
        (r'{FLASK_DIR / "db" / "local_sqlite.db"}', 'db'),
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='app',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='app',
)
'''
    
    with open('app.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)
    
    # 使用PyInstaller打包
    print("使用PyInstaller打包后端...")
    subprocess.run([sys.executable, '-m', 'PyInstaller', 'app.spec', '--distpath', str(DIST_DIR), '--workpath', str(BUILD_DIR), '--noconfirm'], check=True)
    
    print("后端项目打包完成")
    os.chdir(ROOT_DIR)


def create_launcher():
    """创建启动器脚本"""
    print("\n创建启动器...")
    
    # 创建启动批处理文件
    launcher_content = '''\
@echo off
cd /d "%~dp0"
start app\app.exe
'''
    
    with open(DIST_DIR / 'start.bat', 'w', encoding='utf-8') as f:
        f.write(launcher_content)
    
    print("启动器创建完成")


def modify_backend_for_packaging():
    """修改后端代码以适应打包环境"""
    print("\n修改后端代码以适应打包环境...")
    
    # 创建一个临时的app_packaged.py文件
    app_path = FLASK_DIR / 'app.py'
    app_packaged_path = FLASK_DIR / 'app_packaged.py'
    
    with open(app_path, 'r', encoding='utf-8') as f:
        app_content = f.read()
    
    # 添加代码以处理打包后的路径和静态文件服务
    packaged_app_content = '''\
# -*- coding: utf-8 -*-
import os
import sys

# 处理PyInstaller打包后的路径
def resource_path(relative_path):
    """获取资源的绝对路径，兼容开发环境和PyInstaller打包后的环境"""
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller创建的临时文件夹
        base_path = sys._MEIPASS
    else:
        # 正常的开发环境
        base_path = os.path.abspath(".") 
    return os.path.join(base_path, relative_path)

''' + app_content.replace(
        'app = Flask(__name__)', 
        'app = Flask(__name__, static_folder=resource_path("web/dist"), static_url_path="")')
    
    # 添加路由以提供前端文件
    if 'def index():' not in packaged_app_content:
        route_code = '''

@app.route("/")
def index():
    return app.send_static_file("index.html")
'''
        # 在if __name__ == '__main__'之前插入路由
        packaged_app_content = packaged_app_content.replace(
            "if __name__ == '__main__':", 
route_code + "if __name__ == '__main__':")
    
    with open(app_packaged_path, 'w', encoding='utf-8') as f:
        f.write(packaged_app_content)
    
    # 备份原始app.py并替换为打包版本
    shutil.copy2(app_path, app_path.with_suffix('.py.bak'))
    shutil.copy2(app_packaged_path, app_path)
    
    print("后端代码修改完成")


def restore_backend_code():
    """恢复原始的后端代码"""
    print("\n恢复原始的后端代码...")
    
    app_path = FLASK_DIR / 'app.py'
    app_bak_path = app_path.with_suffix('.py.bak')
    
    if app_bak_path.exists():
        shutil.copy2(app_bak_path, app_path)
        os.remove(app_bak_path)
    
    app_packaged_path = FLASK_DIR / 'app_packaged.py'
    if app_packaged_path.exists():
        os.remove(app_packaged_path)
    
    print("原始后端代码已恢复")


def cleanup():
    """清理临时文件"""
    print("\n清理临时文件...")
    
    # 删除临时构建目录
    if BUILD_DIR.exists():
        shutil.rmtree(BUILD_DIR)
    
    # 删除PyInstaller生成的临时文件
    spec_file = FLASK_DIR / 'app.spec'
    if spec_file.exists():
        os.remove(spec_file)
    
    print("临时文件清理完成")


def main():
    """主函数，执行打包流程"""
    print("=== 开始打包流程 ===")
    
    # 创建必要的目录
    os.makedirs(DIST_DIR, exist_ok=True)
    os.makedirs(BUILD_DIR, exist_ok=True)
    
    try:
        # 检查依赖
        check_requirements()
        
        # 构建前端
        build_frontend()
        
        # 修改后端代码以适应打包环境
        modify_backend_for_packaging()
        
        # 打包后端
        build_backend()
        
        # 创建启动器
        create_launcher()
        
        print("\n=== 打包完成 ===")
        print(f"可执行文件已生成在: {DIST_DIR}")
        print("运行dist目录中的start.bat启动应用")
    
    except Exception as e:
        print(f"\n打包过程中出错: {e}")
    
    finally:
        # 恢复原始后端代码
        restore_backend_code()
        
        # 清理临时文件
        cleanup()


if __name__ == "__main__":
    main()