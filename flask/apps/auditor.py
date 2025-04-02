# admin_bp
from flask import Blueprint, request, jsonify
from db.db_config import db_session, UserDepartment, User, Supplier, Material, MonthlyPlan, DailyApplication

auditor_bp = Blueprint('auditor', __name__, url_prefix='/auditor')


# todo 月度计划管理
@auditor_bp.route('/getMonthlyPlan', methods=['POST', 'PUT'])
def getMonthlyPlan():
    if request.method == 'POST':
        with db_session() as session:
            # 获取当前自己部门
            user_id = request.get_json()['user_id']
            UserDepartment_name = db_session.query(User).filter(User.id == user_id).first().UserDepartment_name
            print(UserDepartment_name)

            res = session.query(MonthlyPlan).filter(MonthlyPlan.MonthlyPlan_type == '计划内').all()

            infos_list = []
            for i in res:
                # 获取用户信息
                print(i.user_id)
                User_info = db_session.query(User).filter(User.id == int(i.user_id)).first()

                print(User_info.UserDepartment_name)
                if User_info.UserDepartment_name == UserDepartment_name:
                    print('1')
                    # 获取商品信息
                    Material_info = db_session.query(Material).filter(Material.id == int(i.Material_id)).first()
                    infos_list.append({'name': Material_info.name, 'specifications': Material_info.specifications,
                                       'unit': Material_info.unit, 'price': Material_info.price,
                                       'id': i.id,

                                       'user_name': User_info.name, 'user_phone': User_info.phone,

                                       'Material_number': i.Material_number, 'auditor': i.auditor,
                                       'number_change': i.number_change, 'current_time': i.current_time

                                       })
                else:
                    pass
        infos_list.reverse()
        return jsonify(infos_list)
    if request.method == 'PUT':
        data = request.get_json()
        material_id = data['id']
        new_number = data['number']

        with db_session() as session:
            monthly_plan = session.query(MonthlyPlan).filter(MonthlyPlan.id == material_id).first()
            if monthly_plan:

                if monthly_plan.Material_number != new_number:
                    monthly_plan.number_change = 'True'

                monthly_plan.Material_number = new_number
                monthly_plan.auditor = 'True'
                monthly_plan.finance = 'True'
                session.commit()
                return jsonify({'message': 'Update successful'}), 200
            else:
                return jsonify({'message': 'Material not found'}), 404


# todo 月度计划管理
@auditor_bp.route('/getMonthlyPlanOuter', methods=['POST', 'PUT'])
def getMonthlyPlanOuter():
    if request.method == 'POST':
        with db_session() as session:
            # 获取当前自己部门
            user_id = request.get_json()['user_id']
            UserDepartment_name = db_session.query(User).filter(User.id == user_id).first().UserDepartment_name

            res = session.query(MonthlyPlan).filter(MonthlyPlan.MonthlyPlan_type == '计划外').all()

            infos_list = []
            for i in res:
                # 获取用户信息
                User_info = db_session.query(User).filter(User.id == int(i.user_id)).first()
                if User_info.UserDepartment_name == UserDepartment_name:
                    # 获取商品信息
                    Material_info = db_session.query(Material).filter(Material.id == int(i.Material_id)).first()
                    infos_list.append({'name': Material_info.name, 'specifications': Material_info.specifications,
                                       'unit': Material_info.unit, 'price': Material_info.price,
                                       'id': i.id,

                                       'user_name': User_info.name, 'user_phone': User_info.phone,

                                       'Material_number': i.Material_number, 'auditor': i.auditor,
                                       'number_change': i.number_change, 'current_time': i.current_time

                                       })
                else:
                    pass
        infos_list.reverse()
        return jsonify(infos_list)
    if request.method == 'PUT':
        data = request.get_json()
        material_id = data['id']
        new_number = data['number']

        with db_session() as session:
            monthly_plan = session.query(MonthlyPlan).filter(MonthlyPlan.id == material_id).first()
            if monthly_plan:

                if monthly_plan.Material_number != new_number:
                    monthly_plan.number_change = 'True'
                monthly_plan.MonthlyPlan_type = '计划外'
                monthly_plan.Material_number = new_number
                monthly_plan.auditor = 'True'
                session.commit()
                return jsonify({'message': 'Update successful'}), 200
            else:
                return jsonify({'message': 'Material not found'}), 404


# todo 日度计划管理
@auditor_bp.route('/getDayPlan', methods=['POST', 'PUT'])
def getDayPlan():
    if request.method == 'POST':
        with db_session() as session:
            # 获取当前自己部门
            user_id = request.get_json()['user_id']
            UserDepartment_name = db_session.query(User).filter(User.id == user_id).first().UserDepartment_name

            res = session.query(DailyApplication).filter().all()

            infos_list = []
            for i in res:
                # 获取用户信息
                User_info = db_session.query(User).filter(User.id == int(i.user_id)).first()
                if User_info.UserDepartment_name == UserDepartment_name:
                    # 获取商品信息
                    Material_info = db_session.query(Material).filter(Material.id == int(i.Material_id)).first()
                    if Material_info:
                        infos_list.append({'name': Material_info.name, 'specifications': Material_info.specifications,
                                           'unit': Material_info.unit, 'price': Material_info.price,
                                           'id': i.id,
                                           'user_name': User_info.name, 'user_phone': User_info.phone,
                                           'Material_number': i.Material_number, 'auditor': i.auditor,
                                           'number_change': i.number_change, 'current_time': i.current_time
                                           })
                else:
                    pass
        infos_list.reverse()
        return jsonify(infos_list)
    if request.method == 'PUT':
        data = request.get_json()
        material_id = data['id']
        new_number = data['number']

        with db_session() as session:
            monthly_plan = session.query(DailyApplication).filter(DailyApplication.id == material_id).first()
            if monthly_plan:

                if monthly_plan.Material_number != new_number:
                    monthly_plan.number_change = 'True'

                monthly_plan.Material_number = new_number
                monthly_plan.auditor = 'True'
                session.commit()
                return jsonify({'message': 'Update successful'}), 200
            else:
                return jsonify({'message': 'Material not found'}), 404
