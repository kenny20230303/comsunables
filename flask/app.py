from flask import Flask, request
from apps.admin import admin_bp
from apps.Public import public_bp
from apps.user import user_bp
from apps.auditor import auditor_bp
from apps.finance import finance_bp
from flask_cors import CORS

app = Flask(__name__)
CORS().init_app(app)
# 注册蓝图
app.register_blueprint(public_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(user_bp)
app.register_blueprint(auditor_bp)
app.register_blueprint(finance_bp)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
