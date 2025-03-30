# admin_bp
from flask import Blueprint, request, jsonify
from db.db_config import db_session, UserDepartment, User, Supplier, Material,MaterialHistory

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


# todo 用户部门管理
@admin_bp.route('/UserDepartment', methods=['GET', 'POST', 'PUT', 'DELETE'])
def user_department():
    if request.method == 'GET':
        with db_session() as session:
            res = session.query(UserDepartment).all()
            usertypes = [i.as_dict() for i in res]
        return jsonify(usertypes)


    elif request.method == 'POST':
        data = request.json
        if 'name' not in data:
            return jsonify({'error': 'Missing name field'}), 400
        new_usertype = UserDepartment(name=data['name'])
        with db_session() as session:
            session.add(new_usertype)
            session.commit()
            session.refresh(new_usertype)  # 重新加载对象
        return jsonify({'id': new_usertype.id, 'name': new_usertype.name}), 201

    elif request.method == 'PUT':
        data = request.json
        if 'id' not in data or 'name' not in data:
            return jsonify({'error': 'Missing id or name field'}), 400

        with db_session() as session:
            usertype = session.query(UserDepartment).get(data['id'])
            if usertype:
                usertype.name = data['name']
                session.commit()
                return jsonify({'id': usertype.id, 'name': usertype.name})
            else:
                return jsonify({'error': 'UserType not found'}), 404

    elif request.method == 'DELETE':
        data = request.json
        if 'id' not in data:
            return jsonify({'error': 'Missing id field'}), 400

        with db_session() as session:
            usertype = session.query(UserDepartment).get(data['id'])
            if usertype:
                session.delete(usertype)
                session.commit()
                return jsonify({'message': 'UserType deleted'})
            else:
                return jsonify({'error': 'UserType not found'}), 404


# todo 用户管理
@admin_bp.route('/User', methods=['GET', 'POST', 'PUT', 'DELETE'])
def user():
    if request.method == 'GET':
        usertype = request.args.get('usertype')
        with db_session() as session:
            res = session.query(User).filter(User.user_type == usertype).all()
            users = [i.as_dict() for i in res]
        return jsonify(users)

    elif request.method == 'POST':
        data = request.json
        if 'username' not in data or 'name' not in data:
            return jsonify({'error': 'Missing username or name field'}), 400
        new_user = User(
            username=data['username'],
            password=data.get('password'),  # 密码可以为空
            name=data['name'],
            phone=data.get('phone'),
            user_type=data.get('user_type', 'user'),  # 默认用户类型为'user'
            UserDepartment_name=data.get('UserDepartment_name', '无')  # 默认部门为'无'
        )
        with db_session() as session:
            session.add(new_user)
            session.commit()
            session.refresh(new_user)

        return jsonify({'id': new_user.id, 'username': new_user.username, 'name': new_user.name}), 201

    elif request.method == 'PUT':
        data = request.json
        if 'id' not in data or 'username' not in data or 'name' not in data:
            return jsonify({'error': 'Missing id, username, or name field'}), 400

        with db_session() as session:
            user = session.query(User).get(data['id'])
            if user:
                user.username = data['username']
                user.password = data.get('password', user.password)  # 保持原密码不变
                user.name = data['name']
                user.phone = data.get('phone', user.phone)
                user.user_type = data.get('user_type', user.user_type)
                user.UserDepartment_name = data.get('UserDepartment_name', user.UserDepartment_name)
                session.commit()
                return jsonify({'id': user.id, 'username': user.username, 'name': user.name})
            else:
                return jsonify({'error': 'User not found'}), 404

    elif request.method == 'DELETE':
        data = request.json
        if 'id' not in data:
            return jsonify({'error': 'Missing id field'}), 400

        with db_session() as session:
            user = session.query(User).get(data['id'])
            if user:
                session.delete(user)
                session.commit()
                return jsonify({'message': 'User deleted'})
            else:
                return jsonify({'error': 'User not found'}), 404


# todo 供应商 管理
@admin_bp.route('/Supplier', methods=['GET', 'POST', 'PUT', 'DELETE'])
def supplier():
    if request.method == 'GET':
        with db_session() as session:
            res = session.query(Supplier).all()
            suppliers = [i.as_dict() for i in res]
        return jsonify(suppliers)

    elif request.method == 'POST':
        data = request.json
        if 'name' not in data:
            return jsonify({'error': 'Missing name field'}), 400
        if 'number' not in data:
            return jsonify({'error': 'Missing number field'}), 400

        # 检查是否存在相同编号的供应商
        with db_session() as session:
            existing_supplier = session.query(Supplier).filter_by(number=data['number']).first()
            if existing_supplier:
                return jsonify({'error': 'Supplier with this number already exists'}), 409

            new_supplier = Supplier(number=data.get('number'), name=data['name'], phone=data.get('phone'),
                                    address=data.get('address'))
            session.add(new_supplier)
            session.commit()
            session.refresh(new_supplier)

        return jsonify({'id': new_supplier.id, 'name': new_supplier.name}), 201


    elif request.method == 'PUT':
        data = request.json
        if 'id' not in data or 'name' not in data:
            return jsonify({'error': 'Missing id or name field'}), 400

        with db_session() as session:
            supplier = session.query(Supplier).get(data['id'])
            if supplier:
                supplier.number = data.get('number', supplier.number)
                supplier.name = data['name']
                supplier.phone = data.get('phone', supplier.phone)
                supplier.address = data.get('address', supplier.address)
                session.commit()
                return jsonify({'id': supplier.id, 'name': supplier.name})
            else:
                return jsonify({'error': 'Supplier not found'}), 404

    elif request.method == 'DELETE':
        data = request.json
        if 'id' not in data:
            return jsonify({'error': 'Missing id field'}), 400

        with db_session() as session:
            supplier = session.query(Supplier).get(data['id'])
            if supplier:
                session.delete(supplier)
                session.commit()
                return jsonify({'message': 'Supplier deleted'})
            else:
                return jsonify({'error': 'Supplier not found'}), 404


# todo 材料信息 管理
@admin_bp.route('/Material', methods=['GET', 'POST', 'PUT', 'DELETE'])
def material():
    if request.method == 'GET':
        with db_session() as session:
            res = session.query(Material).all()
            materials = [i.as_dict() for i in res]
        return jsonify(materials)

    elif request.method == 'POST':
        data = request.json
        if 'name' not in data or 'Supplier_id' not in data:
            return jsonify({'error': 'Missing name or Supplier_id field'}), 400
        new_material = Material(
            name=data['name'],
            specifications=data.get('specifications'),
            unit=data.get('unit'),
            price=data.get('price'),
            Supplier_id=data['Supplier_id'],
            secure_days=data.get('secure_days'),
            secure_number=data.get('secure_number')
        )
        with db_session() as session:
            session.add(new_material)
            session.commit()
            session.refresh(new_material)
        return jsonify({'id': new_material.id, 'name': new_material.name}), 201

    elif request.method == 'PUT':
        data = request.json
        if 'id' not in data:
            return jsonify({'error': 'Missing id field'}), 400

        with db_session() as session:
            material = session.query(Material).get(data['id'])
            if material:
                material.name = data.get('name', material.name)
                material.specifications = data.get('specifications', material.specifications)
                material.unit = data.get('unit', material.unit)
                material.price = data.get('price', material.price)
                material.Supplier_id = data.get('Supplier_id', material.Supplier_id)
                material.secure_days = data.get('secure_days', material.secure_days)
                material.secure_number = data.get('secure_number', material.secure_number)
                session.commit()
                return jsonify({'id': material.id, 'name': material.name})
            else:
                return jsonify({'error': 'Material not found'}), 404

    elif request.method == 'DELETE':
        data = request.json
        if 'id' not in data:
            return jsonify({'error': 'Missing id field'}), 400

        with db_session() as session:
            material = session.query(Material).get(data['id'])
            if material:
                session.delete(material)
                session.commit()
                return jsonify({'message': 'Material deleted'})
            else:
                return jsonify({'error': 'Material not found'}), 404


@admin_bp.route('/MaterialHistory', methods=['GET'])
def MaterialHistory_api():
    if request.method == 'GET':
        with db_session() as session:
            res = session.query(MaterialHistory).all()
            materials = [i.as_dict() for i in res]
        return jsonify(materials)

# todo 材料数量 管理
@admin_bp.route('/Material/stock', methods=['POST'])
def stock_material():
    data = request.json
    if 'id' not in data or 'stockQuantity' not in data:
        return jsonify({'error': 'Missing id or stockQuantity field'}), 400

    with db_session() as session:
        material = session.query(Material).get(data['id'])
        if material:
            # 更新库存数量
            current_number = int(material.number)
            stock_quantity = int(data['stockQuantity'])
            material.number = current_number + stock_quantity

            # 创建历史记录
            history_log = MaterialHistory(
                name=material.name,
                specifications=material.specifications,
                unit=material.unit,
                price=material.price,
                Supplier_id=material.Supplier_id,
                number=str(stock_quantity),  # 记录本次入库数量
                type='入库',  # 记录类型
            )
            session.add(history_log)  # 添加到会话

            session.commit()  # 提交事务
            return jsonify({'message': 'Stock updated successfully', 'new_number': material.number})
        else:
            return jsonify({'error': 'Material not found'}), 404
