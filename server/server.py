# -*- coding: utf-8 -*-
import pymysql
from flask import Flask, request, jsonify
from flask_cors import CORS

# 数据库连接
db = pymysql.connect("127.0.0.1", "root", "MySQL123456", "softwareb")
cursor = db.cursor()

# 后端服务启动
app = Flask(__name__)
CORS(app, resources=r'/*')


@app.route('/login/list', methods=['POST'])
def login_list():
    if request.method == "POST":
        cursor.execute("select id,username,role,ctime from login")
        data = cursor.fetchall()
        temp = {}
        result = []
        if (data != None):
            for i in data:
                temp["id"] = i[0]
                temp["username"] = i[1]
                temp["role"] = i[2]
                temp["ctime"] = i[3]
                result.append(temp.copy())  # 特别注意要用copy，否则只是内存的引用
            print("result:", len(data))
            return jsonify(result)
        else:
            print("result: NULL")
            return jsonify([])


@app.route('/app/add', methods=['POST'])
def login_add():
    if request.method == "POST":
        app_name = request.form.get("app_name")
        category = request.form.get("category")
        try:
            cursor.execute("insert into app(app_name, app_category) values (\""
                           + str(app_name) + "\",\"" + str(category) + "\")")
            db.commit()  # 提交，使操作生效
            print("add a new app successfully!")
            return "1"
        except Exception as e:
            print("add a new app failed:", e)
            db.rollback()  # 发生错误就回滚
            return "-1"


@app.route('/app_temp/update', methods=['POST'])
def login_add():
    if request.method == "POST":
        app_name = request.form.get("app_name")
        safe_bool = request.form.get("safe")
        try:
            if (safe_bool == '1'):
                cursor.execute('update app_temp set safe_cnt = safe_cnt + 1 where app_temp.app_name =' + str(app_name))
            cursor.execute('update app_temp set sum = sum + 1 where app_temp.app_name =' + str(app_name))
            db.commit()  # 提交，使操作生效
            print("add a new app successfully!")
            return "1"
        except Exception as e:
            print("add a new app failed:", e)
            db.rollback()  # 发生错误就回滚
            return "-1"


@app.route('/category/add', methods=['POST'])
def login_add():
    if request.method == "POST":
        category = request.form.get("category")
        p_location = request.form.get("p_location")
        try:
            cursor.execute("insert into app(category, p_location) values (\""
                           + str(category) + "\",\"" + str(p_location) + "\")")
            db.commit()  # 提交，使操作生效
            print("add a new category successfully!")
            return "1"
        except Exception as e:
            print("add a new category failed:", e)
            db.rollback()  # 发生错误就回滚
            return "-1"


@app.route('/favorite/count', methods=['POST'])
def favorite_count():
    if request.method == "POST":
        id = request.form.get("id")
        try:
            cursor.execute("update favorite set count=count+1 where id=" + str(id))
            db.commit()
            print("count successfully!")
            return "1"
        except Exception as e:
            print("count failed:", e)
            db.rollback()  # 发生错误就回滚
            return "-1"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
    db.close()
    print("Good bye!")
