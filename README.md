# 项目打包说明

本文档说明如何将项目打包成可执行文件，以便在没有安装Python和Node.js环境的计算机上运行。

## 打包前准备

打包过程需要以下环境：

1. Python 3.7或更高版本
   - Python 3.7-3.11: 完全兼容，使用PyInstaller 5.6.2
   - Python 3.12+: 兼容，但会自动使用PyInstaller 6.x版本
2. Node.js和npm（用于构建前端项目）
3. 已安装项目所需的Python依赖（可通过`pip install -r flask/requirements.txt`安装）

## 打包步骤

1. 确保您的计算机上已安装Python和Node.js
2. 双击运行项目根目录中的`package.bat`文件
3. 等待打包过程完成，这可能需要几分钟时间
4. 打包完成后，可执行文件将生成在`dist`目录中

## 运行打包后的应用

1. 打开`dist`目录
2. 双击运行`start.bat`文件启动应用
3. 应用将自动在浏览器中打开

## 打包过程说明

打包过程会执行以下操作：

1. 检查必要的依赖是否已安装
2. 构建Vue前端项目
3. 修改Flask后端代码以适应打包环境
4. 使用PyInstaller打包Flask后端和前端静态文件
5. 创建启动器脚本
6. 清理临时文件

## 注意事项

- 打包过程中会临时修改后端代码，但会在打包完成后自动恢复
- 打包后的应用包含完整的前后端，无需额外安装Python或Node.js
- 打包后的应用使用SQLite数据库，数据库文件会被包含在可执行文件中
- 如果应用无法启动，请检查是否有杀毒软件阻止了应用运行

## 技术说明

- 前端：Vue.js 2.x
- 后端：Flask 2.0.1
- 数据库：SQLite
- 打包工具：PyInstaller（根据Python版本自动选择兼容版本）
  - Python 3.7-3.11: PyInstaller 5.6.2
  - Python 3.12+: PyInstaller 6.x