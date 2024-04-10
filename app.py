from flask import Flask, jsonify, request
from flask_cors import CORS
import pymysql
from pymysql.cursors import DictCursor

app = Flask(__name__)
CORS(app)  # 允许所有域的跨域请求，即允许前端的 3000 端口访问后端的 5000 端口


# 连接 MySQL 函数
def conn_mysql():
    return pymysql.Connect(
        host="localhost",
        port=3306,
        user="root",
        password="123456",
        charset="utf8",
        database="db_test"
    )


# 断开 MySQL 函数
def close_conn_mysql(conn, cursor):
    cursor.close()
    conn.close()


# 获取数据
def get_data():
    conn = conn_mysql()
    cursor = conn.cursor(cursor=DictCursor)
    cursor.execute("select * from tb_test")
    result = cursor.fetchall()
    close_conn_mysql(conn, cursor)
    return result  # 返回获取结果


# 注册
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': '用户名或密码不能为空'})

    users = get_data()
    for user in users:
        if user['username'] == username:
            return jsonify({'message': '用户名已存在'})

    conn = conn_mysql()
    cursor = conn.cursor(cursor=DictCursor)
    sql = "insert into tb_test(username, password) values(%s, %s)"
    cursor.execute(sql, [username, password])
    conn.commit()
    close_conn_mysql(conn, cursor)
    return jsonify({'message': '注册成功'})


# 登录
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': '用户名或密码不能为空'})

    users = get_data()
    # print(users)
    for user in users:
        if username == user['username'] and password == user['password']:
            return jsonify({'message': '登录成功', 'user': user})

    return jsonify({'message': '用户名或密码错误'})


# 查看用户信息
@app.route('/user_info', methods=['GET'])
def user_info():
    users = get_data()
    return jsonify({'users': users})


if __name__ == '__main__':
    app.run(debug=True)