# public
from flask import Blueprint, request, jsonify
from db.db_config import db_session, UserDepartment, User, Supplier, Material

public_bp = Blueprint('public', __name__, url_prefix='/public')


@public_bp.route('/login', methods=['POST'])
def login():
    # 检查请求方法是否为 POST
    if request.method == 'POST':
        # 获取请求中的 JSON 数据
        data = request.get_json()
        username = data.get('username')  # 获取用户名
        password = data.get('password')  # 获取密码

        # 检查是否缺少必要的字段
        if not all([username, password]):
            return jsonify({'code': 0, 'message': '缺少必要字段'}), 400

        # 根据用户名查询用户
        user = db_session.query(User).filter(User.username == username).first()

        # 检查用户是否存在
        if user:
            # 检查密码是否正确
            if user.password == password:
                return jsonify({'code': 1, 'user_type_value': user.user_type, 'user_id': user.id}), 200
            else:
                return jsonify({'code': 0, 'message': '密码无效'}), 401
        else:
            return jsonify({'code': 0, 'message': '未找到用户'}), 401

    # 如果请求方法不是 POST，返回 405
    return jsonify({'code': 0, 'message': '请求方法无效'}), 405


# todo 获取部门列表
@public_bp.route('/getUserDepartment', methods=['POST'])
def getUserDepartment():
    if request.method == 'POST':
        with db_session() as session:
            res = session.query(UserDepartment).all()
            res = [{'value': i.name, 'label': i.name} for i in res]
        return jsonify(res)
