from flask import Flask, request, jsonify
import mysql.connector

# 创建 Flask 应用 666
app = Flask(__name__)

# 配置数据库连接
db = mysql.connector.connect(
    host="123.57.246.217",           # 数据库主机
    user="shenmi",     # 数据库用户名
    password="FiEyF3AKRKBKtm7y", # 数据库密码
    database="shenmi"           # 数据库名称
)

# 测试数据库连接
@app.route('/test_db')
def test_db():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM company")  # 查询所有公司
    result = cursor.fetchall()
    return jsonify(result)


# 添加公司接口
@app.route('/add_company', methods=['POST'])
def add_company():
    company_name = request.json.get('name')
    company_address = request.json.get('address')
    company_phone = request.json.get('phone')
    company_email = request.json.get('email')

    cursor = db.cursor()
    cursor.execute("INSERT INTO company (name, address, phone, email) VALUES (%s, %s, %s, %s)",
                   (company_name, company_address, company_phone, company_email))
    db.commit()  # 提交事务

    return jsonify({"message": "公司已添加!"}), 201


# 获取公司信息接口
@app.route('/get_companies', methods=['GET'])
def get_companies():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM company")
    result = cursor.fetchall()
    return jsonify(result)


# 添加用户接口
@app.route('/add_user', methods=['POST'])
def add_user():
    company_id = request.json.get('company_id')
    username = request.json.get('username')
    password = request.json.get('password')  # 这里需要加密密码，建议使用 bcrypt 或 hashlib
    cursor = db.cursor()
    cursor.execute("INSERT INTO user (company_id, username, password) VALUES (%s, %s, %s)",
                   (company_id, username, password))
    db.commit()
    return jsonify({"message": "用户已添加!"}), 201


# 登录接口
@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')  # 用户输入的密码

    cursor = db.cursor()
    cursor.execute("SELECT * FROM user WHERE username = %s", (username,))
    user = cursor.fetchone()

    if user and user[2] == password:  # 比对存储的密码（示例中没有加密）
        return jsonify({"message": "登录成功!"})
    else:
        return jsonify({"message": "用户名或密码错误!"}), 401


# 根路由
@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run(debug=True)  # 启动 Flask 开发服务器
