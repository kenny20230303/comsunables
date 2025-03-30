# public
from flask import Blueprint, request, jsonify
from db.db_config import db_session, UserDepartment, User, Supplier, Material, MonthlyPlan, DailyApplication
from datetime import datetime

user_bp = Blueprint('user', __name__, url_prefix='/user')


# todo 月度计划申请
@user_bp.route('/MonthlyPlan', methods=['GET', 'POST'])
def MonthlyPlan_api():
    if request.method == 'GET':  # 获取材料信息
        warehouse_type = request.args.get('warehouse_type', '事务所仓库')  # 默认为事务所仓库
        with db_session() as session:
            res = session.query(Material).filter(Material.warehouse_type == warehouse_type).all()
            materials = [i.as_dict() for i in res]
        return jsonify(materials)
    if request.method == 'POST':
        user_id = request.get_json().get('user_id')
        material_id = request.get_json().get('id')
        material_number = request.get_json().get('stockQuantity')
        warehouse_type = request.get_json().get('warehouse_type', '事务所仓库')  # 获取仓库类型

        # 获取当前日期和当前天数
        current_date = datetime.now()
        current_day = current_date.day

        # 检查当前日期是否在25号之后
        if current_day > 31:
            return jsonify({'error': '每月25号之后禁止添加数据'}), 400

        # 检查本月是否已经存在记录
        # 获取本月的第一天
        first_day_of_month = current_date.replace(day=1)
        existing_record = db_session.query(MonthlyPlan).filter(
            MonthlyPlan.MonthlyPlan_type == '计划内',
            MonthlyPlan.user_id == user_id,
            MonthlyPlan.Material_id == material_id,
            MonthlyPlan.belong_month >= first_day_of_month.strftime('%Y-%m-%d')
        ).first()

        if existing_record:
            return jsonify({'error': '本月已经存在数据，无法再添加'}), 400

        # 如果通过检查，则创建新的记录
        new_plan = MonthlyPlan(
            user_id=user_id,
            Material_id=material_id,
            Material_number=material_number,
            belong_month=current_date.strftime('%Y-%m-%d')
        )

        # 将新记录添加到数据库会话并提交
        db_session.add(new_plan)
        db_session.commit()

        return jsonify({'success': '数据添加成功'}), 201


# todo 月度计划申请
@user_bp.route('/MonthlyPlanHistory', methods=['POST', 'PUT'])
def MonthlyPlanHistory_api():
    if request.method == 'POST':  # 获取材料信息
        user_id = request.get_json().get('user_id')
        with db_session():
            res = db_session.query(MonthlyPlan).filter(MonthlyPlan.user_id == user_id).filter(MonthlyPlan.MonthlyPlan_type == '计划内').all()
            infos_list = []
            for i in res:
                if i.auditor == 'True':
                    res_item = db_session.query(Material).filter(Material.id == int(i.Material_id)).first()
                    res_item = res_item.as_dict()
                    res_item['number'] = i.Material_number
                    res_item['current_time'] = i.current_time
                    res_item['type'] = '已通过'
                    res_item['id'] = i.id
                    infos_list.append(res_item)
                if i.auditor != 'True':
                    res_item = db_session.query(Material).filter(Material.id == int(i.Material_id)).first()
                    res_item = res_item.as_dict()
                    res_item['number'] = i.Material_number
                    res_item['current_time'] = i.current_time
                    res_item['type'] = '未通过'
                    res_item['id'] = i.id
                    infos_list.append(res_item)
        return jsonify(infos_list)

    if request.method == 'PUT':
        user_id = request.get_json().get('user_id')
        material_id = request.get_json().get('material_id')
        new_quantity = request.get_json().get('new_quantity')

        with db_session() as session:
            plan = session.query(MonthlyPlan).filter(MonthlyPlan.id == material_id, MonthlyPlan.user_id == user_id).first()
            if plan:
                plan.Material_number = new_quantity
                session.commit()
                return jsonify({'success': True})
            else:
                return jsonify({'success': False, 'message': '未找到该申请'}), 404


# todo 月度计划外申请
@user_bp.route('/MonthlyPlanOuter', methods=['GET', 'POST'])
def MonthlyPlanOuter_api():
    if request.method == 'GET':  # 获取材料信息
        with db_session() as session:
            res = session.query(Material).all()
            materials = [i.as_dict() for i in res]
        return jsonify(materials)
    if request.method == 'POST':
        user_id = request.get_json().get('user_id')
        material_id = request.get_json().get('id')
        material_number = request.get_json().get('stockQuantity')
        warehouse_type = request.get_json().get('warehouse_type', '事务所仓库')  # 获取仓库类型
        naqi = request.get_json().get('naqi')
        beizhu = request.get_json().get('beizhu')

        # 获取当前日期和当前天数
        current_date = datetime.now()
        current_day = current_date.day

        # 检查当前日期是否在25号之后
        if current_day > 25:
            return jsonify({'error': '每月25号之后禁止添加数据'}), 400

        # 检查本月是否已经存在记录
        # 获取本月的第一天
        first_day_of_month = current_date.replace(day=1)
        existing_record = db_session.query(MonthlyPlan).filter(
            MonthlyPlan.MonthlyPlan_type == '计划外',
            MonthlyPlan.user_id == user_id,
            MonthlyPlan.Material_id == material_id,
            MonthlyPlan.belong_month >= first_day_of_month.strftime('%Y-%m-%d')
        ).first()

        if existing_record:
            return jsonify({'error': '本月已经存在数据，无法再添加'}), 400

        # 如果通过检查，则创建新的记录
        new_plan = MonthlyPlan(
            user_id=user_id,
            MonthlyPlan_type='计划外',
            Material_id=material_id,
            Material_number=material_number,
            belong_month=current_date.strftime('%Y-%m-%d'),
            naqi=naqi,
            beizhu=beizhu,
        )

        # 将新记录添加到数据库会话并提交
        db_session.add(new_plan)
        db_session.commit()

        return jsonify({'success': '数据添加成功'}), 201


# todo 月度计划外申请
@user_bp.route('/MonthlyPlanOuterHistory', methods=['POST', 'PUT'])
def MonthlyPlanOuterHistory_api():
    if request.method == 'POST':  # 获取材料信息
        user_id = request.get_json().get('user_id')
        with db_session():
            res = db_session.query(MonthlyPlan).filter(MonthlyPlan.user_id == user_id).filter(MonthlyPlan.MonthlyPlan_type == '计划外').all()
            infos_list = []
            for i in res:
                if i.auditor == 'True':
                    res_item = db_session.query(Material).filter(Material.id == int(i.Material_id)).first()
                    res_item = res_item.as_dict()
                    res_item['number'] = i.Material_number
                    res_item['current_time'] = i.current_time
                    res_item['type'] = '已通过'
                    res_item['id'] = i.id

                if i.auditor != 'True':
                    res_item = db_session.query(Material).filter(Material.id == int(i.Material_id)).first()
                    res_item = res_item.as_dict()
                    res_item['number'] = i.Material_number
                    res_item['current_time'] = i.current_time
                    res_item['type'] = '未通过'
                    res_item['id'] = i.id

                infos_list.append(res_item)
        return jsonify(infos_list)

    if request.method == 'PUT':
        user_id = request.get_json().get('user_id')
        material_id = request.get_json().get('material_id')
        new_quantity = request.get_json().get('new_quantity')

        with db_session() as session:
            plan = session.query(MonthlyPlan).filter(MonthlyPlan.id == material_id, MonthlyPlan.user_id == user_id).first()
            if plan:
                plan.Material_number = new_quantity
                session.commit()
                return jsonify({'success': True})
            else:
                return jsonify({'success': False, 'message': '未找到该申请'}), 404


# todo 日申请
@user_bp.route('/DayPlan', methods=['GET', 'POST', 'PUT'])
def DayPlan_api():
    if request.method == 'GET':
        user_id = request.args.get('user_id')
        warehouse_type = request.args.get('warehouse_type', '事务所仓库')  # 默认为事务所仓库

        now = datetime.now()
        first_day_of_month = datetime(now.year, now.month, 1)
        if now.month == 12:
            first_day_of_next_month = datetime(now.year + 1, 1, 1)
        else:
            first_day_of_next_month = datetime(now.year, now.month + 1, 1)

        with db_session():
            # 获取该用户本月的所有月计划
            monthly_plans = db_session.query(MonthlyPlan).filter(
                MonthlyPlan.current_time >= first_day_of_month.strftime('%Y-%m-%d %H:%M'),
                MonthlyPlan.current_time < first_day_of_next_month.strftime('%Y-%m-%d %H:%M'),
                MonthlyPlan.user_id == user_id
            ).all()

            # 获取该用户本月的所有日申请
            daily_applications = db_session.query(DailyApplication).filter(
                DailyApplication.current_time >= first_day_of_month.strftime('%Y-%m-%d %H:%M'),
                DailyApplication.current_time < first_day_of_next_month.strftime('%Y-%m-%d %H:%M'),
                DailyApplication.user_id == user_id
            ).all()

            # 计算每种材料的日申请总数
            daily_totals = {}
            for daily in daily_applications:
                if daily.Material_id in daily_totals:
                    daily_totals[daily.Material_id] += int(daily.Material_number)
                else:
                    daily_totals[daily.Material_id] = int(daily.Material_number)

            infos_list = []
            for i in monthly_plans:
                # 获取商品信息，并根据仓库类型筛选
                Material_info = db_session.query(Material).filter(
                    Material.id == int(i.Material_id),
                    Material.warehouse_type == warehouse_type
                ).first()
                
                # 如果该材料不属于所选仓库类型，则跳过
                if not Material_info:
                    continue
                monthly_number = int(i.Material_number)
                daily_number = daily_totals.get(i.Material_id, 0)
                remaining_number = monthly_number - daily_number  # 计算剩余可申请数量

                infos_list.append({
                    'name': Material_info.name,
                    'monthly_plans': i.as_dict(),
                    'Material_info': Material_info.as_dict(),
                    'remaining_number': remaining_number  # 添加剩余数量
                })
        return jsonify(infos_list)

    if request.method == 'POST':
        data = request.json
        user_id = data.get('user_id')
        material_id = str(data.get('id'))
        requested_quantity = int(data.get('stockQuantity'))
        MonthlyPlan_type = str(data.get('MonthlyPlan_type'))

        print(material_id, requested_quantity)

        if not user_id or not material_id:
            return jsonify({'error': '用户ID或材料ID缺失'}), 400

        with db_session() as session:
            now = datetime.now()
            first_day_of_month = datetime(now.year, now.month, 1)
            if now.month == 12:
                first_day_of_next_month = datetime(now.year + 1, 1, 1)
            else:
                first_day_of_next_month = datetime(now.year, now.month + 1, 1)

            start_of_today = datetime(now.year, now.month, now.day)
            end_of_today = start_of_today.replace(hour=23, minute=59, second=59)

            existing_daily_application = session.query(DailyApplication).filter(
                DailyApplication.user_id == user_id,
                DailyApplication.Material_id == material_id,
                DailyApplication.current_time >= start_of_today.strftime('%Y-%m-%d %H:%M'),
                DailyApplication.current_time <= end_of_today.strftime('%Y-%m-%d %H:%M')
            ).first()

            if existing_daily_application:
                return jsonify({'error': '今天已经申请过该材料'}), 400

            monthly_plan = session.query(MonthlyPlan).filter(
                MonthlyPlan.current_time >= first_day_of_month.strftime('%Y-%m-%d %H:%M'),
                MonthlyPlan.MonthlyPlan_type == MonthlyPlan_type,

                MonthlyPlan.current_time < first_day_of_next_month.strftime('%Y-%m-%d %H:%M'),
                MonthlyPlan.user_id == user_id,
                MonthlyPlan.Material_id == material_id,
                MonthlyPlan.auditor == 'True'  # 检查审核员审核是否通过
            ).first()


            if not monthly_plan:
                return jsonify({'error': '未找到相应的月度计划或审核未通过'}), 404

            monthly_quantity = int(monthly_plan.Material_number)

            if requested_quantity > monthly_quantity:
                print(monthly_plan.id)
                print(material_id)
                return jsonify({'error': '申请数量超过月度计划数量'}), 400

            daily_application = DailyApplication(
                user_id=user_id,
                Material_id=material_id,
                Material_number=str(requested_quantity),
                current_time=datetime.now().strftime('%Y-%m-%d %H:%M')
            )
            session.add(daily_application)
            session.commit()

        return jsonify({'message': '申请成功'}), 201

    if request.method == 'PUT':
        data = request.json
        user_id = data.get('user_id')
        material_id = data.get('material_id')
        new_quantity = int(data.get('new_quantity'))
        print(material_id)

        if not user_id or not material_id:
            return jsonify({'error': '用户ID或材料ID缺失'}), 400

        with db_session() as session:
            daily_application = session.query(DailyApplication).filter(
                DailyApplication.user_id == user_id,
                DailyApplication.Material_id == material_id
            ).first()

            if not daily_application:
                return jsonify({'error': '未找到相应的申请记录'}), 404

            monthly_plan = session.query(MonthlyPlan).filter(
                MonthlyPlan.user_id == user_id,
                MonthlyPlan.Material_id == material_id
            ).first()

            if not monthly_plan:
                print(2)
                return jsonify({'error': '未找到相应的月度计划'}), 404

            monthly_quantity = int(monthly_plan.Material_number)

            if new_quantity > monthly_quantity:
                return jsonify({'error': '申请数量超过月度计划数量'}), 400

            # 更新数量
            daily_application.Material_number = str(new_quantity)
            session.commit()

        return jsonify({'message': '数量更新成功'}), 200


# todo 日计划申请
@user_bp.route('/DayPlanHistory', methods=['POST'])
def DayPlanHistory_api():
    if request.method == 'POST':
        user_id = request.get_json().get('user_id')

        now = datetime.now()
        first_day_of_month = datetime(now.year, now.month, 1)
        if now.month == 12:
            first_day_of_next_month = datetime(now.year + 1, 1, 1)
        else:
            first_day_of_next_month = datetime(now.year, now.month + 1, 1)
        with db_session():
            monthly_plans = db_session.query(DailyApplication).filter(
                DailyApplication.current_time >= first_day_of_month.strftime('%Y-%m-%d %H:%M'),
                DailyApplication.current_time < first_day_of_next_month.strftime('%Y-%m-%d %H:%M'),
                DailyApplication.user_id == str(user_id)
            ).all()

            infos_list = []
            for i in monthly_plans:
                # 获取商品信息
                DailyApplication_info = db_session.query(Material).filter(Material.id == int(i.Material_id)).first()
                if DailyApplication_info:
                    if i.auditor == 'True':
                        infos_list.append({'Material_number': i.Material_number,
                                           'current_time': i.current_time,
                                           'id': i.id,
                                           'DailyApplication_info': DailyApplication_info.as_dict(),
                                           'type': '已通过'

                                           })
                    if i.auditor != 'True':
                        infos_list.append({'Material_number': i.Material_number,
                                           'current_time': i.current_time,
                                           'id': i.id,
                                           'DailyApplication_info': DailyApplication_info.as_dict(),
                                           'type': '未通过'
                                           })

        return jsonify(infos_list)
